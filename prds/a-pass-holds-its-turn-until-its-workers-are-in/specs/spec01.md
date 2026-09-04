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

- [x] `references/parts/loop.md` states, in prose and not only by reference, that a pass holds its turn until every worker it dispatched has returned or is measurably dead, and that a background worker does not outlive the pass window that dispatched it.
- [x] `references/parts/loop.md` still says the ceiling is a handover: a pass at `context-budget` hands back `MORE`, and the hold rule is written so as not to contradict it.
- [x] The sentence in `references/parts/loop.md` that names what the guard refuses no longer claims every rule in that list is guard-enforced.
- [x] `references/parts/dispatch.md` says a pass worker's return ends its children, and states the same hold rule from the dispatcher's side.
- [x] `references/parts/workers.md`'s liveness paragraph points at the hold rule and says the check alone does not license returning over a live worker.
- [x] `references/agents/pearde-pass.md`'s verdict table carries a row naming holding as the response to workers in flight.
- [x] `python3 resources/prose.py check` is silent and exits 0 on all four files at once.
- [x] `python3 resources/index.py check` names none of the four files.

## Verify and Proof

Every needle is read off the file with markdown emphasis stripped and
whitespace collapsed, so a re-wrapped paragraph is the same text to the check
and only the words can break it.

```sh
say() { tr '\n' ' ' <"$1" | sed -e 's/[*`]//g' -e 's/  */ /g'; }

say references/parts/loop.md | grep -qF 'A pass holds its turn until every worker it dispatched has returned or is measurably dead.'
say references/parts/loop.md | grep -qF 'A background worker does not outlive the pass window that dispatched it'
say references/parts/dispatch.md | grep -qF 'pass holds its turn until every worker it dispatched has returned or is measurably dead'
say references/parts/dispatch.md | grep -qF "A pass worker's return ends its children."
say references/parts/dispatch.md | grep -qF '"waiting on workers" least of all'
say references/parts/workers.md | grep -qF 'the pass holds its turn until every worker it dispatched has returned or is measurably dead'
say references/parts/workers.md | grep -qF 'it does not license returning over a live one'
say references/agents/pearde-pass.md | grep -qF 'hold the turn | a worker you dispatched is in flight'

say references/parts/loop.md | grep -qF 'does not move the ceiling: a pass at context-budget still hands back MORE, once its workers are in'
say references/parts/loop.md | grep -qF 'the first four are not advice'
if say references/parts/loop.md | grep -qF 'none of these rules is advice'; then exit 1; fi

python3 resources/prose.py check references/parts/loop.md references/parts/dispatch.md references/parts/workers.md references/agents/pearde-pass.md

out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf 'index.py check exit %s\n%s\n' "$rc" "$out"
case "$rc" in 0|1) ;; *) exit 1 ;; esac
if printf '%s\n' "$out" | grep -E 'references/parts/(loop|dispatch|workers)\.md|references/agents/pearde-pass\.md'; then exit 1; fi
```
