#!/usr/bin/env bash
# board-rel-is-a-third-wrong-board-path-resolution — the PRD's probe. Run
# from the repo root, or from anywhere with PEARDE_ROOT set:
#
#     bash pearde/prds/board-rel-is-a-third-wrong-board-path-resolution/probe/verify.sh
#
# Exit 0 while the contract holds, 1 the moment it does not.
#
# The contract: `sort_paths` spells the board inside its own repo's paths
# ONE way, and that spelling is right on both layouts. On a board nested in
# the code repo it is `pearde`; on a board that IS its own git repo it is
# the empty string, because every path that repo prints is already under
# the board. The two readers of it — `scratch`, which swallows the board's
# machine-local dotfiles, and the rider sweep, which carries the board's
# own edits into the PRD's commit — then answer the same on both layouts.
#
# The fault this exists for: `board_rel = os.path.relpath(board, board_root)`
# answers `"."` when those two are the same directory, and `"."` is a prefix
# of no path git ever prints. `inside(path, ["."])` is False for every one of
# them, so `scratch` swallowed nothing and the rider sweep fired on nothing.
# Measured on this board on 2026-09-02: 543 dirty board paths, 0 recognised
# as under the board, every one of them reported `inherited, not added` — so
# a worker's memo, workflow or report written beside its build was committed
# nowhere, and 6 machine-local `.state/` files were listed as if a person
# had to decide about them. This is the third wrong resolution of a board
# path, after the two `foot_root` replaced.
#
# Both halves have to move together, which is why one probe holds both. Fix
# the prefix and leave `scratch`'s `path[len(board_rel) + 1:]` arithmetic
# alone and it chops the first character off every name; fix both and leave
# the `continue` unguarded and a footprint that NAMES a board dotfile —
# `pearde/.gitignore`, the case `a-board-s-own-file-commits-in-the-board-repo`
# exists for — is dropped in silence. Rows D and E are those two traps.
#
# Every repo below is built in a `mktemp -d` removed on exit, so each row is
# arithmetic about the tool and not a reading of whichever tree this machine
# happens to hold — which matters here because this repo IS the nested
# layout, and a check that read the live board would be measuring itself.
#
# It can fail, and the way to prove that is not to trust this comment:
#
#     D=$(mktemp -d)
#     python3 -c 'import sys; t=open(sys.argv[1]).read();
#       k="def board_prefix(board, board_root):"; assert k in t;
#       open(sys.argv[2],"w").write(t.replace(k, k+"\n    return __import__(\"os\").path.relpath(board, board_root)"))' \
#       resources/board/collect.py "$D/collect.py"
#     COLLECT="$D/collect.py" bash <this file>
#
# `COLLECT` points the whole run at another copy of the module: the tree is
# copied to scratch and that file swapped in, because `collect.py` imports
# its siblings from its own directory and a lone copy cannot run. Against a
# `board_prefix` that answers `"."` again, three rows go red — the arithmetic
# one and the two `own-repo` rows the prefix decides — and every
# `nested-in-code` row stays green. That asymmetry is the shape of the real
# regression. Pointed instead at the module as it stood before this PRD
# (`COLLECT=<checkout>/resources/board/collect.py`) four go red: those three,
# and `nested-in-code: the board dotfile the footprint names is added
# anyway`, which was broken on the flat layout too and is closed here.
#
# `PEARDE_PORT` is pinned to a dead port for every run: `post_report` reads
# the machine's live daemon, and an unpinned run would crash collect for a
# reason that has nothing to do with this probe.
set -u

ROOT=${PEARDE_ROOT:-$(cd "$(dirname "$0")/../../../.." && pwd -P)}
COLLECT=${COLLECT:-$ROOT/resources/board/collect.py}
FAIL=0
no() { printf 'FAIL  %s\n' "$*"; FAIL=$((FAIL + 1)); }
okr() { printf 'PASS  %s\n' "$*"; }
say() { if [ "$1" = 0 ]; then okr "$2"; else no "$2"; fi; }

if [ ! -f "$COLLECT" ]; then no "no collect.py at $COLLECT"; exit 1; fi
if [ ! -d "$ROOT/resources/board" ]; then
  no "no resources/board under $ROOT — PEARDE_ROOT is $ROOT"; exit 1
