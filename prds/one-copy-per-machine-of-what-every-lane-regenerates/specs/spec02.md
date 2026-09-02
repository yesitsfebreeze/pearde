---
complexity: 8
footprint:
  - resources/board/shared.py
---

# spec02 — a tree that cannot be shared says so before apply is run

`apply` refuses a link `git status` would show, puts the tree back, and prints
the reason. `status` cannot see any of that: it reports the path as
`store-only`, and `print_status` counts only `linked`, `local`, `tracked` and
`foreign`, so a tree where sharing is impossible is bucketed under nothing.

Measured on this repo: 27 of 30 trees are lane worktrees whose branch still
carries `resources/board/node_modules/` with the trailing slash, so every one of
them is refused on apply — and `pearde share` prints
`232 shared · 0 not yet · 0 refused (git tracks them) · 0 someone else's link`.
The number that matters is the 27 the line does not hold. Reproduced in a
worktree made at run time by
`pearde/prds/one-copy-per-machine-of-what-every-lane-regenerates/probe/probe_share.py`,
probe 2: state `store-only` before, `refused` from apply, `store-only` after.

What already stands: `invisible()` and `ignore_hint()` are the whole judgement
and are correct. What is left is asking them from `state()` instead of only from
`link_one`, so status answers the same question apply does.

`state()` must reach its answer without writing a link — the ignore pattern is
readable from `git check-ignore -v`, whose output names the pattern that matched,
and a matched pattern ending in `/` cannot ignore a symlink. A tree already
`linked` is never re-judged.

## Acceptance

- [x] `state()` returns `refused` for a path whose only matching ignore pattern ends in a slash, in place of `store-only` or `local`.
- [x] The refusal carries `ignore_hint()`'s line into `status`, so a person reads the fix without running `apply`.
- [x] `print_status`'s summary accounts for every row: the counts sum to the number of rows surveyed.
- [x] `share --json` carries the same state, so a caller sees the refusal too.
- [x] A tree already `linked` is still reported `linked` and is not re-judged.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 pearde/prds/one-copy-per-machine-of-what-every-lane-regenerates/probe/probe_share.py
python3 resources/pearde.py share --json | python3 -c "
import json, sys, collections
rows = json.load(sys.stdin)['rows']
c = collections.Counter(r['state'] for r in rows)
assert c['refused'], f'no tree reports refused, states seen: {dict(c)}'
print('ok:', c['refused'], 'refused of', len(rows), 'rows')
"
python3 resources/pearde.py share | tail -3
```
