# Source-search implementation proof

Source commit: `422c521aed170a4d098505c73469a1a59dccf49d` in Landscape. Only the four reviewed footprint files changed. The checkout is clean and held for coordinator collection. Exact source, dependency, executable and log digests are in [proof-inputs.json](proof-inputs.json).

Independent round-3 plan review: `/root`, 95/100 PASS. Independent source audit checked exact selected-owner authority, privacy/hash validation, conservative budgets, per-source failures, deadline/cap behavior and existing Graph ranking equivalence. Its remaining query length-before-trim correction was applied before final gates; no requirement or public gate changed.

| Acceptance | Executable evidence |
| --- | --- |
| Actual three-level owner records and exact same-basename reads | `actual_prd_helper_three_level_bytes_and_fresh_edits_remain_source_owned` imports the collected PRD helpers with pinned source/manifest/lock hashes. Three real board owners return distinct body facts and exact BOM/CRLF bytes. `actual_native_owner_search_and_selected_read_never_activate_discovered_sources` uses real Runtime → PRD native calls for declarations, indexes and reads; selected plugin text matches source bytes. |
| Private, malformed, foreign and stale evidence refused | The real private records never enter owner indexes. Independent consumer tests mutate index/read root, path, visibility, source revision, record hash, title and byte count. No invalid index induces a record call. Exact-reference tests prove zero-call rejection and single-owner changed/unavailable behavior without fallback. |
| Full text, bounded hits, no activation | A unique body fact after 6000 UTF-8 bytes ranks while its preview remains at most 2048 bytes. Three distinct address identities and deterministic owner ties remain. Runtime metadata never sets callable true. The real native fixture grants an explicitly source-only poisoned cartridge root with an unavailable record adapter and retains usable PRD hits; no Memory or source-state effects occur. |
| Counts, bytes, wire size, partial state and one deadline | Tests cover source/record/input/item/hit/read/search caps, rejected-read attempts and rejected body-byte accounting, malformed queries, partial-index truncation, alias deduplication, and unavailable-source preservation. A paused-clock fixture spends time on index plus read then drops the pending next callback at the shared deadline while retaining the completed hit. |
| Fresh owner data and immutable results | The helper fixture changes one real board record, reruns actual owner index/read helpers, refuses the old reference and finds the new body fact; its original serialized result remains unchanged. The separate facade/refresh work remains required for end-to-end native Memo behavior. |

Final public gates, from the runtime checkout with the designated target:

- `just test landscape`: **67 passed**, including 11 new source-search tests and the existing 9 census tests.
- `just check landscape`: **passed**.
- `just test memo`: **77 passed**.

The timer fixture initially expected an exact 30 ms wakeup and observed 31 ms because Tokio timers use millisecond ticks. The retained failure log and final assertion record the bounded 30–31 ms wakeup; timeout status, exactly three callbacks, a retained completed hit and pending-future drop remain mandatory. Synchronous work cannot be preempted; final deadline checks prevent late complete success. Callback cancellation does not imply remote rollback.

No Memo native route, tool schema, owner parser, Sessions source, shared work map, lifecycle transition or receipt collection was changed by this leaf. The original recursive-root-search parent remains incomplete until the separate Memo facade is implemented and its composed acceptance passes. Earlier Landscape receipts that compile the module need the two new transitive Rust paths recorded in proof inputs; coordinator owns those refreshes.
