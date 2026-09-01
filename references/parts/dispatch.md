# The dispatcher

The session that was asked does not work the board. It dispatches
`pearde-round` workers that do, one after another, and carries the user's
answers between them. It holds no board state, opens no PRD, reads no
reference file but this one.

## Why the round is not worked here

Context is billed on every turn, so what the asked session holds it pays for
again on every turn that follows. Measured on this repo's own transcripts, on
2026-09-01: a `/pearde` session opened at a 50,229-token floor — system
prompt, tools, CLAUDE.md, the skill — and ended at 200,725, having produced
66k of actual content. The window is what compounded, not the work.

A round worker's window is thrown away when it returns. The dispatcher's grows
by one prompt and one line per round — about 300 tokens — so a run of twenty
rounds ends roughly where it started, and no round is ever stopped for being
expensive: the expensive thing returns and the next one opens empty.

The board is on disk. `.pearde/.state/round.md` is what crosses between rounds,
and it is written by the worker that ends, not by the session that dispatches.

## The turn

1. **Dispatch** `pearde-round`. The prompt is these lines and nothing else:

   ```
   Work the board at <repo>.
   Resume from .pearde/.state/round.md.
   ```

   Add, each on its own line and only when it is true: `Scope: <prd>.` for
   `run <prd>`; `One round only.` for `once`; `The user answered:` followed by
   what they said, verbatim, one line per fork.

2. **Read the line it returns** — @references/agents/pearde-round.md defines
   the four:

   | it returns | you do |
   |---|---|
   | `MORE` | dispatch the next worker, same prompt. Say nothing to the user |
   | `ASK` | read `.pearde/.state/ask.md` — the one file this session opens — put every fork to the user in one question round with its prepared answers, through the ask-user-question mechanism, then dispatch the next worker carrying their words |
   | `DRAINED` | print the line, then park `python3 @resources/pearde.py view wait` — an answer written in the view wakes you, and you dispatch the next worker |
   | `BLOCKED` | print the line, name what needs a person, stop |

3. **Nothing else.** No scan, no `pearde` command, no PRD, no report, no
   `@@` scope, no README. A dispatcher that opens the manual is a round
   worker with extra steps, and the run pays for the manual on every turn to
   the end of the session.

`status` is the exception, and the only one: it changes nothing and costs one
call, so it is answered here — `python3 @resources/pearde.py scan` and the
progress line, per @references/parts/handles.md. Anything that moves a state
is a round worker's.

## What the user sees

A run is quiet by design. Between rounds, print the worker's own line and
nothing composed on top of it — one line per round, so the run reads as a
list of what moved. The board's own progress lines are in the worker's
window, `.pearde/report.md` is the state written for a person, and the view
draws it live.
