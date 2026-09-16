# @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd-journals-and-outbox-replay-once-in-the-daemon review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd-journals-and-outbox-replay-once-in-the-daemon`,
`.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/prd-journals-and-outbox-replay-once-in-the-daemon/prd.md`.
Scope: one observable outcome — the one prd node owns the job journal and the memory outbox, so attached instances never double either. Executable leaf of the `one-daemon…` roll-up.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg `fe9d038f` (re-checked at the start and the end of this review; unchanged). `prd.md` and `specs/spec01.md` are dirty planning records in the working tree; `src/` and `.cartridge/tests/` are identical between `e32c02b` and `fe9d038f` (`git diff --name-only e32c02b fe9d038f -- src/ .cartridge/tests/` is empty), so the spec's nominal base is sound.

| Input | Content digest |
| --- | --- |
| Plan | `prds/…/prd-journals-and-outbox-replay-once-in-the-daemon/prd.md` — `21d73a4a80415ed564185641ca137990e811aece7f5ef92553f06c48427b601c` |
| Specs | `specs/spec01.md` — `f024219bd7f7f64866ef7ed04323aa29a49789d25a45c3ae13f5ee21d5ab9a36` (byte-identical to the loop draft) |
| Prototype | `.state/loop/…/attempt-1.patch` — `9b9fb6ce139e611187799e5e4e0f4411d4f13fb648924dbe33efd87d2db3e86e` (34 added lines, `.cartridge/tests/service.test.ts` only; `git apply --check` exit 0 at `fe9d038f`) |
| Analyst report | `analyst-1.md` — `09940d37483d33025a3cc0d4060b276320ef89dc9c6f0b6fa9c3b5800ac22e1e` |
| Material contracts | `prd.ctg@fe9d038f src/service.ts` — `c423d868086b5651fc7676b8f160174172d97c7f1840ae42d0a64960c59890f1`; `.cartridge/tests/service.test.ts` — `f5f3c6578f30fc60c893850b5a18ad38f90a4707dbdb4db474a5320283808339`; `src/lifecycle.ts:24`, `:225`, `:43-45` (lane and Verify runner); done `needs` sibling `an-instance-attaches-to-the-daemon-and-never-composes-silently` (`f364f46f`); done shape precedent `agent-runs-key-per-attached-instance-not-per-process` (`f7c38fe`) |

### Re-derivation of the central claim

The claim under review is that **neither audit finding survives one daemon and the third was never true**. Each leg was re-derived from `prd.ctg@fe9d038f src/service.ts`, not from the report. All three hold.

**Leg 1 — the `interrupted` marking (`:127`) dissolves. Confirmed, every sub-claim.**

- `instance = id()` is a field initialiser on `Service` (`:34`), so one id per `Service` object.
- `main()` builds exactly one `Service`, in the `apply` handler (`:236`); a second `apply` throws `cartridge is already applied` (`:235`).
- Jobs journal that id: `{ … instance: this.instance, invocation: key … }` (`:198`).
- **"never written back" — verified independently.** `saveJob` appears at `:117` (definition) and is *called* only at `:199` and `:200`, both inside the `run` branch. `job()` (`:122-129`) reassigns a fresh object (`job = { ...job, state: 'interrupted', … }`) and returns `this.publicJob(job)`; it never calls `saveJob` and the spread leaves `this.jobs`' entry untouched. The overlay is a read-time view only.
- **"only same-session" — verified.** `:125` `if (job.session !== context.session) throw Error('job belongs to another session')` sits *before* the overlay at `:127`.
- **Reachability — verified.** `this.job(` has exactly one call site, `:195`, guarded by `op === 'status' || op === 'stop'`; `prepare` (`:63`) refuses those ops unless `args.length === 1` and `/^[a-f0-9]{32}$/` matches, so no enumeration.

