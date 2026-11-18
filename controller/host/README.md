# host README — 브리지 실행

## 설치
```
pip install -r requirements.txt
```

## 실행
```
# 모의 OBS (하드웨어/OBS 없이 동작 확인)
python3 bridge.py --dry-run

# 실제 OBS (OBS 설정 → WebSocket 서버 켜기, 포트 4455)
export OBS_URL="ws://localhost:4455" OBS_PASSWORD="..." CTRL_PORT="/dev/ttyACM0"
python3 bridge.py
```
인증정보는 env/args로만 전달. 파일에 기록 금지.
