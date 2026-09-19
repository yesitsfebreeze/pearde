---
state: "done"
origin: requested
priority: 76
repo: "/Users/feb/dev/cartridge"
capability-owner: web
needs:
- "the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text"
- "the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url"
footprint:
- "web.ctg/.cartridge/.gitignore"
- "web.ctg/.cartridge/memos"
- ".cartridge/tests/integration/web-tool-policy.test.ts"
commit: "12a1646bd6d37af7ff934e3e652065a749acbff8"
---

# The agent calls it, cites its sources, and policy can refuse it

## Outcome

The composition uses the capability: the tool is in the agent's list, a system
memo tells the model when to reach for it and to name the URL it used, and a
policy rule refuses it with the refusal reported to the caller.

## What the analyst established (2026-09-17, against fd68eae)

- **The agent picks the tool up for free.** `agent.ctg/cartridge.json` declares
  `needs: [..., "tool.*"]`, and the host resolves `tool.*` to every event with
  that prefix that another enabled cartridge listens to
  (`cartridge.ctg/docs/creating-cartridges.txt`, MANIFEST FIELDS). A cartridge
  listening to `tool.web` is in the agent's tool list with **no edit to
  `agent.ctg`, `mcp.ctg` or `harness.ctg`**.
- **Policy refusal already works generically, and per operation.**
  `agent.ctg/src/lib.rs:637` calls `policy` before every dispatch and a `deny`
  returns `{"content": "permission denied", "error": true}` at `:657` — a tool
  result the model sees, never a silent drop. `mcp.ctg/src/service.rs:540` does
  the same and answers with `self.refusal(...)`, and an `ask` with no approval
  channel is reported as a denial naming the operation (`:553`).
  `policy.ctg/init.lua:79` reads `request.input.op` and applies
  `operations[tool][op]` before the tool-level rule, so
  `policy.operations.web = { fetch = "deny" }` refuses only the fetch. So this
  box needs **no new code** — it needs a composition-level rule and a test that
  proves the refusal arrives.
- **The trap at `policy.ctg/init.lua:81`:** once `operations[tool]` exists, a
  call whose `input.op` is not a non-empty string is denied outright as
  `invalid_operation`. This is the reason `web` is one tool with
  `op ∈ {search, fetch}` rather than two tools — two tools would throw the
  per-operation lever away.
- The rules live on the composition, in `.cartridge/config.lua:52`
  (`policy.default = "allow"`, `policy.tools = {...}`); `policy.ctg` knows no
  tool.
- A test that drives two cartridges belongs to the composition under
  `.cartridge/tests/`, not inside one cartridge
  (`.cartridge/memos/system/isolation.md`).

**Landing warning:** `.cartridge/config.lua` was already modified in the working
tree when this was planned. A foreign staged path in `repo` aborts a collect
repo-wide, so check `git status` before collecting anything that touches it.

## Acceptance

- [x] `web.ctg/.cartridge/memos/system/<name>.md` (written through the memo tool, with `docs.ctg/.cartridge/memos/system/docs-entry.md` as the model) tells the model to use the web tool when the answer is not on this disk and to name the source URL; `just prompt` includes that line.
- [x] The tool appears to the agent with no edit to `agent.ctg`, `mcp.ctg` or `harness.ctg` — the `tool.*` glob resolves it.
- [x] With `policy.operations.web = { fetch = "deny" }`, a fetch comes back as a reported refusal, never a silent drop; the policy decision itself carries the reason. With the rule removed it is dispatched. Proven by a test under `.cartridge/tests/integration/` that composes the real `policy.ctg` and real `web.ctg` in its own scratch project config, not by editing the live `.cartridge/config.lua`.

  **Reworded again 2026-09-19 (round 2, reviewer finding N2):** "carrying the
  reason" overstated the agent path — `agent.ctg` returns
  `{"content":"permission denied","error":true}` with no reason attached;
  only the policy decision itself carries one (`"Policy denies web.fetch"`).

  **Reworded 2026-09-19, analyst pass at 4104d36:** the original box named
  `.cartridge/config.lua` as the rule's location. `.cartridge/config.lua` (and
  `.cartridge/justfile`) carry uncommitted edits belonging to someone else on
  this HEAD (`git diff -- .cartridge/config.lua`: an unrelated `router`/`skip`
  change); `prd collect` commits every dirty path inside a spec's footprint, so
  a footprint naming that file would sweep the foreign edit into this change.
  A fixture project's own `config.lua`, composing the real `policy.ctg` and
  real `web.ctg` by symlink, proves the same mechanism more directly (it
  drives `policy` with the exact request shape `agent.ctg`/`mcp.ctg` send, and
  reads `web.ctg`'s real dispatch on either side of the rule) without touching
  the live composition at all. See `specs/spec01.md` for the measured proof.
- [x] An answer built from a search can name its sources: every search result and every fetched page carries its `url`, and the system memo tells the model to name it. Whether a given model turn does so is a recorded ceiling, not a mechanism (see spec01 "Ceiling: box 4").

## Footprint narrowed (2026-09-19, coordinator, review round 2 finding B4)

`.cartridge/config.lua` was removed from this PRD's footprint, and the footprint
now names exactly what the spec changes. Collect takes the union of the PRD's
and the spec's footprints, and `config.lua` carries another session's
uncommitted edits. With a lane, the second verification pass would have aborted
after the fast-forward and left no receipt. Without a lane, collect would have
committed the foreign edit. The test directory was narrowed to the one new test
file for the same reason.

## Box 4 reworded (2026-09-19, coordinator)

Box 4 said "an answer built from a search names its sources". That is a
property of a model turn, and every review round accepted it as a ceiling under
`review-plan.md` step 4 (round 1, finding N5). The engine cannot collect a PRD
with an unticked box, and ticking a claim nobody can observe would be false. So
the box now states the mechanism that can be observed: every result and every
fetched page carries its `url`, and the memo tells the model to name it. The
citation itself stays a recorded ceiling and belongs to product QA on the voice
path.
