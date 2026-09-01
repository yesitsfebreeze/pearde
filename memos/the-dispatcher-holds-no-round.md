---
memo: the-dispatcher-holds-no-round
kind: decision
status: decided
subject: the round runs in a pearde-round worker whose window is thrown away, and the budget is measured from the window's own floor
date: 2026-09-01
supersedes: the-round-has-a-context-ceiling
prds:
  - the-round-runs-in-a-window-that-ends
---

# the-dispatcher-holds-no-round — the window that fills is the one that ends

`.pearde/memos/the-round-has-a-context-ceiling.md` got the diagnosis right and
the remedy half wrong. Cost is `context × turns`, and a window that grew is
charged again on every turn that follows it — that still stands. What it
missed is where a window starts. Measured on this repo's own transcripts,
2026-09-01: a `/pearde` session's first turn was billed 50,229 tokens — system
prompt, tool schemas, `CLAUDE.md`, the skill — before the round had read
anything at all, and its largest was 200,725 over 66k of content it had
actually produced.

So a 100k ceiling measured absolutely spent half itself on turn one and
refused a round that had run one scan, and its only exit was "end the round
and tell the user". The mechanism meant to stop an expensive window was
stopping the work.

**Decided.** Two changes, one shape.

The round runs in a `pearde-round` worker — @references/agents/pearde-round.md
— and the session the user asked is a dispatcher that starts one, reads its
line, carries answers back and starts the next
(@references/parts/dispatch.md). A worker's window is thrown away when it
returns, so it is free to fill; the dispatcher grows by one prompt and one
line per round, and a run of twenty ends about where it started. A worker
ends itself at `transitions-per-round` and hands back `MORE`: reaching the end
of a window is the normal case, not a failure.

`context-budget` is measured as `ctx - floor`, `floor` being the smallest
window the session has been billed for. The floor is not the round's doing and
is not the round's to pay down.

**It beat** raising the budget — which buys turns at the price of paying the
same window again on every one of them — and compacting instead of handing
over, which keeps a summary of a window that was mostly worker reports when
`.pearde/.state/round.md` is that summary written on purpose.

**A worker is never given a ceiling of its own.** The transcript a hook is
handed is the dispatcher's, and a worker's turns are not in it: any number the
guard read there would be somebody else's window. So a call carrying
`agent_id` is skipped, and the worker's own limit is a count it keeps itself.

**And a stamp belongs to one window, not one session.** One session id covers
the dispatcher and every worker under it, so the guard's repeat-read stamps
are keyed by `agent_id` as well as by path. Without that, the second round
worker is refused the first read of a file the first one read — a fresh window
punished for what it never saw.
