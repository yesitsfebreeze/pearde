# the-inline-agent — review

Canonical PRD: [@ui/the-inline-agent](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-inline-agent](../../../root/reviews/round-1/the-inline-agent.md): reviewer 72/100; Rewrite. Opening outcome and checked tests still describe replies entering shell scrollback despite a superseding transcript-only contract; move old checks into history and state one current acceptance set.
  Original SHA-256: `287d31f87683514eb9b15c8c1932d22d60ed87569f1cee64960229575a258fab`.

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

Reconciliation verdict: **REBASE**. Base delivered in tui.ctg (persistent chat beside shell, approvals, handoff, palette per docs/README.md); tui decision inline-agent-overlay (one-shot overlay) and replies-into-scrollback are not the shipped route. Remaining children open. Redundant transitive need on the-gutter-shows-both-sides.

Presented revision: prd.md SHA-256 `d5563a9967bed8524eac139b120911da516c795912208b1b1cfcac70cd366272` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 14 | Generic snapshot text. |
| Ownership and reuse | 15 | Owner fine. |
| Dependencies and implementable slices | 15 | Needs resolve; one redundant. |
| Observable acceptance and baseline evidence | 10 | No integration gate. |
| Failure, recovery and compatibility | 12 | None. |
| Reviewer total | 66 / 100 | |

Findings: Roll-up on the stale `ui` board name; it had no integration gate or revision binding. Blocking: none. Below threshold.
Result: **FAIL (66/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `ec45873f945433543e61b267a41cb64e333af0fb2a28942ca3e46278ca29d5df` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Roll-up rewritten to the current tui.ctg surface with an integration gate `just test tui` / `just check tui` from /Users/feb/dev/cartridge.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | States delivered base and remaining scope. |
| Ownership and reuse | 19 | Clear. |
| Dependencies and implementable slices | 20 | Redundant need dropped; acyclic. |
| Observable acceptance and baseline evidence | 18 | Integration gate (-2). |
| Failure, recovery and compatibility | 17 | Limitations only (-3). |
| Reviewer total | 92 / 100 | |

Findings: Non-blocking: root decision the-agent-surface-preserves-the-visible-shell and tui decision inline-agent-overlay both describe surfaces current tui no longer matches; a decision refresh is outside this board.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (92/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
