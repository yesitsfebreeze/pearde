---
complexity: 16
footprint:
  - resources/board/collect.py
---

# spec01 — the verify block runs fenced, not free, in the checkout it shares

`collect_one`'s verify loop ran every spec's `## Verify and Proof` block, and
the board's `gate`, as arbitrary `bash -e -o pipefail` directly in `repo` /
`board_root` — the checkout other sessions and other PRDs share — with
nothing between the script and the tree until `unland`, which only exists
for a RED check. A block that exits 0 having run `git reset --hard`,
`git clean -fdx` or `rm -rf` takes whatever else was dirty there with it and
`collect` still writes `done`: the exact shape of the incident this PRD is
filed from (see `the-machine-is-the-run-verb`'s report), one step earlier
than the reset `collect-must-not-reset-the-checkout-it-did-not-write`
already fixed. Reproduced at the CLI in section A of the harness below.

`guarded_run` fences each block. Everything dirty in `cwd` that this PRD does
not own is stashed away by pathspec before the block runs — absent from the
working tree for it to reach, not merely reported on afterward — and restored
after. Anything the block changed or created outside what the PRD owns is
reverted: a tracked path back to HEAD's blob, index and tree, so a foreign
`git add` is undone too; a new untracked foreign path removed. The branch is
put back with the same compare-and-swap `commit_private` already uses if the
block moved it, so a real concurrent commit is refused rather than clobbered.

`owned_by` says what the PRD owns, and says it the way `sort_paths` already
does for what `collect` is about to commit — one answer to "whose is this?",
not two that can disagree. A footprint path is spelled relative to `repo`,
never to `board_root`: `sort_paths` resolves every one as
`os.path.join(repo, p)`, and `references/settings.md`'s own board says
footprints are written relative to the repo root. The two roots are the same
only where the board is not its own git repo; on a board that IS one —
this repo since the board moved to `pearde/`, and every nested `.pearde` with
a `.git` — `repo_of` returns the enclosing checkout and they differ. The
board's own root additionally owns the PRD's directory, exactly as
`sort_paths` seeds `groups` with it, so a gate that writes its proof under
`prds/<prd>/` writes where this PRD already commits. A member PRD's own
sigil comes off; another member's stays out. A `cwd` in neither root owns
nothing there, which is the safe reading rather than the permissive one.

What is deliberately NOT fenced is the footprint itself. On the laneless path
that footprint IS the uncommitted work verify exists to measure, so parking
it would make every verify read a clean HEAD instead of the change under
test. The cost of that decision — a green block can delete its own PRD's
uncommitted footprint and nothing puts it back — is measured here and closed
by `spec02`.

## Standing after pass two

Everything below is built and green in this lane against
`resources/board/collect.py`:

- `guarded_run`, `owned_by`, `_park`, `_heal`, `_head_of`, `_restore_head`
  and `_dirty` in `resources/board/collect.py`; the verify loop calls
  `guarded_run` and computes `owned` once, before the loop.
- `probe/probe_unit.py`, 6 cases — the mechanism at the unit level.
- `probe/probe_roots.py`, 6 cases — the grouping, on a board that is its own
  git repo, plus a witness that fails if pass one's rebase comes back.
- `probe/verify.sh`, 14 assertions — the incident reproduced at the CLI on
  `HEAD`'s `collect`, then `pearde collect` driven end to end past a
  destructive block on both board shapes.

Pass one rebased the footprint against `board_root` and had it backwards.
Measured on this board: `repo` is `/Users/feb/dev/infra/pearde` and
`board_root` is its `pearde/`, so pass one's grouping named
`.pearde/resources/board/collect.py` — a path in neither root — the file
under test read as foreign, and the verify block would have measured a clean
HEAD. Pass one's spec claimed the two roots were the same path here; they
are not, and the claim is corrected above.

## Acceptance

Every box below is built and green in this lane — `probe/verify.sh` prints
`14 passed, 0 failed`. They are left open because the run that ticks a box is
the run that re-measures it, and this tree is not the tree the implementer
will hold.


- [x] `guarded_run` stashes every path dirty in `cwd` that this PRD does not
      own before the block runs, by pathspec — absent from the working tree
      for the run, not merely reported on afterward
- [x] a block that empties the working tree leaves every foreign tracked and
      untracked path exactly as it was before the block ran, and the same
      block run unguarded really does empty it — the witness that makes this
      box able to fail
- [x] a block that runs `git reset --hard <old>` then `git clean -fdx`
      leaves foreign dirt intact and the branch back on the commit collect
      started the block from
- [x] the PRD's own footprint is left exactly as the block leaves it —
      `guarded_run` never parks it and never heals it
- [x] `cwd` with nothing foreign dirty: no stash is created, none is left
      behind
- [x] ordinary `git` commands run by a block (`git diff`, `git log`) see a
      correct, unpolluted tree while foreign dirt is parked
- [x] `collect_one`'s verify loop calls `guarded_run`, not `run`, for every
      spec's block and for the gate; `owned` is computed once, before the
      loop
- [x] `owned_by` groups a footprint path under `repo` and the PRD's own
      directory under `board_root`, and the two are separate rows when the
      board is its own git repo
- [x] a member PRD's own member sigil is stripped from its footprint and
      another member's sigil-carrying path is left out, as `sort_paths` does
- [x] a `cwd` that is neither `repo` nor `board_root` owns nothing there, so
      everything dirty in it is parked
- [x] with the board its own git repo, a verify block that reads its own
      footprint sees the change the lane just merged — it is not parked
- [x] `pearde collect` end to end, on both board shapes: a fixture board, a
      lane, foreign uncommitted work in the checkout and a green destructive
      verify block — `collect` reaches `done` and the foreign work survives
- [x] the same fixture on `HEAD`'s `collect` destroys the foreign work — the
      reproduction that makes the box above able to fail

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
grep -n "code, output = guarded_run" resources/board/collect.py
grep -c "^def guarded_run\|^def owned_by\|^def _park\|^def _heal\|^def _restore_head\|^def _head_of\|^def _dirty" resources/board/collect.py
test -z "$(grep -n '_foot_in' resources/board/collect.py)" && echo "no _foot_in left"
bash .pearde/prds/a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh
```
