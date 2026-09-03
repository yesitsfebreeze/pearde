---
complexity: 3
footprint:
  - resources/board/plan.py
---

# spec01 — the merged read is routed again

`dca5ce2` split `plan.py` by responsibility and dropped `_merged_plan` plus
its `if cmd == "plan"` gate on no module: `read_main` in `run.py` kept every
window it computes and lost its only caller, so `plan all`, `plan <group>`
and the four windows `plan boards | slots | progress | groups` resolved the
word as a board path (`pearde: no .pearde/ board at all`) and `plan here`
died the same way. This unit restores the routing with the code that still
exists — the reader in `run.py` is untouched, and `run.py`'s `COMMANDS`
stays `{"run": cmd_run}`: moving stays `run`, reading stays `plan`.

**Already stands**, built and verified in the lane
`.pearde/.lanes/the-module-split-dropped-the-merged-read-plan-all-boards-slo`,
uncommitted: `PLAN_WINDOWS` and `_merged_plan` back in `plan.py` ahead of
`main()`, restoring `run.read_main` lazily so the single-board path never
loads it, and the two-line gate in `main()` ahead of `find_board` with the
`here` strip. Nothing in `run.py` changed. `probe/verify.sh` next to this
spec is green 11/11 against the lane and red on the unfixed checkout.

**Left:** land the lane (collect), then the two dependent holds close on the
repo checkout — the machine-frontier harness and the sibling's collect below.

## Acceptance

- [x] `python3 resources/pearde.py plan all` prints the merged frontier with a `wave 1:` line, exit 0
- [x] `plan boards`, `plan slots`, `plan progress`, `plan groups` each print, exit 0
- [x] `plan --json` emits the merged payload with `waves` and `slots`
- [x] `plan` with no word and `plan here` print the cwd board's own page, and `run` is absent from `sys.modules` after both
- [x] `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` is green on a tree holding this fix
- [ ] `a-harness-never-dispatches-the-live-board` collects

## Verify and Proof

```sh
PEARDE_ROOT="$(git -C . rev-parse --show-toplevel)" \
  bash .pearde/prds/the-module-split-dropped-the-merged-read-plan-all-boards-slo/probe/verify.sh
# PASS — 11 rows: the five verbs, --json, the two single-board pages, the
# sys.modules guard, and the machine-frontier harness. The last acceptance
# box is `pearde collect a-harness-never-dispatches-the-live-board` after
# this PRD lands: measured 2026-09-03 on the unfixed checkout it refuses
# with `pearde: no .pearde/ board at slots` — the deadlock this PRD breaks.
```