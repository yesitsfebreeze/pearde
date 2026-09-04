#!/usr/bin/env bash
# verify — the harness for `a claim names the process that holds it`.
# `doctor.sh --harnesses` runs this with no arguments and from its own cwd,
# so the tree is resolved here: `PEARDE_ROOT` when it is set (that is how a
# lane's build is proved before it merges), else the repo above the board
# this file sits under — the board is its own nested git repo (often reached
# through a `.pearde` symlink), so `git -C "$HERE" rev-parse --show-toplevel`
# answers with the board itself, never the code repo one level up.
set -u
HERE=$(cd "$(dirname "$0")" && pwd -P)
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD=$(dirname "$BOARD"); done
ROOT=${PEARDE_ROOT:-$(dirname "$BOARD")}
[ -n "$ROOT" ] && [ -f "$ROOT/resources/pearde.py" ] || { echo "FAIL  no tree to test — set PEARDE_ROOT"; exit 1; }
exec bash "$(cd "$(dirname "$0")" && pwd)/probe/probe.sh" "$ROOT"
