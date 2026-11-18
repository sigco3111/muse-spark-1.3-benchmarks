# firmware README — Thonny 플래시 절차

1. Pico에 MicroPython UF2 설치 (공식: https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
2. `ssd1306.py` 드라이버를 Pico에 복사 (MicroPython 공식 드라이버).
3. Thonny → 인터프리터: MicroPython (Raspberry Pi Pico).
4. `main.py`를 열어 Pico에 `main.py` 이름으로 저장.
5. 배선(WIRING.md) 연결 후 USB 재연결 → OLED에 IDLE/NO-LINK 표시.
6. host 브리지(`../host/README` 참고) 실행 후 버튼 동작 확인.
