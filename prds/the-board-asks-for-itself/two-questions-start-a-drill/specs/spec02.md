---
complexity: 8
footprint:
  - resources/board/transitions.py
---

# spec02 — the gate: a claim over an unput drill is refused

Already stands: the drill gate inside `gate_claim` in
`resources/board/transitions.py`, after the `dispatchable` gates every caller
already runs. It reads `planlib.drill_questions(board)` — the same list the
scan's drill section prints — and refuses with
`asking N — drill first; the unanswered questions go to the user before
anything is dispatched` when two or more questions are outstanding and not yet
in the round file's `## Asked`. One question outstanding is not a gate: it is
step 2's ordinary put. A question the round file carries (`· out` or
`· answered`) stops gating; the gate word `asking` joins the list
`dispatchable`'s callers map. The drill is the orchestrator's, so the gate is
not skipped by naming the holder — `brief --worker` refuses the same way — but
`--force`, the escape hatch, still passes, and the view's forced `/edit` never
runs the gate at all.

## Acceptance

- [x] on the two-question fixture board, `transitions.py claim other w --as
      engineer` refuses, exit 1, its line naming `asking 2`
- [x] after the question title is written into the fixture round file's
      `## Asked`, the same claim succeeds (open → analyzing) and carries the
      claim line
- [x] with one question outstanding (the second PRD answered in place), the
      claim of a second open PRD goes through — no gate at one

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -m py_compile resources/board/transitions.py
CODE="$PWD" bash -e -o pipefail "$PWD/.pearde/prds/the-board-asks-for-itself/two-questions-start-a-drill/probe/spec-fixture.sh" /tmp/spec02-fixture
echo "spec02 verify done"
```

`spec-fixture.sh` legs 2 and 3 are this spec's boxes: the refusal line
(`OK: claim refused naming asking 2`) and the succeeded claim (`OK: claim went
through once the round was out`) are quoted in its output. The implementer
runs it with its own temp path in place of `/tmp/spec02-fixture`.
`probe done · failures: 0` is the passing line.