# the documented board matches the code — analyst report

Verdict: SPECCED

Eleven of the thirteen drift lines reproduced against the code and are fixed in
the lane, uncommitted, across 25 files. Two do not reproduce and one more was
already fixed before this pass — all three are under **Findings**, with no edit
made for them. A probe at `probe/verify.sh` checks one line each: it goes green
on the lane and red on eleven checks against `HEAD`, so every acceptance box
behind it can fail.

- specs: `specs/spec01.md` … `specs/spec05.md`
- complexity 32 · 5 specs — `pearde specced --check` accepts both
- probe: `probe/verify.sh <repo-root> [<board>]` — 11 checks, exit 1 on any
- baseline: `index.py check` 4 problems before and after, all pre-existing;
  every `doctor.sh` row the same state before and after

## What was built

| # | line | reproduced | fix |
|---|------|---|---|
| 1 | `board.md` draws settings/vision/memos/workflows under `prds/` | yes | tree redrawn at the board root, eight siblings named; `specs` named as the one directory `registry._scan_one` prunes |
| 2 | docstrings name moved `prds/…` paths | yes, in 9 files not 2 | swept: `.state/plan.json`, `.state/pass.md`, `.state/transitions.jsonl`, `.claims/`, `settings.md`, `vision.md` |
| 3 | `commits.md` promises `commits: off` | yes | no key declared, no reader; the promise is replaced by "there is no off switch" |
| 4 | blast-radius breaks ties | yes, in 4 files not 2 | `compute_plan` never reads it; it is a label and a `blast/<blast>` tag |
| 5 | `settings.md` says `pipeline` caps analyst slots | yes, harder than stated | **no** module reads it at all; the row now says so and contrasts `workers`, which `schedule.py` does read |
| 6 | `doctor.md` lists 14 rows for 21 | yes | table rewritten in print order, all 21, conditions read off `doctor.sh`'s own `row` calls |
| 7 | vault rooted at the board | yes, in 4 files not 2 | the project is the vault; `files.md` and `graph.md` carried copies |
| 8 | `view.md` says seven views and a `/pass` route | half | eight tabs: `view.md`, `view.css`, `viewtest.js` corrected and `view.js` bound `⌘1–8`. `/pass` was already gone |
| 9 | `all.md` documents `/sync` | **no** | see Findings |
| 10 | `plan.py` cites an absent memo | yes, wrong file named | the citers are `prdfile.py` and `mapfile.py`; both now point at `standing`'s docstring, which holds the rule |
| 11 | `handles.md` / `skills/pearde.md` name `master <path>` | **no** | see Findings |
| 12 | README says four `.gitignore` names; `unblock` lands on done | half | ten, proved by a real `init --example` in a temp repo. `unblock` was already correct |

One line moved the code rather than the text: `view.js` bound `⌘1`–`⌘7` over
eight tabs, so the eighth was unreachable. Binding `⌘8` is one character; the
alternative was to document a dead tab.

## Findings — no edit made

**`/sync` reproduces nothing.** `serve.py:1503` implements `POST /sync` with
exactly the `board: all` semantics `all.md:108` describes, and `serve.py:109`
documents it in its own header. The claim is correct. What *is* true, and is
not what the sweep said: no client in `view.js` posts `/sync` — it is a route
the page never fetches, the same shape as the `/pass` route that was removed.
Whether to drop it is a decision, not a drift.

**`master <path>` reproduces nothing as stated.** `handles.md`'s Command column
for that row is `—`, and the page defines `—` as "a handle the pass answers by
hand, with no command behind it". The `pearde-master` skill is its
implementation. `pearde members` — the row below it — is the one with a module,
and it has one.

**Three halves were already fixed.** `view.md:325` already says `/pass` is gone
and no `/pass` survives in `serve.py`; `README.md:61` already reads
`blocked --> specced : unblock <prd>`. The PRD says so for `unblock`; it does
not for `/pass`.

**The board's own directory name has three answers.** `boards.py:67-68` sets
`BOARD_DIR = ".pearde"` with `pearde` as the legacy name. `board.md`'s "Where
the board is" says the opposite — the board is `pearde/`, `.pearde/` is the
legacy name and the compat symlink — and names `<project>/pearde/` as "the path
`pearde init` creates". A real `init --example` run in a temp repo creates
`.pearde/`. `doctor.sh`'s `vault` row calls a real `.pearde/` **broken** and
offers `pearde upgrade` as the fix, which is why this repo's own doctor reports
`vault broken`. This also produces one of the four standing `index.py check`
failures: `commits.md` cites `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`,
the memo is on disk at `.pearde/memos/`, and the index resolves `@pearde/`
against a `pearde/` directory that does not exist. Out of this contract — it is
one claim in three places disagreeing, not a documented line the sweep listed —
and it is the largest thing still wrong on this tree.

**`board.md`'s "written seven times" sentence is stale.** It names `plan.py`,
`health.py`, `questions.py`, `memos.py`, `grammar.py`, `guard.py` and
`doctor.sh` as seven copies of the board walk. `resources/common.py:125-132`
now holds `board_above` and `find_board`; `guard.py` defines neither;
`workflows.py:92` has one the sentence does not name. Same file as line 1, but
not the line the contract names, so it is here rather than in spec01.

**`doctor.sh`'s `jstests` row names a deleted file.** Lines 998, 1027 and 1031
run and report `resources/board/hotreload-test.js`, removed in `b1d3f5d`. It is
also two of the four standing `index.py check` failures, via `references/files.md`
and the `@@view` scope.

**`workers` has `pipeline`'s shape but not its problem.** Both rows in
`settings.md` read as caps the tool enforces, and both are honoured by the
orchestrating session. The difference is that `schedule.py:148-150`,
`mapfile.py:246` and `all.py:189` do read `workers`, and nothing reads
`pipeline`. The corrected `pipeline` row names the contrast rather than
rewriting the `workers` row, which is out of contract.

**A recurring job that already has a file.** The build inside step 3 was
`correct-a-documented-claim` end to end — the claim, then its copies, then the
harnesses. Its step 4, `sweep-for-other-copies`, is what turned three of the
thirteen lines from two files into four, eight and nine. No second workflow file
is written; the observation is that a docs PRD dispatched to an implementer
should carry `correct-a-documented-claim`, not `probe-then-spec`.

## Record

`knowledge.py query` returned 90 hits, 88 strong, none about documentation
drift; the query was strong enough that no gap was enqueued into
`.pearde/wiki/pending/`. Nothing was learned outside this repo, so nothing was
written back with `knowledge.py remember`. No word in the contract was missing
from `grammar.py show`.

## Scoring

**complexity 32** — the sum `pearde specced --check` accepts over five specs,
each a claim family already built and swept. The work is wide (25 files) and
shallow: no unit needs a decision, and the largest single edit is one table.

**blast-radius mid** — being wrong here re-plants the exact drift this PRD
removes, in the two pages a person is steered by when setting up a vault or
diagnosing a broken install, and `view.js` carries one real behaviour change
(`⌘8`). Nothing on the board depends on it, which keeps it off `high`.

## Scores

complexity: 32
blast-radius: mid
workflow: probe-then-spec
