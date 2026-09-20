# MASTER BRIEF — CR-10S Pro → SKR Mini E3 V3.0 + TFT35 E3 V3.0.1

**Read this document in full before running any command or editing any file.**
**Re-read sections 2, 5, 6 and 7 any time you lose conversational context.**

---

## 0. HOW TO USE THIS DOCUMENT

You are working on custom Marlin 2.1.2.8 firmware for a physical 3D printer that has been re-boarded. Three files in this source tree were **deliberately modified** before you arrived. Most of what looks wrong in them is intentional and is explained here.

This project has a specific failure history: a previous AI-assisted attempt produced firmware with multiple errors, largely because **context was lost between steps** — earlier decisions were forgotten and silently reversed later in the session. Section 1 exists to prevent that recurring. Take it seriously.

Three roles in this project:
- **The user** — owns the printer, is the only one who can observe physical reality (wire routing, motor direction, measurements). Their observations outrank all reasoning.
- **You (Claude Code)** — can compile, read the full tree, iterate on real errors, edit files.
- **A separate chat assistant** — holds the full design history and reviews proposed changes against it. The user relays between you.

---

## 1. CONTEXT-PRESERVATION PROTOCOL — FOLLOW THIS

The single biggest risk here is not a hard bug. It is you forgetting, 40 minutes in, that the probe pin override was deliberate, "fixing" it, and producing firmware that compiles perfectly and drives the nozzle into the bed.

**Maintain a file called `BUILD-LOG.md` in the project root.** Create it on your first action. Append to it continuously — never rewrite or trim it. Structure:

```markdown
## Session log
- [timestamp] Action taken, file touched, result.

## Changes I made
- file:line — what changed, from → to, why, and which section of MASTER-BRIEF justifies it.

## Open questions for the user
- Numbered, specific, each stating what observation would answer it.

## Things I confirmed but did NOT change
- Settings I examined, found suspicious, and left alone because the brief says they're intentional.
```

Rules:
1. **Before editing any file**, check this brief's sections 5 and 6. If the setting appears there, do not change it — log it under "confirmed but did not change" instead.
2. **After every edit**, append to `BUILD-LOG.md` immediately. Do not batch this.
3. **If your context is compacted or you feel uncertain about earlier decisions**, stop, re-read this brief and `BUILD-LOG.md`, and say so out loud to the user before continuing.
4. **This file and `BUILD-LOG.md` outrank your memory.** If your recollection conflicts with them, they are right.
5. Never make a change because it "seems cleaner." Only fix things that actually break the build or that the user asks for.

---

## 2. THE MACHINE — WHAT IS PHYSICALLY THERE

| Item | Detail |
|---|---|
| Frame | Stock Creality CR-10S Pro |
| Build volume | 300 × 300 × 400 mm |
| System voltage | **24V throughout** |
| Mainboard | BIGTREETECH SKR Mini E3 V3.0, **STM32G0B1RET6** |
| Build target | `STM32G0B1RE_btt` (defined in `ini/stm32g0.ini`) |
| Screen | BTT TFT35 E3 V3.0.1 on the board's TFT header |
| Stepper drivers | 4 × onboard TMC2209, UART mode, not removable |
| X motor | Creality 42-40, single connector → `XM` |
| Y motor | Creality 42-40, single connector → `YM` |
| Z motors | **TWO** Creality 42-34 motors → `ZAM` and `ZBM` |
| Extruder | Stock CR-10S Pro, single motor → `EM` |
| Z probe | Creality **SZC-M18-8DN** inductive proximity sensor |

### The Z axis — important
This board has **one** Z driver with **two** physical connectors wired in parallel. Both Z motors move together off a single driver. There is no independent second Z driver, therefore:
- No `Z2_DRIVER_TYPE`
- No `NUM_Z_STEPPER_DRIVERS`
- No `Z_MULTI_ENDSTOPS`
- No `Z_STEPPER_AUTO_ALIGN` / `G34`

Because two motors share one driver's current, `Z_CURRENT` was raised from 800 to 1000 mA.

