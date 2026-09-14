# Terminal UI improvement plan — review

Canonical PRD: [@ui/improve-ui-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-ui-programme](../../../root/reviews/round-1/improve-ui-programme.md): reviewer 88/100; Reconcile. Combine existing transcript/palette claims with the human-context PRD and shared readiness/PTY contracts; avoid competing UI state sources.
  Original SHA-256: `17f3ace039b161e6c3056da9970146880bb829ee3db2b55a7c2ee5b5e276a4cd`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.


## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**. Roll-up still wanted; children exist and are open. Frontmatter key typo `capability-capability-owner`; no integration gate; child title for tool availability changed with its rebase.

Presented revision: prd.md SHA-256 `e692cc24fd06e83bf904e644af198ac8be2a17d4fa749a5b46693419f7e41761` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Roll-up is index-only. |
| Ownership and reuse | 15 | Frontmatter owner key malformed. |
| Dependencies and implementable slices | 18 | Needs resolve, acyclic. |
| Observable acceptance and baseline evidence | 12 | No integration gate or revision binding. |
| Failure, recovery and compatibility | 14 | No shared-footprint landing order. |
| Reviewer total | 75 / 100 | |

Findings: Roll-up on the stale `ui` board name; it had no integration gate or revision binding. Blocking: none. Below threshold.
Result: **FAIL (75/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `3e944533a8370a2bd9f780d098e1298673238a94185a2bd6d11224a8b4294546` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Roll-up rewritten to the current tui.ctg surface with an integration gate `just test tui` / `just check tui` from /Users/feb/dev/cartridge.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Clear roll-up purpose. |
| Ownership and reuse | 19 | Owner key fixed; not claimable. |
| Dependencies and implementable slices | 20 | All three needs resolve. |
| Observable acceptance and baseline evidence | 18 | Integration gate `just test tui`/`just check tui` at one recorded revision (-2: limitations list only). |
| Failure, recovery and compatibility | 17 | Landing order for shared palette/index/chat footprint (-3: one child is now dependency-free and may land first). |
| Reviewer total | 92 / 100 | |

Findings: Findings resolved. Non-blocking: none.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (92/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
