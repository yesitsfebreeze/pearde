---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/render.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/tool.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/rank.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/expand.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp/doors.rs
commit: "d04ab3329c5a76aec27267454b9b0a82f9fae8d3"
---

# asp answers agents in compact lines and expands a level at once

## Outcome

ASP costs an agent less. The user asked on 2026-09-19 to remove the friction and squeeze out the performance. Measured on the live daemon: a file expand was 10 KB of JSON, a search 39 KB, and a depth-2 expand took 2.8 s because every entity of a level was asked one after another. Now `format: "text"` answers one line per node, edge, action and source, and `tool.asp` answers that way by default with at most 20 nodes or hits unless given a `limit`. A level of an expand is asked in bounded parallel (16 at once). A search ranks a node whose own name and key hold every word of the query above phrases elsewhere that share one of the words.

## Acceptance

- [x] A named test gets both JSON and text through `tool.asp`, and the text is one line per node, action and source, with the id kept whole.
- [x] The whole library suite passes with the parallel expand.
- [x] `docs/asp.txt` describes the text format, the agent limit and the parallel levels.
