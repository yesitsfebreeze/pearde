# The UI presents the human view of the same landscape context — review

Canonical PRD: [@ui/human-context-is-the-same-document](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [human-context-is-the-same-document](../../../root/reviews/round-1/human-context-is-the-same-document.md): reviewer 90/100; Keep. Observable identity, no-execution-on-read, keyboard and PTY invariants are clear; reconcile the older inspector entry-point work during the initial probe.
  Original SHA-256: `f20a6e8f91c71da12ff2f061514507ae4dc46dfe22a43c29239e31de3a6306ed`.
- [the-context-inspector-opens-from-the-chat-editor](../../../root/reviews/round-1/the-context-inspector-opens-from-the-chat-editor.md): reviewer 88/100; Reconcile. Reproduce the missing entry point in current UI before changing it; share this bounded keyboard/escape contract with the human-context PRD.
  Original SHA-256: `6b7583cd7503db5d8c0bc3331ddb4ba8ef8892fbe5e82d2713e3e449b5c0ba7c`.

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

Reconciliation verdict: **REBASE**. Still wanted; no context inspector exists in tui.ctg (palette lists ui.actions() and agent tool names only). Unqualified need `memory-document-works-end-to-end` does not resolve in the ui board (exists only as @root). Title spoke of 'landscape context'; the landscape library is dissolved (decision the-fabric-lives-in-core). Reading docs/memo directly from tui would add undeclared sibling knowledge (a-cartridge-brings-its-own-surface); rebased onto a tui-defined `gather` event answered by owners.

Presented revision: prd.md SHA-256 `d8a2dc642a4ea3f61cffb3cab8dc5bdc7d06f98ce7f1903cdb3d03fe4c25bf25` (the 2026-09-13 migrated text, unchanged). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 15 | Valid outcome, vague source ('owner document'). |
| Ownership and reuse | 10 | Dead ui.ctg links; footprint `tui.ctg/tests` does not exist. |
| Dependencies and implementable slices | 8 | Dead unqualified need; root target itself depends on @landscape work. |
| Observable acceptance and baseline evidence | 12 | Invalid gate. |
| Failure, recovery and compatibility | 14 | Generic recovery. |
| Reviewer total | 59 / 100 | |

Findings: Stale after the ui -> tui rename (root commits 9e4cde8/bc2c190): every starting-file link resolves to /Users/feb/dev/cartridge/ui.ctg, which does not exist; the gate `just test ui` exits 2 with `Unknown owner: ui` (.cartridge/memos/routine/cartridge-development.md `_cargo` accepts `tui`). Blocking: dead need; invalid gate; dead links and footprint; stale landscape framing.
Result: **FAIL (59/100)**. Rounds used / remaining: 3 / 2.
Next action: one coherent rebase revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **REBASE** (revision applied). Presented revision: prd.md SHA-256 `e1f485633ff19acd8e875ade2baffc64120c62baf77e338275b738b5ed6d11da` (includes final frontmatter). Revisions: root 24aa2be (dirty working tree), prd.ctg 077e57a2 (dirty), tui.ctg 9fe1af9, pty.ctg 0db055d, cartridge.ctg c9ef10b, memo.ctg 9a1cf99, agent.ctg fad6d3b, sessions.ctg e9725e8.
Change: Gates rewritten to `just test tui` / `just check tui` from /Users/feb/dev/cartridge (tui.ctg/package.json runs `bun --conditions=browser test ./.cartridge/tests/`); links repointed to tui.ctg/pty.ctg.
Reviewer identity: agent (independent reviewer, plan refresh pass).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Inspector is useful but shows real content only once owners answer (-3). |
| Ownership and reuse | 18 | Event route complies with the decision; merges the context-inspector scope (-2: event contract not probed). |
| Dependencies and implementable slices | 19 | No hard needs; fixture-proven slice; root PRD kept as context (-1). |
| Observable acceptance and baseline evidence | 18 | Four checks incl. failing and stale listener states (-2 until fixtures exist). |
| Failure, recovery and compatibility | 18 | Additive, writes nothing (-2: no event versioning). |
| Reviewer total | 90 / 100 | |

Findings: Non-blocking: needs changed (hard need removed) - coordinator should update work-map; owner listeners (memo, docs) need their own items.
Validation: read current tui.ctg source (ui/terminal.tsx, ui/index.ts, ui/palette.tsx, src/chat.ts, src/term.ts, src/wire.ts, cartridge.json, .cartridge/docs/README.md, .cartridge/help.md), pty.ctg src/main.rs op table, root and tui decision memos, justfiles; a script resolved every relative link, qualified need and footprint path in the revised prd.md (all exist) and counted words. `just --list` inspected. No product gates were run.
User rating: not required under delegation; none supplied.
Result: **PASS (90/100)**. Unresolved blocking findings: none.
Rounds used / remaining: 4 / 1.
Next action: implementation may claim once hard needs are done; probe first as the PRD states.
