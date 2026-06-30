# OPRobots

Documentación técnica del equipo OPRobots de robótica.

## Boards

- [OPRcontrolFOC](OPRcontrolFOC/) — Placa de control FOC (Field-Oriented Control) para 2 motores brushless con STM32F103, encoders magnéticos AS5600, conmutación sinusoidal y lazo PI de velocidad

## Demos

- [CRSF-demo](CRSF-demo/) — Demo de recepción y decodificación del protocolo CRSF (CrossFire) con receptor ELRS y STM32F401
- [H3LIS331-demo](H3LIS331-demo/) — Demo del acelerómetro de alta G H3LIS331DL (±400g, SPI) con STM32F401 y cinemática MeltyBrain
- [SRAM-demo](SRAM-demo/) — Demo de ring buffer heterogéneo en SRAM externa 23AA04M (512 KB, SPI) con STM32F401

## Módulos

- [IRStart](IRStart/) — Sistema de arranque por infrarrojos multi-protocolo (RC5, NEC, SIRC) con mando ESP32-C3 y receptor ATtiny13/85 para competiciones de robótica
- [IRTimer](IRTimer/) — Cronómetro inalámbrico dual-mode (Micromouse + LineFollower) con ESP32-C3, pantalla TFT, WiFi/ESP-NOW y sincronización IR

## Robots

- [FujitoraBot2](FujitoraBot2/) — Robot linefollower de alto rendimiento con STM32F4, 24 sensores IR, motores brushless y control PID en cascada
- [UltiBot](UltiBot/) — Robot de minisumo con arquitectura dual-MCU (STM32F4 + STM32F1), 6 sensores SHARP GP2Y0E03, motores brushless con control FOC, y 3 estrategias de combate
- [ZoroBot3](ZoroBot3/) — Robot micromouse de altas prestaciones con STM32F4, encoders magnéticos, 4 sensores IR y ventilador de succión. 8 medallas de oro en competiciones internacionales.

*Más robots próximamente...*

---

Visita nuestra web: [OPRobots.org](https://oprobots.org)
