---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
  - /Users/feb/dev/cartridge/memory.ctg/src/cartridge/src/asp
  - /Users/feb/dev/cartridge/memory.ctg/src/cartridge/src/lib.rs
  - /Users/feb/dev/cartridge/memory.ctg/src/cartridge/src/source.rs
  - /Users/feb/dev/cartridge/memory.ctg/cartridge.json
  - /Users/feb/dev/cartridge/memory.ctg/init.lua
  - /Users/feb/dev/cartridge/memory.ctg/README.md
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/memory.ctg/.cartridge/tests/integration/asp.rs
commit: "55863b356c7c75032b6a525dbe8addc5b29b924f"
---

# memory contributes its entities to asp

## Outcome

memory.ctg answers ASP on an `asp.memory` event as the owner of the `memory:`
scheme. The key is the full entity id.

- `expand` reads one fact back by id (`{op:"query", ids:[id], compact:true}`)
  and answers its node:
  - a name, and a description of at most 500 characters plus `...`;
  - its source scheme as a tag;
  - the `memory.source` and `memory.truncated` attributes;
  - the same observed-projection revision `context.memory` reports.
- `search` runs one text query, the same request `tool.memory` sends, and
  reads nothing back.
- Search keeps `context.memory`'s filtering exactly. Private rows are free of
  the limit, and every other row uses a slot.
- No edges and no actions are declared.

This row makes no heat claim. Search deposits exactly what a `tool.memory`
query deposits, today and under whatever
`@memory/heat-is-deposited-on-read-back-not-on-delivery` settles. Expand
deposits what a read by id deposits. `context.memory` keeps answering until
`the-context-path-is-deleted`. So the prompt recall and the proxy can move to
ASP `search` and read the same revisions.

`README.md` and `.cartridge/help.md` gain the `asp.memory` surface in this
change: the Events lists and a new `## ASP` section. The heat row rebases over
them.

## Acceptance

- [x] `a_memory_entity_expands_to_its_node_with_the_observed_projection_revision`
      passes: expand makes one by-id read and answers the node with the
      projection revision.
- [x] `expand_answers_nothing_for_a_missing_private_expired_or_respelled_key`
      passes.
- [x] `search_delivers_ranked_rows_without_reading_any_back` passes: search
      sends exactly one `{op, text, k}` request.
- [x] `search_keeps_the_context_filtering_exactly` passes, including the limit
      rule: only private rows are free.
- [x] `search_and_expand_agree_with_context_memory_on_a_real_bank` passes:
      search, expand and `context.memory` report one revision for one
      truncated fact.
- [x] `the_shipped_declaration_is_one_the_host_accepts` passes, and every test
      answer is held against the shipped `asp` block.
- [x] `README.md` and `.cartridge/help.md` carry spec01's Documentation text,
      and neither file's `context.memory` bullet changes.
- [x] The existing `memory_cartridge` tests still pass, and no other path held
      by the heat row changes.
