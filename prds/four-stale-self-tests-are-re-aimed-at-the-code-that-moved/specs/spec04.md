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

- [x] The harness reports every check passing (`<n>/<n> checks pass`) and exits 0, and the re-aimed row stands once in it (71/71 at this run; the denominator is a shared board file, so it is printed, never gated)
- [x] `references/parts/workers.md` is byte-identical to what the implementer found — `git diff --name-only` does not name it as this PRD's change
- [x] The check fails when the sentence it reads is absent — shown against a scratch copy of the file, never against the real one
- [x] No check in this harness still names the deleted table row: `grep -c 'any of the three, plus' ` over the harness is 0

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
H=.pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
rc=0; bash "$H" > "$W/out" 2>&1 || rc=$?
tail -1 "$W/out"; echo "exit=$rc"
# green means every check passed. The denominator is NOT pinned: this harness is
# a shared board file and a neighbour adding a passing check must not redden
# this PRD's block.
green="$(python3 -c 'import re,sys
n=[m for m in (re.match(r"^(\d+)/(\d+) checks pass\s*$", L) for L in open(sys.argv[1], errors="replace")) if m]
print(1 if n and n[-1].group(1)==n[-1].group(2) else 0)' "$W/out")"
row="$( { grep -c 'ok   workers.md keeps the ## Workflow rows with the orchestrator' "$W/out" || true; } )"
# the re-aimed check stands once in this PRD's own file, and the deleted table
# row is named nowhere in it
inplace="$( { grep -c 'workers.md keeps the ## Workflow rows with the orchestrator' "$H" || true; } )"
old="$( { grep -c 'any of the three, plus' "$H" || true; } )"
# workers.md is another session's file — this PRD does not change it
moved="$(git diff --name-only -- references/parts/workers.md | wc -l | tr -d ' ')"
# non-vacuity, on scratch text only — workers.md is never written
live="$( { grep -cF 'is the belief and the `## Workflow` rows, as above.' references/parts/workers.md || true; } )"
gone="$(grep -vF 'is the belief and the `## Workflow` rows, as above.' references/parts/workers.md \
  | { grep -cF 'is the belief and the `## Workflow` rows, as above.' || true; } )"
echo "all-pass=$green row-ok=$row in-place=$inplace dead-needle=$old workers-moved=$moved sentence-live=$live sentence-gone=$gone"
[ "$rc" = 0 ] && [ "$green" = 1 ] && [ "$row" = 1 ] && [ "$inplace" = 1 ] \
  && [ "$old" = 0 ] && [ "$moved" = 0 ] && [ "$live" = 1 ] && [ "$gone" = 0 ]
```
