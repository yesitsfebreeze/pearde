#!/usr/bin/env bash
# the-daemon-must-not-write-into-a-board-path-it-no-longer-own — probe harness.
#
# `planlib.state_dir()` ran `os.makedirs(<board>/.state)` unconditionally, and
# makedirs makes every intermediate directory — so naming the state corner of a
# board that had moved (`.pearde/` -> `pearde/`, this repo's own 92e318c) put
# the board directory BACK at the name the project had moved off. The daemon
# holds absolute paths captured at registration, so its own writers —
# `save_entry`, `drop_entry`, and `scan`'s parse cache — were the ones doing it,
# in projects the daemon does not belong to. Measured live on 2026-09-02: this
# board's daemon on port 8443 had written both a serve.json and a 12 MB
# parse-cache.json into a neighbouring project's abandoned `.pearde/`.
#
# Fixtures are made at run time under <ROOT>/.probe-daemon-path and removed on
# the way out. NOT under /tmp: `serve.EPHEMERAL` makes `save_entry` a no-op
# there, which would hide the very write this harness measures. Nothing here
# touches a real board, a real daemon or a real registry. Run as:
#   bash pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
cd "$ROOT" || exit 1

pass=0; fail=0
ok()  { pass=$((pass+1)); echo "  ok    $1"; }
bad() { fail=$((fail+1)); echo "  FAIL  $1"; }

out="$(PEARDE_ROOT="$ROOT" python3 "$HERE/repro.py" 2>&1)"
while IFS= read -r line; do
  case "$line" in
    PASS\ *) ok "${line#PASS }" ;;
    FAIL\ *) bad "${line#FAIL }" ;;
  esac
done <<< "$out"

# The denominator is pinned: a harness that loses a check to an import error
# and reports "0 checks · 0 pass · 0 fail" exits 0 and reads as success.
if [ "$((pass+fail))" -ne 10 ]; then
  bad "the probe reported $((pass+fail)) checks, not the 10 it defines — it did not run"
  echo "$out"
fi

echo "$((pass+fail)) checks · $pass pass · $fail fail"
echo "probe harness complete"
[ "$fail" -eq 0 ] || exit 1
