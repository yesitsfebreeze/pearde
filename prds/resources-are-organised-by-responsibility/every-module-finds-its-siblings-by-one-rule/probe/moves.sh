#!/usr/bin/env bash
# The one measurement this PRD is about: can a file move under resources/
# with no second edit anywhere?
#
#   probe/moves.sh <src-worktree>
#
# Copies the tracked tree into a temp dir, applies one move, and asks the
# CLI whether it still stands. Four cuts, hardest last:
#
#   0  nothing moved            — the control; must pass or the rest is noise
#   1  one loose module down    memos.py -> resources/text/memos.py
#   2  one board module up      ramp.py    -> resources/ramp.py
#   3  the whole directory      resources/board -> resources/core
#
# A cut passes when `pearde help` exits 0 and prints the same number of
# command rows as the control, and `pearde workflow list` still runs.
set -u
SRC="${1:?usage: moves.sh <worktree>}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

stage() {  # stage <dir> — tracked files only; untracked reads as a regression
  mkdir -p "$1"
  ( cd "$SRC" && git ls-files -z ) \
    | ( cd "$SRC" && rsync -a --files-from=- --from0 . "$1" )
}

rows() {   # rows <dir> — the command-row count `help` prints, 0 when none
  ( cd "$1" && python3 resources/pearde.py help 2>/dev/null ) \
    | grep -c '^  pearde '
}

runs() {   # runs <dir> <args…> — 0 when the command exits 0
  ( cd "$1" && python3 resources/pearde.py "${@:2}" >/dev/null 2>&1 )
}

anchors() {  # anchors <dir> — manifest rows index.py can resolve; 0 when broken
  ( cd "$1" && python3 resources/pearde.py index files 2>/dev/null ) | grep -c .
}

BASE="$WORK/base"; stage "$BASE"
CTRL=$(rows "$BASE")
echo "cut 0  nothing moved                    rows=$CTRL"
ANCH=$(anchors "$BASE")
echo "cut 0  nothing moved                    anchors=$ANCH"
[ "$CTRL" -gt 20 ] && [ "$ANCH" -gt 20 ] || { echo "control is broken — stop"; exit 2; }

FAIL=0
cut() {  # cut <name> <mover…>
  local name="$1"; shift
  local d="$WORK/$name"; stage "$d"
  ( cd "$d" && "$@" )
  local r; r=$(rows "$d")
  local w="ok"; local extra=""
  [ "$r" = "$CTRL" ] || { w="BROKEN"; FAIL=1; }
  # `help` alone only proves discovery. These prove the cross-module
  # imports and the manifest reader survived the move too.
  local a; a=$(anchors "$d")
  if [ "$w" = ok ]; then
    [ "$a" = "$ANCH" ] || { w="BROKEN"; extra=" (index files $a/$ANCH)"; FAIL=1; }
  fi
  if [ "$w" = ok ]; then
    runs "$d" specced --help || { w="BROKEN"; extra=" (specced --help failed)"; FAIL=1; }
  fi
  if [ "$w" = ok ]; then
    runs "$d" memo --help || { w="BROKEN"; extra=" (memo --help failed)"; FAIL=1; }
  fi
  printf 'cut %-6s %-28s rows=%-4s %s%s\n' "$name" "$MSG" "$r" "$w" "$extra"
  if [ "$w" = BROKEN ]; then
    ( cd "$d" && python3 resources/pearde.py help 2>&1 >/dev/null | head -3 | sed 's/^/       /' )
  fi
}

mv_loose() { mkdir -p resources/text && mv resources/memos.py resources/text/memos.py; }
mv_up()    { mv resources/board/ramp.py resources/ramp.py; }
mv_dir()   { mv resources/board resources/core; }

MSG="memos.py -> text/"        cut 1 mv_loose
MSG="board/ramp.py -> up"      cut 2 mv_up
MSG="board/ -> core/"          cut 3 mv_dir

echo
[ "$FAIL" = 0 ] && echo "PASS — a file moves with no second edit" \
                || echo "FAIL — a move still needs a second edit"
exit "$FAIL"
