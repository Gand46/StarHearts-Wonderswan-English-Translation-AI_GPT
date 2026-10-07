# File integrity

[SHA256SUMS.json](SHA256SUMS.json) contains SHA-256 values keyed by paths relative to the repository root. It covers all packaged files except itself.

The inventory under `history/` describes the preceding flat package, using its earlier paths. It is retained for provenance. Use [FILE_RELOCATION.csv](../docs/project/FILE_RELOCATION.csv) to connect those earlier locations and hashes to the organized repository.

The current ROM and BPS identities are recorded separately in [PROJECT_STATE_F37.json](../docs/status/PROJECT_STATE_F37.json). Organizing these files does not change the F37 build.
