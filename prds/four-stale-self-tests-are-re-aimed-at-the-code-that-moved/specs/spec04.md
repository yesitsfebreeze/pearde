---
complexity: 2
footprint:
  - .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
---

# spec04 — the rewritten prose keeps its check, on the sentence that carries it

`workflow-improve` line 331 asserts a needle from a table row in
`references/parts/workers.md`. `78357ed` replaced that whole "On return" table
with prose when `pearde collect --report` took the verdict lookup off the
orchestrator, and no three-way row is left. `references/parts/workers.md` is not
this PRD's to edit — the check moves to the prose.

The row's claim was specific and it survived the rewrite: *whichever verdict a
report carries, its `## Workflow` rows are still the orchestrator's to act on.*
That is now the closing sentence of both the analyst's and the implementer's
return sections — "…is the belief and the `## Workflow` rows, as above." — so
the check reads that sentence.

**Already standing (this analyst's uncommitted pass one):** the check is
retitled "workers.md keeps the ## Workflow rows with the orchestrator", uses the
same fixed-string `doc` helper on `references/parts/workers.md`, and carries a
comment naming the commit and what it replaced. Its two neighbours — the
on-return rule and the pointer to loop step 6 — were green before and after and
are untouched.

**Left to finish:** re-run the harness. Note that another session is editing
`references/parts/workers.md` right now; if the sentence has moved again by the
time this runs, re-aim to whatever sentence carries the same claim, do not edit
that file.

## Acceptance

- [ ] The harness reports 71/71 checks pass and exits 0
- [ ] `references/parts/workers.md` is byte-identical to what the implementer found — `git diff --name-only` does not name it as this PRD's change
- [ ] The check fails when the sentence it reads is absent — shown against a scratch copy of the file, never against the real one
- [ ] No check in this harness still names the deleted table row: `grep -c 'any of the three, plus' ` over the harness is 0

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh; echo "exit=$?"
grep -c 'any of the three, plus' .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
git diff --name-only -- references/parts/workers.md
# non-vacuity, on scratch text only
grep -vF 'is the belief and the `## Workflow` rows, as above.' references/parts/workers.md \
  | grep -qF 'is the belief and the `## Workflow` rows, as above.' \
  && echo "VACUOUS" || echo "check fails when the sentence goes"
```