### The Z probe — the central design decision
The SZC-M18-8DN is a **fixed inductive proximity sensor**. It is NPN, normally-open, and requires **10–30 VDC** on its power wire. It is **not** a BLTouch, has no servo, does not deploy or stow.

It is wired to the **E0-STOP terminal (PC15)**, *not* the board's dedicated 5-pin PROBE header (PC14).

There is **no Z endstop switch on this machine at all.** The CR-10S Pro has no stock Z limit switch; Z homing is done entirely by the probe. The `Z-STOP` terminal (PC2) is physically empty.

---

## 3. WIRING MAP

From the user's own physical survey of the machine:

```
COMPONENT              SKR TERMINAL     PIN
-------------------------------------------------
X motor                XM
Y motor                YM
Z motor 1              ZAM              } same driver,
Z motor 2              ZBM              } wired parallel
Extruder motor         EM

X endstop              X-STOP           PC0
Y endstop              Y-STOP           PC1
Z endstop              (none)           PC2  -- UNUSED
Z probe (signal)       E0-STOP          PC15

Hotend heater          E0               PC8
Bed heater             HB               PC9
Hotend thermistor      TH0              PA0
Bed thermistor         THB              PC4

Part cooling fan       FAN0             PC6
Hotend heatbreak fan   FAN1             PC7
Board / case fan       FAN2             PB15

Touchscreen            TFT header       UART2 (PA2 TX / PA3 RX)
```

---

## 4. ELECTRICAL SAFETY — VERIFY BEFORE POWER-ON

**Probe power.** The SZC-M18-8DN needs 10–30 VDC. The endstop headers supply only ~3.3V. Correct wiring:
```
Brown  → +24V from the PSU        (NOT the E0-STOP VCC pin)
Blue   → GND / 0V
Black  → signal → E0-STOP (PC15)
```
An earlier draft of this project incorrectly suggested all three probe wires could land on E0-STOP. That was wrong. The brown wire must be traced physically to confirm it is on the 24V rail.

**Component voltages.** The CR-10S Pro is a 24V machine. Before powering anything from the SKR, the user should confirm PSU output ≈24V and that the hotend heater cartridge, bed, and all three fans are 24V parts. A surviving 12V component from a past repair would be destroyed on first power-up.

---

## 5. INTENTIONAL MODIFICATIONS — DO NOT REVERT

### 5.1 `Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h`

This is a vendor pins file that has been **deliberately edited**. It is not corrupted. Do not restore it to stock.

| Change | Reason |
|---|---|
| `Z_MIN_PROBE_PIN` changed from `PC14` → `PC15` | The probe is physically on E0-STOP, not the PROBE header |
| `FIL_RUNOUT_PIN` block commented out | It also defaulted to PC15 and would collide; no runout sensor is installed |

The stock file carries a comment reading "Z Probe must be this pin." That refers to the dedicated header's routing. The override is correct for this machine's actual wiring.

### 5.2 `Marlin/Configuration.h`

