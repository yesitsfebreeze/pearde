# report — list-the-collects-the-repo-bug-orphaned

Workflow followed: `probe-then-spec` (read-the-contract · capture-the-harness-baseline
· attempt-the-build · write-the-specs). Baseline before the first edit:
`python3 resources/index.py check` exit 0, `bash resources/doctor.sh` exit 0
(memos/workflows/briefs/questions ok; view/plan/harnesses rows off as installed
— none in this PRD's footprint). Every file this round touched is inside the
PRD folder; no footprint file was edited.

## The build

`prds/…/list-the-collects-the-repo-bug-orphaned/probe/scan.py` + `probe/verify.sh`
(left in the tree, uncommitted — pass one). It reads the nine boards from
`resources/board/state/serve.json`, enumerates their done PRDs (255, 166 with
footprints), and classifies each footprint path against the branch that should
hold it, per the machine's actual git shape:

**The premise moved under the PRD.** `.pearde` is not a second git repo — `git
-C .pearde rev-parse --git-dir` says `/Users/feb/dev/infra/pearde/.git/
worktrees/-pearde`. One store, two worktrees: the code on `main`, the board on
branch `pearde`. The two collects before the fix were hand-committed and the
two before that are suspect — under this shape, "which repo holds sha X" is a
meaningless question (both see every sha), and `git log --all` from either
worktree sees everything, so it can never catch a misdirected commit. The
check that can fail is per-branch: `git log <branch> -- <path>`.

So the probe checks per branch: a footprint path must have a commit on the
branch that actually checks out its worktree. Classes per path: `ok`
(landed on its own branch) · `branch-only` (landed on the OTHER worktree's
branch, never on its own — the repo bug's residue, the class a person
re-commits) · `nowhere` (no commit anywhere, file on disk) · `absent`
(no commit, not on disk — stale spelling). It also honours a PRD's `repo:`
key (collect's `repo_of()` honours it too; a PRD may name a different repo),
and reads `.state/transitions.jsonl` done rows and `time.actual` where the
board keeps them (only the pearde board keeps a transitions file).

The decision tree was proven on a hand-built fixture (temp dir, since
removed): a repo with a nested worktree board and a done PRD whose footprint
path the board branch holds and main does not classifies `branch-only` —
through the probe's own `branch_local` calls. `probe/verify.sh` re-proves the
rest on live data: 6 assertions, `PASS 6`.

## The numbers

Across the nine registered boards: 255 done PRDs, 166 carrying footprints.

**Bug residue — `branch-only`: 0.** Every code footprint that collect
misdirected onto the board branch during the window (board moved to
`.pearde/` 15:49, `repo_of()` fixed 18:36 — commits 7b88100 → 0849795)
already reached `main` via twin commits: the pearde branch holds 25
non-record work commits since the move, 17 of them with same-subject twins
on main (e.g. `eded6ef` → `aea6dae`), and every distinct path they touch is
present in main's history. **There is nothing left for a person to
re-commit from the old bug.** The hand-commits the board already knew about
are visible in the record: the two collects around 22:05–22:06 went in by
hand (`7809756` on main, `2a3c69a` on the board branch with the round's
board-side files).

**Flagged: 5 done PRDs**, none of them bug residue:

- ***dotfiles* `00-delivery/corrections/gate-artifact-leakage`** — spec03's
  footprint names the three leaked artifacts (`cf-rm-site-dropped.nu`,
  `cf-rm-site-in-another-def.nu`, `nvim.log`) the PRD was created to DELETE;
  deleted, never committed. Correct final state, not work.
- ***dotfiles* `00-delivery/corrections/git-diff-integrity-boxes`** — spec02's
  footprint `.claude/skills/prd/README.md` names a retired layout path; absent
  on disk, never tracked. Stale spelling.
- ***dotfiles* `06-help/06-manual-markdown`** — `scripts/generate-manual.mjs`
  and `home/dot_config/television/cable/docs.toml` exist on disk but were
  never committed (the sibling `docs-site/scripts/generate-manual.mjs` was
  tracked and deleted). **This one is real uncommitted work of a done PRD** —
  the only finding in the whole scan a person may want to act on.
- ***pearde* `the-board-runs-itself/vision-is-first-class`** — four ABSOLUTE
  footprint paths into `/Users/feb/dev/infra/prds/…` (the pre-move layout);
  none exists today. Every real landing of that PRD (`resources/board/plan.py`,
  `references/templates/vision.md`, …) is `ok`. Stale footprint spelling.
  Its recorded `commit: e2890a0 9776cb9` is a dangling commit — reachable from
  NO ref (`git branch -a --contains` empty, not in `rev-list --all`); twins
  `db53e81`/`eb2f622` with the same subjects are on main. The frontmatter
  points at a rebased-away commit.
- ***pearde* `the-vault-ignores-the-paths-the-board-writes`** —
  `.obsidian/app.json` is gitignored on main BY the ignore list this PRD's own
  spec delivered — it can never be committed there. The spec's boxes compare
  template vs live lists and both match; the flag is by design.

**The dotfiles board is structurally immune**: `dotfiles/.pearde` has no
`.git`, so the old `repo_of` default resolved to the dotfiles repo itself —
exactly the right repo. Only nested-board worktrees could be bitten.

Also machine-proven along the way: the two earlier probe findings ("census
README.md, gate-artifact-leakage nu files flagged nowhere") were a
cross-repo short-sha collision in a first-draft check — `git log --all` in the
pearde store is NOT the dotfiles repo's history; and census's `repo:
~/dev/infra/pearde` means its README landed in the pearde repo's main, where
it is. Both resolved by honouring `repo:` and dropping `--all` in favour of
per-branch checks.

## Findings (not in any spec)

- **The orchestrator correction's git model is wrong at the git level.** "Two
  git repos, nested" — `.pearde` is a git WORKTREE of the same repository
  (`gitdir: /Users/feb/dev/infra/pearde/.git/worktrees/-pearde`), branch
  `pearde`, code worktree on `main`. Any check written as "does repo X hold
  sha Y" is wrong: one store, 229 commits, all visible from both. The brief's
  `git log --all` instruction would have found every path landed and hidden
  the bug completely — per-branch is the only check that can fail.
- The brief's "nine boards" is right over `serve.json`, but one of them
  (`/Users/feb/dev/prds`) is empty, and the pearde board's transitions file is
  the only one on the machine (`.state/transitions.jsonl`, 155+ rows); done
  PRDs on the other eight carry `time.actual` only in frontmatter.
- `git log --all` from either worktree also resolves short SHAs into both
  repos' histories — any future check on `commit:` frontmatter must use full
  shas (`rev-parse` then `cat-file -e <full>` in the other repo). Today's
  frontmatter shas all resolve on exactly one branch or point at a dangling
  commit (`e2890a0`, vision-is-first-class) — flagged above.
- The knowledge query auto-enqueued nothing this round: a pending note
  (`260831-17e4.md`, "A Verify block that cannot fail is refused") predates
  this claim (written 20:20, claim 22:20) and is not mine.

## What already stands / what is left

- Stands, uncommitted in the probe folder: `scan.py` (188 lines, branch-aware,
  `repo:`-aware, `rows.json` detail), `verify.sh` (PASS 6), `rows.json`.
- Left, in `specs/spec01.md`: land the scan as
  `resources/board/orphans.py` with its manifest row and scopes; fixture
  proof for the `branch-only` class inside the spec's own verify.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec

complexity 12 because the build's substance was discovering the machine's
real git shape (shared store, two worktrees, per-branch semantics) and
rewriting the check three times as that surfaced; the scanner itself is one
stdlib module. blast-radius low: the scan writes nothing and commits nothing —
its worst failure names work as orphaned that is not, costing one wasted look.
Workflow `probe-then-spec` from the library fit as-is; no new route.