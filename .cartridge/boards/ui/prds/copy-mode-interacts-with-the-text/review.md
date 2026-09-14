# copy-mode-interacts-with-the-text — review

Canonical PRD: [@ui/copy-mode-interacts-with-the-text](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [copy-mode-interacts-with-the-text](../../../root/reviews/round-1/copy-mode-interacts-with-the-text.md): reviewer 80/100; Revise. Refresh stale paths; add wide-character/aged-out selection, safe editor path handling, and memory-ingest acceptance rather than only memo-note acceptance.
  Original SHA-256: `a69c35afd5fcb15ded3d9207833dcfa8c83070caefc5ac2d78b15ee37e1379a8`.

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

Reconciliation verdict: **REBASE**. Still wanted; not delivered: tui.ctg only copies a drag selection via OSC 52/pbcopy (ui/terminal.tsx useSelectionHandler, docs/README.md line 82). Its correction path had tui speak memo and memory protocols, which conflicts with decision a-cartridge-brings-its-own-surface (2026-09-14, decided_by user); tui.ctg cartridge.json declares needs only agent/sessions/buffers/router/pty. The compliant route is an event: tui.ctg src/wire.ts has `gather`, and cartridge.ctg c9ef10b gives per-listener outcomes.

Presented revision: prd.md SHA-256 `fbc71bf43c5d2508f78526e0508849a7765cd045b6543f7e3bc5d6eaab15e8cc` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Three actions valid but copy/open/correct bundled. |
| Ownership and reuse | 10 | Dead ui.ctg links; correction design names sibling protocols. |
| Dependencies and implementable slices | 15 | Painter need resolves; memo/memory would be undeclared needs. |
| Observable acceptance and baseline evidence | 12 | Invalid gate. |
| Failure, recovery and compatibility | 14 | Partial-failure reporting stated; no fallback. |
| Reviewer total | 67 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: invalid gate; dead links; sibling-protocol correction path contradicts a-cartridge-brings-its-own-surface.
Result: **FAIL (67/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `cdf1505f2a04c59d198947449d7a74a2b412ad9e8e9ead439d05e95bbf88d9b3` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Coherent copy mode, but three actions and 314 words exceed the 300 target (-3). |
| Ownership and reuse | 18 | Reuses `gather`, pty control and existing selection; event definition/outcome surfacing in TS wire not yet probed (-2). |
| Dependencies and implementable slices | 18 | Painter need; listeners are owners' work (-2: no owner follow-up exists yet). |
| Observable acceptance and baseline evidence | 18 | Four observable checks with failing-listener fixture; `just isolation` added (-2 until fixtures exist). |
| Failure, recovery and compatibility | 19 | Additive, writes no data, never reports 'saved' (-1). |
| Reviewer total | 90 / 100 | |

Findings: Non-blocking: coordinator may open memo/memory listener items in their boards; consider splitting correction out if the probe shows event outcomes need host work.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (90/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
