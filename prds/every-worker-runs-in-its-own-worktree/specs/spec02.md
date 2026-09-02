---
complexity: 6
footprint:
  - resources/board/transitions.py
---

# spec02 — claim cuts the lane, sweep drops it

`pearde claim` gives the worker a worktree; `pearde sweep --apply` takes it
back. Nothing else in the state machine touches git.

**What stands** — `cut_lane` and `drop_lane` are in
`resources/board/transitions.py` from the probe. `transition` calls
`cut_lane` on the `claim` edge, before `snapshot_claim`; `cmd_sweep` calls
`drop_lane` after the transition it applies. A git that says no is printed
and the claim still stands — the state machine is not git's to veto.
Measured in a fixture: `pearde claim change-a analyst-1` printed its
ordinary progress line and `git worktree list` showed
`.pearde/.lanes/change-a [lane/change-a]`.

**What is left** —

- `--dry` says nothing about the lane. `transition`'s dry branch already
  lists `.claims/<rel>/` under `would write:`; the lane dir belongs on that
  line, and a dry claim must cut nothing (it currently would not, because
  `cut_lane` sits past the dry return — confirm and keep it that way).
- `sweep --apply` on an `analyzing` claim releases to `open` and calls
  `drop_lane`; on a `claimed` claim it releases to `failed`. The `## Failure`
  text still says "partial code may stand in the tree" for the `failed`
  case — it now stands on `lane/<slug>`, and the text must name the branch
  so a person can find the work the sweep just unmounted.
- `retry` and `release` leave the lane alone by design: an analyst's probe
  survives its verdict there, which is the contract. Say so in the code, so
  the next reader does not add a cleanup.

## Acceptance

- [x] `pearde claim <prd> <worker>` creates a worktree at `<board>/.lanes/<prd>` on branch `lane/<prd>`
- [x] `pearde claim --dry` creates no worktree and names the lane dir under `would write:`
- [x] a claim on a board outside any git repo still moves the state and prints no traceback
- [x] a second claim of the same PRD after a `failed` reuses the lane standing on disk rather than refusing
- [x] `pearde sweep --apply` removes the worktree of every claim it releases and leaves the `lane/` branch
- [x] the `## Failure` a sweep writes names the lane branch the work is on
- [x] `pearde release <prd> refine|question|open` leaves the lane and its uncommitted work on disk

## Verify and Proof

```sh
python3 -c "import ast,sys; t=ast.parse(open('resources/board/transitions.py').read()); \
n={f.name for f in ast.walk(t) if isinstance(f, ast.FunctionDef)}; \
sys.exit(0 if {'cut_lane','drop_lane'} <= n else 1)"
grep -q 'drop_lane' resources/board/transitions.py
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)resources/board/transitions\.py([ ,:]|$)'; then exit 1; fi
```
