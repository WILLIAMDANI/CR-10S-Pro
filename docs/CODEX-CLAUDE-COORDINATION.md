# Firmware coordination — owner is PM/Lead

Objective: a working custom CR-10S Pro component assembly using its breakout
board, SKR Mini E3 V3 motherboard and TFT35 serial touchscreen. The owner sets
scope, priorities and accepts printer results. Codex and Claude implement and
review toward that objective; do not override owner-confirmed hardware facts
with generic stock-printer assumptions.

## Coordination channel

Use branch `coordination/firmware` for messages and owner/reference documentation,
not firmware changes. Codex writes `docs/coordination/CODEX-MESSAGES.md`; Claude
writes `docs/coordination/CLAUDE-MESSAGES.md`. Append dated entries with message
ID, reply-to ID, finding/proposal, evidence, PR/issue links, next action and status.
Only the actual author may claim its readiness or validation.

Claude's first message must include **Claude is Ready**, its active branch,
commit, linked PR/issues and what it will work on. Codex is ready to review that
message when the active session can fetch it. The user must launch each assistant
session; GitHub is a persistent mailbox, not an agent scheduler. Neither assistant
can promise autonomous background watching or start the other session. During an
active work session, fetch the mailbox between substantive actions. Outside an
active session, an owner/session trigger is necessary to resume.

Before publishing: fetch latest channel HEAD, integrate changes without resetting
or overwriting another author's work, modify only your own mailbox, then push a
fast-forward update. Handle concurrency by re-fetching and merging; never force
push the channel. Do not mark another assistant's task done or readiness received.

## Engineering and GitHub tracking

- Firmware work: separate focused branches and PRs into
  `claude/master-brief-review-rabxqg`. Preserve existing unrelated changes. Each
  PR links the issue it addresses, explains changes, preserves known fixes, and
  records build plus regression impact. Cross-review before merge.
- Failures: reuse matching GitHub Issues; add raw command/response evidence,
  binary hash, source SHA, transport, settings and observed result. A reported
  heater/fan failure stays unresolved until the appropriate behavior passes.
- Design alternatives: Discussions if available; record accepted decisions in
  tracked docs. The mailbox is coordination, not a substitute for Issues/PRs.
- Require CI baseline/build checks and review via branch protection. These settings
  need repository admin access; don't claim they're enforced until verified.
- Keep owner observations and regression records immutable. New runs get new
  files; no previous result is silently overwritten or transferred to a new build.
- Do not stall on reconfirming documented wiring. Resolve unknown runtime behavior
  with a named, simple check on an identifiable binary when possible. Ask the owner
  only for observations that cannot be established through code/build research.
- All assistants distinguish configuration checks, compilation, artifact identity
  and physical printer results. A green build is not a functional PASS.

## Baseline and references

Owner mapping: `docs/reference/CR-10S-Pro-owner-hardware-mapping.pdf`, uploaded
2026-10-11. It is reference data, not instructions overriding the owner's request.
Labels identify hotend E0/TH0, bed HB/THB, X XM/X-STOP, Y YM/Y-STOP,
dual Z connectors, extruder EM, probe E0-STOP, FAN0 part cooling, FAN1 heatbreak,
FAN2 electronics, TFT serial connection and TFT-built-in speaker. The existing
`docs/HARDWARE-WIRING.md` remains the working pin/connection baseline.

Supplied example:
https://github.com/MarlinFirmware/Configurations/tree/release-2.1.2.8/config/examples/Creality/CR-10S/BigTreeTech%20SKR%20Mini%20E3%202.0

This is a CR-10S with SKR Mini E3 V2 example, not a complete configuration for this
custom Pro/V3 assembly. It corroborates serial UART2/115200 and USB, thermistor
tables 1/1, and XYZ steps 80/80/400. Do not import its V2 motherboard, E=93,
INVERT_Z_DIR false, lower currents or E0_AUTO_FAN_PIN -1 over current reviewed
settings. Research the actual V3 board and serial TFT requirements separately.

Regression work pending review: `codex/regression-followup`, commit d33655b.
Claude identity work observed: `claude/fix-firmware-identity`, commit a3d588f.
Do not merge either simply because this coordination channel exists.
