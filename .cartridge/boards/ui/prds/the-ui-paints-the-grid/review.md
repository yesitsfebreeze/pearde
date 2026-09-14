# the-ui-paints-the-grid — review

Canonical PRD: [@ui/the-ui-paints-the-grid](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-ui-paints-the-grid](../../../root/reviews/round-1/the-ui-paints-the-grid.md): reviewer 79/100; Reconcile. Rebase old lane/core/builtin commands to current UI/PTy; define an actual redraw threshold and dropped-frame recovery instead of recording rows/s with no acceptance bound.
  Original SHA-256: `1bdec94748a95794e0ddad01e4cdea44fbf9b377287ebcc0e5bbc3a0326f7427`.

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

Reconciliation verdict: **REBASE**. Outcome still wanted: root decision the-agent-surface-preserves-the-visible-shell keeps 'a UI grid painter' over one pty-owned emulator. pty.ctg src/main.rs already serves `screen`/`viewport`/`frame`/`scroll` (lines 537, 621-630; memo root--pty-owns-the-terminal-grid status done), while tui.ctg ui/terminal.tsx still extends OpenTUI `EmbeddedTerminalRenderable` fed by `pump()` over `term` `read`. Not delivered. Paths and gate target the dropped ui.ctg name.

Presented revision: prd.md SHA-256 `4a9ce7b217bb3cd03c4b8ae267a4c93f645ad2b7352cac57b3d4e59ea6a87ec6` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Outcome valid; body still says 'rebase onto ui.ctg'. |
| Ownership and reuse | 10 | Starting files chat.ts/modules.ts are unrelated to painting and point at nonexistent ui.ctg. |
| Dependencies and implementable slices | 16 | No hard needs; external memos linked but pty-encodes-input status unresolved. |
| Observable acceptance and baseline evidence | 13 | Measurable performance bound, but gate `just test ui` is invalid. |
| Failure, recovery and compatibility | 15 | Generic recovery; no fallback renderer named. |
| Reviewer total | 70 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead starting-file links; wrong starting files.
Result: **FAIL (70/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `1947f49452ff8404b3a5c33d7e272a0c398cd88b47749a6f5ab2b26c13457e46` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome: paint pty frames; removal split to sibling. |
| Ownership and reuse | 19 | Names terminal.tsx pump, term.ts and the served pty ops; reuses existing fixtures/shell. |
| Dependencies and implementable slices | 18 | No hard needs; pty-encodes-input memo still `active` although ops are served and consumed, must be confirmed before claiming (-2). |
| Observable acceptance and baseline evidence | 18 | Four observable checks incl. skipped-generation resync and 20% bound; benchmark fixture still to be created (-2). |
| Failure, recovery and compatibility | 18 | Embedded renderer kept as degraded fallback; no durable data (-2: frame-format compatibility not versioned). |
| Reviewer total | 92 / 100 | |

Findings: Findings resolved by revision. Non-blocking: confirm root--pty-encodes-input completion; the chat/shell split in tui docs/README.md is the layout contract (the root decision's footer/Ctrl+F surface is not what tui ships).
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (92/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