| Setting | Value | Reason |
|---|---|---|
| `MOTHERBOARD` | `BOARD_BTT_SKR_MINI_E3_V3_0` | STM32G0B1RE variant |
| `X/Y/Z/E0_DRIVER_TYPE` | `TMC2209` | Onboard drivers |
| `SERIAL_PORT` | `2` | UART2 = the TFT header on this board (verified in the pins file: `UART2_TX_PIN PA2`, `UART2_RX_PIN PA3`) |
| `BAUDRATE` | `115200` | BTT's standard mainboard↔TFT speed |
| `SERIAL_PORT_2` | `-1` | Keeps USB available alongside the TFT |
| `USE_ZMIN_PLUG` | **disabled** | No Z endstop switch exists |
| `Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` | **disabled** | The probe has its own pin; enabling this conflicts with the PC15 override |
| `USE_PROBE_FOR_Z_HOMING` | **enabled** | Z homes on the probe |
| `Z_MIN_PROBE_PIN` | `PC15` | Mirrors the pins file |
| `FIX_MOUNTED_PROBE` | enabled | Fixed inductive sensor |
| `MULTIPLE_PROBING` | `2` | Improves inductive repeatability |
| `AUTO_BED_LEVELING_BILINEAR` | enabled | 5×5 grid |
| `EXTRAPOLATE_BEYOND_GRID` | enabled | Large negative X probe offset means the probe can't reach all bed edges |
| `RESTORE_LEVELING_AFTER_G28` | enabled | Mesh would otherwise be dropped on every home |
| `Z_SAFE_HOMING` | enabled | Mandatory when homing Z with a bed probe |
| `Z_HOMING_HEIGHT` / `Z_AFTER_HOMING` | `4` / `10` | Clearance |
| bed / Z travel | 300 / 300 / 400 | CR-10S Pro specification |
| `TEMP_SENSOR_0`, `TEMP_SENSOR_BED` | `1`, `1` | Correct for stock CR-10S Pro thermistors |
| accelerations | 500 print, 500 travel, 1000 retract; max `{500,500,100,5000}` | Deliberately conservative for commissioning; will be raised later |
| `EEPROM_SETTINGS`, `EEPROM_AUTO_INIT`, `SDSUPPORT` | enabled | Needed to persist calibration |

### 5.3 `Marlin/Configuration_adv.h`

| Setting | Value | Reason |
|---|---|---|
| `E0_AUTO_FAN_PIN` | `FAN1_PIN` | **Critical.** FAN1 is the hotend heatbreak fan. Without this it never runs automatically → heat creep → jams. This was missed in an earlier pass and is the most recent fix. |
| `USE_CONTROLLER_FAN` + `CONTROLLER_FAN_PIN` | enabled, `FAN2_PIN` | FAN2 is the board/case fan |
| `BABYSTEPPING` + `BABYSTEP_ZPROBE_OFFSET` | enabled | Live Z tuning during first layer; the probe Z offset is uncalibrated |
| `Z_CURRENT` | `1000` | Two motors share the Z driver |

---

## 6. DO NOT ENABLE

| Feature | Why not |
|---|---|
| `Z2_DRIVER_TYPE`, `NUM_Z_STEPPER_DRIVERS`, `Z_MULTI_ENDSTOPS`, `Z_STEPPER_AUTO_ALIGN` | No independent second Z driver exists |
| `BLTOUCH`, `PROBE_MANUALLY`, `NOZZLE_AS_PROBE`, servo probes | Wrong probe type |
| `SENSORLESS_PROBING` | Incompatible with `USE_PROBE_FOR_Z_HOMING` (Marlin will error) |
| `SENSORLESS_HOMING` | Physical endstops are installed and wired |
| `USE_ZMIN_PLUG` | Nothing is connected to PC2 |
| `USE_ZMAX_PLUG` | No identified Z-max hardware |
| `TFT_COLOR_UI`, `TFT_LVGL_UI`, `CR10_STOCKDISPLAY`, DWIN/DGUS | The TFT35 runs its own firmware and talks to Marlin over serial like a host. No native display driver belongs here. |
| `FILAMENT_RUNOUT_SENSOR` | Not currently wired; see section 10 |
| `POWER_LOSS_RECOVERY`, `LIN_ADVANCE` | Deliberately deferred until the machine prints reliably |

---

## 7. UNVERIFIED VALUES — FLAG, DO NOT SILENTLY CHANGE

These are provisional. Only physical testing resolves them. They are **not** bugs to fix.

| Setting | Current | Confidence |
|---|---|---|
| `NOZZLE_TO_PROBE_OFFSET` | `{ -27, 0, 0 }` | X sign correct (probe sits left of nozzle). Magnitude **never measured**. Y assumed 0. Z deliberately 0 pending calibration. |
| E-steps (4th value in `DEFAULT_AXIS_STEPS_PER_UNIT`) | `140` | Reasonable for a stock CR-10S Pro extruder. Uncalibrated. Note: an earlier draft used `415`; that was a bad guess for a different extruder type and was corrected. |
| `INVERT_X_DIR` | `true` | Unverified |
| `INVERT_E0_DIR` | `true` | Unverified |
| `INVERT_Y_DIR` | `true` | Previously established on this machine |
| `INVERT_Z_DIR` | `false` | Should still be confirmed before first `G28` |
| `Z_MIN_PROBE_ENDSTOP_INVERTING` | `true` | Theoretically correct for NPN normally-open. Must be confirmed with `M119`. |

