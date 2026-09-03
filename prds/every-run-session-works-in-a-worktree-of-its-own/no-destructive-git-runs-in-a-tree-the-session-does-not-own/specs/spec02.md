---
complexity: 6
footprint:
  - references/parts/guard.md
  - references/parts/handles.md
  - references/files.md
  - index.md
---

# spec02 — the manual says what the guard now refuses, and stops saying what it no longer is

The guard grew a refusal that discards nothing and stops something being
discarded, and `references/parts/guard.md` does not know. One sentence in it
is now false. The manual is what a session reads before it is surprised, so
this is not tidying.

**What stands.** `references/files.md` carries a row for
`resources/board/refuse.py`, and `index.md` carries the `@@own` keyword
pointing at `session.py`, `refuse.py`, `guard.py`, `lanes.py` and
`collect.py`; `pearde index check` names no problem for either. The
pre-existing `index` failure — `references/language.md` referencing
`@references/personas/writer.md`, which is not on disk — is untouched and is
not this spec's to fix.

**What is left.**

- `references/parts/guard.md` `## What it refuses` has no row for the new
  denial. It needs one, in the table's own two-column voice: the call, and
  what the guard says back.
- The same file ends `## What it refuses` with **"The `Bash` hook is a
  reader's check — it stamps and refuses repeated board reads — so a `>` or a
  `tee` into a skill file through a link passes unrefused."** The first clause
  is now wrong: the Bash hook refuses a writer too. The paragraph's real point
  — that a `>` into a skill file is not caught — survives and must be kept;
  only the claim that the hook reads and nothing else has to go.
- `references/parts/handles.md` has a row for `session take/list/reap/owns`
  and none for `refuse`. `pearde refuse` is a handle and belongs in the table
  beside it, in the same voice.

## Acceptance

- [x] `references/parts/guard.md` `## What it refuses` carries a row for a
      destructive git aimed at a tree the running session does not own, naming
      the four commands and the memo
- [x] the sentence calling the `Bash` hook "a reader's check" is gone from
      `references/parts/guard.md`, and the point it was making — that a `>` or
      a `tee` into a skill file through a link still passes — is still there
- [x] `references/parts/handles.md` carries a row for `refuse`, giving both
      verbs and the `pearde refuse <verb>` spelling in its right-hand column
- [x] `references/files.md` carries one row for `resources/board/refuse.py`
- [x] `index.md` carries a keyword whose files include `refuse.py`
- [x] `pearde index check` names no problem this spec introduced

## Verify and Proof

```sh
cd "$PEARDE_ROOT"
# `grep -q X && echo` cannot fail a block: `-e` skips every command of an
# AND-OR list but the last, so a missed needle printed nothing and the block
# carried on at exit 0. Measured against the checkout, which does not hold
# this build: four of the seven lines below were inert. Each is now written
# so the miss is the last command of its list.
fail() { echo "FAIL: $*"; exit 1; }
grep -q 'pearde refuse <verb>' references/parts/handles.md \
  || fail "handles.md carries no row for the refuse handle"
echo "handles has the row"
grep -qi 'does not own' references/parts/guard.md \
  || fail "guard.md's What it refuses carries no row for the destructive git"
echo "guard.md has the row"
if grep -q "reader's check" references/parts/guard.md; then
  fail "the false claim is still there"
fi
echo "the false claim is gone"
grep -q 'tee' references/parts/guard.md \
  || fail "the surviving point — a > or a tee into a skill file — went too"
echo "the surviving point is still there"
grep -q 'resources/board/refuse.py' references/files.md \
  || fail "files.md carries no row for refuse.py"
echo "files.md has the row"
grep -q 'refuse.py' index.md || fail "index.md names no keyword holding refuse.py"
echo "index.md has the keyword"
# the board's index check carries one pre-existing problem this spec does not
# own — references/language.md pointing at a persona file that is not on disk.
# What this box measures is that no problem NAMES anything of this PRD's.
# Captured, never piped: `index.py check` exits 1 on that pre-existing
# problem, and under pipefail that exit became the pipeline's — so a grep
# that DID match still read as "nothing matched" and the box passed on its
# own failure. The capture is what makes the check able to fail.
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
[ -n "$out" ] || [ "$rc" = 0 ] || fail "index.py check died printing nothing"
if printf '%s\n' "$out" | grep -qi 'refuse\|@@own'; then
  fail "the index check names this PRD's files"
fi
echo "the index check names nothing of this PRD's (index.py check exit $rc)"
```
