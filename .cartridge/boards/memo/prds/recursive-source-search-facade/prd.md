---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: recursive-development-graph
needs: ["@landscape/recursive-development-graph/recursive-root-search/source-record-search", "@prd/public-source-records", "@memo/one-document-serves-every-reader/document-projections"]
---
# The native Memo service exposes configured recursive source search

Bind the new Landscape library to an opt-in versioned native operation on the existing Memo service. Host configuration supplies roots; request/model arguments cannot grant paths, change source scope, or activate providers. Reuse PRD native operations and Memo's actual document reader. This split inherits rounds1–2 from recursive-root-search.

- [x] One real configured native query finds distinct public facts from three board levels and source-only cartridge documents; selected exact reads return only their owner and byte revision.
- [x] Disabled configuration or absent PRD grant is explicit; request overrides, private records and wrong/stale references fail without broadening access.
- [x] One deadline and bounded concurrent work preserve independent evidence and close resources; existing native v2 inventory, legacy landscape and tool schemas remain compatible.

Baseline: Memo's live landscape route still composes only registered entries/descriptors and surveyed memos; its document reader correctly rejects board prds paths and hierarchical owner strings. Preserve both behaviors. This adapter is required before the original root-search acceptance is complete; a library-only test is insufficient. No new service, parser, provider startup or persistent source cache.
