# I14-P3 — Alternative route and diagnostic validation

Date: 2026-09-27  
ROM authority: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`  
Result: `ALTERNATIVE_METHODS_COMPLETE_EXTERNAL_VALIDATION_REQUIRED`  
Release status: `RC_NOT_AUTHORIZED`

## Scope and acceptance boundary

This pass used two non-equivalent methods: controller-only natural exploration from the documented F18 checkpoint, and controlled activation of real F30 event scripts. The latter changes only runtime execution state and is diagnostic by definition. It never supplies route provenance and therefore cannot produce a natural PASS.

No ROM, BPS, source, SRAM or release data was modified. Savestates and private ROMs are excluded from this package; their hashes are recorded in `runtime/p3/PRIVATE_PROVENANCE.json`.

## Results

| Target | Result | Evidence | Consequence |
|---|---|---|---|
| Inde route exploration | `NATURAL_PARTIAL_PROGRESS` | Two additional map-sector transitions reproduced by controller-only input; replay, state trace and captures preserved | Holy Temple still not reached |
| Second First Trial banner | `CONTROLLED_DIAGNOSTIC_PASS` | 58 reads from the real F30 text range and a legible `Event: First Trial` render | Consumer validated; natural route remains open |
| Tirawaka name/dialogue | `CONTROLLED_DIAGNOSTIC_PASS` | 15 reads from the real F30 name range, native speaker handler hit and legible dialogue | Consumer validated; natural encounter remains open |
| Scene `01DE`, script `20A01C` | `REJECTED_BY_CONTROLLED_EXECUTION` | 374 target reads; ordinary Wampa/trial dialogue, no ending transition | Not an ending/credits entry point |
| Scene `01DE`, script `20A43C` | `REJECTED_BY_CONTROLLED_EXECUTION` | 203 target reads; ordinary dialogue, no ending transition | Not an ending/credits entry point |

The previous assumption that a stable `CAD7=0000` meant no map progress was false: the controller-only run crossed visible sectors while `CAD7` remained unchanged. Future external capture should use the map bytes logged in the P3 state traces in addition to the scene field.

## Internet-derived route corrections

The researched route places Fire before Animd/Peljipt, and the second Inde visit plus Holy Temple only after Peljipt, the pyramid and Alsimbal. The Holy Temple B2F dead-end requires a bomb. The final route is substantially later and passes through Big Blank and three time periods before the final castle. These corrections rule out attempting ending or the second trial directly from the early F18 grass checkpoint.

Sources and extraction notes are recorded in `runtime/p3/ADVANCED_INTERNET_RESEARCH.md`.

## Gate decision

The six real-game cases remain open: five `EXTERNAL_PLAYTEST_REQUIRED` and Link `EXTERNAL_HARDWARE_OR_SUPPORTED_PEER_REQUIRED`. Controlled activation proves that selected localized consumers execute, but does not satisfy natural progression, save provenance, or uninterrupted ending-to-credits requirements. There are still 0 `AUTOMATED_NATURAL_PASS` cases, so RC remains unauthorized.

