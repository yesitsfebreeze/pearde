---
state: open        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived     # requested = the user asked | derived = the board found it
from: the-guard-finds-the-board-the-way-the-scan-does
# from-was:            # derived only — the PRD whose work surfaced this one
priority: 88        # higher first
complexity: 0      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual:          # a record. Nothing reads it
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in prds/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# Collect commits the code repo, not the board repo twice

`collect.py` `repo_of()` returns the board's own git repo whenever a PRD
carries no `repo:` key — correct while the board lived at `prds/` *inside*
the code repo, wrong since it moved to `.pearde/`, which is a git repo of its
own nested in this one. The whole footprint is then sorted into the board
repo's group, where none of those paths is ever dirty, so every one of them
is silently dropped: not added, not reported as `inherited`, not raised as a
`stop`. `collect` prints a commit, writes `done`, and the code is still
uncommitted in the working tree.

Measured, not inferred, on `the-guard-finds-the-board-the-way-the-scan-does`
this round: spec01's `footprint:` is `resources/guard.py`; collect printed
`commit 259eaaa · inherited 19 · record 09feb0c`, both commits landed in
`.pearde`, and `resources/guard.py` was still `M` in the code repo
afterwards. It was committed by hand as `0894d51`. The path through the code
is `repo_of` (line ~199) → `sort_paths` (line ~711) `groups.setdefault(repo,
…)` → the per-root loop over `dirty_paths(root)`, which can only see paths
that exist under that root.

What it must do: with no `repo:` key, the default repo is the repo enclosing
the board directory when the board is its own repo — `repo_root` of the
board repo's parent — and the board's own repo otherwise, so a board that
still lives inside its code repo behaves exactly as it does today. A
footprint path that belongs to no group must be refused loudly rather than
dropped; a footprint the collect cannot place is a collect that must not
write `done`.

Every board on this machine is on the `.pearde/` layout, so every collect
since the move is suspect: part of the work is saying which PRDs were
collected with a footprint that never reached a commit, and listing them for
a person to re-commit. The nine boards' `done` PRDs are the search space.

| `collect-defaults-to-the-boards-enclosing-repo` | repo_of()` defaults to the repo enclosing a nested `.pearde` board (not the board's own repo), refuses loudly when a footprint matches no repo, and is unchanged when the board is not its own repo — each proven by fixture | — |
| `list-the-collects-the-repo-bug-orphaned` | every already-`done` PRD on this machine's boards whose footprint never reached a commit under the old bug is found and listed for a person to re-commit | collect-defaults-to-the-boards-enclosing-repo |

## Acceptance sketch, for the analyst

- a PRD with no `repo:`, a board at `.pearde/`, and a footprint in the code
  repo: `collect` commits that footprint in the code repo
- a board that is not its own repo: unchanged behaviour, proven by a fixture
- a footprint path under no group's root: `collect` refuses and writes no
  state
- the list of already-collected PRDs whose footprint never landed
