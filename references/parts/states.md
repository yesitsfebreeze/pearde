# States

The nine states, what sets each, and what a tenth one means.

| state       | meaning                                   | set by                         | leaves via                                    | command |
|-------------|-------------------------------------------|--------------------------------|------------------------------------------------|---------|
| `open`      | claimable for analysis                    | user / orchestrator            | analyst dispatched → `analyzing`               | `add <title>` · `answer <prd> Q<n> "<text>"` on the last question · `retry <prd>` when no spec stands · `release <prd> open` |
| `analyzing` | analyst working out what to do            | orchestrator                   | analyst returns → `specced` \| `refine` \| `question` | `claim <prd> <worker>` · `sweep --apply` → `open` when silent past `claim-ttl` |
| `refine`    | needs a sub-PRD split or more detail      | orchestrator (analyst verdict) | children created → `open`                      | `release <prd> refine` |
| `question`  | blocked on the user                       | orchestrator (analyst verdict) | answers written → `open`                       | `release <prd> question` — gate: a `## Questions` pass `questions.py check` accepts |
| `specced`   | specs exist, ready to implement           | orchestrator                   | implementer dispatched → `claimed`             | `specced <prd> --blast <x>` — gate: every `specs/*.md` accepted, weight summed · `unblock <prd>` — gate: `needs:` all `done` · `retry <prd>` when the specs stand |
| `claimed`   | implementer working it                    | orchestrator                   | returns → `done` \| `failed`                   | `claim <prd> <worker>` · `sweep --apply` → `failed` when silent past `claim-ttl` |
| `blocked`   | waiting on a named event — open boxes     | orchestrator                   | the event lands → `specced`                     | `release <prd> blocked` — gate: `needs:` |
| `done`      | specs implemented and verified            | orchestrator                   | terminal                                       | `collect <prd>` — gate: every box closed in both files, every `## Verify and Proof` block, the board's `gate:` and every binding invariant green |
| `failed`    | attempt failed — red, the queue the loop drains first | orchestrator / `collect` | `retry <prd>` → `specced` \| `open`            | `release <prd> failed` — gate: `## Failure` · `collect <prd>` on a red verify or a lane whose rebase conflicts — no gate, the output or the files are the reason |

**The command is the gate.** Every `state:` above is written by a command in
the last column — @resources/board/transitions.py, @resources/board/specs.py,
@resources/board/collect.py, `pearde <command>` — which checks its gate,
prints the progress line of @references/parts/progress.md, and exits 1 naming
the gate when the table forbids the move.

`claim` runs `plan.dispatchable`, the one predicate loop steps 4 and 5 and
`scan`'s ready band read, so `scan` offers what `claim` takes: unclaimed; leaf
— every child `done`, a parked child holding its parent
(`leaf: … held by <child> (parked)`, listed under `gated`, never ready);
container — children all `done`, no specs, no open box of its own, which
`collect` closes and `claim` refuses (`container:`); `needs:` all `done`;
`workflow:` resolves.

A footprint overlap is not a `claim` gate; it is the round's hold. Every
worker works in a git worktree of its own, and one lane per file at a time:
`scan`'s ready band offers a PRD only while no lane on its files is in flight,
unmerged, or offered above it — the loser reads `after <prd> (footprint)`
under gated and is offered the moment that lane lands (`compute_plan`'s
`clash`, read by `scan`, `next` and `plan`). Seven lanes dispatched together
on two files were seven conflicts at their collects.

`defer <prd>` writes the parked `deferred` below. `set <prd> <state> --force`
writes any transition and says `forced` on the line — the escape hatch, never
the path. The view's drag calls the same function forced, and its line says
`forced · view`.

`blocked` vs `failed` — whose problem the open box is:

- `failed` — the attempt did not produce the work. A worker that guessed, or
  whose own checks are red, is `failed`. So is a lane `collect` could not
  land — a red verify on the merged tree, or a rebase that conflicts —
  written by `collect` rather than by a worker's verdict, `## Failure`
  naming the slug and its output or the lane branch, the branch it would
  not land on and the files (@references/parts/commits.md). Red is not a
  person's: `retry` puts a worker back on the same lane — `specced` when
  the specs stand, `open` when they do not — and `pearde brief` hands it
  the failure verbatim with the rebase to do (`brief:retry` in
  @references/parts/workers.md). `scan` lists red in its own band, above
  `waiting on you`, and `next` dispatches it before anything open.
- `blocked` — the work is done, and a box it cannot close waits on something
  named. Carries `needs:`, and the body says which boxes are open and what
  closes each. Live work — counted in the progress line and the plan, never
  blindly retried — and never a person's: it waits on OTHER tickets, so
  `scan` lists it under gated with its needs, never under `waiting on you`,
  and `next` prints `pearde unblock` the moment every need is `done`. Only
  `question` waits on you.

Never reach for `blocked` to avoid a hard `failed`.

A `state` outside this table is the user's own and **parked**: never
dispatched, never scheduled by `plan`, out of the progress line and the status
line, not folded into `open`. Report parked PRDs by name — neither progress
nor backlog. A parked child holds its parent, neither done nor coming, so the
parent waits until that child is `done`. `release <prd> open` is the way back,
and the one target: it clears `claim:` and files the PRD as claimable work. A
parked container is `collect`'s, and `release` says so.

**Parked on a person owes a pass.** A parked state, or a `mode:`, naming a
human — `hitl`, `waiting`, `user` — makes `question`'s claim without
`question`'s obligation: the board is stopped and nobody wrote down what is
being asked. Whichever word it uses, it carries `## Questions` in the format
of @references/drill.md, and step 2 of the loop puts it to the user with the
`question` PRDs. `doctor`'s `questions` row is that rule as a check.
