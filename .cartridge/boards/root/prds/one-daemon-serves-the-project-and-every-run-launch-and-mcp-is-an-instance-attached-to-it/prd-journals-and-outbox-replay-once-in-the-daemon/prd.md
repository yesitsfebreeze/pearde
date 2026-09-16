---
state: "claimed"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/prd.ctg"
capability-owner: prd
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/service.ts"
- ".cartridge/tests/service.test.ts"
claim: "coordinator-cartridge-1b-1 2026-09-16T12:04:42.460Z"
---

# PRD journals and outbox replay once in the daemon

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies prd as must-exist-once:
under two compositions the job journal shows the other host's jobs as
`interrupted`, and the memory outbox is replayed twice (`service.ts:127`,
`:176`). The job journal also claims every job on start (this session's own
`prd add` events observed the peer item's claim).

## Outcome

The one prd node in the daemon owns the job journal and the memory outbox.
Attached instances' `prd` calls (scan/plan/add/claim/collect) all land on
that one node, so jobs are never marked interrupted by a second host and the
outbox replays once.

## What changes

- With the host-attach contract in force there is one prd node. This child
  **verifies** journal and outbox behaviour under attached instances and
  removes nothing: analysis (analyst-1, confirmed by reviewer-1) found no
  per-process assumption left to remove. The interrupt-marking is correct as it
  stands — it reports a journal left by a service that really ended — and the
  outbox's create-and-register happen in one synchronous tick, so the race this
  bullet originally anticipated does not exist. Removing either would be a
  regression, which is why the spec forbids an `src/` change.

## Acceptance

- [ ] A job started through one attached instance is not shown interrupted
      when another instance starts a job or calls prd.
- [ ] The memory outbox replays exactly once for a given pending
      acknowledgment, no matter how many instances make prd calls.
- [ ] prd.ctg's share of "exactly one prd node exists with the daemon
      running": the cartridge builds one `Wire` and one `Service` per process
      (`src/service.ts:232`, `:236`), refuses a second `apply` (`:235`), and
      starts no host, daemon or node of its own — its only children are its
      own engine CLI, `git` and `ps`. The daemon-wide count is delivered by
      the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` (this
      PRD's `needs`) and re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. **Neither audit finding
survives one daemon**, and the third was never true.

- The `interrupted` marking (`service.ts:127`) dissolves: `instance = id()` is
  per-`Service` (`:34`), a `Service` is built exactly once at `apply` (`:236`,
  a second apply refused at `:235`), jobs journal that id (`:198`), and `job()`
  is reached only from `status`/`stop`, only for a named job id, only in the
  same session, never written back. One node means every live job carries that
  node's id. The code is right as it stands and should stay: it reports a
  journal left by a service that really ended.
- The double outbox replay (`:176`) dissolves: `replayMemory()` has one call
  site, the entry id is `hash(text)` over evidence alone (`:169`) with no
  session, run or call in it, and `deliverMemory` single-flights by that file.
  The analyst specifically chased the create-then-deliver TOCTOU that this
  PRD's own "two instance-driven calls race inside the one node" points at:
  `:170`'s create and `:160`'s registration happen in one synchronous tick
  before the first `await` (`:154`), so the window does not exist. "Twice"
  required two `Service`s.
- "The journal claims every job on start" is **false** — nothing reads the job
  journal at start. What the audit saw is `publish` (`:130-135`) fanning
  `command.*` events node-wide, so one instance sees another's `claim`. The
  events carry `{session, run, call}` and no subscriber mutates a record.
  **Handed up, out of footprint**: narrowing delivery is cartridge.ctg event
  routing, the same hand-up the agent sibling made for `agent.event`.

So this is a proof-only slice, like `agent-runs`: no `src/` change, two
regression tests. Each regression the analyst patched in fails **only** its
matching new test while all 11 pre-existing tests pass, so the suite genuinely
did not cover either shape.

Two coordinator edits: the footprint gained `.cartridge/tests/service.test.ts`
(the only file the spec changes, and outside the declared `src/service.ts`, so
collect would have refused it — `src/service.ts` stays because the guards read
it), and box 3 was narrowed to prd.ctg's provable share using the analyst's
proposed wording verbatim.

Known-red, not caused here: `bun test ./.cartridge/tests/*.test.ts` is already
red at `e32c02b` in a bare worktree with 6 failures (4 `statusline`, `records`
owners/graph, `parity` migration), byte-identical with and without the patch.
Verify is scoped to `service.test.ts` for that reason.
