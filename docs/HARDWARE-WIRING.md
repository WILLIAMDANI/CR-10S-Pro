# Hardware Wiring — CR-10S Pro / SKR Mini E3 V3.0

Source of truth: the user's own hand-annotated wiring schematic (photos of the
actual build, each wire traced and labeled), confirmed 2026-09-29. This
resolved `docs/BUILD-LOG.md` Question 2 — see that entry for the full story.

| Component | SKR Mini E3 V3.0 connection |
|---|---|
| X-axis motor | XM |
| Y-axis motor | YM |
| Z-axis motor 1 of 2 | ZAM |
| Z-axis motor 2 of 2 | ZBM |
| Extruder motor | EM |
| X-axis endstop | X-STOP |
| Y-axis endstop | Y-STOP |
| Z probe (inductive sensor) | **E0-STOP** |
| Hotend heater cartridge | E0 |
| Hotend thermistor | TH0 |
| Heated bed | HB |
| Heated-bed thermistor | THB |
| Part-cooling fan | FAN0 |
| Hotend heatbreak fan | FAN1 |
| SKR board/electronics fan | FAN2 |
| BTT TFT35 E3 V3.0.1 touchscreen | TFT header |
| Speaker/buzzer | Built into the TFT35 assembly — not a separate mainboard connection, and not driven by Marlin's `M300`/`BEEPER_PIN` |

**Z-STOP (PC2) is confirmed physically unused** — the schematic explicitly
marks the breakout pins that would carry it as "Not Used." This matches
`docs/MASTER-BRIEF-FOR-CLAUDE-CODE.md` §2/§3: there is no Z endstop switch on this
machine; Z homes entirely off the probe on E0-STOP.

This table matches the firmware as configured — no pin changes were made as a
result of this schematic. It documents wiring only, not firmware settings;
see `docs/MASTER-BRIEF-FOR-CLAUDE-CODE.md` §5 for what the firmware itself does
and why.