Conclusion: the key is the node, and with one node no live job can mismatch. Keeping the overlay is right — it still reports a journal left by a `Service` that really ended (node or daemon restart), which the pre-existing test at `.cartridge/tests/service.test.ts` ("asynchronous jobs enforce session ownership and never signal stale journals") already exercises across a restarted `Service`.

**Leg 2 — the double outbox replay (`:176`) dissolves. Confirmed, including the tick boundary.**

- `replayMemory()` occurs exactly twice in the file: the definition (`:175`) and one call, `void service.replayMemory()` in the `apply` handler (`:236`).
- Entry identity is `identifier = hash(text)` (`:169`) where `text` is the board basename plus the sorted-key JSON of the verified evidence — no `session`, `run` or `call`.
- `deliverMemory` single-flights by file path: `:149` returns the in-flight promise, `:160` registers it.
- **Tick-boundary claim — re-derived and correct.** `rememberVerified` is `async`; its body runs synchronously from entry until its first `await`. The evidence loop (`:167-171`), including `if (!fs.existsSync(file)) atomic(file, …)` at `:170`, contains no `await`. The first `await` in the body is `await this.deliverMemory(file)` at `:172`. `deliverMemory` is a *synchronous* function returning a promise: it runs `:149`, constructs the async IIFE — whose own body runs synchronously to *its* first `await`, which is `await this.memory(…)` at `:154` — then attaches `.finally` and executes `this.deliveries.set(file, work)` at `:160` before returning. So create (`:170`) and registration (`:160`) are in one uninterrupted synchronous run. No other agent can observe the file existing but unregistered. There is no create-then-deliver TOCTOU, and this is the specific window the PRD's "two instance-driven calls race inside the one node" pointed at.
- The durable retry budget (`attempts < 3`) lives in the entry file (`:152`, `:180`), not the process, so it survives node restart.

Conclusion: "replayed twice" required two `Service`s. Dissolved by one daemon.

**Leg 3 — "the journal claims every job on start" is false. Confirmed.**

- `grep -n 'readdirSync' src/service.ts` returns exactly one hit, `:178`, inside `replayMemory` on the outbox directory. Nothing scans the job journal.
- A journal file is read only at `:124`, on an in-memory miss, for an explicitly named job id.
- What the audit observed is `publish` (`:130-135`): every `command.*` event is sent on the node-wide `prd` channel (`this.host.publish('prd', event)`, `:133`), so one attached instance sees another's `claim`. Events carry `{session, run, call}` (`:131`) and no subscriber mutates a record.
- **Judgement on the hand-up: handing it to cartridge.ctg event routing is right.** `publish` names a cartridge-level channel key; narrowing it from inside prd.ctg would mean either renaming the channel (breaking every subscriber contract) or the host filtering by the `{session, run, call}` prd already stamps. prd.ctg has already supplied everything a router needs. This is the same hand-up `agent-runs-key-per-attached-instance-not-per-process` (`f7c38fe`) made for `agent.event` and that was accepted, so the precedent is consistent.

### Coordinator edits

- **Footprint gained `.cartridge/tests/service.test.ts`.** Correct and necessary: the spec changes only that file, the declared footprint was `src/service.ts` alone, and `collect` refuses out-of-footprint writes. Keeping `src/service.ts` is also correct — Verify blocks 2 and 3 read it, and `prd collect` only commits *changed* in-footprint paths, so an unchanged `src/service.ts` costs nothing. Same edit as the agent sibling.
- **Box 3 narrowed.** Diffed against `analyst-1.md`'s proposed block: verbatim, including the two delegating sibling names. The narrowing is honest — the daemon-wide node count genuinely is not observable from inside prd.ctg, and it is delegated to a `needs` sibling that is `state: done` (`f364f46f`) plus the composed test PRD.
- Frontmatter otherwise carries only engine-written `state: analyzing` and `claim`. The body gained an Acceptance replacement and a new `## Planning note`; no rewrite from a draft.

### Non-vacuity

