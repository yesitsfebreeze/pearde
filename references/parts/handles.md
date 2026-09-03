# Handles

Every command the board answers to.

The spelling follows the setup — `/pearde status` where commands take
arguments, "pearde status" in plain chat. The meanings are fixed.

**Several of these are also skills of their own**, invocable without the
board in front of them: `pearde-drill`, `pearde-memo`, `pearde-view`,
`pearde-report`, `pearde-master`, `pearde-doctor`, `pearde-persona`,
`pearde-persona-ask`, `pearde-persona-create`, `pearde-scout`, `pearde-workflow`, `pearde-grammar`, `pearde-health`. Typed inside a pass they are the
short handles below and behave exactly as this table says. Typed cold they
are the same feature with no pass around it — `@@skills` is the list, and
each skill file says what it does with no board in scope.

| Want                         | Say                                                                                                      | Command |
|------------------------------|-----------------------------------------------------------------------------------------------------------|---------|
| report only, change nothing  | `status` — `@resources/board/plan.py scan` plus the progress line. Changes nothing, reads no file the scan already read | `pearde status` |
| is the machine tooled for this repo? | `ramp` — `@resources/board/ramp.py`: `happiness:` non-zero prints one line, zero prints the gap and writes the forks to `.pearde/.state/ask.md`. Loop step 0, once per board. `have`, `need`, `gap` and `find <job>` answer on their own; `happy <n>` is a person's word, per @references/parts/ramp.md | `pearde ramp` |
| the board as one page        | `scan` — `@resources/board/plan.py scan`: counts, progress terms, collect, in flight, waiting on you, ready, gated. Loop step 1, run on its own | `pearde scan` |
| which step the pass is on   | `next` — `@resources/board/plan.py next`: the loop step, the decision it owes and the exact command, one call after `scan`. Reads and writes nothing | `pearde next` |
| one pass, then stop         | `once`                                                                                                   | — |
| cap the implementers         | `workers=5` — a cap, written to `.pearde/settings.md`, persists; `workers=0` lifts it, and unlimited is the default | — |
| cap the analysts             | `pipeline=5` — a cap, written to `.pearde/settings.md`, persists; `pipeline=0` lifts it, and unlimited is the default | — |
| new PRD                      | `add <title>` — dir + `prd.md` from `@references/templates/prd.md`, `state: open`, `origin: requested`. Runs as printed: with no `--as` and no `PEARDE_AS` it files the PRD `· as engineer (default)`, the one transition that does — a new PRD has no earlier line to rewrite | `pearde add [--dry]` |
| park a derived PRD           | `defer <prd>` — `state: deferred`, per @references/parts/derived.md; `release <prd> open` is its inverse, the one way back from any parked state | `pearde defer [--dry]` |
| work out what is wanted      | `drill <prd>` — interview per `@references/drill.md`. With no `<prd>`: the board's own open frontier where there is one, else a new tree | — |
| retry a failed PRD           | `retry <prd>` — moves `## Failure` into the body as history, sets `open`                                 | `pearde retry [--dry]` |
| a blocked PRD's event landed | `unblock <prd>` — re-runs only the open boxes; `done` when they close                                    | `pearde unblock [--dry]` |
| close what is finished       | `collect` — every PRD whose acceptance boxes are all `[x]`: verify, commit, `done`. Loop step 6, run on its own | `pearde collect [--dry]` |
| run one PRD to done          | `run <prd>` — the loop scoped to that PRD's subtree                                                      | — |
| the state, for a person      | `report` — rewrites `.pearde/report.md` whole: planned, in work, undecided or failing, in plain words per `@@report` | — |
| record a decision            | `memo <subject>` — `.pearde/memos/<slug>.md` from `@references/templates/memo.md`                            | `pearde memo add <subject>` |
| the workflow library         | `workflow` — `@resources/workflows.py list`: slug · kind · runs · updated · subject, per `@@workflows` | `pearde workflow list` |
| one, as a worker sees it     | `workflow <slug>` — `@resources/workflows.py brief`: the `## Use when`, then every step with its atomic inlined. `show` when the slug is an atomic — an atomic is shown, not briefed, and `brief` exits 1 on one | `pearde workflow brief <slug>` |
| a new atomic                 | `workflow add atomic <subject>` — a file from `@references/templates/atomic.md`, slugged as a memo is, at `runs: 0`. An orchestrator write, and only from a job that recurred | — |
| a new workflow               | `workflow add <subject>` — a file from `@references/templates/workflow.md`; every atomic a step names exists first, or the step sends a worker nowhere | — |
| attach a workflow to a PRD   | `workflow attach <prd> <slug>` — writes `workflow:` on that `prd.md`. An orchestrator write; the drill writes it on the tree it produces | — |
| check the library            | `workflow check` — `@resources/workflows.py check`: one problem per line, silent when clean. The `doctor` row alone | `pearde workflow check` |
| the board's vocabulary       | `grammar` — `@resources/grammar.py list`: term · group · meaning, per `@@grammar` | `pearde grammar list` |
| one word, as a worker asks it| `grammar <term>` — `@resources/grammar.py show`: one term and its collision row where the word carries two meanings | `pearde grammar show <term>` |
| a word that was just coined  | `grammar add <term> <meaning>` — appends the row under `--group <g>`, default the file's last group, and moves `updated:`. An orchestrator write, on the transition that introduced the word | `pearde grammar add` |
| check the vocabulary         | `grammar check` — `@resources/grammar.py check`: one problem per line, silent when clean. The `doctor` row alone | `pearde grammar check` |
| words with no row            | `grammar undefined` — `@resources/grammar.py undefined`: every `@@` scope, PRD and spec frontmatter key and `settings.md` key no row defines, with where it is used. Reads keys and scopes, so a word reintroduced in prose alone is not caught. A judgement, in no check | `pearde grammar undefined` |
| which files resist the work  | `health` — `@resources/health.py list`: every file under `health-floor`, worst first, score and what pulls it down, off the ranking. `--under <n>` moves the line, a path narrows it, per `@@health` | `pearde health list` |
| score the tree               | `health score [path...]` — `@resources/health.py score`: one note per tracked file under `.pearde/health/files/` and `ranking.md` worst first, from the tree and the graph. Whole, or for these paths with the ranking rebuilt from every note. An orchestrator write, regenerable | `pearde health score` |
| one file, and why            | `health show <path>` — `@resources/health.py show`: the note — the raw measures, the two axes that pull it down, its callers and calls | `pearde health show <path>` |
| check the record             | `health check` — `@resources/health.py check`: one problem per line, silent when clean; `stale` lines fail nothing. The `doctor` row alone | `pearde health check` |
| who is working               | `persona` — the active one and why; `persona <id>` switches, for this session only: `export PEARDE_AS=<id>`, the variable every command reads, exported as `engineer` by the install line. Stored on no board file | — |
| one persona's read on one problem | `ask <id> <question>` — calls that persona, pointed at this session for context, and talks to it until the question is settled. It answers and writes nothing; the session keeps its own persona. The board calls one on its own judgment too, unasked | — |
| a persona for a new field    | `persona create <topic>` — research the field and its real practitioners, compose one from the best of them, per `@@personas` | — |
| pre-plan the dispatch order  | `plan` — `@resources/board/plan.py plan`; print the frontier and queue it returns                                       | `pearde plan` |
| the local timeline           | `gantt` — `@resources/board/plan.py gantt --open`: the plan as `.pearde/.state/view.html`, x = distance to the vision | `pearde gantt --open` |
| weight in real hours         | `calibrate` — `@resources/board/plan.py calibrate`: fit hours-per-weight from every done PRD with an `actual:` across every registered board; the view prints real hours from it | `pearde calibrate` |
| open the board               | `view` — `@resources/board/serve.py ensure`, then the URL it prints                                          | `pearde view` |
| plan across projects         | `master <path> …` — writes `members:` in `.pearde/settings.md`, asks the group's `name:` the first time. This board is then the parent every pass works in | — |
| what a master merges         | `master` with no path — `@resources/board/plan.py members`: every member, its path, `MISSING` when not on disk | `pearde members` |
| re-order after anything moved| `reconcile` — `@resources/board/plan.py reconcile`: schedule recomputed, anchor kept. The live service already does it, on every board | `pearde reconcile` |
| is this thing wired?         | `doctor` — `@resources/doctor.sh --fix`, per @@doctor; print every line | `pearde doctor --fix` |
| take a PRD for a worker      | `claim` | `pearde claim [--dry]` |
| hand a PRD back with a state | `release` | `pearde release [--dry]` |
| answer a question on a PRD   | `answer` | `pearde answer [--dry]` |
| force any transition         | `set` | `pearde set [--dry]` |
| validate the specs, sum the weight| `specced` | `pearde specced [--dry]` |
| children from the analyst's split| `refine` | `pearde refine [--dry]` |
| print a worker's brief       | `brief <prd> [--role <role>] [--as <id>] [--force]` — `@resources/board/brief.py`: header line, persona line, workflow block, the role's brief from `@references/parts/workers.md` with the placeholders filled; the role follows the state, `--role` overrides. `brief --consult <id> --question "<q>" [--transcript <path>]` is the consultant's | `pearde brief` |
| sweep the stale claims       | `sweep [--apply]` — every claim silent past `claim-ttl` (@references/settings.md), one line each with what `--apply` does: `analyzing → open`, `claimed → failed` with `## Failure` written; never a claim `.pearde/.state/pass.md` names, never an analyst whose specs are on disk. Loop step 1, once per session | `pearde sweep [--dry]` |
| a worktree per run session   | `session take/list/reap/owns` — `@resources/board/session.py`: `take` cuts `.pearde/.sessions/<id>` on `session/<id>` and writes the ledger at `.pearde/.state/sessions.json`; `list` prints who holds which tree and whether that holder is alive; `reap [--apply]` commits everything a dead session left, untracked files included, to `refs/pearde/reaped/<id>` before it removes the tree, and touches neither a live session, nor one whose liveness cannot be decided, nor this one; `owns <path>` exits 0 when the running session holds that path. Both writers run before step 0 | `pearde session <verb>` |
| what a destructive git may do here | `refuse tree/cmd` — `@resources/board/refuse.py`: `tree [<path>]` prints who owns that worktree and whether this session may discard in it; `cmd '<shell line>'` reads every `git` in the line — `reset --hard`, `checkout --`, `clean`, a real `stash`, `restore`, `switch --discard-changes` — and refuses each one aimed at a tree this session does not own, naming the tree, the holder and the memo. Exit 0 allowed, 3 refused, `--json` for either. The same module answers `@resources/guard.py`'s `PreToolUse` hook and the board's own call sites | `pearde refuse <verb>` |
| one copy of what every lane rebuilds | `share` — `@resources/board/shared.py`: the regenerable dirs (node_modules, the graphify cache, the Obsidian bundles) held once under the git common dir and symlinked into the checkout and every lane. `apply` links them and seeds the store from the first copy it finds, `undo` puts real directories back. Only a path `git status` cannot see is ever linked; `claim` runs it on each new lane | `pearde share [apply|undo]` |
| a board, registered and planned| `init` | `pearde init [--dry]` |
| the board's settings         | `settings` | `pearde settings [--dry]` |
| the vision and its axis      | `vision` | `pearde vision` |

