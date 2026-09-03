# collect-runs-the-invariants-and-red-refuses — analyst pass

Verdict: SPECCED

The build went through. `collect` now runs every binding invariant before it
writes a byte of the record, and a red one refuses the collect whole and
leaves the PRD exactly where it was. The probe is green at 18 of 18 and all
six of this board's own invariants hold, so the change does not refuse its own
landing. Two specs, `complexity` 15, footprint below.

Workflow followed: `probe-then-spec`. It fits without amendment — an `open`
PRD, its contract, a build, then specs written from what the build stands up.

## What the build stands up

Uncommitted in the lane, on
`lane/no-work-is-lost-on-the-board-collect-runs-the-invariants-and-red-refuses`:

- `resources/memos.py` — `binding()` and `run_invariants()` split out of
  `verify()`. `binding` is the one answer to "which rules bind now";
  `run_invariants` is the runner both readers share, returning
  `(slug, cmd, exit, output)`. `verify()` became its printer and prints what
  it printed before. An invariant memo with no `verify:` command is exit 1
  there, not a skip.
- `resources/board/collect.py` — step 2b in `collect_one()`, after the lane
  lands and after the gate, before `sort_paths`. No baseline, `--fail` does
  not apply, `--trust` does not skip it; the module docstring's seven-step
  list carries the row.
- `.pearde/prds/…/probe/verify.sh` — nine `mktemp -d` fixtures, each its own
  git repo and board.

Two things this pass changed on top of pass one, both inside the footprint:

1. **The refusal line names the script, not just the slug.** `## Done means`
   asks for the script, and a slug spells its script only where the memo
   author named the two alike —
   `the-board-directory-is-pearde-and-the-compat-symlink-is-gone` verifies
   with an inline `test` and names no file at all. The line now carries the
   `verify:` command verbatim, and the probe asserts on it.
2. **The import block matches the house pair.** Pass one appended
   `sys.path.insert(0, <resources>)` *after* the sibling imports, leaving
   `resources/` ahead of `resources/board/` on the path — the reverse of the
   order every other module in `resources/board/` uses. Nothing collides
   today, but a future `resources/plan.py` or `resources/specs.py` would be
   imported in place of the sibling. Rewritten to the two-line house pair.

## What is left

`specs/spec01.md` — the mechanism. Everything in it stands; the implementer
runs the harness, closes the boxes and hands it back. `specs/spec02.md` — the
prose, nothing done: four documents describe `collect` without this step and
one memo says in as many words that nothing runs the invariants automatically.

Union of the footprints:

```
resources/board/collect.py
resources/memos.py
references/parts/commits.md
references/parts/states.md
references/parts/memos.md
index.md
.pearde/memos/invariants-are-testable-memos-and-the-kind-index-is-generated.md
```

`complexity: 15` — the mechanism is ~55 lines across two files and one gate
step in a module that already had two; the harness is the bulk of the work and
it is written. spec01 10, spec02 5.

`blast-radius: high` — `collect` is the single chokepoint every PRD on every
board on this machine passes through, and every board runs this file live
through a symlink. A wrong exit here either refuses every landing or lands on
a broken rule. The change is additive on a board with no invariant memo, which
is every board but this one, but the code path is not.

## Findings

### One invariant script is run by nothing

`resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh`
opens by calling itself "the verify command of the memo
`lanes-share-one-copy-of-what-they-regenerate`". That memo is `kind: decision`
with no `verify:` key, so `memos verify` does not run it and — after this PRD
— neither will `collect`. Six of the seven scripts under
`resources/invariants/` reach collect; that one does not. `index.md:80`
already indexes it under `@@share` as an invariant.

The script exits 0 today (four claims, 50 trees, 372 links). The fix is two
frontmatter lines. It is not in this PRD's specs because it is another PRD's
file and because making it bind is a real behaviour change on every collect
this board runs from then on — the orchestrator's call, not mine.

The general shape is worth a check: nothing on the board fails when a script
under `resources/invariants/` has no binding memo, so the gap is silent. That
would be a `memos check` row on this repo's own layout.

### `run_invariants` measures the board's parent, the gate measures `repo:`

`run_invariants` runs each command in `os.path.dirname(board)`, matching the
`verify` contract already written down. `collect`'s spec blocks run in
`repo_of(prd, board, board_root)`. On this board the two are the same
directory and the build never hit the difference, but on a board whose `repo:`
points elsewhere the invariants would measure a different tree from the gate
that just passed. Left alone deliberately: changing it would rewrite
`memo verify`'s documented cwd, which is outside this contract.

### The `!` form of an unfailable verify line is not yet in `write-the-specs`

spec02's first draft used `! grep -q …`, which cannot fail a block under
`bash -e -o pipefail`. The record already holds this
(`A leading ! exempts a command from set -e`, 260902-69f0) and says the
`write-the-specs` atomic names the `<test> && <action>` shape but not the `!`
one. Caught and rewritten to `if <found>; then exit 1; fi` before the spec was
filed. The atomic is the orchestrator's to edit; this is the second run to
meet the trap.

A related trap in the same class, found while measuring spec02's greps: a bare
`grep -q 'invariant' references/parts/commits.md` already passes on line 218,
so the box could never fail. Every grep in spec02 is scoped to the paragraph,
row or bullet its box names, and all five were measured at 0 before the edits.

### Pre-existing red, none of it this PRD's

`python3 resources/index.py check` prints four lines on `main` at `f8968fe`,
unchanged by this pass:

```
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
references/parts/commits.md references @pearde/memos/… — not on disk
```

The first is fallout from `7e4d610`, the next two from `b1d3f5d`, the last is
the pre-rename spelling of `.pearde/` left by `c88a64a`. `doctor` is also red
on `health` (four dropped files, ranking 29 commits behind), `knowledge`
(`graph.json` behind two notes) and `questions` (one `## Answers` with no
`## Questions` above it, in
`resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule`).
All predate this PRD.

### Housekeeping

- `python3 resources/knowledge.py query` on the contract returned 90 hits, 81
  strong, over 90 notes — no gap, nothing enqueued to `.pearde/wiki/pending/`.
- No word in the contract was missing from `grammar.py`.
- Nothing was learned outside this repo, so nothing was written back.
- A gitignored `.pearde` symlink to the live board was made at the lane root,
  the way `probe-then-spec` step 1 prescribes, so board-rooted commands
  resolve there. It does not travel with the branch.
- Running the probe during a lane pass needs `PEARDE_ROOT=$PWD`: a probe under
  `.pearde/prds/` resolves its root five levels up, which is the orchestrator's
  checkout, not the lane. After landing the two are the same tree and the
  default is right, which is why the spec's verify block sets nothing.

## Scores

complexity: 15
blast-radius: high
workflow: probe-then-spec
