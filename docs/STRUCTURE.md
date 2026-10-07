# Repository structure

All paths below are relative to the repository root. The archive has one enclosing folder, `StarHearts-WSC-English-F37/`.

| Folder | Purpose |
| --- | --- |
| `source/scripts/` | Cumulative builders, graphics/codec helpers and phase-specific source audit tools |
| `source/manifests/D/`, `E/`, `F/` | Change records and integration manifests, classified by phase prefix |
| `source/assets/` | Translation resource data, native glyph references and name mappings; existing version subfolders preserved |
| `source/baseline/` | Required historical baseline patch used internally by the builder |
| `patches/F37/` | Current cumulative JP-to-F37 patch for players |
| `docs/technical/` | Current addresses, resources, consumer research and replay instructions |
| `docs/status/`, `docs/validation/` | Current project state and validation index |
| `docs/project/` | Changelog, credits and the old-to-new file index |
| `docs/release/` | English GitHub pre-release description |
| `docs/history/F*/` | Historical reports, preserved in their original language and build scope |
| `docs/es/F37/` | Current Spanish report |
| `qa/current/F37/` | Current prompt research, screenshots, replays, regression records and diagnostic states |
| `qa/history/F36/` | Previous shop/name evidence and the 181-field audit |
| `qa/history/F35/` | Menu comparison images and replay |
| `qa/history/legacy/` | Earlier replay scripts, tools and notes, separated by type |
| `qa/history/packaging/` | Prior packaging verification retained as historical evidence |
| `qa/shared/checkpoints/` | Inherited synthetic checkpoint used by the diagnostic replays |
| `qa/packaging/F37/` | Verification of this organized repository |
| `checksums/` | Current package hashes, with earlier inventories under `history/` |

The root contains `README.md`, `BUILD.bat`, `build.sh`, `build.command`, `requirements.txt` and Git configuration. Generated ROMs and local build output belong in the ignored `build/` directory, which is not part of the distribution.

## Path conventions

- User-facing documentation and commands use repository-root paths unless explicitly stated otherwise.
- Python builders resolve their data root to `source/`. References such as `assets/F31/header_03.bin` inside unchanged integration manifests are relative to that source root.
- Manifests retain their original filenames and bytes. Builder lookup strings point into `source/manifests/D`, `E` or `F`.
- Runtime evidence files retain their original bytes. Their earlier path strings document the original run; use the current technical report and relocation index for present locations.
- The [file relocation index](project/FILE_RELOCATION.csv) records every file from the preceding GitHub package, its new location, both hashes and whether content changed.
- The [current inventory](../checksums/SHA256SUMS.json) covers the whole organized repository except the inventory itself. Inventory keys are repository-root paths.

## Ordering

Directories are grouped by purpose; build-specific evidence is grouped by version. The ZIP is emitted in natural path order, so numbered phases such as F2 and F10 appear numerically within their groups. A file manager or GitHub may apply its own display sorting.

No original project input or QA record was discarded by this reorganization. Documentation and path lookups were updated; the reconstructed F37 ROM and cumulative BPS remain identical.
