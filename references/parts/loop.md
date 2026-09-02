# The loop

Step 0, then eight steps, in order. Run until the board is drained, or
everything left is blocked on the user. `once` = one pass. `status` = step 1
plus the progress report, changing nothing.

**You are a `pearde-pass` worker, not the session that was asked** —
@references/parts/dispatch.md dispatched you, reads your line back, says when
to end. Ending is what this window is for.

**Every step is one command and one decision.** The command checks its gate,
writes the state, prints the progress line and refuses what
@references/parts/states.md forbids. The decision is the right-hand column,
the only thing the pass thinks about. **Which step the pass is on is
`pearde next`'s answer, not this file's** — one call after `scan`, it prints
the step, the decision owed and the exact command. This file holds only the
judgment a command cannot make, so a pass running `scan` then `next` needs no
more of it in the routine case. Four rules keep the decision where it
belongs:

- **Read the board with one call, and read it through the tool.** `pearde
  scan` is step 1 — the whole board on one page, box counts included. Walking
  the tree or opening a `prd.md` for its state buys the same page at a hundred
  times the tokens.
- **Write down what the tool cannot know.** `.pearde/.state/pass.md`,
  rewritten at every transition — @references/parts/pass.md. A window ends;
  that file does not. Every command's line ends `pass file owed` until the
  rewrite lands.
- **An established fact is cited, never re-established.** A count verified at
  12:19 is in the pass file with the time on it; re-running it costs the run.
- **The ceiling is a handover, never a stop.** A window is billed again on
  every turn it survives, so `context-budget` (@references/settings.md) caps
  what this one may grow. At it: write `.pearde/.state/pass.md` whole and
  hand back `MORE` — @references/parts/guard.md.

Where @references/parts/guard.md is wired, none of these rules is advice: a
hand-walked board, a board-reading command repeated over an unchanged board,
a third read of an unchanged file and a `state:` written by hand are refused,
and the refusal names the command that answers instead.

| step | the orchestrator decides |
|---|---|
| 0 ramp | nothing — one line, unless the gap is the user's |
| 1 scan | nothing — read |
| 2 answer | what to put to the user, per @references/drill.md, and what they said |
| 3 refine | whether the analyst's `## Split` table is usable; a drill when it is not |
| 4 spec ahead | which persona the job wears |
| 5 implement | which persona the job wears |
| 6 collect | whether to believe the report; whether an edit was the atomic's |
| 7 knowledge | whether the record already answers it — cite the note under `## Answers` and skip the question, or let the drill stand |
| 8 drill, then hand back | the forks and their three answers |

**Before step 0 · The session takes a tree of its own.** Every pass runs
`pearde session reap --apply`, then `pearde session take`. The reap is first,
and safe beside live work: a live session's worktree is never reaped, nor one
whose liveness cannot be decided, nor this session's own, and a dead session's
tree goes only once everything it left — untracked files included — is
committed to `refs/pearde/reaped/<id>`. `take` is idempotent. From it onward the taken tree **is** the code repo:
every board command resolves it, a claim cuts the lane off `session/<id>`, and
a collect merges and commits there. Each collect then puts that branch on the
branch the checkout is on — a rebase, then a fast-forward, `landed on
<branch>` on the transition line. A checkout holding uncommitted work refuses
the fast-forward and the line names the refusal instead. Nothing is lost when
it does: the commit stands on `session/<id>`, and `pearde session land`
retries it once the checkout is clean — @resources/board/session.py.

**0 · Ramp.** `pearde ramp` — once per board, not per pass. `happiness:`
non-zero (@references/settings.md) is a person saying the machine is tooled for
this repo, and the step is one line. Zero is the gate: the gap between the
tree's asks and the install goes to `.pearde/.state/ask.md`, one fork per job
with candidates and their `npx skills add` lines, and the pass hands back `ASK`
before it scans. The board installs nothing — @references/parts/ramp.md.

**1 · Scan.** The sections come out in the pressure order of
@references/parts/order.md — drill, collect, waiting on you, in flight, ready,
gated — and the cut falls after `waiting on you`: above, this pass's; below,
somebody's. The header names the drill count — `asking N over M PRDs` — and
over one a **drill** section stands first, above *collect*: the pass
dispatches nothing past it until the drill is put (step 2). Open a file only
for what the scan does not print, and only to act on it. No
`.pearde/settings.md` means first run: `pearde init` — English by default,
said on its first line.
`master of <n>` with no `name:`: ask the user and write it. The persona is
session state, `engineer` until switched — @references/parts/personas.md.

`pearde sweep` lists every claim silent past `claim-ttl` and what `--apply`
would do (@references/settings.md); a claim `.pearde/.state/pass.md` names is a
session's live work and stays. Before `--apply`, read the swept worker's output
off the scan: a PRD in **collect** is a finished implementer — step 6;
`analyzing` with specs on disk is a finished analyst — `pearde specced`. A
swept worker's `## Workflow` rows are read with its report: the run happened
whatever the verdict did. A worker its infrastructure killed — API error, lost
network, full disk — is resumed, not swept: it holds the context.

**2 · Answer.** A `## Answers` that grew, or a PRD a person moved in the view,
is the user talking to the board. Step 2 depends on the count step 1 printed:

