---
kind: work
description: Surface stale or conflicting memory explicitly during resolution
status: done
needs:
  - "[[@prd/work/memo--implement-memo-usage-resolution.md]]"
---

# Handle memory staleness and conflicts

## Outcome

When memory records disagree or may be stale, the resolver reports that uncertainty instead of hiding it. Agents can prefer current accepted decisions while still seeing conflicting notes or superseded records when they matter.

## Check

- [x] Every item carries `kind` and, where declared, `status`; a replaced memo
      also carries `superseded_by` naming the path that replaced it.
- [x] A memo is never returned above the memo that supersedes it: after ranking,
      a replaced item is deferred until its replacement has been emitted. Its
      own score is untouched, so it keeps its place when the replacement did not
      match at all.
- [x] An open question carries `unresolved`: "open question: the record has no
      answer here; do not read the options as a decision".
- [x] The response carries `conflicts`: a `superseded` entry when a replaced
      memo and its replacement both matched, and an `unsettled` entry for each
      open question on the page. Always present, empty when there is nothing.
- [x] `staleness_is_ordered_labelled_and_called_out` covers a superseded
      decision beside its accepted replacement and an open question about which
      of the two applies, asserting the order, the link back, the marker, both
      conflict entries, and that an unrelated result carries an empty list.

## Approach

`status` reached the caller through [[@prd/work/memo--preserve-memory-type-boundaries.md]], but
`supersedes` was read nowhere: a decision said what it overtook and nothing
turned that into what replaced it.

1. `builtin/memo/src/usage.rs`: build the reverse map of `supersedes`, report it
   as `superseded_by`, and after the sort defer a replaced hit until its
   replacement has been emitted.
2. Mark an open question `unresolved`, and collect both kinds of disagreement
   into a `conflicts` list on the response.
3. `builtin/memo/tests/resolver.rs`: one test over the whole shape.

## Result

Ordering is targeted rather than a blanket demotion: a replaced memo sinks below
its replacement only when the replacement actually matched. Asking about the
history still finds the old rule at its own rank, labelled with what replaced it.

`conflicts` is deliberately narrow — supersession the record states, and open
questions the record marks. It does not guess at contradictions between two
accepted decisions; that would be inference presented as fact.
