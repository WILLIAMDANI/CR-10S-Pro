#!/usr/bin/env python3
"""Snapshot current test procedures into a new run; never overwrite a result file."""
import argparse
import hashlib
import re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--firmware-commit', required=True)
parser.add_argument('--firmware-sha256', required=True)
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
if not re.fullmatch(r'[0-9a-f]{40}', args.firmware_commit):
    parser.error('--firmware-commit must be the full source commit from the artifact manifest')
if not re.fullmatch(r'[0-9a-f]{64}', args.firmware_sha256):
    parser.error('--firmware-sha256 must be the verified binary hash')
source = Path(__file__).resolve().parent / 'TEST-CASES.md'
cases = source.read_text()
cases = re.sub(r'(?m)^(### TC-[^\n]+)$',
               r'\1\n\n**Result:** NOT RUN\n**Evidence / GitHub issue:** <fill after execution>', cases)
header = f'''# Firmware regression run

Firmware source commit: `{args.firmware_commit}`
Firmware SHA256: `{args.firmware_sha256}`
TFT firmware/version: <record>
Tester / date / command transport: <record>
M503 settings backup: <attach>
Raw startup identity and M115/M105: <attach>
Procedure snapshot SHA256: `{hashlib.sha256(source.read_bytes()).hexdigest()}`
Issue(s) / pull request: <link>

All tests start NOT RUN. Use PASS / FAIL / BLOCKED / NOT RUN separately.
Physical results belong to this artifact and settings; do not transfer previous
passes to a different binary. Snapshot procedures below must be reviewed before
execution. Deferred fault tests remain NOT RUN. Complete the low-temperature
quick-check first; busy M112 requires verified motion/heating and a reboot after
each attempt. Back up calibration before reset; never blindly run M502/M500.

---

'''
try:
    with args.output.open('x') as output:
        output.write(header + cases)
except FileExistsError:
    parser.error(f'refusing to overwrite existing run: {args.output}')
print(f'Created {args.output}; no printer tests executed.')
