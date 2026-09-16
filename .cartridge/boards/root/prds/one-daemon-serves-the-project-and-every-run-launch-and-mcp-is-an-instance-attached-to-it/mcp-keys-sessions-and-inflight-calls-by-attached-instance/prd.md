---
state: "specced"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
capability-owner: mcp
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "mcp.ctg"
- "mcp.ctg/src/service.rs"
- "mcp.ctg/src/lib.rs"
- "mcp.ctg/cartridge.json"
- "mcp.ctg/.cartridge/tests/unit/tests.rs"
- "mcp.ctg/.cartridge/tests/integration/instances.test.ts"
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
---

# MCP keys sessions and inflight calls by attached instance

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies mcp stdio clients and
in-flight calls as per-instance state keyed inside the shared cartridge: mcp
keeps one `session` and one `inflight` map per node today
(`mcp.ctg/src/service.rs:100-113`), so two attached stdio clients would share
one session and one call set.

## Outcome

The one mcp node keys its `session` and `inflight` maps by attached instance
(the connected stdio client), so two attached MCP clients keep separate
sessions and separate in-flight calls, while the node itself exists once.

## What changes

- `session`/`inflight` maps become keyed by instance id (the connection), not
  one entry per node.
- Session lifecycles: **not in this slice** (round 1, F3). The bridge sends no
  `closed` event today, so nothing can be dropped or cancelled on disconnect.
  What this slice delivers is isolation while attached: one instance's session
  and in-flight calls are neither visible to nor disturbed by another's. The
  cost is one small map entry per bridge that ever attaches — the same trade
  the done sibling `agent-runs-key-per-attached-instance-not-per-process` took.
  A `closed` event and real teardown are their own PRD.

## Acceptance

- [x] Two `cartridge mcp` stdio clients attached to one daemon keep separate
      sessions (each sees only its own initialization and history), and one
      closing does not affect the other's session or calls.
- [x] An in-flight call from one instance is not visible in or cancellable
      from the other.
- [x] Exactly one mcp node exists with the daemon running, proven at composed
      scope inside this PRD's own fixture: with two bridges attached to one
      daemon, `instances.test.ts` asserts that `status` lists exactly one `mcp`
      node in state `active`, and that the run directory holds exactly one pid
      directory containing exactly one `mcp.sock`. Structurally, mcp.ctg starts
      no host, node or child process of its own — a standing property, guarded
      against regression rather than introduced here. For the live project,
      the daemon-wide count is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`,
      which is still `open` — that re-proof has not landed yet.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. Unlike the sibling
`agent-runs-key-per-attached-instance-not-per-process`, **the audit premise
holds here**: `mcp.ctg/src/service.rs:100-113` keeps one `session` OnceCell,
one `inflight` map keyed by the client's own JSON-RPC id (every client counts
from 1, so two clients collide on `"1"`) and one `restored` set per node. The
analyst reproduced it live — two `cartridge mcp` children on one daemon both
echoed `session-1`.

`repo` moved from `mcp.ctg` to the superproject and the footprint was widened
across both submodules, because no instance identity exists anywhere today:
`cartridge mcp` sends `{"op":"message","line"}` only
(`cartridge.ctg/src/cli/host.rs:283-317`), the socket handler passes `data`
through verbatim, and stdio MCP carries no session header. The key's only
possible producer is the bridge, in `cartridge.ctg`. This is not a SPLIT — the
bridge's id has no consumer without the node, and the node's keying is
unobservable without the bridge — so it lands the established superproject way:
commit inside each submodule, bump the pointers, collect against the
superproject. Both submodules were clean when the footprint was widened; check
again before collecting, because the `cartridge.ctg` and `mcp.ctg` directory
entries make collect sweep everything inside them.

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, after reviewer-4 (round 4, PASS 95) and
verifier-1.

Boxes 1 and 2 were proven by execution in verifier-1: two real `cartridge mcp`
children with distinct, stable sessions, and two genuinely concurrent held calls
under the same JSON-RPC id 1 where a cancel reaches only its own context.

Box 3 is ticked on an assertion that **fails in the world it denies**, which it
took two corrections to reach. Round 3 found my earlier narrowing rested on a
false premise (the daemon-wide count *is* observable from this PRD's own
fixture). Round 3 then recommended `filter(n => n.id === 'mcp').length === 1` —
and the implementer found that this too cannot fail for the reason it claims:
with `{id="mcp",path="mcp"}` removed from the composition, `cartridge status`
still prints `{"id":"mcp",…,"state":"disabled"}`, because the entry comes from
the profile directory. Round 4 reproduced that independently. The shipped
assertion adds `&& node.state === 'active'`, which returns 0 in that world, plus
a `mcp.sock` route that fails there too.

The dead `run.length <= 1` check is **deleted**, not disclaimed: run directories
live at `base()/tag(descriptor)/<pid>` (`cartridge.ctg/src/host/socket.rs:46-84`),
never the project's `.cartridge`, so it looked where numeric entries cannot
appear.

Carried, non-blocking (F17): both boxes say "with two bridges attached" while the
assertion runs after `a.close()`. Step 6 and the code comment are accurate; the
box wording gets the one-line fix when the fixture is next touched.
