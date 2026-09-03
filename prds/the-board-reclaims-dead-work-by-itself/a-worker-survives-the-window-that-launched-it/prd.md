---
state: open
origin: requested
priority: 90
complexity: 0
blast-radius:
---

# a worker survives the window that launched it

Measured twice on 2026-09-03. Six workers died when their pass returned. Then
eighteen workers, every one verified alive and growing at 11:14, **all stopped
at 11:18:04 to the second** when the user interrupted a tool call in the pass
window. No API error in any transcript. The window's end ended every child it
held, and `sweep --apply` at 11:10 dropped 44 uncommitted paths across four
lanes — whatever they had built before they died.

The sibling `a-pass-holds-its-turn-until-its-workers-are-in` (p90, already
specced) makes the pass hold its turn, which stops a pass from dropping its own
children **on a normal return**. It does not survive a user Ctrl+C, which is
what actually happened at 11:18:04, and it cannot: holding a turn is a
discipline, not a lifetime.

The user is explicit that killing workers by hand should be survivable.

When this is done, a worker's work is recoverable after its launching window
dies — whether by detaching the worker from the window, by re-attaching it from
the session ledger, or by committing its lane continuously so a death costs the
verdict and not the build. Say in the report which of those the tree can
actually support and what each costs; the cheapest honest answer may be the
third.

**Distinct from the p90 sibling**, which this does not replace: that one keeps
a well-behaved pass from killing its own workers, this one keeps a
badly-ended one from destroying their work.
