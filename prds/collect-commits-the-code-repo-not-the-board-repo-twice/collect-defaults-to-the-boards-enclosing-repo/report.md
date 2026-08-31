# report — collect-defaults-to-the-boards-enclosing-repo

**DONE.** 1 spec, 4 of 4 acceptance boxes verified by independent re-run.
No box unticked. No code written: the tree already held a correct
implementation, and this round is its proof rather than its authorship.

## What I re-ran, and why the ticks stand

The analyst pre-ticked all four boxes. I re-ran each myself against what is
on disk now, and then ran a second, harder check on each: whether the test
would also pass on the *pre-fix* code. A test that passes either way proves
nothing, and that is how a pre-ticked box goes false without anyone noticing.

Spec01's `## Verify and Proof` block, run verbatim from the code repo root:

```
box1 ok
box2 ok
box3 ok
box4 ok
repo_of: all four scenarios pass
```

### The discriminating runs

I copied `resources/` to a temp dir, reverted one hunk in the copy, and
re-ran the same fixtures against the copy. Each box fails on the reverted
code, so each box is load-bearing:

| box | reverted hunk | pre-fix result | post-fix result |
|---|---|---|---|
| 1 — nested board defaults to the enclosing code repo | `if board_root == board:` branch removed | exit 1, `guard.py` still dirty, `state: claimed` | exit 0, committed in the code repo |
| 2 — unnested board unchanged | same | exit 0, clean, `state: done` | **identical** — which is the claim |
| 3 — footprint under no repo refuses loudly | `sort_paths` `raise Stop` removed | exit 0, `state: done` written over code never found | exit 1, `state: claimed`, 0 commits |
| 4 — a deletion still commits | `and not tracked` dropped from the guard | exit 1, `state: claimed` — a deletion wrongly refused | exit 0, commits |

Box 2 is the one box that is *supposed* to read the same both ways; I
confirmed it does, which is what "unchanged behaviour" means. Boxes 1, 3
and 4 each flip.

Two supporting facts I checked because box 3 is worthless without them:
`collect` does reach `state: done` on the happy path (so "state untouched"
on a refusal is a real assertion, not a no-op), and the refusal leaves zero
commits in the code repo. The refusal message names the resolved repo:

```
collect: fake-prd: footprint resources/does-not-exist.py is not under
<code repo> — repo_of matched no repo for it; nothing written
```

## Call sites of `repo_of` — the whole set

Swept every file in the repo, not just `.py`. Three callers of collect's
`repo_of`, all on the three-argument signature:

- `resources/board/collect.py:888` — in `collect_one`, `board_root` in scope
- `resources/board/collect.py:1085` — in `last_child_commit(kids, board, board_root)`
- `resources/board/brief.py:210` — `collectlib.repo_of(prd, board, board_root)`

`brief.py:320` calls brief's *own* two-argument `repo_of(prd, board)`,
which matches its own definition at line 204 — consistent, not stale.

`resources/guard.py` defines an unrelated `repo_of(args)` with three
one-argument callers of its own; `guard.py` does not import `collect`, so
it is not a call site. No stale caller remains.

I re-proved `brief.py` end to end, since the TypeError there silently
produced empty briefs: `pearde brief` on this PRD exits 0 and writes 1961
bytes, and its header reads `repo /Users/feb/dev/infra/pearde` — the code
repo, which is box 1's mechanism firing on the real board.

## Out of scope — three doctor rows and three harnesses already broken at HEAD

Not mine, not fixed, reported as the brief directs.

`bash resources/doctor.sh` shows three broken rows, none touching my
footprint: `skills` (`skills/` holds no `.md` file — the fallout of the
`agents/` → `references/` rename), `guard` (does not refuse a hand-walked
board), and `origin` (15 derived PRDs, 3 with no `from:`).

Three harnesses that exercise `collect` and `brief` fail heavily:

| harness | result |
|---|---|
| `the-board-runs-itself/brief-is-printed` | 41/104 pass |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 33 pass · 68 fail |
| `the-board-runs-itself/collect-is-a-command` | 32 pass · 101 fail |

I established these are not mine two ways. With both of my hunks reverted
in a copy of the tree, the counts are byte-identical (41/104, 33/68,
32/101). In a clean `git worktree` at HEAD, they are identical again. So
they are neither my change nor the working tree — they are already broken
in committed history.

The cause is visible in the fixtures: these harnesses build a board at
`$D/prds` with the repo at `$D`, the layout that commits 7d40481
(`init-writes-a-board-on-the-pearde-layout`) and aea6dae (the rename table)
replaced with `.pearde/prds`. The harnesses were not carried across that
rename. Worth a PRD of its own — three harnesses over `collect` and `brief`
are currently reporting nothing, and `harnesses:` is `off` on this board,
so nobody is being told.

One incidental observation: `resources/guard.py` line numbers shifted
between two greps a few minutes apart, so another session is editing it
concurrently. Nothing of mine touches it.

## Footprint

`resources/board/collect.py` and `resources/board/brief.py`, both already
in the working tree, both unchanged by this round. Nothing committed —
the orchestrator collects.
