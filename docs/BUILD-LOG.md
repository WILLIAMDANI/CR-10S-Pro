# BUILD-LOG.md — CR-10S Pro → SKR Mini E3 V3.0 + TFT35 E3 V3.0.1

This file is append-only. Do not rewrite or trim history — add new entries at the bottom of each section.

## Session log
- [2026-09-17] Read MASTER-BRIEF-FOR-CLAUDE-CODE.md in full before touching any file.
- [2026-09-17] Read all three provided source files (Configuration.h, Configuration_adv.h, pins_BTT_SKR_MINI_E3_V3_0.h) in full.
- [2026-09-17] Inspected target repo `williamdani/cr-10s-pro`: brand-new, empty, zero commits, no branches on origin. This is not an existing Marlin checkout — the whole source tree had to be established from scratch.
- [2026-09-17] Brief says "Marlin 2.1.2.8". Confirmed the exact matching upstream source: cloned MarlinFirmware/Marlin (read-only, via add_repo), fetched full history of `bugfix-2.1.x`, found git tag `2.1.2.8` (commit 1cd56c4, 2026-06-25). Verified its stock `Marlin/Configuration.h` and `Configuration_adv.h` both declare `CONFIGURATION_H_VERSION 02010206` / `CONFIGURATION_ADV_H_VERSION 02010206`, exactly matching the version numbers in the two user-provided files. This confirms the provided config files were authored against this exact upstream snapshot, not some other point release — using any other commit risked a SanityCheck.h version-mismatch error or, worse, silent incompatibility.
- [2026-09-17] Exported the full `2.1.2.8` tree (`git archive 2.1.2.8`) into the (empty) target repo root.
- [2026-09-17] Overwrote the three files with the user-provided, deliberately-modified versions:
  - `Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h`
  - `Marlin/Configuration.h`
  - `Marlin/Configuration_adv.h`