---

## 8. DECISION RULES

**Rule 1 — Never silence an error by changing a hardware fact.**
If a compile error would be resolved by changing something in sections 5 or 7, that is a signal, not a solution. Stop and report. The correct fix may be a wiring change on the physical machine, not a config edit.

**Rule 2 — Distinguish the three error classes.**
- *Syntax / structural* (missing `#endif`, typo, malformed macro) → fix freely, log it.
- *Sanity-check conflict* (`#error` from `Marlin/src/inc/SanityCheck.h`) → read the actual error text, find which two settings conflict, then check both against sections 5 and 6 before deciding which to change. Report your reasoning before editing.
- *Hardware mismatch* (a setting is wrong because the machine is wired a certain way) → do not fix. Report to the user.

**Rule 3 — Explain before you edit.** State what you're changing, why, and which brief section supports it.

**Rule 4 — The user's physical observation wins.** If they say a motor turned the wrong way, that is ground truth regardless of what the config implies.

**Rule 5 — Scope discipline.** No refactoring, no tidying, no enabling features that weren't requested, no "while I was in there" changes.

---

## 9. YOUR TASK

### Phase 1 — Orient
1. Read this brief fully.
2. Create `BUILD-LOG.md`.
3. Read the three modified files and confirm they match section 5. Report any discrepancy **without fixing it**.

### Phase 2 — Build
4. Install PlatformIO if not present.
5. Build: `pio run -e STM32G0B1RE_btt`
6. Report the complete result — success or full error text.

### Phase 3 — Resolve
7. Apply section 8's rules to any errors. Explain each proposed fix before making it.
8. Rebuild until clean.

### Phase 4 — Deliver
9. Report the exact `firmware.bin` path.
10. Give SD-card flashing instructions for this board (card format, filename requirements, what the board does on boot, how to tell it succeeded).

### Phase 5 — Support commissioning
11. The user will run the section 11 sequence on the physical printer and report results — `M119` output, jog directions, measurements.
12. Translate those observations into config changes, rebuild, and hand back a new binary.

---

## 10. WHEN YOU NEED INFORMATION YOU DON'T HAVE

**You cannot query ChatGPT or any other assistant directly.** You have no connection to them. What you can do is write a precise question for the user to relay.

Put such questions in `BUILD-LOG.md` under "Open questions for the user," and also state them in chat. Format each as:

```
QUESTION [n]
What I need to know:      <the specific fact>
Why it matters:           <what decision it unblocks>
How it could be answered: <measurement / observation / lookup>
Who can answer:           [user's own printer] / [outside research] / [design-history assistant]
```

Routing guidance:
- **Physical facts** (wire routing, motor direction, measurements, component labels) → only the user, at the printer. No assistant can answer these, and an assistant that appears to answer them confidently is guessing. This already happened once in this project: an assistant asserted an `M119` test had established the probe polarity when no such test had been run.
- **Design rationale** ("why is this pin overridden?", "was this deliberate?") → the design-history assistant, via the user. Usually this brief already answers it — check first.
- **External documentation** (board specs, Marlin feature semantics) → you may have this knowledge already, or the user can look it up. Prefer reading the actual Marlin source in this tree over asking; it is authoritative and it is right here.

Treat any relayed answer as a claim to verify, not a fact. If an answer contradicts this brief or the source tree, say so rather than accepting it.

---

## 11. FIRST-BOOT COMMISSIONING SEQUENCE

Give this to the user once a clean binary exists. **Order matters** — several steps can crash the nozzle into the bed if done early.

**Pre-power checks:** PSU is 24V · heater, bed, all three fans are 24V parts · probe brown wire traced to the 24V rail.

