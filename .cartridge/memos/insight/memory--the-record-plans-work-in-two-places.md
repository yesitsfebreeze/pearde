---
kind: insight
description: "`open-work` declares itself the only place that plans work while 36 open `kind: work` parts plan work beside it, and neither register lists the other — the register split the collapse was supposed to end, re-formed inside `memos/`"
read_when: "picking up work, ranking a defect, or asking where the next thing to do lives"
---

# the-record-plans-work-in-two-places

[[@prd/note/memory--open-work.md]] opens with "**The only place in the repo that plans work.**
Ordering is the content: the topmost item is the most important open thing, and
importance falls monotonically from there." Measured 2026-09-06, it ranks 29
items. In the same `memos/` tree, 63 parts carry `kind: work` — 23 done, 4
blocked and **36 open** — each with its own `Do` and `Check`, and
[[SYSTEM]] defines that kind as "one unit of planned work" with [[@prd/routine/run-board.md]] as the
routine that runs it. Both statements are in the protocol, and they cannot both
be true.

The two registers do not know about each other. Sampling five open work parts —
`an-empty-memory-is-reaped`, `embeds-go-through-one-lane`, `the-graph-converges`,
`query-caps-its-default-answer`, `one-daemon-per-store` — none appears anywhere
in `open-work`. The traffic in the other direction exists but is accidental:
`open-work` item 14 names the stale `entity_memory` for a reparented stray, which
is the same defect [[@prd/work/memory--the-stray-entity-rescue-cannot-run.md]] was written about
without either citing the other. So a session picking up work reads one list or
the other and gets a different answer about what matters most, and a defect can
be filed twice with neither filing visible from the other.

This is [[one-memory]]'s split, re-formed one level down. [[the-registers-collapse]]
deleted `docs/` and `.pearde/` so that `memos/` would be the whole record, and
inside `memos/` the same two shapes came straight back: a ranked prose list that
carries priority and no `Check`, and a set of atomic units that carry a `Check`
and no priority. Each has the half the other lacks, which is exactly why both
survive and why neither absorbs the other on its own. Naming the split is not
the fix; deciding which one ranks and which one executes is, and that is a
decision nobody has made.
