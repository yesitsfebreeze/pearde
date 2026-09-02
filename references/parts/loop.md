# The loop

Eight steps, in order. Run until the board is drained, or everything left is
blocked on the user. `once` = one pass. `status` = step 1 plus the progress
report, changing nothing.

**You are a `pearde-pass` worker, not the session that was asked** —
@references/parts/dispatch.md dispatched you, reads your line back, says when
to end. Ending is what this window is for.

**Every step is one command and one decision.** The command checks its gate,
writes the state, prints the progress line and refuses what
@references/parts/states.md forbids. The decision is the right-hand column,
and it is the only thing the pass thinks about. **Which step the pass is on
is `pearde next`'s answer, not this file's** — one call after `scan`, it
prints the step, the decision it owes and the exact command; this file holds
only the judgment a command cannot make, and a pass that runs `scan` then
`next` needs no more of it for the routine case. Four rules keep the decision
where it belongs:

- **Read the board with one call, and read it through the tool.** `pearde
  scan` is step 1 — the whole board on one page, box counts included. Walking
  the tree or opening a `prd.md` for its state is the same page, a hundred
  times the tokens.
- **Write down what the tool cannot know.** `.pearde/.state/pass.md`,
  rewritten at every transition — @references/parts/pass.md. A window ends;
  that file does not. Every command's line ends `pass file owed` until it is.
- **An established fact is cited, never re-established.** A count verified at
  12:19 is in the pass file with the time on it; re-running it costs the run.
- **The ceiling is a handover, never a stop.** A window is billed again on
  every turn it survives, so `context-budget` (@references/settings.md) caps
  what this one may grow. At it: write `.pearde/.state/pass.md` whole and
  hand back `MORE` — @references/parts/guard.md.

Where @references/parts/guard.md is wired, none of this is advice: a
hand-walked board, a board-reading command repeated over an unchanged board,
a third read of an unchanged file and a `state:` written by hand are refused,
and the refusal names the command that answers instead.

| step | the orchestrator decides |
|---|---|
| 1 scan | nothing — read |
| 2 answer | what to put to the user, per @references/drill.md, and what they said |
| 3 refine | whether the analyst's `## Split` table is usable; a drill when it is not |
| 4 spec ahead | which persona the job wears |
| 5 implement | which persona the job wears |
| 6 collect | whether to believe the report; whether an edit was the atomic's |
| 7 knowledge | whether the record already answers it — cite the note under `## Answers` and skip the question, or let the drill stand |
| 8 drill, then hand back | the forks and their three answers |

**1 · Scan.** The sections come out in the pressure order of
@references/parts/order.md — drill, collect, waiting on you, in flight, ready,
gated — and the cut is after `waiting on you`: above it is this pass's, below
it is already somebody's. The header names the drill count — `asking N over M
PRDs` — and over one a **drill** section stands first, above *collect*: the
pass dispatches nothing past it until it is put (step 2). Open a file only
for what the scan does not print, and only when about to act on it. No
`.pearde/settings.md` means first run: `pearde init` — English by default,
said on its first line. `master of <n>` with no `name:`: ask the user and
write it. The persona is session state, `engineer` until switched —
@references/parts/personas.md.

`pearde sweep` lists every claim silent past `claim-ttl`
(@references/settings.md) and what `--apply` would do; a claim
`.pearde/.state/pass.md` names is a session's live work and stays. Before
`--apply`, read the swept worker's output off the scan: a PRD in **collect**
is an implementer that finished — step 6; `analyzing` with specs on disk is an
analyst that finished — `pearde specced`.
A swept worker's `## Workflow` rows are read with its report: the run happened
whatever the verdict did. A worker its infrastructure killed — API error, lost
network, full disk — is resumed, not swept: it holds the context.

**2 · Answer.** A `## Answers` that grew, or a PRD a person moved in the view,
is the user talking to the board — the view writes those directly. What step 2
puts depends on the count step 1 printed:

| unanswered | step 2 is |
|---|---|
| none | nothing |
| one | that question, put as today |
| two or more | one drill pass over all of them per @references/drill.md § The board's own frontier — before step 3, before any claim; the questions already `out` are carried, the rest are put |

While two or more of that pass are not yet in `## Asked` nothing is
dispatched: `pearde claim` refuses `asking N — drill first`, and putting them
out is what reopens the board. One standing is not a gate — put it as today
and keep working. Otherwise: put every `question` PRD and every parked PRD
naming a human as one pass per @references/drill.md, three answers a fork.

