# Memory serves query and ingest through its own adapter — review

Canonical PRD: [@memory/memory-owns-its-tool/memory-adapter-core](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [memory-owns-its-tool](../../../../root/reviews/round-1/memory-owns-its-tool.md): reviewer 88/100; Revise. Reconcile the three memory-tool enhancement leaves with adapter retirement and specify the mixed-version interval and exact profile exposure snapshots.
  Original SHA-256: `4725b397890c58624ff423048e24c77dc8863973320aae8be1dc272549d0563a`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **DELIVERED**. Aligned with the parent's round-3 DELIVERED verdict, checked for this leaf on the route taken (memory.ctg `2e21dcc`, the events-model port, on main and ws branch `transport`):
- Query and ingest reach one store writer in process. `src/cartridge/src/lib.rs` routes the `memory`, `tool.memory` and `context.memory` events to one `memory()` service over a single `ENGINE` cell. Integration test `ingest_query_tool_and_context_reach_one_store_through_the_base` (`.cartridge/tests/integration/cartridge.rs`) ingests through `memory`, recalls through `tool.memory` and `context.memory`, asserts the store lock is held once and released on dispose.
- No recursion through the host: `tool_call` calls `memory()` directly ("no separate tool process involved"); the manifest declares no `needs`.
- Configured endpoint failure is explicit. Attached-owner settings are refused at apply (`a_bad_configuration_fails_the_cartridge_before_it_listens`), and `owner_attachment_absent_stale_and_operation_failure_are_explicit` is in `.cartridge/tests/unit/src/transport/src/owner_test.rs`. The standalone CLI remains at `src/main.rs`.
- The need `@gitfs/tool-results-interoperate` is `done`. The "retain memory-tool forwarding" clause is moot: root `9e4cde8` dropped memory-tool.

Presented revision: `prd.md` SHA-256 `0b45fa84563c2fbaeef51e66a8691ceef8b2781f4abc73d47cf3093cdfcda9fb`. Before: `6b722e9e98a25ce074e8455b54b1ef8440d7aa7a3908fe7ea5d117aae9b793bd`. Frontmatter only changed (review-round, review-status); the body is unchanged.

Agent score: not scored (delivered-pending-verification).
Findings: (1) The port `6889302` removed the old integration test `memory_persists_and_replacement_does_not_open_a_second_writer`. One-writer under *replacement* is no longer proven on the base; the new test proves a single writer and release on dispose only. The coordinator should either accept that proof or have a replacement check restored before marking done. (2) The starting-file link `memory.ctg/src/cartridge.rs` no longer exists; the file is now `src/cartridge/src/lib.rs`. It is left unedited because the item should close, not be reworked. `state:` is untouched.
Unresolved blocking findings: none.
Validation (cwd /Users/feb/dev/cartridge, read-only): `ls`/`rg` existence checks of the cited source and tests on memory.ctg main and ws/memory.ctg branch `transport` (both `2e21dcc`) and on the pre-port revision `c25af4d` (`git show`); `git show --stat 9e4cde8`; `rg --hidden memory-tool` over the composition excluding prd.ctg and target; needs resolution under `boards/<owner>/prds/<slug>/prd.md`; `shasum -a 256`. No product gates (`just test memory`, `just check memory`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator runs `just test memory` at `2e21dcc` and marks done on green.
