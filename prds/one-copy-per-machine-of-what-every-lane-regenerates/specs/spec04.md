---
complexity: 3
footprint:
  - index.md
---

# spec04 — the share handle resolves in a lane

`index.md` gives `@@share` three files, and one of them is
`@pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md`. The board is a
worktree on its own branch, so a code checkout holds that path only where the
board happens to sit beside it. A lane holds no board at all.

Measured: `python3 resources/index.py check` is clean of share rows in the
checkout and reports two extra failures in this PRD's lane —
``@@share names @pearde/memos/... — not on disk`` and
``index.md references @pearde/memos/... — not on disk``. Every worker runs that
check as its repo gate, so the landed handle reddens the gate for all of them.

What already stands: the memo is right where it belongs and does not move. What
is left is that the handle must name only what a checkout holds.

## Acceptance

- [x] `@@share` names no path under the board directory.
- [x] `python3 resources/index.py check` reports no failure naming the share memo, run inside a lane worktree as well as in the checkout.
- [x] The memo file itself is not moved, renamed or copied.
- [x] No other handle in `index.md` names a board path.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 -c "
import re
bad = [l.rstrip() for l in open('index.md') if re.search(r'@\.?pearde/', l)]
assert not bad, 'handles naming a board path:\n' + '\n'.join(bad)
print('ok: no handle names a board path')
"
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed, rc=$rc"; exit 1;; esac
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '^index\.md |^@@|lanes-share-one-copy'; then
  echo "index.md still names a path a checkout does not hold"; exit 1
fi
echo "ok: index.py check names no handle failure"
```

`index.py check` reads the whole manifest, so its exit is decided by rows in
every other file on the board. It is captured and printed, and only the lines
naming `index.md` or a handle decide this block — the shape
`references/workflow.md` calls for. The rows it prints for
`references/language.md` and `references/skills/pearde-machine.md` were red
before this unit's first edit and belong to no spec here.
