"""USB OBS controller firmware (MicroPython, Raspberry Pi Pico).
USB CDC serial JSON-lines. Buttons -> host, host pushes actual REC state.
LED lights ONLY on host-reported rec state, never directly from button.
"""
import sys
import json
import time

try:
    from machine import Pin, I2C
    import ssd1306
    ON_DEVICE = True
except ImportError:
    ON_DEVICE = False  # PC py_compile check

DEBOUNCE_MS = 20
UART_BAUD = 115200

BTN_REC = 13
BTN_S1 = 14
BTN_S2 = 15
LED_PIN = 16

seq = 0
rec_state = False
rec_time = 0
link_ok = False
last_rx_ms = 0


def now_ms():
    if ON_DEVICE:
        return time.ticks_ms()
    return int(time.time() * 1000)


def send(obj):
    sys.stdout.write(json.dumps(obj) + "\n")


def fmt_time(s):
    return "%02d:%02d" % (s // 60, s % 60)


def setup():
    global buttons, led, oled
    if not ON_DEVICE:
        return
    buttons = {}
    for pin, name in ((BTN_REC, "rec"), (BTN_S1, "s1"), (BTN_S2, "s2")):
        buttons[name] = {"pin": Pin(pin, Pin.IN, Pin.PULL_UP),
                         "last": 1, "t": 0, "fired": False}
    led = Pin(LED_PIN, Pin.OUT)
    led.value(0)
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    draw()


def draw():
    if not ON_DEVICE:
        return
    oled.fill(0)
    oled.text("OBS CTRL", 0, 0)
    if not link_ok:
        oled.text("NO-LINK", 0, 20)
    elif rec_state:
        oled.text("REC " + fmt_time(rec_time), 0, 20)
    else:
        oled.text("IDLE", 0, 20)
    oled.text("R S1 S2", 0, 50)
    oled.show()


def poll_buttons():
    global seq
    if not ON_DEVICE:
        return
    t = now_ms()
    for name, b in buttons.items():
        v = b["pin"].value()
        if v != b["last"]:
            b["last"] = v
            b["t"] = t
        elif v == 0 and not b["fired"] and (t - b["t"]) >= DEBOUNCE_MS:
            b["fired"] = True
            seq += 1
            if name == "rec":
                send({"cmd": "rec_toggle", "seq": seq})
            elif name == "s1":
                send({"cmd": "set_scene", "name": "Scene1", "seq": seq})
            else:
                send({"cmd": "set_scene", "name": "Scene2", "seq": seq})
        elif v == 1:
            b["fired"] = False


def handle_line(line):
    global rec_state, rec_time, link_ok, last_rx_ms
    try:
        msg = json.loads(line)
    except ValueError:
        return  # broken line: ignore
    if not isinstance(msg, dict):
        return
    if "rec" in msg:
        rec_state = bool(msg["rec"])
        link_ok = True
        last_rx_ms = now_ms()
        if ON_DEVICE:
            led.value(1 if rec_state else 0)
    if "time" in msg:
        try:
            rec_time = int(msg["time"])
        except (ValueError, TypeError):
            pass
    if msg.get("link") == "ok":
        link_ok = True
        last_rx_ms = now_ms()
    if ON_DEVICE:
        draw()


def main():
    setup()
    send({"event": "hello", "fw": "1.0"})
    buf = ""
    if not ON_DEVICE:
        return
    import select
    poller = select.poll()
    poller.register(sys.stdin, select.POLLIN)
    while True:
        poll_buttons()
        for _, ev in poller.poll(10):
            chunk = sys.stdin.read(1)
            if chunk:
                if chunk == "\n":
                    if buf.strip():
                        handle_line(buf.strip())
                    buf = ""
                else:
                    buf += chunk
        # link timeout 3s
        if link_ok and (now_ms() - last_rx_ms) > 3000:
            link_ok = False
            led.value(0)
            draw()


if __name__ == "__main__":
    main()
