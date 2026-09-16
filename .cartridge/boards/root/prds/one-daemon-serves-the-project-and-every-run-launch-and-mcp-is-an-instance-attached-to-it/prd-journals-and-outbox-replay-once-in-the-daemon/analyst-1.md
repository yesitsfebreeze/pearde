# analyst-1 — prd-journals-and-outbox-replay-once-in-the-daemon

2026-09-16. Verdict: **SPECCED**. Base `e32c02b` (re-checked at start and end of
the pass; prd.ctg HEAD did not move). Probed in a detached worktree of prd.ctg
under the scratchpad, `node_modules` symlinked from the live checkout. The live
boards and the live daemon were never touched.

Drafts:

- `.state/loop/one-daemon-…/prd-journals-and-outbox-replay-once-in-the-daemon/spec01.md`
- `.state/loop/one-daemon-…/prd-journals-and-outbox-replay-once-in-the-daemon/attempt-1.patch`
  (34 added lines, `.cartridge/tests/service.test.ts` only; applies clean to a
  pristine `e32c02b` and passes unmodified)

## Code traced

All line numbers `prd.ctg@e32c02b`.

**Finding 1 — "the job journal shows the other host's jobs as `interrupted`"
(`service.ts:127`).**

- `src/service.ts:34` — `instance = id()`: one `randomUUID` per `Service`.
- `src/service.ts:236` — `apply` builds the one `Service`; `:235` refuses a
  second `apply` ("cartridge is already applied"). One node, one `Service`,
  one `instance`.
- `src/service.ts:198` — a `run` job is journalled with `instance:
  this.instance`; `:117` `saveJob` persists it under
  `.cartridge/.state/prd-service/<job_id>.json`.
- `src/service.ts:127` — the overlay: `if (job.instance !== this.instance &&
  job.state === 'running') job = { ...job, state: 'interrupted', … }`. It is a
  read-time view, never written back.
- Reachability: `:195` routes only `status`/`stop` into `job()`; `:63` demands
  one explicit 32-hex job id (no enumeration); `:125` refuses a job whose
  `session` is not the caller's; `:123-124` serves the in-memory map first and
  only falls to the journal file on a miss.

So the key is the **node**, not the process-per-call and not the caller. With
one daemon every live job carries that node's id and the mismatch cannot
happen — from one instance or from any number of them, racing or not. The
overlay keeps doing the job it was written for: reporting a journal left by a
service that really ended (daemon or node restart). **Does not survive
one-daemon as a defect; keep the code as is.**

**Finding 2 — "the memory outbox is replayed twice" (`service.ts:176`).**

- `src/service.ts:175-182` — `replayMemory()`; one call site, `:236` (`apply`).
  Once per node. Its `attempts >= 16` and `this.closed` bounds are per-pass;
  the durable budget `attempts < 3` lives in the entry file (`:152`, `:180`).
- `src/service.ts:169` — the entry identifier is `hash(text)` over the verified
  evidence alone. No session, run or call. Two instances landing identical
  evidence address one file.
- `src/service.ts:148-160` — `deliverMemory` single-flights by that file path:
  `:149` returns the in-flight promise, `:160` registers it. `:170`
  (`if (!fs.existsSync(file)) atomic(file, …)`) and `:172`'s
  `await this.deliverMemory(file)` run in **one synchronous tick** — the async
  IIFE at `:150` runs to its first `await` (`:154`) before `:160` returns — so
  there is no create-then-deliver window a second instance-driven call can slip
  into. I looked specifically for that TOCTOU because the PRD's "if two
  instance-driven calls race inside the one node" points at it; it is closed.

"Twice" required two `Service`s, i.e. two nodes. **Does not survive
one-daemon.**

**Finding 3 — "the job journal also claims every job on start".**
**Not in this code.** `service.ts`'s only `readdirSync` is the outbox (`:178`);
a journal file is read only when `status`/`stop` names its id (`:124`). Nothing
scans the journal at start. What that audit line observed is `publish`
(`:130-135`) fanning every `command.*` event out on the node-wide `prd`
channel, so an attached instance sees another instance's `claim` event. Events
carry `{session, run, call}`, subscribers filter, and no record is mutated by a
subscriber — narrowing delivery to the owning instance is cartridge.ctg event
routing, out of this footprint. **Handed up to the parent**, the same hand-up
`agent-runs-key-per-attached-instance-not-per-process` made for `agent.event`.

## What is left

Proof, and nothing else — the `agent-runs` sibling's shape. Neither behaviour
is pinned against a change that re-keys it per caller:

- `.cartridge/tests/service.test.ts:59` races `replayMemory` against
  `rememberVerified` in **one** context.
