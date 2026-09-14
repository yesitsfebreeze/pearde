# 18 — review

Canonical PRD: [@landscape/landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/route-context-provider](prd.md). Accountable cartridge: Router answers context with redacted route explanations (repo `/Users/feb/dev/cartridge/Router answers context with redacted route explanations.ctg`).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.
Inherited rounds: 1–2 from `@landscape/landscape-composes-system-context/live-file-context-contributors` (round 1: 85/100, Split; round 2: 94/100) via `live-owner-evidence-adapters`. Splitting does not reset the allowance.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE** (created by the round-3 split of `live-owner-evidence-adapters`; see that review for the program evidence). Route taken: owner-declared `context.<kind>` events on the events model (ws/cartridge.ctg `transport-design` `ba198f4`; memo `83bf1ad` `.cartridge/docs/context.md`); decision `a-cartridge-brings-its-own-surface`.
Presented revision: `prd.md` SHA-256 `e302feac9a24c391f95d80b5703f7b41b1e7e5fa1e44913059f61bd417588895outer` (new record).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | See note. |
| Ownership and reuse | 19 | One accountable owner; reuses the existing observation; no cross-cartridge protocol. |
| Dependencies and implementable slices | 18 | All needs resolve to existing PRDs; acyclic. |
| Observable acceptance and baseline evidence | 18 | Three checks against memo's documented provider shape, with owner gates `just test Router answers context with redacted route explanations`, `just check Router answers context with redacted route explanations` and `just isolation`. |
| Failure, recovery and compatibility | 92 | Named unavailable/changed/absent states; rollback removes only the event. |
| Reviewer total | Reuses the delivered `explain_routes` (router `src/proxy.rs`) with no live provider calls. The scope facade need is deliberately omitted (routes are not session-scoped). -2 on value / 100 | |

Deductions:  route rows describe configuration, not the caller's actual calls. -1 on ownership: the board alias. -1 on dependencies: none beyond a done item. -2 on acceptance: which routes count as configured is a probe item. -2 on failure: row size against evidence caps is unverified.
Result: **PASS**.
Unresolved blocking findings: none.
Validation (read-only): `ls`/`rg` existence checks on memo.ctg `83bf1ad` (main = ws branch `transport`: `src/context.rs`, `evidence/`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/{host.ts,context.test.ts}`), fs.ctg ws `03f360e` manifest, sessions.ctg `118b784`, ws/pty.ctg `c003065`, ws/router.ctg `ab184a1` (`src/context.rs`, `src/proxy.rs` `explain_routes`), ws/cartridge.ctg `ba198f4` `docs/transport.txt` and coordination `PORTING.md` (`--dir <dir> run <event>`); reads of the analysis files in context-baseline-corpus; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md`, footprint paths on main or ws, and every relative link; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator adds this item to the work map (rehome to the Router answers context with redacted route explanations board is allowed; it keeps this history).
