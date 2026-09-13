---
kind: work
level: 10
status: done
estimate: 4h
description: Route internal inference through mine and compact eligible intake automatically by project and kind
read_when: "implementing mine-backed internal model access or automatic intake compaction"
---

# mine-backed-intake-compaction

## Do

User approved routing all memory model traffic through mine, including pinned embeddings and reasoning used by compaction. Preserve the configured embedding model and vector dimensions; never switch embedding spaces through an arbitrary model fallback. Use mine provider routing for reasoning, retain intake on provider failure, and avoid overwriting existing uncommitted mine changes.

User approved configurable defaults: 20 committed unchanged intake memos per project and kind trigger compaction, checked once a minute, with bounded batches and a daily low-volume flush. Serialize manual and automatic runs, revalidate sources before deletion, and protect uncommitted intake and condensed outputs. Drain the full eligible intake only after these safety checks pass.

Integrated main `026b6dc8` includes the hub-owned mine completion path, pinned embedding callback/status propagation and bounded scheduler. `just check` passed; 308 process-isolated tests across commands/config/mine/llm/hub/transport passed; memo and one-client gates passed. Release installation from integrated main completed. The full eligible drain moved 475 memos byte-for-byte (record commit `38727d9`), leaving 41 intake files: index, 39 uncommitted/changed memos, and one unsafe `kind: intake`. Post-drain memo gate passed.

Runtime activation was blocked by an unreadable store: `memory health` reported embedding stamp format version 11. A consistent read-only LMDB snapshot (`mdb_copy`) showed 220 hot memory rows all at v14, 352 cold rows at v11 (5) and v12 (347), and meta embed at v11 with graph/epoch at v14. The current build read only v14/v13, so `scan_with` would have skipped the old cold rows.

The repair landed on main (`86983b2a`): frozen v11/v12 cold-row decoders in `legacy.rs`, arms in `decode_cold`, and `READABLE_VERSIONS` extended to `[13,12,11]` so the layout-stable v11 embedding stamp decodes. Verified on the snapshot: `snapshot_cold_rows_and_stamp_all_decode` decodes all 352 cold rows and the v11 stamp; 61 store_core tests and `just check` pass.

Runtime activation completed with the user's approval. The new binary was installed, the memory daemon unloaded, and `memory migrate` rewrote 221 memories and 352 cold rows to v14 (re-inventory confirmed all rows and meta at v14). The daemon restarted and now serves: `memory health` shows `embed: qwen3-embedding:0.6b (dim 1024)` (the stamp decodes), 221 memories / 25738 thoughts, and the tick queue processing. `memory models status` confirms mine routing is live at `http://127.0.0.1:4140`. The automatic compaction scheduler runs in the daemon; the intake is already drained, so it has little to fold. See [[intake-compaction-policy]] and [[persistence]]. The earlier standalone-proxy implementation is retained on `mine-auto-compact` as unlanded history, not installed.

The Check ran on 2026-09-09 in lane `mine-backed-intake-compaction`: 205 process-isolated nextest tests across mine, llm, hub and commands pass, including `pinned_protocol_body_and_key_reach_only_exact_endpoint` (authenticated model-pinned forwarding), `redirects_errors_and_dead_endpoints_never_fallback` (no cross-model embedding fallback), `schedule_threshold_daily_and_bounds` (19 vs 20, same-day crossing, daily flush, batch bounds), `lock_serializes_canonical_aliases_and_releases` (concurrent-run refusal) and `landing_preserves_existing_and_changed_sources` (dirty-file preservation). Failed-fold retention had no test and now does: `a_failed_fold_retains_the_intake_for_retry` drives `compact` with a completion that errors and asserts the report says retained, the intake file, the absent stamp and the absent output directory. `just check` and the memo gate pass in the lane; main was fmt-red at `f10f4b53` in `commands_exit.rs` and `lib.rs` and the lane carries the rustfmt fix. Live: the scheduler folded on its own — nine per-kind stamps under `memos/intake/` dated 2026-09-08, the intake down to six entries. Eligible drain: three committed unchanged memos await the next flush. Protected and untouched: `_index_.md` and `new-work-is-on-the-plan-by-default.md`, both uncommitted or changed, plus `index.json`.

## Check

Run isolated tests covering mine reasoning routing, authenticated model-pinned embedding forwarding, no cross-model embedding fallback, threshold boundaries, same-day threshold crossing, daily flush, concurrent-run refusal, dirty-file preservation, and failed-fold retention. Run `just check` and the memo gate in the lane. Verify live compaction only after the routing and preservation tests pass; report protected intake separately from the eligible drain.
