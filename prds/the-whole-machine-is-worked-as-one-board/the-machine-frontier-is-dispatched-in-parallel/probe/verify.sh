#!/usr/bin/env bash
# the machine frontier, dispatched. Two halves: the fixture cases (races, and a
# race cannot be proved against the real board), and the guarantees that hold
# against this repo — the order is printed before anything moves, --dry moves
# nothing, and the sibling's read-only mode is exactly as it was.
set -u
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
SIB="$BOARD/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh"
fail=0
t() { if eval "$2" >/dev/null 2>&1; then echo "ok   $1"; else echo "FAIL $1"; fail=1; fi; }

# ── the fixture cases ────────────────────────────────────────────────────────
while read -r line; do
  case "$line" in
    PASS*) echo "ok   fixture ${line#PASS }" ;;
    FAIL*) echo "FAIL fixture ${line#FAIL }"; fail=1 ;;
  esac
done < <(python3 "$HERE/fixture.py" 2>&1)

# ── against this repo ────────────────────────────────────────────────────────
# The command, not a copy of it: the probe's dispatcher moved to
# resources/board/dispatch.py with spec01, and `run` is the verb that moves —
# `machine dispatch` stopped existing with the-machine-is-the-run-verb.
#
# "--dry moved nothing" is measured on the BOARDS, never on a repo-root `git
# status`: `.pearde/` is git-ignored, so a repo-root status cannot see a board
# write at all and can only ever report a neighbouring session's edit to
# `resources/` — which is what it did, twice, while this ran.
# @.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md.
# The race-free half of this row is the `dry` fixture case above, which owns
# two boards and compares every file on them byte for byte.
LOGS_BEFORE="$(ls "$BOARD/.state"/run-*.log 2>/dev/null | wc -l | tr -d ' ')"
DRY="$(cd / && python3 "$ROOT/resources/board/run.py" run all --dry 2>&1)"
LOGS_AFTER="$(ls "$BOARD/.state"/run-*.log 2>/dev/null | wc -l | tr -d ' ')"

t "the verb is run's, not a second command"        'grep -q "argv\[0\] == \"run\"" "$ROOT/resources/board/run.py"'
t "--dry runs from / with no board above the cwd"  '[ -n "$DRY" ]'
t "the order is printed before anything moves"     'awk "/^wave 1: /{w=NR} /^would |^skip /{if(!f){f=NR}} END{exit !(w && f && w < f)}" <<<"$DRY"'
t "--dry names every row it would launch"          'grep -qE "^would @[a-z0-9-]+/" <<<"$DRY"'
t "--dry opened no run log on this board"          '[ "$LOGS_BEFORE" = "$LOGS_AFTER" ]'
t "a claim refusal is named with its reason"       'grep -qE "^skip @[a-z0-9-]+/.* · [a-z]+:" <<<"$DRY"'
t "the merged progress line is printed"            'grep -qE "^▸ machine: [0-9]+ boards · " <<<"$DRY"'
t "the closing tally accounts for every row"       'grep -qE "^dispatched [0-9]+ · refused [0-9]+ · dead [0-9]+$" <<<"$DRY"'

# The refusal is the one the shipped read path does NOT hold: the read marks
# the container `ready` and puts it in a wave, and `claim` refuses it. The row
# below fails the moment the dispatcher stops re-asking the gate.
#
# The read is `plan.py plan all`, and the word `plan` is load-bearing. This
# line used to be `run.py all`, which was not a read: it DISPATCHED the whole
# watch set, three nested command substitutions deep, every time this harness
# ran — including under `doctor.sh --harnesses`. It is the fan-out of
# 2026-09-03, and `--dry opened no run log on this board` above was true of the
# line above it and false of the file.
# @.pearde/memos/no-harness-under-the-board-dispatches-it.md.
t "a row the frontier marks ready but claim refuses is skipped" '
  A="$(grep -oE "@[^ ]+" <<<"$(grep " ready  " <<<"$(cd / && python3 "$ROOT/resources/board/plan.py" plan all 2>&1)")" | sort -u)"
  B="$(grep -oE "^skip @[^ ]+" <<<"$DRY" | sed "s/^skip //" | sort -u)"
  [ -z "$B" ] || comm -12 <(echo "$A") <(echo "$B") | grep -q .'

# ── the read path is untouched ───────────────────────────────────────────────
if [ -x "$SIB" ] || [ -f "$SIB" ]; then
  SIBOUT="$(bash "$SIB" 2>&1)"
  n_ok="$(grep -c "^ok   " <<<"$SIBOUT")"
  # the count is written down, not >=, so a check DELETED over there is a red
  # row here rather than a silent shrink. 18 read-path rows + 15 group rows.
  t "the sibling read-only harness is still 33/33" '[ "'"$n_ok"'" = "33" ] && grep -q "^PASS$" <<<"'"$SIBOUT"'"'
else
  echo "FAIL sibling harness not found at $SIB"; fail=1
fi

[ $fail -eq 0 ] && echo "PASS" || echo "FAIL"
exit $fail
