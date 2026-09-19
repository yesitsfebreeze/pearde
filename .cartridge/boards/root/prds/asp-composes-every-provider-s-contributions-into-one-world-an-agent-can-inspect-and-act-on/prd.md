---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/loader/document.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/architecture.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/creating-cartridges.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/llms.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/host/plan.rs
commit: "7af748a7a59d0daf65d1aa9545aeaa076272a74a"
---

# asp composes every provider's contributions into one world an agent can inspect and act on

## Outcome

An agent asks one service, `asp`, about an entity such as a file, a symbol, a
test or a commit. It gets back one merged view: the nodes, edges, attributes
and actions that every loaded provider contributes for that entity, with each
fact labelled by the provider that asserted it. Loading a provider adds its
contributions. Unloading it removes them, and leaves in place every entity
that another provider still supports. No provider knows about any other
provider, and no agent needs its own integration with any provider.

The runtime composes capabilities. ASP composes what those capabilities mean.
Graph ownership, identity and retraction belong to ASP, and ASP is part of the
host: it lives in `cartridge.ctg/src/asp`, beside the event system, because
every agent depends on it (see the decision below).

## Context

The user asked to add and conceptualize ASP (Agent Server Protocol), the
layer named in the untracked `MANIFEST.md` at the repository root:

    Kasuri    = runtime
    Events    = communication
    ASP Graph = live semantic world
    ASP       = interface to that world

Most of the pieces already exist in this repository, and ASP reuses them
rather than building beside them:

- Contributors injected by glob. memo already takes every `context.<kind>`
  provider through `inject = { "context.*" }`. Removing a provider from the
  profile removes its contribution and changes nothing in memo (see
  `@root/invert-memo-context-sources`). ASP uses the same pattern with
  `asp.<kind>`.
- Owned, revisioned references. `Reference { owner, kind, id, revision,
  revision_kind }` in `memo.ctg/evidence/src/lib.rs`, together with the
  `read` operation that answers `available`, `changed` or `unavailable`,
  already covers per-fact ownership and staleness for flat evidence rows.
- A node and edge engine. The tool graph (`@root/tool-graph-engine-is-the-ranking-database`)
  already stores keyed nodes and deduplicated edges.
- Shared activity. fs reports every mutation to sessions as change evidence,
  and in gitfs mode each agent's work is a branch other agents can inspect.

What is missing is a shared identity for one entity across providers, edges
between entities, actions attached to entities, and one service that merges
all of it.

Closest prior art: ActiveGraph (shared typed graph, events carrying actor
identity and causal links, packages bundling types, tools and behaviours) and
OpenCog AtomSpace. ActiveGraph derives its graph from an authoritative event
log. ASP instead asks the live providers each time, and the event ring only
points into it.

## Concept

### Identity

An entity is a string ID made of a scheme and a canonical key. The provider
that owns a scheme also owns its canonical form, and every other provider
uses that form without re-deriving it.

| Scheme   | Key                                         | Canonical owner |
|----------|---------------------------------------------|-----------------|
| `file`   | workspace-relative path, normalized          | fs              |
| `symbol` | `<file key>#<qualified name>`                | lsp             |
| `range`  | `<file key>:<line>:<col>-<line>:<col>`       | fs              |
| `commit` | full sha                                     | gitfs           |
| `test`   | runner-qualified test name                   | the test runner |
| `agent`  | session id                                   | sessions        |
| `event`  | ring sequence number                         | sessions        |

An entity exists in the world while at least one loaded provider asserts it.
No provider can delete an entity. It can only stop asserting it.

### Ownership

Every fact names the contributor that asserted it and the revision it was
computed against:

- **Node**: `{ id, contributor, revision }`. Several contributors can assert
  the same node, and ASP takes the union.
- **Edge**: `{ from, to, kind, contributor, revision }`, for example
  `file:src/a.rs --contains--> symbol:src/a.rs#main` from lsp, or
  `file:src/a.rs --matches--> range:src/a.rs:4:1-4:9` from a search provider.
- **Attribute**: namespaced by the contributor, such as `lsp.diagnostics` or
  `search.count`. A contributor never writes into another contributor's
  namespace, so merged attributes never collide.

### Lifecycle

ASP pulls. It does not keep a pushed store:

1. `{ op: "expand", entity, depth, limits }` fans out to every injected
   `asp.*` provider that declares the entity's scheme, then merges the
   answers.
2. Each answer carries its revision, for example the content hash from fs
   or a git sha. If a fact's revision disagrees with the canonical owner's
   current revision, the fact is returned marked `stale` and is never
   silently dropped.
