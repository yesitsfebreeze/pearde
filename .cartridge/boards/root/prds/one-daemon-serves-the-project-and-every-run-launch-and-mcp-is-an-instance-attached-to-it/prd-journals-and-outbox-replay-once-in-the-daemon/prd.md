---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/prd.ctg"
capability-owner: prd
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/service.ts"
- ".cartridge/tests/service.test.ts"
commit: "c3295cb71e54e3a177f5a909e8b7a1b17b1f3bfe"
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

- [x] A job started through one attached instance is not shown interrupted
      when another instance starts a job or calls prd.
- [x] The memory outbox replays exactly once for a given pending
      acknowledgment, no matter how many instances make prd calls.
- [x] prd.ctg's share of "exactly one prd node exists with the daemon
      running": the cartridge builds one `Wire` per process
      (`src/service.ts:232`), refuses a second `apply` (`:235`) and keeps
      serving from the one `Service` the first built (`:236`) — a job started
      before the refusal still reads as this node's afterwards, which a
      replacement `Service` with a fresh `instance` (`:34`) would not — and
      starts no
      host, daemon or node of its own — every child it starts is its own engine
      CLI (`src/service.ts:89`), `git` (`src/records.ts:25`, `:33`,
      `src/lifecycle.ts:73`, `:81`, `:131`, `:145`, `:165`), `ps`
      (`src/process.ts:59`), `sh -eu -c` running a spec's own Verify block
      (`src/lifecycle.ts:45`) and the configured adapter executable
      (`src/coordinator.ts:59-63`). None of those is a host. The daemon-wide
      count is delivered by
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
regression tests, plus a third added after verification showed box 3's
second-apply and one-`Service` clauses rested on a source `grep` and on prose
(`a second apply is refused, so one process serves from exactly one service`).
Each regression the analyst patched in fails **only** its
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

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, after three verification passes.

Boxes 1 and 2 were proven in pass 1 and are non-vacuous on two axes each.

Box 3 took three attempts, and the record is worth keeping because two of the
three fixes looked right and were not:

- Pass 1 found 3b, 3c and 3e executed **nowhere** — 3c rested on a `grep` for a
  string literal while no test ever called `apply` twice — and 3d's guard pinned
  spelling, not behaviour (a real `Bun.spawn(['cartridge','daemon','--replace'])`
  left it green while a bare comment failed it).
- Pass 2 confirmed 3c, 3d and 3e closed, but showed 3b still unproven: probe E
  (`if (service) { service = new Service(config ?? {}, wire); throw … }`) puts a
  **second** `Service` in the one process, keeps the refusal, and left the suite
  at 14/0. The implementer's argument covered a *closed* service, not a
  *replaced* one.
- Pass 3 verified the fix: a `--dry` job started before the second `apply`, read
  back after the refusal, asserted not `interrupted`. Probe E now fails at
  `service.test.ts:148` with `Expected: not "interrupted"`, **6 runs out of 6**,
  while `tsc` and blocks 2/3 stay green — so the test is the only thing that
  catches it.

Why 3b mattered rather than being a formality: a replacement `Service` gets a
fresh `instance` (`:34`), so every live job mismatches at `:127` and reads
`interrupted` — precisely what box 1's own test pins for a foreign entry — and a
fresh empty `deliveries` map kills the outbox single-flight that box 2 pins.
Both boxes this PRD exists to protect would have regressed while the suite
stayed green.

Pass 3 also ruled out the weaker reading: if the entry were merely *lost*,
`job()` throws, `.state` is `undefined`, and the assertion would pass — it
demonstrated that path separately. So the red means the entry was found and
judged foreign, which is exactly what box 3's wording claims.

Measured boundary, recorded not hidden: a replacement that deliberately copies
`service.instance` forward escapes the check. That requires a line whose only
effect is to defeat it; the canonical replacement is caught.
