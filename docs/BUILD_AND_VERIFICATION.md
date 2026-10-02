# Build and verification record

Source archive: `StarHearts_F34_Fuentes_Completas_2026-09-28(1).zip` (163 F34 files, byte-identical to the F34 source tree inside private audit package before launcher correction). Standalone BPS: SHA-256 `3a9a3805f9e982ba36023c47c6f34671e742e2312b095bfacaddb556db01f114`. The same BPS is stored at `iterations/I14/patches/StarHearts_EN_phase13BG_F34_CUMULATIVE_2026-09-28.bps` inside the supplied private archive, byte-identical.

## BPS container, inspected in this preparation

| Field | Value |
| --- | --- |
| Format | `BPS1` |
| Source size | 4,194,304 bytes |
| Destination size | 4,194,304 bytes |
| Source CRC32 | `138D1018` (metadata; not recalculated against a source ROM here) |
| Destination CRC32 | `A8F5C374` (metadata; not recalculated against a target ROM here) |
| Patch CRC32 | `10A9E5A3` (recomputed and matched) |
| SHA-256 | `3a9a3805f9e982ba36023c47c6f34671e742e2312b095bfacaddb556db01f114` (calculated from supplied BPS) |

The I14-P9 `BUILD_VALIDATION.json` records an earlier successful Linux/Python build from the exact JP ROM, independent BPS application, F34 SHA-256 `d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0`, and WonderSwan checksum `3CD5`. These are **prior documented results**, not a fresh rebuild. The original commercial ROM was absent from the inputs for this packaging run; source rebuild, BPS application, comparison of reconstructed bytes, and current emulator execution were **NOT_RUN** here.

Root launcher targets were corrected from F32 to F34 without changing the cumulative builder, manifests or BPS. Python syntax and entry point checks in this run are recorded below after final verification. Windows `BUILD.bat` and macOS `.command` execution remain NOT_RUN in this environment.

Build from source requires the exact original JP ROM locally. `scripts/build_phase13BG_F10.py` first applies the included `baseline/StarHearts_EN_phase13BG_B_2026-09-15.bps` to that ROM and checks the intermediate hash. Later builders apply each D/E/F manifest in sequence with byte preconditions; F34 checks the F33 SHA-256, exact allowed offsets, target SHA-256 and WonderSwan checksum, then creates a new direct JP→F34 BPS. The baseline BPS is a necessary historical dependency, not an end-user installation chain. Keep generated `.wsc` files outside the repository.

## Current packaging checks

All Python files passed syntax parsing; the F34 builder `--help` entry point passed on Linux/Python 3; all three launchers now reference F34. The repo was scanned recursively for ROM/save/executable/container files, each `.bin` resource was checked under 4 KiB, and each selected evidence hash was recomputed. The included older baseline BPS is a necessary build dependency. The standalone F34 patch CRC was recalculated. No original ROM was available, so **source→ROM build and source-output↔BPS-target equality are NOT_VALIDATED in this run**.
