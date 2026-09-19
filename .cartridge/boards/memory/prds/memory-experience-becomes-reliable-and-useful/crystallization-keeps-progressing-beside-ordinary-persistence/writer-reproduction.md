# Advancing writer reproduction

This analysis uses committed baseline `ff22be8`. It follows the composed `fix-root-causes` principle: reproduce and instrument before selecting a correction. ASP lookup found `symbol:memory.ctg/src/bootstrap/src/lib.rs#save_graph_guarded`; the PRD contributor timed out but source lookup was available.

## Executed observation

A disposable standalone source snapshot instruments the existing `bootstrap::save_graph_guarded` immediately after successful `graph::persist::flush_snapshot` and before `graph.write().set_flushed_epoch`. A file barrier pauses only that publication. The RPC unit probe invokes the actual ordinary save in another thread and the actual `Server::commit_experiences` path through the existing drain fixture.

The named test `experience_probe_actual_ordinary_save_window_then_retry` passed twice, with one executed test and 105 filtered tests each time. With the barrier held, the store epoch was 1 and the shared graph epoch was 0. The crystallization commit refused the stale snapshot, rolled back its graph mutation and retained one acknowledged input. After releasing the ordinary saver, the same graph retried successfully without reload: one processed input, zero pending rows, store epoch 2.

This establishes the ordinary saver as an advancing writer in the controlled reproduction. It does not establish the writer responsible for historical live cycle 22. This particular local race is transient: the current error incorrectly requires reload even though completing the ordinary save permits normal retry. No permanent local wedge was proved.

## Persistence boundary findings

The registry persistence closure invokes `save_graph_guarded`, which snapshots under a graph read lock, releases that lock for the LMDB write, then publishes the returned epoch. Its transaction guard rejects old snapshots. Crystallization instead holds the graph write lock across its atomic graph/receipt commit and epoch publication. The protocols are not coordinated.

A truly external advance without publication into this graph can keep both operations refusing until an operator reconciles or restarts. The existing stale-refusal test proves retained intake and explicit reload recovery. It must remain passing; copying the live disk epoch into stale RAM would invalidate the guard. CLI `flush_guarded_retrying` does not publish its returned epoch, but its current callers own a local writer claim and a short-lived graph; source evidence does not establish this as a background-host wedge. Per-memory maintenance writes do not advance the full-store epoch, so they do not explain the reproduced epoch increment.

## Artifact and execution isolation

Disposable snapshot: `/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/memory-writer-repro-25k8_vg0`.

Target: `/tmp/cartridge-memory-stack-baseline-target`; no loaded target or runtime artifact was replaced. Full captured rerun output: `/tmp/memory-writer-repro.log`. Darwin emitted missing debug object warnings, but the named test executed and exited zero.

Probe file digests:

- `src/bootstrap/src/lib.rs`: `5e9f39c309f3f08b09b6926df9587b8280e6e47c375bb80bd7a091be78a46309`.
- `.cartridge/tests/unit/src/rpc/src/experience_test.rs`: `387f0abc2f7df250f29e889c9bd0f611aa51853ddf6afb469a40ecfb6c58bcbe`.

The probe instrumentation is deliberately not a proposed production API or implementation change.
