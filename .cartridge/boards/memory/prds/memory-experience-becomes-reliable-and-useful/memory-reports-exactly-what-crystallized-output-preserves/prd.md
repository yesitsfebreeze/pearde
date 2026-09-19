---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/memory.ctg"
work-kind: leaf
footprint:
  - "src/graph/src/experience/metadata.rs"
  - "src/graph/src/experience/observe.rs"
  - "src/rpc/src/experience/view.rs"
  - "src/cartridge/src/asp/expand.rs"
  - "src/retrieval/piece/src/id_detail.rs"
  - ".cartridge/tests/unit/src/rpc/src/tests/server_query_test.rs"
  - ".cartridge/tests/unit/src/graph/src/tests/experience_test.rs"
  - "README.md"
  - ".cartridge/help.md"
---

# Memory reports exactly what crystallized output preserves

Publish an explicit fidelity contract for representative output, bounded samples and unavailable originals. Retain provenance of the chosen representative and explain which distinctions were discarded. Semantic condensation remains the default; this leaf does not create a parallel ledger or promise exact historical replay.

## Evidence

The probe merges six variants into one entity, one provenance reason and three examples. Examples are limited to 512 characters; only the first representative remains complete. Successful commit deletes the input row. See [investigation](../investigation.md).

## Acceptance

- [ ] ASP and exact-ID readback label full representative, truncated sample and unavailable original distinctly.
- [ ] More than three variants and long Unicode output cannot be presented as exact per-occurrence replay.
- [ ] Repeated equivalent evidence increments count without implying that missing original reasons or outputs can be reconstructed.
- [ ] Legacy groups receive an honest unknown/representative-only fidelity label; restart and schema rollback preserve the representative.

## Proof and recovery

Promote similar_contexts_merge_and_only_three_examples_survive, add truncation and legacy readback tests. Use the shared id_detail.rs serializer for single and batch exact-ID responses. Add a public RPC regression named experience_fidelity_readback in server_query_test.rs, exercising representative, truncated sample and legacy responses through single and batch gets. Run cargo test --locked -p graph -p rpc experience --lib and cargo test --locked -p memory_cartridge asp --lib from memory.ctg; the first command must execute the new named regression.

Do not invent lost bytes. Exact retention, if later required, needs its own bounded memory-owned content-addressed policy and explicit quota; it is not silently added here. Scope S.

## Dependencies and review

Hard prerequisites are in frontmatter; other related work is indexed in the investigation. All new work remains open and unclaimed. [Review](review.md) must reach 90/100 without blockers before implementation. Update owner README and help together; finish with ./task audit and ./task isolation from the composition root.
