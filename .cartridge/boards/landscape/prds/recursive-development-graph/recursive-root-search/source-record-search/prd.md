---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: recursive-development-graph
needs: ["@landscape/recursive-development-graph/recursive-source-census", "@prd/public-source-records"]
commit: "422c521aed170a4d098505c73469a1a59dccf49d"
---
# Census sources contribute bounded search hits with exact addresses

Join permitted census rows to owner-normalized public record indexes and exact reads. Reuse structured census addresses and existing Landscape lexical ranking; transport, parsing and record authority stay with owners. This split inherits rounds1–2 from recursive-root-search.

- [x] Actual PRD-generated records at three levels yield distinct body-fact hits and exact selected-owner reads despite identical basenames.
- [x] Private/malformed/changed owner replies cannot enter ranking or readback; inactive documentation remains source-only and never callable.
- [x] Source/record/input/output/deadline limits return bounded partial state while preserving usable sources; wrong owner/path/revision never falls back to another record.

Measured baseline: census sees all3 owners, but existing surface composition finds only the supplied ROOTAMBER record; BASEBERYL and PLUGINCOBALT return0 hits. There is no record callback or exact census read function. Use actual collected PRD helper/native fixtures. No durable cache, provider activation, Memo owner-grammar change or record copying belongs here. Root keeps the original parent incomplete until the real Memo facade is proven.
