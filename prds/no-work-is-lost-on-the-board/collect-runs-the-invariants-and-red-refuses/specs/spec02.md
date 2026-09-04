---
complexity: 5
footprint:
  - references/parts/commits.md
  - references/parts/states.md
  - references/parts/memos.md
  - index.md
  - .pearde/memos/invariants-are-testable-memos-and-the-kind-index-is-generated.md
---

# spec02 — the prose says collect runs the invariants, and one memo stops saying nothing does

spec01 puts a step into `collect` that four documents describe without it, and
falsifies one sentence a memo wrote down on purpose. This spec closes both.
Prose only — no behaviour changes here, and nothing in `resources/` is touched.

**What already stands**: all five edits, made by the implementer pass of
2026-09-03 — four in the lane, the memo in the board. The reads that found
them are kept below because they are the argument for each edit, not a
worklist.

**The five edits**, one each:

1. `references/parts/commits.md` — the paragraph beginning "`collect` is the
   command" lists that command's behaviour in order: reads the finished
   condition, runs every spec's `## Verify and Proof` block and the board's
   `gate:`, commits, writes `commit:` and `actual:`, clears `claim:`, sets
   `done`. The invariants belong in that sequence, between the gate and the
   commit, said in the page's own voice: a non-zero exit refuses the collect
   whole and the PRD stays where it was.
2. `references/parts/states.md` — the `done` row's gate cell reads "every box
   closed in both files, every `## Verify and Proof` block and the board's
   `gate:` green". Every binding invariant green is now part of that gate and
   the cell has to say so.
3. `references/parts/memos.md` — the `kind: invariant` bullet says the rule is
   "re-run by `verify` whenever a change might bend it", which was true while
   `verify` was the only runner. `collect` is now the second, and it runs them
   on every landing without being asked. The bullet says both.
4. `index.md` — the `@@memos` row ("recording a decision and checking it")
   names `@resources/memos.py` as the last anchor. `@resources/board/collect.py`
   now reads that format too and belongs in the row, so a session looking up
   how an invariant is checked finds the automatic reader as well as the
   manual one.
5. `.pearde/memos/invariants-are-testable-memos-and-the-kind-index-is-generated.md`
   — its last `## Consequences` bullet reads "What this does not fix: nothing
   runs `memo verify` automatically. Wiring it into doctor or a hook is the
   next memo's problem, named here." That is the sentence spec01 makes false.
   Replace the bullet with what now runs them and where — `collect`, step 2b,
   before the record is written — naming this PRD. The memo's decision is not
   superseded and its `status:` does not change: making the memo registry the
   thing collect reads is that decision holding, not being replaced.

`references/parts/handles.md` was read and needs nothing: its `collect` bullet
is about a PRD's own open boxes, not about the board's rules.

## Acceptance

- [x] `references/parts/commits.md` names the invariant step inside the
      `collect` sequence, and says a red one refuses the collect whole
- [x] The `done` row in `references/parts/states.md` names every binding
      invariant green as part of the gate
- [x] The `kind: invariant` bullet in `references/parts/memos.md` names
      `collect` as a runner alongside `verify`
- [x] The `@@memos` row in `index.md` lists `@resources/board/collect.py`
- [x] The memo no longer claims that nothing runs `memo verify` automatically,
      and names `collect` in its place; its `status:` is still `decided` and
      no `superseded_by` was added
- [x] `python3 resources/index.py check` prints no line naming any of the five
      files this spec edits — the four lines it already prints about
      `resources/common.py`, `hotreload-test.js` and
      `references/parts/commits.md`'s `@pearde/memos/…` anchor are older than
      this PRD and are not this spec's to fix
- [x] `python3 resources/memos.py check .pearde` is silent

## Verify and Proof

Every negative below is written `if <found>; then exit 1; fi`, never
`! <found>`: a leading `!` exempts the line from `set -e`, so under the
`bash -e -o pipefail` this block is run with, both its cases leave the block
at exit 0 — the check could not fail. See the record,
`A leading ! exempts a command from set -e`.

```sh
MEMO=.pearde/memos/invariants-are-testable-memos-and-the-kind-index-is-generated.md
# each grep is scoped to the paragraph, row or bullet the box names: a bare
# `grep -q invariant references/parts/commits.md` already passes on line 218
# and could not fail. All five were measured at 0 before the edits.
# each consumer drops `-q` on purpose: a `grep -q` downstream of a producer
# exits on its first match and SIGPIPEs the producer, and under `pipefail`
# that 141 decides the block — seen nondeterministically at 1 on a green
# tree. A plain `grep` reads to EOF and the pipeline's exit is the match.
grep -A8 'is the command' references/parts/commits.md | grep 'invariant'
grep '| `done`' references/parts/states.md | grep 'invariant'
grep -A2 'is the testable memo' references/parts/memos.md | grep 'collect'
grep '@@memos' index.md | grep 'board/collect.py'
if grep -q 'nothing runs `memo verify` automatically' "$MEMO"; then exit 1; fi
grep -q 'collect' "$MEMO"
# the memo's own key carries the closed set as a trailing comment —
# `status: decided    # open | decided | superseded` — so the anchor cannot
# end at `decided$`; it ends at the word.
grep -qE '^status: decided([[:space:]]|$)' "$MEMO"
if grep -q '^superseded_by:' "$MEMO"; then exit 1; fi
IDX=$(mktemp)
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
# a crashed producer prints nothing this grep can find, and would read as a
# pass; refuse it by name before the miss is counted as one.
if printf '%s\n' "$out" | grep -q '^Traceback'; then
  printf '%s\n' "$out"; rm -f "$IDX"; exit 1
fi
# the four lines this gate printed before this PRD are not this spec's to
# fix, and one of them names `references/parts/commits.md` — its
# `@pearde/memos/…` anchor, the pre-rename spelling left by `c88a64a`. That
# one line is dropped; no other line naming a file this spec edits may stand.
printf '%s\n' "$out" | grep -v '@pearde/memos/' > "$IDX" || true
if grep -Eq 'parts/(commits|states|memos)\.md|^index\.md' "$IDX"; then
  cat "$IDX"; rm -f "$IDX"; exit 1
fi
rm -f "$IDX"
python3 resources/memos.py check .pearde
```
