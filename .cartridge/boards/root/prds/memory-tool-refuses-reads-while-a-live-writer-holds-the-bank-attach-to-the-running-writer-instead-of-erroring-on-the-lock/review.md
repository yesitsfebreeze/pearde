# memory-tool-refuses-reads-while-a-live-writer-holds-the-bank-attach-to-the-running-writer-instead-of-erroring-on-the-lock review history

Plan: `@root/memory-tool-refuses-reads-while-a-live-writer-holds-the-bank-attach-to-the-running-writer-instead-of-erroring-on-the-lock` — `prd.ctg/.cartridge/boards/root/prds/memory-tool-refuses-reads-while-a-live-writer-holds-the-bank-attach-to-the-running-writer-instead-of-erroring-on-the-lock/prd.md` (memory reads under a live writer).
Scope: one observable outcome: a memory read succeeds while another process holds the bank; leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (no round-1 record for this scope exists under `boards/root/reviews/round-1/`).

Use the shared [review method](../../../../workflows/review-plan.md). Rounds are appended; earlier results are never rewritten. This record does not replace the item's implementation state.

## Round 1 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `0d78d6cd30dd89859b473828d2c7c54dbc637ea2635bcea96921bf12c0807258`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: memory.ctg was ported to the transport protocol (`9cc0f0b`, `c25af4d`): the cartridge serves `memory`, `context.memory`, `tool.memory` via `ctx.provide` on its cartridge socket and binds no memory-RPC endpoint (no `serve_memory_rpc_loop` in src/cartridge.rs). Old paths `transport/typed.rs Endpoint::memory()` moved: `Endpoint::memory` is memory.ctg/src/transport/src/endpoint.rs, the typed endpoint lives in cartridge.ctg/src/transport. memory.ctg/.cartridge/docs/owner-attachment.md documents explicit attachment that 'does not discover or start a daemon' and keeps exclusive-writer refusal without `owner`; the original option (a) auto-attach contradicts that contract. Rewrote with a probe-first step, explicit-attachment default, refusal and read-only-ingest checks, gates and a stop condition that escalates discovery to a question. Original SHA-256 `ce89aca36fc97c98c6a5a956c7e531f84da8522fbdbfc172527e184f87a4c3e5`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 18 | Real failure on a primary tool. -2: the recommended default requires the user's second composition to configure `owner`, not zero-config. |
| Ownership and reuse | 17 | Reuses `ServiceConfig::Attached`, `read_observed`, existing owner tests. -3: memory-owned work homed in the root board; rehome to memory recommended. |
| Dependencies and slices | 18 | No needs; one owner. -2: the endpoint choice (cartridge socket vs memory RPC) is left to the first probe. |
| Acceptance and baseline | 19 | Four checks including refusal and read-only ingest; gates `just test memory`, `just check memory`. -1: 'hits for facts the writer ingested' needs a fixed fixture fact. |
| Failure and compatibility | 18 | No local fallback on owner failure, local path unchanged, stop condition before reversing the documented contract. -2: no statement on socket permissions across users. |

Agent score: **90/100 — PASS**.
Findings: Original text cited moved paths, a stale 'binds none' claim, an unresolved (a)/(b) choice and an ingest acceptance incompatible with read-only attachment (would have scored about 72). memory.ctg has no AGENTS.md, so the old routine's worktree rule is not cited.
Unresolved blocking findings: none.
Disposition: keep; rehome to `@memory` recommended. If the probe shows discovery is required, set needs-decision.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 1 / 4.
Next action: run the endpoint probe with a disposable writer.
