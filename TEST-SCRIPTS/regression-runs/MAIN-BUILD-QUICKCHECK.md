<!--
Quick-check sheet for firmware-main-<sha>.bin (the "main-build" GitHub
Release, branch claude/master-brief-review-rabxqg) — tests exactly the 5
things flagged as broken/fixed: fans, Z direction, Z probe, hotend heat,
hotbed heat. This is NOT the full regression suite — TEST-CASES.md and
regression-runs/TEMPLATE.md are the real suite for a full pass later.
Fill this out on the iPad at the printer.

Revised 2026-10-11 per Codex review (docs/CODEX-REVIEW-FOR-CLAUDE.md,
finding 5) — the previous version could produce misleading results: it
had no settings-inspection step, no explicit FAN2-enable command, a
heat threshold test that doesn't reliably cross the threshold it claims
to test, no distinction between BLOCKED and FAIL, and incomplete probe
open/triggered expectations.
-->

# Main Build Quick-Check — Fans / Z Direction / Z Probe / Heat

**Result key:** ✅ PASS · ❌ FAIL · ➖ NOT RUN · 🚧 BLOCKED (couldn't run because an earlier step failed — this is NOT the same as FAIL; don't mark a fan FAIL just because the heater step it depends on never got there).

**SAFETY:**
- Hotend: `M104 S50` only to start. Watch the temperature actually climb. Only go higher once that behaves.
- Skip the bed entirely until the hotend passes.
- Do not home any axis until probe states, endstop states and jog directions pass on this artifact. Keep a hand on the power switch; initial `G28 X Y` may include a Z-clearance move.
- After any `M112`: **reboot the board** and re-confirm with `M115`/`M105` before continuing to the next section. Do not keep testing against a killed board.

---

Firmware source SHA from saved manifest: __________
Binary SHA256 (verify against saved .sha256): __________
TFT firmware/version and command transport (USB/TFT): __________
Save raw startup identity and M115 output: __________
For build 480b79d, the SHA is in the startup Author line, NOT the M115 response. Do not infer firmware SHA from current repository HEAD or a moving release page.

**Step 0 — Inspect settings before touching anything (do this first, every time)**
Send `M503` and record what it reports for probe offset, E-steps, and currents: __________
Why: EEPROM-saved values can override compiled defaults for these items. Direction and pin macros (`INVERT_Z_DIR`, `Z_MIN_PROBE_PIN`, etc.) are compile-time and are NOT affected by EEPROM — but offsets/steps/PID/currents can be. `EEPROM_AUTO_INIT` does not erase valid old settings on every flash.
**Do not run `M502` (factory reset)** unless you intend to lose saved calibration — back up the `M503` output above first if you ever do.

**Hotend heat**
`M104 S50` — **measured** temp (`M105`) actually climbs toward 50, not just that the command was accepted: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Shut off afterward: `M104 S0`, confirm target is zero and temperature begins cooling. If temperature does not rise plausibly or a fault appears, stop heating; dependent fan checks are BLOCKED.

**Fans**
FAN0 (parts cooling) spins at `M106 S255`, then stop with `M106 S0`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 (hotend aux, automatic — not a manual fan): heat hotend to `M104 S60` (not S50 — regulation can settle at/below 50°C and never visibly cross the threshold the fan actually watches) and confirm FAN1 comes on once **measured** temp (`M105`), not just the commanded target, reaches ~50°C: ✅ PASS ❌ FAIL 🚧 BLOCKED (hotend didn't heat — see Hotend section) ➖ NOT RUN — Notes: __________
FAN2 (controller, automatic): explicitly enable motors with `M17` (do not assume they're already enabled), then confirm FAN2 spins. Disable with `M84` afterward and confirm FAN2 stops after its configured off-delay (it will not stop instantly — that's expected): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

After FAN1 check: `M104 S0`, verify target zero and cooling; FAN1 stays on until measured temperature falls below its threshold.

**Endstop and probe gates — before any homing**
`M119`: X/Y each open released and TRIGGERED pressed; probe open clear and TRIGGERED with metal. Record both states. A failed gate means STOP: no homing.

**Z direction**
With physical clearance and all probe-state checks passed: `G91`, `G1 Z2 F60`, then `G90`. Hand near the power switch; stop immediately if motion is toward the bed. Nozzle/bed move the correct way (away from each other): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Do NOT run `G28` yet — do the Z probe section first; TC-009/TC-012's gate applies here too.

**Z probe**
Released (nothing near probe face), check `M119` — `z_probe` reads `open`: ✅ PASS ❌ FAIL ➖ NOT RUN
Hold metal to the probe face, check `M119` again — `z_probe` reads `TRIGGERED`: ✅ PASS ❌ FAIL ➖ NOT RUN
**Stop here and do not run `G28` if either state above is wrong or reversed.** Report it instead.
`M119` output, both states, pasted verbatim: __________
Only if X/Y endstops, X/Y/Z positive jog directions, and both probe states passed: `G28 X Y`, then `G28 Z`: Z homes cleanly (clearance raise, then descent, then stops at probe trigger, then post-home raise — a raise at the start/end is normal, not a sign of inversion), no crash into the bed: ✅ PASS ❌ FAIL 🚧 BLOCKED (probe states wrong above) ➖ NOT RUN — Notes: __________

**Hotbed heat** (only after hotend passed — mark 🚧 BLOCKED, not FAIL, if skipped because hotend failed)
`M140 S40` — measured temp actually climbs toward 40: ✅ PASS ❌ FAIL 🚧 BLOCKED (hotend failed above) ➖ NOT RUN — Notes: __________
Shut off afterward: `M140 S0`, confirm via `M105` it's cooling.

Finish: `M104 S0`, `M140 S0`, `M106 S0`, `M84`. Confirm heater targets zero and cooling; allow automatic fans their temperature/off-delay behavior.

Any freeze? When, what it affected, and did you reboot+re-verify before continuing: __________
