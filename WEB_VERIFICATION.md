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
