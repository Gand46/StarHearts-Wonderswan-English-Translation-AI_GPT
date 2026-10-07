# Star Hearts F37 — four retained prompt graphics

2026-10-06. Japanese to English. F37 completes the translation and synthetic rendering validation of the four common prompt graphics left open in F36. It preserves the earlier 181-name correction and the additional inline name byte for byte.

| Resource 0 frame | Japanese | English | Status |
| --- | --- | --- | --- |
| 12 | 対戦？ | Battle? | Translated, integrated and rendered in Mesen |
| 13 | 値段？ | Price? | Translated, integrated and rendered in Mesen |
| 14 | 伝授？ | Teach? | Translated, integrated and rendered in Mesen |
| 17 | 戻す？ | Return? | Translated, integrated and rendered in Mesen |

**Four-prompt translation/render scope: closed.** The four resources are not selected in the audited menu routes. Their test uses a controlled frame selector in the real decoder and popup renderer. This establishes their rendering, not a natural menu route or the effects of confirming an associated action. The classification is `RECURSO_CONSERVADO_SIN_SELECCION_EN_RUTAS_AUDITADAS`, not a claim that they are globally unused. F37 remains an internal testing build; whole-game final approval is not granted.

## Build and patch identity

All ROMs are 4,194,304 bytes.

| Build | SHA-256 | WonderSwan checksum |
| --- | --- | --- |
| Original JP | `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255` | `8EED` |
| F36 reference | `da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2` | `775C` |
| F37 | `f0791dcf53045afc126ce11ed5b9eb7091c47c1c8195eaa525737c5fec5ffb57` | `DB46` |

Cumulative JP→F37 BPS: 649,925 bytes; SHA-256 `dba7b7f5cd2a4980f2ae7af9ed80b5bef6b8042279dda0f46ba00084696eddde`.

Requires Python 3 and Pillow, as in the preceding cumulative sources. Windows:

```text
BUILD.bat "C:\path\original.wsc" -o "C:\path\StarHearts_F37.wsc" --bps "C:\path\StarHearts_F37.bps"
```

Linux/macOS:

```text
python3 source/scripts/build_phase13BG_F37.py /path/to/original.wsc -o /path/to/StarHearts_F37.wsc --bps /path/to/StarHearts_F37.bps
```

The builder reconstructs all previous work from the original JP ROM, verifies F36, regenerates these four graphics, verifies F37 and writes a BPS directly from JP. No incremental patch chain is required. The Linux/Python route was executed; Windows/macOS wrappers were updated and source-reviewed. Independent BPS application with WS_Patch_Tools v0.1.1 matched the clean build exactly. Wrong base, truncated/corrupt BPS, wrong integration base and an invalid expected resource address were rejected.

## Consumer trace: what was established

Astra audited **77 direct calls** to `A000:254C`, **19 menu mode records**, **18 loader callsites**, and the two direct consumers of alternative decoder `A000:2618`.

The common graphic resource is Bank 30 resource 0 at ROM `0x30843E`, selected through the resource table at `0x30841C`. Initializers explicitly load common frames 0..3. Loader `A000:94F0` reads the bounded mode table at `0x365F94`; its common-frame loop at `A000:9576` selects only frames 4..11, 15 and 16. Each of the 18 identifiable callers supplies bounded mode values covering 0..18. No target frame 12/13/14/17 is selected in those paths.

The apparently dynamic frame selector at `A000:8D2E` belongs to resource 12, not resource 0. The alternate decoder's two consumers select other resource banks and were excluded using their actual data selectors. The decoder indexes one requested frame; it does not implicitly load the omitted frames sequentially.

Full scope and limitations are retained in `qa/current/F37/astra/static_report.txt`, `decoder_routes.csv`, `scan.json` and the focused disassembly. This is bounded positive analysis of the selection paths, not proof of every possible indirect/generated call in the ROM. The relevant code banks, selection tables and resource-table pointer bytes remain identical in F37, so this F36 trace transfers to F37 with explicit byte-equality evidence.

## Graphics and bounded writes

Every prompt is a 448-byte decoded 56×16 bitmap. F37 uses exact native Latin glyph masks from `source/assets/F32/native_latin_glyphs.json`; the original question-mark mask is retained from the F36 reference. No shared font, font mapping, decoder, action handler or palette is changed. Empty horizontal glyph margins are trimmed as in F36; baseline pixels and the native one-pixel shadow are preserved.

