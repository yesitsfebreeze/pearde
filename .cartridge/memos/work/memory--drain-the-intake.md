---
kind: work
level: 10
status: done
description: start the daemon and drain the five queued captures into typed claims
read_when: "executing the dashboard plan"
---

# drain-the-intake

From [[working-with-memory]] item 3.

## Do
Start the daemon for this root, `memory intake drain`. If the distill pass
needs a reason model that is not configured, stop and report what is missing
— never fake the drain.

## Check
`memory report --group claim_kind` shows more labels than the two it shows
today; no file remains in `.memory/intake/`.
Ran 2026-09-05: the intake was already empty (`memory intake status` pending=0
stuck=0 failed=0), a literal `memory intake drain` confirmed "nothing pending",
and the daemon serves this root again on the current build — the installed
`memory` on PATH predates the `report` operation, so the daemon was restarted
from `target/release/memory`. `memory report --group claim_kind` now shows nine
labels (decision, documentation, insight, knowledge, procedural, question,
research, skill, work) against the two the plan measured. The drained jobs
remain archived under `.memory/intake/direct/done/`, which is where a drain puts
them.
