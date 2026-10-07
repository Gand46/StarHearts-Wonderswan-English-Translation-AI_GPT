# Validation evidence and remaining scope

## Current authority

F37 output SHA-256: `f0791dcf53045afc126ce11ed5b9eb7091c47c1c8195eaa525737c5fec5ffb57`.

The [current state](../status/PROJECT_STATE_F37.json), [F37 technical report](../technical/TECHNICAL_F37.md) and [per-prompt statuses](../../qa/current/F37/four_prompt_status.json) define the current scope. The global `FINAL_APPROVED` value remains false. The four-prompt translation/render task is closed through documented synthetic evidence.

## Evidence index

| Record | Meaning |
| --- | --- |
| [F37 build verification](../../qa/current/F37/build_verification.json) | Clean build, independent BPS application, checksum and rejection cases |
| [GitHub package verification](../../qa/packaging/F37/verification.json) | Build from the staged repository, exact output identity and preserved build inputs |
| [Evidence reuse](../../qa/current/F37/evidence_reuse.json) | Unchanged 181 fields, metadata, inline name and static-consumer dependencies |
| [Astra consumer report](../../qa/current/F37/astra/static_report.txt) | Bounded routing analysis and its limitations |
| [Astra scan](../../qa/current/F37/astra/scan.json) | Structured calls, modes and selectors |
| [Pixel regression](../../qa/current/F37/pixel_regression.json) | Changes confined to the tested prompt rectangles |
| [Shop regression](../../qa/current/F37/shop_regression.json) | 18 buying plus 18 selling captures unchanged from F36 |
| [State reload](../../qa/current/F37/state_reload/reload.csv) | Four F37 prompt states loaded successfully |
| [181-field results](../../qa/history/F36/companions/final_summary.json) | 181 native-copy passes; one initial-name field individually visualized in the preserved evidence |
| [181 mappings](../../source/assets/F36/translation_mapping_181.csv) | Per-field translation and provenance |

## Savestate provenance

Use Mesen 2.1.1 with the ROM hash associated with each record. Compatibility is not asserted for unrelated builds or other emulator versions.

| Location | Build/origin | Scope |
| --- | --- | --- |
| `qa/shared/checkpoints/P4_repair_synthetic_entry.mss` | Inherited F34 P4 diagnostic checkpoint; SHA-256 `edde91825ed7c9bf5669ef3317bb1210a6ca331fe432f220a2143914b15b3059` | Synthetic seed used by later replays |
| `qa/history/F36/shop_buy/` and `qa/history/F36/shop_sell/` | F36 synthetic shop replays; exact ROM hash in the historical F36 report | Historical shop rendering and transitions |
| `qa/current/F37/runtime/F37/prompt_*/SYNTHETIC_PROMPT_RENDER_ONLY.mss` | F37; WRAM fixture plus native graphics-selector injection | Render only; do not interpret the underlying shop action as the substituted label |

All four F37 states were reloaded and their popup images matched the reference pixels after five frames. The current Lua scripts and replay instructions are included. Historical replay scripts remain research records and may refer to fixtures outside this curated package; use the F37 instructions for the current supported reproduction route.

## Remaining scope

- A complete natural playthrough, whole-game Japanese-text census and global linguistic/visual review are not established by this iteration.
- The 181/181 result is exhaustive native loading coverage for the defined name fields, not exhaustive individual scene rendering or natural reachability.
- No natural selection of the four F37 prompts was found in the audited paths. Their rendering passes synthetically; global non-use is not proven.
- Actions suggested by the substituted labels were not executed. No gameplay feature was enabled by translating them.
- F37-specific hardware validation and Windows/macOS build execution remain unperformed here.
- Earlier F35 hardware observations are historical. They are not a newly reproduced F37 defect or a current hardware compatibility verdict.

The unchanged ROM/BPS identity lets this packaging operation reuse the recorded runtime evidence. No emulator run was added solely for reorganizing documentation. Token savings were not measured.
