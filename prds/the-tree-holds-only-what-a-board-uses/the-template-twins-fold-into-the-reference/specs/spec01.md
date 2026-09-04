---
complexity: 8
footprint:
  - references/templates/prd.doc.md
  - references/templates/spec.doc.md
  - references/templates/memo.doc.md
  - references/templates/atomic.doc.md
  - references/templates/workflow.doc.md
  - references/templates/report.doc.md
  - references/templates/vision.doc.md
  - references/files.md
  - index.md
  - references/drill.md
  - references/memo.md
  - references/parts/contract.md
  - references/workflow.md
  - resources/memos.py
---

# spec01 — the seven `.doc.md` twins are gone, their load-bearing sentences folded in

Already built on this pass (uncommitted, in the lane). The seven
`references/templates/*.doc.md` files are read by no code and no skill; a
`probe/unique.py` line-overlap scan against every other `references/**.md`
file, then a manual read of each twin against its target, found the twins
almost entirely restate the manifest, the contract table and the workers'
brief text word for word. The handful of sentences that were not on record
anywhere else are folded into the reference each format already belongs to:

- **prd.doc.md** — "an empty `## Failure` reads as a failed attempt" and
  "one contract per PRD" fold into `references/drill.md`.
- **spec.doc.md** — "a spec with no `## Acceptance` box is refused" (an
  existing `pearde specced` check, reproduced at `resources/board/specs.py:603,608`,
  that no reference page named) folds into `references/parts/contract.md`.
- **memo.doc.md** — the concrete "slower is no reason" example and "what it
  deliberately does NOT fix: the next memo's problem, named" fold into
  `references/memo.md`'s body table.
- **atomic.doc.md** — the two concrete examples ("`python3 resources/index.py
  check`, not 'verify the index'"; "'the check is silent', not 'the index is
  tidy'") fold into `references/workflow.md`'s Atomic body table.
- **workflow.doc.md** — "named the way a request arrives", "the section is
  the lookup, so the boundary earns its bullet", and "`→ 1` on every row is a
  list, not a workflow" fold into `references/workflow.md`'s Workflow
  section.
- **report.doc.md**, **vision.doc.md** — nothing unique survived the scan;
  `references/report.md`, `references/parts/order.md`,
  `references/parts/board.md` and `resources/board/init.py`'s own docstring
  already carry everything they said. Nothing added.

`references/files.md`'s `references/templates/` table drops the seven
`.doc.md` rows and its intro line's `.doc.md` mention; `index.md`'s
`@@templates` row drops the seven `.doc.md` anchors and its `.doc.md`
description. `resources/memos.py`'s one remaining `@references/templates/memo.doc.md`
citation (a docstring anchor `pearde index check` tracks) is repointed at
`@references/memo.md`.

## Acceptance

- [x] `ls references/templates/*.doc.md` prints nothing (no matches)
- [x] `python3 resources/index.py check` names no `.doc.md` anchor and no
      `@@templates` `.doc.md` entry (pre-existing unrelated failures from a
      concurrent uncommitted pass — `resources/common.py`,
      `resources/board/hotreload-test.js` — are not this spec's to clear;
      see the report)
- [x] `python3 resources/grammar.py check` is silent
- [x] `python3 resources/workflows.py check` is silent
- [x] `git grep -n 'doc\.md'` under `references/` and `resources/` finds no
      anchor citation of a removed file (the one remaining hit,
      `resources/knowledge.py`'s `index_stem` docstring, is a naming-convention
      example, not a citation of a file on disk)

## Verify and Proof

```sh
# 1 — no `.doc.md` twin survives
n=$({ ls references/templates/*.doc.md 2>/dev/null || true; } | wc -l | tr -d " ")
echo "doc.md twins on disk: $n"
[ "$n" = 0 ]

# 2 — the reference gate names no `.doc.md` anchor and no `@@templates` entry.
#     Captured, not gated: `index.py check` is board-wide and is red on two
#     inherited rows (`resources/common.py`, `resources/board/hotreload-test.js`)
#     from a concurrent uncommitted pass. Only a `doc.md` row is this spec's.
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf "%s\n" "$out"
[ "$rc" -lt 2 ]
if printf "%s\n" "$out" | grep -q "doc\.md"; then exit 1; fi

# 3 — the grammar and workflow libraries stay silent
g=$(python3 resources/grammar.py check 2>&1 || true);   printf "%s\n" "$g"; [ -z "$g" ]
w=$(python3 resources/workflows.py check 2>&1 || true); printf "%s\n" "$w"; [ -z "$w" ]

# 4 — the one surviving `doc.md` hit is knowledge.py's naming example,
#     not a citation of a file on disk
hits=$({ git grep -n "doc\.md" -- references resources || true; })
printf "%s\n" "$hits"
[ "$(printf "%s\n" "$hits" | grep -c . || true)" = 1 ]
printf "%s\n" "$hits" | grep -q "^resources/knowledge.py:"

# 5 — every sentence the fold moved is on record in its target
grep -q "One contract per PRD" references/drill.md
grep -q "reads as a failed" references/drill.md
grep -q "refuses a spec with no box" references/parts/contract.md
grep -q "slower" references/memo.md
grep -q "deliberately does NOT fix" references/memo.md
grep -q "not \"verify the index\"" references/workflow.md
grep -q "not \"the index is tidy\"" references/workflow.md
grep -q "named the way a request arrives" references/workflow.md
grep -q "this section is the lookup" references/workflow.md
grep -q "is a list, not a workflow" references/workflow.md
echo "folds: all on record"
```
