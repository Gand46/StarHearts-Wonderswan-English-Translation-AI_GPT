# Cumulative source inputs

Run the build entry points from the repository root, as described in [README.md](../README.md).

| Subfolder | Contents |
| --- | --- |
| `scripts/` | Builders, binary/graphics helpers and phase audit tools |
| `manifests/D/` | D-phase change records |
| `manifests/E/` | E-phase change records |
| `manifests/F/` | F-phase change records and F36/F37 integration manifests |
| `assets/` | Glyph references, resource assets and translation tables |
| `baseline/` | Historical baseline BPS required to reconstruct the cumulative result |

The Python entry point is `source/scripts/build_phase13BG_F37.py`. It resolves `source/` from its own location, so source inputs do not depend on the shell's working directory. Keep these subfolders together.

Asset paths stored in integration manifests are relative to `source/`, not the manifest's D/E/F directory. Existing asset bytes and manifests are unchanged. Only the builder's manifest lookup paths were adjusted during organization.
