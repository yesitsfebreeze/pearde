# File and live context retain owner and freshness — review

Canonical PRD: [@landscape/landscape-composes-system-context/live-file-context-contributors](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [landscape-composes-system-context](../../../../root/reviews/round-1/landscape-composes-system-context.md): reviewer 85/100; Split. Freeze contributor/status/read contracts and baseline first; stage memory, live-state and file adapters separately and include their actual owner footprints.
  Original SHA-256: `a42df9f537bf0a35558deb445fce5cb9b51b47bde400c3f5e2b51e65b54fd2eb`.

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

Reconciliation verdict: **REBASE**. Aligned with the parent `landscape-composes-system-context` round 3 (REBASE, owner memo, providers per decision `a-cartridge-brings-its-own-surface`).
- **File/kernel half delivered.** `file-kernel-evidence-adapter` is done (`422c521`, historical landscape). `@memo/landscape-file-kernel-context-facade` is done (memo `a458148`). fs listens to `context.file` on the route taken (ws/fs.ctg `transport` `03f360e`), and memo composes `context.*` providers (`memo.ctg/.cartridge/docs/context.md`).
- **Live half not delivered.** No `context.session`, `context.terminal` or `context.route` event exists on main or the transport branches (manifests at sessions `118b784`, pty `c003065`, router `ab184a1`).
- **Stale text.** It cited `landscape.ctg` paths and `just test landscape`, and its needs named the two memo facades but not its own children. Its "Owner split" prose still gave Landscape the adapters.

Revision: repo and owner set to memo, which the coordinator listed among the parent rebases; needs now point at the file/kernel child (done), the memo file/kernel facade (done) and the live-owner roll-up; the live-owner facade moves down to the providers that consume it; integration acceptance and gate added.

Stale presented revision: `8d2bbec3f3721f55eb1e9c06f1573b7320209f7ec9ed34a3dee12b639fb0c21e`. Revised revision: `prd.md` SHA-256 `19659caf445797ca3fee62bc9cbaa40ea35dace9ca383d2e59bbe6ec136218f6`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One query with attributed file, kernel and live rows; the delivered half is stated. -1: overlaps the grandparent's integration acceptance. |
| Ownership and reuse | 19 | memo composes, providers are owner-owned, no copied protocol. -1: the board alias is landscape. |
| Dependencies and implementable slices | 18 | All three needs resolve (two done); acyclic. -2: the live roll-up is new in this round and its providers need a specced pty leaf. |
| Observable acceptance and baseline evidence | 18 | Exact readback states, changed-on-edit, absent-on-removal; real gates. -2: the live-row part of `context.test.ts` does not exist yet. |
| Failure, recovery and compatibility | 18 | Removal changes only the removed kind; shared budget preserved. -2: no rollback stated at roll-up level (it is delegated to the leaves). |
| Reviewer total | 92 / 100 | |

Result: **PASS**.
Findings: `original-leaf-prd.md`, `work-map-proposal.json` and the baseline files in this directory are historical and unchanged.
Unresolved blocking findings: none.
Validation (read-only): `ls`/`rg` existence checks on memo.ctg `83bf1ad` (main = ws branch `transport`: `src/context.rs`, `evidence/`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/{host.ts,context.test.ts}`), fs.ctg ws `03f360e` manifest, sessions.ctg `118b784`, ws/pty.ctg `c003065`, ws/router.ctg `ab184a1` (`src/context.rs`, `src/proxy.rs` `explain_routes`), ws/cartridge.ctg `ba198f4` `docs/transport.txt` and coordination `PORTING.md` (`--dir <dir> run <event>`); reads of the analysis files in context-baseline-corpus; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md`, footprint paths on main or ws, and every relative link; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: implement the provider leaves after `@memo/landscape-live-owner-context-facade`. Coordinator: rehome to memo with the grandparent and update work-map entries for the new children.
