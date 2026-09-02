---
complexity: 6
footprint:
  - references/parts/consult.md
  - references/parts/health.md
  - references/parts/grammar.md
  - references/parts/memos.md
---

# spec03 — the four small parts rewritten dense

`consult.md`, `health.md`, `grammar.md` and `memos.md` are rewritten in the
writer's prose: 1,807 → 1,771 words together. All four were red on
`prose.py check` (four, four, one and two unbound waste words) and are green.
No committed harness greps any of them, so these four are bounded by the
checker and the fact audit alone.

**What stands:** all four rewrites are applied in the lane and every check
below is green. **What is left:** re-run the boxes and tick them.

## Acceptance

- [x] `python3 resources/prose.py check` exits 0 on all four files
- [x] `python3 resources/index.py check` reports three lines — the same three
      pre-existing problems as at `HEAD`, none of them naming
      `references/parts/` — so every `@` link in the four still resolves.
      `wc -l` pads its count on macOS, so the count is taken with `grep -c ''`
- [x] Every backticked token, every `@` link, every table row (7, 5, 6, 0) and
      every heading (5, 5, 4, 1) present at `HEAD` are still present
- [x] `git diff --stat` over the four shows no file renamed and none deleted

## Verify and Proof

```sh
set -e
python3 resources/prose.py check references/parts/consult.md references/parts/health.md references/parts/grammar.md references/parts/memos.md
test "$(python3 resources/index.py check 2>&1 | grep -c '')" = 3
! python3 resources/index.py check 2>&1 | grep -q 'references/parts/'
test -z "$(git diff --diff-filter=RD --name-only -- references/parts/)"
git diff --stat -- references/parts/consult.md references/parts/health.md references/parts/grammar.md references/parts/memos.md
echo "spec03 ok"
```
