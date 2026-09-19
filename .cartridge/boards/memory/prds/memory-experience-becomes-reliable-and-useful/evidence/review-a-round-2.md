# Independent review A — round 2

Reviewer: `/root/memory_plan_review_a`. Review-only, 2026-09-19. This bounded review reads only the revised parent, signals and retention PRDs against round-1 findings. No production or PRD changes, runtime mutation or new product test execution. Scores concern the plans, not product quality. Dimensions are user value/scope, ownership/reuse, dependencies/slices, acceptance/baseline, failure/recovery/compatibility; each is out of 20.

| Plan | Dimensions | Score | Result | Reviewed prd.md SHA256 |
| --- | --- | --- | --- | --- |
| parent | 19/19/19/19/19 | 95 | PASS | 5bbcc0a4f282d3bf242358f8c1714ece8da0ab4904baf5d0b7243e0de6d19022 |
| signals | 19/19/19/18/18 | 93 | PASS | cf24ca93773552f4d9b4d23a4bb1c26bdb5044114e089a78152fc2cf8b18026b |
| retention | 19/19/18/19/18 | 93 | PASS | 7e8eb1fb407d6d08dfaa58adf3e92db4f4a14f5bcb3d983914f116eb374bc953 |

No unresolved blocking findings in these three revisions.

Parent explicitly orders generic delivery behind a memory-owned classification contract and records existing claim blocks. This improves owner boundaries without taking over existing work. Its score remains conditional roll-up approval: the new contract child needs its own review and all children still need proof before collection. This reviewer does not approve the new child merely by approving its inclusion in the index.

Signals resolves both round-1 blockers: frozen-query is now an explicit hard prerequisite; canonical heat.rs and its test footprint are authorized, and proof explicitly reuses rather than duplicates decay policy. The existing frozen owner's read_only/spelling reconciliation and read-back owner's carve-out remain authoritative. Material limits: historical aggregate heat cannot be truthfully split retroactively, reinforcement counts cannot become literal read totals, and ranking improvement remains unmeasured until the specified frozen fixture executes.

Retention resolves the round-1 blocker by naming the real shared exact-ID serializer and public single/batch regression. The experience_fidelity_readback name is included by the specified RPC experience test filter. This now proves a consumer-facing boundary rather than only graph or ASP metadata. Material limits: schema rollback still requires a concrete compatible-reader fixture during specification; preserve representatives, do not pretend legacy readers understand new fidelity semantics, and keep exact archival policy outside this leaf.

Original round-1 history remains intact in /tmp/memory-plan-review-a.md. These scores supersede only the three concrete digests above; writer, evidence and merge retain their original revision-bound round-1 assessments. Passing plans remain open and unclaimed; existing ownership blocks are unchanged.
