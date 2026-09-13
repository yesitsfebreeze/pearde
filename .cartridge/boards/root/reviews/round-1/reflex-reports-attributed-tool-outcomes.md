---
kind: work
level: 10
status: open
estimate: 1d
description: Reflex distinguishes caller classes and successful tool outcomes from attempts, polling, and discovery overhead
read_when: measuring whether agent tools improve work rather than merely receiving calls
---

# reflex-reports-attributed-tool-outcomes

## Do

Tool-use evidence distinguishes deliberate agent work, other clients, background
polling, and automatic discovery. Attempts, successful completion, errors,
cancellation, duration, and result size are separately interpretable. A report
states its collection window and missing dimensions; it does not label raw call
counts as productivity or model-token estimates as measured billing.

Historical counts retain their unknown attribution rather than acquiring invented
successes or timestamps. Task outcomes, when observed, are distinct from the
agent's useful, situational, or dead verdict. Tool-contract changes and expired
verdicts are visible so a repaired tool is not judged from an obsolete failure.
Sensitive arguments and response bodies are not necessary telemetry.

The 2026-09-09 ledger mixed pre-dispatch attempts, UI activity, initialization,
and retired operations. [[reflex-measures-the-surface]] remains the existing
measurement mechanism; this work improves its evidence rather than adding a
second ledger. [[routine-usage-distinguishes-loading-from-completion]] owns the
specific skill execution gap. [[reflex-guides-deferred-tool-visibility]] consumes
the resulting evidence only after discovery is safe.
