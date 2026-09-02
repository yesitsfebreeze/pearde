---
complexity: 10
footprint:
  - references/parts/workers.md
---

# spec01 — workers.md rewritten dense, its five brief blocks still rendering

`references/parts/workers.md` is rewritten in the writer's prose: 3,351 → 3,331
words, `prose.py check` green where it was red on six unbound waste words. The
file is machine-read — `resources/board/brief.py` renders its five
`<!-- brief:X -->` blocks verbatim into every worker's brief — so the unit is
bounded by three committed harnesses that grep it for exact strings, not by
prose taste alone.

**What stands:** the rewrite is applied in the lane and every check below is
green. **What is left:** re-run the boxes and tick them.

## Acceptance

- [x] `python3 resources/prose.py check references/parts/workers.md` exits 0
- [x] `brief.check()` returns no problems — five blocks, every placeholder in
      the table used, `Verdict:` and `40` named in `brief:every`
- [x] The analyst and implementer briefs both still render, and the rendered
      text differs from the same render at `HEAD` only by rewrapping and the
      two intentionally reworded sentences — no operative instruction dropped
- [x] `the-brief-names-the-verdict-line-collect-requires` scores `13 ok · 2 FAIL`,
      its `HEAD` baseline — the harness plants a duplicate of the exact line
      `> fits the build ahead, as you would one the PRD already carries. Then read`,
      so that line must survive verbatim
- [x] `workflows-on-the-board/workflow-improve` scores `70/71`, its `HEAD`
      baseline — it greps for the one-line string
      `is the belief and the ## Workflow rows, as above.`
- [x] Every backticked token, every `@` link, all 20 table rows and the one
      heading present at `HEAD` are still present

## Verify and Proof

```sh
set -e
L="$PWD"
python3 resources/prose.py check references/parts/workers.md
python3 -c "import sys;sys.path.insert(0,'resources/board');import brief;b=brief.check();print('briefs problems:',len(b));sys.exit(1 if b else 0)"
grep -qF '> fits the build ahead, as you would one the PRD already carries. Then read' references/parts/workers.md
grep -qF 'is the belief and the `## Workflow` rows, as above.' references/parts/workers.md
B=/Users/feb/dev/infra/pearde/.pearde/prds
PEARDE_ROOT=$L bash $B/the-brief-names-the-verdict-line-collect-requires/probe/verify.sh > /tmp/h1.txt 2>&1 || true
grep -qF '13 ok · 2 FAIL' /tmp/h1.txt && tail -1 /tmp/h1.txt
PEARDE_ROOT=$L bash $B/workflows-on-the-board/workflow-improve/probe/verify.sh > /tmp/h2.txt 2>&1 || true
grep -qF '70/71 checks pass' /tmp/h2.txt && tail -1 /tmp/h2.txt
echo "spec01 ok"
```