- [2026-09-17] Diffed all three against the stock 2.1.2.8 versions to verify every change matches brief section 5. Result: **full match, no unexplained changes**. Details below under "Changes I made" (these are the user's pre-existing edits, not edits I made this session, but logging them here satisfies the brief's requirement to confirm section 5 before doing anything else).
- [2026-09-17] Committed the baseline tree (commit `57df68b`).
- [2026-09-17] Installed PlatformIO 6.2.0 via pip (not previously present in this environment).
- [2026-09-17] Ran `pio run -e STM32G0B1RE_btt`. **Build blocked, not a code error** — see "Open questions" below. This is an environment/infra issue, not a firmware bug, so per brief Rule 1 no config or source file was touched in response to it.
- [2026-10-04] User issued a direct "change of role" instruction after the heater/fan non-function and "firmware is finicky/freezes" reports: stop sampling, audit everything with no shortcuts, work on a separate branch, rebuild+log+track every change, bisect instead of guessing, and never claim "hardware" without a named measurement. Treated as binding and superseding prior looser working style.
- [2026-10-04] Cloned three independent reference sources to compare against (none of these existed in this repo before today): (1) MarlinFirmware/Configurations repo → the official Creality CR-10S + BigTreeTech SKR Mini E3 3.0 example (exact printer+board match), (2) bigtreetech/Marlin fork, branch `SKR-mini-E3-V3.0-G0B1` → BTT's own maintained config for this exact board, (3) re-confirmed MarlinFirmware/Marlin tag `2.1.2.8` (already cloned previously) as the stock baseline, re-checked out to the exact tag after discovering it had drifted to `bugfix-2.1.x` HEAD mid-session (see below).
- [2026-10-04] Wrote a parser (`diffdefs4.py`, scratchpad-only, not committed) that extracts every `#define NAME value` from `Configuration.h`/`Configuration_adv.h` in this repo vs. all three references, normalizes "absent" and "commented-out" to the same DISABLED state, and reports every row where our value differs from stock OR the name matches a curated list of structural/safety keywords (serial, baud, TMC UART, thermal protection, mintemp/maxtemp, watchdog, heater/fan pins and polarity, probe pins and polarity, endstop polarity, driver type, motherboard, cold-extrusion guards, kill/power-loss pins, emergency parser, runaway timers). Deliberately excluded pure per-printer tuning numbers (PID gains, acceleration, jerk, steps/mm, bed size, offsets) since those are expected to differ legitimately.
- [2026-10-04] First run produced 1239 then 954 "differences," almost all spurious — the stock clone had moved to the latest `bugfix-2.1.x` HEAD (`CONFIGURATION_H_VERSION 02010300`) instead of staying on tag `2.1.2.8`. Re-checked out the exact tag, verified the version line matched, re-ran. Final meaningful row count: 61.
- [2026-10-04] Manually cross-checked the pins file (`pins_BTT_SKR_MINI_E3_V3_0.h`) by hand (not run through the script, since its `#define` syntax needed separate review) for probe pin, filament-runout pin, heater pins, fan pins, TEMP pins, and TMC2209 slave addresses, against the same three references. Result: byte-identical everywhere except the two already-documented, already-approved probe-remap lines (`Z_MIN_PROBE_PIN` PC14→PC15, `FIL_RUNOUT_PIN` disabled).
- [2026-10-04] Manually checked `X_CURRENT`/`Y_CURRENT`/`E0_CURRENT` by hand after noticing the automated script correctly skipped them (our value equals the *stock* A4988-era default of 800mA, so the "changed from stock" filter didn't fire) — but both the official example and the BTT fork use markedly lower, TMC2209-appropriate values (580/580/650mA). This is a real finding the automated audit structurally could not catch alone; logged separately from the 61-row table.
- [2026-10-04] Created branch `bisect/batch-audit` off this branch's HEAD (`386ae5b`) per Rule 2 — did not touch `Marlin/Configuration.h`, `Marlin/Configuration_adv.h`, or the pins file on this (main) branch. Built three cumulative batches on that branch for hardware bisection, none compiled (sandbox PlatformIO registry block still in effect — see existing open question):
  - `c964220` Batch 0 — official MarlinFirmware/Configurations CR-10S + SKR Mini E3 3.0 example verbatim, stock pins file (no probe remap at all). This is the pure "known-good reference" build with zero of this project's own changes.
  - `1aacf31` Batch 1 — Batch 0 + this repo's motor currents (`X/Y_CURRENT` 580→800, `Z_CURRENT` 580→1000, `E0_CURRENT` 650→800).
  - `e49a451` Batch 2 — Batch 1 + this repo's full probe architecture (pins file remap, `Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` off, `USE_PROBE_FOR_Z_HOMING`/`FIX_MOUNTED_PROBE`/`MULTIPLE_PROBING`/`Z_SAFE_HOMING` on).
  - Pushed to `origin/bisect/batch-audit`. Verified afterward that `claude/master-brief-review-rabxqg` (this branch) is unchanged — clean diff on all three protected files, log still ends at `386ae5b`.
- [2026-10-04] Delivered the required A–E report (builds table, full diff table, batch/test plan, FOR CHATGPT question, newest-.bin link) to the user in chat. No new config changes made to this (main) branch as part of this entry — audit and bisection work only, per Rule 2.

## Changes I made
(This session did not need to change any of the settings covered by brief sections 5–7. The following entries record the pre-existing customizations found in the three uploaded files, verified against the brief, not new edits.)

- `Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h:71` — `Z_MIN_PROBE_PIN` PC14 → PC15. Matches brief §5.1. Confirmed did not change.
- `Marlin/src/pins/stm32g0/pins_BTT_SKR_MINI_E3_V3_0.h:84-86` — `FIL_RUNOUT_PIN` block commented out (was PC15). Matches brief §5.1. Confirmed did not change.
- `Marlin/Configuration.h:91` — `MOTHERBOARD` → `BOARD_BTT_SKR_MINI_E3_V3_0`. Matches §5.2.
- `Marlin/Configuration.h:104` — `SERIAL_PORT` → `2`. Matches §5.2.
- `Marlin/Configuration.h:117` — `BAUDRATE` → `115200`. Matches §5.2.
- `Marlin/Configuration.h:126` — `SERIAL_PORT_2` → `-1` (explicitly enabled/set). Matches §5.2.
- `Marlin/Configuration.h:164-178` — X/Y/Z/E0 `_DRIVER_TYPE` → `TMC2209`. Matches §5.2.
- `Marlin/Configuration.h:1065` — `USE_ZMIN_PLUG` disabled. Matches §5.2 and §6 (no Z endstop switch installed).
- `Marlin/Configuration.h:1151` — `Z_MIN_PROBE_ENDSTOP_INVERTING` → `true`. Matches §7 (flagged there as **unverified**, theoretically correct for NPN N.O., to be confirmed with M119).
- `Marlin/Configuration.h:1199` — E-steps → `140` (4th value). Matches §7 (flagged unverified; note in-file correctly references the earlier bad guess of 415 from brief §13.4).
- `Marlin/Configuration.h:1219,1234-1236` — accelerations lowered to conservative commissioning values (500/500/100/5000 max; 500/1000/500 print/retract/travel). Matches §5.2.
- `Marlin/Configuration.h:1305` — `Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN` disabled. Matches §5.2 (this was the bug described in §13.2 — confirmed it is correctly disabled here, not re-introduced).
- `Marlin/Configuration.h:1308` — `USE_PROBE_FOR_Z_HOMING` enabled. Matches §5.2.
- `Marlin/Configuration.h:1323` — `Z_MIN_PROBE_PIN` → `PC15`, mirrors the pins file. Matches §5.2.
- `Marlin/Configuration.h:1343` — `FIX_MOUNTED_PROBE` enabled. Matches §5.2.
- `Marlin/Configuration.h:1514` — `NOZZLE_TO_PROBE_OFFSET` → `{ -27, 0, 0 }`. Matches §7 (unverified magnitude, flagged not fixed).
- `Marlin/Configuration.h:1574` — `MULTIPLE_PROBING` → `2`. Matches §5.2.
- `Marlin/Configuration.h:1673` — `INVERT_X_DIR` → `true`. Matches §7 (unverified).
- `Marlin/Configuration.h:1686` — `INVERT_E0_DIR` → `true`. Matches §7 (unverified).
- `Marlin/Configuration.h:1707,1710` — `Z_HOMING_HEIGHT` 4 / `Z_AFTER_HOMING` 10 enabled. Matches §5.2.
- `Marlin/Configuration.h:1727-1736` — bed/Z travel → 300×300×400. Matches §5.2 (CR-10S Pro spec).
- `Marlin/Configuration.h:1908,1923,1994,2004` — `AUTO_BED_LEVELING_BILINEAR`, `RESTORE_LEVELING_AFTER_G28`, `GRID_MAX_POINTS_X` 5, `EXTRAPOLATE_BEYOND_GRID` enabled. Matches §5.2.
- `Marlin/Configuration.h:2125` — `Z_SAFE_HOMING` enabled. Matches §5.2.
- `Marlin/Configuration.h:2211,2216,2497` — `EEPROM_SETTINGS`, `EEPROM_AUTO_INIT`, `SDSUPPORT` enabled. Matches §5.2.
- `Marlin/Configuration.h:INVERT_Y_DIR / INVERT_Z_DIR` — left at stock-derived values per brief §7 (Y=true previously established, Z=false unverified). Confirmed present, did not change.
- `Marlin/Configuration_adv.h:536,538` — `USE_CONTROLLER_FAN` + `CONTROLLER_FAN_PIN` → `FAN2_PIN`. Matches §5.3.
- `Marlin/Configuration_adv.h:638` — `E0_AUTO_FAN_PIN` → `FAN1_PIN`. Matches §5.3 — this is the critical fix called out in brief §13.5.
- `Marlin/Configuration_adv.h:2067,2090` — `BABYSTEPPING` + `BABYSTEP_ZPROBE_OFFSET` enabled. Matches §5.3.
- `Marlin/Configuration_adv.h:2775` — `Z_CURRENT` → `1000`. Matches §5.3.

No settings from brief §6 ("Do Not Enable") were found enabled: confirmed absent — `Z2_DRIVER_TYPE`, `NUM_Z_STEPPER_DRIVERS`, `Z_MULTI_ENDSTOPS`, `Z_STEPPER_AUTO_ALIGN`, `BLTOUCH`, `PROBE_MANUALLY`, `NOZZLE_AS_PROBE`, `SENSORLESS_PROBING`, `SENSORLESS_HOMING`, `USE_ZMAX_PLUG`, `TFT_COLOR_UI`/`TFT_LVGL_UI`/`CR10_STOCKDISPLAY`/DWIN/DGUS, `FILAMENT_RUNOUT_SENSOR`, `POWER_LOSS_RECOVERY`, `LIN_ADVANCE`.

**Update [2026-09-30] — housekeeping pass, no firmware/config content changed:**
User requested a repo organization pass ahead of bringing back physical test
results. None of `Configuration.h`, `Configuration_adv.h`,
`pins_BTT_SKR_MINI_E3_V3_0.h`, or anything Marlin needs to build was touched.
Changes:
- Moved `BUILD-LOG.md`, `HARDWARE-WIRING.md`, and
  `MASTER-BRIEF-FOR-CLAUDE-CODE.md` into `docs/` (via `git mv`) and updated
  every cross-reference to the new paths, including inside the brief itself
  and this log's own historical entries (path strings only — narrative left
  intact).