| Probe | Result |
| --- | --- |
| **A** `instance: this.instance` → `instance: context.call` (`:198`) | `bun test ./.cartridge/tests/service.test.ts` → exit 1, 12 pass / **1 fail**, and the one failure is `the job journal is keyed by node…`. All 11 pre-existing tests and the new outbox test pass. Verify block 2 also exits 1; Verify block 1 exits 1. |
| **B** `hash(text)` → `hash(text + context.session)` (`:169`) | exit 1, 12 pass / **1 fail**, the one failure is `the memory outbox replays once per pending acknowledgment…`. Verify block 2 exits 1. |
| **B′** `deliveries` keyed `file + entry.session` | exit 0, **13 pass / 0 fail** — reproduced, discarded correctly. `deliverMemory` reads `session` out of the entry file, and that file is created once by whichever caller arrives first (`:170`), so both callers compute the identical key. B′ changes no behaviour; it is not a regression. Verify block 2 *does* catch it (exit 1), because the literal guard `if (this.deliveries.has(file)) return this.deliveries.get(file)!;` no longer matches. |
| **B″ (reviewer-added)** a *genuine* per-caller single-flight key: `deliverMemory(file, who)` keyed `file + who`, with `rememberVerified` passing `context.session` | exit 1, 11 pass / **2 fail**: the new `the memory outbox replays once per pending acknowledgment…` **and** the pre-existing `memory replay acknowledges once and deduplicates simultaneous deliveries`. |

B″ answers the concern that B′'s non-failure means the outbox test is weak: it does not. The delivery-key axis *is* covered; B′ simply was not a change. The new outbox test's unique contribution over the pre-existing one is entry *identity* (B), which the pre-existing single-context test cannot reach — confirmed by B failing only the new test.

The new `service.test.ts` was run 5 consecutive times on the patched tree: 13 pass / 0 fail every time, ~3.9 s. No flakiness observed in the `--dry` job race the spec calls out.

### Validation actually run

Scratch worktrees of `prd.ctg` under the session scratchpad. The live `.cartridge/boards` tree was read only, never written or run against; the live project daemon was never started, stopped, replaced or reloaded. All Verify blocks were executed verbatim as `sh -eu -c "<block>"`, repo-root-relative, with no `cd`. No cargo is involved (TypeScript repo), so the `CARGO_TARGET_DIR` rule does not apply.

