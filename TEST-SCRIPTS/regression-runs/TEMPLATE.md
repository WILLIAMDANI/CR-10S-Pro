<!--
Copy this file to regression-runs/<YYYY-MM-DD>-<short-sha>.md for each new
firmware build. Get the short SHA with: git rev-parse --short HEAD
Delete this comment block in the copy. Fill in every ⬜ Result line as you go
— nothing else to reference, everything you need is right here.
-->

# Regression Run — <YYYY-MM-DD> — commit `<short-sha>`

**Firmware commit:** `<full git SHA>` | **Tester:** <name> | **Date:** <date>
**What changed since last run:** <one line>

Mark each result: **PASS / FAIL / BLOCKED / NOT RUN**. Any FAIL or BLOCKED → open a GitHub Issue, put the number in Notes.

---

## A. Boot

**TC-001 — Firmware flashes via SD card**
Copy `firmware.bin` to a FAT32 SD card root → insert in mainboard slot, power on 10s → power off, check filename on a computer.
Expected: filename renamed (e.g. `FIRMWARE.CUR`).
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-002 — Correct firmware identifies itself**
Connect USB, serial terminal, send `M115`.
Expected: reports machine name "CR-10S Pro".
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-003 — TFT35 connects to mainboard**
Power on with TFT attached.
Expected: TFT reaches normal status screen, temps update live. (Note: TFT's buzzer is its own firmware, not Marlin `M300` — not wired here, no test for it.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-039 — TFT touch, encoder, and button all respond**
Tap touchscreen, turn encoder, press encoder button.
Expected: each does something on screen.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## B. Emergency Stop

**TC-004 — M112 emergency stop** — do this before any motion/heating below
With a motor enabled or a heater on, send `M112`.
Expected: immediate total stop, requires reset before resuming.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## C. Driver Health

**TC-005 — TMC2209 driver communication**
Send `M122`.
Expected: all 4 drivers (X/Y/Z/E) report OK, no overtemp warning.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-006 — Driver currents match configuration**
Send `M906`.
Expected: Z reads ~1000mA (doubled for the parallel Z motors), others plausible.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## D. Endstops & Probe (probe confirmed on E0-STOP — see docs/HARDWARE-WIRING.md)

**TC-007 — X endstop logic**
`M119`, note `x_min`. Press X endstop by hand, `M119` again.
Expected: `open` released → `TRIGGERED` pressed.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-008 — Y endstop logic**
Same as TC-007 for `y_min`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-009 — Z probe trigger logic**
`M119` with probe clear, note `z_probe`. Hold metal (must be metal — inductive sensor) to probe face, `M119` again.
Expected: `open` clear → `TRIGGERED` with metal present. No response at all → STOP, do not proceed to homing.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## E. Motor Directions (jog only — no homing yet)

**TC-010 — X direction**
Move gantry to mid-travel by hand. Jog small `+X`.
Expected: moves toward increasing X. (Fail → flip `INVERT_X_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-011 — Y direction**
Jog small `+Y`. Expected: increasing Y. (Fail → flip `INVERT_Y_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-012 — Z direction ⚠️ SAFETY: hand near power switch**
Jog small `+Z` only.
Expected: nozzle moves AWAY from bed. (Fail → flip `INVERT_Z_DIR`. Do not run G28 until this passes.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-013 — Extruder direction**
Hotend ≥200°C. Extrude 10mm, then retract 10mm.
Expected: extrude feeds toward nozzle, retract pulls back. (Fail → flip `INVERT_E0_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## F. Fans

**TC-014 — FAN1 (heatbreak) auto-control** ⚠️ critical, this is the heat-creep-jam fix
Heat hotend past 50°C, don't command any fan manually.
Expected: FAN1 starts on its own.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-015 — FAN2 (controller/case)**
Send `M17` (enable motors).
Expected: FAN2 runs.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-016 — Part-cooling fan isolation**
`M106 S255` with hotend cold, motors off.
Expected: only FAN0 spins.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## G. Heaters
*(Typing these commands = pressing the TFT's preheat buttons — same command either way. Can reuse the TC-014 heating cycle.)*

**TC-017 — Hotend heats to target**
Send `M104 S200`. Watch with `M105` or the TFT.
Expected: climbs steadily to ~200°C and holds within a few degrees, no error.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-018 — Bed heats to target**
Send `M140 S60`. Watch with `M105` or the TFT.
Expected: climbs steadily to ~60°C and holds within a few degrees, no error.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## H. Thermal Sanity — do before trusting G or L results

**TC-019 — No swapped/crossed thermistors**
Warm hotend only, watch `M105`; then warm bed only, watch `M105`.
Expected: hotend heat only moves hotend reading; bed heat only moves bed reading.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-020 — Cold-extrusion rejection**
Hotend below 170°C, attempt `G1 E10 F60`.
Expected: firmware refuses, motor doesn't turn.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## I. Homing & Leveling

**TC-021 — XY homing**
`G28 X Y`.
Expected: completes cleanly, no grinding at endstops.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-022 — Full homing (Z via probe)** ⚠️ hand near power switch
Full `G28`.
Expected: Z homes via probe, no collision.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-023 — Bed mesh sanity**
`G29`, look at the 5×5 values.
Expected: smooth plausible surface, no wild outlier or all-zero mesh. Pass → `M500`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## J. Travel Limits

**TC-024 — Software endstops enforce travel limits**
`M211` to confirm enabled. Try `G1 X310` (beyond 300mm bed).
Expected: move clamped/rejected, no crash into frame.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## K. Calibration

**TC-025 — Probe X/Y offset**
Measure probe-to-nozzle X/Y with calipers → `M851 X__ Y__` → `M500`.
Expected: matches physical measurement.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-026 — Probe Z offset (paper test)**
Paper-drag test at bed center → `M851 Z-__` → `M500`.
Expected: slight drag, no gouge, no gap.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-027 — E-steps calibration**
Mark 120mm filament, extrude 100mm commanded, measure actual. `new = 140 × 100 ÷ actual` → `M92 E__` → `M500`.
Expected: stable/repeatable within ~1–2% across 2–3 runs.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-028 — X/Y/Z travel accuracy**
Command 100mm X, then Y (10mm for Z), measure actual travel.
Expected: within ~1% of commanded on all axes.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-038 — Probe repeatability**
`M48 P10 V2` (probes same point 10x, reports mean/deviation).
Expected: low deviation, all 10 trigger successfully.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## L. Temperature Safety — requires TC-019 PASS first

**TC-029 — Hotend PID autotune**
`M303 E0 S200 C8 U1` → `M500`.
Expected: completes, no "failed" message, holds temp with low oscillation.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-030 — Bed PID autotune**
`M303 E-1 S60 C8 U1` → `M500`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-031 — Hotend thermal runaway protection** ⚠️ do under supervision
While hotend heating, briefly unplug its thermistor connector, reconnect.
Expected: Marlin halts heater, reports thermal error. (Fail = kept driving blind — highest severity.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-032 — Bed thermal runaway protection** ⚠️ do under supervision
Same test as TC-031, for the bed thermistor.
Expected: Marlin halts bed heater, reports thermal error.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-033 — MINTEMP/MAXTEMP enforcement**
`M104 S300` (above 275 max).
Expected: firmware refuses/clamps, doesn't drive to unsafe setpoint.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## M. EEPROM Persistence

**TC-034 — Settings survive cold power cycle**
After TC-025–030 saved, power off 30s, power on, check values (`M503` or re-check offsets/E-steps/PID).
Expected: all values match what was saved.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-035 — Factory reset**
`M502` → `M500`.
Expected: returns to compiled defaults cleanly, no corruption/hang.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## N. First Print

**TC-036 — First-layer quality with babystepping**
Start calibration print, watch layer one live.
Expected: even squish across the bed, no gaps.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-037 — Sustained print, no heat-creep jam**
Run 30–60 min continuous print.
Expected: no jams, no under-extrusion developing.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

---

## Failure detail (one block per FAIL/BLOCKED — delete if none)

### TC-### — <short title>
**Expected:** ...
**Actual:** ...
**Reproduction:** e.g. 3/3 attempts
**Evidence:** photo/video/log — attach to the GitHub Issue
**GitHub Issue:** #<number>
