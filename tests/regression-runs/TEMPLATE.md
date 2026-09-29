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
Expected: TFT reaches normal status screen, temps update live.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## B. Endstops & Probe

**TC-004 — X endstop logic**
`M119`, note `x_min`. Press X endstop by hand, `M119` again.
Expected: `open` released → `TRIGGERED` pressed.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-005 — Y endstop logic**
Same as TC-004 for `y_min`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-006 — Z probe trigger logic**
`M119` with probe clear, note `z_probe`. Hold metal to probe face, `M119` again.
Expected: `open` clear → `TRIGGERED` with metal present. (If inverted: flip `Z_MIN_PROBE_ENDSTOP_INVERTING`, rebuild, reflash, retest.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## C. Motor Directions (jog only — no homing yet)

**TC-007 — X direction**
Move gantry to mid-travel by hand. Jog small `+X`.
Expected: moves toward increasing X. (Fail → flip `INVERT_X_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-008 — Y direction**
Jog small `+Y`. Expected: increasing Y. (Fail → flip `INVERT_Y_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-009 — Z direction ⚠️ SAFETY: hand near power switch**
Jog small `+Z` only.
Expected: nozzle moves AWAY from bed. (Fail → flip `INVERT_Z_DIR`. Do not run G28 until this passes.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-010 — Extruder direction**
Hotend ≥200°C. Extrude 10mm.
Expected: filament feeds toward nozzle. (Fail → flip `INVERT_E0_DIR`.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## D. Fans

**TC-011 — FAN1 (heatbreak) auto-control** ⚠️ critical, this is the heat-creep-jam fix
Heat hotend past 50°C, don't command any fan manually.
Expected: FAN1 starts on its own.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-012 — FAN2 (controller/case)**
Send `M17` (enable motors).
Expected: FAN2 runs.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-013 — Part-cooling fan isolation**
`M106 S255` with hotend cold, motors off.
Expected: only FAN0 spins.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## E. Homing & Leveling (needs B, C above all PASS)

**TC-014 — XY homing**
`G28 X Y`.
Expected: completes cleanly, no grinding at endstops.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-015 — Full homing (Z via probe)** ⚠️ hand near power switch
Full `G28`.
Expected: Z homes via probe, no collision.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-016 — Bed mesh sanity**
`G29`, look at the 5×5 values.
Expected: smooth plausible surface, no wild outlier or all-zero mesh. Pass → `M500`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## F. Calibration

**TC-017 — Probe X/Y offset**
Measure probe-to-nozzle X/Y with calipers → `M851 X__ Y__` → `M500`.
Expected: matches physical measurement.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-018 — Probe Z offset (paper test)**
Paper-drag test at bed center → `M851 Z-__` → `M500`.
Expected: slight drag, no gouge, no gap.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-019 — E-steps calibration**
Mark 120mm filament, extrude 100mm commanded, measure actual. `new = 140 × 100 ÷ actual` → `M92 E__` → `M500`.
Expected: stable/repeatable within ~1–2% across 2–3 runs.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## G. Thermal Safety

**TC-020 — Hotend PID autotune**
`M303 E0 S200 C8 U1` → `M500`.
Expected: completes, no "failed" message, holds temp with low oscillation.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-021 — Bed PID autotune**
`M303 E-1 S60 C8 U1` → `M500`.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-022 — Thermal runaway protection** ⚠️ do under supervision
While hotend heating, briefly unplug its thermistor connector, reconnect.
Expected: Marlin halts heater, reports thermal error. (Fail = heater kept driving blind — highest severity, fire-safety.)
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-023 — MINTEMP/MAXTEMP enforcement**
`M104 S300` (above 275 max).
Expected: firmware refuses/clamps, doesn't drive to unsafe setpoint.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## H. EEPROM Persistence

**TC-024 — Settings survive cold power cycle**
After TC-017–021 saved, power off 30s, power on, check values (`M503` or re-check offsets/E-steps/PID).
Expected: all values match what was saved.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-025 — Factory reset**
`M502` → `M500`.
Expected: returns to compiled defaults cleanly, no corruption/hang.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

## I. First Print

**TC-026 — First-layer quality with babystepping**
Start calibration print, watch layer one live.
Expected: even squish across the bed, no gaps.
Result: ⬜ PASS ⬜ FAIL ⬜ BLOCKED ⬜ NOT RUN — Notes/Issue#: __________

**TC-027 — Sustained print, no heat-creep jam**
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
