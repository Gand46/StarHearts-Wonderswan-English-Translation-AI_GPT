# Star Hearts F36 — purchase labels and initial actor names

2026-10-06. Japanese to English. Cumulative source continuation of the hash-verified F35 build. Classification: **internal testing**; this is not a whole-game linguistic or visual approval.

F36 translates the two Japanese graphics observed in the buying interface, **バザー → Bazaar** and **買う？ → Buy?**. It also resolves and translates all **181 initial actor-name fields** identified by the F35 audit, plus **one additional real opcode 0022 name operand** discovered while investigating those fields. Astra performed the independent consumer analysis and the native 181-field loading test.

## Original and output identity

| File | Size | SHA-256 | WS checksum |
| --- | --- | --- | --- |
| Original Japanese ROM | 4,194,304 bytes | `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255` | `8EED` |
| F35 reference | 4,194,304 bytes | `6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084` | `8BE9` |
| F36 | 4,194,304 bytes | `da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2` | `775C` |

Direct JP→F36 BPS SHA-256: `038daaa050834cf5532beaf74f4431f2cfbe60b9d79c481ef8845c6860b0653d`.

F35→F36 changes **2,425 bytes**. Every changed byte is accounted for by the two compressed graphics, 181 fixed name fields, the additional inline name, and the final checksum. Code, pointers, resource tables, palettes, actor identifiers and the four metadata bytes following each fixed name remain unchanged. Original and earlier translated ROMs were kept immutable.

## Build and apply

Requires Python 3 and Pillow, as in the earlier cumulative source package.

Windows:

```text
BUILD.bat "C:\path\Star Hearts (Japan).wsc" -o "C:\path\StarHearts_F36.wsc" --bps "C:\path\StarHearts_F36.bps"
```

Linux/macOS:

```text
python3 scripts/build_phase13BG_F36.py /path/to/original.wsc -o /path/to/StarHearts_F36.wsc --bps /path/to/StarHearts_F36.bps
```

The complete earlier cumulative sources are included. The builder reconstructs F35 from the clean Japanese ROM, regenerates the new graphics from native glyph references, inserts the guarded name fields, updates the checksum, checks the expected F36 hash, and generates a BPS directly from JP. End users apply only the cumulative BPS to their original Japanese ROM; no incremental patch chain is required.

The Linux/Python build was executed successfully. Windows and macOS wrappers were inspected and updated; those operating-system routes were not executed here. An independent supplied `WS_Patch_Tools_v0.1.1` BPS applicator reproduced the build byte for byte. Wrong source, corrupt/truncated patch, wrong integration base and a modified manifest offset were all rejected. See `qa/F36/build_verification.json`.

## Graphics: two local changes

| Label | Resource / frame | Compressed ROM address | New / available bytes |
| --- | --- | --- | --- |
| Bazaar | Bank 30 resource 15, frame 2 | `0x30F931` | 308 / 536 |
| Buy? | Bank 30 common resource 0, frame 15 | `0x308E2B` | 138 / 170 |

Both blocks fit in their existing compressed slots. No relocation or pointer change was needed. Unused bytes after the new compressed streams remain untouched. Other frames of both resource containers decode identically to F35.

Letters use the exact native CP932 glyph masks already captured in `assets/F32/native_latin_atlas.png` and recorded in `native_latin_glyphs.json`. Horizontal empty margins are trimmed; vertical glyph pixels are preserved. The question mark is copied from the original purchase graphic. The purchase prompt retains its native one-pixel shadow; the title retains colour index 11. Neither the shared font nor the shared renderer was changed.

Decoded changes are confined to the header rectangle `[8,0,80,14)` and prompt rectangle `[4,1,52,14)`. Native Mesen captures visibly read **Bazaar** and **Buy?**, with no clipping or frame changes. The equivalent buying screenshots have 174 changed pixels before the prompt and 369 with the prompt open, all in the intended areas. Every captured selling frame was byte-identical to the equivalent F35 capture. Final F36 screenshots also matched the independently tested graphical integration.

## The 181 fields: confirmed name consumers, not inert metadata

Every candidate is the 16-byte name field of an actual opcode `0004` actor record, eight bytes after that opcode. The dispatch at `0x3931F8` calls `0x390EDA`; the two loading paths copy eight words into `actor + 0x62`:

- 180 records: copy instruction `0x3973C8` in the `0x397348` path.
- 1 record, Belphego: copy instruction `0x391FA6` in the `0x391F30` path.

The speaker bridge at `0x39E929` passes that same buffer to native renderer `0x3AB7DE`. Its eight-cell limit permits at most eight CP932 characters (64 nominal pixels). In F35, the Tirawaka record at `0x195816` was captured with a Japanese speaker name below English dialogue; its later English opcode 0022 replacement occurred only after that visible text. This disproves the earlier assumption that a later translated name necessarily hides the initial name.

Translation identity is independently grounded:

