# F8 runtime QA scripts

Use Mesen 2.1.1 TestRunner with a clean save directory for each case.

Environment variables:
- `MESEN_OUTDIR`: directory for screenshots and buffer dumps.
- `MESEN_LUA_REPORT`: output text report.

Scripts:
- `route_hero_short_F8.lua`: 1-glyph hero name and C0DE dump.
- `route_hero_max_F8.lua`: 8-glyph hero name and C0DE dump.
- `route_options_F8.lua`: natural New Game route to in-game menu / Options.

These scripts do not use savestates or external RAM writes.
