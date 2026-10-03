# Firmware Builds — CR-10S Pro / SKR Mini E3 V3.0

Each `.bin` here is a build of the `STM32G0B1RE_btt` PlatformIO environment,
named `firmware-YYYY-MM-DD-vN.bin`. `.pio/` itself stays untracked (build
junk), but these specific release binaries are force-added on purpose — they
are the actual deliverable.

## Builds

| Filename | Date | What changed | Status |
|---|---|---|---|
| [`firmware-2026-10-03-v1.bin`](firmware-2026-10-03-v1.bin) | 2026-10-03 | First build verified against this repo's config (user-built locally, attached in chat). Compiled 2026-09-24. Confirmed via embedded strings: `Marlin 2.1.2.8`, `MACHINE_TYPE:CR-10S Pro`, config date 2026-06-24 — matches this repo, not a different/stock build. `z_probe` reporting is compiled in; `z_min` is not (expected, since the probe shares logic with the would-be Z-min endstop). | **untested** — TC-001/002/003/039 passed on hardware; TC-004 onward produced results still being diagnosed (see `docs/BUILD-LOG.md`), largely complicated by the TFT console appearing to relabel/mangle some output. Not yet a clean pass or a confirmed fail. |

This sandbox's outbound network policy still blocks
`api.registry.platformio.org`/`api.registry.nm1.platformio.org`, so builds in
this environment remain blocked (see `docs/BUILD-LOG.md`) — the entry above
was built locally by the user and attached in chat, same path as before.

Status values used in the table above: **untested** (compiles, never run on
the printer) · **passed** (a regression run completed with no blocking FAILs)
· **failed** (a regression run found a blocking FAIL — see the linked GitHub
Issue).

## Flashing to the SD card

1. Rename the file to exactly `firmware.bin` (the board looks for this name).
2. Format an SD card **FAT32** (not exFAT) — smaller/older cards (≤32GB) tend
   to be more reliable than very large ones.
3. Copy `firmware.bin` to the **root** of the card — not inside a folder.
4. Power off the printer, insert the card into the **SKR Mini E3's own onboard
   micro-SD slot** (not the touchscreen's), power on.
5. Wait about a minute, then power off and check the card on a computer.
6. **Success looks like:** the file has been renamed to `FIRMWARE.CUR`. If it's
   still called `firmware.bin`, the board didn't accept it — try a different
   card or re-check the FAT32 format before touching anything on the printer.
