Verdict: SPECCED

# the-module-split-dropped-the-merged-read-plan-all-boards-slo — an-merged-read, engineer

## Build

Restored the dropped routing in the lane
`.pearde/.lanes/the-module-split-dropped-the-merged-read-plan-all-boards-slo`,
uncommitted, from the pre-split source (`dca5ce2~1`):

- `resources/board/plan.py` — `PLAN_WINDOWS` and `_merged_plan` back ahead of
  `main()`, importing `run.read_main` lazily; the `if cmd == "plan":` gate
  restored ahead of `find_board`, with the `here` strip.
- `resources/board/run.py` — **untouched.** `read_main`'s body needed
  nothing; `COMMANDS = {"run": cmd_run}` stands. The PRD's footprint named it
  as a ceiling, not a change.

## Verify

`prds/the-module-split-dropped-the-merged-read-plan-all-boards-slo/probe/verify.sh`,
new this pass: **11/11 ok** against the lane, **FAIL on the unfixed checkout**
(so it can fail). Covers every acceptance box except the sibling collect:
`plan all` with `wave 1:`, the four windows, `--json` (`waves`+`slots`),
bare `plan` and `plan here` printing the cwd page with `run` absent from
`sys.modules`, and `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh`
**PASS** (10 ok + sibling 33/33) under `PEARDE_ROOT=<lane>`.

`a-harness-never-dispatches-the-live-board` **does not collect yet**, measured:
`pearde collect a-harness-never-dispatches-the-live-board` → `spec01 exit 1 —
nothing written … pearde: no .pearde/ board at slots`. It collects on the repo
checkout, which does not hold a lane's edit — this PRD landing is what closes
its box. That ordering is the PRD's reason to exist; not a question.

## Specs

- `specs/spec01.md` — the merged read is routed again. complexity 3,
  footprint `resources/board/plan.py`. Says what already stands (the two
  hunks, verified) and what is left (land, then the two dependent holds).

Union of footprints: `resources/board/plan.py`.

## Scores

complexity: 8
blast-radius: high
workflow: probe-then-spec

complexity — the PRD's own 8 stands: the change is two hunks, but it is the
read path of every board on the machine and three harnesses route through it,
which is where the cost of getting it wrong lives. blast-radius high — five
documented verbs and every harness read (`plan all`, `plan slots`) break
loudly if the gate is wrong again; the fix itself touches one file.

## Findings

1. **The fix already exists on the board, specced under a different PRD.**
   `a-harness-never-dispatches-the-live-board/specs/spec01.md` carries the
   same restoration ("restored from 60f49d1 and adapted to the split module")
   built in another lane, plus a second half this PRD does not ask for (the
   bare-word refusal in `run.py`). Its collect was refused by exactly the gap
   this PRD names — the two are ordered, not duplicates: this PRD lands
   first, the sibling's collect then closes. A job recurred across two PRDs;
   named here once, no second file written.
2. **The collect I ran left the repo checkout damaged.** Output ended
   `NOT put back in /Users/feb/dev/infra/pearde — restore by hand:` naming six
   `docs/node_modules/zod/**` files, and all six are now missing from the
   worktree; `index.md` and `references/parts/handles.md` are staged that were
   not before. That is the `a-collect-stages-a-deleted-footprint-path-as-a-deletion`
   defect, already on the board with a worker on it — defect outside this
   footprint, not fixed here. Whoever collects next may hit it again.
3. No knowledge gap: the record answered 112 hits on the contract, nothing
   enqueued worth asking. No question — the build hit no fork.

Probe left in the tree uncommitted: the lane's `plan.py` hunks and
`probe/verify.sh` under this PRD's directory.