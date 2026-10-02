#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 scripts/build_phase13BG_F34.py "$@"
