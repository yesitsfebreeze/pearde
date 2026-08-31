---
complexity: 6
footprint:
  - references/files.md
  - index.md
  - .pearde/memos/the-board-keeps-two-journals.md
---

# spec01 — register `references/archive.md`, and close the journals finding

Both halves of this PRD are built already, in the tree, uncommitted. This
spec is the record of what stands and the check that it holds.

**Registration.** `references/archive.md` now has a row in
`references/files.md` (under the `references/` — read table, alongside
`files.md`/`language.md`) and is listed in `index.md`'s `@@board` Keywords
row (the scope its subject fits — the PRD flattening shape and `scan`'s
existing prune, alongside `board.md`, `plan.py`, `states.md`, `init.py`).
`resources/index.py check` was run and is silent.

**Journals finding.** The output at
`/private/tmp/claude-501/-Users-feb-dev-infra-pearde/072e209a-b9bc-484c-92dc-2acab1b93ce6/tasks/w41yjawt8.output`
was read. It named two things: a real naming defect in `collect.py`
(`HISTORY_FILE`/`history_row()` aliased onto what is actually the
transitions writer) and `specs.py`'s docstring naming the wrong file — both
already fixed in the current tree (`TRANSITION_FILE`/`transition_row()` in
`resources/board/collect.py`; the corrected docstring in
`resources/board/specs.py`) — and a design question, whether both journals
are needed, which the finding itself answers yes to (different shape,
writer, reader, purpose). No code defect remains to fix. The outcome is the
memo at `.pearde/memos/the-board-keeps-two-journals.md`, recording what each
journal is for and why both exist. `resources/memos.py check` was run and is
silent.

## Acceptance

- [x] `python3 resources/index.py check` from the CODE repo root
      (`/Users/feb/dev/infra/pearde`) exits 0 with no output
- [x] `references/archive.md` has a row in `references/files.md` and appears
      in an `index.md` Keywords row
- [x] `.pearde/memos/the-board-keeps-two-journals.md` exists, `kind:
      decision`, `status: decided`, and `python3 resources/memos.py check`
      exits 0 with no output
- [x] `resources/board/collect.py` defines `TRANSITION_FILE`/
      `transition_row()` and no longer aliases a transitions writer under a
      `HISTORY_*`/`history_row` name; `resources/board/specs.py`'s docstring
      names `.transitions.jsonl`, not `.history.jsonl`, for what
      `transitions.py` records

## Verify and Proof

Every assertion is chained — the closing `echo` runs only when all of them
hold, so the block's exit code is 0 exactly when the four boxes are true.

```sh
cd /Users/feb/dev/infra/pearde
python3 resources/index.py check &&
python3 resources/memos.py check &&
grep -q '^| @references/archive.md |' references/files.md &&
grep -q '@references/archive.md' index.md &&
grep -q '^kind: decision$' .pearde/memos/the-board-keeps-two-journals.md &&
grep -q '^status: decided$' .pearde/memos/the-board-keeps-two-journals.md &&
grep -q 'TRANSITION_FILE' resources/board/collect.py &&
grep -q 'def transition_row' resources/board/collect.py &&
! grep -q 'HISTORY_FILE\|def history_row' resources/board/collect.py &&
grep -q 'transitions\.jsonl' resources/board/specs.py &&
! grep -q 'history\.jsonl' resources/board/specs.py &&
echo "spec01 verified: archive.md registered, memo decided, journals named right"
```