The Command column is the line @resources/pearde.py answers. A `—` is a
handle the pass answers by hand, with no command behind it. `[--dry]` marks
a command that writes: with it, the command prints the line the real run
would print, `dry ·` in front, then `would write:` and every path, and
writes nothing. A flag a command does not declare is refused before the
board is read — `unknown flag --dyr — release takes: --as, --board, --dry`,
exit 2 — and `pearde <cmd> --help` prints that same list.

- `add` is the user asking, so `origin: requested`. Only the orchestrator
  writes `origin: derived`, and only with `from:` — @references/parts/derived.md
  says what must be true before it is filed `open` rather than `deferred`.
- `collect` changes nothing about the gate: a PRD with an open box, or with no
  verify output on record, is verified first and `failed` if the tree is red —
  a board whose finished work is not closed schedules around it.
- `master <path>` takes one or more paths, each a board or a repo holding one,
  and appends them to `members:`. It creates nothing in the member and moves
  no file. Print what the merged board now holds: member count, PRD count, the
  plan `reconcile` produced.
- `report` is the only document on the board a person is the reader of. It is
  one state and never a log: the file is rewritten whole, and no PRD name,
  board state or weight survives into it.
- `memo <subject>` slugs the subject — lowercase, spaces to hyphens. The slug
  is both the filename and the `memo:` key, and `doctor` fails if they
  disagree. Write the memo when the call is made, not when the work lands.
