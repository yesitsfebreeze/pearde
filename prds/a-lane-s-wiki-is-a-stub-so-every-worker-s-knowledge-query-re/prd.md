---
state: done
origin: requested
priority: 70
complexity: 18
blast-radius:
workflow: probe-then-spec
actual: 0.24h
commit: 148e009 57db2bf
---

# a lane's wiki is a stub so every worker's knowledge query returns nothing

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
  ok   fixture carries resources/knowledge.py
  ok   lane worktree carries the script
  ok   lane starts with no wiki of its own
== A: a query from the lane reads the live board's record ==
  ok   query from the lane: query: 1 hit(s), 1 strong · 1 notes on record
== B: the query made no stub beside the lane ==
  ok   no <lane>/pearde/wiki was created
== C: a finding remembered from the lane lands on the live board ==
  ok   the board's wiki holds 2 source notes after remember
  ok   the lane's tree holds no source note of its own
== D: negative control — the pre-fix resolver fails these same checks ==
  ok   pre-fix resolver reports 0 notes from a lane — the check can fail
  ok   pre-fix resolver created the stub the PRD names
== E: no board above the cwd still falls back to the script's own repo ==
  ok   a call from outside any board still answers: query: 2 hit(s), 2 strong · 2 notes on record
== G: harvest recovers what the stubs already on disk are holding ==
  ok   harvest --dry reports without moving: dry · harvest: 1 note(s) recovered, 1 already on record, from 1 lane wiki(s)
  ok   harvest --dry moved nothing
  ok   harvest: harvest: 1 note(s) recovered, 1 already on record, from 1 lane wiki(s)
  ok   the stranded finding stands in the board's wiki
  ok   the emptied stub was removed from the lane
  ok   the shared graphify cache beside it is untouched
  ok   a second harvest finds nothing: harvest: no lane holds a wiki of its own — nothing stranded
== F: the live board — the tree under test reads it, and writes nothing ==
  ok   the tree under test reads 88 note(s), matching the board on disk (88)
  ok   no stub wiki under the tree under test

19 checks · 19 pass · 0 fail
verify.sh done, fail=0
knowledge.py parses
doctor: clean — 88 notes, graph in sync, pending honest
references/language.md references @references/personas/writer.md — not on disk
verify block complete

spec02: exit 0
harvest: no lane holds a wiki of its own — nothing stranded
       0
doctor: clean — 88 notes, graph in sync, pending honest
= 269 of 269 row(s) surveyed
  ok   fixture carries resources/knowledge.py
  ok   lane worktree carries the script
  ok   lane starts with no wiki of its own
== A: a query from the lane reads the live board's record ==
  ok   query from the lane: query: 1 hit(s), 1 strong · 1 notes on record
== B: the query made no stub beside the lane ==
  ok   no <lane>/pearde/wiki was created
== C: a finding remembered from the lane lands on the live board ==
  ok   the board's wiki holds 2 source notes after remember
  ok   the lane's tree holds no source note of its own
== D: negative control — the pre-fix resolver fails these same checks ==
  ok   pre-fix resolver reports 0 notes from a lane — the check can fail
  ok   pre-fix resolver created the stub the PRD names
== E: no board above the cwd still falls back to the script's own repo ==
  ok   a call from outside any board still answers: query: 2 hit(s), 2 strong · 2 notes on record
== G: harvest recovers what the stubs already on disk are holding ==
  ok   harvest --dry reports without moving: dry · harvest: 1 note(s) recovered, 1 already on record, from 1 lane wiki(s)
  ok   harvest --dry moved nothing
  ok   harvest: harvest: 1 note(s) recovered, 1 already on record, from 1 lane wiki(s)
  ok   the stranded finding stands in the board's wiki
  ok   the emptied stub was removed from the lane
  ok   the shared graphify cache beside it is untouched
  ok   a second harvest finds nothing: harvest: no lane holds a wiki of its own — nothing stranded
== F: the live board — the tree under test reads it, and writes nothing ==
  ok   the tree under test reads 88 note(s), matching the board on disk (88)
  ok   no stub wiki under the tree under test

19 checks · 19 pass · 0 fail
verify.sh done, fail=0
verify block complete
