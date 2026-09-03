---
state: open
origin: requested
priority: 75
complexity: 0
blast-radius:
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
