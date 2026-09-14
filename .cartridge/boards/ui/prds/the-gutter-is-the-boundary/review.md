# the-gutter-is-the-boundary — review

Canonical PRD: [@ui/the-gutter-is-the-boundary](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-gutter-is-the-boundary](../../../root/reviews/round-1/the-gutter-is-the-boundary.md): reviewer 84/100; Reconcile. Keep as a roll-up of two current UI contracts; resolve active sidebar ownership and old lane evidence before claiming integration complete.
  Original SHA-256: `ee9409ad7951f13f0c7d90560c7bef982b00af9a1a35a7860fee2bd0f0498f8e`.

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

Reconciliation verdict: **REBASE**. Premise 'the gutter is the only boundary' came from decision the-terminal-grid-lives-in-pty, status superseded by the-agent-surface-preserves-the-visible-shell (indicators coexist, replace nothing). Source memo root--the-gutter-is-the-boundary already reframed it; its second child root--the-sidebar-slides-over-the-shell is an active claimed memo, not a PRD. One-child roll-up; no gutter indicators exist in tui.ctg yet.

Presented revision: prd.md SHA-256 `3ed6919df45e79bc646fa455b26ffe3a6c355ba667309e9584c2d89eec558a51` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 12 | Generic index with a superseded title premise. |
| Ownership and reuse | 14 | Owner fine. |
| Dependencies and implementable slices | 16 | One need resolves; second child missing. |
| Observable acceptance and baseline evidence | 10 | No integration check. |
| Failure, recovery and compatibility | 12 | None. |
| Reviewer total | 64 / 100 | |

Findings: Roll-up on the stale `ui` board name; it had no integration gate or revision binding. Blocking: none. Below threshold.
Result: **FAIL (64/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `7e4eaf0a77af96b035dbc244627ddf3250c88c27e851fcf247273afa975ce56b` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Roll-up rewritten to the current tui.ctg surface with an integration gate `just test tui` / `just check tui` from /Users/feb/dev/cartridge.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | States the coexistence outcome; one-child roll-up (-3). |
| Ownership and reuse | 18 | External claimed memo referenced, not reclaimed (-2). |
| Dependencies and implementable slices | 19 | Need resolves (-1). |
| Observable acceptance and baseline evidence | 18 | Integration check at one revision (-2). |
| Failure, recovery and compatibility | 18 | Records limitations (-2). |
| Reviewer total | 90 / 100 | |

Findings: Non-blocking disposition: merge this roll-up into the-inline-agent (coordinator/user action).
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (90/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
