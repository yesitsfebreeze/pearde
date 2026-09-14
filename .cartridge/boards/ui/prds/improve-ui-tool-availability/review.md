# Explain tool readiness and policy in the palette — review

Canonical PRD: [@ui/improve-ui-tool-availability](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-ui-tool-availability](../../../root/reviews/round-1/improve-ui-tool-availability.md): reviewer 89/100; Revise. Share the defined readiness snapshot with MCP and the human-context view; a common schema must precede palette state wiring.
  Original SHA-256: `5dd4165a8941bd99586ec66a6d69483c3e00fcb20ed2e036bad34ab41b4335ba`.

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

Reconciliation verdict: **REBASE**. Still wanted; not delivered (palette.tsx renders bare tool names from `chat` `tools`). Its source was 'Landscape's generic readiness row' plus a policy revision via @mcp/improve-mcp-tool-readiness, which needs @landscape/... and @policy/improve-policy-explain: the landscape library is dissolved (the-fabric-lives-in-core) and policy knows no tool (a-cartridge-brings-its-own-surface). Rebased onto a tui-defined `gather` readiness event answered by owners.

Presented revision: prd.md SHA-256 `c372746ecd2fff5150cb6c9ed87610aedb9439963ed44d061813bcd687ae90a1` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | Valid outcome. |
| Ownership and reuse | 10 | Dead links/footprint; depends on dissolved Landscape. |
| Dependencies and implementable slices | 8 | Need chain rests on removed architecture. |
| Observable acceptance and baseline evidence | 12 | Invalid gate. |
| Failure, recovery and compatibility | 13 | Stale snapshot handling stated but no fallback. |
| Reviewer total | 58 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: dependency contradicts current decisions; invalid gate; dead paths.
Result: **FAIL (58/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `71f59a2077a6310bfbfe6735f8bbe872e226c99f24667c3324b33e542b564188` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Useful but real answers need owner listeners (-3). |
| Ownership and reuse | 18 | Event route complies; policy/MCP answer in their own work (-2: event contract unprobed). |
| Dependencies and implementable slices | 19 | No hard needs; fixture-proven (-1). |
| Observable acceptance and baseline evidence | 18 | Four checks incl. unknown readiness (-2 until fixtures exist). |
| Failure, recovery and compatibility | 18 | Read-only, revert restores list (-2). |
| Reviewer total | 90 / 100 | |

Findings: Non-blocking: needs changed (@mcp/improve-mcp-tool-readiness removed) - coordinator should update work-map and tell the mcp board its readiness PRD targets the dissolved Landscape row.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (90/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
