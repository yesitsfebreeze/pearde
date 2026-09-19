---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: rollup
capability-owner: runtime
needs:
- "@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on"
- "@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp"
- "@agent/the-run-is-a-stream-of-typed-events"
- "@runtime/a-listener-subscribes-to-event-types"
---

# ASP is the agent's one interface: entities, events, the ring and fabric under one extensible protocol

## Outcome

An agent reaches everything it needs to know about the project through one
interface, ASP (Agent Server Protocol), served by the host in
`cartridge.ctg/src/asp`. It asks about an entity (a file, a symbol, a memo, an
event, an agent, a range) and gets one merged answer. That answer holds what
every installed cartridge contributes about the entity, what happened to it
recently according to the event ring, and how the fabric ranks it for the
current task. Installing a cartridge adds its types and its links into ASP.
Removing the cartridge removes both. Nothing an agent looks up lives beside
ASP: the code outline and usages, file and context search, memos, the event
stream, the durable ring and the fabric all sit below it.

This PRD coordinates the work and is not itself implementation work. Its
children and needs deliver it. `/Users/feb/dev/cartridge/ASP.md` is the
hand-off guide for the agent that works it.

## ASP is the fabric with a better protocol (2026-09-19, user)

The user's words: "the asp is basically the fabric, but with a better protocol.
we need to make that known, and implement it clean and correctly into the
catridge.ctg". Read every mention of the fabric below in that light. ASP is
the fabric's graph and ranking with typed ids, declared types, per-fact
ownership and revision, staleness and actions. The comparison table is in
`@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on`,
and the protocol is `cartridge.ctg/docs/asp.txt`.

## Decisions (2026-09-19, user)

These are the user's decisions from the 2026-09-19 session, quoted where the
wording matters:

1. **ASP is the root for everything.** "The ASP is the number one interface
   and we can register different types and just add to it, similar to how the
   memo system works and how the event system works." And: "the fabric should
   also be in the ASP. the ASP is the root for everything."
2. **ASP lives in the host.** "all in cartridge.ctg, move the asp into it, its
   an important base tool." ASP is not a separate `asp.ctg` cartridge. It is
   host code in `cartridge.ctg/src/asp`, beside the transport and event
   system. Providers stay isolated cartridges that only declare into ASP.
3. **Types are registered, not built in.** A cartridge declares the ASP
   schemes, edge kinds, attributes and actions it contributes in its
   `cartridge.json`, the same way it declares events today and the same way
   memo requires a kind to be declared before its instances. ASP refuses a
   contribution to anything undeclared, and the refusal names the contributor.
4. **The ring is bounded and rolls over.** The live ring holds 1024 entries
   and folds into day, week, month and year tiers, compacted, durable and
   readable in every older format.
5. **The fabric moves into ASP.** The ranking engine that memo serves today as
   `memo {op:"fabric"}` (`memo.ctg/src/fabric_graph.rs`) becomes ASP's ranker
   over the whole ASP world. memo keeps authoring memos and contributes
   `memo:` entities to ASP like any other provider.
6. **external code index goes.** The external code-graph tool is removed once ASP answers
   outline, definition, usages, callers and callees from the live language
   server.

## Decisions (2026-09-19, coordinator)

These were settled from the evidence, and the reasons are given:

- **Naming.** "Landscape" was renamed **fabric** (`memo fabric`; the
  `landscape.ctg` crate was dissolved in host commit `939e7d1`). In this
  codebase "trace" is the per-request correlation id in
  `cartridge.ctg/src/trace/` and has nothing to do with context. No ASP part
  is called "trace". "Landscape" survives only as a board name.
- **Scheme owners.** fs owns `file:` and `range:`. lsp owns `symbol:`. memo
  owns `memo:`. sessions owns `agent:`. The host owns `event:` and `ring:`,
  because the host's transport assigns sequence numbers and the ring lives
  beside it. This resolves the split between the ASP core PRD, which names
  sessions as the owner of `event:`, and the ring PRD, which names the ring.
  There is no `commit:` provider until a git cartridge exists, because
  `gitfs.ctg` is not in this composition.
