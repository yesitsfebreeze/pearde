#!/usr/bin/env bash
# every-artifact-lands-inside-the-board — the verify command of the memo of
# the same name. Run from the repo root:
#
#     bash resources/invariants/every-artifact-lands-inside-the-board.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not. Three checks,
# in the order a break shows up:
#
#   1. this tree      — no `.state/` corner anywhere but inside a `.pearde/`
#   2. a fresh board  — the whole command surface driven against a throwaway
#                       project, and nothing lands in it outside `.pearde/`
#   3. the mechanism  — the guard still refuses a round writing a board file
#                       into a `.state/` that is not the board's
#
# Check 2 is the one that catches a regression: a writer that spells a path
# relative to the working directory instead of `plan.py state_dir(board)`
# creates its file next to the board, and the diff of the project tree names
# it. `.gitignore` is the one path pearde is allowed to touch outside the
# board — the ignore rule for `.pearde/.state/` has to sit in a file git
# reads, and git reads the parent repo's.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd -P)
R="$REPO/resources"
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }

# ── 1. no `.state/` outside a board in this tree ─────────────────────────────
stray=$(find "$REPO" -name .git -prune -o -type d -name .state -print 2>/dev/null \
        | sed "s|^$REPO/||" | grep -v '^\.pearde/\.state$' || true)
if [ -n "$stray" ]; then
  no "a .state/ outside the board:"
  printf '        %s\n' $stray
else
  okr "no .state/ in this tree but the board's own"
fi

# ── 2. a throwaway project, driven ───────────────────────────────────────────
D=$(mktemp -d) || exit 1
trap 'rm -rf "$D"' EXIT
P="$D/probe-board"
mkdir -p "$P"
git -C "$P" init -q
git -C "$P" config user.email invariant@local
git -C "$P" config user.name invariant
printf 'x\n' > "$P/README.md"
git -C "$P" add -A && git -C "$P" commit -qm init >/dev/null

# the guard's own session cache is machine-local and must not be written by a
# check; PEARDE_AS keeps `add` from asking which persona is working.
export PEARDE_GUARD_STATE="$D/guard"
export PEARDE_AS=engineer
py() { python3 "$R/pearde.py" "$@" >/dev/null 2>&1 || true; }

outside() {   # every path in the project that is not .git/ and not .pearde/
  ( cd "$P" && find . -mindepth 1 \
      \( -path './.git' -o -path './.git/*' \
         -o -path './.pearde' -o -path './.pearde/*' \) -prune -o -print ) \
    | sed 's|^\./||' | sort
}

cd "$P" || exit 1
py init --name pearde-invariant-probe
py add "a thing the board must carry"
py scan
py plan
py gantt
py next
py set a-thing-the-board-must-carry analyzing
py claim a-thing-the-board-must-carry w1
py release a-thing-the-board-must-carry
py sweep
py memo add "a decision the probe records"
py memo check
py workflow check
py upgrade
py doctor
python3 "$R/memos.py" index "$P/.pearde" >/dev/null 2>&1 || true
printf '{"workspace":{"current_dir":"%s"},"model":{"display_name":"x"},"transcript_path":""}\n' \
  "$P" | bash "$R/statusline.sh" >/dev/null 2>&1 || true
cd "$REPO" || exit 1

# `serve.py ensure` runs from `init`; leave the machine's daemon as it was.
python3 "$R/board/serve.py" forget pearde-invariant-probe >/dev/null 2>&1 || true

made=$(outside | grep -v '^README\.md$' | grep -v '^\.gitignore$' || true)
if [ -n "$made" ]; then
  no "the commands wrote outside the board:"
  printf '        %s\n' $made
else
  okr "a driven board wrote nothing outside .pearde/ (bar .gitignore)"
fi

# ── 3. the guard still refuses a round writing the file by hand ──────────────
hook() {   # hook <path> -> the guard's stdout
  printf '{"tool_name":"Write","cwd":"%s","session_id":"invariant","tool_input":{"file_path":"%s","content":"x"}}' \
    "$P" "$1" | python3 "$R/guard.py" pre 2>/dev/null
}
if printf '%s' "$(hook "$P/.state/round.md")" | grep -q '"permissionDecision": "deny"'; then
  okr "the guard refuses a round file written outside the board"
else
  no "the guard let a round file be written to $P/.state/round.md"
fi
if printf '%s' "$(hook "$P/.pearde/.state/round.md")" | grep -q '"deny"'; then
  no "the guard refuses the board's own round file — the rule is too wide"
else
  okr "the guard passes the board's own round file"
fi

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
exit $([ "$FAIL" = 0 ] && echo 0 || echo 1)
