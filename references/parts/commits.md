# Commits

One PRD, one commit, on the transition that lands it.

The command is `collect` — `python3 @resources/board/collect.py [<prd>…]`:
it reads the finished condition off both files, runs every spec's `## Verify
and Proof` block and the board's `gate:`, commits the paths below with the
message below, writes `commit:` and `actual:`, clears `claim:`, sets `done`,
posts the report, prints the progress line. `--dry` prints what it would add
and what it would leave. The rules on this page are what that command does,
and the scope rules are the spec of its step 3.

Commit on the transition — otherwise one working tree holds every PRD's work,
and nothing can be reviewed, reverted, or bisected on its own.

The orchestrator commits. Never a worker — two implementers committing in
parallel write each other's half-finished files into each other's commits.

**Where the commit is made: the lane.** `claim` cuts the worker a git
worktree of its own at `<board>/.lanes/<slug>` on branch `lane/<slug>`
(@resources/board/lanes.py), and the brief names it as `<repo>`, so the
worker's code never touches the checkout the orchestrator holds. `collect`
merges that branch in before it measures anything: step 1b commits the
lane's footprint paths **on the lane**, with the message below, rebases the
lane onto the branch the checkout is on and fast-forwards it in — then runs
the verify blocks and the gate on the MERGED tree, because a lane that
passes alone and breaks against what landed while it ran is a red here and
nowhere else. The lane's commit **is** the PRD's commit: step 4 does not
commit that repo a second time, so the checkout's branch gains exactly two
commits for a collected PRD — the work, and `<prd> — record`. A red verify
moves the checkout's **branch pointer** back to the commit it was on —
`git reset --keep`, never `--hard` — and leaves the lane branch untouched,
so a retry merges the same commits again. Only the pointer moves: the
checkout's uncommitted work standing beside the merge, other sessions' and
other PRDs', is kept, because a gate that deletes the work it was checking
is worse than a gate that stops. A merge that **merged nothing** is not
rolled back at all — no commits came in, so there is nothing to put back and
no ref to move. And a rollback that cannot keep the uncommitted work refuses
rather than discarding it: `collect` prints the paths git named, leaves the
merge standing in the checkout, and gives the `git reset --keep` line that
finishes the rollback once those paths are clear.

**A merge conflict is a red collect, never a silent stage.** When the lane
disagrees with what landed in the checkout while the worker ran, `collect`
exits non-zero naming every conflicting file, the rebase and the merge are
both aborted, the checkout is on the commit it was on and nothing is
staged. The lane branch still holds the work; a person merges it by hand.
That is the designed outcome of two PRDs claimed on one file — the plan
orders the pair with an `after … (footprint)` edge, and the clash is
resolved here rather than refused at `claim`.

A board with no lane — a claim taken before lanes, a board outside any git
repo — collects exactly as it did before: the work is dirt in the checkout,
step 4 commits it, and every scope rule below reads that tree.

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
proved no other PRD with work standing in the tree writes that footprint. That
band is every live state but `open`, which has never been worked and carries no
spec, and `done`, whose work is already in a commit: an analyst leaves its probe
uncommitted on every verdict, so a `specced`, `question` or `refine` sibling
holds code exactly as a `claimed` one does. A file two of them share is split by
hunk whenever the claim baseline explains part of its dirt, and refused with
`--widen <path>` offered when it explains none — never swept whole in silence.

- **The inherited tree is not the board's.** Step 1 records what is dirty
  before the pass starts. Those paths are never added, whatever footprint
  they fall in. Name them once in the pass.
  `collect` reads that record from `.pearde/.claims/<prd>/` — the tracked diff,
  the untracked list and the gate's output at `claim:`, written by
  `snapshot()` in @resources/board/collect.py. That record covers two roots —
  the repo the board is in and the code repo the footprint lands in — keyed
  apart, so a board that is its own repo (a nested `.pearde`, or the linked
  worktree this machine runs) still has the code repo's dirt on record and can
  be split against it. A claim recorded before the baseline covered the code
  repo holds no side for it, so nothing tells that file's authors apart: the
  collect refuses, names the root the baseline never covered, and offers
  `pearde collect --snapshot <prd>` on a clean tree. A dirty path outside the
  footprint is listed once and left. A dirty path inside the footprint that
  the claim predates stops the collect; `--widen <path>` takes it, and the
  message names it on a `widen:` line. A file holding inherited hunks and the
  worker's is committed by hunk: the staged blob is
  the working file with the inherited hunks reversed, each hunk at the line
  the working file has it, checked for parse and placement before the commit
  — never a patch `git apply` places — and the inherited hunks stay in the
  tree.
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
  before the commit that carries them; `commit:`, the one key that cannot
  name the commit it is in, lands in a second, one-key commit
  `<prd> — record` right behind it, so what `collect` writes never rides.
- **A parent whose children are all `done` is closed by `collect`.** With
  no spec and no open box of its own it is a container — `scan` lists it
  under collect, `claim` refuses it with `container: every child done —
  pearde collect closes it` — and `collect <parent>` sets `done`, `actual:`
  the sum of its children's, `commit:` the last child's, in one commit
  `<parent> — done: every child landed` that adds its `prd.md` alone; a
  parent with specs or boxes of its own is ordinary work.
- **Board state written between transitions rides the next collect.** An
  `answer` writes a `prd.md` no collect is about to commit; `owe()` lists
  the path in `.pearde/.claims/riders`, and the next collect on the board adds
  it and says `rides <path>` on the line.
- **A path the worker wrote outside its footprint is a wrong footprint.**
  Commit it with the rest and say so.
- **The pass that moves an interface runs the probes that assert it.** A
  commit that changes what a tool prints, where a payload sits, or whether a
  route exists can leave a landed PRD's `probe/verify.sh` red without the
  commit going red — the probe lives in the PRD folder and nothing re-runs
  it. Read the change backward: which harnesses name the moved thing in their
  `want:` lines, and run those before landing (`bash resources/doctor.sh
  --harnesses` is the whole census, one line per red harness). A probe whose
  contract moved on purpose asserts the move — `/pass`'s removal is
  asserted as a 404 — rather than going quietly red.
- **A workflow file a collect edited is added with the rest, and named in the
  message.** It is the one path in the commit that no `footprint:` declares:
  the library is the board's, not the PRD's, so the PRD's footprint does not
  grow to hold it — @references/parts/workflows.md. Name each edited file on
  its own line under the spec lines, `workflow: <slug> — <what the run
  taught>`, so the commit says which run paid for the change.

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

`workflow:` and `widen:` lines are there only when the collect took such a
path — one per file.

Write the sha to `commit:` on the PRD, beside `actual:` — the only link from a
`done` PRD to its code, and where `retry` on a regression starts.

**One commit per repo the PRD wrote.** A PRD with `repo:` elsewhere writes
code there and its record on the board: commit each where it lives, same
subject. On a master board that is the member's repo. A library that
`workflows:` points into another repo is that same rule: its edits commit
there, same subject, and never ride a commit in the repo the PRD wrote.

**Never push.** The commit is the board's, the push is the user's. Report what
is ahead and stop.

`commits: off` in `.pearde/settings.md` holds all of it — each transition then
names its dirty footprint. While on, a `*<dirty>` count climbing across passes
is a board whose commits are not landing.