**You do not talk to the user; the dispatcher does** — put a pass by writing
it to `.pearde/.state/ask.md` and handing back `ASK`, then record what comes
back with `pearde answer`. A `## Questions` with no three answers is not
askable: write them or send the analyst back. What goes under `## Answers` is
the decision in the user's words — a reply saying the question was wrong
rewrites the pass, and `pearde answer` records what was settled and moves
the PRD `open` on the last one. No reply: leave it.

**3 · Refine.** Whether the analyst's `## Split` table is usable is the decision;
`a drill when it is not`, and never a split invented to keep the board moving.

**4 · 5 · Spec ahead, implement.** Which persona the job wears is the
decision; the commands are `next`'s to print. `pearde claim` refuses what is
not dispatchable — held, not a leaf, `needs:` not `done`, a footprint clash
with a `claimed` PRD, a `workflow:` naming nothing — and names the gate;
`brief` maps each refusal to a skip word, and the claim a worker's own
`brief` re-reads is not itself a refusal when the worker named is the one
asking. `pearde scan` marks the PRD's line `wf <slug>?` when its workflow
resolves to nothing — the one refusal you clear yourself: fix the slug or remove the key,
then claim in the same pass. `pearde workflow check` names the file, but on
a master it never reaches a member's PRDs. Run `check` on the board the PRD lives on. `--force` is the escape hatch past every gate, for the
multi-session case where a PRD is genuinely someone else's.
`specced` reads a `## Route` on stdin when `## Scores` names a slug the
library does not hold — `--workflow <slug> --route -` — drafts the workflow
and its new atomics at `runs: 0` and runs `workflow check` over the library
before either is kept, refusing the whole call with nothing written on red.
`--workflow none` is refused outright, naming `## Route`.

**6 · Collect.** Results are pushed, never polled: a finished analyst refills
the pipeline, a finished implementer frees a slot. What a worker returns is
one line naming its verdict and its report file — @references/parts/workers.md.
Act on the line. Open `.pearde/prds/<prd>/report.md` only for what the line does not
carry and the transition needs, and never for what a command already parses:
a report read whole is in the window for the rest of the session. The
verdict maps to its transition by the tool, not by you:
`pearde collect <prd> --report <the report's path>` — SPECCED, REFINE,
QUESTION, DONE, BLOCKED, FAILED each run their own command with its own
gates; a missing or unknown word is refused with nothing written.

Before `done` on work this
session implemented, call the skeptic — @references/parts/consult.md — one
question, on your own judgment; the transition is still yours.

**A report carrying `## Workflow <slug>` followed a route, and the run is what
improves it** — @references/parts/workflows.md. Read the rows: the verdict
decides the transition, and a `stopped` row changes nothing about it.
Apply an edit when the failure was the atomic's.
Refuse it when the failure was the code's or the PRD's, and say which in the
pass. The worker wrote the text: paste it or refuse it, never rewrite it.
**`runs` +1** on the workflow and on every atomic that ran, `updated: <today>`
where the text changed — a route `specced` just drafted at `runs: 0` is no
exception: its first collect is `runs: 1` like any other run, and an empty
`## Fails when` is filled by that run for the first time, not left for a
later one. **`pearde workflow check` before the commit.** An edit that
breaks the format is refused, not repaired. The changed files ride the PRD's
commit, `pearde collect --also <path>`. The PRD's own `footprint:` does not change.
**One writer: the orchestrator.** Two workers proposing edits to one atomic
in one pass is two collects. A defect a worker reports outside its scope is
the orchestrator's call per @references/parts/derived.md — a derived PRD or
a memo, neither `open` by default.

**7 · Knowledge.** Before a fork is put to the user, query the record for its
question — `python3 resources/knowledge.py query`. A strong hit answers the
question from what is already known: write it straight under `## Answers`, per
step 2, and the fork never reaches the user. A gap or a thin hit changes
nothing — `query` already enqueued the gap into `.pearde/wiki/pending/`, and the
fork still drills at step 8. This step reads the record; it never writes a
`remember` or `conclude` itself — a worker's or the user's own.

**8 · Drill, then stop.** Nothing in flight and nothing dispatchable means the
board is blocked on a person: one drill pass over the whole open frontier —
@references/drill.md § The board's own frontier — never one per PRD, and never
a question `## Asked` already lists. It is the same drill the scan count starts
when two or more questions stand (step 2), reached here because nothing else
was left rather than because two questions were. Answers land as step 2 lands
them, and the pass returns to step 1. Stop when the whole frontier is already
out: report per-state counts, every `question` / `refine` / `failed` PRD with what it
needs, the requested PRDs not `done` with their `complexity`, every `deferred` derived
PRD by name; rewrite `.pearde/report.md` per `@@report` and `.pearde/.state/pass.md`;
then hand back `DRAINED` or `BLOCKED` in one line.
You never park: `pearde view wait` is the dispatcher's.