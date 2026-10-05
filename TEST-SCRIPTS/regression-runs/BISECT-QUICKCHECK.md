<!--
Quick-check sheet for the Batch 0/1/2 bisection builds ONLY (see
docs/BUILD-LOG.md and the "bisect-batches" GitHub Release for what's in each
batch). This is NOT the full regression suite — TEST-CASES.md and
regression-runs/TEMPLATE.md are untouched and still the real suite for a
normal firmware build. Fill this out on the iPad at the printer, one batch
at a time, in order (0, then 1, then 2).

Branch: bisect/batch-audit-v2 (not bisect/batch-audit — that branch's first
three batch commits failed to compile and were superseded; see
docs/BUILD-LOG.md, 2026-10-05 entries).
-->

# Bisect Quick-Check — Batches 0, 1, 2

**SAFETY — read before flashing anything:**
- Hotend: `M104 S50` only to start. Watch the temperature actually climb. Only go higher once that behaves.
- Skip the bed entirely until the hotend passes.
- **Batch 0 and Batch 1: NO Z jogging, NO `G28`.** Z direction is wrong for this machine on these two builds.
- **Batch 2: home X and Y first.** Keep a hand on the power switch for any Z move.
- **Stop here if Batch 0 fails any heat or fan check below.** Batch 0 has none of this project's changes — a failure there points at hardware, not firmware. Report it and don't move on to Batch 1.

---

## Batch 0 — official example, zero of our changes
GitHub Issue: #1 — paste/fill results there too



Batch/commit SHA: `e0b3175` __________ (confirm it matches what you flashed)
M115 compile date shown: ______________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255`): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on above 50°C: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN2 spins with motors enabled: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40` (only if hotend passed): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Any freeze? When, what it affected: __________

## Batch 1 — Batch 0 + our stepper currents
GitHub Issue: #2 — paste/fill results there too



Batch/commit SHA: `a89cdf4` __________
M115 compile date shown: ______________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255`): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on above 50°C: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN2 spins with motors enabled: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40` (only if hotend passed): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Any freeze? When, what it affected: __________

## Batch 2 — Batch 1 + our probe architecture
GitHub Issue: #3 — paste/fill results there too



Batch/commit SHA: `5626eb4` __________
M115 compile date shown: ______________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255`): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on above 50°C: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN2 spins with motors enabled: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40` (only if hotend passed): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Any freeze? When, what it affected: __________
`M119` output (paste verbatim): __________
Probe trigger behavior (manually trip it, what happened): __________
