# Star Hearts 13BG-F34 — patch instructions

Status: `RC_SYNTHETIC_FOR_TESTING`, not approved as a general final release. Six synthetic cases pass their stated scope; whole-project legibility is not approved.

Bring your own unmodified Japanese Star Hearts WonderSwan Color ROM: 4,194,304 bytes; expected SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. Apply the included cumulative F34 `.bps` once with a BPS compatible patcher. Do not apply previous F patches first. The expected output SHA-256, documented in the I14-P9 audit, is `d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0`; WonderSwan checksum `3CD5`. The source ROM and output ROM are not distributed.

The BPS was checked for internal CRC integrity during packaging. The correct original ROM was unavailable here, so the BPS was not reapplied in this packaging run. The prior audit records a successful Linux/Python rebuild and independent application. Read `RELEASE_NOTES.md` for test scope and limitations.
