#!/usr/bin/env bash
# a-pass-holds-its-turn-until-its-workers-are-in — the verify command of the
# memo of the same name. Run from the repo root:
#
#     bash resources/invariants/a-pass-holds-its-turn-until-its-workers-are-in.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: the hold rule — a pass holds its turn until every worker it
# dispatched has returned or is measurably dead, because a background worker
# does not outlive the pass window that dispatched it — is still written in
# the four places a pass reads it: the loop, the dispatcher, the worker
# briefs' liveness paragraph and the pass's verdict table. The 2026-09-03
# measurement this exists for: six workers dispatched in a pass's last turn,
# their transcripts stopped with no `API Error`, five empty `specs/`
# directories, 44 uncommitted paths dropped by `sweep --apply`.
#
# Each file is read with markdown emphasis stripped and whitespace collapsed
# to single spaces, so a re-wrapped paragraph or a bolded phrase still matches
# and only the words can break it. A missing file is a failure with its own
# message. `ROOT=` points the whole run at another copy of the tree, which is
# how each assertion is proved able to go red.
set -u

ROOT=${ROOT:-$(cd "$(dirname "$0")/../.." && pwd -P)}
FAIL=0

# want <file> <phrase> <what it is>
want() {
  local file="$ROOT/$1" phrase="$2" what="$3" text=""
  if [ ! -f "$file" ]; then
    printf 'LOST %s — %s (no file at %s)\n' "$1" "$what" "$file"
    FAIL=$((FAIL + 1))
    return
  fi
  text=$(tr '\n' ' ' <"$file" | sed -e 's/[*`]//g' -e 's/  */ /g')
  if printf '%s' "$text" | grep -qF -- "$phrase"; then
    printf 'HELD  %s — %s\n' "$1" "$what"
  else
    printf 'LOST %s — %s\n' "$1" "$what"
    FAIL=$((FAIL + 1))
  fi
}

want references/parts/loop.md \
  'A pass holds its turn until every worker it dispatched has returned or is measurably dead' \
  'the hold rule, stated in the loop'

want references/parts/loop.md \
  'does not move the ceiling: a pass at context-budget still hands back MORE, once its workers are in' \
  'the hold rule composed with the ceiling, not against it'

want references/parts/dispatch.md \
  "A pass worker's return ends its children" \
  'the hold rule from the dispatcher side — the window that ends, ends them'

want references/parts/dispatch.md \
  'A pass holds its turn until every worker it dispatched has returned or is measurably dead' \
  'the hold rule, stated in the dispatcher'

want references/parts/workers.md \
  'it does not license returning over a live one' \
  'the liveness check does not license returning over a live worker'

want references/parts/workers.md \
  'the pass holds its turn until every worker it dispatched has returned or is measurably dead' \
  'the hold rule, pointed at from the liveness paragraph'

want references/agents/pearde-pass.md \
  'hold the turn | a worker you dispatched is in flight' \
  'the verdict table names holding as the response to workers in flight'

if [ "$FAIL" -gt 0 ]; then
  printf '%d assertion(s) lost\n' "$FAIL"
  exit 1
fi
printf 'all 7 assertions hold\n'
exit 0