- Added `firmware/` with a `README.md` build table (filename/date/what
  changed/status) and SD-flashing steps. **Attempted a fresh build first** —
  `pio run -e STM32G0B1RE_btt` still fails identically to every prior attempt
  in this sandbox: `api.registry.platformio.org` returns 403 (org network
  policy). No `.bin` exists in this repo yet; `firmware/README.md` documents
  this honestly rather than showing a fabricated entry, and gives the two
  ways to actually get one (attach a locally-built binary, or fix the
  sandbox's registry access).
- Added `TEST-SCRIPTS/RESULT-ENTRY-TEMPLATE.md` (a single-test copy/paste
  block emphasizing exact raw printer output, not summarized results) and a
  "Reporting results back to Claude" section at the top of
  `TEST-SCRIPTS/README.md` pointing to it.
- Replaced the stock Marlin `README.md` with a project-specific one: status
  banner, hardware summary, the three modified files with links, a folder
  map, and a "Latest firmware" pointer (currently: none yet, see above).
- Did NOT merge to `main` — all of the above is on the existing feature
  branch only, per explicit instruction that this repo is not ready to share.

**[2026-10-04] First actual firmware fixes, based on the user's direct physical
observation (brief Rule 4 — user's observation outranks guessing from logs):**

- `Marlin/Configuration.h:1151` — `Z_MIN_PROBE_ENDSTOP_INVERTING` `true` → `false`.
  User directly confirmed, from watching the machine, that the probe's trigger
  logic is backwards. This was flagged unverified in brief §7 from the start;
  now resolved by physical test.
- `Marlin/Configuration.h:1675` — `INVERT_Z_DIR` `false` → `true`. User directly
  confirmed Z homed in the wrong direction. Also flagged unverified in §7;
  resolved the same way.
- `Marlin/Configuration.h:1673` — updated the `INVERT_X_DIR` comment to
  "confirmed" rather than "starting guess, verify" — user confirmed `+X` jog
  moves away from the X endstop as expected. Value itself (`true`) unchanged.
- Before making the Z changes, did a full pass of `Configuration.h` and
  `Configuration_adv.h` specifically for anything that could explain the fans
  and both heaters being completely unresponsive: `HEATER_0_INVERTING`/
  `HEATER_BED_INVERTING` (the only `HEATER_BED_INVERTING` in the file is
  inside a disabled `#if ENABLED(HEPHESTOS2_HEATED_BED_KIT)` block — inert),
  fan PWM/inversion settings (`FAN_SOFT_PWM`, `FAN_MIN_PWM`, `FAN_OFF_PWM` —
  all commented out, defaults apply), heater pins in the pins file (PC8/PC9,
  correct, not -1), and MINTEMP/MAXTEMP/`EXTRUDE_MINTEMP` (all sane values,
  nothing blocking). **Found nothing wrong in the code for fans or heaters.**
  Reporting this as a genuine negative result, not a dodge: the two most
  likely remaining explanations are (a) a real hardware/wiring issue
  (connector, MOSFET, fuse — exactly what a separate ChatGPT session
  concluded independently for FAN0 on this same project), or (b) the TFT
  console's demonstrated unreliability (the `z_min`/`z_probe` mislabeling and
  the `M105` "black screen" already logged above) is also swallowing or
  misrepresenting the heater/fan command results. Direct USB serial testing
  (bypassing the TFT) remains the fastest way to tell these apart and hasn't
  been done yet.

## Open questions for the user

**[2026-10-03] First physical test run received.** Raw results saved verbatim
at `TEST-SCRIPTS/regression-runs/2026-10-02-pending-sha.md`. Summary: TC-001,
002, 003, 039 (boot/TFT) all PASS. Everything from TC-004 onward (E-stop,
driver comm, fans, heaters) reported FAIL, plus free-form notes on Z
homing/probe behavior and X/Y jogging. Analysis before touching anything —
per Rule 1, no config or firmware file was changed in response to this data:

- **Leading hypothesis for TC-005/006/014/015/016 and the heater failure:**
  `M112` (TC-004) is designed to halt everything and refuse further commands
  until the board is reset — that is correct, intended behavior, not a bug.
  If the board was not power-cycled between TC-004 and the tests that follow
  it, every one of those "FAILs" could be the same single cause (board still
  killed) rather than five independent defects. Asked the user to confirm
  whether a reset happened, and to re-test `M105`/`M104`/`M140` fresh after a
  power cycle, with no `M112` involved, before concluding anything about
  drivers or heaters.
- **Z-axis/probe behavior (Group D) treated as a real, separate finding,
  not noise.** The user ran full `G28` (not the isolated `M119` checks in
  TC-007–009) and described: (a) with the probe clear, Z drove *upward*
  during homing and gave up — the homing search should drive toward the bed;
  this is the signature of `INVERT_Z_DIR` being backwards, which brief §7
  already flags as unverified. (b) With the probe deliberately held
  triggered, Z kept driving down the whole time, only reacting once released
  — Marlin should refuse to move at all if the probe already reads triggered
  before the search starts; this is the signature of
  `Z_MIN_PROBE_ENDSTOP_INVERTING` also being backwards, also flagged
  unverified in §7. Both are plausible and both are exactly the kind of
  setting brief Rule 1 says must be confirmed by physical test, not guessed —
  declined to flip either setting on a paraphrased description of a full
  `G28` run. Also flagged to the user that this skipped the safety order the
  brief specifies: TC-012 (manual `+Z` jog, hand near the power switch) is
  meant to happen *before* any `G28`, specifically to catch a bad Z direction
  by hand rather than during an automated homing search. This time the
  failure direction happened to be the safe one (away from the bed), but
  that was luck, not confirmation, and the user was asked not to run further
  `G28` attempts until the direction is confirmed via isolated `M119` first.
- Asked for exact verbatim on-screen/serial text for TC-015 and TC-016
  (notes were too garbled to act on — e.g. "notification no move ok p15 B3")
  — pointed back to `RESULT-ENTRY-TEMPLATE.md`'s "exact printer output" field
  for future reports.
- Noted the run's header still has unfilled placeholders — asked which
  commit this firmware was actually built from, and asked the user to attach
  the actual `firmware.bin` they built and flashed locally, since it passed
  TC-001/002 but was never added to `firmware/`.

No GitHub Issues opened yet for any of the above — premature until the
reset/power-cycle question resolves which failures (if any) are independent
of each other.

**Update [2026-10-03] — user provided M119 photos, then the actual flashed
`firmware.bin`. Binary inspected directly (strings on the raw .bin, no
toolchain needed) rather than guessing. Findings, and one correction to the
prior update's analysis:**

- The user initially worried this firmware came from "the other Claude chat"
  (a different, possibly unconfigured build). Checked the binary directly:
  `FIRMWARE_NAME:Marlin 2.1.2.8`, `MACHINE_TYPE:CR-10S Pro`, and a config date
  of `2026-06-24` are all embedded in it — matches this repo's actual
  `Configuration.h`/pins file exactly (`MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V3_0`,
  `HEATER_0_PIN PC8`, `HEATER_BED_PIN PC9`, `FAN0/1/2_PIN` PC6/PC7/PB15,
  `USE_CONTROLLER_FAN`/`CONTROLLER_FAN_PIN FAN2_PIN`,
  `E0_AUTO_FAN_PIN FAN1_PIN` — all present since the very first commit,
  confirmed via `git log -p`, never touched). **This is this repo's build.**
  A separate narrative the user relayed from ChatGPT, describing "fixing" the
  motherboard selection and heater pins, describes symptoms of an
  unconfigured/stock Marlin checkout — not anything that was ever wrong in
  this repo. Likely explanation: a separate local folder/download, unrelated
  to this one. No action needed on this repo either way, since the settings
  it describes "fixing" already match.
- **Correction to this file's own prior update:** the previous entry
  theorized the M119 `z_min:` line was noise from the physically-unused
  Z-STOP (PC2) pin floating. That reasoning was based on this repo's
  *source*, not the actual compiled binary. Checking the real `.bin` directly:
  the literal string `z_min` is **not compiled in at all** (absent from the
  binary), while `z_probe` **is** present and correctly structured. Marlin
  physically cannot emit a `z_min:` line from this exact build. This means
  the TFT's display of `z_min: TRIGGERED`/`open` was almost certainly the
  TFT's own generic endstop-label template being applied to whatever it
  received (likely the real `z_probe:` line), not a literal relay of Marlin's
  field name — so the earlier "it's just floating-pin noise, ignore it"
  guidance was probably wrong, and was retracted to the user. The two
  different readings between the two M119 captures may reflect a genuine,
  meaningful probe state change after all, not noise.
- Saved the binary at `firmware/firmware-2026-10-03-v1.bin` and logged it in
  `firmware/README.md`'s build table as **untested** (verified to match this
  repo; hardware test results still inconclusive, not yet a clean pass or a
  confirmed fail).
