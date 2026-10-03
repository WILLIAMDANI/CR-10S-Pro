# CR-10S Pro — SKR Mini E3 V3.0 Conversion

Marlin **2.1.2.8** firmware for a stock **Creality CR-10S Pro**, converted from
its original controller to a **BIGTREETECH SKR Mini E3 V3.0** mainboard
(STM32G0B1RET6) with a **BIGTREETECH TFT35 E3 V3.0.1** touchscreen running as
a serial host.

## Status

> ⚠️ **Work in progress. Compiles cleanly. NOT yet verified on hardware.**
> Pending physical calibration: probe offset, E-steps, X and E motor
> directions, probe polarity.

This is not ready to share or use on a printer as-is. See
[`firmware/README.md`](firmware/README.md) for the current build table and
[`docs/BUILD-LOG.md`](docs/BUILD-LOG.md) for the full history of what's been
verified, changed, and is still open.

## Hardware

| | |
|---|---|
| Frame | Creality CR-10S Pro, 300×300×400mm |
| Mainboard | BIGTREETECH SKR Mini E3 V3.0 (STM32G0B1RET6), 4× onboard TMC2209 |
| Display | BIGTREETECH TFT35 E3 V3.0.1 (serial host, not a native Marlin display) |
| Z axis | Two motors, one driver, wired in parallel |
| Z probe | Fixed inductive proximity sensor, wired to E0-STOP |

Full component-to-connector table, sourced from the actual wiring: see
[`docs/HARDWARE-WIRING.md`](docs/HARDWARE-WIRING.md).

## What's customized

This is upstream Marlin `2.1.2.8` with three files deliberately modified for
this hardware. Each is explained in full in
[`docs/MASTER-BRIEF-FOR-CLAUDE-CODE.md`](docs/MASTER-BRIEF-FOR-CLAUDE-CODE.md) §5:

- [`Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h`](Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h) — Z probe moved to E0-STOP (PC15); filament-runout pin disabled (not installed, shared the same pin).
- [`Marlin/Configuration.h`](Marlin/Configuration.h) — board/driver selection, TFT serial port, probe-only Z homing, bed size, conservative commissioning accelerations.
- [`Marlin/Configuration_adv.h`](Marlin/Configuration_adv.h) — hotend auto-fan on FAN1 (critical heat-creep fix), controller fan on FAN2, doubled Z current for the parallel Z motors.

## Folder map

```
Marlin/, buildroot/, ini/, config/, docker/, platformio.ini, Makefile  — stock Marlin build tree (unmodified except the 3 files above)
docs/          — project documentation: the master brief, build log, wiring reference
firmware/      — built .bin releases, one per tested build, with a status table
TEST-SCRIPTS/  — the test case library and per-build regression run records
```

## Latest firmware

[`firmware/firmware-2026-10-03-v1.bin`](firmware/firmware-2026-10-03-v1.bin) —
status: **untested** (verified to match this repo's config; hardware test
results still being diagnosed). See [`firmware/README.md`](firmware/README.md)
for the full build table.

## Credits & License

Built on [Marlin Firmware](https://marlinfw.org/), the open-source 3D printer
firmware. Marlin is licensed under **GPL-3.0** — see [`LICENSE`](LICENSE).
This repository's project-specific documentation and test material follow the
same license as the codebase it documents.
