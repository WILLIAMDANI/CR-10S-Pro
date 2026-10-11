# Regression follow-up for Claude

Reviewed main `cb06b38616e708baa6057abbc298050f7a79e118` and released source
`480b79db43dc27334f46f457ebdbe907e4b63590`. The downloaded release binary hash
matches the published manifest:
`ba2c8a1e3797c889c5282ab7bd0ae27e932ba209d8d2ca60265d9bf6b80a5656`.

The earlier Z/probe corrections, confirmed pins, automatic fans, current values,
and protection declarations are retained. TFT integration and M48 changes are
present. This confirms source preservation and artifact checksum, not printer
behavior. The owner's confirmed hardware/wiring remains the baseline.

## Corrections in this proposed PR

- Add `regression-checks` for pull requests and selected branch pushes: reviewed
  declaration guards plus a real STM32G0B1RE_btt build. The guards deliberately
  fail if preserved fixes are changed. They inspect declarations, not evaluated
  preprocessor state or physical behavior; compilation and printer results remain
  separate requirements. An intentional baseline change needs explicit review,
  rationale and corresponding regression evidence, rather than weakening checks.
- Replace the stale hand-maintained full-run template with a generator that
  snapshots TEST-CASES, records artifact commit/hash and procedure hash, starts
  all cases NOT RUN, and refuses to overwrite a saved result file. Historical
  regression files are untouched.
- Run the low-temperature heater check before the 60°C automatic-fan check,
  require endstop/direction/probe gates before homing, and include shutdowns.
- Move busy M112 testing behind verified low-temperature heating and safe motion;
  keep idle M112 early and mandatory reboot after every stop test.
- Defer live thermistor-disconnect fault induction. Source inspection of watchdog
  settings is not demonstrated behavioral regression validation.

## Remaining issue: firmware identity is NOT in M115

The downloaded binary contains `Author: main-build 480b79d` in its startup
message, but its FIRMWARE_NAME/M115 string has no source SHA. The workflow changes
STRING_CONFIG_H_AUTHOR; M115.cpp uses DETAILED_BUILD_VERSION instead. Claude's
claim that M115 identifies the exact commit is therefore incorrect. The updated
quick-check explicitly records the startup author line for this existing artifact.

Create a separate fixing PR using Marlin's supported detailed-build-version
override. Validate the built binary's M115 identity string before publishing,
then verify the actual M115 response on the printer. Avoid changing upstream
Version.h merely to maintain an injected identity. Include source full SHA,
configuration/tool versions and artifact hashes in the saved manifest. Current
manifest grep also misses indented MOTHERBOARD and motor-current declarations;
fix its whitespace handling and validate required fields exist.

## GitHub workflow required going forward

1. Open a PR from `codex/regression-followup` into
   `claude/master-brief-review-rabxqg`. Review and merge only after CI is green.
   Proposed title: **Preserve firmware fixes and synchronize regression validation**.
   This note supplies the PR description, validation and outstanding limitations.
2. Require the `firmware-regression` job in repository branch protection/rulesets
   for the firmware branch. Add review requirements for configuration, guards,
   workflows and test procedures. Merely adding a workflow does not enforce merge
   protection; an authorized repository administrator must configure it. Avoid
   direct pushes of firmware changes to the integration branch.
3. Use GitHub Issues for individual reproducible defects, linked to fixing PRs
   using `Refs #N` while hardware validation is pending. Don't auto-close a
   heater/fan/homing defect merely because CI compiled a binary. Close only with
   per-artifact raw-output evidence for the affected checks and required safety
   gates. Reuse existing relevant issues; don't create duplicate defects.
4. Record each printer run as its own committed regression file and attach logs
   to the relevant issue. Include binary SHA256, full source SHA, TFT version,
   USB/TFT transport, saved settings and exact observed output. Preserve earlier
   files and results; a new binary requires fresh results, not copied PASS labels.
5. Keep disagreements or proposed tuning in Discussions if enabled; confirmed
   defects belong in Issues, code/procedure changes in PRs, outcomes in regression
   records. No discussion feature is presumed enabled.
6. Preserve immutable per-commit release/artifact bundles alongside any moving
   'latest' convenience link. The current cleanup deletes every unrecognized
   asset name; restrict cleanup to explicitly obsolete firmware names. Add build
   concurrency or an explicit latest-source check so overlapping runs cannot
   publish older firmware last. `target_commitish` does not move an existing tag;
   verify actual tag SHA separately from release metadata.

## Prepared issue details (create/reuse via GitHub)

**Firmware identity missing from M115 and incomplete manifest**
Evidence: downloaded 480b79d binary startup author includes SHA; FIRMWARE_NAME
does not. MOTHERBOARD and current fields absent from downloaded manifest.
Acceptance: correct identity in binary and actual M115, required manifest fields,
matching hash and immutable source reference.

**Regression procedures drifted from master tests**
Evidence: previous TEMPLATE still prescribed M303 E-1, lacked the mandatory M112
reboot, and retained old TMC/thermal expectations. Main quick-check ran S60 before
its claimed S50-first check. Addressed by this proposed PR; acceptance requires
CI and review of a generated, entirely NOT RUN preview. Physical outcomes remain
pending and must not be overwritten by documentation changes.

**Remaining physical regressions: heaters/fans, Z/probe, emergency-stop**
Reuse existing matching issues if present, or create distinct issues. Record
current status as awaiting controlled validation of 480b79d. This review does not
establish that these reported failures persist or have been fixed. Owner-confirmed
wiring is the baseline; investigate firmware, command transport and runtime state
before unsupported hardware conclusions.

## Validation performed here

- 58 baseline declaration checks pass.
- Temporary-copy mutations reverting Z direction, changing PC15 to PC14, and
  disabling EMERGENCY_PARSER each fail the guard; original files remain unchanged.
- Actual main-source build with PlatformIO 6.1.19 succeeds in 39.32 seconds.
- Generator creates an inlined NOT RUN preview; a second invocation refuses to
  overwrite it. No printer tests were executed and no hardware PASS is claimed.
- Application firmware configuration/source is unchanged in this proposed PR.

GitHub API access returns Forbidden in this environment. Branch publication uses
the working Git proxy, but Issues, PR creation and branch-protection updates have
not been performed here. Claude should use its working GitHub access to complete
the numbered tracking steps, rather than treating this file as a substitute for
actual GitHub Issues/PRs.
