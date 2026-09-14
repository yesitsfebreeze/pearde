# Inherited review history

Rounds1–2 remain inherited from @landscape/landscape-composes-system-context/live-file-context-contributors. Historical source review85 split, migration review94 before owner split. Parent review SHA256 `44098ce7820bc34cc3bcc85575b6ec5401fdb5d30a65f282db8bbb1c534db0bd`. Maximum five rounds; a concrete independent round3 is required before source changes.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **REBASE** (with a split).
- The stale leaf asked one Landscape adapter to call session, terminal and router APIs through a "canonical collector". That contradicts decision `a-cartridge-brings-its-own-surface` (2026-09-14): memo must carry no sibling protocol, and each owner offers `context.<kind>` itself (the done work `invert-memo-context-sources`; fs `context.file`, memory `context.memory`).
- The dependency direction is inverted, as the coordinator directed. The consumers of the scope contract `@memo/landscape-live-owner-context-facade` (passed round 3) are now the providers, not memo.
- The need on the landscape `context-contributor-contract` is dropped; that contract now lives in `memo.ctg/evidence` and memo's documented provider shape.

Owner evidence for the split:
- sessions `src/context.rs` `context_metadata` (`@sessions/context-session-metadata` done `92240c6`; token-authenticated today).
- pty `src/context.rs` `pty.context.v1` (`@pty/context-terminal-metadata` specced).
- router `src/proxy.rs` `explain_routes` (`@router/improve-router-route-explanation` done `4ad9cd3`; per request, not per session).

One leaf spanning three repositories breaks the one-accountable-cartridge rule. This item therefore becomes a roll-up with three same-board children (`session-context-provider`, `terminal-context-provider`, `route-context-provider`), each with its owner's repo and gate and ready to rehome to its owner's board. All original acceptance themes are kept: distinct owner identities, read-only allowlists without activation or payload, exact revision readback, and named unavailable/timeout states under one budget.

Stale presented revision: `505f89ff3b62a09ff5cc41964bdcd06c878e2955a73ac8a9481a13537c0e1ca2`. Revised revision: `prd.md` SHA-256 `c0a9c5779e1f06a6292dd7241911f90f9ed1741be56f6572483ddff56ecbb08c`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Live evidence in one scoped query; roll-up only. -2: route rows are not session-scoped, so "caller's scope" applies to two of three kinds (stated in the leaf). |
| Ownership and reuse | 19 | Owner-provided events reusing delivered or specced metadata operations. -1: children sit on the landscape board pending rehome. |
| Dependencies and implementable slices | 18 | Three child needs resolve; the children need resolving owner PRDs; acyclic. -2: the terminal leaf waits on a specced pty item. |
| Observable acceptance and baseline evidence | 18 | One prepare with three kinds, timeout/absent isolation, no payload. -2: integration fixture not yet written. |
| Failure, recovery and compatibility | 18 | A failing provider affects only its kind; rollback per leaf. -2: the trust model for the forwarded scope is a probe item in the session leaf, not settled. |
| Reviewer total | 91 / 100 | |

Result: **PASS**.
Unresolved blocking findings: none.
Validation (read-only): `ls`/`rg` existence checks on memo.ctg `83bf1ad` (main = ws branch `transport`: `src/context.rs`, `evidence/`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/{host.ts,context.test.ts}`), fs.ctg ws `03f360e` manifest, sessions.ctg `118b784`, ws/pty.ctg `c003065`, ws/router.ctg `ab184a1` (`src/context.rs`, `src/proxy.rs` `explain_routes`), ws/cartridge.ctg `ba198f4` `docs/transport.txt` and coordination `PORTING.md` (`--dir <dir> run <event>`); reads of the analysis files in context-baseline-corpus; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md`, footprint paths on main or ws, and every relative link; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2 (inherited 1–2 from `live-file-context-contributors`).
Next action: coordinator adds the three children to the work map and rehomes each to its owner's board; the session provider is first-ready after the memo facade.
