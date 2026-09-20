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

## Open questions for the user

QUESTION [1]
What I need to know:      This sandbox session's outbound network policy blocks `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, and `collector.platformio.org` (confirmed via the proxy status endpoint: each returns HTTP 403, "policy denial"). PlatformIO needs the first two to download the `ststm32` platform, the STM32G0 Arduino framework, and the ARM GCC toolchain — none of that is present locally and there is no code-only substitute.
Why it matters:           The firmware cannot be compiled at all until these downloads succeed. This blocks Phase 2/3/4 of the brief entirely — it is not a config or source problem, so I have not touched any file in response to it (see brief Rule 1).
How it could be answered: Either (a) allow the three hosts above in this Claude Code environment's network egress policy and re-run the build in a new session, or (b) build locally instead, following the "Deliver" instructions I've prepared below once you tell me which route you prefer.
Who can answer:           [user, via environment settings] — this is an infrastructure/environment setting, not a hardware or design-history question. See https://code.claude.com/docs/en/claude-code-on-the-web for how environment network policy is configured.

**Update [2026-09-17, later same session]:** User reported allowlisting `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, `dl.registry.platformio.org`, `dl.registry.nm1.platformio.org`, `registry.platformio.org`. Re-ran `pio run -e STM32G0B1RE_btt` in this same session: **still blocked**, identical 403 from the egress proxy on `api.registry.platformio.org` and `api.registry.nm1.platformio.org` (plus `collector.platformio.org`, PlatformIO's telemetry endpoint — harmless if left blocked). Confirmed via the proxy's own status endpoint, not just the pio error text. This session's proxy evidently has not picked up the policy change — network policy is a property of the environment and this running session was likely started before the change was saved, so it is still enforcing the old policy. Have NOT claimed success; told the user directly. Waiting on either a fresh session against this environment, or confirmation the setting actually persisted.

**Update [2026-09-20]:** User relayed a concern from another Claude chat: `MASTER-BRIEF-FOR-CLAUDE-CODE.md` was never actually committed to this repo (it only ever existed as an uploaded chat attachment, not a tracked file) — only `BUILD-LOG.md` reflected its contents. Confirmed this was correct: `find . -iname "MASTER-BRIEF*"` returned nothing. Wrote the brief's full text into `MASTER-BRIEF-FOR-CLAUDE-CODE.md` at the project root from this session's own conversation history (verbatim, unchanged) and committed it, so it survives session resets and a fresh session reading "the brief in the project root" will actually find it.

**Update [2026-09-17, new session]:** User confirmed this is a fresh session against the same environment, with the allowlist update in place. Re-verified with direct `curl` probes (not just `pio`) before running the build: `api.registry.platformio.org`, `api.registry.nm1.platformio.org`, and `dl.registry.platformio.org` all still return 403 ("gateway answered 403 to CONNECT (policy denial)") from the egress proxy. Ran `pio run -e STM32G0B1RE_btt` anyway to confirm — identical failure, `HTTPClientError` with no further detail during `Platform Manager: Installing ststm32 @ 17.1.0`. This is the **second consecutive fresh session** where this exact allowlist has failed to take effect, which suggests the block is not a stale per-session proxy cache but something about how the policy change itself was applied (typo in the allowlisted hostnames, change not saved, or an org-level policy that isn't overridden by environment-level settings). Reported this pattern to the user rather than retrying again. No source/config changes made. Have not attempted any workaround (manual package placement, alternate mirrors, etc.) since that would circumvent an explicit policy denial per /root/.ccr/README.md.

## Things I confirmed but did NOT change

- `Z_MIN_PROBE_PIN` override (pins file + Configuration.h) — intentional per §5.1/§5.2.
- `FIL_RUNOUT_PIN` disabled — intentional per §5.1.
- `Z_MIN_PROBE_ENDSTOP_INVERTING true` — unverified per §7, left as-is; only physical M119 test can resolve it.
- `NOZZLE_TO_PROBE_OFFSET { -27, 0, 0 }` — unverified magnitude per §7, left as-is.
- E-steps `140` — uncalibrated per §7, left as-is.
- `INVERT_X_DIR` / `INVERT_E0_DIR` set to `true` — unverified per §7, left as-is; only physical jog/extrude test can resolve.
- `INVERT_Z_DIR` — left at its provided value (false); unverified per §7.
- Conservative acceleration values — deliberate per §5.2, not "fixed" toward stock defaults.
