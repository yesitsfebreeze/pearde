---
state: done
origin: requested
priority: 75
complexity: 8
blast-radius: mid
workflow: probe-then-spec
actual: 0.7h
---

# a fork reaches the user when it is written

Questions batch until the pass returns. On 2026-09-03 a worker knew a fork at
roughly minute three; the user saw it about twenty-five minutes later, when the
pass finally handed back `ASK`. Nothing was blocked in between except the user.

The user's friction, verbatim: *"apparently I still have to drill into the
questions by hand (you are not automatically asking)"*. The ASK path did fire
automatically and all four forks went out in one pass — the complaint is
**latency**, not absence, and the fix is not a second asking mechanism.

`.pearde/.state/ask.md` exists on disk before the pass ends. When this is done,
writing a fork wakes the dispatcher rather than waiting for the pass's return
line, and a user answering early does not have to wait for a pass boundary to
unblock the PRD that asked.

**What must not change.** A pass still hands back `ASK`, and the drill still
covers the whole frontier in one pass rather than trickling one question at a
time — @references/drill.md. Waking the dispatcher earlier must not turn one
drill pass into four interruptions.

## Questions

### Q1: When a question reaches you

Several helpers can each hit a fork minutes apart, and a run is not finished
when the first one does. Reaching you the moment the first is written gets you
answering soonest, but the same run could reach you four separate times
instead of once?

1. **The moment one is written** — you hear within seconds of the first, and again each time a later one lands. (recommended)
2. **When nothing can still ask** — you hear once, after everything running has finished and the list can no longer grow.
3. **After a short hold** — you hear once the first has waited a few minutes for company, whatever is still running.

<!-- for the board: ask.py `settled()` and the one-pass-out rule in `cmd_wait`; the wake predicate is the only thing the answer moves — probe p2-wake.sh cases 4 and 5 -->

## Answers

**Q1** *(answered 2026-09-03 14:56)* — Not one of the three prepared options — the user asked to search the repo for a satisfactory answer instead. Found one: `resources/board/serve.py`'s daemon already has this mechanism. `POLL_S = 1.0` — the mirror loop stat-sweeps every board file once a second and calls `bump()`, which increments the board's `seq` and does `cond.notify_all()`, waking every long-poller blocked on `/wait`. `pearde view wait` already rides this. Consequence: forks written within the same one-second window collapse into a single wake, and a fork written any time after still wakes within about a second — no dispatcher-side batching, hold timer, or "wait for the whole run" logic needed. Route the fork-write through this existing seq/wait primitive rather than building new mechanism: when `ask.md` changes, bump the board the same way any other board file change already does, and let existing `/wait` callers pick it up.

## Report

spec01: exit 0
control (nothing)          3 -> 3   quiet
ask.md written             3 -> 4   BUMP
control (nothing)          4 -> 4   quiet
## Questions in prd.md     4 -> 5   BUMP
control (nothing)          5 -> 5   quiet
--- what the board says it owes, with no pass worker involved ---
one                                           1 open   0 answered  analyzing
drill_questions: [('one', 'Q1', 'What the thing does', False)]
