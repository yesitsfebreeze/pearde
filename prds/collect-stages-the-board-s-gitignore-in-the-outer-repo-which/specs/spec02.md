---
complexity: 7
footprint:
  - resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
  - references/files.md
  - pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
---

# spec02 — the routing gets a committed guard

spec01's proof is this PRD's probe, and a probe is one worker's. The rule it
holds — a footprint path under a board that is its own git repo is committed in
that repo, never staged in the code repo that ignores it — is the kind that
regresses silently: the flat layout stays green, and only the nested one, which
is the layout this repo itself runs, goes red. This unit turns the probe into a
committed harness plus the memo it is the `verify:` of.

The script builds its own repos in a `mktemp -d` removed on exit — a code repo
that ignores its board, a board that is its own repo, a lane, and a spec whose
footprint names one file in each — so what it asserts is arithmetic about the
tool rather than a reading of whichever trees this machine holds. It takes
`COLLECT=<path>` to point the run at another copy of the module, and points its
own `PEARDE_PORT` at a dead port so no run reaches the machine's daemon. The
memo carries `kind: invariant`, `verify:` naming the script, and the fault it
was written for.

This spec is also its own first customer: `pearde/memos/…` is a path under the
board, so committing it is the case spec01 fixed. It is written where the board
is, not in the lane — a lane is cut without the board and has no `pearde/` to
write into, so the memo goes to the real board directory (the lane sits at
`<board>/.lanes/<slug>`, so the board is two levels up) and `collect` picks it
up there. The script and the manifest row are ordinary code-repo files and are
written in the lane as usual.

**What already stands**: the mechanism and both fixtures, as
`probe/fixture.py` in this PRD's folder — `build`, `build_flat`, `work`,
`check` and `mutant` are the script's whole content, in Python. **What is
left**: port it to a bash invariant under `resources/invariants/` in the shape
of `a-master-need-is-the-union-of-its-members.sh` (a `no()` counter, one `PASS`
or `FAIL` line per assertion, exit 1 on any), write the memo, and give the
script its row in `references/files.md` beside the three that are there.

## Acceptance

- [x] `bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh`
      exits 0 on this tree and prints one `PASS` line per assertion
- [x] the same script with `COLLECT=` pointed at a copy of `collect.py` whose
      `foot_root` routes nothing exits 1 — the guard is watched failing
- [x] the script reaches no daemon and leaves nothing behind: after a run,
      `git status --porcelain` in this repo and in the board repo is
      unchanged, and its temp dir is gone
- [x] `pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md` has
      `kind: invariant` and a `verify:` naming that script, and
      `python3 resources/memos.py check` exits 0
- [x] `references/files.md` holds a row for the new script, and
      `python3 resources/index.py check` reports no new line against the
      count before this PRD

## Verify and Proof

```sh
S=resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
M=pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
bash "$S"
D=$(mktemp -d)
python3 -c 'import sys; t=open(sys.argv[1]).read(); k="def foot_root(p, board, board_root, repo):"; assert k in t; open(sys.argv[2],"w").write(t.replace(k, k+"\n    return repo, p"))' resources/board/collect.py "$D/collect.py"
if COLLECT="$D/collect.py" bash "$S"; then rm -rf "$D"; exit 1; fi
rm -rf "$D"
grep -q "a-board-s-own-file-commits-in-the-board-repo.sh" references/files.md
grep -q "^verify: bash $S" "$M"
grep -q "^kind: invariant" "$M"
grep -q "PEARDE_PORT" "$S"
python3 resources/memos.py check
```
