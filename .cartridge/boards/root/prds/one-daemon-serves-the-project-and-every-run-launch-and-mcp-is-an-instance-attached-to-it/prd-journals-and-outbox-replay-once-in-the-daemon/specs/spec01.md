---
complexity: small
footprint:
  - src/service.ts
  - .cartridge/tests/service.test.ts
---

# spec01 — pin that the job journal and the memory outbox are node state, so attached instances never double them

Base: prd.ctg `e32c02b` ("Collect …/memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock"). HEAD moved to `fe9d038f` during the pass; `git diff --name-only e32c02b fe9d038f -- src/ .cartridge/tests/` is empty and `attempt-1.patch` still applies clean at HEAD, so the base is only nominal.

## Option chosen

**No production change. Add the two regression tests the outcome is missing.**

Both audit findings are many-*node* symptoms of `service.ts` state that is
already per-node, and the one-daemon rule removes both. Traced end to end:

- **The interrupted marking is per-node, and correct.** `this.instance = id()`
  is one random id per `Service` (`src/service.ts:34`), and a `Service` is built
  exactly once, on `apply` (`:236`, refused twice by `:235`). A `run` job is
  journalled with that id (`:198`, `saveJob` `:117`). `job()` overlays
  `interrupted` only when `job.instance !== this.instance` (`:127`), and `job()`
  is reached only from `status`/`stop` (`:195`), only for a job id the caller
  names (`:63`), and only when `job.session === context.session` (`:125`). With
  one node every live job carries that node's id, so no call — from any number
  of attached instances, concurrent or not — can make it mismatch. The overlay
  is not even persisted: it is a read-time view of a journal left by a service
  that really did end (a daemon or node restart), which is exactly what it
  should report. Two hosts made it fire wrongly; one daemon does not.
- **The outbox replay is per-node, and single-flighted per entry.**
  `replayMemory()` (`:175`) has one call site, `apply` (`:236`), so it runs once
  per node. Its `attempts < 3` budget lives in the entry file, not in the
  process (`:152`, `:180`). The entry's identity is the hash of the verified
  evidence alone (`:169`) — no session, run or call — so two instances landing
  the same evidence address one file. Delivery is single-flighted by that file:
  `deliverMemory` returns the in-flight promise for the same path (`:149`) and
  registers it (`:160`) in the same synchronous tick in which
  `rememberVerified` creates the file (`:170`), before its first `await`
  (`:154`). There is no create-then-deliver window for a second instance-driven
  call to slip into. "Replayed twice" needed two `Service`s, i.e. two nodes.
- **"The journal claims every job on start" is not in this code.** Nothing
  reads the job journal at start: the only `readdirSync` in `service.ts` is the
  outbox (`:178`), and a journal file is read only when `status`/`stop` names
  its id and the in-memory map misses (`:124`). What that audit line actually
  observed is `publish` (`:130-135`) fanning every `command.*` event out on the
  node-wide `prd` channel, so an attached instance sees another instance's
  `claim`. The events carry `{session, run, call}` and subscribers filter, so no
  record is claimed twice — narrowing delivery to the owning instance is
  cartridge.ctg event routing, out of this footprint. Handed to the parent.

So the PRD's "removes any per-process assumption that would still misbehave if
two instance-driven calls race inside the one node" finds nothing to remove:
inside one node both keys are already the node and the entry, not the caller.
Adding an instance id above them would be a second name for `this.instance`.
Rejected.

What is missing is proof. The suite pins neither shape against a change that
re-keys it per caller: the existing outbox test
(`.cartridge/tests/service.test.ts:59`) races one `replayMemory` against one
`rememberVerified` in **one** context, and the existing job test (`:65`) only
asserts cross-session refusal and that a restarted service refuses `stop`.
Both regressions below pass that suite untouched. This spec closes that.

## Steps

1. `.cartridge/tests/service.test.ts`: append the two tests in
   `attempt-1.patch`, which apply and pass unmodified against `src/`:
   - `the job journal is keyed by node, so a second attached instance never
     interrupts a live job` — two attached instances of one session (same
     `session`, different `run`/`call`) each start a `--dry` run job and a
     second instance also calls `scan`; both jobs' in-memory and on-disk
     `instance` must equal `service.instance`, and a `status` from a third
     instance must not read `interrupted` for either. Then a hand-written
     journal entry carrying a foreign `instance` **must** still read
     `interrupted`, so the test pins the behaviour rather than its removal.
     Asserting the stored key, not a live `state`, keeps it free of the race
     against a `--dry` job finishing first.
   - `the memory outbox replays once per pending acknowledgment however many
     instances call in` — two instances in **different sessions** land the same
     verified evidence concurrently while `replayMemory()` runs alongside;
     exactly one outbox file, exactly one `ingest`, both receipts `committed`;
     then a further `replayMemory()` and a further `rememberVerified` leave the
     count at one.
