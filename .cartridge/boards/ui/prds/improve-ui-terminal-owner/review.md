# Display shared terminal ownership and cwd — review

Canonical PRD: [@ui/improve-ui-terminal-owner](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-ui-terminal-owner](../../../root/reviews/round-1/improve-ui-terminal-owner.md): reviewer 89/100; Revise. Depend on the settled PTY preemption/busy-shell contract; ensure the rendered ownership revision matches the next input admission check.
  Original SHA-256: `9dde7f2761e64e17e181ee3e1420d6eb37e84bbe7d08b4ef6dad2a719f450a1c`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.


## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**. Still wanted; not delivered: pty.ctg src/main.rs has only a boolean `agent_control` and `control` op (lines 203, 540-558); tui mirrors it via src/term.ts. Hard need @pty/improve-pty-input-ownership exists, open, review stale. Dead ui.ctg links and nonexistent tests footprint.

Presented revision: prd.md SHA-256 `b989d6a8621e9a60294aa6bb9dcc03cd70c69c9c29e91a77b105a42704dd5582` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Clear outcome. |
| Ownership and reuse | 12 | Dead links/footprint; starting files omit term.ts where control lives. |
| Dependencies and implementable slices | 16 | Need resolves but is unreviewed. |
| Observable acceptance and baseline evidence | 12 | Invalid gate. |
| Failure, recovery and compatibility | 15 | No behaviour when lease fields absent. |
| Reviewer total | 72 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead paths.
Result: **FAIL (72/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `a0de933fd332def3f55b842992c53a30dcb62b7b3ee8464eb81f5de916bfeaeb` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Clear. |
| Ownership and reuse | 19 | Names current control path. |
| Dependencies and implementable slices | 17 | Open, stale-reviewed pty dependency must land first (-3). |
| Observable acceptance and baseline evidence | 18 | Three checks; lease fields probed at landed revision (-2). |
| Failure, recovery and compatibility | 19 | Falls back to today's indicator; UI holds no ownership state (-1). |
| Reviewer total | 91 / 100 | |

Findings: Non-blocking: blocked on @pty/improve-pty-input-ownership passing its own review.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (91/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
