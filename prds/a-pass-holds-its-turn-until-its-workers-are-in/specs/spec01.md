---
complexity: 5
footprint:
  - references/parts/loop.md
  - references/parts/dispatch.md
  - references/parts/workers.md
  - references/agents/pearde-pass.md
---

# spec01 — the hold rule is written in all four places a pass reads

The rule that a pass holds its turn until every worker it dispatched has
returned or is measurably dead is stated in the loop, in the dispatcher, in the
liveness paragraph of the worker briefs, and in the verdict table. The ceiling
handover and the liveness check keep the behaviour they had; this unit adds the
sentence that binds them and removes the reading under which a pass returns
over live children.

**What already stands.** The analyst's probe wrote all four edits into the
working tree of this lane, uncommitted, and they are green against
`resources/prose.py` and against the harness `spec02` builds. Read them before rewriting anything:
`git diff -- references/` is the whole of it. What is left is to judge the
wording, keep or improve it, and commit it inside the footprint.

Four edits, one per file:

- `references/parts/loop.md` — the intro's rule list grows from four to five,
  the fifth being the hold rule: a background worker does not outlive the pass
  window that dispatched it, handing back a verdict with workers in flight
  kills them, and the pass holds the turn instead, collecting and dispatching
  as returns land. The sentence after that list said `none of these rules is
  advice` about four guard-enforced rules; it now says `the first four`, and
  names the verdict table as what holds the fifth. The paragraph says
  explicitly that the ceiling does not move: a pass at `context-budget` still
  hands back `MORE`, once its workers are in.
- `references/parts/dispatch.md` — a paragraph under `## Why the pass is not
  worked here` saying it from the dispatcher's side: a pass worker's return
  ends its children, this harness promises them no life past that window, so
  the pass holds and hands back `MORE` after. Step 2's `Anything else` note
  gains the reason `waiting on workers` is worse than an unrecognised line: a
  pass that prints it has just killed the workers it was waiting on.
- `references/parts/workers.md` — the liveness paragraph (`A launch is not a
  life`) gains a closing sentence saying the check tells a dead worker from a
  live one and does not license returning over a live one; a worker still
  growing its transcript is in flight, and the pass holds its turn until every
  worker it dispatched has returned or is measurably dead.
- `references/agents/pearde-pass.md` — the verdict table gains a first row for
  the situation with no verdict: a worker in flight, the response `hold the
  turn`, and the dispatcher column saying it never reads the row because the
  turn has not ended. The prose above the table already said this; the table
  did not, which is what made a status line reachable as a return.

## Acceptance

- [ ] `references/parts/loop.md` states, in prose and not only by reference, that a pass holds its turn until every worker it dispatched has returned or is measurably dead, and that a background worker does not outlive the pass window that dispatched it.
- [ ] `references/parts/loop.md` still says the ceiling is a handover: a pass at `context-budget` hands back `MORE`, and the hold rule is written so as not to contradict it.
- [ ] The sentence in `references/parts/loop.md` that names what the guard refuses no longer claims every rule in that list is guard-enforced.
- [ ] `references/parts/dispatch.md` says a pass worker's return ends its children, and states the same hold rule from the dispatcher's side.
- [ ] `references/parts/workers.md`'s liveness paragraph points at the hold rule and says the check alone does not license returning over a live worker.
- [ ] `references/agents/pearde-pass.md`'s verdict table carries a row naming holding as the response to workers in flight.
- [ ] `python3 resources/prose.py check` reports no new violation on the four files against the pre-change baseline: `loop.md` clean, `dispatch.md` clean, `workers.md` clean, `pearde-pass.md` 6 unbound waste words and no more.
- [ ] `python3 resources/index.py check` prints the same four lines it printed before the change and no fifth.

## Verify and Proof

```sh
python3 resources/prose.py check references/parts/loop.md references/parts/dispatch.md references/parts/workers.md
python3 resources/prose.py check references/agents/pearde-pass.md; test $? -eq 1
python3 resources/prose.py check references/agents/pearde-pass.md | grep -qF '6 unbound waste word'
python3 resources/index.py check; test "$(python3 resources/index.py check 2>&1 | wc -l | tr -d ' ')" = 4
```