3. A provider that times out or crashes appears in the reply's `sources`
   list with state `unavailable`, and its facts are absent. This is the same
   `Availability` the evidence contract already uses.
4. Retraction needs no bookkeeping. A provider removed from the profile is no
   longer injected, so ASP no longer asks it, so its contributions are gone.
   Any cache ASP keeps is keyed by contributor and is dropped when the host
   reconciles the injection set.

### Actions

A provider declares actions per scheme:
`{ name, applies_to: "file", effect: "read" | "mutate", tool: "<tool key>", args }`.
An action is a pointer to a tool key the host already serves, with the
entity bound into its arguments. ASP only lists actions. Running one goes
through the normal tool dispatch, so policy.ctg remains the only authority on
permissions, and ASP adds no permission model of its own.

### The ring points into the world

A ring event names `agent → action → target entity → revision`. Another
agent follows the target ID into ASP and inspects the current state instead
of reading a text report:

    agent A -> ring: edited symbol:src/a.rs#main @ rev 3f2c
    agent B -> asp : expand symbol:src/a.rs#main  (diff, diagnostics, test action)
    agent B -> ring: ran test:a::main_works, failed
    agent C -> asp : expand test:a::main_works    (failure, rerun action)

The event shape is designed here. Emitting it from sessions is a separate
PRD.

## Direction (2026-09-19, user)

The user made ASP, together with the event system
(`@agent/the-run-is-a-stream-of-typed-events` and its children), priority one.
Both were raised to priority 100, and the event chain was reopened from
`deferred`.

The first real use is to replace external code index, the external code-graph tool this
workspace currently loads over MCP. An agent should get a file's outline, a
symbol's definition and usages, and its callers and callees as ASP entities.
One search should cover workspace files and the composed context (memos, help,
docs) together, natively rather than through a separate index. That makes the
first real providers:

- lsp: `symbol:` nodes with their spans and signatures, `contains` edges from
  `file:`, `references` and `calls` edges from `textDocument/references` and
  `callHierarchy/*`, and lookup by name through `workspace/symbol`. These come
  from the live language server, so they are never a stale prebuilt index.
- a search provider over files and context: `matches` edges and `range:`
  nodes, with memo and doc records addressed by their own scheme, so a single
  query returns code and context hits side by side.

Evidence gathered while evaluating external code index on 2026-09-19:

- `tool.lsp` `symbols` already answers from rust-analyzer. `references` fails
  on every call with `Failed to deserialize textDocument/references: missing
  field 'context'`: `lsp.ctg/src/service.rs` sends the request without the
  `context: { includeDeclaration }` field the LSP specification requires.
- `lsp.ctg` has no `workspace/symbol` or `callHierarchy` operations yet, and
  its outline is raw LSP JSON with numeric kinds and full URIs. external code index's value
  was a compact outline and name-based lookup, and ASP expansion should give
  agents both.
- external code index links edges by name and drops a caller whenever a name is ambiguous,
  for example "2 definitions share the name PASSTHROUGH". Compiler-resolved
  edges from the language server do not have that gap.

external code index is removed once these providers pass their probes: its MCP server,
hooks, skill and retired code index.

## Decision (2026-09-19, user)

ASP moves into the host, `cartridge.ctg`, and is not a separate `asp.ctg`
cartridge. The user's words: "all in cartridge.ctg, move the asp into it, its
an important base tool." The started `cartridge.ctg/src/asp/protocol.rs` is
where the work begins. Providers stay isolated cartridges that declare `asp.*`.
The host merges their contributions, and no provider depends on another.

## Decision: ASP is the agent's first interface (2026-09-19, user)

The user's words: "The ASP is the number one interface and we can register
different types and just add to it, similar to how the memo system works and
how the event system works." And: "the ASP itself is extendable the same way
the base cartridge is based on whatever cartridge we have installed. It
provides a link into the ASP if it has any data."

This means:

- **Everything lives below ASP.** The code outline and symbols (lsp), files
  and search (fs), memos (`memo:`), the event stream (`event:`), the context
  ring (`ring:`), sessions (`agent:`) and commits (`commit:`) are all reached
  through ASP. None of them is a separate place an agent has to know about.
- **Types are registered, not built in.** A cartridge declares the ASP schemes
  it owns, the edge kinds and attributes it contributes and the actions it
  offers. It declares them in `cartridge.json`, the same way it declares
  events today and the same way memo declares kinds before their instances.
  The identity table above is therefore the starting registry, not a closed
  list. Installing a cartridge adds its types and links. Removing it removes
  both.
