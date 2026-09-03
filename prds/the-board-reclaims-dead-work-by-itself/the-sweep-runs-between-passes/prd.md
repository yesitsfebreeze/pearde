---
state: specced
origin: requested
priority: 85
complexity: 16
blast-radius: mid
workflow: probe-then-spec
---

# the sweep runs between passes

`sweep` is loop step 1 — it runs once, when a pass opens. Between passes
nothing reclaims anything, so a ghost claim survives until somebody starts a
pass, regardless of what `claim-ttl` says. The four ghosts of 2026-09-03 sat
claimed from 11:18:04 until a pass happened to open at ~12:0x; the ttl of 30m
had expired long before, and no ttl could have helped, because nothing was
running to notice.

When this is done, the sweep fires without a pass. Decide and implement one
carrier: the view daemon's own tick, or a scheduled run — `resources/board/
schedule.py` already exists — and say in the report which was chosen and what
the other would have cost.

**Needs `a-claim-names-the-process-that-holds-it`.** A sweep that runs more
often against the *mtime* rule reclaims live work faster, which is a
regression, not a fix. It must be asking the session ledger before it is
allowed to run unattended.

**Constraint.** `sweep --apply` drops uncommitted lane paths. An unattended
sweep must commit a lane before it releases the claim over it, or it turns a
cancelled worker into lost work automatically instead of manually.
