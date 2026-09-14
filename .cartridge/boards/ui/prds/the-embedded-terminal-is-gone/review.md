# the-embedded-terminal-is-gone — review

Canonical PRD: [@ui/the-embedded-terminal-is-gone](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-embedded-terminal-is-gone](../../../root/reviews/round-1/the-embedded-terminal-is-gone.md): reviewer 76/100; Reconcile. Its historical probe removes raw read/output paths while the amended outcome requires consumer parity first; rewrite the handoff around current PTY/UI consumers and tests.
  Original SHA-256: `ec97a6ef3be83e18ca8218e5d6376a60298e30972fe1dfaa9b95a60c26200510`.

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

Reconciliation verdict: **REBASE**. Still wanted (one emulator, pty-owned). tui.ctg ui/terminal.tsx and .cartridge/tests/integration/transcript.test.tsx (lines 3, 36, 116) still use EmbeddedTerminalRenderable; not delivered. Acceptance cited the latest-tool footer/status surface, which current tui (docs/README.md: chat/shell split) does not ship.

Presented revision: prd.md SHA-256 `fdd58f6ace1fe3bdc3f0e97b69bdb78ec39029ba2a94c82229a09946f4ae828a` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Parity-ledger outcome valid. |
| Ownership and reuse | 11 | Starting files wrong and in nonexistent ui.ctg. |
| Dependencies and implementable slices | 17 | Hard need on painter resolves. |
| Observable acceptance and baseline evidence | 12 | Invalid gate; acceptance names footer/status widgets absent from current tui. |
| Failure, recovery and compatibility | 15 | Recovery generic. |
| Reviewer total | 72 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead links; acceptance names a surface that no longer exists.
Result: **FAIL (72/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `b6bade4b4e76cb49c208eba358db6fb51a6c49a66d0409f39e77ffe8dd8e9905` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Bounded removal with named consumers. |
| Ownership and reuse | 19 | Names the three current consumers and keeps pty `read`/`commands` for non-UI callers. |
| Dependencies and implementable slices | 19 | Single hard need; stop condition if fallback still used. |
| Observable acceptance and baseline evidence | 18 | rg-based check plus behavioural parity; ledger captured in first step (-2 until run). |
| Failure, recovery and compatibility | 18 | Separate revertible commit; pty state untouched (-2: rollback of test migrations not detailed). |
| Reviewer total | 92 / 100 | |

Findings: Findings resolved by revision. Non-blocking: land strictly after the-ui-paints-the-grid.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (92/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
