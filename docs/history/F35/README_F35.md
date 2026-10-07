# Star Hearts — F35 menu typography (experimental/internal test)

F35 corrects the 14 main-menu labels whose early English 8-pixel graphics have incomplete-looking and uneven strokes. It is a **documented menu-specific redraw**, on the same 8×8 tile grid, 4bpp colour index 8, two columns and 16-pixel row spacing. Every replacement letter has a complete 5×7 bitmap. The menu background, icons, selection frame, bottom `None` field, palette, dispatcher, menu logic, inventory and text of other panels are unchanged. This is not a claim of exact native-font identity; the local typographic redesign is disclosed explicitly.

The version is an internal testing build. The reported AliExpress reproduction-cartridge failure when opening item submenus is unresolved. A readable main menu in Mesen cannot validate that hardware path. Keep `RC_NOT_AUTHORIZED` for hardware compatibility.

## Rebuild from the clean Japanese ROM

Base: 4,194,304 bytes, SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. Supply your own ROM; no commercial ROM is included.

Windows: `BUILD.bat path\to\original.wsc -o F35.wsc`

Linux: `./build.sh /path/to/original.wsc -o F35.wsc`

macOS: `sh build.command /path/to/original.wsc -o F35.wsc`

Python 3 and Pillow are required, as for the bundled image scripts. `build_phase13BG_F35.py` reconstructs all F34 history from the included cumulative sources and applies the menu redraw. It generates a BPS directly from the original JP ROM and checks byte-exact round trip. The convenience wrappers were updated to call F35. Only the Linux/Python route was executed in this environment; Windows and macOS wrappers remain source-reviewed, unexecuted.

F34 SHA-256 `d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0`.

F35 SHA-256 `6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084`, WonderSwan checksum `8BE9` (stored little-endian E9 8B).

Direct JP→F35 BPS SHA-256 `1a26ea54e466e145110cf1c538eea0e126cd046155da819b9a12cc52dce359d3`.

## Change attribution

Resource 1 of Bank 30 starts at `0x309036` (three decoded frames). Frame 0 is a 5,216-byte tile sheet; frame 1 is a 1,024-byte tile map; frame 2 is a 64-byte palette. Tiles for the main labels are displayed in two columns, seven rows. `scripts/rebuild_main_menu_font.py` decodes the existing resource, redraws only its 14 label rectangles, deduplicates tiles, recompresses the graphics in the original frame-0 slot, and relocates only the revised compressed frame-1 data into the verified FF span at `0x30FC0F`. Its three-byte frame-1 relative pointer changes accordingly. The original frame-1 data, palette and all unrelated assets stay intact. Frame 1 uses 625 bytes in that FF span. The decoder and fixed-menu logic are not patched.

The root-menu screenshot of F34 has the same glyph artifacts reported by the user, so this correction is based on an actual rendered failure, not an inferred text string. This redesign improves glyph integrity at the cost of differing slightly from the old English menu graphic style. It does not alter the older JP font or claim a global visual approval.

## Bounded QA

- Build from clean JP and direct BPS application yield byte-identical F35 output; source input and ROM checksum checked.
- Changed bytes F34→F35: 1,749, confined to the menu resource compressed graphics/pointer, the FF relocation span, and checksum. No handler changes.
- Synthetic checkpoint provenance: `qa/P4_repair_synthetic_entry.mss`, SHA-256 `edde91825ed7c9bf5669ef3317bb1210a6ca331fe432f220a2143914b15b3059`, copied from `PRIVATE_CHECKPOINTS/P4_repair_synthetic_entry.mss` in the F34 audit bundle. It is a diagnostic state, not natural progression.
- `qa/menu_key_replay.lua` enters the menu and selects Key Items using controller input. It reads the checkpoint and captures frame 380; it makes no WRAM/SRAM writes. The same replay on F34 and F35 produced the before/after screenshots. Status for the **14 main-menu labels only**: `LEGIBILITY_PASS_SYNTHETIC`, `TYPOGRAPHY_REDRAW_PASS_SYNTHETIC`. Global linguistic/visual and hardware status remain unapproved.
- Pixel comparison of F34/F35 captures: 1,965 changed pixels, all within the two text columns from y=8..119; zero changed pixels elsewhere. Palettes retain the same seven displayed RGB colours in this scene. This does not prove all gameplay surfaces unaffected, only the captured menu state and the bounded binary diff.

The ZIP contains complete cumulative sources and the diagnostic checkpoint/screenshots, without either ROM. The `.bps` is the sole end-user patch. There is no bat/Wine execution or hardware PASS claim.