| # | Command (cwd) | Exit |
| --- | --- | ---: |
| 1 | `git -C prd.ctg rev-parse HEAD` → `fe9d038f…` (start and end of review, unchanged) | 0 |
| 2 | `git diff --name-only e32c02b fe9d038f -- src/ .cartridge/tests/` → empty | 0 |
| 3 | `git worktree add --detach <scratch>/wt-head fe9d038f`, `node_modules` symlinked | 0 |
| 4 | `git apply --check attempt-1.patch` (wt-head) | 0 |
| 5 | `bun test ./.cartridge/tests/service.test.ts` — unpatched baseline, 11 pass / 0 fail | 0 |
| 6 | `bun test ./.cartridge/tests/*.test.ts` — unpatched, Ran 85, 76 pass / **6 fail** (4 `statusline`, `records` owners/graph, `parity` migration) | 1 |
| 7 | `git apply attempt-1.patch` (wt-head) | 0 |
| 8 | `bun test ./.cartridge/tests/service.test.ts` — patched, 13 pass / 0 fail | 0 |
| 9 | `bun test ./.cartridge/tests/*.test.ts` — patched, Ran 87, 78 pass / **6 fail**, the same six by name | 1 |
| 10 | Verify block 1 verbatim (`test -f` + `bun test` + `bun run check`), patched repo-shaped tree; measured 4 s of the 120 s limit | 0 |
| 11 | Verify block 2 verbatim, patched tree | 0 |
| 12 | Verify block 3 verbatim, patched tree | 0 |
| 13 | regression A + `bun test …/service.test.ts` | 1 |
| 14 | regression A + Verify block 2 | 1 |
| 15 | regression A + Verify block 1 | 1 |
| 16 | regression B + `bun test …/service.test.ts` | 1 |
| 17 | regression B + Verify block 2 | 1 |
| 18 | regression B′ + `bun test …/service.test.ts` — **no failure**, as the analyst reported | 0 |
| 19 | regression B′ + Verify block 2 | 1 |
| 20 | regression B″ (reviewer) + `bun test …/service.test.ts` — 2 failures | 1 |
| 21 | Verify block 2 with `src/service.ts` renamed away | 1 |
| 22 | Verify block 3 with `src/service.ts` renamed away | 1 |
| 23 | Verify block 1 with `.cartridge/tests/service.test.ts` renamed away | 1 |
| 24 | Verify block 2 with `.cartridge/tests/service.test.ts` renamed away | 1 |
| 25 | Verify block 3 against a tree with `// cartridge daemon` appended to `src/cli.ts` — printed `prd.ctg reaches for a host of its own` | 1 |
| 26 | `bun test ./.cartridge/tests/service.test.ts` × 5 on the patched tree — 13 pass / 0 fail each | 0 |
| 27 | Verify block 1 in a **bare** worktree with no `node_modules` anywhere above it — `error: Cannot find package 'yaml' from src/records.ts`, and `bun run check` reports `TS2307: Cannot find module 'yaml'` | 1 |
| 28 | Verify block 1 in a worktree nested as the real lane is (`<root-with-node_modules>/.cartridge/boards/root/.lanes/lane`), patched, **no local `node_modules`** — 13 pass / 0 fail, `tsc --noEmit` clean | 0 |
| 29 | Verify blocks 2 and 3 in that simulated lane | 0, 0 |
| 30 | `git status --porcelain` in the simulated lane after all three blocks — only ` M .cartridge/tests/service.test.ts` (the patch); no block wrote inside the footprint | 0 |
| 31 | `git apply --check attempt-1.patch` in a fresh worktree at the re-checked HEAD | 0 |

Rows 27–29 settle a risk neither the analyst nor the spec records. `src/lifecycle.ts:225` creates the lane with `git worktree add -b <branch> <dir> HEAD`, which carries no `node_modules`, and row 27 shows Verify block 1 *fails* in such a tree. It passes in the real lane only because `lane()` (`:24`) places the worktree at `prd.board/.lanes/<slug>` — i.e. **inside** `prd.ctg` — so Node/Bun resolution walks up to `prd.ctg/node_modules` and `prd.ctg/node_modules/.bin/tsc`. Row 28 reproduces that nesting exactly and passes. The block is therefore sound as written, but its correctness rests on an unstated property of the lane's location.

No guard in any block is `!`-prefixed (every negative is `if grep -qn … ; then echo …; exit 1; fi`), and every block opens with `test -f` on each path it reads, so a rename fails it (rows 21–24) rather than passing vacuously.

**Judgement on scoping Verify to `service.test.ts`: honest, and it hides nothing.** Rows 6 and 9 show the same six failures by name with and without the patch. I inspected the two non-`statusline` reds: `records.test.ts:34-38` scans the *live committed board* (`boards/root`) and asserts every id in the `record-migration` manifest is still present, and `parity` does the same against a `git archive` of `3d1848d7`. They are red from board-record drift committed into prd.ctg, not from anything under `src/`. Since this spec changes no `src/` file at all, the full suite could not add signal here.

### Findings