fi

T=$(mktemp -d) || exit 1
trap 'rm -rf "$T"' EXIT

export PEARDE_PORT=1        # a dead port: no run below reaches the daemon
unset PEARDE_ROOT           # the fixtures are their own roots

# ── the module under test ────────────────────────────────────────────────────
SRC="$T/src"
mkdir -p "$SRC"
cp -R "$ROOT/resources" "$SRC/resources" || exit 1
cp "$COLLECT" "$SRC/resources/board/collect.py" || exit 1
CO="$SRC/resources/board/collect.py"

# ── the arithmetic, with no fixture at all ───────────────────────────────────
# `board_prefix` and `under_board` are the whole of the resolution. Four rows
# of arithmetic pin them before any git repo is built, so a red below is read
# as "the prefix is wrong" and not as "the fixture is wrong".
UNIT=$(python3 - "$SRC/resources/board" <<'PY' 2>&1
import sys
sys.path.insert(0, sys.argv[1])
import collect as c
r = []
r.append(("own-repo prefix is the empty string, not '.'",
          c.board_prefix("/r/pearde", "/r/pearde") == ""))
r.append(("nested prefix is the directory name",
          c.board_prefix("/r/pearde", "/r") == "pearde"))
r.append(("under_board keeps the whole name under an empty prefix",
          c.under_board("memos/m1.md", "") == "memos/m1.md"))
r.append(("under_board strips the prefix and the slash under a named one",
          c.under_board("pearde/memos/m1.md", "pearde") == "memos/m1.md"))
r.append(("under_board answers None for a path outside a named prefix",
          c.under_board("resources/x.py", "pearde") is None))
r.append(("scratch sees a board dotfile through an empty prefix",
          c.scratch(".state/history.jsonl", "") is True))
r.append(("scratch leaves an ordinary board file alone",
          c.scratch("memos/m1.md", "") is False))
for name, good in r:
    print(("0 " if good else "1 ") + name)
PY
) || true
if printf '%s' "$UNIT" | grep -q '^[01] '; then
  while IFS=' ' read -r code rest; do
    [ -n "${rest:-}" ] && say "$code" "arithmetic: $rest"
  done <<< "$UNIT"
else
  no "the arithmetic rows did not run: $(printf '%s' "$UNIT" | tail -3)"
fi

# ── the fixtures ─────────────────────────────────────────────────────────────
SETTINGS='---
board: probe
language: English
max-complexity: 40
max-specs: 6
---

# settings
'

PRD='---
state: claimed
origin: requested
priority: 50
complexity: 4
blast-radius: low
claim: probe 2026-09-02 10:00
---

# p1 — a session ledger
'

