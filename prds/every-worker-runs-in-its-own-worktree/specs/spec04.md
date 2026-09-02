---
complexity: 13
footprint:
  - resources/board/collect.py
  - references/parts/commits.md
---

# spec04 — collect merges the lane, then measures the merged tree

The worker's code is committed on `lane/<slug>` in a worktree the checkout
cannot see. `collect` merges it in, runs the verify blocks and the gate on
the merged tree, commits once, and puts the checkout back when a check goes
red.

**What stands** — `land_lane` and `unland` are in
`resources/board/collect.py` from the probe, called from `collect_one`
between step 1 and step 2. `land_lane` commits the lane's footprint paths,
names what the worker left outside the footprint, merges, and returns the
checkout's pre-merge commit; `unland` resets to it. A conflict raises
`Stop` with the file on it and the lane branch untouched. Measured in a
fixture: before the merge step existed, `collect` failed `spec01 exit 1`
because the work was in the lane and the verify ran on the checkout; with
it, the same collect printed `lane lane/change-a merged — 1 commit(s)` and
went green.

**What is left** — the commit count. The measured run wrote **three**
commits for one PRD: the lane's, `collect`'s step-4 commit, and the record
commit. `@references/parts/commits.md` says one commit per PRD on the
transition that lands it, and that is not this PRD's to change. The lane's
commit is the PRD's commit: step 4 must stop committing the code repo a
second time when a lane landed, and commit only the board record and its
`<prd> — record` follow-up. The message step 4 builds — the contract line,
the spec goals, `widen:`, `prd:` — is the message `land_lane` must put on
the lane's commit, so it is built once and used by whichever commits.

Also left:

- Step 3's hunk-splitting. `CONTENDING` and the two-authors refusal exist
  because one tree held every PRD's dirt. A lane is cut clean off HEAD, so
  everything dirty in it is one worker's and nothing needs splitting. Keep
  the machinery for the **board** repo — every PRD still writes one
  `.pearde/` — and stop running it against the code repo when that repo's
  work arrived through a lane. Say which in the docstring; do not delete a
  path a laneless board still takes.
- `--dry` must say what it would merge — the branch and the commit count —
  and merge nothing.
- The gate is measured against the claim's baseline, and the baseline is
  snapshotted in the checkout. With a lane the checkout is not where the
  worker wrote, so `snapshot` must record the lane's root for the code side
  once the lane exists, or the `known — every line is in the claim's
  baseline` softening reads the wrong tree.
- `references/parts/commits.md` states the scope rules as `collect`'s step
  3 spec. It must say where the commit is made now, that the lane's commit
  is the PRD's, and that a merge conflict is a red collect naming the file.

## Acceptance

- [x] `pearde collect <prd>` on a PRD whose work stands only in its lane runs the verify blocks green
- [x] the checkout's branch gains exactly two commits for a collected PRD — the work and `<prd> — record`
- [x] a verify block that fails leaves the checkout at the commit it was on before the collect and the lane branch holding the worker's commits
- [x] a lane that conflicts with the checkout exits non-zero, names every conflicting file, and stages nothing
- [x] `pearde collect --dry` names the lane branch it would merge and merges nothing
- [x] a PRD with no lane collects exactly as it did before lanes existed
- [x] `references/parts/commits.md` says the lane's commit is the PRD's commit and that a merge conflict is a red collect

## Verify and Proof

```sh
python3 -c "import ast,sys; t=ast.parse(open('resources/board/collect.py').read()); \
n={f.name for f in ast.walk(t) if isinstance(f, ast.FunctionDef)}; \
sys.exit(0 if {'land_lane','unland'} <= n else 1)"
grep -q 'lane' references/parts/commits.md
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)(resources/board/collect\.py|references/parts/commits\.md)([ ,:]|$)'; then exit 1; fi
```
