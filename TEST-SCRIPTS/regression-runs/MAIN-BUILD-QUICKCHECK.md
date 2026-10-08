<!--
Quick-check sheet for firmware-main-<sha>.bin (the "main-build" GitHub
Release, branch claude/master-brief-review-rabxqg) — tests exactly the 5
things flagged as broken/fixed: fans, Z direction, Z probe, hotend heat,
hotbed heat. This is NOT the full regression suite — TEST-CASES.md and
regression-runs/TEMPLATE.md are the real suite for a full pass later.
Fill this out on the iPad at the printer.
-->

# Main Build Quick-Check — Fans / Z Direction / Z Probe / Heat

**SAFETY:**
- Hotend: `M104 S50` only to start. Watch the temperature actually climb. Only go higher once that behaves.
- Skip the bed entirely until the hotend passes.
- Z direction/probe: home X and Y first. Keep a hand on the power switch for the first `G28` (Z probing).

---

Commit SHA: `a15e1b4` __________ (confirm it matches what you flashed)
M115 compile date shown: ______________

**Fans**
FAN0 (parts cooling) spins at `M106 S255`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 (hotend aux) comes on above 50°C: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN2 (controller) spins with motors enabled: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

**Z direction**
Jog Z+ a few mm — nozzle/bed move the correct way (away from each other): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

**Z probe**
Manually trigger the probe, check `M119` — `z_probe` state flips correctly: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
`M119` output (paste verbatim): __________
`G28` — Z homes cleanly, no crash into the bed: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

**Hotend heat**
`M104 S50` — temp actually climbs: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

**Hotbed heat** (only after hotend passed)
`M140 S40` — temp actually climbs: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________

Any freeze? When, what it affected: __________
