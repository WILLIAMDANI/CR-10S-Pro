# Test Case Library — CR-10S Pro / SKR Mini E3 V3.0

Permanent, reusable procedures. No pass/fail lives in this file — see
`regression-runs/` for results against a specific build. When you add a new
test case, append it at the end of its group (don't renumber existing ones —
old run files reference these IDs).

Each test case cites the `MASTER-BRIEF-FOR-CLAUDE-CODE.md` section it's
grounded in, where applicable, so the *reason* a test exists stays attached to it.

**Probe wiring confirmed 2026-09-29:** the user's own hand-annotated schematic
traces the Z probe to E0-STOP (PC15), matching this firmware, and separately
marks the Z-STOP breakout pins "Not Used." See `HARDWARE-WIRING.md` and
`BUILD-LOG.md` Question 2 (resolved). TC-009 and everything gated behind it
are clear to run.

---

## A. Boot

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
**Expected Result:** TFT reaches its normal status screen (not a "disconnected"/no-response state), temps update live.
**Pass Criteria:** TFT shows live status. **Fail Criteria:** TFT reports no connection.
**Note:** The TFT35's speaker/buzzer is driven by the TFT's own onboard firmware, not by Marlin's `M300` — no `BEEPER_PIN` is wired here (no EXP1 cable used, per brief §5.2/§6). Don't expect `M300` to produce sound; that's not a defect, it's how this build is wired.
**Brief ref:** §5.2 (`SERIAL_PORT 2`), §6 (no native display driver used — TFT is a serial host).

### TC-039 — TFT touch, encoder, and button all respond
**Area:** Boot | **Priority:** Medium
**Procedure:** Tap the touchscreen, turn the rotary encoder, press the encoder button.
**Expected Result:** Each produces the expected on-screen effect (menu navigation, selection). A working screen doesn't by itself prove the underlying output is mapped correctly (see TC-017/018 for that) — this only confirms the TFT hardware itself is alive.
**Fail Criteria:** Any control unresponsive.

---

## B. Emergency Stop

### TC-004 — M112 emergency stop
**Area:** Safety | **Priority:** Critical — do this before any motion/heating test below.
**Procedure:** With motors enabled and/or a heater on, send `M112`.
**Expected Result:** Heaters and motion cut immediately; firmware requires a reset/reboot before accepting further motion (it should not silently resume).
**Pass Criteria:** Immediate, total stop; no motion or heat continues after. **Fail Criteria:** Anything keeps running, or a subsequent command resumes motion without a reset.

---

## C. Driver Health

### TC-005 — TMC2209 driver communication
**Area:** Drivers | **Priority:** High
**Procedure:** Send `M122`.
**Expected Result:** All four drivers (X, Y, Z, E) report UART communication OK, no overtemperature warning, no all-zero/all-one garbage response.
**Pass Criteria:** Clean report on all 4. **Fail Criteria:** Any driver reports a comm error or overtemp flag.

