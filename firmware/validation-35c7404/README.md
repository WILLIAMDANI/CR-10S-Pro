# Fixed-revision validation candidate — 35c7404

Firmware source: `35c74044828af093f8753d5fa3f2a26c43955ac9`.
Binary SHA256: `b7cdbfeaf600df8b163b45b8fb1afa079d9a4e833a0c1f4b52a75d3658475264`.
Build: https://github.com/WILLIAMDANI/CR-10S-Pro/actions/runs/38329940387

Build and 58 baseline guards passed. Downloaded CI output independently checked
against its manifest, checksum and compiled FIRMWARE_NAME identity. Physical
behavior remains NOT RUN; the owner is PM/Lead and confirmed wiring is the baseline.
This artifact branch adds delivery files only; source was compiled from the
commit above, before those files were committed.

1. Verify firmware-main.bin against firmware-main.bin.sha256.
2. Rename to firmware.bin and flash using the SKR mainboard SD slot; see the
   source firmware/README.md. Preserve existing calibration with an M503 backup.
3. Follow COMPONENT-CHECK.md manually. Save raw M115/M105/M119 and observations.
4. Record each result against this exact binary. REGRESSION-RUN.md is an unfilled
   snapshot for the subsequent full suite; never overwrite an older run.
5. Attach failures to issue #6 and live M115 identity evidence to #4. Neither
   issue closes from compilation or this unfilled record.

Automatic heatbreak/controller cooling differs from M106 part-fan control.
Idle M112 requires a reboot before continuing; busy M112 is gated after verified
heating/motion. No unattended heater/homing stream or induced live connector fault.
