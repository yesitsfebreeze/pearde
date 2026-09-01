# filing-refuses-a-file-it-does-not-hold — analyst report

Verdict: SPECCED

Workflow followed: `probe-then-spec` — its `## Use when` names exactly this
job ("A PRD is `open` and needs specs before anyone can be sent at it"). All
five of its steps were taken, in order. No new workflow is named, so there is
no `## Route` below.

One spec: `specs/spec01.md` — `--also` resolves against the board, and refuses
what the board does not hold. `pearde specced --check` reads
`ok · complexity 8 · footprint .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe, resources/board/collect.py`.

Footprint union: `resources/board/collect.py`,
`.pearde/prds/filing-refuses-a-file-it-does-not-hold/probe`.

**complexity 8** — one guard and one resolution change in one file, 37 lines,
against a mechanism the PRD had already located line for line; the harness was
the larger half of the work.
**blast-radius mid** — `collect` is the board’s only write path and every board
inherits this, and the change can newly refuse a call that used to succeed (a
relative `--also` spelled from a cwd that is not the board); it is not `high`
because it fires only when `--also` is passed, and the 133-check `collect`
harness is unchanged by it.

## What the record said

`python3 resources/knowledge.py query` on the contract returned 11 hits, 11
strong, over 11 notes on record — the closest being `[[260901-90ed]]
collect-report-routes-the-verdict` and `[[260901-ee0f]] Every pearde board on
this machine is on the .pearde layout`. **No gap was enqueued**:
`.pearde/wiki/pending/` holds the same six files it held before the query, the
newest dated 2026-09-01. Nothing was learned outside this tree, so nothing was
written back with `remember`.

## The build

The PRD’s mechanism was accurate line for line; it was cited, not re-derived.
The build went through end to end and is in the tree, uncommitted.

`resources/board/collect.py`, +37/-1:

- `also_path(board_root, a)` — the one place an `--also` entry becomes a path,
  resolving a relative entry against `board_root` the way `--widen` already
  does two lines below the loop. Both the guard and `sort_paths` read it, so
  the path a refusal names and the path a commit carries cannot drift.
- `check_also(board_root, opts)` — refuses on `not os.path.exists(p)`, naming
  the entry as given, the absolute path it resolved to, and the board root.
- `cmd_collect` calls it immediately after `find_board`.
- `sort_paths`’ `--also` loop reads `also_path(board_root, a)` in place of
  `os.path.abspath(a)`. `--widen` and the footprint loop are untouched.

**Why the guard sits in `cmd_collect` and not in `sort_paths`.** The build hit
this, and it decided the shape: `cmd_collect`’s `for rel in rels` loop catches
`Stop` per PRD and carries on to the next one. A guard inside `collect_one`
would refuse the PRD that noticed the bad path and then commit every later PRD
on the same call — a partial filing, not the refusal the user chose at the
drill. Probe section B holds this down: two collectable PRDs, one bad `--also`,
both left `claimed` with no commit, and the refusal printed once, not per PRD.

**The predicate is `os.path.exists`, not `os.path.isfile`.** The contract says
"a file that exists on the board", but the model it names as correct — the
footprint loop eight lines above — uses `os.path.exists`, and footprints are
routinely directories. Narrowing to `isfile` would refuse `--also
references/parts`, a live use and not what the PRD asks to stop. The probe pins
both halves: a directory the board holds goes through and its files ride the
commit; a directory the board does not hold is refused.

## The reproduction

`.pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh` — a
throwaway board under its own `git init` per scenario, never the real board.
Eight sections, 41 checks, **41 pass · 0 fail**.

The harness is provably able to fail: `COLLECT` is overridable, and pointed at
`git show HEAD:resources/board/collect.py` the same 41 checks read **20 pass ·
21 fail**. On that pre-fix binary `--also notes/nope.md` exits **0**, commits,
and writes eleven paths into the record including
`../../../../../../../private/var/…` — the `ca29535` mechanism, reproduced.

