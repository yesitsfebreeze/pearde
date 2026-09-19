---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
---

# JEV grounds each model step in the shared ASP memory world

## Outcome

The next model step receives a fresh JEV judgement when completed tool evidence changes. JEV searches the shared ASP world, hydrates selected provider bodies, and returns validated closed-set answers with a cited decision summary. Memory supplies durable knowledge and recorded experience. Identical observation rounds reuse their assessment, and JEV-only results do not recursively trigger another judgement.

This extends the completed request-preflight integration and serves the JEV row in ranking/cartridges.md. “Whole ASP” means every published provider is eligible, with explicit coverage and finite retrieval budgets. It does not mean that one prompt contains the complete graph. Tool permissions remain with their existing owners.

## Acceptance

- [x] Memo, document and memory bodies can affect real JEV answers beyond their compact previews.
- [x] Changed, absent, stale and malformed evidence cannot silently authorize a decision.
- [x] Native, proxy and loaded Claude tool hooks automatically consume fresh decisions after tool observations without JEV recursion.
- [x] Validated answers, decision summaries and source references survive JEV reload; memory exposes runtime judgement experience through its current graph.
- [x] Owner checks, live grounding and connected-system proofs pass, with audit and isolation evidence.

## Proof and recovery

Starting surfaces are JEV retrieval/assessment, harness assessment cache, proxy tool observations, memo/memory ASP providers and workspace integration tests. The provider changes are bounded projections, with no memory store-format change or reset. Preserve concurrent migrations. Reverting scoped changes and rebuilding the previous native modules restores prior behavior.

Run `./task test jev`, owner checks for harness/proxy/memo/memory, and `CARTRIDGE_LIVE_SYSTEM=1 bun test ./.cartridge/tests/integration/jev-grounding.test.ts ./.cartridge/tests/integration/jev-workflow.test.ts ./.cartridge/tests/integration/asp-system.test.ts` from the composition. The live checks use actual stored authentication and isolated source fixtures.

## Review

Round 1 is recorded in the memo `note/jev-feedback-design-review.md`. Independent design_review approved plan digest `7798f09212d8d3cfbab854757506ae5008daa262530b4aa83a7cea31c1920d32` at 91/100 without blockers. Candidate A supplies provider-owned hydration; candidate B supplies stable tool-generation feedback. An unbounded graph crawl was rejected. Implementation acceptance remains separate from that design rating.

## Implementation evidence

The implementation hydrates up to sixteen selected provider entities, validates their revisions and every declared choice distribution, and preserves answers, summaries and source references across JEV reload. Native and proxy tool observations invalidate the assessment cache; unchanged observations and JEV-only results do not. Claude prompt, successful-tool and failed-tool hooks carry the same response into the model context. New Claude sessions must load the updated hooks.

JEV type checking and 49 tests with 556 assertions pass. The live connected workflow passes 88 assertions, including failed-tool refresh and unchanged-evidence reuse. Hook tests pass 69 assertions. The graph-native combined system gate passes 148 assertions: actual JEV decision `918bf6de-3ad3-48c9-bdb8-deb685ac17b2`, its source edges and exact retained memory occurrence were inspected; all four scope views rendered. All five owner hard audits and 21-cartridge isolation pass. Provider and native owner test details are recorded in `note/jev-feedback-implementation-proof.md`.

Independent implementation review confirmed that malformed choice validation, body revision checks, journal provenance validation and finding-only citations address its earlier blockers. Live timeout variability is tracked separately in `issue/jev-live-assessment-timeout.md`. The authored acceptance evidence does not imply collection: this PRD remains open and the working tree remains uncommitted alongside concurrent migrations.

The final independent live grounding run passes two tests and 171 assertions. Combined memo/memory and deep document changes reverse the actual answers, missing providers abstain or escalate, and normalized answers with both source references remain durable. The tests use explicit source identities and do not claim exhaustive retrieval recall.

## Sessions path compatibility handoff

The file-drift review found that the untracked root JEV reliability fixture calls Sessions touch with a relative path. The coordinator changed only that argument to path.resolve(cwd, "jev.ctg/src/assess.ts"), preserving the foreign file. Syntax and the existing normalized absolute target were checked; the opt-in real JEV test was not rerun. Preserve this incremental migration when landing the owned fixture, and rerun its integration gate with the identified Sessions artifact. The exact patch, original bytes and SHA bindings are retained in the Sessions file-drift loop report root-jev-fixture-handoff.md. Current modified fixture SHA-256 is e101e2aab73a74ebe26edec2e54b669105515868dd3813b8d9c18764321e30ec. This handoff does not certify the broader JEV implementation or alter its review score.
