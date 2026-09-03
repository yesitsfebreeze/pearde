---
state: blocked
origin: derived
from: resources-are-organised-by-responsibility/the-largest-module-is-cut-by-responsibility
priority: 85
complexity: 3
blast-radius: high
repo: pearde
footprint:
  - resources/board/plan.py
  - resources/board/run.py
workflow: probe-then-spec
needs: a-harness-never-dispatches-the-live-board
---

# the-module-split-dropped-the-merged-read-plan-all-boards-slo

When this is done, every read @references/parts/run.md documents works again:
`plan all`, `plan <group>` and the four windows `plan boards | slots |
progress | groups` print the merged frontier, and `plan` / `plan here` stay
the cwd board's own page.

## The measured regression

`dca5ce2` (2026-09-03 09:51, `the-largest-module-is-cut-by-responsibility`)
split `plan.py` into ten modules and says "every command, caller and harness
unchanged from the outside". The pre-split `plan.py` held `_merged_plan(argv)`
plus `PLAN_WINDOWS = ("boards", "slots", "progress", "groups")` and routed
`cmd == "plan"` through it first:

```python
if cmd == "plan":
    handled, code = _merged_plan(raw[1:])
    if handled:
        sys.exit(code)
```

The split dropped `_merged_plan` and the routing from `plan.py` and landed it
in **no module** — `grep -rl _merged_plan resources/board/` on `80c8d81`
answers nothing. Measured on `80c8d81`, from `/Users/feb/dev/infra/pearde`:

```
$ python3 resources/pearde.py plan all
pearde: no .pearde/ board at all            # rc 2 — "all" parsed as a board arg
$ python3 resources/pearde.py plan slots
pearde: no .pearde/ board at slots
$ python3 resources/pearde.py plan boards
pearde: no .pearde/ board at boards
$ python3 resources/board/run.py run slots
pearde run: `slots` is neither a group nor a PRD here.
```

`run.py` still holds `read_main` and `READ_VERBS = ("boards", "slots",
"progress", "groups")` — the read half is intact, it is only unreachable:
no module imports it for a CLI word. `dispatch.py` imports `run.frontier`
and `run.waves` internally, but nothing routes `plan <window>` there.

## Who depends on it

- @references/parts/run.md lines 12–18 document all five verbs.
- `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` runs
  `python3 "$ROOT/resources/board/plan.py" plan all` in two assertions.
- `a-harness-never-dispatches-the-live-board/specs/spec01.md` asserts
  `plan slots` and `plan all` (its collect is refused by this gap —
  `pearde: no .pearde/ board at slots`).
- `pearde plan --json` is the merged read as data, same routing.

## The fix

Restore the routing the split dropped, with the code that still exists:
`plan.py` regains `_merged_plan` (importing `run.read_main` lazily — the
single-board path must not load it), the `PLAN_WINDOWS` tuple, and the
`if cmd == "plan": handled, code = _merged_plan(raw[1:])` gate ahead of
`find_board`. The body of `read_main` in `run.py` is unchanged — the fix is
the routing, not the reader.

## Constraints

- `plan` with no word and `plan here` never load the merged machinery.
- The five verbs and `--json` exit 0 and print what run.md says, on the
  merged set of watched boards.
- `run.py`'s own `COMMANDS = {"run": cmd_run}` is untouched — moving stays
  `run`, reading stays `plan`.

## Acceptance

- [x] `python3 resources/pearde.py plan all` prints the merged frontier with a `wave 1:` line, exit 0
- [x] `plan boards`, `plan slots`, `plan progress`, `plan groups` each print, exit 0
- [x] `plan --json` emits the merged payload with `waves` and `slots`
- [x] `plan` with no word and `plan here` print the cwd board's own page, and `run` is absent from `sys.modules` after both
- [x] `the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh` is green on a tree holding this fix
- [ ] `a-harness-never-dispatches-the-live-board` collects

## Pointers

- `git show dca5ce2~1:resources/board/plan.py` — `_merged_plan`, `PLAN_WINDOWS`, and the two-line routing to restore
- `resources/board/run.py:792` — `read_main`, unchanged
- @references/parts/run.md — the contract the five verbs are documented under

## Blocked

- Box `- [ ] \`a-harness-never-dispatches-the-live-board\` collects` waits on
  the collect of `a-harness-never-dispatches-the-live-board`, whose
  `spec01` verify is red on its own scope on the current main:
  `python3 resources/board/run.py all` dispatches instead of refusing the
  bare scope (measured 2026-09-03 21:29 — it printed nothing and ran past
  two minutes; killed before it could launch). Lines 1–4 of that same
  verify (plan slots / plan all / plan progress / read_main grep) are green
  in this PRD's lane — the half this PRD owns. What closes the box is that
  PRD's own fix landing; its worker holds the claim (impl-harness-nodispatch2
  since 21:03). This PRD's five code boxes stand verified on the lane
  (probe/verify.sh 11/11 under PEARDE_ROOT=<lane>).
