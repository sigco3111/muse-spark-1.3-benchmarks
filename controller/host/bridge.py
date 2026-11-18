"""Host bridge: USB CDC serial <-> OBS-WebSocket v5.
Secrets via env/args only, never in files.
Deps: pyserial, websocket-client (pure WS, obs-websocket-py optional).
"""
import argparse
import json
import os
import sys
import time

try:
    import serial
except ImportError:
    serial = None


def log(msg):
    print("[bridge] " + msg, flush=True)


class FakeOBS:
    """--dry-run mock: toggles rec, alternates scenes."""

    def __init__(self):
        self.rec = False
        self.t0 = 0

    def handle(self, cmd):
        c = cmd.get("cmd")
        if c == "rec_toggle":
            self.rec = not self.rec
            self.t0 = time.time() if self.rec else 0
            log("MOCK StartStopRecord -> rec=%s" % self.rec)
        elif c == "set_scene":
            log("MOCK SetCurrentProgramScene %s" % cmd.get("name"))

    def status(self):
        t = int(time.time() - self.t0) if self.rec else 0
        return {"rec": self.rec, "time": t}


class RealOBS:
    """Minimal OBS-WebSocket v5 client over websocket-client."""

    def __init__(self, url, password):
        import websocket
        self.ws = websocket.create_connection(url, timeout=5)
        self.password = password
        self._hello_auth = None
        # v5: read Hello, send Identify (auth optional, omitted if no password)
        hello = json.loads(self.ws.recv())
        ident = {"op": 1, "d": {"rpcVersion": 1}}
        self.ws.send(json.dumps(ident))
        self.ws.recv()  # Identified
        self.last_seq = 0

    def handle(self, cmd):
        c = cmd.get("cmd")
        if c == "rec_toggle":
            self._req("StartStopRecord", {})
        elif c == "set_scene":
            self._req("SetCurrentProgramScene", {"sceneName": cmd.get("name")})

    def _req(self, rtype, data):
        self.last_seq += 1
        rid = str(self.last_seq)
        self.ws.send(json.dumps({"op": 6, "d": {"requestType": rtype,
                                                "requestId": rid,
                                                "requestData": data}}))
        self.ws.recv()  # response (ignore detail here)

    def status(self):
        self.last_seq += 1
        rid = str(self.last_seq)
        self.ws.send(json.dumps({"op": 6, "d": {"requestType": "GetRecordStatus",
                                                "requestId": rid}}))
        resp = json.loads(self.ws.recv())
        d = resp.get("d", {}).get("responseData", {})
        secs = 0
        try:
            ms = d.get("outputDuration", 0)
            secs = int(ms / 1000)
        except (TypeError, ValueError):
            pass
        return {"rec": bool(d.get("outputActive", False)), "time": secs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default=os.environ.get("CTRL_PORT", "/dev/ttyACM0"))
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--obs-url", default=os.environ.get("OBS_URL", "ws://localhost:4455"))
    ap.add_argument("--obs-password", default=os.environ.get("OBS_PASSWORD", ""))
    ap.add_argument("--dry-run", action="store_true", help="mock OBS, mock serial input")
    args = ap.parse_args()

    last_seq = 0
    if args.dry_run:
        obs = FakeOBS()
        log("dry-run start (mock OBS + mock serial)")
        demo = [{"cmd": "rec_toggle", "seq": 1},
                {"cmd": "set_scene", "name": "Scene1", "seq": 2},
                {"cmd": "set_scene", "name": "Scene2", "seq": 3},
                {"cmd": "set_scene", "name": "Scene1", "seq": 3},  # dup -> ignore
                {"cmd": "rec_toggle", "seq": 4}]
        for pkt in demo:
            if pkt["seq"] <= last_seq:
                log("ignore dup seq=%s" % pkt["seq"])
                continue
            last_seq = pkt["seq"]
            log("rx %s" % json.dumps(pkt))
            obs.handle(pkt)
            st = obs.status()
            log("tx %s" % json.dumps(st))
            time.sleep(0.2)
        log("dry-run done")
        return

    if serial is None:
        print("need pyserial: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(2)
    obs = RealOBS(args.obs_url, args.obs_password)
    log("OBS connected, opening %s" % args.port)
    while True:
        try:
            ser = serial.Serial(args.port, args.baud, timeout=1)
            log("serial open, sending link ok")
            ser.write(b'{"link":"ok"}\n')
            while True:
                line = ser.readline().decode("utf-8", "ignore").strip()
                if line:
                    try:
                        pkt = json.loads(line)
                    except ValueError:
                        continue
                    if pkt.get("seq", 0) <= last_seq and "cmd" in pkt:
                        continue  # dup
                    last_seq = pkt.get("seq", last_seq)
                    if "cmd" in pkt:
                        obs.handle(pkt)
                try:
                    ser.write((json.dumps(obs.status()) + "\n").encode())
                except Exception:
                    pass
                time.sleep(1.0)  # ~1Hz status poll
        except Exception as e:
            log("reconnect in 2s: %s" % e)
            time.sleep(2)


if __name__ == "__main__":
    main()
