---
complexity: 3
footprint:
  - resources/board/example/
---

# spec01 — the example board fixtures read dense

Sixteen of the seventeen tracked `.md` files under `resources/board/example/`
rewritten against `## Density` in @references/language.md. `memos/README.md`
is machine output and belongs to spec03. Every frontmatter key, acceptance
box, table row, claim string and date survives character-identical — the file
`plan.py scan` reads is a contract, not prose.

Every box below is measured on the **merged tree**, never on the lane and
never on main. The merged tree is `git merge-tree --write-tree main
<lane>` with the lane's uncommitted files laid over it, because `collect`
commits those onto the lane before it merges. A gate run on either side alone
is the defect this retry exists for.

## What already stands

- Thirteen files rewritten on the lane at `760ed8e`, rebased onto `fc75bcf`;
  `big/first/prd.md`, `big/second/prd.md` and `finished/specs/spec01.md` were
  already dense and are untouched.
- The lane merges into `8bbb4c1` clean: `git merge-tree --write-tree` exits 0
  and returns `f77f2d6`. The conflict the retry was opened on was against
  `d240590`, a base the lane has since left.
- Every box below re-run on that merged tree by
  `probe/verify_merged.sh`: green.

## What is left

- Land the lane and re-run `probe/verify_merged.sh` on whatever main is then.
  Nothing else in this spec has work in it.

## Acceptance

- [x] on the merged tree, `python3 resources/prose.py check` over every tracked `.md` under `resources/board/example/` and `resources/board/knowledge/` names no file under `resources/board/example/`, and `prose.py` itself exits 0 or 1 rather than crashing
- [x] `python3 resources/board/plan.py scan` over a fresh `plan.py example` copy of the merged tree prints 8 PRDs, the counts `boxes 3/5` and `boxes 3/3`, and the bands in the order collect, waiting on you, in flight, ready, gated
- [x] `python3 resources/memos.py check`, `python3 resources/workflows.py check` and `python3 resources/questions.py check` are silent on that copy
- [x] `git diff --name-status main <merged-tree> -- resources/board/example/` names thirteen or more files and every line is `M` — no add, no rename, no delete
- [x] the box text of every box in `prds/building/specs/spec01.md` and `prds/finished/specs/spec01.md` is unchanged; only line numbers move
- [x] `prds/asking/prd.md` still carries three answers with exactly one marked recommended

## Verify and Proof

```sh
bash .pearde/prds/every-document-is-written-in-the-writer-s-prose/\
example-and-knowledge-fixtures-are-rewritten-dense/probe/verify_merged.sh
```

The probe prints one `PASS`/`FAIL` line per box and `boxes N/26` at the end.
`REF=main bash …` is its negative control: on main alone six of the twenty-six
go red, so the set can still fail.
