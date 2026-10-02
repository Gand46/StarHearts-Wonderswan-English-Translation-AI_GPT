# F14 runtime QA

Important: each `--testRunner` execution must start from a clean Mesen profile or with the per-ROM `Saves/*.sav`, `Saves/*.ieeprom` and `SaveStates/*` removed. The emulator creates an initialized 32 KiB `.sav` even before a verified in-game Save Drum save, so the mere existence of `.sav` is NOT evidence of persistence.

`route_wampa_second_west_F14.lua` deterministically reaches the second-west village screen from a clean New Game path. It is a navigation checkpoint, not proof that Wampa/Save Drum was reached.

Do not declare Save/Continue PASS unless a screenshot of `SAVED!` is captured and the exact SRAM generated after that point survives two independent cold-process Continue cycles.
