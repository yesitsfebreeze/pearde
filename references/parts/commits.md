# Commits

One PRD, one commit, on the transition that lands it.

`collect` is the command — `python3 @resources/board/collect.py [<prd>…]`:
it reads the finished condition off both files, runs every spec's `## Verify
and Proof` block and the board's `gate:`, commits the paths below with the
message below, writes `commit:` and `actual:`, clears `claim:`, sets `done`,
posts the report, prints the progress line. `--dry` prints what would be added
and what would be left. This page is that command's behaviour, the scope
rules its step 3's spec.

Commit on the transition, or one working tree holds every PRD's work and
nothing can be reviewed, reverted or bisected alone.

The orchestrator commits. Never a worker — two implementers committing in
parallel write each other's half-finished files into each other's commits.

**Where the commit is made: the lane.** `claim` cuts the worker a git
worktree of its own at `<board>/.lanes/<slug>` on branch `lane/<slug>`
(@resources/board/lanes.py), named `<repo>` in the brief, so the worker's code
never touches the orchestrator's checkout. `collect` merges the branch in
before measuring: step 1b commits the lane's footprint paths **on the lane**
with the message below, rebases the lane onto the checkout's branch and
fast-forwards it in, then runs the verify blocks and the gate on the MERGED
tree — a lane that passes alone and breaks against what landed while it ran
goes red here and nowhere else. The lane's commit **is** the PRD's commit:
step 4 does not commit that repo again, so the checkout's branch gains two
commits per collected PRD — the work, and `<prd> — record`.

A red verify moves the checkout's **branch pointer** back to the commit it
started from — `git reset --keep`, never `--hard` — leaving the lane branch
untouched, so a retry merges the same commits again. Only the pointer moves:
the checkout's uncommitted work beside the merge, other sessions' and other
PRDs', survives, because a gate that deletes the work under measurement is
worse than a gate that stops. A merge that **merged nothing** is not rolled
back at all — no commits came in, so nothing goes back and no ref moves. A
rollback that cannot keep the uncommitted work refuses rather than discard it:
`collect` prints the paths git named, leaves the merge standing in the
checkout, and gives the `git reset --keep` line that finishes the rollback
once those paths are clear.

**A merge conflict is a red collect, never a silent stage.** When the lane
disagrees with what landed in the checkout while the worker ran, `collect`
exits non-zero naming every conflicting file, aborts both the rebase and the
merge, and leaves the checkout on its starting commit with nothing staged.
The lane branch still holds the work; a person merges it by hand. Two PRDs
claimed on one file end here by design — the plan orders the pair with an
`after … (footprint)` edge, and the clash resolves here rather than being
refused at `claim`.

A board with no lane — a claim taken before lanes, a board outside any git
repo — collects as before: the work is dirt in the checkout, step 4 commits
it, and every scope rule below reads that tree.

| transition          | do                                                              |
|---------------------|------------------------------------------------------------------|
| `claimed → done`    | commit                                                           |
| `claimed → blocked` | commit — the work is done, the open boxes wait on something named |
| `blocked → done`    | commit what closing the boxes wrote                              |
| `claimed → failed`  | nothing. Name the dirty paths in the report, leave them on disk  |

Board state written between transitions — answers, a refine split, a memo —
rides the next commit.

**Scope: the footprint, never the tree.** Add the union of the specs'
`footprint:` and the PRD's own, plus the PRD's folder, plus any workflow file
the collect edited. Never `git add -A`, never `git commit -a` — step 5 already
proved no other PRD with work in the tree writes that footprint. That band is
every live state but `open`, never worked and carrying no spec, and `done`,
whose work is already committed: an analyst leaves its probe uncommitted on
every verdict, so a `specced`, `question` or `refine` sibling holds code
exactly as a `claimed` one does. A file two of them share is split by hunk
wherever the claim baseline explains part of its dirt, and refused with
`--widen <path>` offered where it explains none — never swept whole in silence.

- **The inherited tree is not the board's.** Step 1 records what is dirty
  before the pass starts. Those paths are never added, whatever footprint
  they fall in. Name them once in the pass.
  `collect` reads that record from `.pearde/.claims/<prd>/` — the tracked diff,
  the untracked list and the gate's output at `claim:`, written by
  `snapshot()` in @resources/board/collect.py. The record covers two roots,
  keyed apart — the repo the board is in and the code repo the footprint lands
  in — so a board holding its own repo (a nested `.pearde`, or the linked
  worktree this machine runs) still has the code repo's dirt on record to
  split against. A claim recorded before the baseline covered the code repo
  holds no side for it and cannot tell that file's authors apart: the collect
  refuses, names the uncovered root, and offers
  `pearde collect --snapshot <prd>` on a clean tree. A dirty path outside the
  footprint is listed once and left. A dirty path inside the footprint that
  the claim predates stops the collect; `--widen <path>` takes it, and the
  message names it on a `widen:` line. A file holding inherited hunks and the
  worker's is committed by hunk: the staged blob is the working file with the
  inherited hunks reversed, each hunk at the line the working file has it,
  checked for parse and placement before the commit — never a patch
  `git apply` places — and the inherited hunks stay in the tree.
- **A hunk with two authors is refused, never committed whole.** Two edits
  on adjacent lines merge into one `-U0` hunk whose body is in neither the
  baseline nor the worker's diff, so `collect` exits 1 with
  `two authors on one hunk: <file>:<line>` and stages nothing;
  `--widen <file>` takes the file whole, or the worker leaves one untouched
  line between the edits.
- **The PRD's own folder is committed whole, and its `done` is in the same commit.**
  Nothing under `.pearde/prds/<prd>/` is staged by hunk or stopped as
  inherited — the record has one writer, the board — and `state: done`,
  `actual:`, the cleared `claim:` and the posted `## Report` are written
  before the commit that carries them; `commit:`, the one key that cannot name
  its own commit, lands in a second, one-key commit `<prd> — record` right
  behind it, so what `collect` writes never rides.
