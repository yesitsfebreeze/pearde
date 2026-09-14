# Reopen completed run evidence after closing the panel — review

Canonical PRD: [@ui/improve-ui-run-history](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-ui-run-history](../../../root/reviews/round-1/improve-ui-run-history.md): reviewer 91/100; Keep. Reuses canonical sessions and proves editor preservation; expose retention-driven missing history explicitly.
  Original SHA-256: `f579e8ca5ccb79d6b843908a8e03fa6737dc8fb68e3cf80a689a97e7c2053ffa`.

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

Reconciliation verdict: **REBASE**. Still wanted; not delivered: tui.ctg ui/index.ts keeps one transcript in ui.state('transcript.v1') (survives module replacement per docs/README.md) and cannot reopen a past run from sessions. Hard need @sessions/improve-sessions-recovery is state done. Footprint tests under `tui.ctg/tests/` do not exist (tests live in .cartridge/tests/integration).

Presented revision: prd.md SHA-256 `fa0ebae1c9164ea3ac2e948eeaeaf4c6e58f10b0380cdfa85a80fba0a57d8d5b` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Clear outcome. |
| Ownership and reuse | 12 | Dead links and footprint paths; frontmatter owner key typo. |
| Dependencies and implementable slices | 17 | Need resolves and is done. |
| Observable acceptance and baseline evidence | 11 | Malformed acceptance (blank line, third item mixes constraints); invalid gate. |
| Failure, recovery and compatibility | 14 | Retention/missing history not covered. |
| Reviewer total | 71 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead footprint/test paths.
Result: **FAIL (71/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `59827ecc437bfde80d6632c833ac13fa1cf229efc477cebc1afff43ca645d915` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Bounded read-only reopen. |
| Ownership and reuse | 19 | Reads the sessions owner; existing tests extended. |
| Dependencies and implementable slices | 20 | Done prerequisite. |
| Observable acceptance and baseline evidence | 18 | Four checks incl. unavailable history (-2: sessions op to be probed). |
| Failure, recovery and compatibility | 18 | Read-only, disable keeps PTY/session data (-2). |
| Reviewer total | 93 / 100 | |

Findings: Findings resolved by revision.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (93/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