- `.cartridge/tests/service.test.ts:65` asserts only cross-session refusal and
  that a restarted `Service` refuses `stop` on a journalled job.

Both regressions below pass that 11-test file untouched.

## Commands and observed exit codes

All in the scratch worktree unless noted.

| # | Command | Exit |
|---|---|---|
| 1 | `git worktree add --detach $S/prdwt e32c02b` | 0 |
| 2 | `bun test ./.cartridge/tests/service.test.ts` (baseline, unmodified) | 0 — 11 pass, 0 fail |
| 3 | `bun test ./.cartridge/tests/service.test.ts` (with attempt-1) | 0 — 13 pass, 0 fail |
| 4 | regression A (`instance: this.instance` → `instance: context.call`, `:198`) + `bun test …/service.test.ts` | **1** — 12 pass, **1 fail**: only `the job journal is keyed by node …`. The 11 pre-existing tests all still pass, so the suite would not have caught it. |
| 5 | regression B (`hash(text)` → `hash(text + context.session)`, `:169`) + `bun test …/service.test.ts` | **1** — 12 pass, **1 fail**: only `the memory outbox replays once per pending acknowledgment …`. Same: the existing tests pass. |
| 6 | regression B′ (`deliveries` keyed `file + entry.session`) + `bun test …` | 0 — **no fail**. Discarded: `deliverMemory` reads the session out of the entry, so that key is the same key. Recorded because it shows the probe was run, not assumed. |
| 7 | spec Verify block 2 (guards) against regression A's tree | **1** |
| 8 | spec Verify block 2 (guards) against regression B's tree | **1** |
| 9 | spec Verify block 2 with `src/service.ts` renamed away | **1** (the leading `test -f` catches it, not a vacuous grep) |
| 10 | spec Verify block 3 with `src/service.ts` renamed away | **1** |
| 11 | spec Verify block 3 against a tree with `cartridge daemon` added to `src/` | **1**, printing `prd.ctg reaches for a host of its own` |
| 12 | `bun run check` (`tsc --noEmit`), patched tree | 0 |
| 13 | fresh worktree at `e32c02b`, `git apply --check attempt-1.patch` | 0 |
| 14 | same, `git apply attempt-1.patch` | 0 |
| 15 | same, spec Verify block 1 (`test -f` + `bun test …/service.test.ts` + `bun run check`) | 0 |
| 16 | same, spec Verify block 2 | 0 |
| 17 | same, spec Verify block 3 | 0 |

Every negative guard is written `if grep -qn 'pattern' path; then echo …; exit
1; fi` — no `!`-prefixed command, which `set -e` ignores — and every block
opens with `test -f` on each path it reads, so a rename fails it (rows 9, 10)
instead of passing vacuously.

## Failure evidence, not a question

`bun test ./.cartridge/tests/*.test.ts` (the repo's own `npm test` script) is
**already red at `e32c02b`** in a bare worktree: exit 1, 6 failures — 4
`statusline`, `records` "central records retain explicit owners and a
resolvable acyclic dependency graph", `parity` "migration preserves original
PRD fields …". Identical with and without attempt-1 (85 tests / 6 fail
pristine, 87 tests / 6 fail patched), so none of it is this change. Verify is
therefore scoped to `service.test.ts`. Pre-existing red in an unrelated file is
not this PRD's gate and is not a question for the coordinator either; flagging
it for whoever owns `statusline`.

## Acceptance boxes

Boxes 1 and 2 are provable from inside prd.ctg and are wired to the two new
tests. Box 3 is **not** observable from this repo — the same shape the memory
and agent siblings delegated. Proposed narrowing, for the coordinator to apply
(I have not edited `prd.md`):

> - [ ] prd.ctg's share of "exactly one prd node exists with the daemon
>       running": the cartridge builds one `Wire` and one `Service` per process
>       (`src/service.ts:232`, `:236`), refuses a second `apply` (`:235`), and
>       starts no host, daemon or node of its own — its only children are its
>       own engine CLI, `git` and `ps`. The daemon-wide count is delivered by
>       the done sibling
>       `an-instance-attaches-to-the-daemon-and-never-composes-silently` (this
>       PRD's `needs`) and re-proven composed by
>       `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`.

## Footprint change needed

The declared footprint is `src/service.ts` alone. The only file the spec
changes is `.cartridge/tests/service.test.ts`, which sits outside it — `collect`
would refuse. **Add `.cartridge/tests/service.test.ts` to the footprint** and
keep `src/service.ts` (unchanged, but the Verify guards read it). Same edit the
coordinator made for the agent sibling.
