---
complexity: 6
footprint:
  - references/parts/commits.md
  - pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
---

# spec03 — the prose and the memo say the rule the code now follows

Both documents tell a spec author there is exactly one way to spell a footprint
under the board — `pearde/<file>`, code-repo-relative — and that a path
"resolving inside a board" is the board's. After spec01 the first is no longer
a restriction and the second is no longer true: the board's own spelling
resolves as well, and a code checkout nested under the board stays its own
repo. A reader who follows the current prose writes a footprint that works and
a reader who follows the current memo reasons about routing by a rule the code
no longer uses.

**What already stands.** Nothing in either file. The rule they must carry is
settled and green in spec01.

**What is left.** One paragraph in each, and this PRD added to the memo's
`prds:` list. The memo's key set is closed and `resources/memos.py check` fails
on a stray one.

## Acceptance

- [x] `references/parts/commits.md` says membership is decided by the git checkout that holds the path, not by the board's path as a prefix
- [x] it says both spellings resolve — the code repo's (`pearde/<file>`) and the board's own (`prds/<prd>/probe/verify.sh`) — and that the code repo's stays the one to prefer for a file the code repo could hold
- [x] it says a code checkout nested under the board — a lane, a run-session worktree — is its own repo and its footprints are never the board's
- [x] the memo's `## Decision` carries the same three sentences, and its `## Consequences` no longer claims `pearde/<file>` is "the one way there is"
- [x] the memo's `prds:` names `collect-resolves-a-board-path-two-ways-and-both-are-wrong`
- [x] `python3 resources/memos.py check` reports no new failure
- [x] `python3 resources/index.py check` reports no new failure

## Verify and Proof

```sh
# `memos.py check` and `index.py check` read the whole board and the whole
# tree. Their output stays visible and their exit decides nothing: this unit
# owns two files and may only go red on a line naming one of them. The
# checkout carries one inherited index failure — `references/language.md`
# references a persona that is not on disk — and a bare call would fail this
# block for a defect it does not own.
out=$(python3 resources/memos.py check 2>&1) && rc=0 || rc=$?
printf 'memos.py check rc=%s\n%s\n' "$rc" "$out"
[ "$rc" -le 1 ] || exit 1
if printf '%s\n' "$out" | grep -q 'a-board-s-own-file-commits-in-the-board-repo'; then exit 1; fi
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf 'index.py check rc=%s\n%s\n' "$rc" "$out"
[ "$rc" -le 1 ] || exit 1
if printf '%s\n' "$out" | grep -q 'references/parts/commits\.md'; then exit 1; fi
grep -c 'show-toplevel\|the checkout that holds' references/parts/commits.md
grep -c 'A code checkout nested \*\*under\*\* the board is a repo of its own' references/parts/commits.md
grep -c 'prds/<prd>/probe/verify.sh' references/parts/commits.md
grep -c 'collect-resolves-a-board-path-two-ways-and-both-are-wrong' .pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
grep -c 'a repo of its own, and its footprints are never the' .pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
if grep -q 'the one way there is' .pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md; then exit 1; fi
echo "the claim is gone"
```
