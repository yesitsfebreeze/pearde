# Each capability ships its own executable documentation — review

Canonical PRD: [capabilities-live-with-their-owners](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [capabilities-live-with-their-owners](../../reviews/round-1/capabilities-live-with-their-owners.md): reviewer 84/100; Split. Create independently claimable owner migrations; connect shell work to PTY input ownership and preserve direct-FS parity before retirement.
  Original SHA-256: `990147ebe7129477ba49047e365acf0292465529cb96a5c5c1d6b91b6ddc58e6`.
- [the-tool-surface-is-search-and-shell](../../reviews/round-1/the-tool-surface-is-search-and-shell.md): reviewer 42/100; Rewrite. Unconditional FS deletion and removing its record conflict with current parity-first requirements; retain optional FS until consumer census and equivalent guarded writes justify retirement.
  Original SHA-256: `34037023dd8f9a7869a9203b0701eb6de964b2a5d8db5c25ba1af4689e8183de`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `c053f84e1c6e4eefe2863b9aa4d7cb6d9d05dc12f6d580629f4722eecbc51f84`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: prior text predated the transport host and a-cartridge-brings-its-own-surface (2026-09-14): help.md per cartridge and `cartridge help` now exist (19/19 `*.ctg/.cartridge/help.md`), `just isolation` exists. Revised the roll-up to that architecture, added an integration gate with cwd, a baseline and a failure/retirement rule. Pre-revision SHA-256 `fe9fafc26ea1aefef339d55cf9309bf43bc20079bef6bc1d8159caf23983a905`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 18 | Outcome still wanted and now framed against the accepted surface decision; delivered help-page part is named rather than re-planned. |
| Ownership and reuse | 18 | Six owner-board leaves; no parent implementation. -2: frontmatter key `capability-capability-owner` is malformed (board-wide, 68 files, no tool reads it). |
| Dependencies and slices | 17 | All six qualified needs resolve and are acyclic. -3: every child is still `stale-after-migration` and some name dead starting files (pty-document links `tool.rs`, `input.rs`). |
| Acceptance and baseline | 19 | Integration gate `just check`, `just test`, `just isolation` from the composed root, with SHA recording. -1: gate baseline is known red. |
| Failure and compatibility | 18 | Retired/exhausted leaves keep the parent open; failure attributed to the changed pin, previous pins retained. -2: no rollback of an individual child beyond reopening. |

Agent score: **90/100 — PASS**.
Findings: Pre-revision text lacked any integration gate or failure rule (would have scored about 81). Revision adds both. Children must be rebased in their owner boards before claiming.
Unresolved blocking findings: none.
Disposition: keep as roll-up.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: rebase the six child leaves in their owner boards; no implementation at this level.