- **A parent whose children are all `done` is closed by `collect`.** With
  no spec and no open box of its own the parent is a container — `scan` lists
  it under collect, `claim` refuses it with `container: every child done —
  pearde collect closes it` — and `collect <parent>` sets `done`, `actual:`
  the sum of its children's, `commit:` the last child's, in one commit
  `<parent> — done: every child landed` that adds its `prd.md` alone; a
  parent with specs or boxes of its own is ordinary work.
- **Board state written between transitions rides the next collect.** An
  `answer` writes a `prd.md` no collect is about to commit; `owe()` lists
  the path in `.pearde/.claims/riders`, and the next collect on the board adds
  it and says `rides <path>` on the line. Beyond that named list, the collect
  sweeps the board: any file in the board's repo dirty since the claim's
  snapshot, that no other held PRD's folder holds, rides too — a memo, a
  workflow file, a report a worker wrote beside its build. Anything already
  dirty at `claim:` predates the claim and is inherited, never swept, so the
  sweep carries this worker's board edits and nobody else's.
- **The board's own machine-local dotfiles ride nothing, unless a footprint
  names one.** A dotfile under the board — `.claims/`, `.state/`, a
  `.pass.md`, a `.plan.json` — is this machine's, not the board's record, and
  the collect drops it in silence: not added, and not listed as inherited
  either, because nobody has to decide about it. The exception is a claim: a
  `footprint:` naming `.pearde/.gitignore`, a `--widen`, or a path inside the
  PRD's own folder is committed like any other, since somebody said out loud
  that it is theirs.
- **Which board a path is under is one string, and on a board that is its own
  repo that string is empty.** Both rules above ask "is this path under the
  board?", spelled inside the board's *own* repo. On the flat layout the
  answer is the board's directory name, `.pearde`. On a board that is a git
  repo of its own — this repo since 2026-09-02, and every nested `.pearde`
  with a `.git` — every path that repo prints is already under the board, so
  the prefix is the empty string and `under_board` in
  @resources/board/collect.py is the one function that reads it.
  `os.path.relpath` answers `"."` for that case, which is a prefix of no path
  git prints, and a `"."` here is the third wrong resolution of a board path
  after the two @.pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md
  replaced.
