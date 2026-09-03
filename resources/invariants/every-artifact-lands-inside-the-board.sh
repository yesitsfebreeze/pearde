#!/usr/bin/env bash
# every-artifact-lands-inside-the-board — the verify command of the memo of
# the same name. Run from the repo root:
#
#     bash resources/invariants/every-artifact-lands-inside-the-board.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not. Five checks,
# in the order a break shows up:
#
#   1. this tree      — no `.state/` corner anywhere but inside the board
#   2. the install    — pearde writes nothing into its own directory: no
#                       `resources/board/state/`, and no source line that
#                       roots a writable path at the install
#   3. a fresh board  — the whole command surface driven against a throwaway
#                       project, and nothing lands in it outside `.pearde/`
#   4. the install, after driving — the surface of check 3 left the install
#                       byte-identical, daemon and guard included
#   5. the mechanism  — the guard still refuses a pass writing a board file
#                       into a `.state/` that is not the board's
#
# Checks 3 and 4 are the ones that catch a regression. A writer that spells a
# path relative to the working directory instead of `plan.py state_dir(board)`
# creates its file next to the board, and the diff of the project tree names
# it; a writer that roots a path at the install instead shows up as a new file
# under `resources/`. `.gitignore` is the one path pearde is allowed to touch
# outside the board — the ignore rule for `.pearde/.state/` has to sit in a
# file git reads, and git reads the parent repo's.
#
# The install had one exemption until 2026-09-01: `plan.py MACHINE_DIR`,
# `resources/board/state/`, holding the daemon registry, its log, the
# calibration fit and the guard's session cache. That is decided and gone —
# one root, the board's `.pearde/` — so checks 2 and 4 exist to keep it gone.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd -P)
R="$REPO/resources"
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }

# ── 1. no `.state/` outside a board in this tree ─────────────────────────────
# A lane is a git worktree of this repo (`.pearde/.lanes/<slug>/`), so it
# carries a whole checkout — its own board, and that board's own `.state/`.
# That is the worker's state inside the worker's board, which is what this
# check is for, so the lanes are excluded rather than counted as strays.
stray=$(find "$REPO" -name .git -prune -o -type d -name .state -print 2>/dev/null \
        | sed "s|^$REPO/||" | grep -vE '^\.?pearde/\.state$' \
        | grep -vE '^\.?pearde/\.lanes/' || true)
if [ -n "$stray" ]; then
  no "a .state/ outside the board:"
  printf '        %s\n' $stray
else
  okr "no .state/ in this tree but the board's own"
fi

# ── 2. the install is not a place this tool writes ───────────────────────────
if [ -e "$R/board/state" ]; then
  no "the install holds a state dir: resources/board/state — MACHINE_DIR is back"
else
  okr "the install holds no state dir of its own"
fi

# and no source line roots a writable path at the install. The one surviving
# mention is LEGACY_MACHINE_DIR, whose whole body moves the old directory into
# the boards and deletes it — so the name is allowed exactly where the
# migration defines and uses it.
bad_machine=$(grep -rn --include='*.py' 'MACHINE_DIR' "$R" 2>/dev/null \
  | grep -v '__pycache__' | grep -v 'LEGACY_MACHINE_DIR' || true)
if [ -n "$bad_machine" ]; then
  no "MACHINE_DIR is referenced outside the legacy migration:"
  printf '        %s\n' "$bad_machine"
else
  okr "no MACHINE_DIR outside the one-shot migration"
fi

# ── 3. a throwaway project, driven ───────────────────────────────────────────
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
# `init` runs `serve.py ensure`, and with no port named that reaches the
# machine's real daemon on 8443 and registers this `mktemp -d` board into it —
# a throwaway path the daemon then watches until somebody notices. Port 1 is
# privileged and nothing is listening on it, so every command below refuses to
# connect instead: no registration to undo, and no repair that has to run
# after the fact on a line with no trap behind it.
export PEARDE_PORT=1
py() { python3 "$R/pearde.py" "$@" >/dev/null 2>&1 || true; }