- **164 records** use entity IDs `0x01E0..0x027F`. Code at `0x394228` subtracts `0x01E0`, and the far pointer at `0x39424A` identifies the name table at `0x386B60`. Each companion Japanese name begins with that entity's canonical Japanese name. English comes from the resolved current table target, including MTE indirection; five overlong table forms use previously approved eight-character glossary variants.
- **17 exceptions** use explicit glossary/identity evidence and three editorial resolutions. `ポコ` uses **Poco**, already present in translated dialogue and mission text. `えいへい` becomes **Guard**. `ジムス` becomes the documented phonetic romanization **Jimusu**; it is not conflated with a nearby Pergypt Soldier or the different name ジムハ/Jim.

The 181 fields contain 172 distinct English display forms. Each replacement uses fullwidth CP932 Latin glyphs, padded to exactly 16 bytes with zeroes when shorter. Eight-character names fill the whole field, as allowed by the native renderer. The following metadata and all record offsets are preserved. Later shorter aliases such as Tiraw, Belphe and Hrn retain their existing engine/context constraints; the field mapping records full and short forms explicitly.

**181/181 native loading tests pass on the final F36 ROM.** Each test executed the real opcode 0004 through the native event coroutine, observed eight source-word copies and compared all 16 resulting name bytes. These are exhaustive loading checks for the defined 181-field universe. They are not 181 natural scene visits or 181 individual visual approvals. The Tirawaka eight-character name and the extra inline Tiraw name are directly visible in the retained screenshots. Per-record evidence and scoped statuses are in `qa/F36/companions/`.

## Additional name outside the 181

At `0x1B7D30`, a real opcode 0022 has a Japanese operand at `0x1B7D32`. It ends before control bytes `1C 00 3C 00`, rather than the narrower grammar used by the previous 216-operand scan. F36 changes its ten-byte `ティラワカ` operand to the existing five-character alias **Tiraw**, preserving the following control. The native trace and screenshot confirm the translated result. This is recorded separately and is not added to the 181 denominator.

## Reproduce the diagnostic evidence

Mesen 2.1.1 Linux executable SHA-256: `ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41`. Obtain the emulator separately. Diagnostic base state `qa/P4_repair_synthetic_entry.mss`, SHA-256 `edde91825ed7c9bf5669ef3317bb1210a6ca331fe432f220a2143914b15b3059`, comes from the prior F34 P4 synthetic checkpoint and was reused with documented F36 changes.

For shop replay, set absolute `OUT` and `BASESTATE` environment paths and `MODE=buy` or `MODE=sell`. Run:

```text
Mesen --testRunner --doNotSaveSettings --debug.scriptWindow.allowIoOsAccess=true --timeout=35 /absolute/qa/F36/trace_shop.lua /absolute/StarHearts_F36.wsc
```

The supplied Linux binary also needed `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6` in this host. Replays stop after 840 frames and were bounded by an external 45-second timeout. For the 181 test, use `qa/F36/companions/trace_all_copies.lua`, set `TARGETS` to its adjacent `targets.lua`, and set `EXPECT=after`; use the same base state and final F36 ROM. `probe.lua` and the accompanying Astra report document the representative name routes.

Access classification: **WRAM_POKE**, using a synthetic checkpoint, native event-coroutine seeding and diagnostic actor/inventory setup. The scripts do not write ROM. Stored scene states are synthetic diagnostic states tied to the F36 hash; they do not establish save persistence or natural progression. All four delivered shop states were created from CPU callbacks and reloaded successfully; the two buying states and first selling state reproduced identical pixels after five frames, while the second selling state continued its menu transition. Mesen's uninitialized-read diagnostics are retained in the logs; no broad gameplay stability claim is inferred from these tests.

## Scope of closure and remaining work

| Area | Outcome |
| --- | --- |
| Two buying graphics | Integrated; native runtime, direct visual reading and bounded regression pass |
| 181 initial-name fields | Consumers resolved; translations integrated; 181 native copies pass |
| Additional inline name | Integrated and native render confirmed |
| Build, checksum, cumulative BPS | Byte-exact pass, including independent BPS application |
| Individual visual approval of all 181 scene/name combinations | Not claimed; representative rendering only |
| Natural playthrough, final F36 hardware test, whole-game linguistic/visual approval | Not validated by this iteration |

The four previously identified Japanese graphics **対戦？**, **値段？**, **伝授？** and **戻す？** remain unchanged and require consumer tracing. This iteration does not close all raw CP932 candidates or all other graphical resources. **FINAL_APPROVED remains false.** The 181-field uncertainty is closed as a defined consumer/integration task; whole-game translation completeness is a separate question.

See `phase13BG_F36_manifest.json` for bounded writes, `assets/F36/translation_mapping_181.csv` for editorial provenance, and `qa/F36/` for screenshots, diagnostic states, traces, build verification and Astra's independent analysis. Token savings were not measured.
