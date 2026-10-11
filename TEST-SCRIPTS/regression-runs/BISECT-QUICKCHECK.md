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

Revised 2026-10-11 per Codex review (docs/CODEX-REVIEW-FOR-CLAUDE.md,
finding 6): a Batch 0 heat/fan failure does NOT by itself "point at
hardware" — baseline correctness, command transport, thermal faults,
saved EEPROM state, and test execution itself all still need checking
first. Also: Batch 2 still has INVERT_Z_DIR false (official's value,
not this project's confirmed-correct true), so it gets the same
no-Z-motion gate as Batches 0/1, not a relaxed one.
-->

# Bisect Quick-Check — Batches 0, 1, 2

**Result key:** ✅ PASS · ❌ FAIL · ➖ NOT RUN · 🚧 BLOCKED (an earlier step failed — not the same as FAIL).

**SAFETY — read before flashing anything:**
- Hotend: `M104 S50` only to start. Watch the **measured** temperature (`M105`) actually climb. Only go higher once that behaves.
- Skip the bed entirely until the hotend passes.
- **All three batches (0, 1, AND 2): NO Z jogging, NO `G28`.** Batch 2's probe architecture does not make its Z direction trustworthy — it still carries `INVERT_Z_DIR false` (the official example's value), not this project's physically-confirmed `true`. Treat all three batches identically here.
- After any `M112` or freeze/reboot: re-confirm with `M115`/`M105` before continuing.
- **If Batch 0 fails a heat or fan check, stop and report it — but that is a lead, not a verdict.** It does NOT by itself "point at hardware." Before concluding anything: check `M503` for stale saved settings, confirm the exact commit actually flashed via `M115` compile date, and check for a thermal/MINTEMP error in the response rather than assuming silence means a dead heater. Report what you see; let the diagnosis happen from there, not from this sheet.

---

## Batch 0 — official example, zero of our changes
GitHub Issue: #1 — paste/fill results there too

Batch/commit SHA: `e0b3175` __________ (confirm it matches what you flashed)
M115 compile date shown: ______________
`M503` output (settings as-saved — note anything unexpected): __________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50` (measured temp climbs, not just command accepted): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255`, then `M106 S0` to stop): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on once measured temp reaches ~50°C (use `M104 S60` to actually cross the threshold, not S50): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
FAN2 spins after explicit `M17` (motors enabled): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40`, measured temp climbs (only if hotend passed, else 🚧 BLOCKED): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
Shut down: `M104 S0`, `M140 S0`, `M106 S0` — confirm cooling/stopping.
Any freeze? When, what it affected: __________

## Batch 1 — Batch 0 + our stepper currents
GitHub Issue: #2 — paste/fill results there too

Batch/commit SHA: `a89cdf4` __________
M115 compile date shown: ______________
`M503` output: __________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50` (measured temp climbs): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255` / `M106 S0`): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on at measured ~50°C (`M104 S60` to actually cross it): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
FAN2 spins after explicit `M17`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40` (only if hotend passed, else 🚧 BLOCKED): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
Shut down: `M104 S0`, `M140 S0`, `M106 S0`.
Any freeze? When, what it affected: __________

## Batch 2 — Batch 1 + our probe architecture
GitHub Issue: #3 — paste/fill results there too

Batch/commit SHA: `5626eb4` __________
M115 compile date shown: ______________
`M503` output: __________
M105 temps sane at room temp: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Hotend heats at `M104 S50` (measured temp climbs): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN0 spins (`M106 S255` / `M106 S0`): ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
FAN1 comes on at measured ~50°C (`M104 S60` to actually cross it): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
FAN2 spins after explicit `M17`: ✅ PASS ❌ FAIL ➖ NOT RUN — Notes: __________
Bed heats at `M140 S40` (only if hotend passed, else 🚧 BLOCKED): ✅ PASS ❌ FAIL 🚧 BLOCKED ➖ NOT RUN — Notes: __________
Shut down: `M104 S0`, `M140 S0`, `M106 S0`.
Any freeze? When, what it affected: __________
`M119` released (nothing at probe) — `z_probe` state: __________
`M119` triggered (metal at probe) — `z_probe` state: __________
**No Z jog, no `G28` on this batch** — its `INVERT_Z_DIR` is the official example's `false`, not this project's confirmed `true`. Probe state is informational only here, not a go-ahead for Z motion.