### TC-006 — Driver currents match configuration
**Area:** Drivers | **Priority:** Medium
**Procedure:** Send `M906` (no parameters) to report configured currents.
**Expected Result:** Z current reads ~1000mA (raised from the 800 default specifically because two Z motors share this one driver — brief §5.3). X/Y/E at their configured values.
**Pass Criteria:** Z reads ~1000mA, others plausible. **Fail Criteria:** Z still at stock 800 (means the current bump didn't take), or wildly wrong values.
**Brief ref:** §5.3 `Z_CURRENT`.

---

## D. Endstops & Probe Logic

### TC-007 — X endstop logic
**Area:** Endstops | **Priority:** Critical
**Procedure:** `M119`; observe `x_min`. Press the X endstop by hand; `M119` again.
**Expected Result:** `open` when released, `TRIGGERED` when pressed.
**Pass/Fail:** Matches expected = PASS; inverted or stuck = FAIL.
**Brief ref:** §11 Step 2.

### TC-008 — Y endstop logic
Same as TC-007 for `y_min`.

### TC-009 — Z probe trigger logic
**Area:** Probe | **Priority:** Critical
**Procedure:** `M119` with nothing near the probe face; observe `z_probe`. Hold a metal object (this is an inductive sensor — must be metal, not any material) to the probe face; `M119` again.
**Expected Result:** `open` when clear, `TRIGGERED` when metal is present.
**Pass Criteria:** Matches expected. **Fail Criteria:** Inverted (if so: flip `Z_MIN_PROBE_ENDSTOP_INVERTING`, rebuild, reflash, re-run this test). **No response at all on `z_probe` → stop, this may mean the wiring question above is real; do not proceed to homing.**
**Brief ref:** §7 (flagged unverified), §11 Step 2.

---

## E. Motor Directions (no homing — jog only)

### TC-010 — X direction
**Priority:** Critical | **Procedure:** Move gantry to mid-travel by hand. Jog a small `+X` move.
**Expected:** Nozzle moves toward increasing X. **Fail →** flip `INVERT_X_DIR`.
**Brief ref:** §7, §11 Step 3.

### TC-011 — Y direction
Same pattern for `+Y`. **Fail →** flip `INVERT_Y_DIR`.

### TC-012 — Z direction (**safety-critical — read before running**)
**Priority:** Critical | **Procedure:** Jog a small `+Z` move only, with a hand near the power switch.
**Expected:** Nozzle moves **away** from the bed. **Fail →** flip `INVERT_Z_DIR`. **Never run `G28` until this passes.**
**Brief ref:** §11 Step 3 — explicitly the step that "can crash the nozzle into the bed if done early."

### TC-013 — Extruder direction
**Priority:** High | **Preconditions:** Hotend ≥200°C. **Procedure:** Extrude 10mm, then retract 10mm.
**Expected:** Extrude feeds filament toward the nozzle; retract pulls it back the opposite way. **Fail →** flip `INVERT_E0_DIR`.
**Brief ref:** §7, §11 Step 5.

---

## F. Fans

### TC-014 — Heatbreak fan (FAN1) auto-control
**Priority:** Critical (this is the fix from brief §13.5 — heat-creep jams without it)
**Procedure:** Heat hotend past 50°C without commanding any fan manually.
**Expected:** FAN1 starts on its own. **Fail Criteria:** FAN1 stays off — this is a serious regression, treat as a blocking bug.
**Brief ref:** §5.3 `E0_AUTO_FAN_PIN`.

### TC-015 — Controller/case fan (FAN2)
**Procedure:** Enable any stepper motor (e.g. send `M17`). **Expected:** FAN2 runs.
**Brief ref:** §5.3 `CONTROLLER_FAN_PIN`.

### TC-016 — Part-cooling fan isolation
**Procedure:** `M106 S255` with hotend cold and no motors enabled.
**Expected:** Only FAN0 spins — FAN1/FAN2 stay under their own automatic control, not driven by M106.

---

## G. Heaters

Run these using typed commands, not the TFT screen's preheat buttons. A typed
command (`M104`/`M140`) is exactly what those buttons send internally — same
result — but typing it directly isolates the firmware/hardware from the TFT.
If a typed command works but the TFT button doesn't, the problem is in the
TFT's own configuration, not this firmware. You can run these in the same
physical heating cycle you use for TC-014 (FAN1 auto-on) — no need to heat twice.

### TC-017 — Hotend heats to target temperature
**Area:** Heaters | **Priority:** Critical
**Procedure:** Send `M104 S200`. Watch temperature with `M105` (or the TFT display) as it climbs.
**Expected Result:** Temperature climbs steadily toward 200°C and holds within a few degrees, no error, no thermal shutdown.
**Pass Criteria:** Reaches and holds target. **Fail Criteria:** Doesn't climb, climbs but won't hold near target, or firmware reports a thermal error.
**Brief ref:** §5.2 `TEMP_SENSOR_0`, `HEATER_0_MAXTEMP`.

### TC-018 — Bed heats to target temperature
**Area:** Heaters | **Priority:** Critical
**Procedure:** Send `M140 S60`. Watch temperature with `M105`/TFT as it climbs.
**Expected Result:** Temperature climbs steadily toward 60°C and holds within a few degrees.
**Pass Criteria:** Reaches and holds target. **Fail Criteria:** Doesn't climb, won't hold, or firmware reports a thermal error.
**Brief ref:** §5.2 `TEMP_SENSOR_BED`, `BED_MAXTEMP`.

---

## H. Thermal Sanity

### TC-019 — No swapped/crossed thermistors
**Area:** Safety | **Priority:** Critical, do this before trusting either heater test above.
**Procedure:** With both at room temp, gently warm the hotend area only (e.g. with the hotend heater briefly on, hand elsewhere) and watch `M105`. Then let it cool, and instead let the bed heat briefly, watching `M105` again.
**Expected Result:** Heating the hotend changes only the hotend reading; heating the bed changes only the bed reading.
**Fail Criteria:** The *other* channel's reading moves instead/also — thermistor wires are crossed or a sensor is loose. **Do not trust TC-017/TC-018/TC-029–033 results until this passes.**

### TC-020 — Cold-extrusion rejection
**Area:** Safety | **Priority:** High
**Procedure:** With hotend below 170°C (`EXTRUDE_MINTEMP`), attempt `G1 E10 F60`.
**Expected Result:** Firmware refuses the move with a cold-extrusion warning; motor does not turn.
**Fail Criteria:** Extruder moves anyway — `PREVENT_COLD_EXTRUSION` isn't working.
**Brief ref:** §5.2 `PREVENT_COLD_EXTRUSION`, `EXTRUDE_MINTEMP 170`.

---

## I. Homing & Leveling

### TC-021 — XY homing
**Priority:** Critical | **Preconditions:** TC-007, TC-008, TC-010, TC-011 all PASS.
**Procedure:** `G28 X Y`. **Expected:** Completes cleanly, no grinding/skipped steps at the endstops.

### TC-022 — Full homing (Z via probe)
**Priority:** Critical | **Preconditions:** TC-009, TC-012, TC-021 all PASS. Hand near power switch.
**Procedure:** Full `G28`. **Expected:** Z homes using the probe (per `USE_PROBE_FOR_Z_HOMING`), `Z_SAFE_HOMING` keeps the probe over the bed throughout, no collision.
**Brief ref:** §5.2, §2 (no Z endstop switch exists — probe-only Z homing).

### TC-023 — Bed mesh sanity
**Priority:** High | **Preconditions:** TC-022 PASS. **Procedure:** `G29`, inspect the 5×5 mesh values.
**Expected:** Values form a smooth, plausible surface (no single wild outlier point, no all-zero mesh). **Pass →** `M500`.
**Brief ref:** §5.2 `GRID_MAX_POINTS_X 5`, `EXTRAPOLATE_BEYOND_GRID`.

---

## J. Travel Limits

### TC-024 — Software endstops enforce travel limits
**Priority:** Medium | **Preconditions:** TC-022 PASS (homed).
**Procedure:** `M211` to confirm software endstops are enabled. Then attempt to move slightly beyond a configured limit (e.g. `G1 X310` when `X_BED_SIZE` is 300).
**Expected:** Move is clamped/rejected at the boundary rather than crashing the gantry into the frame.
**Fail Criteria:** Machine drives past the mechanical limit.

---

## K. Probe Offset & Calibration

Requires TC-022/023 passing first.

### TC-025 — Probe X/Y offset
**Procedure:** Measure probe-to-nozzle X/Y distance with calipers. `M851 X__ Y__`, `M500`.
**Expected:** Matches physical measurement (starting config value `{-27, 0, 0}` is an estimate, not measured — expect to correct it here).
**Brief ref:** §7 (flagged unverified magnitude).

### TC-026 — Probe Z offset (paper test)
**Procedure:** Standard paper-drag first-layer test at bed center. `M851 Z-__`, `M500`.
**Expected:** Slight drag on the paper, no gouging, no visible gap.

### TC-027 — E-steps calibration
**Procedure:** Mark 120mm of filament above the extruder gear, command 100mm extrusion, measure filament actually consumed. `new = old(140) × 100 ÷ actual`. `M92 E<new>`, `M500`.
**Expected:** New value is stable and repeatable across 2–3 runs (within ~1–2%).
**Brief ref:** §7, §13.4 (previous bad guess of 415 corrected to 140 — still uncalibrated until this test runs).

### TC-028 — X/Y/Z travel accuracy
**Priority:** Medium | **Procedure:** Command a 100mm move on X, then Y, physically measure actual travel with a tape measure/calipers. Repeat with a 10mm Z move (harder to measure precisely — best effort).
**Expected:** Measured travel within ~1% of commanded, on all three axes. Confirms steps/mm (80/80/400) are actually correct for this hardware, independent of the E-steps test above.
**Fail Criteria:** Consistent error beyond ~1–2% — steps/mm may need adjusting, or something is slipping.

### TC-038 — Probe repeatability
**Priority:** Medium | **Preconditions:** TC-022 PASS (homed). **Procedure:** `M48 P10 V2` — probes the same point 10 times and reports mean/deviation.
**Expected:** Low standard deviation (inductive sensors are usually very consistent — large scatter suggests a mounting, wiring, or interference problem).
**Fail Criteria:** High deviation, or any of the 10 probes fails to trigger.
**Brief ref:** §7 — this is the objective check behind whether the probe is actually reliable enough to trust for `G29`.

---

## L. Temperature Safety

**Requires TC-019 (no swapped thermistors) PASS first.**

### TC-029 — Hotend PID autotune
**Procedure:** `M303 E0 S200 C8 U1`, then `M500`.
**Expected:** Completes without a "PID Autotune failed" message; hotend holds target temp with acceptably low oscillation afterward.

### TC-030 — Bed PID autotune
Same pattern: `M303 E-1 S60 C8 U1`, `M500`.

### TC-031 — Hotend thermal runaway protection (**do under supervision**)
**Priority:** Critical, safety
**Procedure:** While hotend is heating toward a target, briefly unplug the hotend thermistor connector, then reconnect.
**Expected:** Marlin halts the heater and reports a thermal error (`THERMAL RUNAWAY` or `HEATING FAILED`) rather than continuing to heat blind.
**Fail Criteria:** Heater keeps driving with no sensor feedback — this is a fire-safety-relevant failure, treat as highest severity.
**Brief ref:** §5.2 `THERMAL_PROTECTION_HOTENDS`.

### TC-032 — Bed thermal runaway protection (**do under supervision**)
**Priority:** Critical, safety — same test as TC-031, for the bed.
**Procedure:** While the bed is heating toward a target, briefly unplug the bed thermistor connector, then reconnect.
**Expected:** Marlin halts the bed heater and reports a thermal error.
**Fail Criteria:** Bed heater keeps driving with no sensor feedback.
**Brief ref:** §5.2 `THERMAL_PROTECTION_BED`.

### TC-033 — MINTEMP/MAXTEMP enforcement
**Procedure:** Attempt `M104 S300` (above `HEATER_0_MAXTEMP 275`).
**Expected:** Firmware refuses/clamps rather than driving the heater to an unsafe setpoint.

---

## M. EEPROM / Configuration Persistence

### TC-034 — Settings survive a cold power cycle
**Priority:** High | **Procedure:** After TC-025–TC-030 are saved with `M500`, fully power off for 30 seconds, power back on, `M503` or re-check the relevant values (probe offset, E-steps, PID).
**Expected:** All values match what was saved — nothing reverts to compiled defaults.
**Brief ref:** §5.2 `EEPROM_SETTINGS`, `EEPROM_AUTO_INIT`.

### TC-035 — Factory reset
**Procedure:** `M502` then `M500`.
**Expected:** Values return to the compiled-in defaults from `Configuration.h`/`Configuration_adv.h`, cleanly, no corruption or hang.
**Brief ref:** §11 Step 1 (this is literally the first commissioning step, done right after every flash).

---

## N. First Print

### TC-036 — First-layer quality with babystepping
**Procedure:** Start a simple calibration print, watch layer one live with babystepping ready.
**Expected:** Even first-layer squish across the bed, no gaps despite `Z_MIN_PROBE_PIN`/offset being freshly calibrated rather than production-tested.
**Brief ref:** §5.3 `BABYSTEPPING`/`BABYSTEP_ZPROBE_OFFSET`, §11 Step 11.

### TC-037 — Sustained print, no heat-creep jam
**Procedure:** Run a print of at least 30–60 minutes continuous extrusion.
**Expected:** No jams, no under-extrusion developing over time (the failure mode TC-014 exists specifically to prevent).

---

## O. Regression

Empty at project start. **Every bug found and fixed gets a test case added here**,
so it has a permanent, repeatable check that it doesn't silently return in a
later firmware build. Format: same as above, plus a `Regression for:` line
pointing at the GitHub Issue that originally reported it.

(none yet)