- Asked the user to re-run `M119` and the heater commands over **direct USB
  serial** (bypassing the TFT console entirely) for the next round of
  testing, since the TFT has now been implicated in at least two confusing
  results (this mislabeling, and the earlier `M105` "black screen"). No
  firmware/config changes made — the puzzle at this point looks increasingly
  like "the TFT's console view can't be fully trusted as a raw data source,"
  not a firmware defect.

QUESTION [1]
What I need to know:      This sandbox session's outbound network policy blocks `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, and `collector.platformio.org` (confirmed via the proxy status endpoint: each returns HTTP 403, "policy denial"). PlatformIO needs the first two to download the `ststm32` platform, the STM32G0 Arduino framework, and the ARM GCC toolchain — none of that is present locally and there is no code-only substitute.
Why it matters:           The firmware cannot be compiled at all until these downloads succeed. This blocks Phase 2/3/4 of the brief entirely — it is not a config or source problem, so I have not touched any file in response to it (see brief Rule 1).
How it could be answered: Either (a) allow the three hosts above in this Claude Code environment's network egress policy and re-run the build in a new session, or (b) build locally instead, following the "Deliver" instructions I've prepared below once you tell me which route you prefer.
Who can answer:           [user, via environment settings] — this is an infrastructure/environment setting, not a hardware or design-history question. See https://code.claude.com/docs/en/claude-code-on-the-web for how environment network policy is configured.

