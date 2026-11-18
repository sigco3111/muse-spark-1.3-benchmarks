# Muse Spark 1.3 Benchmarks

muse-spark-1.3이 같은 다섯 과제를 구현한 결과를 기록하는 저장소입니다. 원본 저장소(`instinct-benchmarks`)의 구조와 리드미에 보존된 원문 메타프롬프트만을 기준으로 독립 구현했으며, 원본의 결과 수치·스크린샷은 참고하지 않았습니다.

[웹에서 결과 바로 보기](https://sigco3111.github.io/muse-spark-1.3-benchmarks/) · [USB OBS 컨트롤러 3D](https://sigco3111.github.io/muse-spark-1.3-benchmarks/1-controller-3d.html)

## 비교 기록

| 항목 | 이 저장소 |
| --- | --- |
| 실행 주체 | muse-spark-1.3 |
| 과제 출처 | 유튜버 코드팩토리의 메타프롬프트 (원문 `ORIGINAL_PROMPTS.txt`에 그대로 보존) |
| 평가 기준 | 기능 충족·화면 품질·재현성·검증 증거·미검증 항목 |
| 실행 성격 | 단일 구현. 사용자 피드백 반영 수정 없음 |

다른 실행과 비교할 때는 원문 해시, 지정 모델·effort, 실행 날짜, 시간/비용 제한, 수정 라운드를 함께 기록해야 합니다. 값이 없으면 점수나 완료로 채우지 않습니다.

## 결과물

| 과제 | 파일 | 현재 상태 |
| --- | --- | --- |
| 경복궁 근정전 브릭 모션 | [palace.html](palace.html) | 32초 타임라인·시간 슬라이더·파트별 실측 집계 구현 (브라우저 렌더 미확인) |
| 한강시 3인칭 게임 | [hangang-city.html](hangang-city.html) | 걷기·차량·AI·미션 3종·수배·미니맵·시간순환 구현 (플레이 완주 미검증) |
| 모델 소개 스크롤 페이지 | [model-intro.html](model-intro.html) | 입자 구름 6장면 모핑·2테마·로컬 질문 UI (수치는 자리표시자) |
| 을지로 인쇄소 단편 | [웹 읽기](novel.html) · [원고](novel.md) | 제목·5장면 구성·본문 완성, 본문 공백 제외 약 10,122자 |
| USB OBS 촬영 컨트롤러 | [3D 웹에서 바로 조작](https://sigco3111.github.io/muse-spark-1.3-benchmarks/1-controller-3d.html) | 설계·펌웨어·브리지·CAD원본·시뮬레이션 미리보기, 실물 미검증 |

## 실행

각 HTML을 Chrome/Edge/Safari 등 최신 WebGL 지원 브라우저에서 여세요. `palace.html`·`hangang-city.html`은 three.js 0.170.0, 소개 페이지는 three.js 0.170.0 + GSAP/ScrollTrigger 3.12.5를 CDN에서 읽으므로 인터넷 연결이 필요합니다. 컨트롤러 미리보리(`1-controller-3d.html`)는 three.js 0.152.2 CDN을 사용합니다.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

그 뒤 `http://127.0.0.1:8000/`의 목차(`index.html`)에서 실행합니다. 별도 계정·API 키는 필요 없습니다.

## 검증과 한계

- [WEB_VERIFICATION.md](WEB_VERIFICATION.md)와 [web-checks.json](web-checks.json)에 실행한 검사를 기록했습니다. 브라우저 렌더·조작감·FPS 실측은 하지 않았습니다.
- [NOVEL_VERIFICATION.md](NOVEL_VERIFICATION.md)에 소설 분량·요건 점검을 기록했습니다.
- 컨트롤러는 [controller/VERIFICATION.md](controller/VERIFICATION.md)를 보세요. `py_compile` + host `--dry-run`만 통과했고 실물 제작·실OBS 연동은 미검증입니다.
- 소개 페이지의 성능 수치는 `{{PLACEHOLDER}}`·`—` 자리표시자이며 지어내지 않았습니다.

## 원문 메타프롬프트

전체 원문은 [ORIGINAL_PROMPTS.txt](ORIGINAL_PROMPTS.txt)에 보존합니다. 맞춤법과 자리표시자(`{{MODEL_NAME}}`, `{{EFFORT}}`, `{{TASK_DIR}}`)를 고치지 않은 원문이며, 이 저장소에서는 `{{MODEL_NAME}}` 자리에 `muse-spark-1.3`을 적용해 구현했습니다.
