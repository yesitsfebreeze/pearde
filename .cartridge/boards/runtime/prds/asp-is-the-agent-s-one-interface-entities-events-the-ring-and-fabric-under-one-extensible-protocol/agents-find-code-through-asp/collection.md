---
commit: 147fecf88a3a5ac14534be9573508a96ced2908a
spec-digests: {"spec01.md":"3bcc088f7cc2b27522400fb48ef296d1241dbe3bcbc6bb0cf375458dad7f0978"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/agents-find-code-through-asp/specs/spec01.md: exit 0

Command SHA-256: f4f75866fc44c895438c8dc24189daf9e12f9350fd9bcc828c0a614b3e1e7b98

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/integration/asp-code-lookup.test.ts:
(pass) tool.asp alone answers who-calls, a file's outline, and where-used [1905.36ms]

 1 pass
 0 fail
 11 expect() calls
Ran 1 test across 1 file. [1.93s]
`system`

One line per memo: the rule, the memos it links, the path of its body. When a line is not enough, `memo read <path>` returns the body; a link is a memo name read the same way.

- A cartridge owns one capability, declares its whole surface in cartridge.json, ships its own README and help page, and is not done until `just audit` and `just isolation` report nothing for it. Links: [[a-cartridge-brings-its-own-surface]], [[a-cartridge-is-a-cli-tool-for-the-agent]], [[audit-cartridges]], [[cartridge-readme-stays-current]], [[check-cartridge-isolation]], [[no-redundant-comments]], [[the-surface-is-the-orchestrators-doors]]. Body: system/vision.md
- The router answers whatever a reachable provider can answer: it adapts the request to each route's accepted shape, and never shelves a route for a shape it could have rewritten. Body: @router/system/vision.md
- Own the record through the memo tool: read @memo/type/type.md for the protocol, `types` for the kinds, declare a kind before its instances, write only through the tool. Body: system/memos.md
- Resolve memos once per task and intended usage; reuse matches until scope or evidence changes, and never treat a match as authorization. Body: @memo/system/resolver-guidance.md
- Use targeted cartridge help once for an unfamiliar capability; task discovery already does this, and a known page needs no repeated index. Body: system/help.md
- Start unfamiliar repository work with just task and a short goal; reuse its evidence, read only relevant results, and prove behavior with probes. Links: [[@memo/note/program-map.md]], [[start-task]]. Body: @memo/system/program-entry.md
- Use documentation already found by task discovery or targeted help; ask docs list only when the needed documentation is still unknown. Links: [[@docs/note/documentation-service.md]]. Body: @docs/system/docs-entry.md
- PRD owns planning, specifications, dependency schedules and work orchestration. Body: @prd/system/prd.md
- When the answer is not on this disk, use the web tool to search or fetch it, and name the source URL in the answer you give. Body: @web/system/reach-the-web-and-name-the-source.md
- Every cartridge ships a README.md and a .cartridge/help.md, and a change to its behavior or surface updates both in the same change. Links: [[audit-cartridges]], [[vision]]. Body: system/cartridge-readme-stays-current.md

<system-reminder>
Current working directory: `cwd`

Current date: `date`

`environment`

`terminal`

Context anchor (quote it when recording a correction): `anchor`

The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

`instructions`
</system-reminder>

- No legacy retention: superseded code, docs and fixtures are deleted in the same change; git is the archive. Body: system/delete-superseded-work.md
- No monoliths: one file per responsibility. A file that answers for two things is split before more is added to it. Body: system/one-file-per-responsibility.md
- The board says what is blocked, in progress or possible; ranking/cartridges.md says in what order and why. After every finished task run rank-cartridges, and plan the board top down from the ranking. Links: [[rank-cartridges]], [[vision]]. Body: system/plan-the-board-from-the-ranking.md
- Inspect the user's pane before interacting with it; use ordinary shell tools for repository work and preserve running programs. Links: [[start-task]]. Body: system/terminal-agent.md
- Ask ASP first for code lookup; search text with rg and fd; rewrite code structurally with ast-grep and text with sd; query JSON with jq, YAML and TOML with yq, GitHub with gh. Body: system/shell-tools.md
- Reply terse in the terminal; write anything persisted in whole sentences; never compress a negation, number, unit, error string or command. Links: [[@prd/persona/root--dispatcher.md]], [[the-register-is-chosen-by-surface]], [[unslop]], [[writer]]. Body: system/register.md
- A cartridge crosses a boundary only by a declared need or an event and includes no sibling's crate, script, fixture or file; `just isolation` must report nothing before a change is done. Links: [[a-cartridge-brings-its-own-surface]], [[check-cartridge-isolation]]. Body: system/isolation.md
- Twenty-four standing principles, one leaf each; before a non-trivial change read the leaf whose situation matches and cite only what you read. Links: [[@prd/routine/root--show-me-your-work.md]], [[architect]], [[arena]], [[attack-the-premise]], [[blast-radius]], [[boundary-discipline]], [[build-the-lever]], [[encode-lessons-in-structure]], [[exhaust-the-design-space]], [[experience-first]], [[explain-how]], [[explain-why]], [[fix-root-causes]], [[foundational-thinking]], [[guard-the-context-window]], [[interrogate]], [[laziness-protocol]], [[make-operations-idempotent]], [[migrate-callers-then-delete-legacy-apis]], [[minimize-reader-load]], [[model-the-domain]], [[never-block-on-the-human]], [[no-redundant-comments]], [[outcome-oriented-execution]], [[principle]], [[prove-it-works]], [[redesign-from-first-principles]], [[separate-before-serializing-shared-state]], [[sequence-verifiable-units]], [[subtract-before-you-add]], [[swarm]], [[test-behavior-not-implementation]], [[type-system-discipline]], [[unslop]]. Body: system/principles.md
- Record every user correction in the same turn as a note or routine memo quoting the context anchor, with the anchor's words in uses.when; recall by those words too. Body: system/corrections.md

`summary`
toolchain: cargo cargo-nextest bun tmux
Isolation passed for 20 cartridges.
isolation composition pass

```
