# Firmware Builds — CR-10S Pro / SKR Mini E3 V3.0

Each `.bin` here is a build of the `STM32G0B1RE_btt` PlatformIO environment,
named `firmware-YYYY-MM-DD-vN.bin`. `.pio/` itself stays untracked (build
junk), but these specific release binaries are force-added on purpose — they
are the actual deliverable.

## Builds

| Filename | Date | What changed | Status |
|---|---|---|---|
| *(none yet)* | — | — | — |

**No build exists in this repo yet.** This sandbox's outbound network policy
blocks `api.registry.platformio.org`/`api.registry.nm1.platformio.org`, which
PlatformIO needs to download the STM32G0 toolchain — this has been a
persistent, unresolved blocker across multiple sessions (see
`docs/BUILD-LOG.md`). Two ways to get the first real entry into this table:

1. **Build locally** (as done once before, successfully, in VS Code + PlatformIO
   on a normal machine with internet access) and attach the resulting
   `firmware.bin` to the chat — it'll be placed here, named, and logged
   properly.
2. **Fix the sandbox's network policy** so this environment can reach the
   PlatformIO registry, then ask for a fresh build.

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
