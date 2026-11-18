# ARCHITECTURE.md — USB OBS 촬영 컨트롤러

## 1. 부품 선정 이유
- **Raspberry Pi Pico (RP2040)**: Micro USB 내장, USB CDC 시리얼 기본 지원, 3.3V I2C, 공식 문서·핀맵·Thonny+MicroPython 생태계 확보. 별도 USB-시리얼 칩 불필요.
- **SSD1306 0.96" I2C OLED**: 3.3V 동작, Pico I2C0 직결, MicroPython `ssd1306` 드라이버 표준. 저전류(~20mA).
- **택트 버튼 3개 + 빨간 LED**: GPIO 풀업 + GND 방식으로 디바운스 처리 용이. LED는 GPIO 직결(저항 경유).
- **Micro USB**: Pico 온보드 커넥터 사용. 별도 커넥터 부품 없음.

## 2. 통신 구조
```
[Pico firmware] --USB CDC 115200 JSON-lines--> [host bridge.py] --OBS-WebSocket v5--> [OBS]
```

### 2.1 선정 이유
- 펌웨어가 OBS-WebSocket을 직접 처리하지 않음: Pico에 TCP/WS 스택·인증·TLS 부담을 주지 않고, USB CDC 텍스트 1줄이면 되므로 펌웨어가 단순·견고해짐.
- host 파이썬 브리지가 시리얼↔OBS-WebSocket(v5) 변환: `obs-websocket-py` 또는 순수 `websocket-client` 중 택1. v5 프로토콜(`StartStopRecord`, `GetRecordStatus`, `SetCurrentProgramScene`) 사용.
- LED/시간 동기: host가 `GetRecordStatus` 폴링(약 1Hz)으로 실제 상태를 받아 `{"rec":true/false,"time":sec}`를 펌웨어에 푸시. LED는 이 수신값으로만 점등 → OBS 실제 상태 반영 보장.

### 2.2 프로토콜 (JSON + `\n`)
- Device→Host: `{"cmd":"rec_toggle","seq":12}`, `{"cmd":"set_scene","name":"Scene1","seq":13}`, `{"event":"hello","fw":"1.0"}`
- Host→Device: `{"rec":true,"time":83}`, `{"rec":false,"time":0}`, `{"link":"ok"}`
- `seq`: 단조 증가 정수. host는 직전 seq 이하 패킷 무시 → 중복명령 방지. 부팅 시 `hello`.

## 3. 상태/에러 처리
- 디바운스 20ms (펌웨어 인터럽트+타이머).
- USB 단절 시 OLED `NO-LINK`, LED 소등, 재접속 시 `hello` 재전송 후 상태 재요청.
- OBS 단절 시 OLED `OFFLINE`, LED 소등, host가 2초 간격 재접속.
- 중복 시리얼 라인/깨진 JSON은 무시하고 카운터만 증가.

## 4. 전원
USB 5V → Pico 내장 LDO → 3.3V периф러л. 총 예산 500mA 이내 (WIRING.md).
