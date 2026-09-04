# report — init and upgrade write the dotted board

Verdict: SPECCED

complexity 14 · blast-radius mid · workflow `probe-then-spec`

## What the build found

The four clauses of the contract were already standing as **uncommitted work in
this PRD's lane** — pass one, left by the parent's own probe. `git log -S` finds
neither `dot_board` nor `split_ignore_block` in any commit; `git status` in
`.pearde/.lanes/…-init-and-upgrade-write-the-dotted-board` shows
`M resources/board/init.py`, 176 insertions against 85 deletions. So the first
thing this pass did was measure that work rather than repeat it.

A probe of six cases was written and it passed all of them: a fresh `pearde
init` leaves a real `.pearde/` with nothing at `pearde/`; `pearde upgrade` moves
a legacy board and rewrites the ignore block whole; a file an older append had
doubled heals to one block; a directory called `pearde/` that carries no
`settings.md` is not renamed, because the guard is `planlib.is_board_dir` and
not `os.path.isdir`; a second `upgrade` writes nothing.

Then the probe was pointed at the one real file the footprint names — this
repo's own `.gitignore` — and two defects fell out that the synthetic fixtures
could not reach.

### The whole-block rewrite did not fire on a header a person had annotated

`split_ignore_block` matched its header by equality. This repo's header line is
`# machine-local per board — regenerable.` followed by a sentence, with five
comment lines under it. Equality found no block, so `write_gitignore` appended a
**second** header and left every stale row of the first standing — measured:
header count 2, `/pearde` and `/.pearde` still there, `pearde/.state/` and
`pearde/wiki/` still there. The clause the contract names — rewrites the block
whole instead of appending a second — was therefore false on the only file that
mattered.

Fixed in the build: the header is matched by `startswith` and the block runs to
the first blank line, so the header, whatever a person wrote under it, and the
rows are one block. The block is the tool's, so a comment inside it is dropped
on the rewrite — which is how a stale explanation goes rather than outliving the
layout it describes. `write_gitignore`'s idempotence check now compares only the
non-comment rows and requires the header exact, so an annotated block is
normalised once and every run after that writes nothing.

### Dropping the whole-directory row would have staged the board as a gitlink

`init.py`'s new comment says the `/.pearde` row "could not stay, because
`.pearde` is now the board itself" — right for the normal board, whose plan the
parent repo tracks, and wrong for a board that carries its own `.git`. This
repo's board is a **worktree of the code repo** (`.pearde/.git` reads
`gitdir: …/.git/worktrees/-pearde`), and git will not descend into a nested work
tree. Measured in a fixture — `git init r; git worktree add .pearde board`,
per-folder rows only:

```
--- git status ---     ?? .pearde/
--- git add -A ---     warning: adding embedded git repository: .pearde
--- ls-files -s ---    160000 18bb912… 0    .pearde
```

A submodule entry pointing at a commit no clone can fetch, on any `git add -A`
in the code repo, forever. Fixed in the build: `ignored_names(board)` prepends
`/<board>` — leading slash, no trailing one, because `pearde share` symlinks the
graphify cache under the board and a `dir/` pattern does not match a symlink —
when `os.path.exists(board/.git)` (`exists`, not `isdir`: a worktree's `.git` is
a file). A board the parent tracks still gets the per-folder rows only, so the
PRDs stay in the parent's history. That measurement is on the record as
`.pearde/wiki/sources/260903-4626.md`.

This repo's `.gitignore` was then brought to the shape the tool would write:
one canonical block holding `/.pearde` and the eight dotted rows, the stale
second block and its comment gone, every other block byte for byte where it was.

The probe now stands at 26 checks, all passing, and it is left uncommitted at
`prds/…/init-and-upgrade-write-the-dotted-board/probe/probe.sh`.

## Harnesses

Baseline captured before the tree was touched and re-run after: unchanged.
`index.py check` prints the same single finding, `install.sh --check` the same
rows, and the same three invariants read FAIL from a lane worktree
(`every-artifact-lands-inside-the-board`,
`no-colour-group-in-the-vault-preset-is-a-path-query`,
`no-destructive-git-runs-in-a-tree-the-session-does-not-own`). Nothing this pass
wrote moved a count.

## Specs

| spec | goal | complexity | footprint |
|---|---|---|---|
| `specs/spec01.md` | init writes a real `.pearde/`, upgrade moves a board into it, and the ignore block is rewritten whole | 10 | `resources/board/init.py` |
| `specs/spec02.md` | this repo's own `.gitignore` is the block the tool would write | 4 | `.gitignore` |

Footprint union: `resources/board/init.py`, `.gitignore`. Disjoint from every
sibling on this parent — `the-board-name-is-one-dotted-constant` owns
`resources/board/name.py`, `boards.py`, `guard.py`, `grammar.py`, `health.py`,
`memos.py`, `questions.py`, `statusline.sh` and `doctor.sh`; the prose child owns
`references/` and `resources/invariants/`.

Both specs are review-and-land rather than build-from-nothing: the code stands
and is green under the probe. Each spec's *What already stands* section says
what is there and *What is left to finish* says what the second reader owes.

## Findings — outside this PRD, not fixed here

1. **`references/parts/commits.md` names `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`,
   which is not on disk.** `index.py check`'s one standing finding, and the file
   is under `.pearde/memos/`. Belongs to
   `the-prose-and-the-invariants-say-dot-pearde`.
2. **`resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh`
   refuses with `BROKEN: no board at pearde/`.** It resolves the board by the
   legacy name alone, so it is broken on every board this repo now makes. Same
   sibling.
3. **`resources/workflows.py list <board>` answers
   `workflows: no pearde/ board at <board>`** — a second reader still spelling
   the legacy name, and in a message a worker reads. Same sibling.
4. **`resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh`
   reports `resources/board/session.py:586 — git reset is not gated`.** The
   commit `cc624b3` claims that invariant is green again; it is not, from a lane
   worktree. Outside this footprint entirely.
5. **`every-artifact-lands-inside-the-board` fails its own fourth check** —
   "the guard refuses the board's own pass file — the rule is too wide". A check
   that fails at baseline is not this PRD's, but it is not a check anyone is
   reading either.
6. **`init.py` is 1,371 lines and holds init, upgrade, the vault, the knowledge
   seed, the grammar seed, the graph plant, the host-settings advice and two
   gitignore writers.** `pearde health` would have an opinion. Recorded, not
   acted on.

## A workflow that recurred and already has a file

`probe-then-spec` fit this run step for step — read the contract, capture the
baseline, attempt the build, re-run the harnesses, write the specs — and its
step 3 is exactly what turned a PRD that looked already-done into two real
defects. No new file is warranted.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
