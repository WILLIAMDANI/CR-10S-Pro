# Codex review and handoff to Claude — CR-10S Pro firmware

Review date: 2026-10-10. Reviewed main checkout `71656c9`, including firmware source at `a15e1b4`, project history, wiring brief, regression records, quick-check sheets, build/release workflows, upstream Marlin 2.1.2.8, and BTT board/TFT documentation.

## Direction from the owner

The owner confirms the hardware and wiring are correct. Treat the documented wiring in `docs/HARDWARE-WIRING.md` as the baseline. Stop attributing the remaining failures to wiring, fuses, MOSFETs, or hardware without contrary measured evidence. Work with this review to investigate and fix firmware, TFT protocol integration, saved settings, build provenance, and test procedure. A successful compilation or a correct pin table is not proof that the printer works. Do not repeat broad audits without converting their findings into tested changes and an identifiable binary.

This review does not independently certify electrical hardware or establish the cause of every reported failure. It does establish several concrete software/documentation defects and unresolved contradictions. Do not claim the heaters are fixed until a representative functional check passes.

## Confirmed baseline

- Main firmware uses `BOARD_BTT_SKR_MINI_E3_V3_0`, target `STM32G0B1RE_btt`, TFT UART2 at 115200, and native USB as the second serial port.
- `INVERT_Z_DIR true`, `Z_MIN_PROBE_ENDSTOP_INVERTING false`, and probe PC15 are present at `a15e1b4`. These source files are unchanged through `71656c9`.
- Hotend PC8, bed PC9, part fan PC6, heatbreak fan PC7, controller fan PB15, thermistors PA0/PC4 match upstream board definitions. The PC15 probe override matches the owner's wiring. No arbitrary pin reassignment is justified.
- FAN1 is deliberately automatic; FAN2 is deliberately controller cooling. They are excluded from ordinary part-fan indexing by `Conditionals_post.h`. `M106 P1/P2` is not a valid substitute for testing those automatic functions in this configuration.
- Full upstream file comparison: 2,866 files identical; changes only in README, Configuration.h, Configuration_adv.h, and the board pins file. One upstream editor workspace file is absent. There is no hidden custom heater-control implementation in the main checkout.
- Downloaded released `firmware-main-a15e1b4.bin`: 152,952 bytes; SHA256 `19e8c8f1733515c82fddb911ab9ff9bd529fc80e7ee3cbfca2e8c3ef5488451e`. Embedded identity says Marlin 2.1.2.8, CR-10S Pro, build Oct 8 2026 20:14:07. Strings alone do not prove all configuration values or exact source provenance.

## Findings to act on

### 1. High: incomplete TFT35 host integration

BTT's TouchScreenFirmware README specifies general Marlin requirements including AUTO_REPORT_POSITION, M115_GEOMETRY_REPORT, M114_DETAIL, and REPORT_FAN_CHANGE. All four are disabled here. AUTO_REPORT_TEMPERATURES and EXTENDED_CAPABILITIES_REPORT are enabled. BTT also documents EMERGENCY_PARSER, HOST_ACTION_COMMANDS, HOST_PROMPT_SUPPORT and HOST_STATUS_NOTIFICATIONS for host dialogs; these are disabled. Onboard-media host reporting options LONG_FILENAME_HOST_SUPPORT and AUTO_REPORT_SD_STATUS are disabled too.

These are real integration gaps; they do not alone prove why PC8/PC9 or FAN0 appear unresponsive. Identify the installed TFT firmware/version and capabilities, then implement the required compatible Marlin host features as a coherent change. A serial-host TFT needs host protocol support even though it needs no native Marlin display driver. The existing 'no feedback method' warning should not be dismissed without reviewing host feedback support.

Source: `Marlin/Configuration_adv.h` around 1639, 1659, 2452, 3621–3679, 3863–3870; BTT README 'Marlin Dependencies'.

### 2. High: emergency-stop behavior needs an actual firmware test

EMERGENCY_PARSER is disabled in the main configuration, despite being enabled in the reconstructed bisect baseline and documented by BTT for host dialogs. The reported emergency-stop failure was never resolved by a controlled test.

Be precise: M112 still exists without EMERGENCY_PARSER. `queue.cpp` processes unnumbered critical commands early during normal serial ingestion, and `gcode.cpp` has the fallback handler. Do not claim M112 is absent or that every emergency stop necessarily waits for normal execution. The parser adds receive-path handling that must be checked during blocking operations and queue pressure on both UART2 and USB. Test idle stop and busy stop separately, record acknowledgments/errors and actual cessation, then reboot before continuing. Never present a serial software stop as a replacement for power cutoff during commissioning.

