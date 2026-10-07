# Changelog

## F37 repository organization — 2026-10-06

- Reduced the top level from 61 files to 7, including the two Git configuration files.
- Grouped cumulative builders, assets and the baseline under `source/`; classified 49 manifests into D, E and F subfolders.
- Classified current documentation by technical report, status, validation, release and project metadata; archived reports are grouped by build.
- Separated current F37 QA, historical evidence, shared checkpoints and package checks. Added folder guides and a complete old-to-new file index.
- Updated manifest lookup paths and Windows/macOS/Linux entry points for the new source root.
- Rebuilt from the original Japanese ROM after relocation and checked byte identity with the known F37 ROM and BPS. No new ROM revision is introduced.

## F37 GitHub packaging — 2026-10-06

- Prepared an English repository README, release notes, credits and validation index.
- Moved older root reports to `docs/history/` and the current Spanish report to `docs/es/`.
- Preserved every cumulative build dependency, the F37 ROM identity and the existing end-user BPS.
- Added dependency and Git configuration files; marked shell wrappers executable.
- Retained current and historical QA records, diagnostic states and screenshots with their original build scope.
- Verified the packaged build from the clean Japanese ROM. Packaging does not create a new ROM revision or broaden its quality approval.

## F37 — 2026-10-06

- Translated common prompt frames 12, 13, 14 and 17 to Battle?, Price?, Teach? and Return?.
- Reused native Latin masks and the original question-mark design.
- Relocated frame 17 to `0x30FE80`; other three streams remain in place.
- Audited 77 direct decoder calls, 19 mode records and 18 loader callsites with Astra.
- Verified all four prompts in the native renderer with controlled selector injection, and reloaded all four diagnostic states with identical pixels.
- Preserved the 181-name and inline-name corrections. All 36 normal buying/selling captures match F36.
- Remains experimental/internal testing. Natural selection of these four resources and global final approval are not established.

## F36 — 2026-10-06

- Translated Bazaar and Buy? in the purchase interface.
- Resolved and translated 181 initial actor-name fields, preserving their fixed sizes and following metadata.
- Translated an additional real opcode 0022 inline name separately from the 181-field denominator.
- Passed 181/181 native name-copy checks and representative rendering checks.
- Preserved independent consumer analysis, translation provenance and the cumulative build/BPS evidence.

## F35 — historical base

- Redrew 14 main-menu labels on their existing tile grid.
- Preserved menu logic and surrounding surfaces; documented the local typography redesign and bounded synthetic comparison.

See `docs/history/` and the root change manifests for earlier technical history. Historical claims apply to the build identified by each record.