Sections: A a path that exists nowhere · B the whole call is refused, with a
no-`--also` control · C board-relative resolution, including from a foreign cwd
· D a path that exists only under the callers cwd · E absolute paths, both ways
· F a directory, both ways · G a container close · H usage unchanged.

## Harnesses

Baseline taken before the first edit, from `find .pearde/prds -name verify.sh`
(48 harnesses), filtered to the six that read `collect.py` or enumerate the
board. HEAD was `f3aea95` and `git status --short` was empty at that point.

| harness | before the first edit | after |
|---|---|---|
| `collect-keeps-its-word` | 101 · 101 pass · 0 fail | 101 · 101 pass · 0 fail |
| `hunks-land-where-they-came-from` | 47 · 47 pass · 0 fail | 47 · 47 pass · 0 fail |
| `the-line-tells-the-truth` | 85 · 85 pass · 0 fail | 85 · 85 pass · 0 fail |
| `collect-is-a-command` | 133 · 132 pass · **1 fail** | 133 · 133 pass · 0 fail |
| `the-collect-and-brief-harnesses…` | 7 · 5 pass · **2 fail** | 7 · 7 pass · 0 fail |
| `workflow-improve` | 70/71 · **1 fail** | 71/71 |

`python3 resources/index.py check` exit 0 before and after.
`bash resources/doctor.sh` exit 0, every row `ok` or `off`, no row added and
none removed.
`resources/invariants/every-artifact-lands-inside-the-board.sh` green, 5/5.

**Three harnesses were red before the first edit and are green after, and none
of the three flips is mine.** They are a sibling session’s uncommitted work
landing mid-run — finding 1 below. My diff is `resources/board/collect.py`
alone; `git diff --stat` reads `1 file changed, 37 insertions(+), 1 deletion(-)`.

Baselined failure lines, recorded before the first edit:

- `collect-is-a-command`: `FAIL R the copy s registry never learned the fixture`
- `the-collect-and-brief-harnesses-are-carried-across-the-layou`: both its
  failures were only it observing `collect-is-a-command` at 132/133.
- `workflow-improve`: `FAIL workers.md s table row — references/parts/workers.md
  lacks any of the three, plus ## Workflow <slug>`

## Findings — outside this contract, not fixed

1. **A sibling session is writing this tree right now.** At the end of the run
   `git status --short` lists ` M references/parts/workers.md`, ` M
   resources/board/brief.py`, ` M resources/board/init.py`, ` M
   resources/doctor.sh` — none of them mine, none committed, HEAD still
   `f3aea95`. Those edits are what flipped `workflow-improve` (`workers.md`) and
   `collect-is-a-command`’s registry check (`init.py`) green under me. Whoever
   collects this PRD must not carry those four files with it.

2. **`close_container()` silently drops a valid `--also`.** It reads no
   `opts["also"]` at all — the PRD says so and the build confirmed it. The new
   pre-flight now refuses a *bad* `--also` on a container close (probe section
   G), but a *good* one is still dropped: the file is not added and the message
   never mentions it. That is a second way filing can fail to hold what it
   names, and a different contract from this one — this PRD asks for a refusal,
   not for `--also` to start working on containers.

3. **`--widen` has no existence guard either.** The loop at `:860-862` builds a
   set of absolute paths and never checks them; `--widen <path the board does
   not hold>` silently widens nothing. Harmless where `--also` was not — it
   drops a path rather than inventing one, and nothing false is named in the
   record — but it is the same missing check. The PRD forbids touching
   `--widen`, so it is left alone.

4. **`capture-the-harness-baseline` still names the pre-`.pearde` layout.** Its
   step 1 says `find prds -name verify.sh`, which finds nothing on this board;
   the harnesses live under `.pearde/prds/`. This is the job
   `every-probe-harness-is-re-aimed-at-the-pearde-layout` already covers — a
   finding, not a second workflow file and not a new PRD.

## Scores

complexity: 8
blast-radius: mid
workflow: probe-then-spec
