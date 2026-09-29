# Result Entry Template

Use this for any single test you want to report back — especially failures,
or anything where the exact printer output matters for diagnosis. This is
different from `regression-runs/TEMPLATE.md` (the full-run checklist you keep
for your own records): this is the block to copy, fill in, and paste to
Claude in chat.

One entry per test. Copy the block below as many times as you need.

```
Test ID: TC-###
Date: YYYY-MM-DD
Result: PASS / FAIL / BLOCKED
Exact printer output:
<paste the raw text here — e.g. the full M119 response, not a summary>

Notes: <anything else you noticed — what you did differently, what it looked/sounded like, etc.>
```

**Why "exact printer output" matters:** "the probe didn't trigger" and
`z_probe: TRIGGERED` when you expected `open` are two different bugs.
Paste the actual serial text, not your interpretation of it — that's the
difference between a five-minute fix and a guessing game.
