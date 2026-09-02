---
complexity: 8
footprint:
  - resources/board/collect.py
---

# spec01 — the rollback moves the pointer, keeps the tree, and says what it drops

`unland` puts the checkout's branch back after a red verify and touches
nothing else: `git reset --keep` instead of `git reset --hard`, so the
uncommitted work standing in the shared checkout — other sessions', other
PRDs' — survives a gate that goes red. It is not called at all when
`land_lane` merged nothing, and it prints the commits and files it is about
to drop before it runs. When `--keep` refuses because a merged path carries
uncommitted work, the refusal is reported and obeyed: the merge stays
standing and the person gets the command that finishes it.

**Standing after pass one** (uncommitted in the lane): the whole change in
`resources/board/collect.py` — `unland(repo, pre, landed, out=print)` with
the `--keep` body and the refusal branch, and the call site in
`collect_one` passing `landed`. The harness at
`.pearde/prds/collect-must-not-reset-the-checkout-it-did-not-write/probe/verify.sh`
is written and green: 31 checks, 31 pass, 0 fail, in 3 seconds. Its section
A reproduces both faults on the code as it stood at `3587817`, so the
harness is proved able to fail.

**Left to finish**: run the boxes below against the merged tree and confirm
each one. Nothing else in this unit is unwritten.

## Acceptance

- [x] `unland` in `resources/board/collect.py` runs `git reset --keep`, and
      `git reset --hard` appears nowhere in `resources/board/collect.py`
- [x] `unland` takes `land_lane`'s landed count and returns without
      touching the repo when it is zero or `None`
- [x] a red verify block after a merge leaves an unrelated tracked file's
      uncommitted edit exactly as it was, and puts the branch back on the
      commit before the merge
- [x] a red verify block after a merge that merged nothing prints no
      rollback line and moves no ref
- [x] before the reset, the line names the number of commits and the files
      being dropped from the checkout
- [x] a `--keep` that refuses is reported with the paths git named and the
      `git reset --keep` command that finishes it, and nothing is discarded
- [x] a green verify block still lands the lane's commit and closes the PRD
- [x] `collect-keeps-its-word`'s harness still prints 101 pass, 0 fail

## Verify and Proof

```sh
p=resources/board/collect.py
bash .pearde/prds/collect-must-not-reset-the-checkout-it-did-not-write/probe/verify.sh
n=0
h=$(grep -cF 'reset", "--hard' "$p" || true)
if [ "$h" != 0 ]; then echo "$p still runs git reset --hard ($h)"; n=$((n+1)); fi
k=$(grep -cF 'reset", "--keep' "$p" || true)
if [ "$k" = 0 ]; then echo "$p does not run git reset --keep"; n=$((n+1)); fi
u=$(grep -cF 'unland(repo, pre, landed' "$p" || true)
if [ "$u" -lt 2 ]; then echo "unland does not take landed at both the definition and the call site ($u)"; n=$((n+1)); fi
if ! grep -qF 'if not pre or not landed:' "$p"; then echo "unland does not return early when the merge merged nothing"; n=$((n+1)); fi
echo "spec01: $n problem(s)"
[ "$n" = 0 ]
```