outside() {   # every path in the project that is not .git/ and not the board
  # both board names: `.pearde/` is what init makes, `pearde/` the legacy
  # name a board that has not run `pearde upgrade` still carries
  ( cd "$P" && find . -mindepth 1 \
      \( -path './.git' -o -path './.git/*' \
         -o -path './.pearde' -o -path './.pearde/*' \
         -o -path './pearde' -o -path './pearde/*' \) -prune -o -print ) \
    | sed 's|^\./||' | sort
}

# what the install looks like before the surface runs against the probe. The
# daemon and the guard are the two that used to write here.
installed() { find "$R" -name '__pycache__' -prune -o -print | sort; }
before=$(installed)

cd "$P" || exit 1
py init --name pearde-invariant-probe
# the board init made, under whichever of the two names this tree gives it —
# `.pearde/` is what init makes, `pearde/` on a board that has not upgraded
B="$P/.pearde"; [ -d "$B" ] || B="$P/pearde"
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
python3 "$R/memos.py" index "$B" >/dev/null 2>&1 || true
printf '{"workspace":{"current_dir":"%s"},"model":{"display_name":"x"},"transcript_path":""}\n' \
  "$P" | bash "$R/statusline.sh" >/dev/null 2>&1 || true
cd "$REPO" || exit 1

# PEARDE_PORT=1 above is what keeps the machine's daemon out of this; this
# line stays as a second net for a board that landed there before that export
# existed, and it names the port too so it cannot itself become the reach.
PEARDE_PORT=1 python3 "$(ls "$R"/serve.py "$R"/*/serve.py 2>/dev/null | head -1)" forget pearde-invariant-probe \
  >/dev/null 2>&1 || true

# `.gitignore` and `.obsidian/` are the two paths pearde writes outside the
# board, and both are outside because they can be nowhere else: git reads the
# ignore file from the repo it belongs to, and Obsidian reads a vault's config
# from the vault's own root — and the vault is the PROJECT since 2026-09-02
# (@references/obsidian.md), not the board.
made=$(outside | grep -v '^README\.md$' | grep -v '^\.gitignore$' \
       | grep -vE '^\.obsidian(/|$)' || true)
if [ -n "$made" ]; then
  no "the commands wrote outside the board:"
  printf '        %s\n' $made
else
  okr "a driven board wrote nothing outside .pearde/ (bar .gitignore, .obsidian/)"
fi

# ── 4. the install is unchanged by the whole surface ─────────────────────────
grew=$(comm -13 <(printf '%s\n' "$before") <(installed) || true)
if [ -n "$grew" ]; then
  no "the commands wrote into the install:"
  printf '        %s\n' $grew
else
  okr "the driven surface left the install unchanged"
fi

# ── 5. the guard still refuses a pass writing the file by hand ──────────────
hook() {   # hook <path> -> the guard's stdout
  printf '{"tool_name":"Write","cwd":"%s","session_id":"invariant","tool_input":{"file_path":"%s","content":"x"}}' \
    "$P" "$1" | python3 "$R/guard.py" pre 2>/dev/null
}
if printf '%s' "$(hook "$P/.state/pass.md")" | grep -q '"permissionDecision": "deny"'; then
  okr "the guard refuses a pass file written outside the board"
else
  no "the guard let a pass file be written to $P/.state/pass.md"
fi
if printf '%s' "$(hook "$B/.state/pass.md")" | grep -q '"deny"'; then
  no "the guard refuses the board's own pass file — the rule is too wide"
else
  okr "the guard passes the board's own pass file"
fi

[ "$FAIL" = 0 ] || printf '\n%s check(s) failed — the invariant is broken.\n' "$FAIL"
exit $([ "$FAIL" = 0 ] && echo 0 || echo 1)
