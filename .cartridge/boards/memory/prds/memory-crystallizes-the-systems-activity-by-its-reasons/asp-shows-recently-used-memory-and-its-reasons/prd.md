---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/memory.ctg"
---

# ASP shows recently used memory and its reasons

## Outcome

Users explore memory, recent usage, submemories and reasons in the existing ASP graph interface. Repeated activity is a normal memory entity, with its recurrence and heat visible there.

## Design

Expose memory:root and memory:recent as virtual navigation nodes and memory-group:<id> as a submemory projection. Existing memory:<entity> identifiers remain stable. A memory entity exposes bounded outgoing reason nodes using memory-reason:<id>. Declare every scheme, attribute and edge in the cartridge manifest. Keep trace:root as an ingress-era navigation alias while callers migrate.

The engine supplies a read-only projection with deterministic ordering and a maximum of 256 nodes per response. Recent usage means the entity's recorded retrieval time, not its last occurrence timestamp. Browsing does not deposit heat or increment access counters. Include recurrence count and occurrence timestamps separately from usage. Omit inactive, private and expired entities according to the same visibility rules as retrieval. Do not reload the entire graph to render a node. Report residency limits if a root projection only includes resident entities.

Search queries the memory graph once; remove the separate calendar search. Entity expansion preserves existing provenance and revision behavior while adding reason and usage attributes. Host ASP and Scope remain generic consumers of declared graph objects.

## Acceptance

- [ ] Memory roots, groups, entities and reasons navigate within ASP without a separate memory screen.
- [ ] Recent entities are sorted by actual retrieval time with stable identifier tie breaks.
- [ ] Repeated rendering does not change heat, access counts or recurrence.
- [ ] Failed and successful experiences remain distinct nodes.
- [ ] Projection limits, visibility, Unicode and empty memory are covered by tests.
- [ ] Search performs one memory query and yields graph-native activity results.
- [ ] The manifest, README and help match the implemented projection and its residency limits.

## Projection and recovery contract

A page contains its parent, at most limit minus two children, and a declared memory-page continuation node when more children remain. Continuations encode the subject and offset and are stable for an unchanged graph; changes between pages can reorder results, so refresh restarts from the root. Clamp the page limit to 3 through 256. Return an empty projection for malformed continuation identifiers. Enumerate resident recent entities and label that scope explicitly. Named group expansion can read that one memory from storage without modifying graph usage clocks.

Content provenance revisions continue to hash only the existing evidence projection; volatile usage, recurrence and heat attributes do not change that revision. Direct reason expansion checks the source and any nonempty target with the same active, retention and knowledge-space visibility rule; unknown or hidden endpoints suppress the reason. The engine has no persisted private flag today; the cartridge adapter retains its existing private-row refusal.

ASP search sets an explicit read_only query option. It suppresses both cache-hit and fresh-query CommitAccess tasks and the advisory save callback. Ordinary memory retrieval retains its current usage behavior.

## Proof

Run `cargo test -p graph experience`, `cargo test -p rpc experience` and the cartridge ASP integration tests in the standalone checkout. Add a fixture spanning several pages, retrieve every visible node through continuation edges, and compare entity access_count, accessed_at, heat and recurrence before and after search and expansion. Test direct reason access with a hidden endpoint, expired entities, empty graphs and malformed cursors. Failed projection requests retain the graph unchanged and can be retried. Integration validation includes the declared manifest surface and repository isolation checks.

## Dependencies

The recurrence attributes depend on repeated-activity-becomes-weighted-graph-knowledge. Durable activity navigation depends on activity-recording-drains-into-memory-and-retires-calendar-history. Reason groups depend on sub-memories-split-by-their-attached-reasons. Read-only ASP navigation for existing memories can be verified independently; final acceptance requires all three integrated.

## Implementation checkpoint

Implemented in the current memory.ctg working tree. [Shared verification evidence](../implementation.md) records integration, tests and remaining limits. This checkpoint does not replace formal PRD collection.