### 3. High: Z inversion contradicts the preserved physical test record

The original regression run says `ZMove - moves z+ moves z up & z-moves z down` before commit 386ae5b inverted Z. The same record reports abnormal homing and reversed probe behavior. Its flashed commit was unknown, while the later log says a user confirmation justified flipping both settings. These claims cannot establish the right direction for the current binary without reconciliation.

Keep the owner's wiring fixed. Do not blindly revert the value, and do not certify it from the macro alone. Establish a small relative positive-Z move with clearance, before homing, on the identified current binary; record the physical result. Separate initial G28 clearance raises, homing descent, probe-trigger response, and post-home raise. A G28 sequence can legitimately contain upward moves; interpreting every upward move as inverted Z is wrong. Require released probe=open and metal-triggered probe=TRIGGERED before any Z homing.

### 4. Medium: bed PID test is impossible with this build

PIDTEMPBED is disabled (`Configuration.h:770`), but the master brief Step 9 and TC-030 prescribe `M303 E-1 S60 C8 U1`. In this exact source, `M303.cpp` accepts H_BED only with PIDTEMPBED; otherwise it reports a bad heater identifier. This is a deterministic test/configuration mismatch, not broken bed hardware.

Either retain bang-bang bed control and remove bed-PID autotune from this workflow, or deliberately enable and validate bed PID in a separate justified change. M140 bed heating remains supported without bed PID.

### 5. High: quick-check and regression instructions can create misleading failures

- TC-004 demands M112 before the remaining tests but has no explicit mandatory reboot step in its procedure. The next tests may run against a killed board. Add the reboot and renewed M115/M105 readiness gate, including in the inlined regression template.
- MAIN-BUILD-QUICKCHECK omits M503/settings inspection, controlled default initialization, explicit FAN2 enabling command, exact relative Z-jog commands, released AND triggered probe expectations, and heater/fan shutdown commands. Inspection/backup must precede M502; resetting loses calibration. EEPROM_AUTO_INIT does not erase valid old settings on every flash. Valid old PID/current/steps/offset settings can override compiled defaults; direction and pin macros are compile-time and do not come from EEPROM.
- Hotend target S50 does not reliably demonstrate FAN1 operating ABOVE its 50°C measured-temperature threshold: regulation can settle below it. First establish safe heating at 50, then use a modest target above the threshold and observe actual temperature/fan response. The code condition is measured temperature >=50, not simply 'M104 S50 sent'.
- A FAN1 test blocked by a nonheating hotend is BLOCKED, not an independently established fan FAIL. Likewise TFT menu response is not proof the MCU executed a command.
- `M119` needs both clear and triggered readings, plus an explicit stop gate on reversed results. 'State flips correctly' alone is insufficient.
- TC-031/032 prescribe unplugging a thermistor during powered heating and expect THERMAL RUNAWAY or HEATING FAILED. An open thermistor normally tests MINTEMP/sensor-disconnect protection, which is a different failure path. These procedures do not establish thermal-runaway behavior with a valid sensor reading and introduce unnecessary live connector handling. Replace them with a clearly specified controlled safety-validation procedure; distinguish sensor-disconnect, heat-rise watch, and sustained thermal-runaway tests, and require a reboot after each deliberate fault.
- TC-038 calls `M48 P10 V2`, but Z_MIN_PROBE_REPEATABILITY_TEST is disabled (`Configuration.h:1603`), so M48 is not part of this build. Either enable the feature intentionally or mark the test unsupported. TC-033's oversized target tests target clamping, not sensor MINTEMP/MAXTEMP fault detection; label that distinction accurately and avoid a high-temperature physical trial merely to test parsing/clamping.

### 6. High: bisection conclusions and metadata overstate what was established

BISECT-QUICKCHECK says a Batch 0 heat/fan failure 'points at hardware, not firmware.' This is unjustified: baseline correctness, command transport, thermal faults, saved EEPROM, common Marlin/framework behavior and test execution still need examination. A CR-10S example is not an exact CR-10S Pro conversion with an inductive probe and a serial TFT. The later reconstructed Batch 0 is not the verbatim official example described by the workflow release body.

The BUILD-LOG claim that no version-matched official configuration branch exists is false as checked now: `MarlinFirmware/Configurations` has `release-2.1.2.8`, HEAD `f083973abeb6ece641e3437ddf03dc43a268c6a4`. That branch does not provide an exact CR-10S Pro + SKR Mini E3 V3 example; use it as a version-matched reference, never as proof of this conversion. Pin exact references and correct the narrative.

