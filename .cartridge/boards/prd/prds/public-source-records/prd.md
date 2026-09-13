---
repo: /Users/feb/dev/cartridge/prd.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: prd
work-kind: leaf
review-round: 4
review-status: "passed"
canonical-scope: recursive-development-graph
needs: ["@prd/declared-source-edges"]
commit: "e4fd43461237e8068e63ba1c29f6722434177c6c"
---
# Native readers can index and exactly read permitted PRD records

Add a bounded native public-source projection to the existing PRD owner. Reuse its actual frontmatter parser and granted board scope. The trusted planner remains unchanged. This split inherits rounds1–2 from recursive-root-search; it is not a new review allowance.

- [x] A three-level fixture can independently index each board's local PRDs and read a selected record with exact source-byte revision, without descendant scanning or basename fallback.
- [x] Private or malformed-visibility records expose no path, title, text or private count; exact read refuses them identically to unavailable records.
- [x] Byte/count/depth/deadline, UTF8, symlink/FIFO, expected-revision and directory-change checks fail explicitly; no CLI, Memory, journal, event, spill or source writes occur.

Measured baseline: trusted scan currently returns private flags/visibility and replacement-decodes invalid UTF8; no public source-record operation exists. Exact baseline inputs and commands are in ../baseline.json. Root owns implementation after independent round3 review. Preserve authoritative files on every failure.