2. Nothing else. No change under `src/`. `src/service.ts` stays in the
   footprint only so the guards in Verify may read it; if a step wants to edit
   it, stop and report — the behaviour is already correct and the diff is churn.

## Acceptance

- [ ] A job started through one attached instance is not shown interrupted
      when another instance starts a job or calls prd. (Both jobs keep
      `service.instance` in memory and in the journal; a third instance's
      `status` reads neither as `interrupted`; a genuinely foreign journal
      entry still does.)
- [ ] The memory outbox replays exactly once for a given pending
      acknowledgment, no matter how many instances make prd calls. (Two
      sessions' concurrent `rememberVerified` plus `replayMemory` produce one
      outbox file and one `ingest`; a later replay and a later instance add
      none.)
- [ ] prd.ctg's share of "exactly one prd node exists with the daemon
      running": the cartridge builds one `Wire` and one `Service` per process,
      refuses a second `apply`, and starts no host, daemon or node of its own —
      its only children are its own engine CLI, `git` and `ps`. Checked below.
      The daemon-wide count is not observable from this repo; it is delivered
      by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` (this
      PRD's `needs`) and re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.

## Verify and Proof

```sh
test -f .cartridge/tests/service.test.ts
bun test ./.cartridge/tests/service.test.ts
bun run check
```

```sh
test -f src/service.ts
test -f .cartridge/tests/service.test.ts
# The two regressions this PRD pins are present and named.
grep -q 'the job journal is keyed by node' .cartridge/tests/service.test.ts
grep -q 'the memory outbox replays once per pending acknowledgment' .cartridge/tests/service.test.ts
# A job is keyed by the node's one service instance, never by the invocation that started it.
grep -q 'instance: this.instance, invocation: key' src/service.ts
if grep -qn 'instance: context\.' src/service.ts; then echo 'job key became per-invocation'; exit 1; fi
# The outbox entry is identified by the verified evidence alone and single-flighted by that entry's file.
grep -q 'identifier = hash(text)' src/service.ts
grep -q 'if (this.deliveries.has(file)) return this.deliveries.get(file)!;' src/service.ts
if grep -qn 'hash(text +' src/service.ts; then echo 'outbox identity became per-instance'; exit 1; fi
# Replay happens once per node, at apply, and nowhere else: one definition, one call.
test "$(grep -c 'replayMemory()' src/service.ts)" = 2
```

```sh
test -f src/service.ts
# One wire and one service per node; a second apply is refused.
test "$(grep -c 'new Wire()' src/service.ts)" = 1
grep -q 'cartridge is already applied' src/service.ts
# prd.ctg starts no host, daemon or node of its own; its only children are the engine CLI, git and ps.
if grep -rn 'cartridge daemon\|host\.sock\|cartridge launch\|cartridge mcp' src/; then echo 'prd.ctg reaches for a host of its own'; exit 1; fi
```

## Remaining risk

- The full `bun test ./.cartridge/tests/*.test.ts` is **already red at
  `e32c02b`** in a bare worktree: 6 pre-existing failures, identical with and
  without this change. They have two distinct causes, not one: 4 are
  `statusline` code, while `records` (owners/graph, `records.test.ts:34-38`)
  and `parity` (migration manifest) both scan the **live committed board** and
  assert manifest ids still exist — board-record drift committed into prd.ctg,
  not `statusline` and not `src/`. Verify is scoped to `service.test.ts` for
  that reason; the red suite is not this PRD's and should not gate it.
- Verify block 1 needs `node_modules` resolvable from the lane, and the lane
  carries none: `src/lifecycle.ts:225` creates it with `git worktree add`. It
  resolves only because `lane()` (`:24`) places the worktree at
  `<repo>/.cartridge/boards/<board>/.lanes/<slug>` — **inside** `prd.ctg` — so
  Node/Bun walks up to `prd.ctg/node_modules` and `node_modules/.bin/tsc`. In a
  worktree outside the repo the block fails with `Cannot find package 'yaml'`.
  Relocating lanes would silently turn Verify red.
- `service.ts:130-135` publishes every `command.*` event node-wide, so an
  attached instance sees another instance's `claim`/`collect` events. They
  carry `{session, run, call}` and no record is mutated by a subscriber, but
  narrowing delivery is host event routing in cartridge.ctg. Handed up, out of
  footprint — the same hand-up the agent sibling made for `agent.event`.
- Job capacity (`:197`: 4 running, 128 total) and the invocation map cap
  (`:189`: 4096) are now shared by every attached instance rather than held per
  host. Four concurrent `prd run` jobs across all instances is the ceiling.
  Deliberate: raise it only if a real daemon is ever measured against it.
- `this.jobs` is never pruned, so one long-lived daemon keeps one entry per
  job ever started, up to the 128 cap. Intended — `stop` serves only jobs this
  service owns (`:126`).
