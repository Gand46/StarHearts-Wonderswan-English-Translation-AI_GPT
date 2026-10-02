# Star Hearts (WonderSwan Color) — English translation 13BG-F34

**Release status: `RC_SYNTHETIC_FOR_TESTING` (I14-P9 / 2026-09-28).** This is a test candidate with six documented `PASS_SYNTHETIC` cases. The audit package explicitly records `public_release_authorized=false` and `whole_project_legibility_approved=false`; this repository preparation does not change those states. Japanese-to-English localization, based on a specific Japanese 4 MiB WSC ROM.

This repository contains the cumulative translation sources and engineering records. The standalone `StarHearts_EN_phase13BG_F34_CUMULATIVE_2026-09-28.bps` is supplied separately as a release asset; GitHub users should obtain it from the corresponding F34 asset set. No commercial ROM, BIOS, save, or emulator is included.

## Apply the patch

1. Supply your own unmodified Japanese **Star Hearts** WonderSwan Color ROM, exactly **4,194,304 bytes**, with SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255` (the expected hash is documented in the F34 builder and audit; it could not be recalculated here without the ROM). Check locally with `shasum -a 256 original.wsc` on macOS, `sha256sum original.wsc` on Linux, or `Get-FileHash original.wsc -Algorithm SHA256` in PowerShell.
2. Apply `StarHearts_EN_phase13BG_F34_CUMULATIVE_2026-09-28.bps` to that original ROM using a BPS compatible patcher. Select a new output filename. **Apply this single cumulative patch directly to the original Japanese ROM**, without earlier F patches.
3. The documented translated output is 4,194,304 bytes, SHA-256 `d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0`, and WonderSwan checksum `3CD5`. The BPS SHA-256 calculated from the supplied patch is `3a9a3805f9e982ba36023c47c6f34671e742e2312b095bfacaddb556db01f114`.

The patch header records source CRC32 `138D1018` and target CRC32 `A8F5C374`; the patch's own CRC32 `10A9E5A3` was recalculated and matches. SHA-256 is the stronger identity check. No ROM download or commercial assets are provided.

## Build from source

Python 3 and the exact original ROM are required. From this repository root:

```text
python3 scripts/build_phase13BG_F34.py /path/to/your/original_JP.wsc -o /path/outside/repo/StarHearts_F34.wsc --bps /path/outside/repo/rebuilt_F34.bps
```

On Windows, `BUILD.bat` invokes the same F34 Python builder. On macOS, `build.command` invokes it from this directory; `build.sh` is also retained. These three launchers were updated from their stale F32 targets during packaging. Only the Python entry point was checked in the current Linux environment; Windows and macOS launchers were **not executed here**. The underlying builder uses the included BPS module and accumulated D/E/F manifests, enforces intermediate hashes and byte preconditions, verifies the WonderSwan checksum, and generates a *new direct* JP→F34 BPS. `baseline/StarHearts_EN_phase13BG_B_2026-09-15.bps` is an internal prerequisite for rebuilding the earlier translation base; end users apply only the F34 release BPS. Verify rebuilt ROM SHA-256 and compare the rebuilt BPS/output against the supplied asset. See [build record](docs/BUILD_AND_VERIFICATION.md) for the exact checks performed and the checks that require a ROM.

## Repository layout

| Path | Purpose |
| --- | --- |
| `scripts/` | Accumulated versioned builders F10–F34, resource builders, BPS encoder/decoder, audits. |
| `phase13BG_*_changes.json` | Cumulative, ordered translation and binary edit manifests; F34 checks a known F33 base. |
| `assets/` | Small necessary edited graphics/tiles and reference data; no full game dump. |
| `baseline/*.bps` | Required historical translated baseline used by the F10 source builder. |
| `qa/` | Lua and Python diagnostics kept with the source; scripts requiring private states do not by themselves reproduce the archived captures. |
| `README_F27.md`–`README_F34.md` | Original phase notes in Spanish, preserved with the source. |
| `docs/TECHNICAL_FINDINGS.md` | English architecture, address types, text consumers and tracked findings. |
| `docs/research_original_es/` | Selected original Spanish reports and current ledgers, preserved as provenance. |
| `docs/evidence/` | Captures/traces cited by the current acceptance ledger; no savestates. |
| `docs/ORGANIZATION_MANIFEST.csv` | Input to output/exclusion decisions. |

## Architecture and findings

The original game's scripts use CP932 text, fixed fields, native glyph loading and several independently consumed text surfaces. The cumulative source checks the before bytes of each revision rather than searching and replacing Japanese globally. Bank `0x38` uses pointer tables and an added 110-byte English pool; inline entity names use opcode `0x0022`, while other companion fields are deliberately left unchanged. Some menu captions live in compressed graphical resources in Bank `0x30`, and the shared skills description comes from Bank `0x38`. F34 fixes the second First Trial banner and the Link error formatter without changing the shared font, dictionary or renderer. See the [technical findings and memory/consumer tables](docs/TECHNICAL_FINDINGS.md) for exact addresses, code/data distinctions, confidence and report references.

## Validation scope and remaining limits

The final I14-P9 ledger has six cases tagged `PASS_SYNTHETIC`: shop sale/repair, Fire/Magic, Link wait/error display, Holy Temple/Tirawaka/second First Trial excerpt, 29 epilogue pages, and 45 credit cards/66 strings. Access included declared synthetic state and native consumers; it was not a full natural playthrough or a real Link transfer. A bad moving frame of `WAITING P2` and earlier incorrect Link error/banner captures were explicitly revoked and replaced. The 94 printable Latin/symbol glyph comparison found 93 native-identical glyphs; historical `_` provenance and visible use remain `NOT_VALIDATED`. Whole-game visual and linguistic approval is not established. The 237 integrated records from the earlier structural audit have a defined scope, not a claim that every game string was checked.

The [validation record](docs/VALIDATION.md) maps each current case to its evidence and exclusions. Earlier reports under `docs/research_original_es/` may contain superseded conclusions; always apply the I14-P9 ledger and `SUPERSEDED_APPROVALS.json` before quoting a historical PASS. This packaging run verified source identity, BPS container integrity and evidence hashes; it did not rebuild or run a ROM, because the required original ROM was not supplied.

## Credits, rights and provenance

This package preserves the upstream project files and their own credits; it does not assert authorship of the game or grant a license to its content. No explicit redistribution license for these project sources was found in the supplied source archive. The BPS is a translation patch for use with a separately obtained original game. Original research reports are available under `docs/research_original_es/`, with an English technical synthesis in `docs/TECHNICAL_FINDINGS.md`. The review is tied to the supplied 1.40 / I14-P9 / F34 source and audit package, not to later revisions mentioned elsewhere.
