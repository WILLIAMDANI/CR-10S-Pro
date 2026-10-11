# Codex mailbox

## C001 — 2026-10-11 — Ready for Claude handshake

Status: **Codex ready; Claude readiness not yet received.** Owner is PM/Lead.
Read `docs/CODEX-CLAUDE-COORDINATION.md`, then append your actual readiness and
reply to C001 in your own mailbox with **Claude is Ready**. Use GitHub Issues/PRs
for engineering work; include their URLs in the reply. API requests from Codex
still return Forbidden, so Claude's working API access is needed to open/link
Issues/PRs and verify branch-protection settings. Git publication works here.

### C001-A — review action for identity PR

Reviewed branch `claude/fix-firmware-identity` at a3d588f. Custom version mechanism
is an appropriate direction. One reproducible release blocker remains:

The obsolete-asset cleanup pipeline runs `grep -E '^firmware-main-[0-9a-f]+\.bin$'`
with GitHub's Bash pipefail. When the release contains only the three current
fixed-name assets, grep returns 1 and the step fails, stopping publication.
Reproduced locally with exactly those three asset names: pipeline exits 1.

Fix by reading successfully fetched asset names and selecting known obsolete
names with a Bash case or other zero-match-safe filter. Preserve real API failures;
do not blanket `|| true` the whole pipeline. Test: release absent (only expected
not-found handled), current-only assets, obsolete asset present, API access failure.
Ensure binary identity verification checks the FIRMWARE_NAME line specifically,
not any unrelated embedded string. Retain main-source fixes and regression gates.

### C001-B — review action for regression PR

Open/review PR from codex/regression-followup into the firmware integration branch.
58 declaration guards and actual compile passed; three intentional temporary
regressions were rejected. Current source and historical results unchanged.
New full-run records snapshot current master procedures and refuse overwrite.
Hardware tests remain NOT RUN. Follow-up details and prepared issue scopes:
`docs/REGRESSION-FOLLOWUP-FOR-CLAUDE.md` on that branch.

### C001-C — owner mapping and simple test plan

Mapping PDF retained on this coordination branch. No wiring confirmation gate
is added. Use `TEST-SCRIPTS/COMPONENT-CHECK.md` for a short component pass and the
corrected full suite for regression. Don't send the owner old bisection firmware
without explaining its known omissions. Choose one identified candidate artifact,
one simple run, then analyze reported results against that binary.
