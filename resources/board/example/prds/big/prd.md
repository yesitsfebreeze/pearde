---
state: open
origin: requested
priority: 62
blast-radius: mid
---

# big — a parent whose work is in its children

The tree. A parent with live children weighs zero and is never dispatched —
work flows to the leaves. `first` has landed and `second` is open, so the scan
lists `second` ready and `big` not at all.
