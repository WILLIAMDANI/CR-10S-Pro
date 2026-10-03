<!--
Filename placeholder: commit SHA not yet confirmed by the user. Rename to
2026-10-02-<short-sha>.md once known (see docs/BUILD-LOG.md open question).
-->

# Regression Run — 2026-10-02 — commit `<pending confirmation>`

**Firmware commit:** `<pending confirmation — user built/flashed locally, commit not yet identified>`
**Tester:** <not given> | **Date:** 2026-10-02
**What changed since last run:** First real hardware run. No prior run exists.

Raw results as reported by the user, preserved as given. Analysis and follow-up
questions are in `docs/BUILD-LOG.md` (2026-10-03 entry) — **no config/firmware
changes have been made based on this data yet.**

---

## A. Boot

**TC-001 — Firmware flashes via SD card** — Result: **PASS**

**TC-002 — Correct firmware identifies itself** — Result: **PASS**

**TC-003 — TFT35 connects to mainboard** — Result: **PASS**

**TC-039 — TFT touch, encoder, and button all respond** — Result: **PASS**

## B. Emergency Stop

**TC-004 — M112 emergency stop** — Result: **FAIL**
Notes (verbatim): "noting occured with M112 & Menu>EM.STOP did noting on
screen but then nothing works, open black notification and cleard and
directionals move"

**⚠️ Open question:** was the board power-cycled/reset after this test before
continuing to C/D/E/F below? If not, TC-005/006/014/015/016 and the
heater failure may be downstream symptoms of this, not independent bugs —
see docs/BUILD-LOG.md.

## C. Driver Health

**TC-005 — TMC2209 driver communication** — Result: **FAIL**
Notes (verbatim): "NOthing occured with M122"

**TC-006 — Driver currents match configuration** — Result: **FAIL**
Notes: (none given)

## D. Endstops & Probe

Reported as free-form observations from full `G28` rather than isolated
`M119` checks (TC-007/008/009 not filled in individually):

> Zprobe light off/untriggered z home = X moves to end stop, y moves to end
> stop and Z moves up 2 times and stops
>
> Zprobe light on/triggered z home = z moves continuously down while light is
> on and probe is triggered, once unblocked/light off/untriggered — z moves
> up twice

**Analysis pending isolated `M119` confirmation** — see docs/BUILD-LOG.md.
Possible `INVERT_Z_DIR` and/or `Z_MIN_PROBE_ENDSTOP_INVERTING` issue. No
config change made — full `G28` was run before the safer manual-jog
(TC-012) gate; this time it failed in the non-destructive direction, but
should not be repeated until the probe logic is confirmed via `M119` alone.

## E. Motor Directions

Reported as free-form observations rather than individual PASS/FAIL:

> X home - move x to end stop
> Xmove - X+ moves x to right and X- moves x to left
> ZMove - moves z+ moves z up & z-moves z down
> Ymove - Y- moves away from user/front & y+ moves y towards user/front
> yHome - moves y away from front to endstop

**TC-013 — Extruder direction** — Result: NOT RUN (blocked — requires hotend ≥200°C, which is not currently heating; see Group G)

## F. Fans

**TC-014 — FAN1 (heatbreak) auto-control** — Result: **FAIL**
Notes (verbatim): "not heat working" — likely blocked by the heater issue (Group G) rather than an independent fan defect; re-test once heat works.

**TC-015 — FAN2 (controller/case)** — Result: **FAIL**
Notes (verbatim): "notification no move ok p15 B3" — too garbled to act on; need exact verbatim text per `RESULT-ENTRY-TEMPLATE.md`.

**TC-016 — Part-cooling fan isolation** — Result: **FAIL**
Notes (verbatim): "no ourcom black screen"

## G. Heaters

**No hotbed or hotend working** (user's summary — TC-017/018 not individually marked).

---

## Follow-up needed before any firmware/config change (see docs/BUILD-LOG.md for full reasoning)

1. Was the board reset/power-cycled after TC-004, before C–G were tested?
2. Exact `M119` output, probe clear, then probe triggered (no G28 needed for this).
3. Exact verbatim on-screen/serial text for TC-015 and TC-016 (not paraphrased).
4. Which commit was this firmware built from, and can the actual `firmware.bin` be attached?
