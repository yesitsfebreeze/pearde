---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 70       # higher first
complexity: 12     # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid  # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.02h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
footprint:
  - resources/guard.py
  - references/agents/pearde-round.md
  - references/parts/dispatch.md
  - references/parts/loop.md
  - references/parts/guard.md
  - references/parts/workers.md
  - references/skills/pearde.md
  - references/settings.md
  - README.md
  - index.md
  - references/files.md
  - .pearde/.gitignore
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/quickstart.sh
  - .pearde/prds/workflows-on-the-board/workflow-skill/probe/verify.sh
---

# the round runs in a window that ends

The board's own transcripts, 2026-09-01: a `/pearde` session opened at a
50,229-token window — system prompt, tool schemas, `CLAUDE.md`, the skill,
before the round had read anything — and ended at 200,725 having produced 66k
of content. Context is billed on every turn, so what the session held it paid
for again on every turn that followed, and `context-budget` (100k, measured
absolutely) refused the round at what was really 50k of work. The ceiling
meant to stop a half-million-token window was stopping the work instead, and
the way out of it — "end the round and tell the user" — stopped it for a
person too.

Two things are wrong and this PRD fixes both.

**The window that fills is not the one that should hold the round.** The
session the user asks is the dispatcher: it starts `pearde-round` workers,
carries the user's answers between them, and holds one prompt and one line per
round. A round worker's window is thrown away when it returns, so a run of
twenty rounds ends roughly where it started. Reaching a ceiling stops nothing:
the worker writes the round file and hands back `MORE`, and the next window
does the rest.

**A budget on a window must be a budget on what the round grew.** The floor —
the smallest window the session was billed for — is not the round's doing and
is not the round's to pay down. `context-budget` is measured from it.

Non-goals. The loop's eight steps do not change, and neither does what a
worker is handed or returns: the round worker is the same orchestrator the
briefs already describe, in a window that ends on purpose. Analysts and
implementers are untouched. No new command.

Pointers: `references/parts/loop.md`, `references/parts/guard.md`,
`resources/guard.py` (`budget`, `context_now`, `dispatched`),
`.pearde/memos/the-round-has-a-context-ceiling.md` — the memo this PRD is the
correction to.

## Report

spec01: exit 0
— the budget is measured from the floor
  ok   A1 the first turn sets the floor and passes
  ok   A2 90k of growth over a 60k floor passes
  ok   A3 110k of growth is refused
  ok   A4 a 99k window whose floor is 99k is not over budget
— the ceiling leaves a way on
  ok   B1 the round file stays writable
  ok   B2 dispatching a worker stays allowed
  ok   B3 asking the user stays allowed
  ok   B4 a worker is never judged by the dispatcher's window
  ok   B5 the refusal names the handover, not a stop
  ok   B6 ...and the worker that carries on
  ok   B7 ...and reports the growth over the floor
— a stamp belongs to one window
  ok   C1 a third read by the same worker is refused
  ok   C2 the next worker's first read passes
  ok   C3 the dispatcher's own first read passes
— the text says the same thing the code does
  ok   D1 references/parts/dispatch.md exists
  ok   D2 references/agents/pearde-round.md exists
  ok   D3 the skill sends the session to the dispatcher
  ok   D4 dispatch.md names the four verdicts
  ok   D5 ...and the prompt it sends
  ok   D6 the round agent names its stop conditions
  ok   D7 loop.md says the ceiling is a handover
  ok   D8 guard.md says the budget is measured from the floor
  ok   D9 settings.md documents transitions-per-round
  ok   D10 loop.md is still one page
  ok   D11 files.md lists the round worker
  ok   D12 files.md lists the dispatcher

26 checks · 26 pass · 0 fail
60 checks · 60 pass · 0 fail
loop.md one page
pearde: every part this repo owns checks out.
verify done rc=0
