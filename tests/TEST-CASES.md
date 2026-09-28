# Test Case Library — CR-10S Pro / SKR Mini E3 V3.0

Permanent, reusable procedures. No pass/fail lives in this file — see
`regression-runs/` for results against a specific build. When you add a new
test case, append it at the end of its group (don't renumber existing ones —
old run files reference these IDs).

Each test case cites the `MASTER-BRIEF-FOR-CLAUDE-CODE.md` section it's
grounded in, where applicable, so the *reason* a test exists stays attached to it.

---

## A. Smoke / Boot

### TC-001 — Firmware flashes via SD card
**Area:** Boot | **Priority:** Critical
**Preconditions:** `firmware.bin` built successfully; SD card formatted FAT32.
**Procedure:**
1. Copy `firmware.bin` to the root of a FAT32 SD card.
2. Power off printer, insert card into the SKR Mini E3's onboard slot, power on.
3. Wait ~10 seconds, power off, remove card, inspect filename on another computer.
**Expected Result:** File is renamed (e.g. to `FIRMWARE.CUR`) by the bootloader, indicating it flashed.
**Pass Criteria:** Filename changed. **Fail Criteria:** Filename unchanged, or board shows no sign of life.

### TC-002 — Correct firmware identifies itself
**Area:** Boot | **Priority:** Critical
**Preconditions:** TC-001 passed.
**Procedure:** Connect via USB, open a serial terminal at any baud (native USB CDC), send `M115`.
**Expected Result:** Response includes machine name `CR-10S Pro` (from `CUSTOM_MACHINE_NAME`).
**Pass Criteria:** Name present and correct. **Fail Criteria:** Old/stock firmware identifies instead, or no response.

### TC-003 — TFT35 connects to mainboard
**Area:** Boot | **Priority:** High
**Preconditions:** TFT35 wired to the TFT header (UART2).
**Procedure:** Power on with TFT attached; observe screen.
**Expected Result:** TFT reaches its normal status screen (not a "disconnected"/no-response state).
**Pass Criteria:** TFT shows live status (temps update, etc). **Fail Criteria:** TFT reports no connection.
**Brief ref:** §5.2 (`SERIAL_PORT 2`), §6 (no native display driver used — TFT is a serial host).

---

## B. Endstops & Probe Logic

### TC-004 — X endstop logic
**Area:** Endstops | **Priority:** Critical
**Procedure:** `M119`; observe `x_min`. Press the X endstop by hand; `M119` again.
**Expected Result:** `open` when released, `TRIGGERED` when pressed.
**Pass/Fail:** Matches expected = PASS; inverted or stuck = FAIL.
**Brief ref:** §11 Step 2.

### TC-005 — Y endstop logic
Same as TC-004 for `y_min`.

### TC-006 — Z probe trigger logic
**Area:** Probe | **Priority:** Critical
**Procedure:** `M119` with nothing near the probe face; observe `z_probe`. Hold a metal object to the probe face; `M119` again.
**Expected Result:** `open` when clear, `TRIGGERED` when metal is present.
**Pass Criteria:** Matches expected. **Fail Criteria:** Inverted (if so: flip `Z_MIN_PROBE_ENDSTOP_INVERTING`, rebuild, reflash, re-run this test).
**Brief ref:** §7 (flagged unverified), §11 Step 2.

---

## C. Motor Directions (no homing — jog only)

### TC-007 — X direction
**Priority:** Critical | **Procedure:** Move gantry to mid-travel by hand. Jog a small `+X` move.
**Expected:** Nozzle moves toward increasing X. **Fail →** flip `INVERT_X_DIR`.
**Brief ref:** §7, §11 Step 3.

### TC-008 — Y direction
Same pattern for `+Y`. **Fail →** flip `INVERT_Y_DIR`.

### TC-009 — Z direction (**safety-critical — read before running**)
**Priority:** Critical | **Procedure:** Jog a small `+Z` move only, with a hand near the power switch.
**Expected:** Nozzle moves **away** from the bed. **Fail →** flip `INVERT_Z_DIR`. **Never run `G28` until this passes.**
**Brief ref:** §11 Step 3 — explicitly the step that "can crash the nozzle into the bed if done early."

### TC-010 — Extruder direction
**Priority:** High | **Preconditions:** Hotend ≥200°C. **Procedure:** Extrude 10mm.
**Expected:** Filament feeds toward the nozzle. **Fail →** flip `INVERT_E0_DIR`.
**Brief ref:** §7, §11 Step 5.

---

## D. Fans

### TC-011 — Heatbreak fan (FAN1) auto-control
**Priority:** Critical (this is the fix from brief §13.5 — heat-creep jams without it)
**Procedure:** Heat hotend past 50°C without commanding any fan manually.
**Expected:** FAN1 starts on its own. **Fail Criteria:** FAN1 stays off — this is a serious regression, treat as a blocking bug.
**Brief ref:** §5.3 `E0_AUTO_FAN_PIN`.

### TC-012 — Controller/case fan (FAN2)
**Procedure:** Enable any stepper motor (e.g. send `M17`). **Expected:** FAN2 runs.
**Brief ref:** §5.3 `CONTROLLER_FAN_PIN`.

### TC-013 — Part-cooling fan isolation
**Procedure:** `M106 S255` with hotend cold and no motors enabled.
**Expected:** Only FAN0 spins — FAN1/FAN2 stay under their own automatic control, not driven by M106.

