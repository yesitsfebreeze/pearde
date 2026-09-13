---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: one-document-serves-every-reader
footprint:
- src/document.rs
- src/projection.rs
- .cartridge/tests/unit/projection.rs
- .cartridge/tests/fixtures/projections
- .cartridge/docs/documents.md
needs:
- '@memo/one-document-serves-every-reader/document-identity'
commit: "3251566e6c92439e4a32c5ce8b734e55726801ee"
---

# Readable projections hydrate bounded linked prose

Derive commands/docs/human views from one document; linked prose has a separate digest closure and depth/byte bounds.

## Acceptance

- [x] An edited prose dependency changes the hydrated projection digest.
- [x] Cyclic or excessive expansion reports truncation within the declared bounds.
- [x] References inside code blocks stay literal and private source bodies remain hidden.

## Proof and recovery

Start at [service.rs](../../../../../../../memo.ctg/src/service.rs), [record.rs](../../../../../../../memo.ctg/src/record.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test memo` from the composed root with the acceptance fixtures. Public test/check gates pass at 76800a23d90202645a2eca7d4ee5dcdca3951998; see proof.json and retained logs.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-document-serves-every-reader`; maximum five rounds.

Reverification: executable validation at3251566 adds a separate native action to shared document.rs; frozen identity/projection fixtures and acceptance remain unchanged.
