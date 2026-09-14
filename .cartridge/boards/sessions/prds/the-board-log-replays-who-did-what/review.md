# the-board-log-replays-who-did-what — review

Canonical PRD: [@sessions/the-board-log-replays-who-did-what](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-board-log-replays-who-did-what](../../../root/reviews/round-1/the-board-log-replays-who-did-what.md): reviewer 86/100; Revise. Specify atomic ordering between channel commits and telemetry, gap reporting after crashes, and scoped read access; avoid claiming one total order from separate unsynchronized appends.
  Original SHA-256: `0e2e588bf8b07c111c6485d1a6f5b737ebce6e23359724c1d9aaff75ad6d96d1`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. Not delivered: lines carry only per-channel `seq`. Changed: the transport host provides publisher-owned channels with bounded replay and `subscribe since` plus `cartridge follow <cartridge>.<channel>` (`cartridge.ctg/docs/transport.txt`) and a `trace` id on every frame (`cartridge.ctg/src/trace.rs`). Under `a-cartridge-brings-its-own-surface.md` sessions cannot own run, tool-call or spawn records of other cartridges; the trace id is the join.
Stale revision: `5fcef079acb5e795ce97bea2a03d28745b8a9b017df2d90305c64a35eb936477` (dead start link; "telemetry projection" and "global journal sequence" named no current mechanism).
Presented revision: prd.md SHA-256 `c1003f7a7020d3d16f77cdb872d44d32ae2c12f5c1a52c20887b0bb6141d5526`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: scope-wide sequence + trace stamped in the sessions snapshot and published on a sessions channel; crash rebuild from snapshot; scoped subscription; cross-owner total order excluded; shared footprint noted instead of a soft need.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Followable board order with a trace join. -3: the original "every run, tool call and spawn" story is now a cross-owner join left to consumers. |
| Ownership and reuse | 18 | Reuses transport channels and trace. -2: whether a Rust node can read the inbound trace is a probe. |
| Dependencies and slices | 19 | No hard needs; sequencing with sibling leaves stated. -1: shared `channels.rs`. |
| Acceptance and baseline | 18 | Order, crash rebuild, named retention gaps, scope isolation, legacy `unsequenced`. Current gate baseline: `.cartridge/memos/note/release-status.md` records 8 failing sessions workspace tests; the plan requires naming them before judging new failures. -2. |
| Failure and compatibility | 18 | Snapshot authoritative; channel derived. -2: snapshot growth from per-event metadata against the 8 MiB scope cap not bounded. |
| Reviewer total | **90 / 100** | |

Result: **PASS**. Blocking findings: none.
Validation: file existence; transport docs read; `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: probe inbound trace availability, then specs.
