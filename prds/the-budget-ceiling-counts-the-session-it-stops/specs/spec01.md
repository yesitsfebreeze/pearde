---
complexity: 18
footprint:
  - resources/guard.py
---

# spec01 — the ceiling binds the orchestrator, not the worker it dispatches

**All of this stands in the tree**, built in place, not staged elsewhere:
`resources/guard.py` now carries a `dispatched(data)` helper and a one-line
early return at the top of `budget()`.

The fix rests on one fact, established empirically against this board's own
live hook traffic while building this spec (dumped real `PreToolUse`
payloads to a scratch file, one call at a time, then read them back): the
hook payload's `session_id` and `transcript_path` are identical for the
orchestrator and every subagent it dispatches — one shared session, one
shared transcript file, exactly as `references/parts/round.md` says the
round file is the session's own memory. They cannot be the signal. But every
payload from a dispatched worker (a `pearde-analyst`, a `pearde-implementer`,
this very probe) carries `agent_id` and `agent_type`; every payload from the
orchestrator's own direct tool use carries neither. `dispatched()` reads
that.

`budget()` now returns immediately when `dispatched(data)` is true — before
`budget_of()`, before `context_now()`, before the 70%/85% note band, before
the `ESCAPE` check. Two consequences fall out of the single early return,
not two separate patches:

- A dispatched worker is never refused `Read`, `Write`, `Edit` or `Bash` by
  the round's ceiling, whatever its own window holds — the non-goal here is
  giving it a budget of its own, so it gets none, not a separate one.
- A dispatched worker is never denied at the ceiling, so it is never shown
  the deny text that names `.pearde/.state/round.md` as the file still open
  to write — the mechanism that had one worker overwrite the orchestrator's
  round file today. The `ESCAPE` bypass for that file is reached only from
  inside the post-cap branch of `budget()`, which a dispatched call now
  never enters.

Unchanged: `budget_of()`'s `off` / bare-number / `k`-suffix parsing,
`context_now()`'s token sum, the orchestrator's own refusal at the ceiling,
its one-shot 70%/85% notes, and the set of paths (`round.md`,
`references/parts/loop.md`, `references/parts/round.md`, the board's own
commands) that stay open to it — none of that code moved.

**Left to the orchestrator, outside this spec's footprint and this worker's
writable paths**: flipping `.pearde/settings.md`'s `context-budget` off
`off` back to a number. That file lives in the board repo outside this
PRD's own folder, which no worker may write; and flipping it is only safe
once the orchestrator's own session is far enough from its own ceiling not
to wall itself on the next call — a judgment call for whoever holds the
round, not a check this spec can automate. The mechanism this spec closes is
what makes that flip safe to make at all: once it lands, `context-budget` on
a board only ever measures the orchestrator's own session.

## Acceptance

- [x] `python3 .pearde/prds/the-budget-ceiling-counts-the-session-it-stops/probe/verify.py`
      prints `13 of 13 checks pass` and exits 0
- [x] in that run, a payload shaped like the orchestrator's own call (no
      `agent_id`, no `agent_type`), over a fixture board's `context-budget`,
      is denied — `"permissionDecision": "deny"` naming the budget
- [x] in the same run, a payload shaped like a dispatched worker's call
      (`agent_id` and `agent_type` set, as this repo's own hook payloads
      show for every analyst and implementer dispatch), over the same cap,
      on `Read`, `Write` and `Bash`, is never denied
- [x] a dispatched worker's call writing `.pearde/.state/round.md` while
      over the cap raises no ceiling denial — it is never funneled toward
      that file by the ceiling's own deny text, because it is never denied
      by the ceiling at all
- [x] the orchestrator's own call writing `.pearde/.state/round.md` while
      over the cap still goes through — the `ESCAPE` bypass is unchanged
      for the session it was written for
- [x] the orchestrator's own call at 75% of a fixture cap still gets the
      one-shot warn note; a dispatched worker's call at the same 75% gets
      none
- [x] `budget_of()` still reads `off` as `0`, a bare number as itself, and a
      `k`-suffixed number as thousands — the three cases `references/settings.md`
      documents, unchanged by this spec
- [x] `python3 resources/guard.py check` still runs clean against this
      repo's own board, unaffected by the fixture runs above
- [x] the signal is real, not assumed: against this board's own live
      `PreToolUse` traffic, the orchestrator's own calls carry neither
      `agent_id` nor `agent_type` while every dispatched worker's carry
      both, and all of them share one `session_id` — captured by the
      implementer independently of the analyst, with the orchestrator's
      concurrent calls as the control, and pinned as three probe checks

## Verify and Proof

```sh
python3 .pearde/prds/the-budget-ceiling-counts-the-session-it-stops/probe/verify.py || exit 1
echo "---"
python3 resources/guard.py check || exit 1
echo done
```
