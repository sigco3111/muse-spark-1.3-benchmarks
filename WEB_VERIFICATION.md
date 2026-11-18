# WEB_VERIFICATION.md — 웹 3종 + 컨트롤러 미리보기 검증

실행일: 2026-11-19 · 실행 주체: muse-spark-1.3 · 환경: macOS, python 3.9.6, node v26.11.1

## 실행한 검사

| # | 대상 | 검사 | 결과 |
|---|------|------|------|
| W1 | palace.html | 파일 존재 + three.js 0.170.0 importmap + 실측 집계 코드(`length`, TOTAL/GEN/ERR) 포함 | PASS (브라우저 렌더 미실시) |
| W2 | hangang-city.html | 파일 존재 + three.js 0.170.0 importmap + HUD/미니맵 구조 포함 | PASS (플레이·FPS 미실측) |
| W3 | model-intro.html | three.js 0.170.0 + GSAP 3.12.5 CDN, 모델명 muse-spark-1.3, 수치 자리표시자(`{{PLACEHOLDER}}` 4건·`—`) | PASS (스크롤 렌더 미확인) |
| W4 | 1-controller-3d.html | controller/preview/index.html과 동일 파일, three.js 0.152.2 CDN, 시뮬레이션 명시 | PASS (브라우저 렌더 미실시) |
| W5 | web 공통 | 외부 3D/이미지 에셋 없음, 단일 HTML + CDN 구조 | PASS |

## 미검증 항목 (NOT TESTED)

- 세 HTML의 실제 브라우저 렌더·콘솔 에러·조작감·60fps 실측
- 한강시 미션 3종 완주, 수배/순찰 전체 루프
- 소개 페이지 6장면 모핑·모바일 60fps·prefers-reduced-motion 실기
- 컨트롤러 미리보기의 브라우저 렌더 (CDN 필요)

## 재현

```sh
python3 -m http.server 8000 --bind 127.0.0.1
# http://127.0.0.1:8000/ 에서 각 HTML 열기
```

## 추가 검증 — 브라우저 렌더 확인 (2026-11-19, 마무리 라운드)

배포된 Pages 주소를 데스크톱 클라우드 브라우저(Chromium)로 열어 실제 렌더를 확인하고 README의 다섯 캡처를 직접 촬영했습니다.

| 대상 | 확인 내용 |
|------|-----------|
| palace.html | 캔버스 렌더, 6단계 타임라인, 파트별 실측 집계(월대 1,071·기둥 228·공포 200·지붕 659·마당 325), 시간 슬라이더 탐색 |
| hangang-city.html | 로드, HUD(수배·미니맵·속도계), 걷기 이동, F 차량 탑승·주행(50 km/h 표시), 낮·노을·밤 전환, 한글 네온 간판 |
| model-intro.html | 히어로 장면 입자 타이포그래피 렌더, 테마 토글·SCROLL UI 표시 |
| novel.html | 제목·5장면 구성·본문 렌더 |
| 1-controller-3d.html | 시뮬레이션 패널과 3D 기판·버튼·OLED 미리보기 렌더 |

여전히 미검증: 미션 3종 완주, FPS 실측(클라우드 환경 표시값 20–24fps는 실기 성능 근거로 쓰지 않음), 모바일·prefers-reduced-motion, 실물 하드웨어·실OBS 연동.
