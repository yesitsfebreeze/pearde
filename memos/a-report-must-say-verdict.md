---
memo: a-report-must-say-verdict
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: collect requires the literal word Verdict: in a report and nothing tells a worker to write it; the orchestrator adds the prefix rather than sending the worker back
date: 2026-09-01
prds:
  - seven-closed-probes-drifted-red/the-doctor-completes-without-a-home
---

# a-report-must-say-verdict — the tool demands a marker the brief never asks for

## Decision

`collect` will not read a report whose first 40 lines lack a line matching the
literal word `Verdict:`. Nothing a worker is handed says so. Until the
instrument or the templates are changed, **the orchestrator adds the prefix to
the worker's own verdict line and changes nothing else** — no rewording, no
re-ordering, no summarising — and says in the round file that it did.

A report is not sent back for this. A round-trip that costs a worker dispatch
to insert seven characters is the board paying for its own instrument.

## Why

`resources/board/collect.py:254` holds `VERDICT_RE`, and it demands the literal
word. `references/parts/workers.md` and every file under
`references/templates/` contain the string `Verdict:` zero times. The
implementer on `the-doctor-completes-without-a-home` wrote `**DONE** — …`,
which is the shape its brief describes, and `collect` refused with "names no
`Verdict:`".

That is the definition of an instrument defect under
@references/parts/derived.md rule 2: fixing it changes nothing about what
ships, only how loudly the board notices a report it already understands. A
worker that follows its brief exactly produces a report the tool rejects, and
the failure surfaces at the orchestrator, one dispatch too late to be cheap.

The prefix is safe to add because it carries no judgment. The word after it is
the worker's; the orchestrator is transcribing a verdict, not forming one. The
line the board must never let an orchestrator write is the *verdict itself*,
and this rule does not come near it.

## Alternatives considered

**Send the report back for a re-write** — the clean answer, and the one the
worker-writes-its-own-report rule points at. It lost on cost: a full
implementer dispatch, its whole context rebuilt, to add a prefix to a line
whose content is already correct and already the worker's. The board would pay
that on every report until the templates change.

**Fix the templates and `workers.md` in the same round** — the actual repair,
and the right one eventually. It lost here on scope: it is a change to the
skill's own references with no PRD behind it, made by an orchestrator mid-round
on a board that has three other sessions live in the same tree. `derived.md`
rule 2 routes an instrument defect to a memo precisely so it does not become an
unbudgeted edit. The repair is still owed and this memo is the record of the
debt.

**Loosen `VERDICT_RE` to accept `**DONE**`** — cheapest in code. It lost
because it makes the marker optional in practice while leaving it mandatory in
the regex, which is the worst of both: reports drift into three spellings and
the next parser has to accept all of them.

## Consequences

- Every collect on this board is preceded by a check that the report's first 40
  lines carry the marker, and the orchestrator's round file must name the
  addition when it makes one. An unrecorded edit to a worker's report is
  indistinguishable from an orchestrator writing the verdict.
- It deliberately does not fix the defect. `workers.md` and the report template
  still owe the sentence "the report's first 40 lines must contain a line
  beginning `Verdict:`", and every dispatch until then has to carry it in the
  prompt by hand.
- It says nothing about a report with *two* `Verdict:` lines, or one inside a
  quoted block from an earlier report. Both are now reachable, since workers
  are being told to carry a predecessor's findings forward verbatim. That is
  the next memo's problem.