# the footprint names one code file and one board dotfile. The pair is the
# whole case: the code file proves the run works, the board dotfile proves a
# claim beats `scratch`.
mkspec() { printf -- '---
complexity: 4
footprint:
  - resources/board/session.py
  - %s/.gitignore
---

# spec01 — the session tree is not dirt on the board branch

## Acceptance

- [x] `session.py` stands

## Verify

```bash
true
```
' "$1"; }

gitq() { git -C "$1" -c user.email=probe@example.com -c user.name=probe \
         "${@:2}" >/dev/null 2>&1; }

# build <dir> <board-dir-name> <own-repo yes|no>
#
#   yes — a code repo that IGNORES its board, and a board that is its own git
#         repo. This repo's own layout since 2026-09-02, and the case the
#         contract is about.
#   no  — the flat layout: the board INSIDE the code repo and not a repo of
#         its own, so the prefix is the directory name and always was. The
#         regression guard: every answer must be the same as `yes`.
build() {
  code=$1/code; board=$code/$2
  mkdir -p "$code/resources/board" "$board/prds/p1/specs" \
           "$board/memos" "$board/.state"
  gitq "$code" init -q -b main
  printf '# session\n' > "$code/resources/board/session.py"
  printf '%s' "$SETTINGS" > "$board/settings.md"
  printf '%s' "$PRD" > "$board/prds/p1/prd.md"
  mkspec "$2" > "$board/prds/p1/specs/spec01.md"
  printf 'seed\n' > "$board/.state/history.jsonl"
  printf 'before the claim\n' > "$board/memos/older.md"
  if [ "$3" = yes ]; then
    printf '/%s\n' "$2" > "$code/.gitignore"
    gitq "$code" add -A; gitq "$code" commit -qm base
    gitq "$board" init -q -b pearde
    printf '.lanes/\n.claims/\n' > "$board/.gitignore"
    gitq "$board" add -A; gitq "$board" commit -qm board
  else
    printf '%s/.lanes/\n' "$2" > "$code/.gitignore"
    gitq "$code" add -A; gitq "$code" commit -qm base
  fi
}

# probe <label> <board-dir-name> <own-repo yes|no>
probe() {
  lab=$1; D=$T/$1; mkdir -p "$D"; build "$D" "$2" "$3"
  C=$D/code; B=$C/$2
  # `memos/older.md` is dirty BEFORE the snapshot: the sweep must leave it,
  # or the fix would carry the whole board into one PRD's commit.
  printf 'edited before the claim\n' > "$B/memos/older.md"
  ( cd "$C" && python3 "$CO" --board "$B" --snapshot p1 ) >/dev/null 2>&1 \
    || { no "$lab: the snapshot did not record"; return; }
  # what the worker leaves standing, all of it AFTER the snapshot
  printf '# session\ndef take():\n    pass\n' > "$C/resources/board/session.py"
  printf '# a memo the worker wrote beside the build\n' > "$B/memos/m1.md"
  printf '.sessions/\n' >> "$B/.gitignore"
  printf 'seed\nrow\n' > "$B/.state/history.jsonl"
  OUT=$( cd "$C" && python3 "$CO" p1 --board "$B" --as engineer --trust --dry \
         2>&1 ); RC=$?

  [ "$RC" = 0 ]
  say $? "$lab: collect exits 0 (got $RC)$(if [ "$RC" != 0 ]; then \
    printf ' — %s' "$(printf '%s' "$OUT" | tail -1)"; fi)"

  # A — the board's own edit rides. This is the whole point: without it a
  # worker's memo is committed nowhere and the board grows dirt forever.
  case "$OUT" in *"rides:"*"memos/m1.md"*) r=0;; *) r=1;; esac
  say $r "$lab: the memo written after the claim rides into the commit"

  # B — the machine-local dotfile is swallowed in silence. Not committed,
  # and not reported either: nobody has to decide about it.
  case "$OUT" in *"rides:"*".state/history.jsonl"*) r=1;; *) r=0;; esac
  say $r "$lab: the board's own .state/ ledger does not ride"
  case "$OUT" in *"inherited"*".state/history.jsonl"*) r=1;; *) r=0;; esac
  say $r "$lab: the board's own .state/ ledger is not even listed"

  # C — `predates` still governs. A board file dirty before the snapshot is
  # another worker's, and the sweep leaves it inherited.
  case "$OUT" in *"rides:"*"memos/older.md"*) r=1;; *) r=0;; esac
  say $r "$lab: a board file dirty before the claim does not ride"
  case "$OUT" in *"inherited"*"memos/older.md"*) r=0;; *) r=1;; esac
  say $r "$lab: that older file is reported inherited, not silently dropped"

  # D — a footprint that names a board dotfile beats `scratch`. The trap an
  # unguarded `continue` falls into once the prefix is honest.
  case "$OUT" in *"would add:"*".gitignore"*) r=0;; *) r=1;; esac
  say $r "$lab: the board dotfile the footprint names is added anyway"

  # E — the code repo's half is untouched by any of it.
  case "$OUT" in *"would add:"*"resources/board/session.py"*) r=0;; *) r=1;; esac
  say $r "$lab: the code file still lands in the code repo"
}

probe own-repo pearde yes
probe nested-in-code .pearde no

case "$T" in /*) r=0;; *) r=1;; esac
say $r "every fixture is under one mktemp -d, removed on exit ($T)"

printf '\nprobe: %s check(s) failed\n' "$FAIL"
[ "$FAIL" = 0 ] || printf 'the contract is broken.\n'
[ "$FAIL" = 0 ]
