# VERIFICATION.md — 검증 로그 + 제한 + 인수테스트

## 실행한 검증 (2026-11-18, python 3.9.6)
1. `python3 -m py_compile firmware/main.py host/bridge.py` → **COMPILE_OK** (CPython 문법 검사. MicroPython 전용 `machine`/`ssd1306` import는 실기에서만 검증).
2. `python3 host/bridge.py --dry-run` → 로그:
```
[bridge] dry-run start (mock OBS + mock serial)
[bridge] rx {"cmd": "rec_toggle", "seq": 1}
[bridge] MOCK StartStopRecord -> rec=True
[bridge] tx {"rec": true, "time": 0}
[bridge] rx {"cmd": "set_scene", "name": "Scene1", "seq": 2}
[bridge] MOCK SetCurrentProgramScene Scene1
[bridge] tx {"rec": true, "time": 0}
[bridge] rx {"cmd": "set_scene", "name": "Scene2", "seq": 3}
[bridge] MOCK SetCurrentProgramScene Scene2
[bridge] tx {"rec": true, "time": 0}
[bridge] ignore dup seq=3
[bridge] rx {"cmd": "rec_toggle", "seq": 4}
[bridge] MOCK StartStopRecord -> rec=False
[bridge] tx {"rec": false, "time": 0}
[bridge] dry-run done
```
중복 seq=3 무시 확인 → 중복명령 방지 동작.
3. `case.scad` 문법 육안 확인 (OpenSCAD 미설치로 렌더 검증 불가).
4. `preview/index.html` → `1-controller-3d.html` 복사 확인 (브라우저 렌더 미실행, CDN 필요).

## 실물 없이 불가 항목 (미검증)
- Pico 실기 MicroPython 동작, USB CDC 인식, OLED I2C 표시, 버튼 디바운스 실측.
- 실제 OBS-WebSocket v5 연동 (URL/비밀번호/OBS 버전별 상이), GetRecordStatus 폴링 주기 실측.
- 케이스 STL 출력 적합성·간섭·공차 (슬라이서/실측 없음).
- USB 전원 실측 (계산상 122mA, 계측기 없음).

## 인수테스트표
| 항목 | 방법 | 결과 |
|------|------|------|
| REC 토글 모의 | --dry-run | PASS (로그) |
| 중복 seq 무시 | --dry-run seq=3 중복 | PASS |
| py_compile | 위 1 | PASS (CPython 문법 한정) |
| 실기/OBS/출력물 | — | NOT TESTED (위 목록) |
