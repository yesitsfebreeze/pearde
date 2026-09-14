# fabric-landscape-ranked-fabric-query-times-out-isolate-and-fix review history

Plan: `@root/fabric-landscape-ranked-fabric-query-times-out-isolate-and-fix` — `prd.ctg/.cartridge/boards/root/prds/fabric-landscape-ranked-fabric-query-times-out-isolate-and-fix/prd.md` (ranked fabric query latency).
Scope: one observable outcome: a ranked `fabric` query returns within a bound or the item is retired as fixed; leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (no round-1 record for this scope exists under `boards/root/reviews/round-1/`).

Use the shared [review method](../../../../workflows/review-plan.md). Rounds are appended; earlier results are never rewritten. This record does not replace the item's implementation state.

## Round 1 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `f59eb0919564167f8315a18e6b71b0af4bc2e96ff54ef1cad203c3fb2557c627`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: the reported op `landscape` is now `fabric` (decision the-fabric-lives-in-core; memo.ctg/src/service.rs:116). Its acceptance item 'land the landscape->fabric rename' is DELIVERED (memo.ctg `1d2fa92`, `src/fabric_graph.rs`; memo.ctg worktree clean). The host no longer assembles the graph; memo does (`Service::fabric`, service.rs:267). Rewrote to reproduce-first against the stand-in host `memo.ctg/.cartridge/tests/integration/host.ts`, added a latency bound, a hung-listener case, gates and a retire path. Original SHA-256 `7fbf585bd92af803ef56fd0911c670585395c2c3f154c2f57fead1ecfa467e0d`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | Real user report on the intended entry point. -3: the hang was observed on the pre-port path and may already be gone; source query path (`fabric_graph::search`, `view::view`) is linear. |
| Ownership and reuse | 17 | Starting files exist in memo.ctg. -3: memo-owned work homed in the root board; rehome to memo recommended. |
| Dependencies and slices | 19 | No needs; single owner. -1: the MCP reproduction depends on the currently failing mcp smoke (`memo inactive`). |
| Acceptance and baseline | 19 | Four checks with a measurable 5 s bound, count parity and a retire outcome; gates `just test memo`, `just check memo`. -1: bound is a reviewer-chosen default. |
| Failure and compatibility | 18 | Fallback to plain `fabric`, no durable state, cancellation and output-cap behavior preserved, hung listener bounded by `event_timeout_ms`. -2. |

Agent score: **90/100 — PASS**.
Findings: Original text named a removed op and an already-landed rename, had no gate or cwd, and no frontmatter work-kind/review fields (would have scored about 70).
Unresolved blocking findings: none.
Disposition: keep; rehome to `@memo` recommended; retire if the first reproduction step shows no hang.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 1 / 4.
Next action: run the reproduction fixture first.

### Citation correction after the round above — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Coordinator correction: decision memo `the-fabric-lives-in-core` is outdated; cartridge.ctg `939e7d1` deleted core `src/graph.rs`, `src/fabric.rs`, `src/evidence.rs`. The fabric graph is `memo.ctg/src/fabric_graph.rs` and the evidence contract is the crate `memo.ctg/evidence` (memo `8d6a803`); owner memo, gate `just test memo`.
Change (citation only): replaced the link to that decision memo with source/commit evidence.
- Before: `Since then the op is `fabric` ([the-fabric-lives-in-core](../../../../../../.cartridge/memos/decision/the-fabric-lives-in-core.md))`
- After: `Since then the op is `fabric` (`memo.ctg/src/service.rs`; the host rewrite cartridge.ctg `939e7d1` removed the core graph, fabric and evidence modules)`
SHA-256 before `f59eb0919564167f8315a18e6b71b0af4bc2e96ff54ef1cad203c3fb2557c627`, after `e84fa1cf7545df65928fcd83996465e64c8978bbc0810a2f2dbc579e4ae3e8a1`. No acceptance, need, owner, gate or scope changed, so the score, result and round count above stand; no round consumed. Earlier mentions of that decision in this history refer to the outdated memo; the facts relied on (op renamed to `fabric`, landscape dissolved, fabric owned by memo) are verified in source.
