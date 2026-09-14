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
review-status: passed
canonical-scope: one-document-serves-every-reader
footprint: ["src/document.rs","src/validation.rs",".cartridge/tests/unit/validation.rs",".cartridge/tests/integration/validation.test.ts",".cartridge/tests/fixtures/validation",".cartridge/docs/documents.md","src/source_search.rs",".cartridge/tests/unit/source_search.rs"]
needs:
- '@memo/one-document-serves-every-reader/document-identity'
commit: "45d5a54ab9da1a798cd9997af9a8c19bed8a1812"
---

# Invalid executable documents refuse before launch

Require kind, description, recipe, invocation mode and owner-relative execution base. V1 rejects executable imports/includes and filesystem-reading just expressions; probe the actual parser before implementing enforcement.

## Acceptance

- [x] Duplicate recipes and malformed fences report source locations.
- [x] Forbidden executable dependency forms cause zero process starts.
- [x] Valid frozen extraction produces the declared recipe and argv without re-reading mutable source.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. Public/native gates pass at 3251566e6c92439e4a32c5ce8b734e55726801ee; see proof.json and retained logs.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`; maximum five rounds.

Inventory facade revalidation: unchanged behavior and acceptance at memo 45d5a54; shared native registration is checked with its registered inventory module.
