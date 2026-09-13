---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: rollup
review-round: 3
review-status: "passed"
canonical-scope: recursive-development-graph
needs: ["@landscape/recursive-development-graph/recursive-root-search/source-record-search", "@memo/recursive-source-search-facade"]
---
# Root search reads every permitted descendant record

Join the bounded census into root search and exact readback, preserving source-only versus callable availability.

- [ ] Root search finds distinct facts from all three fixture levels.
- [ ] Inactive documentation never becomes a callable service.
- [ ] Exact reads resolve the selected owner rather than another matching basename.

Original acceptance is preserved verbatim. Owner leaves implement the public PRD projection, Landscape search/read logic and actual Memo native route; this parent retains the mixed end-to-end proof. It inherits the existing two rounds and cannot complete from the library fixture alone. All leaf receipts and their current source footprints must be valid before composed validation. No records are copied, deleted, rewritten or activated by this feature.
