# README — USB OBS 촬영 컨트롤러

## 조립
1. WIRING.md 배선표대로 브레드보드에 Pico–OLED–버튼3–LED(220Ω) 연결.
2. enclosure/case.scad 치수 가정 확인 (Pico 51x21mm, OLED 27x27mm, M3, 공차 0.2mm).
3. schematic/wiring.svg는 전기 CAD가 아닌 배선 그림.

## 플래시
firmware/README.md (Thonny) 참고. `firmware/main.py` + `ssd1306.py` 저장.

## 실행
```
pip install -r host/requirements.txt
python3 host/bridge.py --dry-run   # 모의 확인
CTRL_PORT=/dev/ttyACM0 OBS_URL=ws://localhost:4455 OBS_PASSWORD=... python3 host/bridge.py
```

## 미리보기
`preview/index.html` (시뮬레이션 명시, Three.js CDN 필요) = 최상위 `1-controller-3d.html` 복사본.
