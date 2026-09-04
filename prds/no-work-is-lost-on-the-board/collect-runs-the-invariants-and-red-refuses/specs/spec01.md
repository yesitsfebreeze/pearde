---
complexity: 10
footprint:
  - resources/board/collect.py
  - resources/memos.py
---

# spec01 — collect runs the board's invariants, and a red one refuses it

`collect` gains step **2b**: after the lane lands and after the gate, before a
single byte of the record is written, every binding invariant memo's `verify:`
command runs against the merged tree. Any non-zero exit refuses the collect
whole — the slug, the command and the script's own output are printed, the
lane is put back, and the PRD stays exactly where it was.

The registry is `kind: invariant` memos, not a directory listing. That is not
this spec's call to make: the memo
`invariants-are-testable-memos-and-the-kind-index-is-generated` already
rejected a directory as the record and made the memo it, and every
`resources/invariants/*.sh` on this board reaches collect as the `verify:` of
its own memo.

**What already stands** — the whole mechanism is built and uncommitted in the
lane, and the harness below is green at 18 of 18:

- `resources/memos.py` — `binding(board, only=None)` and
  `run_invariants(board, only=None)` split out of `verify()`. `binding` is the
  one answer to "which rules bind now" (`kind: invariant`, status not
  `superseded`); `run_invariants` is the runner both readers share, returning
  `(slug, cmd, exit, output)` with stdout and stderr in one stream in the order
  a reader saw them, cwd the board's parent. `verify()` is now its printer and
  prints exactly what it printed before.
- An invariant memo carrying no `verify:` command is exit 1 in the runner, not
  a skip: a rule that cannot be checked is indistinguishable from one that is
  broken.
- `resources/board/collect.py` — step 2b in `collect_one()`, between the
  verify blocks and `sort_paths`, plus its row in the module docstring's
  seven-step list. Three things it deliberately does not do, each the gate's
  behaviour and each wrong here: no baseline (a rule already broken when the
  PRD was claimed is still broken now), no `--fail` (a red invariant says the
  BOARD is broken, and filing this PRD `failed` blames the wrong thing and
  loses the claim), and `--trust` does not skip it (nobody has run the board's
  invariants, and they measure a merged tree that exists only now).
- The refusal line carries the `verify:` command verbatim, not the slug alone:
  the PRD's `## Done means` asks the output to name the *script*, and a slug
  spells its script only where the memo author named the two alike —
  `the-board-directory-is-pearde-and-the-compat-symlink-is-gone` verifies with
  an inline `test` and names no file at all.
- `collect.py` imports `memos` by name and nothing else. The build carried a
  two-line `sys.path` pair to reach `resources/` from `resources/board/`;
  `every-module-finds-its-siblings-by-one-rule` landed `@resources/pearde_path.py`
  at `e55a0e7` while this PRD was claimed, and that module already puts
  `resources/` on the path ahead of every directory under it. The pair went
  and `import memos as memolib` sits with the other sibling imports — the one
  rule, not a second copy of it.
- `probe/verify.sh` — nine fixtures, each a `mktemp -d` git repo and board of
  its own, removed on exit.

**What is left**: run the harness, close the boxes, and let the orchestrator
land it. No code is known to be missing.

## Acceptance

- [x] `probe/verify.sh` prints `OK` and exits 0 — 18 of 18, run from the repo
      root with no `PEARDE_ROOT` set, so it measures the tree that is landing
- [x] A planted invariant memo exiting 1 makes `collect` exit 1, leave the
      PRD `claimed` with its `claim:` still on the file, write no `actual:`,
      and make no commit
- [x] The refusal output carries three things: the failing slug, the `verify:`
      command that ran, and the script's own stdout
- [x] `--fail` does not file the PRD `failed` on a red invariant, and
      `--trust` does not skip the invariants
- [x] Removing the planted memo makes the same `collect` exit 0 and reach
      `done`
- [x] A board with no invariant memo runs nothing and prints nothing about
      invariants; a `superseded` invariant does not bind
- [x] An invariant memo with no `verify:` command refuses the collect rather
      than being skipped
- [x] `python3 resources/memos.py verify` still prints one line per invariant
      in the shape it printed before — `<slug>: holds` /
      `<slug>: BROKEN (exit N) — <tail>` / `<slug>: BROKEN — no verify:
      command`
- [x] The six invariants this board held when the PRD was claimed are all
      green. A seventh, `a-pass-holds-its-turn-until-its-workers-are-in`,
      was written to the board by a live sibling mid-run and its `verify:`
      names a script still in that sibling's lane: exit 127, not this unit's,
      and it refuses every collect on this board — this PRD's own included —
      until that lane lands

## Verify and Proof

```sh
python3 -m py_compile resources/board/collect.py resources/memos.py
B="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde"; bash "$B/prds/no-work-is-lost-on-the-board/collect-runs-the-invariants-and-red-refuses/probe/verify.sh"
# `memos.py verify` is a board-wide gate: its exit is decided by every
# invariant memo on the board and not one of them is in this spec's
# footprint. A sibling whose memo lands before its script reddens it, and a
# bare call would hand this unit's colour to that sibling. So the output is
# captured and kept visible, and the block gates on what this unit owns: the
# printer's three shapes, and the six invariants that bound when this PRD was
# claimed still holding. `collect` step 2b refuses the landing on the red one
# on its own account — that is this PRD's whole point, and not this block's
# job to repeat.
out=$(python3 resources/memos.py verify .pearde 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
[ -n "$out" ]
BAD=$(printf '%s\n' "$out" | grep -vcE ': (holds|BROKEN \(exit [0-9]+\)( — .*)?|BROKEN — no `verify:` command)$') || true
[ "$BAD" = 0 ]
for s in the-board-directory-is-pearde-and-the-compat-symlink-is-gone \
         no-destructive-git-runs-in-a-tree-the-session-does-not-own \
         no-colour-group-in-the-vault-preset-is-a-path-query \
         a-master-need-is-the-union-of-its-members \
         a-board-s-own-file-commits-in-the-board-repo \
         every-artifact-lands-inside-the-board; do
  printf '%s\n' "$out" | grep -qxF "$s: holds"
done
python3 resources/memos.py check .pearde
```