| Frame | English width | Encoded bytes | Original slot | F37 compressed address |
| --- | --- | --- | --- | --- |
| 12 | 37 px | 182 | 198 | `0x308BE3` |
| 13 | 32 px | 165 | 194 | `0x308CA9` |
| 14 | 37 px | 179 | 192 | `0x308D6B` |
| 17 | 41 px | 196 | 171 | `0x30FE80` |

The first three remain in place. Return? requires 196 compressed bytes, so it is stored in the verified FF tail at `[0x30FE80,0x30FF44)`, after the F35 menu-map allocation. Only its three-byte relative pointer at `0x308474` changes (`000B48` → `007A42`). The old compressed block at `0x308F86` is preserved but is no longer the source of common frame 17. Its retained raw bytes must not be mistaken for an untranslated current frame.

F36→F37 changes **689 bytes**, confined to the three in-place streams, one frame pointer, the new Return? stream and checksum. Other common frames decode byte-identically. Pixel edits are confined to `[4,1,52,14)` inside each prompt; the outer masks are unchanged. Preconditions, capacities, hashes, native glyph provenance and exact bounds are recorded in `source/manifests/F/phase13BG_F37_manifest.json`. The earlier 181 name fields, metadata and additional inline name are unchanged.

## Runtime and regression evidence

Mesen 2.1.1 Linux executable SHA-256: `ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41`.

The existing P4 synthetic checkpoint seeds the native buying coroutine. At the native common-frame decode (`A000:254C`, `ES:SI=2000:843E`, `DS:DI=0000:4FC0`), the diagnostic script substitutes the requested CX value 15 with exactly 12, 13, 14 or 17. The decoder reads the ROM resource and the existing popup displays it. There are no ROM writes or direct decoded-VRAM writes. The test stops before confirming the displayed action.

Access classification: `WRAM_POKE` for the inherited event fixture, then `POINTER_INJECTION` for the graphics selector. These screenshots use a shop popup as a rendering fixture; Battle?, Price?, Teach? and Return? are not newly enabled shop actions.

Four F36/F37 replay pairs confirm the Japanese original and English replacement in the same native renderer. The visible transcriptions are Battle?, Price?, Teach? and Return?, with no clipped letters or overflow at native scale. Changed pixels are 254/246/223/252 respectively, all inside the popup text. Pre-popup frames are identical. Without selector substitution, all 18 buying and all 18 selling captures match F36 byte for byte.

Four F37 `SYNTHETIC_PROMPT_RENDER_ONLY.mss` states are included, each reloaded successfully with pixel-identical popup output after five frames. They are diagnostic rendering states; their underlying shop action must not be interpreted as the operation named by the substituted graphic. They do not establish save persistence or natural progression. Historical F36 states remain under their original QA directory and retain their F36 provenance.

The inherited P4 state is `qa/shared/checkpoints/P4_repair_synthetic_entry.mss`, SHA-256 `edde91825ed7c9bf5669ef3317bb1210a6ca331fe432f220a2143914b15b3059`. Logs preserve Mesen's diagnostic uninitialized-memory warnings; they are not a whole-game functional PASS. No emulator, ROM or BIOS is distributed.

## Reproduce the checks

Static audit, requiring GNU objdump and the known F36/JP images:

```text
python3 qa/current/F37/astra/trace_four_common.py --rom /path/F36.wsc --jp /path/original.wsc --out /path/new_audit
```

For runtime, create an output folder; set absolute `OUT` and `BASESTATE` paths, `MODE=buy`, and `PROMPT` to 12, 13, 14 or 17. Then run:

```text
Mesen --testRunner --doNotSaveSettings --debug.scriptWindow.allowIoOsAccess=true --timeout=35 /absolute/qa/current/F37/trace_prompt.lua /absolute/F37.wsc
```

This Linux host also used `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6` and an external 45-second timeout. Each replay stops after 660 frames. `reload_states.lua` uses `QA_ROOT` pointing to `qa/current/F37` and an `OUT` directory to reload all four states. The portable static script reproduced the original scan JSON exactly.

The package includes complete cumulative sources, the current direct BPS, four-prompt status records, traces, comparison images and diagnostic states. Earlier 181-field evidence is reused because the fields and consumers remain byte-identical. No new all-game census, natural playthrough, final F37 hardware test or global linguistic/visual approval is claimed. The four graphics are no longer pending translation; their natural selection remains unestablished outside the audited routes. Token savings were not measured.
