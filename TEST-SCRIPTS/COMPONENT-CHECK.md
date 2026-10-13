# Simple component check — owner result sheet

Use one identified main firmware candidate; keep all results NOT RUN until
observed. Save source SHA, binary SHA256, TFT version, transport and M503 output.
Use the corrected MAIN-BUILD-QUICKCHECK from codex/regression-followup. Stop at a
failed prerequisite; dependent rows are BLOCKED. This sheet is manually paced,
not a G-code file to stream unattended. Do not reset calibration without backup.

| Check | Action / expected observation | Result / raw output |
|---|---|---|
| Board and TFT | Fresh boot, startup identity and M115; TFT connects, controls respond; M105 gives plausible hotend/bed readings | NOT RUN |
| Idle emergency stop | Before heating/motion: send M112 while idle, capture response; reboot and recheck M115/M105 before any later row. Repeat per transport being tested | NOT RUN |
| Stored settings | M503 and M906; save offsets, steps, PID and currents | NOT RUN |
| Drivers | M122: X/Y/Z/E communication; detailed diagnostics only if compiled | NOT RUN |
| X/Y endstops | M119 released, then each pressed: open → TRIGGERED | NOT RUN |
| Probe | M119 clear, then metal present: open → TRIGGERED | NOT RUN |
| Part fan FAN0 | Cold printer: M106 S255 spins FAN0; M106 S0 stops it | NOT RUN |
| Electronics fan FAN2 | M17 starts it; M84 then configured off-delay stops it | NOT RUN |
| Hotend + TH0 | M104 S50, poll M105: only hotend reading rises plausibly; M104 S0 | NOT RUN |
| Heatbreak fan FAN1 | After previous pass: M104 S60; fan starts at measured ≥50°C; M104 S0 and confirm cooling | NOT RUN |
| Bed + THB | After hotend check: M140 S40, poll M105: only bed reading rises; M140 S0 | NOT RUN |
| X/Y/Z motors | With clearance and probe/endstop gates passed, small positive relative jogs; record physical directions, restore G90; Z+ must move away from bed | NOT RUN |
| Homing | Only after direction and input gates: G28 X Y, then G28 Z; recognize clearance and post-home raises | NOT RUN |
| Extruder EM | Only after heatbreak fan/thermal checks: use the master's hot-extrusion procedure; verify feed/retract direction, then shut down heat | NOT RUN |
| TFT speaker | Test its own UI sound setting/control if supported; it is not a Marlin M300 output | NOT RUN |
| SD/media | Check mainboard card listing and a known safe file via TFT; a directory listing alone is not a print pass | NOT RUN |
| Busy emergency stop | Only after the preceding heat/direction/homing gates pass: follow corrected TC-004 using validated low heating and bounded motion on TFT/USB; reboot/readiness check after every M112 | NOT RUN |
| Saved calibration | Verify saved values survive reboot; never replace actual calibrated values merely to match defaults | NOT RUN |
| Previous fixes | Repeat probe/Z direction, fan isolation/automatic cooling and low-temp heater checks on every changed candidate | NOT RUN |

Finish: M104 S0, M140 S0, M106 S0, M84; confirm targets zero and cooling.
Automatic cooling fans may continue by temperature/off-delay. Don't induce live
sensor-disconnect faults or count protection source inspection as a behavioral PASS.

After this check, generate a fresh full regression run with
`create_regression_run.py`. Link raw responses and any failed behavior to GitHub
Issues and the fixing PR; previous runs remain historical evidence. No component
is certified by this unfilled sheet or by successful firmware compilation.
