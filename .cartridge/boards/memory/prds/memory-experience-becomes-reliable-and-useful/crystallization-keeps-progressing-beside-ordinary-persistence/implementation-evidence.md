# Writer implementation evidence

The implementation is independently verified and committed as `d9161cd2f3a363915c7a7d642a4955e7a3836065` and collected through the checked committed-snapshot lifecycle. Its baseline is `ff22be8dda3814e79b4d830c9904261b167af160`. [The source digest manifest](evidence/writer-source-digests.json) binds the final source files. No loaded runtime library was replaced; compilation used `/tmp/cartridge-memory-stack-baseline-target`.

## Implemented behavior

A per-store gate coordinates ordinary snapshot persistence, crystallization and maintenance divergence checks through epoch publication. Ordinary persistence releases graph locks for durable I/O, so unrelated dirty graph changes remain possible and survive the next save. Transactional stale-snapshot comparisons remain in place. Maintenance no longer automatically replaces dirty RAM after a real or apparent external advance.

The existing trace status and cycle snapshots expose writer readiness, automatic coordination or operator-required divergence. Divergent passes retain accepted inputs and dirty RAM before embedding. Authoritative epoch reads and transactional writes reject corrupt metadata; legacy advisory reads retain their compatibility behavior. The existing per-engine pass lock continues to exclude duplicate batches. No schema, delivery identity or receipt migration changed.

## Executed verification

- The initial actual-writer probe reproduced disk epoch 1 before RAM epoch publication, followed by safe refusal and a successful retry without reload. That establishes the controlled local race, not historical live causation.
- [Maintenance red evidence](evidence/writer-reconcile-red.log) records two new tests failing before correction: reconciliation bypassed the held publication gate, and a true external advance discarded dirty RAM.
- [Bootstrap verification](evidence/writer-reconcile-green.log) passed all four writer tests after correction. The actual flush callback is paused after durable commit; actual ordinary save and actual maintenance reconciliation wait correctly while graph reads and dirty mutation remain available. Separate stores progress independently.
- [RPC verification](evidence/writer-rpc-revised.log) passed all 11 experience tests. Named new tests cover ordinary-save/crystallization concurrency, retained external divergence, concurrent delivery/pass idempotency, and child-process exit without destructors after durable commit followed by restart and duplicate receipt recognition. Existing stale-snapshot refusal and rollback tests still pass.
- [Store-core verification](evidence/writer-store-core.log) passed all 77 unit tests. [The focused corruption test](evidence/writer-corrupt-epoch.log) proves failed writes retain durable rows and corrupt epoch metadata.
- [The affected commands regression](evidence/writer-command-reconcile.log) executed and passed, with 129 unrelated tests filtered out.
- [Strict Clippy](evidence/writer-clippy-revised.log) passed for all targets of bootstrap, RPC, store-core and commands with warnings denied. Cargo formatting and Git diff whitespace checks also passed.

## Remaining gates

[Independent verification passed](evidence/memory-writer-independent-verdict.json), and all 14 committed file hashes match the independent manifest. The root owner audit and isolation gates passed as attributed below. [Checked collection succeeded](evidence/writer-checked-collection.json) with committed verification true and workspace verification false. Parent quality, latency and controlled loaded-artifact integration gates are not claimed by these tests. The historical live advancing writer remains unestablished. External divergence requires explicit operator recovery; this implementation deliberately does not infer how arbitrary dirty RAM should merge into newer durable state.

## Integrated owner checks and workspace distinction

After the verified source fast-forward, the root coordinator ran `./task audit memory` and reported the hard gate passing, with existing soft stray/dirty findings retained. The root also ran the isolation gate and reported all 21 cartridges passing. This evidence is attributed to `/root`; the implementer did not rerun or reinterpret those checks.

The committed source is independently verified. Live README/help contain preserved unrelated changes and newer concurrent owner text. [The scoped integration record](evidence/writer-scoped-integration-recovery.json) distinguishes the independently verified candidate from those unverified live edits. No newer owner work was overwritten or collected into the writer commit.
