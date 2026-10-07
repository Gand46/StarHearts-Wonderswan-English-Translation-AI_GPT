# QA evidence map

| Subfolder | Scope |
| --- | --- |
| `current/F37/` | Four-prompt audit, native synthetic rendering, shop regression and F37 diagnostic states |
| `history/F36/` | Two purchase graphics and 181 initial actor names plus the separate inline name |
| `history/F35/` | Menu typography screenshots and replay |
| `history/legacy/` | Older scripts, notes and tools, classified by file purpose |
| `history/packaging/` | Verification of previous package layouts |
| `shared/checkpoints/` | Inherited synthetic base checkpoint |
| `packaging/F37/` | Current folder/path/hash checks and clean build result |

Use the [validation index](../docs/validation/VALIDATION_F37.md) and [current technical report](../docs/technical/TECHNICAL_F37.md) for supported replay commands. For F37 state reloading, `QA_ROOT` points to the absolute `qa/current/F37/` directory. For prompt replay, `BASESTATE` points to `qa/shared/checkpoints/P4_repair_synthetic_entry.mss`.

All runtime evidence and replay code retain their original bytes. Historical paths in logs or reports are evidence of the earlier run, not current entry points. The [relocation index](../docs/project/FILE_RELOCATION.csv) provides the new locations. Rendering-only states do not establish natural reachability or save persistence.
