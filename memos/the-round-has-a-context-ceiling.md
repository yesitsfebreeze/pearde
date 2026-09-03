---
memo: the-round-has-a-context-ceiling
kind: decision
status: superseded
tags:
  - memo
  - kind/decision
  - status/superseded
subject: a round is capped at 100k context and resumed from the round file, and workers are dispatched as typed agents
date: 2026-08-31
superseded_by: the-dispatcher-holds-no-round
---

# the-round-has-a-context-ceiling — a window is paid for once per turn, not once

Seven days of transcripts, read off `~/.claude/projects/*/*.jsonl`: 18,716
orchestrator turns on the large model, averaging 252k of context each, 4,712M
cache-read tokens. The turns above 300k are 28% of the count and 59% of the
spend. One board session — 34 hours, 1,023 turns, 532k average — held 514k
tokens of unique content and replayed it a thousand times.

That is the whole defect. Cost is `context × turns`, and a window that grew is
charged again on every turn that follows it, whether or not anything in it is
still needed. The board is on disk. `prds/.round.md` is what a session carries.
A round past its ceiling is cheaper to end and resume than to continue, and
nothing in the large window was worth the second payment.

**Decided.** `context-budget`, 100k, in `prds/settings.md`. `resources/guard.py`
reads the last assistant usage off the transcript, notes the crossing at 70%
and 85%, and at the ceiling refuses everything except the round file,
`references/parts/loop.md`, `references/parts/round.md` and the board's own
commands — the four things a restart needs and nothing else.

**It beat** two others. Leaving it as a sentence in `loop.md`: the three rules
already there became mechanisms for the same reason, and a rule the round can
forget is a rule it forgets at 400k. Compacting instead of restarting: a
compaction keeps a summary of a window that was mostly worker reports, and the
round file is that summary written on purpose.

**And workers are typed.** `agents/pearde-analyst.md` on the cheaper model,
`agents/pearde-implementer.md` on the one that writes code. Dispatch had named
no type, so every worker ran the orchestrator's own model — 439 of them in the
same seven days. An analyst turning a settled contract into specs was never the
job that needed it.

**A report is a file.** Workers write `prds/<prd>/report.md` and return one
line. A report returned whole is pinned in the orchestrator's window for the
rest of the session, which is the mechanism that made the 532k session 532k.