**Update [2026-09-17, later same session]:** User reported allowlisting `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, `dl.registry.platformio.org`, `dl.registry.nm1.platformio.org`, `registry.platformio.org`. Re-ran `pio run -e STM32G0B1RE_btt` in this same session: **still blocked**, identical 403 from the egress proxy on `api.registry.platformio.org` and `api.registry.nm1.platformio.org` (plus `collector.platformio.org`, PlatformIO's telemetry endpoint — harmless if left blocked). Confirmed via the proxy's own status endpoint, not just the pio error text. This session's proxy evidently has not picked up the policy change — network policy is a property of the environment and this running session was likely started before the change was saved, so it is still enforcing the old policy. Have NOT claimed success; told the user directly. Waiting on either a fresh session against this environment, or confirmation the setting actually persisted.

**Update [2026-09-20]:** User relayed a concern from another Claude chat: `MASTER-BRIEF-FOR-CLAUDE-CODE.md` was never actually committed to this repo (it only ever existed as an uploaded chat attachment, not a tracked file) — only this log reflected its contents. Confirmed this was correct: `find . -iname "MASTER-BRIEF*"` returned nothing. Wrote the brief's full text into `MASTER-BRIEF-FOR-CLAUDE-CODE.md` at the project root (both this file and the brief were later moved into `docs/` during a 2026-09-30 housekeeping pass) from this session's own conversation history (verbatim, unchanged) and committed it, so it survives session resets and a fresh session reading "the brief in the project root" will actually find it.

**Update [2026-09-24] — BUILD SUCCEEDED, on the user's own machine.** After confirming the sandbox environment's egress policy still blocked the PlatformIO registry (see below), the user built locally in VS Code/PlatformIO on their own PC instead, which has normal internet access. Full result:

```
Environment      Status    Duration
---------------  --------  ------------
STM32G0B1RE_btt  SUCCESS   00:04:03.992
```
- RAM:   11.4% used (16,876 / 147,456 bytes)
- Flash: 29.6% used (152,684 / 516,096 bytes)
- Output: `.pio\build\STM32G0B1RE_btt\firmware.bin` (on the user's machine, not in this sandbox)

Two compiler warnings, both reviewed:
1. `"Your Configuration provides no method to acquire user feedback!"` — informational only, expected given no LCD/host-prompt feature is enabled (correct per brief §6, the TFT35 is its own host, not a Marlin-native display). Not a defect.
2. `"Motherboard DIAG jumpers must be removed when SENSORLESS_HOMING is disabled."` — **real, actionable, physical hardware note**, not a firmware bug. Per brief §6, `SENSORLESS_HOMING` is correctly disabled (physical X/Y endstops are wired and used). The SKR Mini E3 V3.0 board has DIAG jumper pins near the TMC2209 drivers that route each driver's DIAG (stall-detect) signal onto the endstop input pin, for use with sensorless homing only. If any jumper caps are physically installed on this board's DIAG headers, they must be removed before relying on the real endstop switches — otherwise the DIAG signal could interfere with the genuine endstop signal on the same pin. Logged as a new physical pre-flight check (added to §4 checklist mentally, not a config change) rather than a config item, since it's a physical jumper on the board, not a `#define`. No firmware action needed or possible — routed to the user per brief §10 ("physical facts → only the user, at the printer").