1. **(non-blocking, scope wording)** The PRD's `## What changes` still reads "removes any per-process assumption … that would still misbehave if two instance-driven calls race inside the one node", while the Planning note concludes nothing is removed. A reader of `What changes` alone infers a code change that the spec explicitly forbids (spec step 2: "if a step wants to edit it, stop and report"). The agent sibling rewrote its `What changes` to state the dissolved premise. *Recommendation:* one sentence in `What changes` saying the premise dissolved and the slice is proof-only. Not blocking — the Planning note, the spec and the Acceptance boxes are unambiguous.
2. **(non-blocking, traceability)** The leg-3 hand-up to cartridge.ctg event routing exists only in this child's Planning note and the spec's Remaining risk. The agent sibling's `agent.event` hand-up sits in the same place. Two hand-ups now live only in child planning notes with nothing on the parent roll-up or a sibling PRD to carry them. *Recommendation:* one line on the parent's audit or a `needs`-less note PRD, at the coordinator's discretion.
3. **(non-blocking, evidence precision)** The known-red note flags all six pre-existing failures "for whoever owns `statusline`". Two of them (`records`, `parity`) are board-record drift, not `statusline` code. *Recommendation:* attribute them separately, since a board rename in this very loop is a plausible cause.
4. **(non-blocking, undocumented dependency)** Verify block 1 needs `node_modules` resolvable from the lane; it is resolvable only because the lane nests inside `prd.ctg` (rows 27–28). *Recommendation:* one line in Remaining risk, so a future lane relocation does not silently turn Verify red.
5. **(non-blocking, coverage nuance)** The job test models "a second attached instance" as a different `run`/`call` in the **same** `session`. That is the only configuration in which the overlay at `:127` is reachable at all (`:125` refuses a foreign session outright), so the choice is right, and the spec states it plainly. It does mean acceptance box 1 is proven for the run-level reading of "instance"; the session-level reading is satisfied trivially by the `:125` refusal, which the pre-existing test already covers.

Nothing above blocks: no finding changes a contract, an acceptance check, a footprint or a Verify outcome.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One observable outcome; premise correctly dissolved and independently re-derived; box 3 narrowed to prd.ctg's provable share with the daemon-wide count delegated to a `done` sibling. −2: `## What changes` still promises a removal the spec forbids (finding 1). |
| Ownership and reuse | 19 | `repo: prd.ctg`, `capability-owner: prd`; footprint corrected to exactly the file the spec touches; no new abstraction — two tests appended to the existing `service.test.ts` reusing its `call`/`value`/`atomic` helpers; leg-3 hand-up matches the accepted `f7c38fe` precedent and is genuinely host-side. −1: hand-up recorded only in the child's Planning note (finding 2). |
| Dependencies and implementable slices | 20 | `needs` sibling is `state: done` (`f364f46f`); one spec, one file, 34 lines; base re-checked against a moved HEAD and `git apply --check` exits 0 at `fe9d038f`; `src/` and tests unchanged `e32c02b`→`fe9d038f`. No deduction. |
| Observable acceptance and baseline evidence | 19 | Each acceptance box maps to a named test or a Verify guard; A and B each fail *only* their matching new test with all 11 pre-existing passing; B′ reproduced as a non-regression and correctly discarded; reviewer-added B″ shows the delivery-key axis *is* covered; all guards non-vacuous under rename; 5/5 stable runs; blocks run in 4 s of 120 s and write nothing inside the footprint. −1: finding 5's run-level reading of "attached instance". |
| Failure, recovery and compatibility | 18 | Scoping to `service.test.ts` verified honest — identical six reds by name with and without the patch, and both non-`statusline` reds traced to board-record drift, not code. Verify's grep guards will fail on innocuous reformatting of `:149`/`:198`, which is the intended pinning but a future churn cost. −1 finding 3 (mis-routed known-red attribution), −1 finding 4 (undocumented lane `node_modules` dependency). |
| Reviewer total | **94** / 100 | ≥ 90 and no blocking finding. |

Findings and concrete revisions: five non-blocking findings above, each with a recommendation; none gates implementation.
Disposition: **keep**. Proceed to implementation of `spec01` as written (apply `attempt-1.patch`, no `src/` change).
Validation: rows 1–31 above; scratch worktrees under the session scratchpad; live boards read-only; live daemon untouched.
Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS**.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation; optionally fold findings 1–4 into the PRD body and the spec's Remaining risk as a formatting-level clarification, which does not consume a round if it makes no semantic change.