Batch 2 still has INVERT_Z_DIR false. Its quick-sheet must not invite Z motion/homing merely because the probe architecture was added. Preserve the same direction/probe gates used for the main binary. Do not flash old batches just to satisfy an unfocused bisection checklist.

### 7. Medium: stale source-of-truth documents and weak build identity

Master brief section 7 still lists Z direction false and probe inversion true. The log's 'confirmed but did not change' section also contains superseded values. Add clearly visible superseding notes to preserve history while preventing a future assistant from undoing the current configuration.

M115 compile date and generic machine-name strings cannot uniquely identify a commit, nor demonstrate heater pin values. Embed a short source revision in the firmware's supported version metadata; publish SHA256 and configuration manifest with each artifact. CI currently installs floating PlatformIO and uses a moving release tag. Pin build tooling and associate each result with the full source SHA. The release action does not explicitly set target_commitish, so do not assume the main-build tag identifies the source named in the release body. Review retained assets too: older binaries can remain alongside newer ones unless managed explicitly.

### 8. Medium: TMC diagnostics need correct expectations

TMC_DEBUG is disabled. M122 is nevertheless compiled under HAS_TRINAMIC_CONFIG and calls `test_tmc_connection` even without TMC_DEBUG. TC-005 can check communication, but its expected comprehensive driver/overtemperature report is not available with the current flags. Enable TMC_DEBUG if that report is required, or narrow the test. Do not diagnose silent M122 from TMC_DEBUG alone.

X/Y/E currents are still 800mA and Z is 1000mA. References for other printers do not prove these values wrong; tune deliberately from the installed motors and observed behavior. They do not explain both heater outputs failing at idle by themselves.

## Next work for Claude

1. Read this note and the owner's direction; correct the known test/documentation errors and reconcile Z evidence before automated motion.
2. Make one identifiable firmware change for TFT host integration/emergency handling, retaining confirmed wiring/pins and protection features. Explain which settings are required for the installed TFT and which are optional. Build and provide complete result and artifact hash.
3. Capture a fresh-session, command-by-command trace: M115 identity, M503 current settings, M105 actual and target temperatures, M119 clear/triggered. Compare a short direct-USB trace with the TFT path if possible; this isolates protocol integration, not a demand to rewire correct hardware. Preserve raw errors and `ok` responses.
4. After readiness, test FAN0 explicitly; FAN2 with M17 and M84 plus its configured timeout; hotend low-target rise and shutdown; FAN1 above its measured threshold; bed low-target rise and shutdown. For heater nonresponse record target acceptance and reported heater power (`@`/`B@` if available), not just a blank TFT notification. Stop on thermal errors; never disable protection to force a pass.
5. Only after direction/probe gates pass, test homing, offsets, mesh and extrusion calibration. Record actual results, not inferred passes. M112 tests end with a reboot before any later checks.
6. Answer each finding with a change, a source-backed rebuttal, or a named unresolved observation. Deliver a concise owner-facing status identifying what was actually fixed and what remains unverified.

## Research sources and limitations

- Marlin 2.1.2.8, commit `1cd56c4ccd483045eb5a92c99e3ad3b5ab1bea6d`: https://github.com/MarlinFirmware/Marlin/tree/2.1.2.8
- Version-matched configuration examples: https://github.com/MarlinFirmware/Configurations/tree/release-2.1.2.8/config/examples/Creality
- BTT SKR Mini E3 V3 hardware pinout/schematic/manual: https://github.com/bigtreetech/BIGTREETECH-SKR-mini-E3/tree/master/hardware/BTT%20SKR%20MINI%20E3%20V3.0
- BTT TFT host requirements: https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware#marlin-dependencies
- Printer-specific wiring, motor/probe observations and test history: this repository's owner-confirmed docs and regression record. A stock CR-10S configuration is not an exact hardware match for the converted CR-10S Pro.

No physical printer tests were performed in this review. No application source was changed. GitHub API access for issues is unavailable in this environment; this note is intended to be published as a Git branch file so Claude can read it. Local build result is recorded below when complete.

## Local build verification

Registry access became available during review. Built unchanged main source at `71656c9` with PlatformIO 6.1.19, `pio run -e STM32G0B1RE_btt -j 4`: SUCCESS in 106.89 seconds. Output `.pio/build/STM32G0B1RE_btt/firmware.bin`, 152,952 bytes, SHA256 `030f660d236d62ac4486ed03aa117b01f447bfd9a9dbad9f893879ac52e7dad7`. The locally built binary differs from the downloaded release; matching byte counts do not establish byte identity. No claim of a functional fix or printer pass follows from this compile. Warnings: no user feedback method, and DIAG-jumper advisory. No hardware inference was made from those warnings.