- `persona <id>` and `ask <id>` are the switch and the question. Switch when
  the whole pass wants a different reading. Ask when one problem does.
  Neither writes a board file — the switch is `export PEARDE_AS=<id>` per
  `@@personas`, or `--as <id>` on a line that runs in a fresh shell; the call
  is `@@consult`; and the pass's `· as <id>` is the only record on the board
  either leaves.
- `ask` is a handle, not a permission. The board reaches a persona on its own
  judgment mid-pass — before `done`, on a naming call, on a report it cannot
  check from inside its own frame — and says who it asked and what came back.
  Typing `ask` is how you start that conversation rather than waiting for it.
- `add` takes the title as written. A one-line title is too thin to spec, so
  the analyst returns REFINE or QUESTION. `drill` settles it first — it runs
  @references/drill.md to completion and leaves a tree the loop picks up:
  settled contract as the body, each branch a child dir, `state: open`.
  Dispatch nothing while a drill is running.

`run <prd>` filters the board to that PRD and its children:

- Scan still parses everything, for the sweep and the progress line, but only
  PRDs inside `.pearde/prds/<prd>/` change state.
- The user named it, so a `failed` target or child is reopened first, as
  `retry` would.
- A `done` target is reported and left alone. No match: list the near-misses,
  change nothing.
- The run ends when the subtree is drained — report the target's final state —
  or everything left in it is blocked on the user.

One writer per file, sequenced between sessions. On start, fresh `analyzing`
/ `claimed` claims you did not make may be another session's live workers:
say so and run `status` only. `sweep` lists them and `--apply` leaves any
claim `.pearde/.state/pass.md` names.
