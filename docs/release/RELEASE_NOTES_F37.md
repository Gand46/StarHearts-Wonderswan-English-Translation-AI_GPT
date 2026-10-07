# Star Hearts English F37 — Test Build

F37 translates the four remaining common prompt graphics identified in the preceding audit: **Battle?**, **Price?**, **Teach?** and **Return?**. It retains the F36 Bazaar/Buy? graphics, all 181 initial actor-name corrections and the additional inline name.

Apply `StarHearts_EN_phase13BG_F37_CUMULATIVE_FROM_JP.bps` directly to the original Japanese ROM. No prior patch is needed.

- Original ROM: 4,194,304 bytes; SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`.
- F37 ROM: SHA-256 `f0791dcf53045afc126ce11ed5b9eb7091c47c1c8195eaa525737c5fec5ffb57`; WS checksum `DB46`.
- BPS: 649,925 bytes; SHA-256 `dba7b7f5cd2a4980f2ae7af9ed80b5bef6b8042279dda0f46ba00084696eddde`.

The cumulative build and independent patch application match byte for byte. All four prompts pass native rendering and diagnostic state reload checks under synthetic access; 36 normal shop captures match F36. Astra audited 77 direct decoder calls and 19 mode records without finding a selector for these four frames in those paths.

This is an **experimental/internal test pre-release**, not an approved final translation. Synthetic evidence verifies rendering, not a natural route or the actions named by these labels. Whole-game approval and F37-specific hardware validation remain outside this evidence.

The source ZIP includes the cumulative build inputs, Windows/macOS/Linux entry points, English documentation, technical addresses, consumer traces, screenshots, diagnostic savestates and file hashes. No complete ROM, BIOS or emulator is included.
