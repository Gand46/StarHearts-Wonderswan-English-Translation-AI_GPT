#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 source/scripts/build_phase13BG_F37.py "$@"