- **One contributor contract.** ASP's node, edge and fact shapes extend the
  evidence contract (`Reference {owner, kind, id, revision, revision_kind}`,
  `Availability`, `Contribution`) in `memo.ctg/evidence/src/lib.rs`. The host
  mirrors that shape on the wire and does not depend on memo's crate.
  `context.*` and `asp.*` coexist only until the migration child lands. That
  child deletes the `context.*` path in the same change, in line with the
  no-legacy rule.
- **One search.** ASP's `search` fans out to every provider that declares
  search, and the fabric ranks the merged result. This supersedes
  `@landscape/one-search-covers-the-record-and-memory` and absorbs
  `@landscape/a-search-ranks-current-guidance-over-delivered-history` as a
  ranking rule.
- **The query surface.** ASP is a host service key `asp` (reached through
  `cartridge call asp`) and a `tool.asp` tool for agents. Both go over the
  existing transport and add no new wire.

## Order of work

Each step leaves a working, tested system:

1. **Fix the substrate.** `@runtime/a-listener-subscribes-to-event-types`
   covers the gap envelope and the epoch that survives a restart. The lsp
   fixes are the first slice of the lsp child: `references` sends the
   required `context`, and there is one client per workspace root.
2. **Build the ASP core.** The root ASP PRD covers the registry in
   `cartridge.json`, `expand`, `search`, `types`, merge, stale marking,
   retraction and actions.
3. **Add the first providers.** fs (files, ranges, search), then lsp (symbols,
   usages, calls), then memo (memos and their kinds as types).
4. **Put events under ASP.** Declared events become ASP types and envelopes
   become `event:` entities. The durable ring with its tiers follows, then
   sessions (`agent:` and activity). The typed-event chain
   `@agent/the-run-is-a-stream-of-typed-events` lands alongside, and its
   failed leaf `@agent/an-event-declares-its-type` has to pass review first.
5. **Move the fabric into ASP.** The ranker moves from memo into the host and
   ranks ASP entities.
6. **Cut over.** `context.*` providers migrate to `asp.*` and the `context`
   path is deleted. Superseded landscape PRDs are retired with a pointer
   here. external code index is removed, and the agent prompt names ASP as the first place
   to look.

## Children

- [lsp contributes symbols, usages and calls to ASP](lsp-contributes-symbols-usages-and-calls-to-asp/prd.md)
- [fs contributes files, ranges and search to ASP](fs-contributes-files-ranges-and-search-to-asp/prd.md)
- [memos are ASP entities and memo kinds are ASP types](memos-are-asp-entities-and-memo-kinds-are-asp-types/prd.md)
- [every declared event is an ASP type and every published envelope an event entity](every-declared-event-is-an-asp-type-and-every-published-envelope-an-event-entity/prd.md)
- [sessions contributes agents and their activity to ASP](sessions-contributes-agents-and-their-activity-to-asp/prd.md)
- [fabric ranks the ASP world from the host](fabric-ranks-the-asp-world-from-the-host/prd.md)
- [context providers become ASP providers and the context path is deleted](context-providers-become-asp-providers-and-the-context-path-is-deleted/prd.md)
- [agents find code through ASP and external code index is removed](agents-find-code-through-asp/prd.md)

## Acceptance

- [ ] Each need and child passes its own review and acceptance.
- [ ] Integration: in one disposable profile with fs, lsp, memo and sessions
      loaded, one agent edits a Rust function through fs. A second agent asks
      ASP about that function's file and receives, in one answer: the
      function as a `symbol:` with its callers, the ring's `touched` edge
      naming the first agent and the revision, the memos that mention the
      file, and a fabric rank. Unloading lsp removes the `symbol:` facts and
      nothing else.
- [ ] `memo {op:"fabric"}`, the `context.*` injection and external code index no longer
      exist, and nothing refers to them.
- [ ] `cartridge help host` documents ASP, and the host README and help page
      describe it.
- [ ] `just audit`, `just isolation`, `just test runtime` and
      `just check runtime` pass.
