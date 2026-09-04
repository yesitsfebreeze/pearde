---
complexity: 4
footprint:
  - references/files.md
  - index.md
---

# spec03 — the two shared modules are named in the manifest and reachable by scope

`pearde index scope board` is how the parent PRD says these readers are found,
and neither shared module was reachable that way. `resources/common.py` was on
disk with no row in `references/files.md` at all — `python3 resources/index.py
check` reported it before this PRD touched anything — and
`resources/board-name.sh` is new. The `@@board` scope named the modules that
now import the resolver but not the file holding it.

**What already stands** (built in the analysis pass, uncommitted in the lane):
both rows added to `references/files.md`, and `@@board` extended to name
`@resources/common.py` and `@resources/board-name.sh` first, ahead of the
readers that stand on them. `index.py check` went from four problems to three.

**What is left to finish**: nothing. The three problems that remain name
`@resources/board/hotreload-test.js` (in `references/files.md` and in `@@view`)
and `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md` (in
`references/parts/commits.md`). None is this contract's: the first two are a
deleted file's leftovers, and the third is an undotted board path in prose,
which is `the-prose-and-the-invariants-say-dot-pearde`'s. Do not fix them here.

## Acceptance

- [ ] `references/files.md` holds one row anchored `@resources/common.py` and one anchored `@resources/board-name.sh`, each saying what the file is.
- [ ] `index.md`'s `@@board` row names both files.
- [ ] `python3 resources/index.py check` reports three problems, none of them naming `common.py` or `board-name.sh`.
- [ ] `python3 resources/pearde.py index scope board` prints both files.

## Verify and Proof

```sh
grep -q '^| @resources/common.py |' references/files.md
grep -q '^| @resources/board-name.sh |' references/files.md
if grep '`@@board`' index.md | grep -q 'common.py' && grep '`@@board`' index.md | grep -q 'board-name.sh'; then :; else exit 1; fi
# index.py check is a repo-wide gate red on three rows this contract does not
# own (a deleted file's leftovers and an undotted board path in prose, per the
# spec's own text) — capture, then refuse only on a row naming this footprint,
# never on the gate's exit, which -e would otherwise take.
iout=$(python3 resources/index.py check 2>&1) && irc=0 || irc=$?
[ -n "$iout" ] || exit 1
if printf '%s\n' "$iout" | grep -E 'common\.py|board-name\.sh'; then exit 1; fi
printf '%s\n' "$iout"
python3 resources/pearde.py index scope board | grep -E 'common\.py|board-name\.sh'
```
