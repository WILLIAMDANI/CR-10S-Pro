# Creating a regression run

Use the current master procedures in `TEST-SCRIPTS/TEST-CASES.md` to generate
an independent, fully inlined run. This replaces the hand-maintained duplicate
that retained obsolete bed PID, emergency-stop and thermistor procedures.
Existing run records are historical evidence: never regenerate over them.

From the repository root:

```sh
python3 TEST-SCRIPTS/create_regression_run.py \
  --firmware-commit <full-source-commit-from-saved-manifest> \
  --firmware-sha256 <verified-binary-sha256> \
  --output TEST-SCRIPTS/regression-runs/<date>-<short-firmware-sha>.md
```

The command refuses to overwrite an existing file. It includes the current
procedures, their snapshot hash, artifact identity, raw-output fields, issue/PR
links, and a NOT RUN result for every test. Replace each result only after the
test executes; distinguish FAIL, BLOCKED and NOT RUN. Deferred fault tests
remain NOT RUN. Compilation or source review is not a physical PASS.

Complete `MAIN-BUILD-QUICKCHECK.md` first. Busy emergency-stop checks require
verified motion and low-temperature heating, followed by a reboot/readiness
check. Back up saved calibration before any factory reset. After a changed
binary, re-run affected tests and all safety gates; do not copy earlier passes.
Attach raw logs and link each failed behavior to its GitHub issue. Close issues
only after the linked fixing PR and required regression evidence are recorded.
