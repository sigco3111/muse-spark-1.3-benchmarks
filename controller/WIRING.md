# WIRING.md — 배선표 + 전원예산

## 1. 배선표 (Pico 기준)
| 신호 | Pico 핀 | 상대 | 비고 |
|------|---------|------|------|
| REC 버튼 | GP13 | GND | 내부 풀업, 20ms 디바운스 |
| Scene1 버튼 | GP14 | GND | 내부 풀업 |
| Scene2 버튼 | GP15 | GND | 내부 풀업 |
| 빨간 LED + | GP16 via 220Ω | — | LED 애노드→저항→GP16, 캐소드→GND |
| OLED SDA | GP0 (I2C0 SDA) | OLED SDA | 3.3V 로직 |
| OLED SCL | GP1 (I2C0 SCL) | OLED SCL | 400kHz |
| OLED VCC | 3V3(OUT) | OLED VCC | 3.3V |
| OLED GND | GND | OLED GND | 공통 GND |
| USB | Micro USB 온보드 | PC | CDC 115200bps |

핀맵 출처: https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html

## 2. 전원예산 (USB 5V 500mA 이내)
| 항목 | 전압 | 전류(최대 가정) |
|------|------|-----------------|
| Pico 본체 (RP2040+ LDO) | 5V 입력 | 90mA |
| SSD1306 OLED | 3.3V | 25mA |
| 빨간 LED (220Ω → 약 6mA) | GPIO | 6mA |
| 버튼 3개 (풀업 누설) | — | 1mA |
| **합계** | | **약 122mA < 500mA 여유** |

계산 근거: Pico datasheet 활성 전류 ~90mA 가정, OLED 제조사 스펙 ~20–25mA, LED (3.3−2.0)V/220Ω≈6mA.