- **A path the worker wrote outside its footprint is a wrong footprint.**
  Commit it with the rest and say so.
- **The pass that moves an interface runs the probes that assert it.** A
  commit that changes what a tool prints, where a payload sits, or whether a
  route exists can leave a landed PRD's `probe/verify.sh` red without the
  commit going red — the probe lives in the PRD folder and nothing re-runs
  it. Read the change backward: run every harness naming the moved thing in
  its `want:` lines before landing (`bash resources/doctor.sh --harnesses` is
  the whole census, one line per red harness). A probe whose contract moved on
  purpose asserts the move — `/pass`'s removal is asserted as a 404 — rather
  than going quietly red.
- **A workflow file a collect edited is added with the rest, and named in the
  message.** No `footprint:` declares that path: the library is the board's,
  not the PRD's, so the PRD's footprint does not grow to hold it —
  @references/parts/workflows.md. Name each edited file on its own line under
  the spec lines, `workflow: <slug> — <what the run taught>`, so the commit
  says which run paid for the change.

**Message.** Subject `<prd> — <what landed>`, one line per spec, `prd:` naming
the folder:

```
<prd> — <the PRD's contract in one line>

<specNN>: <goal>
<specNN>: <goal>
workflow: <slug> — <what the run taught>
widen: <path>

prd: prds/<path>
```

`workflow:` and `widen:` lines appear only where the collect took such a path
— one per file.

Write the sha to `commit:` on the PRD, beside `actual:` — the only link from a
`done` PRD to its code, and where `retry` on a regression starts.

**One commit per repo the PRD wrote.** A PRD with `repo:` elsewhere writes
code there and its record on the board: commit each where it lives, same
subject — on a master board, the member's repo. A library `workflows:` points
into another repo follows the same rule: its edits commit there, same subject,
never riding a commit in the repo the PRD wrote.

**Which repo a footprint path lands in.** Which repo holds a path is the git
checkout's answer, never a string's. `foot_root` in
@resources/board/collect.py tries each place a spelling can resolve — the code
repo first, then the board — takes the first one the filesystem or an index
holds, and asks `git rev-parse --show-toplevel` for the checkout that holds
it. The board's path as a prefix decides nothing.

Both spellings resolve. `.pearde/.gitignore`, code-repo-relative, is the one to
prefer for any file the code repo could hold; the board's own spelling —
`prds/<prd>/probe/verify.sh`, where every probe on the board lives — resolves
as well, and a spec that names it is no longer refused. Either way a path
under a board holding a `.git` of its own is committed in the **board repo**
under its **board-relative** name, beside the PRD's record. The code repo
never stages it, because that repo ignores the board and holds no such path;
`git add` there answers `fatal: pathspec … did not match any files` and aborts
the whole add, so one such path used to take down a merge with nothing else
wrong with it. The lane never stages it either — `claim` cuts the lane without
the board — so the board's own file is the checkout's to commit. Where the
board is not a repo of its own the two roots are one and nothing is rerouted.

A code checkout nested **under** the board is a repo of its own, and its
footprints are never the board's. Every lane at `<board>/.lanes/<slug>` and
every run-session worktree has that shape: inside the board's path, in neither
the board's index nor its worktree. A prefix test read each of them as the
board's, staged them against an index that ignores them, and committed
nothing — no error, no refusal, an empty commit. `foot_root` is the single
answer all three of the lane's add, the ownership fence and the grouping read,
and @.pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md is the
invariant that holds it.

**Never push.** The commit is the board's, the push is the user's. Report what
is ahead and stop.

`commits: off` in `.pearde/settings.md` holds all of it — each transition then
names its dirty footprint. While on, a `*<dirty>` count climbing across passes
is a board whose commits are not landing.
