---
complexity: 7
footprint:
  - references/parts/workflows.md
  - references/parts/personas.md
---

# spec02 — workflows.md and personas.md rewritten dense

The two mid-sized parts are rewritten in the writer's prose: workflows 1,230 →
1,224 words, personas 1,201 → 1,173. Both were red on `prose.py check` (four
and seven unbound waste words) and are green. `personas.md` carries one
sentence a committed harness greps verbatim, which fixes its wording.

**What stands:** both rewrites are applied in the lane and every check below is
green. **What is left:** re-run the boxes and tick them.

## Acceptance

- [x] `python3 resources/prose.py check` exits 0 on both files
- [x] `personas.md` still holds the literal `` `--as <id>` on the line `` —
      `the-board-runs-itself/the-next-line-runs` greps for it, and the density
      rule's obvious rewrite (dropping the `it is` before it) breaks the grep
- [x] `the-board-runs-itself/the-next-line-runs` scores `94 pass · 2 fail`, its
      `HEAD` baseline
- [x] Inline code spans stay on one line: `` `export PEARDE_AS=<id>` ``,
      `` `· as <id>` `` and `` `▸ … · as <id>` `` each appear unbroken
- [x] Every backticked token, every `@` link, every table row (22 and 19) and
      every heading (5 and 7) present at `HEAD` are still present

## Verify and Proof

```sh
set -e
L="$PWD"
python3 resources/prose.py check references/parts/workflows.md references/parts/personas.md
grep -qF '`--as <id>` on the line' references/parts/personas.md
grep -qF '`export PEARDE_AS=<id>`' references/parts/personas.md
grep -qF '`· as <id>`' references/parts/personas.md
grep -qF '`▸ … · as <id>`' references/parts/personas.md
PEARDE_ROOT=$L bash /Users/feb/dev/infra/pearde/.pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh > /tmp/h3.txt 2>&1 || true
grep -qF '94 pass · 2 fail' /tmp/h3.txt && tail -1 /tmp/h3.txt
echo "spec02 ok"
```