No source/config changes made in response to either warning — both are either expected-and-correct or purely physical/hardware, consistent with brief Rule 1.

**Update [2026-09-29]:** User shared a hand-drawn wiring schematic (tabulated by another AI assistant) that lists the Z probe as connected to **Z-STOP**. This directly contradicts the original master brief and this firmware's actual configuration, both of which place the probe on **E0-STOP (PC15)** — precisely because this machine has no Z endstop switch at all and Z-STOP (PC2) is documented as physically empty. Per Rule 4 (user's physical observation wins) and Rule 1 (never silence a signal by assuming), this needed to be raised, not resolved by guessing which source is right — especially since the brief's own history (§13.6) already records one prior incident of an assistant asserting a physical result that was never actually tested. Did NOT change `Z_MIN_PROBE_PIN` in either the pins file or `Configuration.h` in response to this. Also corrected two smaller mismatches in the same schematic for the test docs: the probe is inductive (SZC-M18-8DN, metal-only trigger), not capacitive as labeled; and the extruder type (Bowden vs. direct-drive) isn't confirmed anywhere in the original brief, so it's flagged rather than asserted either way.

QUESTION [2]
What I need to know:      Is the Z probe's signal wire physically landed on the SKR Mini E3's Z-STOP terminal (PC2), or on E0-STOP (PC15) as the firmware currently assumes?
Why it matters:           If it's really on Z-STOP, `Z_MIN_PROBE_PIN` in both `pins_BTT_SKR_MINI_E3_V3_0.h` and `Configuration.h` need to change from PC15 to PC2, `USE_ZMIN_PLUG` may need reconsidering, and — most importantly — Z homing (`G28`) will currently never see the probe trigger, meaning the nozzle would drive straight into the bed. TC-009 and everything depending on it (homing, calibration, PID, EEPROM tests) are blocked in TEST-SCRIPTS/TEST-CASES.md until this is resolved.
How it could be answered: Physically trace the probe's black/signal wire back from the sensor to the exact terminal block it's screwed into on the SKR Mini E3 board, and read the silkscreen label at that terminal.
Who can answer:           [user's own printer] — this is a physical wiring fact; no assistant (including whichever one produced "Z-STOP") can substitute for tracing the actual wire.

**RESOLVED [2026-09-29]:** User provided their own hand-annotated wiring schematic (photos of the actual build, with labeled wires traced to board connectors) — `docs/HARDWARE-WIRING.md` now holds the full table derived from it. The schematic explicitly labels the Z-probe wire "E0-STOP," and separately marks the breakout pins where Z-STOP would connect as "Not Used" — independent confirmation of the original brief's claim that Z-STOP (PC2) is physically empty. The "Z-STOP" claim in the earlier ChatGPT-generated table was a transcription error on that assistant's part, not something in the user's actual schematic. Firmware's `Z_MIN_PROBE_PIN` (PC15/E0-STOP) is correct as-is — no change made. TC-009 and the tests gated behind it in `TEST-SCRIPTS/TEST-CASES.md` are now unblocked.

**Update [2026-09-28]:** User asked how to document build/test failures going forward and shared a Jira-based test-management proposal (Test Case / Regression Cycle / Bug, from another AI assistant) for review. Recommended keeping that same conceptual model (test case vs. execution vs. bug, strict PASS/FAIL/BLOCKED/NOT RUN) but implementing it as versioned files in this repo rather than standing up Jira, since this project is one tester/one physical unit and git already provides the build-to-test traceability Jira would need extra integration for. Added `TEST-SCRIPTS/README.md` (workflow explanation), `TEST-SCRIPTS/TEST-CASES.md` (27 permanent test cases, TC-001–TC-027, covering boot, endstops/probe, motor directions, fans, homing/leveling, probe/E-step calibration, thermal safety, EEPROM persistence, and first-print reliability — each cross-referenced to the relevant docs/MASTER-BRIEF-FOR-CLAUDE-CODE.md section), and `TEST-SCRIPTS/regression-runs/TEMPLATE.md` for per-build result logging. Bugs are tracked as GitHub Issues in this repo rather than a separate system. This is infrastructure only — no test results exist yet; the user has not yet specified what they observed as "non-functional," so no FAIL entries or bug issues were created (asked for specifics rather than guessing).

**Update [2026-09-29]:** Expanded the test suite from 27 to 37 test cases (renumbered — safe, no real run results exist yet) after reviewing a comprehensive test proposal the user got from another AI assistant. Adopted the genuinely useful additions: TMC2209 driver health (`M122`), driver current check (`M906`, specifically verifying the `Z_CURRENT` 1000mA bump), an early `M112` emergency-stop test, a thermistor-swap sanity check, cold-extrusion rejection, software travel-limit enforcement, a bed-side thermal-runaway test (previously only had the hotend version), and commanded-vs-measured travel accuracy. Declined the rest of that proposal's structure: a full per-test Test-ID/Manual-vs-Automated/Evidence-column format (duplicates process weight the user already asked to cut) and a from-scratch re-audit of every config line (already done and logged above). Also declined the granular TFT button/touch/encoder test list and per-file SD-card path tests as disproportionate to this project's scale; kept the existing single TFT connectivity check (TC-003) with a note that the TFT's buzzer is its own firmware and not wired to Marlin's `M300`.** User confirmed this is a fresh session against the same environment, with the allowlist update in place. Re-verified with direct `curl` probes (not just `pio`) before running the build: `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, and `dl.registry.platformio.org` all still return 403 ("gateway answered 403 to CONNECT (policy denial)") from the egress proxy. Ran `pio run -e STM32G0B1RE_btt` anyway to confirm — identical failure, `HTTPClientError` with no further detail during `Platform Manager: Installing ststm32 @ 17.1.0`. This is the **second consecutive fresh session** where this exact allowlist has failed to take effect, which suggests the block is not a stale per-session proxy cache but something about how the policy change itself was applied (typo in the allowlisted hostnames, change not saved, or an org-level policy that isn't overridden by environment-level settings). Reported this pattern to the user rather than retrying again. No source/config changes made. Have not attempted any workaround (manual package placement, alternate mirrors, etc.) since that would circumvent an explicit policy denial per /root/.ccr/README.md.

## Things I confirmed but did NOT change

- `Z_MIN_PROBE_PIN` override (pins file + Configuration.h) — intentional per §5.1/§5.2.
- `FIL_RUNOUT_PIN` disabled — intentional per §5.1.
- `Z_MIN_PROBE_ENDSTOP_INVERTING true` — unverified per §7, left as-is; only physical M119 test can resolve it.
- `NOZZLE_TO_PROBE_OFFSET { -27, 0, 0 }` — unverified magnitude per §7, left as-is.
- E-steps `140` — uncalibrated per §7, left as-is.
- `INVERT_X_DIR` / `INVERT_E0_DIR` set to `true` — unverified per §7, left as-is; only physical jog/extrude test can resolve.
- `INVERT_Z_DIR` — left at its provided value (false); unverified per §7.
- Conservative acceleration values — deliberate per §5.2, not "fixed" toward stock defaults.
