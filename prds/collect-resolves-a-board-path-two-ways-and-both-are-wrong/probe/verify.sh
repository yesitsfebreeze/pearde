#!/usr/bin/env bash
# collect-resolves-a-board-path-two-ways-and-both-are-wrong — the harness.
#
# Which repo holds a footprint is git's answer, never a string's. Three
# layouts, built fresh under one `mktemp -d` and removed on exit:
#
#   L1  a plain board inside the code repo — the two roots are one and
#       nothing is rerouted.
#   L2  a board with a `.git` of its own. A footprint spelled the code
#       repo's way (`pearde/.gitignore`) and one spelled the BOARD's way
#       (`prds/<prd>/probe/verify.sh`, where every probe on this board is
#       told to live) must BOTH land in the board repo. The second was
#       refused outright: `footprint … is not under <repo> — repo_of
#       matched no repo for it`, which held `two-harnesses-still-name-a-
#       tree-they-do-not-measure` at DONE 7/7 and uncollectable.
#   L3  the CODE repo checked out UNDER the board — what a lane at
#       `<board>/.lanes/<prd>` and a run-session worktree both are. The
#       prefix test read "inside the board's path" as "the board's file",
#       so every footprint of that repo was routed to the board, staged
#       against an index that ignores it, and committed as nothing at
#       all — no error, no refusal, an empty commit.
#
# PEARDE_ROOT names the tree under test; it defaults to the repo above the
# board this file sits in. One line per assertion, a count at the end.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] \
      && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
BOARDLIB="$ROOT/resources/board"

if [ ! -f "$BOARDLIB/collect.py" ]; then
  echo "  FAIL no collect.py under $BOARDLIB"
  echo ""
  echo "1 checks · 0 pass · 1 fail"
  exit 1
fi

OUT="$(python3 "$HERE/cases.py" "$BOARDLIB" 2>&1)"
echo "$OUT"
P="$(printf '%s\n' "$OUT" | grep -c '^  pass  ')"
F="$(printf '%s\n' "$OUT" | grep -c '^  FAIL  ')"
N=$((P + F))
echo ""
echo "$N checks · $P pass · $F fail"
[ "$F" = 0 ] && [ "$N" -ge 7 ]
