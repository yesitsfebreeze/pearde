---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: multimodal-content-reaches-the-graph
---

# One image format ingests into memory with its media and model identity

Memory ingests only text. `IngestArgs` (`src/rpc/src/server.rs`) and `Source` (`src/base/src/base_types.rs`) carry no media type. Embedding identity is one store-wide `EmbedStamp {model, dim}` (`src/graph/src/persist.rs`, checked by `check_embed_stamp` in `src/store/core/src/lib.rs`), which deliberately fails open at save.

Outcome, owned by memory: `ingest` accepts `media: {type: "image/png", path}`. It extracts text claims through the configured `reason` endpoint, but only when that endpoint declares image input (memory decision `memory-alone-owns-model-access`). Each claim records its source path, media type and extraction model. Other media types are refused. There is no UI and no second media store.

## Acceptance

- [ ] A PNG fixture and a mixed text+PNG fixture produce claims that `query` finds, and `get` reads each back with source path, media type and extraction model.
- [ ] Each of these returns a distinct refusal and writes no row, with no substitution of unlabelled text: unsupported type, malformed PNG, a reason endpoint without image input, failed extraction.
- [ ] A media ingest whose embedding model or dimension differs from the store stamp is refused before vectors are stored. Text ingest and save keep their current fail-open behaviour.
- [ ] Existing stores and text ingest stay compatible. Offline fixtures use the `test_support` HTTP stubs and contact no undeclared endpoint.

## Proof and recovery

First probe: confirm whether `src/llm/src/llm.rs` can send an image to the configured reason endpoint, and how an endpoint declares image input. If it cannot, stop and split out a provider-capability leaf. This is size L, so split after the probe. Tests go under `.cartridge/tests/integration/`. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check` and `just test`; neither has been run. Rollback: refuse `media`; text paths stay untouched.

## Dependencies and review

No hard needs. Sending private images to a provider that has not yet received them requires user approval. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.