---

## E. Homing & Leveling

### TC-014 — XY homing
**Priority:** Critical | **Preconditions:** TC-004, TC-005, TC-007, TC-008 all PASS.
**Procedure:** `G28 X Y`. **Expected:** Completes cleanly, no grinding/skipped steps at the endstops.

### TC-015 — Full homing (Z via probe)
**Priority:** Critical | **Preconditions:** TC-006, TC-009, TC-014 all PASS. Hand near power switch.
**Procedure:** Full `G28`. **Expected:** Z homes using the probe (per `USE_PROBE_FOR_Z_HOMING`), `Z_SAFE_HOMING` keeps the probe over the bed throughout, no collision.
**Brief ref:** §5.2, §2 (no Z endstop switch exists — probe-only Z homing).

### TC-016 — Bed mesh sanity
**Priority:** High | **Preconditions:** TC-015 PASS. **Procedure:** `G29`, inspect the 5×5 mesh values.
**Expected:** Values form a smooth, plausible surface (no single wild outlier point, no all-zero mesh). **Pass →** `M500`.
**Brief ref:** §5.2 `GRID_MAX_POINTS_X 5`, `EXTRAPOLATE_BEYOND_GRID`.

---

## F. Probe Offset & Calibration

### TC-017 — Probe X/Y offset
**Procedure:** Measure probe-to-nozzle X/Y distance with calipers. `M851 X__ Y__`, `M500`.
**Expected:** Matches physical measurement (starting config value `{-27, 0, 0}` is an estimate, not measured — expect to correct it here).
**Brief ref:** §7 (flagged unverified magnitude).

### TC-018 — Probe Z offset (paper test)
**Procedure:** Standard paper-drag first-layer test at bed center. `M851 Z-__`, `M500`.
**Expected:** Slight drag on the paper, no gouging, no visible gap.

### TC-019 — E-steps calibration
**Procedure:** Mark 120mm of filament above the extruder gear, command 100mm extrusion, measure filament actually consumed. `new = old(140) × 100 ÷ actual`. `M92 E<new>`, `M500`.
**Expected:** New value is stable and repeatable across 2–3 runs (within ~1–2%).
**Brief ref:** §7, §13.4 (previous bad guess of 415 corrected to 140 — still uncalibrated until this test runs).

---

## G. Temperature Control & Safety

### TC-020 — Hotend PID autotune
**Procedure:** `M303 E0 S200 C8 U1`, then `M500`.
**Expected:** Completes without a "PID Autotune failed" message; hotend holds target temp with acceptably low oscillation afterward.

### TC-021 — Bed PID autotune
Same pattern: `M303 E-1 S60 C8 U1`, `M500`.

### TC-022 — Thermal runaway protection (**do under supervision**)
**Priority:** Critical, safety
**Procedure:** While hotend is heating toward a target, briefly unplug the hotend thermistor connector, then reconnect.
**Expected:** Marlin halts the heater and reports a thermal error (`THERMAL RUNAWAY` or `HEATING FAILED`) rather than continuing to heat blind.
**Fail Criteria:** Heater keeps driving with no sensor feedback — this is a fire-safety-relevant failure, treat as highest severity.
**Brief ref:** §5.2 `THERMAL_PROTECTION_HOTENDS`/`THERMAL_PROTECTION_BED` (stock Marlin defaults, not customized, but worth verifying on this specific hardware).

### TC-023 — MINTEMP/MAXTEMP enforcement
**Procedure:** Attempt `M104 S300` (above `HEATER_0_MAXTEMP 275`).
**Expected:** Firmware refuses/clamps rather than driving the heater to an unsafe setpoint.

---

## H. EEPROM / Configuration Persistence

### TC-024 — Settings survive a cold power cycle
**Priority:** High | **Procedure:** After TC-017–TC-021 are saved with `M500`, fully power off for 30 seconds, power back on, `M503` or re-check the relevant values (probe offset, E-steps, PID).
**Expected:** All values match what was saved — nothing reverts to compiled defaults.
**Brief ref:** §5.2 `EEPROM_SETTINGS`, `EEPROM_AUTO_INIT`.

### TC-025 — Factory reset
**Procedure:** `M502` then `M500`.
**Expected:** Values return to the compiled-in defaults from `Configuration.h`/`Configuration_adv.h`, cleanly, no corruption or hang.
**Brief ref:** §11 Step 1 (this is literally the first commissioning step, done right after every flash).

---

## I. First Print

### TC-026 — First-layer quality with babystepping
**Procedure:** Start a simple calibration print, watch layer one live with babystepping ready.
**Expected:** Even first-layer squish across the bed, no gaps despite `Z_MIN_PROBE_PIN`/offset being freshly calibrated rather than production-tested.
**Brief ref:** §5.3 `BABYSTEPPING`/`BABYSTEP_ZPROBE_OFFSET`, §11 Step 11.

### TC-027 — Sustained print, no heat-creep jam
**Procedure:** Run a print of at least 30–60 minutes continuous extrusion.
**Expected:** No jams, no under-extrusion developing over time (the failure mode TC-011 exists specifically to prevent).

---

## J. Regression

Empty at project start. **Every bug found and fixed gets a test case added here**,
so it has a permanent, repeatable check that it doesn't silently return in a
later firmware build. Format: same as above, plus a `Regression for:` line
pointing at the GitHub Issue that originally reported it.

(none yet)
