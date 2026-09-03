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
- `collect.py`'s import block now matches the house pair every other module in
  `resources/board/` uses — `resources/` inserted first, its own directory
  second — so `resources/board` still wins a name held by both.
- `probe/verify.sh` — nine fixtures, each a `mktemp -d` git repo and board of
  its own, removed on exit.

**What is left**: run the harness, close the boxes, and let the orchestrator
land it. No code is known to be missing.

## Acceptance

- [ ] `probe/verify.sh` prints `OK` and exits 0 — 18 of 18, run from the repo
      root with no `PEARDE_ROOT` set, so it measures the tree that is landing
- [ ] A planted invariant memo exiting 1 makes `collect` exit 1, leave the
      PRD `claimed` with its `claim:` still on the file, write no `actual:`,
      and make no commit
- [ ] The refusal output carries three things: the failing slug, the `verify:`
      command that ran, and the script's own stdout
- [ ] `--fail` does not file the PRD `failed` on a red invariant, and
      `--trust` does not skip the invariants
- [ ] Removing the planted memo makes the same `collect` exit 0 and reach
      `done`
- [ ] A board with no invariant memo runs nothing and prints nothing about
      invariants; a `superseded` invariant does not bind
- [ ] An invariant memo with no `verify:` command refuses the collect rather
      than being skipped
- [ ] `python3 resources/memos.py verify` still prints one line per invariant
      in the shape it printed before — `<slug>: holds` /
      `<slug>: BROKEN (exit N) — <tail>` / `<slug>: BROKEN — no verify:
      command`
- [ ] All six of this board's own invariants are green, so this change does
      not refuse its own collect

## Verify and Proof

```sh
python3 -m py_compile resources/board/collect.py resources/memos.py
bash .pearde/prds/no-work-is-lost-on-the-board/collect-runs-the-invariants-and-red-refuses/probe/verify.sh
python3 resources/memos.py verify .pearde
python3 resources/memos.py check .pearde
```
