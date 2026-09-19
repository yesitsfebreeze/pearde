---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
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
Graph ownership, identity and retraction belong to ASP. None of them moves
into the generic host.

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

## Not in this PRD

- The proxy step that enriches the request (`MANIFEST.md`'s "enriched request").
- JEV and model decisions made over the world.
- Moving existing `context.*` providers onto `asp.*`. The first slice runs
  alongside them, and a later PRD migrates the providers and deletes the old
  path in the same change.
- Renaming to kasuri (`@root/kasuri-names-the-system-and-each-kasuri-directory-ends-in-ki`).

## Acceptance

- [ ] `asp.ctg` exists as a cartridge with its own `cartridge.json`, `README.md`
      and `.cartridge/help.md`, and it injects its providers with `asp.*`.
- [ ] A named executed test loads two fixture providers owned by `asp.ctg`,
      `files` (asserts `file:` nodes) and `search` (asserts `matches` edges and
      `range:` nodes). It expands a file, sees both contributions, reconciles
      the composition without `search`, expands again, and asserts that the
      `matches` edges and `range:` nodes are gone and the `file:` nodes remain.
- [ ] A named executed test has two providers assert the same `file:` node.
      Unloading one leaves the node present with only the other contributor
      listed.
- [ ] A named executed test changes a file's canonical revision after a
      provider answered. The next expand returns that provider's facts marked
      `stale`.
- [ ] A named executed test lists an action for an entity. Invoking it runs
      through the tool dispatch, and a policy denial reaches the caller
      unchanged.
- [ ] `just audit` and `just isolation` report nothing for `asp`.
