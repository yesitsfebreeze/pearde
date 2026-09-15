---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the distill prompt's kind list is the eight built-ins followed by the registered ones in `HashMap` order, so the prompt text varies per process — two kinds are registered on this store today, and `kinds-are-declared` would grow that

## Do

`kind_list` (`src/ingest/src/ingest_distill.rs:44-51`) builds the kinds offered
to the model as `DEFAULT_KINDS` — a fixed array — followed by whatever
`extra_kinds` holds, joined with `", "` straight into the prompt. Every caller
builds `extra_kinds` from a `HashMap` walk:

```
commands_intake_cmd.rs:142   g.read().root.claim_kinds.keys().cloned().collect()
rpc/server.rs:2330           self.graph.read().root.claim_kinds.keys().cloned().collect()
commands/src/lib.rs:1466     g_c.read().root.claim_kinds.keys().cloned().collect()
```

`HashMap` iteration order is randomised per process, so the tail of that
sentence is a different string run to run. Measured on this store 2026-09-06
08:30, `memory health` reports **claim kinds: 2** — live, not hypothetical, with
two orderings possible today and more as the registry grows.
[kinds-are-declared](../kinds-are-declared/prd.md) is the open item that would grow it: retiring
`DEFAULT_KINDS` moves every kind into that map and makes the whole list
hash-ordered.

The prompt is meant to be fixed. `insights` runs two prompts chosen precisely
so runs can be compared ([[insights-prompts-are-the-experiment]]), and both go
through this list; `commands_insights.rs`' own header says "a pipeline whose
prompt set moves is a pipeline whose output cannot be compared across runs".

Sort the extras before joining — one line in `kind_list`, which fixes all three
callers at once and leaves the built-in order untouched. This is the same defect
as [clustering-walks-the-entity-map-unsorted](../clustering-walks-the-entity-map-unsorted/prd.md) in a different file, and both
are the third and fourth instances of the walk `build_gnn_snapshot` already
sorts against.

**Done 2026-09-06.** `kind_list` sorts the extras before appending them, so all
four callers are fixed at once and the built-in order stays as declared — the
`DEFAULT_KINDS` sequence is a choice about what the model sees first, and
sorting it would have been a second, unrequested change.

The part names three callers; there are **four**. `commands_insights.rs:173`
collects the same `root.claim_kinds.keys()` walk, which matters more than the
count: `insights` is the pipeline the part's own argument rests on, and it was
missing from the list of things affected. Found by re-running the `rg` rather
than reading the three.

Held by `kind_list_is_the_same_string_whatever_order_the_extras_arrive_in`:
three different input orders of the same set, one output, with the sorted tail
asserted explicitly and the built-in prefix asserted to be *un*sorted. That last
assertion is the one that would catch someone "fixing" this by sorting the whole
list.

## Acceptance
`kind_list` returns the same string for the same set of registered kinds across
processes; a unit test passing extras in two different input orders asserts one
output. Three orders rather than two, and `just test` green at 1,256 passed.
