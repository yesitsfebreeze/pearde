# the-panel-switches-to-a-sub-agent — review

Canonical PRD: [@ui/the-panel-switches-to-a-sub-agent](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-panel-switches-to-a-sub-agent](../../../root/reviews/round-1/the-panel-switches-to-a-sub-agent.md): reviewer 85/100; Revise. Add per-session unsent draft retention, child termination during selection and approval routing after switching; preserve the foreground editor.
  Original SHA-256: `d51bd59fb2f251f11e85d55f55163eab114760e86ef67a5a0d38eee8095722d9`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.


## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**. Still wanted; not delivered: tui.ctg ui/index.ts binds one `session.v1`; Ctrl+V `channel` switching between typed and voice conversations is the reusable pattern. Hard need @agent/the-agent-spawns-wakes-and-owns-sub-agents exists, open. Dead ui.ctg links, invalid gate.

Presented revision: prd.md SHA-256 `f6ee718d97c7213f206f38a91622293f96fd4cae7541ef87c302ed374fb81e2e` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Valid. |
| Ownership and reuse | 11 | Dead links; no reuse of channel switch. |
| Dependencies and implementable slices | 16 | Need resolves, open. |
| Observable acceptance and baseline evidence | 12 | Invalid gate. |
| Failure, recovery and compatibility | 14 | Generic. |
| Reviewer total | 70 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead links.
Result: **FAIL (70/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `ca0fb1bb965863585306245771ccb5746727b0d239d0c94888e66804a485f072` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Clear. |
| Ownership and reuse | 19 | Reuses Ctrl+V channel switch. |
| Dependencies and implementable slices | 18 | Open agent dependency (-2). |
| Observable acceptance and baseline evidence | 18 | Three checks (-2 until fixtures). |
| Failure, recovery and compatibility | 18 | No-children behaviour unchanged (-2). |
| Reviewer total | 91 / 100 | |

Findings: Non-blocking: blocked until the agent sub-agent leaf lands.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (91/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