**Step 1 — Reset EEPROM after flashing**
```
M502
M500
```

**Step 2 — Endstop and probe logic**
```
M119
```
Expected: X and Y each read `open` released, `TRIGGERED` pressed. Probe reads `open` with nothing near it, `TRIGGERED` when metal is held to its face.
If the probe reads inverted → flip `Z_MIN_PROBE_ENDSTOP_INVERTING`, rebuild, reflash.

**Step 3 — Motor directions (NO homing yet)**
Move the gantry to mid-travel by hand first. Jog small `+X`, `+Y`, `+Z` moves.
- `+X` → increasing X, else flip `INVERT_X_DIR`
- `+Y` → increasing Y, else flip `INVERT_Y_DIR`
- **`+Z` must move the nozzle AWAY from the bed** — confirm this before ever running `G28`. Else flip `INVERT_Z_DIR`.

**Step 4 — Fans**
Heat the hotend past 50°C: FAN1 must start on its own. Enable a motor: FAN2 should run. `M106 S255` should spin only FAN0.

**Step 5 — Extruder direction** (hotend ≥200°C)
Extrude 10 mm. Filament must feed toward the nozzle. Else flip `INVERT_E0_DIR`.

**Step 6 — Homing**
`G28 X Y` first. Full `G28` only after Z direction and probe logic are confirmed. Hand near the power switch.

**Step 7 — Probe offset**
Measure probe-to-nozzle X and Y with calipers → `M851 X__ Y__`. Paper-test Z → `M851 Z-__`. Then `M500`.

**Step 8 — E-steps**
Mark 120 mm of filament, extrude 100 mm, measure the remainder.
`new = old × 100 ÷ actually_extruded` → `M92 E__` → `M500`.

**Step 9 — PID**
```
M303 E0 S200 C8 U1
M303 E-1 S60 C8 U1
M500
```

**Step 10 — Mesh**
`G29` → inspect values for sanity → `M500`.

**Step 11 — First print**, watching layer one with babystepping ready.

---

## 12. KNOWN OPEN ITEMS

- **Filament runout sensor.** The CR-10S Pro shipped with one; it is not currently wired. PC15 is taken by the probe, but **PC2 (Z-STOP) is free** and is the natural candidate. Requires identifying the stock sensor's wiring first, then a custom `FIL_RUNOUT_PIN`. Do not enable `FILAMENT_RUNOUT_SENSOR` until that's resolved.
- **Unidentified upper-frame switch.** The user mentioned a possible switch near the top of Z travel. The CR-10S Pro has no stock Z limit switch, so this may be aftermarket or unrelated. Do not configure anything around it until traced.
- **Thermistor tables.** `1`/`1` is correct for stock parts. Only consider `11` if a thermistor was replaced with a documented 100K B3950.
- **Post-commissioning tuning.** Raise accelerations, consider `PIDTEMPBED`, `LIN_ADVANCE`, and TMC current tuning via `M906` — all deferred until the machine prints reliably.

---

## 13. PROJECT HISTORY — MISTAKES ALREADY MADE

Listed so they aren't repeated.

1. **A prior AI-assisted firmware attempt produced multiple errors**, largely from losing track of earlier decisions mid-session. This is why section 1 exists.
2. **`Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` was left enabled** in an early draft while the probe was on a custom pin — a direct conflict. Caught and fixed.
3. **All three probe wires were initially suggested to land on E0-STOP.** Wrong: the sensor needs 24V that the header cannot supply. Corrected in section 4.
4. **E-steps were initially set to 415**, a guess borrowed from a geared extruder. Corrected to 140 for the stock CR-10S Pro extruder — still uncalibrated.
5. **`E0_AUTO_FAN_PIN` was left at `-1`**, meaning the hotend heatbreak fan would never have run automatically. Found late. This would have caused heat-creep jams on the first print.
6. **An assistant asserted an `M119` probe test had already been performed** when it had not. Do not accept claimed physical results without the user confirming they personally ran the test.
