# Testing & Regression Tracking — CR-10S Pro / SKR Mini E3 V3.0

This directory is the test-management system for this firmware, sized for how this
project actually works: one tester, one physical printer, firmware built by hand
from a specific git commit rather than on a release train.

## Reporting results back to Claude

For any test you run on the printer, copy the block from
`RESULT-ENTRY-TEMPLATE.md`, fill it in, and paste it directly into chat — one
per test, or several in one message. The important part is **exact printer
output** (the actual `M119`/`M105`/etc. text), not a summary in your own
words — that's what makes a failure diagnosable instead of a guessing game.
For a full end-to-end run across every test case, use
`regression-runs/TEMPLATE.md` instead (see "Workflow" below) and report the
whole filled-in file back the same way.

## The model (same one used by Jira test-management tools like Xray/Zephyr)

Three things, kept separate on purpose:

1. **Test Case** (`TEST-CASES.md`) — the master copy of each procedure, with full
   detail and the reasoning behind it. Edit this when a procedure itself changes.
   It never contains a pass/fail result.
2. **Regression Run** (`regression-runs/<date>-<git-short-sha>.md`) — a
   **self-contained checklist**: the steps and expected result are copied inline
   for every test, so you fill it out top-to-bottom on your phone at the printer
   without flipping back to `TEST-CASES.md`. This is where PASS / FAIL / BLOCKED /
   NOT RUN actually live. If a run's inlined text and `TEST-CASES.md` ever
   disagree, `TEST-CASES.md` is the source of truth — update the next run's copy
   from it.
3. **Bug** — opened only when a test fails. Tracked as a **GitHub Issue** in this
   repo (not a separate system), so it's permanently linked to the exact commit
   that was being tested and the exact commit that later fixes it.

Traceability reads the same way Jira/Xray would give you:
`commit abc1234 → regression run 2026-09-28-abc1234.md → TC-009 → FAIL → GitHub Issue #7 → fixed in commit def5678 → TC-009 → PASS`

## Result statuses — exactly four, no in-between

- **PASS** — expected result fully achieved.
- **FAIL** — it wasn't. If it's "mostly right but," that's still FAIL — write down why in the run file.
- **BLOCKED** — couldn't be run (earlier step failed, hardware not in the right state, etc.). Not the same as FAIL.
- **NOT RUN** — not attempted yet this cycle.

## Workflow for a new firmware build

1. Copy `regression-runs/TEMPLATE.md` to `regression-runs/<YYYY-MM-DD>-<short-sha>.md`.
2. Fill in the header (git commit, what changed since the last run, tester, date).
3. Work through `TEST-CASES.md` in order, recording one result line per test case.
4. Any FAIL or BLOCKED → open a GitHub Issue, paste in the actual-vs-expected and
   any evidence (photo/video/M119 output/serial log), and put the issue number
   next to that test case's result line.
5. Commit the run file. That's the permanent record.
6. When a bug is fixed, add a test case for it if one doesn't already exist
   (see "Regression" section at the bottom of `TEST-CASES.md`), so it can never
   silently come back unnoticed.

## Why not Jira

Nothing wrong with Jira's model — it's the right model. But for this project,
git already gives you the "which exact build was this tested against" link that
Jira would need a separate integration to provide, and GitHub Issues already
exist here at no extra cost. If this project ever grows past one tester/one unit
(e.g. testing multiple printers, or handing this off to someone else), moving
this same TC library into Jira/Xray at that point is a straightforward export —
ask and a CSV can be generated from these files.
