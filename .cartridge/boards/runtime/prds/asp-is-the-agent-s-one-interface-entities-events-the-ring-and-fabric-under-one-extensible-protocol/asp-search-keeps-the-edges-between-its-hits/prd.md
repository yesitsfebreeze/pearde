---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
commit: "5980c7cfc13f89dfc49ec38ba8e785b42c8a1a61"
---

# asp search keeps the edges between its hits

## Outcome

A search answer carries the edges its providers asserted between the nodes it returns. A search provider such as fs answers `file:` and `range:` nodes joined by `matches` edges, and the edge is what says which file holds a match. The host's search merged the nodes and dropped every edge, so a caller could not tell. The fs provider worker found this on 2026-09-19.

## Acceptance

- [x] A named test searches a fixture provider that answers two nodes and an edge between them, and the answer's `edges` holds that edge with its contributor.
- [x] An edge whose end is not among the hits is left out.
- [x] `docs/asp.txt` says a search answer carries the edges between the hits.