- **ASP validates contributions against the registry.** A contribution to an
  undeclared scheme or edge kind is refused, and the refusal names the
  contributor.

Acceptance that follows from this decision:

- [x] A named executed test installs a fixture cartridge that declares a new
      scheme in its `cartridge.json`. ASP lists the scheme, and an `expand`
      returns the cartridge's nodes. Removing the cartridge removes both the
      scheme and the nodes.
- [x] A named executed test has a provider contribute an edge kind it did not
      declare, and ASP refuses it with an error that names that provider.

The durable ring is its own PRD:
`@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp`.

Emitting ring events that name `agent → action → target entity → revision`
still needs its own PRD, which will join ASP with the event chain above.

## Decision: ASP is the fabric with a better protocol (2026-09-19, user)

The user's words: "the asp is basically the fabric, but with a better protocol.
we need to make that known, and implement it clean and correctly into the
catridge.ctg".

ASP is therefore not a layer above the fabric, and the fabric is not a part
beside it. The fabric was one graph of everything the composition can reach,
assembled from each cartridge's `graph.announce` answer and ranked by match
times observed use. ASP is that same graph with the protocol it lacked:

| The fabric had | ASP has |
|---|---|
| `kind` and an untyped `key` per node | `scheme:key` ids, with one owning cartridge per scheme |
| whatever a contributor announced | types declared in `cartridge.json`, and a refusal that names the contributor |
| `from` stamped on a node | a contributor and a revision on every node and edge, and `stale` against the owner's revision |
| one ranked search | the same ranking formula, over nodes merged from every search provider |
| nothing to do with a node | actions that run through the tool dispatch |
| a graph rebuilt from every announce | a pull per entity, so nothing is stored and nothing is retracted |

The ranking formula moved into `cartridge.ctg/src/asp/rank.rs` with this PRD.
What remains for `fabric-ranks-the-asp-world-from-the-host` is to move the
`graph.announce` contributors onto `asp.*`, feed use counts from the ring, and
delete `memo {op:"fabric"}`.

## Decision (2026-09-19, coordinator)

- A cartridge declares its types in an `asp` block of `cartridge.json`:
  `schemes` (with `owner`), `edges`, `attributes`, `actions` and `search`. It
  answers on exactly one `asp.<name>` event it listens to, which is how the
  host finds its door without a second declaration.
- A provider is asked about an entity when it declares the entity's scheme.
  It may assert nodes only of schemes it declares and edges only of kinds it
  declares. One undeclared fact refuses its whole answer, and `sources`
  carries the refusal with the provider's name.
- The canonical revision of an expanded entity is the revision on the node
  its scheme owner asserts. A fact from any other contributor with a different
  revision comes back `stale`.
- `asp` is served on the host socket as its own method, granted to cartridges
  beside `status`, `snapshot` and `cartridges`, and on the `bail` key `asp`,
  so `cartridge call asp` and `cartridge.host("asp", ...)` both work on the
  existing wire. The key `asp` is refused as an event name.
- The agent tool `tool.asp` is not in this PRD. It needs the host to own and
  listen to an event, which the transport cannot do yet, and that is its own
  change.

## Not in this PRD

- The proxy step that enriches the request (`MANIFEST.md`'s "enriched request").
- JEV and model decisions made over the world.
- Moving existing `context.*` providers onto `asp.*`. The first slice runs
  alongside them, and a later PRD migrates the providers and deletes the old
  path in the same change.
- Renaming to kasuri (`@root/kasuri-names-the-system-and-each-kasuri-directory-ends-in-ki`).

## Acceptance

- [x] ASP lives in `cartridge.ctg/src/asp`. The host serves it as a built-in
      `asp` service that asks every loaded provider declaring `asp.*`, and
      `cartridge help host` documents it.
- [x] A named executed test loads two fixture providers from the host's test tree,
      `files` (asserts `file:` nodes) and `search` (asserts `matches` edges and
      `range:` nodes). It expands a file, sees both contributions, reconciles
      the composition without `search`, expands again, and asserts that the
      `matches` edges and `range:` nodes are gone and the `file:` nodes remain.
- [x] A named executed test has two providers assert the same `file:` node.
      Unloading one leaves the node present with only the other contributor
      listed.
- [x] A named executed test changes a file's canonical revision after a
      provider answered. The next expand returns that provider's facts marked
      `stale`.
- [x] A named executed test lists an action for an entity. Invoking it runs
      through the tool dispatch, and a policy denial reaches the caller
      unchanged.
- [x] `just audit` and `just isolation` report nothing for `asp`. ASP is part
      of the host, so this is `just check runtime`, which runs isolation.
