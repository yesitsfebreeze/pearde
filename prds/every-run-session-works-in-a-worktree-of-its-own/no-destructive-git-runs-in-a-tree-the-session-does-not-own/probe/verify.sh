#!/usr/bin/env bash
# no-destructive-git-runs-in-a-tree-the-session-does-not-own — the probe.
#
# Two sessions, each holding uncommitted edits in a tree of its own, plus the
# main checkout that neither owns. Nothing here mocks git: every refusal is
# measured against a real worktree, a real ledger and a real process.
set -u
set +m            # no job-control notice on stderr when the two pids are killed
R="${PEARDE_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)}"
RES="$R/resources"
RF="$RES/board/refuse.py"
SS="$RES/board/session.py"
G="$RES/guard.py"
fails=0
ok(){ printf '  ok   %s\n' "$1"; }
no(){ printf '  FAIL %s\n' "$1"; fails=$((fails+1)); }
is(){ [ "$2" = "$3" ] && ok "$1" || no "$1 — got: $2 · want: $3"; }

T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$T" && git init -q repo && cd repo
git config user.email t@t; git config user.name t
mkdir -p pearde/prds; printf 'language: English\n' > pearde/settings.md
echo one > a.txt; git add -A; git commit -qm init >/dev/null
REPO=$PWD; BOARD=$REPO/pearde

# ── A the reader: what discards, and what only looks like it ────────────────
say(){ python3 - "$1" <<'PY'
import sys, os
sys.path.insert(0, os.environ["RESB"])
import refuse
print("yes" if refuse.destructive(sys.argv[1]) else "no")
PY
}
export RESB="$RES/board"
is "A1  reset --hard discards"        "$(say 'git reset --hard')" yes
is "A2  reset --keep does not"        "$(say 'git reset --keep HEAD')" no
is "A3  checkout -- discards"         "$(say 'git checkout -- .')" yes
is "A4  checkout <branch> does not"   "$(say 'git checkout main')" no
is "A5  clean discards"               "$(say 'git clean -fdx')" yes
is "A6  clean -n does not"            "$(say 'git clean -n')" no
is "A7  a real stash discards"        "$(say 'git stash push -u')" yes
is "A8  stash create does not"        "$(say 'git stash create')" no
is "A9  a cd carries to the git"      "$(say 'cd /somewhere && git clean -fdx')" yes
is "A10 a quoted mention does not"    "$(say "echo 'git reset --hard'")" no

# ── B two sessions, two trees ───────────────────────────────────────────────
mk(){ PEARDE_SESSION_PID=$1 python3 "$SS" take --board "$BOARD" --json \
        | python3 -c 'import json,sys;print(json.load(sys.stdin)["worktree"])'; }
# two pids that are alive for the whole probe, and are not each other
sleep 60 & P1=$!
sleep 60 & P2=$!
WT1=$(mk "$P1"); WT2=$(mk "$P2")
[ -d "$WT1" ] && [ -d "$WT2" ] && [ "$WT1" != "$WT2" ] \
  && ok "B1  two sessions took two trees" || no "B1  two sessions did not get two trees"
echo "session one" > "$WT1/uncommitted.txt"
echo "session two" > "$WT2/uncommitted.txt"

verdict(){ PEARDE_SESSION_PID=$1 python3 "$RF" tree "$2" --board "$BOARD" \
             --cwd "$3" >/dev/null 2>&1; echo $?; }
is "B2  a session may discard its own tree"   "$(verdict "$P1" "$WT1" "$WT1")" 0
is "B3  it may not discard the other's"       "$(verdict "$P1" "$WT2" "$WT1")" 3
is "B4  nor the other way round"              "$(verdict "$P2" "$WT1" "$WT2")" 3
is "B5  nor the checkout neither owns"        "$(verdict "$P1" "$REPO" "$WT1")" 3
is "B6  a shell sitting in the checkout may"  "$(verdict "$P1" "$REPO" "$REPO")" 0

# ── C a whole shell line, the way a session types it ────────────────────────
line(){ PEARDE_SESSION_PID=$1 python3 "$RF" cmd "$2" --board "$BOARD" \
          --cwd "$3" >/dev/null 2>&1; echo $?; }
is "C1  reaching into a peer's tree by -C"  "$(line "$P1" "git -C $WT2 reset --hard" "$WT1")" 3
is "C2  reaching in by cd"                  "$(line "$P1" "cd $WT2 && git clean -fdx" "$WT1")" 3
is "C3  its own tree is allowed"            "$(line "$P1" "git clean -fdx" "$WT1")" 0
is "C4  a read is allowed"                  "$(line "$P1" "git -C $WT2 status" "$WT1")" 0

# ── D the guard denies the same line a session types ────────────────────────
hook(){ printf '{"tool_name":"Bash","cwd":%s,"session_id":"probe","tool_input":{"command":%s}}' \
          "$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$1")" \
          "$(python3 -c 'import json,sys;print(json.dumps(sys.argv[1]))' "$2")" \
        | PEARDE_SESSION_PID=$3 PEARDE_GUARD_STATE="$T/gs" python3 "$G" pre 2>/dev/null; }
D1=$(hook "$WT1" "git -C $WT2 reset --hard" "$P1")
case "$D1" in *'"deny"'*) ok "D1  the guard denies a peer's tree";;
  *) no "D1  the guard let it through — $D1";; esac
D2=$(hook "$WT1" "git clean -fdx" "$P1")
case "$D2" in *'"deny"'*) no "D2  the guard denied a session its own tree — $D2";;
  *) ok "D2  the guard allows a session its own tree";; esac
D3=$(hook "$WT1" "git -C $REPO stash push -u" "$P1")
case "$D3" in *'"deny"'*) ok "D3  the guard denies a real stash in the checkout";;
  *) no "D3  the guard let a stash into the checkout — $D3";; esac
case "$D1" in *reset*'--hard'*|*'reset --hard'*) ok "D4  the denial names the command";;
  *) no "D4  the denial does not name the command";; esac
case "$D1" in *a-session-that-writes-a-shared-checkout*) ok "D5  the denial names the memo";;
  *) no "D5  the denial does not name the memo";; esac

# ── G the board that decides is the target's, not the cwd's ─────────────────
# A session types this from wherever it is standing, and a directory with no
# board above it must not be a way around the ledger one above the TARGET.
mkdir -p "$T/elsewhere"
G1=$(hook "$T/elsewhere" "git -C $WT2 reset --hard" "$P1")
case "$G1" in *'"deny"'*) ok "G1  a cwd outside every board is no way round";;
  *) no "G1  denied nothing from a boardless cwd — $G1";; esac

# ── E nothing was destroyed ─────────────────────────────────────────────────
is "E1  session one's work stands" "$(cat "$WT1/uncommitted.txt" 2>/dev/null)" "session one"
is "E2  session two's work stands" "$(cat "$WT2/uncommitted.txt" 2>/dev/null)" "session two"

# ── F a tree with no board is nobody's business ─────────────────────────────
mkdir -p "$T/bare" && git -C "$T/bare" init -q .
is "F1  no board above it: allowed" \
   "$(PEARDE_SESSION_PID=$P1 python3 "$RF" tree "$T/bare" --cwd "$T/bare" >/dev/null 2>&1; echo $?)" 0

{ kill "$P1" "$P2"; wait "$P1" "$P2"; } 2>/dev/null
echo
[ "$fails" -eq 0 ] && echo "probe: green" || echo "probe: $fails failed"
exit $(( fails > 0 ))