| unanswered | step 2 is |
|---|---|
| none | nothing |
| one | that question, put as today |
| two or more | one drill pass over all of them per @references/drill.md § The board's own frontier — before step 3, before any claim; the questions already `out` are carried, the rest are put |

While two or more of that pass are missing from `## Asked`, `pearde claim`
refuses `asking N — drill first` on those and names the asker — the PRDs they
reshape: each asker, its ancestors and descendants, and whatever `needs:` one.
Everything else dispatches first; the pass goes out when those workers are in,
reopening the rest. Otherwise every `question` PRD and parked PRD naming a
human goes out, one pass per @references/drill.md, three answers a fork.

**You do not talk to the user; the dispatcher does** — put a pass by writing
`.pearde/.state/ask.md`, hand back `ASK`; `pearde answer` records the reply in
the user's words and moves the PRD `open` on the last one. A `## Questions`
without three answers is unaskable: write them or send the analyst back. A
reply calling the question wrong rewrites it. No reply: leave it.

**3 · Refine.** Whether the analyst's `## Split` table is usable is the
decision; `a drill when it is not` — never a split invented to move the board.

**4 · 5 · Spec ahead, implement.** Which persona the job wears is the decision;
the commands are `next`'s to print. Every ready PRD is claimed and dispatched
in one turn, each a background worker of its own whose whole prompt is one line
naming `pearde brief <prd> --worker <name>`, so the brief never enters this
window. `workers` and `pipeline` in `.pearde/settings.md` are caps a person
set; `0`, the default, is no cap. `pearde claim` refuses what is not
dispatchable — held, not a leaf, `needs:` not `done`, a `workflow:` naming
nothing — and names the gate. A footprint clash is none of those: each worker
holds a worktree of its own, so the plan orders the pair and the merge resolves
it; `brief` maps each refusal to a skip word, and a worker's own `brief`
re-reading its claim is no refusal. `pearde scan` marks the PRD's line `wf <slug>?` when
its workflow resolves to nothing: fix the slug or remove the key, then claim in
the same pass. `pearde workflow check` names the file; on a master it
never reaches a member's PRDs. Run `check` on the board the PRD lives on.
`--force` passes every gate — for the PRD genuinely another session's.
`specced --workflow <slug> --route -` reads a `## Route` on stdin when
`## Scores` names a slug the library lacks, drafts the workflow and its atomics
at `runs: 0`, and runs `workflow check` before keeping either — red refuses the
call whole, nothing written; `--workflow none` is refused, naming `## Route`.

**6 · Collect.** Results are pushed, never polled: a return is collected as it
lands, and what it unblocks is dispatched in the same turn — the frontier is
re-read off `scan` after every transition, never batched to the pass's end. A
worker returns one line — @references/parts/workers.md — verdict and report
file. Act on the line: the tool maps the verdict to its transition, not you —
`pearde collect <prd> --report <path>` runs SPECCED, REFINE, QUESTION, DONE,
BLOCKED, FAILED each through its own command and gates, and refuses a missing
or unknown word, writing nothing. Open `.pearde/prds/<prd>/report.md` only for
what the line does not carry and the transition needs, never for what a command
already parses: a report read whole sits in the window all session. Before
`done` on work this session implemented, call the skeptic —
@references/parts/consult.md — one question, your judgment; the transition is
still yours.

**A report carrying `## Workflow <slug>` followed a route, and the run is what
improves it** — @references/parts/workflows.md. Read the rows: the verdict
decides the transition, and a `stopped` row changes nothing about it. Apply an
edit where the failure was the atomic's, refuse it where the failure was the
code's or the PRD's, and say which in the pass. The worker wrote the text:
paste it or refuse it, never rewrite it.
**`runs` +1** on the workflow and on every atomic that ran, `updated: <today>`
where the text changed — a route `specced` just drafted at `runs: 0` is no
exception: its first collect is `runs: 1` and fills its empty `## Fails when`.
**`pearde workflow check` before the commit.** An edit that breaks the format
is refused, not repaired. The changed files ride the PRD's commit —
`pearde collect --also <path>`. The PRD's own `footprint:` does not change.
**One writer: the orchestrator.** Two workers on one atomic is two collects. A
defect outside a worker's scope is the orchestrator's:
@references/parts/derived.md — a derived PRD or memo, not `open` by default.

**7 · Knowledge.** Before a fork goes to the user, query the record for it —
`python3 resources/knowledge.py query`. A strong hit is the answer: write it
under `## Answers` per step 2, and the fork never reaches the user. A gap or
thin hit changes nothing — `query` already enqueued it in
`.pearde/wiki/pending/`, and the fork still drills at step 8. This step only
reads; a `remember` or `conclude` is a worker's or the user's own.

**8 · Drill, then stop.** Nothing in flight and nothing dispatchable means a
person blocks the board: one drill pass over the open frontier —
@references/drill.md § The board's own frontier — never one per PRD, never a
question `## Asked` lists. The same drill the scan count starts at two or more
questions (step 2), reached now that nothing else is left. Answers land per
step 2; back to step 1. Stop when the frontier is all out: report per-state
counts, each `question` / `refine` / `failed` PRD with what it needs, requested
PRDs not `done` with `complexity`, `deferred` derived PRDs by name; rewrite
`.pearde/report.md` per `@@report` and `.pearde/.state/pass.md`; hand back
`DRAINED` or `BLOCKED`. `pearde view wait` is the dispatcher's; you never park.
