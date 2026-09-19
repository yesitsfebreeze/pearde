# @runtime/a-cartridge-call-can-be-cancelled review history

Plan: `@runtime/a-cartridge-call-can-be-cancelled`, `prds/a-cartridge-call-can-be-cancelled/prd.md`.
Scope: one observable outcome — an abandoned caller releases the provider's resources; executable leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the prd board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `cartridge.ctg` at `d1692932449c89106bb1928b717146ee8b0083a8`
(worktree clean at review start and end). No dirty files in the reviewed inputs.

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-cartridge-call-can-be-cancelled/prd.md` — `6655277d0e693c7e758fc09582e7aa0dc29131fde9a6a810638a0f1d744a7bd9` |
| Specs | `specs/spec01.md` — `6f953bd495a015049df7c5f9a6907fb792f4fa8a362c45e5a037fc3a08e37609` |
| Material contracts/dependencies | `prd.ctg/src/planner.ts` `fd60f4c7…` (`feet`), `prd.ctg/src/lifecycle.ts` `177200f0…` (footprint guards), `cartridge.ctg@d169293` `src/transport/{cartridge.rs,rpc.rs}`, `src/node/mod.rs` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The defect is real and precisely located; I confirmed every cited line at `d169293`. `serve` (`cartridge.rs:820-823`) drops notifications, so a cancel frame already reaches the provider and is discarded; the permit (`:27`, `:851`, `:855-858`) is held to completion; `spawn_blocking(block_on(listener))` (`:944-948`) cannot be aborted. One outcome, stated ceilings (next await point; `event` arm only). −2: the spec never says what the provider does with the `Request` once the listener is cancelled (see N1). |
| Ownership and reuse | 17 | Right owner and right layer; reuses `CancellationToken`, already imported at `cartridge.rs:13`; no new caller API — `Waiting::drop` is the exact abandonment predicate because `dispatch` (`rpc.rs:349-353`) removes the id on a response. −3: the sibling analysis is correct but stale against the records (N3): two of its three recommendations are already written into the PRDs it names. |
| Dependencies and implementable slices | 19 | I implemented the three described hunks myself, from the spec text alone, in an independent clone: the gate passes and the full library suite is **161 passed, 0 failed**. A spec another agent can execute blind is an implementable slice. `feet()` (`planner.ts:5-9`) is verified a union of the PRD footprint with `specs(prd)` (`records.ts:341-344`, every `.md` in `specs/`, no publication state), and `lifecycle.ts:129/144/152/173` all read `feet(prd)`, so `src/transport/tests/cartridge.rs` is collectable with no PRD edit. −1: N4. |
| Observable acceptance and baseline evidence | 11 | The gate is above this board's average and its `Drop` guard is sound (see ruling below), but it is beatable. **I passed the whole Verify block, exit 0, on a tree that implements no cancellation whatsoever.** The block also never runs the other 160 tests. |
| Failure, recovery and compatibility | 13 | The deadlock the PRD explicitly owns is argued by construction — correctly, and I reproduced the green suite — but the one code shape the hazard names is executed by no test in the gate and none in the suite (B3). Compatibility is otherwise good: the cancel is a notification, an old provider ignores it, an old caller sends none. |
| Reviewer total | **78** / 100 | Below the 90 threshold; three blocking findings. |

### Reproduced cheat table (my own trees, my own reference)

Five clones of `cartridge.ctg` at `d169293`, one shared `CARGO_TARGET_DIR` outside every
repository, the spec's Verify block run verbatim as `sh -eu`.

| tree | what it is | block exit | observed |
| --- | --- | ---: | --- |
| reference | my own implementation of the spec's three hunks + the spec's test | **0** | gate green, base transplant fails; full suite 161 passed / 0 failed |
| base | `d169293` untouched + the spec's test | **1** | step 1: `left: 0 / right: 64` |
| surface | `Request::id`, `cancels: HashMap<u64, CancellationToken>`, a `cancel` notification arm, the token threaded into `handle` — every token present, nothing wired | **1** | step 1: same assertion, `left: 0 / right: 64` |
| inert | `d169293` + the gate's name and an empty body | **1** | step 1 green, step 2: `the gate does not discriminate` |
| **cheat (new)** | `IN_FLIGHT: 64 → 65` and a test under the gate's name whose body is `assert_eq!(IN_FLIGHT, 65)` | **0** | **the gate passes with zero cancellation implemented** |
| no-build (new) | a test calling a function that exists only in the changed tree | **1** | step 2: compile error at base → no `test result:` line → rejected |

Cost reproduced: **9.05 s** with a cold `CARGO_TARGET_DIR`, **2.18 s** warm, against the
engine's 120 s limit — the analyst's 9.0 s / 3.2 s confirmed on this machine.

### Findings

**B1 (blocking) — the discrimination step pins the test's name, not its observation.**
Evidence: the `cheat` row above. The block's only constraints are (a) a test whose
name contains `$NAME` passes here as exactly one test, (b) the same *file*, transplanted
onto `$BASE`, builds and fails. Any behavioural difference between the two trees that
the named test can see satisfies (b). A one-character mutation of a private constant,
plus a three-line assertion carrying the spec's own failure message, clears the gate at
exit 0 and cancels nothing. The idea is right — this is mutation gating and it is the
strongest thing on this board — but as written it certifies "this tree differs from base
in a way this test sees", not "a cancelled call stops its listener".
Recommendation (text-free, so it hands out no bypass): make step 2 a *partial-application*
check. Transplant onto the base tree the test plus **only** `src/transport/rpc.rs` from
this tree, and require a failure; then the test plus **only** `src/transport/cartridge.rs`,
and require a failure. Passing then requires an observation that depends on both files
changing together, which a single-constant or single-file mutation cannot fake. Both
extra trees are the same compile cost already measured (two more cached builds).

**B2 (blocking) — the gate never runs the rest of the suite.**
`cargo test --lib "$NAME"` filters to one test in both steps, so a change that breaks the
other 160 tests collects green. My `cheat` tree is the live example: `IN_FLIGHT = 65`
directly contradicts `a_connection_runs_at_most_its_in_flight_limit_at_once`, and the
block never notices. Recommendation: add an unfiltered `cargo test --lib` to step 1
(measured 14.99 s on the reference tree, inside the 120 s budget). This is also the
cheapest partial defence against B1.

**B3 (blocking) — the hazard the PRD owns is exercised by nothing.**
The PRD says the deadlock analysis "is the analysis this PRD owns" and that an analyst
who cannot show the hazard is not reopened is not finished. The spec's argument is
structural and I agree with it: the `select!` goes inside `block_on`, the
`spawn_blocking(move || runtime.block_on(...))` statement keeps its shape, nothing moves
onto a worker. I verified that by writing the change and getting 161 green. But the
comment at `:939-941` is about a **listener that takes its node's Lua lock
synchronously** — `node/mod.rs:28-33`, `wait()` → `block_in_place`. The gating test's
listener is a plain Rust closure registered with `ctx.on`; it never enters a node, never
takes that lock, and never awaits another cartridge. So the new capability — *dropping a
listener future mid-flight* — is executed only against a `tokio::time::sleep`, and never
against the shape the hazard names. A green suite is evidence of no regression; it is not
evidence that cancelling a lock-taking, nested-calling listener is safe, because no test
cancels one. Recommendation: add a second named test in which the listener awaits another
cartridge call (`ctx.on` + `ctx.bail`, both present at the base revision) and is cancelled
mid-call; assert both that its guard drops and that the connection still serves. This
contends, it is writable at base surface, and it is what turns the hazard analysis from
INFERRED into measured.

**N1 (non-blocking) — the reply on the cancelled path is unspecified.** `handle` owns the
`Request`; the spec does not say whether it replies, drops it, or returns. `impl Drop for
Request` (`rpc.rs:118-126`) pushes `request dropped without a reply` back over the wire.
Because `Waiting::drop` fires for *every* abandonment, not only a timeout, a caller whose
connection is still alive receives an `INTERNAL_ERROR` frame for an id it no longer
tracks (harmless — `dispatch` drops unknown ids — but it belongs in the spec). State the
intended behaviour; my reference implementation chose "answer nobody".

**N2 (non-blocking)** — `Waiting` is constructed before `out.send` (`rpc.rs:248-252`), so
the send-failure path emits a cancel for a request that never left. Harmless on a closed
peer; worth one line.

**N3 (non-blocking) — the sibling analysis is right but already recorded.**
`@mcp/a-cancelled-tool-call-reaches-its-running-tool` **already** declares
`needs: "@runtime/a-cartridge-call-can-be-cancelled"`, and
`@runtime/a-wedged-call-reports-its-late-answer` **already** declares
`needs: "a-cartridge-call-can-be-cancelled"` — so `refusal()` (`planner.ts:22-36`) already
refuses to dispatch the wedged-call PRD until this one is done, and the "do not dispatch
concurrently" advice needs no coordinator action. The `@mcp/…the-mcp-event-declares-its-own-bound`
ruling is correct and verified: its footprint is `cartridge.json` in `mcp.ctg`, zero
overlap, and neither should `needs` the other.

**N4 (non-blocking)** — `src/node/mod.rs` stays in the PRD footprint. Since `feet()` is a
union, the spec omitting it narrows nothing: the path is still reserved and still counts
in `clash()`. The spec's wording ("is **not needed**") should not be read as a narrowing.

### Guard-shape audit

No statement-level `! grep`, no `grep 'a\|b'` alternation, no
`test -n "$X" && test "$X" -ge N`. Both text conditions are
`grep -q … || { echo …; exit 1; }`, which fails correctly under `set -e`. Both failure
messages name the property rather than the token that satisfies it. The block correctly
distinguishes **does not build at base** from **fails at base**: a compile error produces
no `test result:` line, so `grep -q 'test result: FAILED'` fails and the block exits 1
(measured, `no-build` row). The `cargo test --lib <filter>` no-match hole is real and the
`test result: ok. 1 passed` condition closes it (measured on the `inert` row).

### Ruling on the `Drop` guard

Sound. `Bell` is constructed inside the listener's own async body, so it exists only in
the provider-side future's state; it cannot be reached from `src/transport/`, and no
caller-side drop can increment it. The listener's `sleep(3 s)` cannot elapse inside the
test's 350 ms window, so a completed listener cannot ring it either. Confirmed by
measurement, not argument: the base tree reports `left: 0`, meaning the caller's timeout
alone rings nothing. The permit clause is likewise observed by a second call being served,
not by a string.

Findings and concrete revisions: B1, B2, B3 above, each with a bounded fix. Resolution pending the next round.
Disposition: revise — the plan, the change and the `Drop` guard are right; the Verify block under-constrains the test it gates and the PRD's own hazard is unexercised.
Validation: cwd `/private/tmp/claude-501/…/scratchpad/reviewer-cancel`; six clones of `cartridge.ctg@d169293`; `CARGO_TARGET_DIR` outside every repository; the spec's Verify block run verbatim as `sh -eu`; exit codes 0/1/1/1/0/1 as tabled; `cargo test --lib` on the reference tree 161 passed / 0 failed in 14.99 s; block cost 9.05 s cold, 2.18 s warm. `git -C cartridge.ctg status --porcelain` empty before and after, HEAD `d169293` unchanged, `git worktree list` unchanged (3 entries, none mine), 2 daemons before and after, none started or killed.
Reviewer identity: reviewer-cancel (independent review sub-agent, Opus 5 1M), round 1.
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL** (78/100, three blocking findings).
Unresolved blocking findings: B1 the discrimination step pins the test name, not its observation (defeated, exit 0, zero cancellation); B2 the gate never runs the remaining 160 tests; B3 no test anywhere cancels a listener of the shape the PRD's deadlock hazard names.
Rounds used / remaining: 1 / 4.
Next action: bounded revision of the Verify block (partial-application discrimination + unfiltered suite run) and one added gating test that cancels a nested, lock-taking listener; then round 2.

## Round 2 — 2026-09-17

Presented revision: `specs/spec01.md` second revision (the analyst's `spec02` draft, landed at
`specs/spec01.md`), against `cartridge.ctg` at `d1692932449c89106bb1928b717146ee8b0083a8`
(worktree clean, HEAD unchanged, at review start and end).

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-cartridge-call-can-be-cancelled/prd.md` — `6655277d0e693c7e758fc09582e7aa0dc29131fde9a6a810638a0f1d744a7bd9` (unchanged from round 1) |
| Specs | `specs/spec01.md` — `e1ddcd7a3e8dbfef7dd1870d3e4e57e8df26bbe780d42088116c7ce4c769c864` |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts:39-45` (verify runner: `sh -eu -c`, 120 s, **no injected environment**), `prd.ctg/src/planner.ts:5-9` (`feet`), `cartridge.ctg@d169293` `src/transport/{cartridge.rs,rpc.rs,tests/cartridge.rs}` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged defect analysis, all lines re-confirmed at `d169293`. N1 is closed: the spec now states the cancelled call is answered `Err(application("cancelled"))` and why (`impl Drop for Request`, `rpc.rs:117-129`, would otherwise push an untrue INTERNAL_ERROR). N2 closed in the "two edges" paragraph. |
| Ownership and reuse | 18 | Right owner, right layer, no new caller API; `Waiting::drop` remains the exact abandonment predicate. `src/transport/tests/cartridge.rs` is declared in the spec footprint and `feet()` unions it, so the gate's own test file is collectable. −2: N4 stands (the spec's "`src/node/mod.rs` is **not needed**" narrows nothing — the PRD footprint still reserves it). |
| Dependencies and implementable slices | 19 | I implemented the three hunks **again, blind, from the spec text alone** in my own clone (`Request::id`, cancel notification in `Waiting::drop`, `cancels: HashMap<u64, CancellationToken>` in `serve`, `select!` inside the existing `spawn_blocking(move \|\| runtime.block_on(...))`). Result: 163 passed / 0 failed, block exit 0 in 46 s warm. A spec two different agents can execute blind is an implementable slice. |
| Observable acceptance and baseline evidence | 12 | Real gains: the suite is unfiltered (base is now rejected `161 passed; 2 failed`), the named tests are confirmed from the suite's own output, the three-way planting is correctly implemented, and the nothing-applied/half-applied distinction is enforced exactly as written. But **I defeated the partial-application step on my first attempt** (B1-R2 below, block exit 0 with zero cancellation), and the block as written **cannot run under collection at all** (B4, `BASE` is never set by the engine). |
| Failure, recovery and compatibility | 15 | `a_cancelled_call_stops_a_listener_waiting_on_another_cartridge` is real, executed, and fails on base with `left: 0 / right: 1` — the shape the PRD's hazard names (a listener parked on another cartridge's answer) is now cancelled by an executed test, not by argument. The hang the analyst reports is genuinely fixed: the base tree fails in bounded time, no wedge. −5: the "listener must never run on a tokio worker" invariant is un-gated (the `wedge` tree is exit 0 — reproduced), and the permit-held window between the cancel and the next await is stated but unmeasured. |
| Reviewer total | **83** / 100 | Below 90. One blocking finding (B4); two recorded ceilings. |

### Reproduced table — my own trees, my own reference, my own cheat

Four trees cut from `d169293` (`git clone --local`), one `CARGO_TARGET_DIR` outside every
repository, the spec's Verify block run verbatim as `sh -eu` with `BASE` supplied by hand.

| tree | what it is | block exit | rejected by |
| --- | --- | ---: | --- |
| reference (mine) | my own implementation of the three hunks + the spec's three tests | **0** | — (46 s warm; serial suite alone 34.6 s of it, 163 tests) |
| base | `d169293` + the three tests | **1** | step 1: `test result: FAILED. 161 passed; 2 failed`, both cancellation tests, nothing else — confirms the analyst's row exactly |
| **const2 (my new cheat)** | **one pre-existing constant mutated in *each* file — `rpc::PARSE_ERROR` −32700→−32701 and `MAX_FRAME` +1 — and the two gate names asserting both constants. Nothing else. No cancellation whatsoever.** | **0** | **NOT REJECTED — see B1-R2** |
| wedge | my reference with the listener awaited directly on the worker (the hazard reopened) | **0** | not rejected — the analyst's declared ceiling, reproduced |

`const2`'s suite is green (`163 passed; 0 failed`), and all six planting runs report
`test result: FAILED` — i.e. it satisfies "must build and fail with nothing applied" and
"must not pass with either half" while observing nothing but two integers.

### Verdicts on round 1's findings

**B2 — CLOSED.** Step 1 is an unfiltered `cargo test --lib -- --test-threads=1`; my `base`
tree is rejected by it with the whole-suite line, and my reference's 163-test green run is
the same suite. The per-test cargo invocations are gone and the named tests are read out of
the suite's own log (`::$name ... ok`), which keeps the empty-filter hole closed for free.
The serial finding checks out as the analyst reports: the flake is *its own* tests
interacting with the pre-existing thread-local log capture, not a pre-existing flake, and
`--test-threads=1` removes it. **Cost, stated plainly:** the whole 163-test library suite
now runs serially inside a 120 s block — 34.6 s measured, of a 46 s block. That is the
right trade (a flaky gate is worse than a slow one), but the margin is thinner than it
looks: the three plantings re-extract fresh trees every run, so a cold or `kache`-missing
build has no room. The spec says this; it is honest, not hidden.

**B3 — CLOSED for the nested listener, CEILING ACCEPTED for the worker invariant.** See
the ruling below.

**B1 — NOT CLOSED, but no longer blocking; recorded as the gate's ceiling.** The
partial-application step is a genuine improvement: it kills round 1's single-constant cheat
(a constant lives in one file, so it passes when that file alone is applied). It does not
constrain the *observation*. The property it actually enforces is "this test sees a
difference that needs both files", and a mutation of one pre-existing constant per file
satisfies that for 12 lines of work: `const2`, exit 0, suite green, all three plantings
red, zero cancellation. The step raised the price of a fake from one constant to two.
Under the review method's own rule (`review-plan.md:60-69` and the "gate is defeated again"
row) this is exactly the ceiling that rule anticipates: judge and judged run in one
process, one round was spent on the gate, the gate was defeated again. It is therefore
**recorded as a ceiling with its defeated attempt, with the diff reading named as the
backstop** — and it is not by itself a blocking finding. I performed that backstop reading
twice over: I wrote the change from the spec text and read the `event` arm on my own tree.
No further round should be spent hardening this gate.

### Ruling on the declared ceiling (the `wedge` tree)

**Accepted, non-blocking.** Reproduced: my `wedge` tree — the reference with the listener
awaited on the worker instead of handed to `spawn_blocking` — is block exit 0.

What tips it to accepted:
- The invariant is preserved by a *textual* property of the diff that a reviewer checks in
  five lines: the statement `tokio::task::spawn_blocking(move || runtime.block_on(...))`
  is unchanged and the `select!` is nested *inside* it. Nothing moves onto a worker,
  nothing is aborted, no lock is added. I confirmed that by writing the change myself.
- The `wedge` shape is not reachable by executing this spec. It requires deleting a line
  the spec tells the implementer to keep, against a comment in the source that says why.
  A gate defends against an implementation that drifts; this one would have to be deleted
  on purpose.
- The analyst declined the gate that would have looked closed and been worthless (a grep
  for `spawn_blocking`, which a comment satisfies), named the failed discriminator and the
  exact reason it failed (one worker, the ping racing the listener's first poll), and named
  the honest upgrade path (thread identity inside the listener). That is the behaviour the
  method asks for at a ceiling.
- The PRD's hazard has two halves. The half about *cancelling* a listener that is parked on
  another cartridge — the novel capability, the thing that could plausibly deadlock — is now
  executed by `a_cancelled_call_stops_a_listener_waiting_on_another_cartridge`. Only the
  "never on a worker" half, which the change does not touch, is un-gated.

What would have tipped it the other way, recorded so the next reviewer can hold the line:
if the change had *altered* the `spawn_blocking(block_on(...))` shape (then the un-gated
invariant would be the PRD's own product and a diff reading would not be enough), if the
ceiling had been undeclared or dressed as covered, or if `a_listener_that_blocks_does_not_
park_the_only_worker` had been kept while claiming it gates the invariant. None of those
holds. Keep the test — it is deterministic green on a correct tree and only its *failure*
is racy, so it can produce a false green on a wrong tree but never a false red on a right
one.

### New finding

**B4 (blocking, mechanical) — the block cannot run under collection: `BASE` is never set.**
Line 2 of the Verify block is `BASE="${BASE:?}"`. `verify()` (`prd.ctg/src/lifecycle.ts:39-45`)
runs `['sh','-eu','-c', block.command]` with `{ cwd, signal, timeout: 120_000 }` and injects
no environment; nothing in the engine, the lane or the collector defines `BASE`. Under
`sh -eu`, `${BASE:?}` aborts the block immediately, so **both passes fail** and the PRD
cannot collect. Every measurement in this spec (mine and the analyst's) was taken with
`BASE` supplied by hand on the command line, which is why it was not noticed. It fails
closed, so it cannot pass anything wrongly. Fix is one character class:
`BASE="${BASE:-d1692932449c89106bb1928b717146ee8b0083a8}"` — the base revision is already
stated at the top of the spec. Re-measure nothing; the block is otherwise byte-identical.

### Hang check (the analyst's own report, verified)

Confirmed. On my `base` tree — which cancels nothing — the block returns exit 1 in bounded
time, rejected by the suite, with `a_cancelled_call_stops_a_listener_waiting_on_another_cartridge`
failing on its `Bell` assertion (`left: 0 / right: 1`). The listener's nested call is
bounded at 900 ms inside the listener, so a non-cancelling tree cannot leave a blocking
task parked on a socket read at runtime shutdown. No run of mine approached the 120 s
limit; the longest block was 46 s.

### The two discarded mutations (`seq` in the subscribe reply; the listener-less reply)

Confirmed as a real coverage gap, and the analyst was right not to report them as gate
evidence — they say nothing about *this* gate. `serve`'s `subscribe` arm replies
`{"seq": seq}` (`cartridge.rs:838-840`) and the listener-less `event` path replies
`Value::Null` (`:975-978`); no library test asserts either. **That gap belongs to a new
PRD, not to this one.** This PRD owns one outcome (an abandoned call releases the
provider's resources); neither mutation is on that path, and widening the gate to cover the
rest of the transport's reply shapes is scope this leaf should not carry. Worth one line in
the runtime board's backlog as "the subscribe/listener-less reply shapes are unasserted".

### Guard-shape audit

Clean. No statement-level `! grep`; no `grep 'a\|b'` alternation; no
`test -n "$X" && test "$X" -ge N`. Every text condition is either
`grep -q … || { …; exit 1; }` or `if grep -q …; then exit 1; fi` — the analyst's own
correction of a `grep -q X && { exit 1; }` is right and the fixed form is what is in the
file. `run_there` ends `|| true` deliberately, and the verdict is taken from the log, not
the exit code, which is correct for a step that must distinguish "failed" from "did not
build". Failure messages name properties, never the token that satisfies them.

Findings and concrete revisions: B4 (blocking, one-line fix); B1-R2 recorded as the gate's
ceiling with its defeated attempt (`const2`); the `wedge` ceiling accepted as declared;
N4 stands from round 1.
Disposition: revise — one line, then re-review. The plan, the change, the tests and the
ceilings are sound; the block cannot execute as written.
Validation: cwd `/private/tmp/claude-501/…/scratchpad/reviewer-cancel-r2`; four
`git clone --local` trees of `cartridge.ctg@d169293`; `CARGO_TARGET_DIR` outside every
repository; the spec's Verify block run verbatim as `sh -eu` with `BASE` exported by hand;
exit codes reference **0**, base **1**, const2 **0**, wedge **0**; reference block 46 s
(serial suite 34.6 s, 163 tests) against the engine's 120 s.
`git -C cartridge.ctg status --porcelain` empty before and after, HEAD
`d1692932449c89106bb1928b717146ee8b0083a8` unchanged, no worktree created or removed by me
(`git worktree list` is 2 entries; `/Users/feb/dev/cxr5-cartridge` was listed at my start
and is gone at my end — another session owns it, exactly the drift the analyst recorded).
One daemon before and after, untouched; no process killed.
Reviewer identity: reviewer-cancel-r2 (independent review sub-agent, Opus 5 1M), round 2.
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL** (83/100, one blocking finding).
Unresolved blocking findings: B4 — `BASE` is unset under `verify()`, so the block aborts at
line 2 in both passes and the PRD cannot collect.
Recorded ceilings (not blocking, per `review-plan.md:60-69`): the discrimination step is
defeatable by one mutated constant per file (`const2`, exit 0, measured); the "listener
must not run on a tokio worker" invariant is held by review of the `event` arm, not by the
gate (`wedge`, exit 0, measured). Diff reading is the backstop for both.
Rounds used / remaining: 2 / 3.
Next action: replace `BASE="${BASE:?}"` with a default naming the base revision, then a
short round 3 that re-runs the block with no environment and re-scores dimension 4. Do not
spend round 3 hardening the discrimination step.

## Round 3 — 2026-09-19

Presented revision: `specs/spec01.md` third revision (analyst-3: `BASE` default pinned, N4
reworded), against `cartridge.ctg` at `d1692932449c89106bb1928b717146ee8b0083a8`. The only
dirty entry in the live checkout is `?? src/asp/` (pre-existing, another session's, outside
the footprint). HEAD has **not** moved past the pinned base:
`git -C cartridge.ctg merge-base --is-ancestor d169293… HEAD` exit 0, and HEAD is that sha.

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-cartridge-call-can-be-cancelled/prd.md` — `2e8865756e64e41731a5001ac5782902e9ccdbf76ee1cff118945afc9626fd05` (body unchanged since round 1; digest differs by frontmatter claim/state only) |
| Specs | `specs/spec01.md` — `65dd1d03b44e947b6a4bc88b12301d67a3be4121a047ce9bc6a1f1e806a5b133` |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts` `177200f02a8c…` (`verify()` at `:41-51`: `['sh','-eu','-c',block]`, `{cwd, signal, timeout: 120_000}`, no env), `cartridge.ctg@d169293` `src/transport/{cartridge.rs,rpc.rs,tests/cartridge.rs}` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged from round 2. −1: the permit-held window between a cancel arriving and the listener's next await is stated, not measured. |
| Ownership and reuse | 20 | N4 closed: the spec now says `src/node/mod.rs` is "not needed **by this spec**" and that `feet()`'s union keeps it reserved. Nothing else outstanding. (Cosmetic: the heading still reads `spec02` inside `spec01.md`.) |
| Dependencies and implementable slices | 19 | Unchanged; the reference used this round is a third blind implementation (analyst-3's), 163 passed / 0 failed. −1: N5 below. |
| Observable acceptance and baseline evidence | 18 | **B4 closed by measurement.** Extracted with `verificationBlocks()`'s own regex (one block), run under `env -i PATH HOME sh -eu -c`: base rejected, both pass simulations green, all well under 120 s. The named tests are confirmed `ok` from the suite log; the discrimination step behaved as written (nothing-applied: build + FAILED ×2; rpc-only: build + FAILED ×2; cartridge-only: E0599, no verdict line ×2, which the step correctly treats as "not passed"). −2: the recorded `const2` ceiling (two mutated constants defeat step 3), per `review-plan.md` step 4 not blocking, diff reading is the backstop. |
| Failure, recovery and compatibility | 15 | Unchanged from round 2: the "listener never on a worker" invariant stays review-held (`wedge` ceiling, accepted); cancel is a notification, so old peers interoperate. |
| Reviewer total | **91** / 100 | ≥ 90, no blocking finding. |

### Runs (my own clones, no environment)

Three `git clone --local` copies of live `cartridge.ctg` under
`scratchpad/reviewer-cancel-3/`. The reference change is analyst-3's commit `65a73c3`
applied as a patch; the three test bodies in it match the spec's `## The three tests`
verbatim (whitespace-insensitive check). Each clone used the block's own default
`CARGO_TARGET_DIR` (`$PWD/target/cancel-verify`, cold per clone, `kache` on `PATH`).

| tree | state | block exit | wall | observed |
| --- | --- | ---: | ---: | --- |
| base | HEAD `d169293`, tests only, uncommitted | **1** | 45 s | step 1: `161 passed; 2 failed` — the two cancellation tests |
| pass 1 sim | HEAD `d169293`, reference change uncommitted (collect's state at `verify()`) | **0** | 55 s | suite `163 passed; 0 failed` in 34.1 s; step 3 as tabled above |
| pass 2 sim | reference committed (`2ebe195`), HEAD a descendant of `d169293` (`merge-base --is-ancestor` exit 0) | **0** | 58 s | suite `163 passed; 0 failed` in 33.6 s |

`target/` is git-ignored, so no run dirtied a clone beyond the applied change, and nothing
was written inside the footprint.

### Diff reading (the named backstop), on the reference

The `event` arm keeps `tokio::task::spawn_blocking(move || runtime.block_on(...))` and puts
the `select!` inside `block_on`; nothing is aborted and no lock is added. `Waiting::drop`
notifies only when `pending.remove` returned `Some`. The cancels map entry is removed after
`handle` returns and before the permit drops. Holds.

### New findings (non-blocking)

**N5 — the pinned `BASE` fails closed if HEAD drifts first.** Step 3 plants the *current*
`cartridge.rs`/`rpc.rs`/test file onto `d169293`. If another PRD lands transport or
test-helper changes on `cartridge.ctg` before this one collects, the nothing-applied planting
can stop building and the block exits 1 with "does not discriminate" — a false red, never a
false green. HEAD has not moved today, so the block works as pinned. Re-pin `BASE` (and the
spec's "Base revision") if HEAD moves through `src/transport/` before implementation.

**N6 — the reference distinguishes the cancel by string.** analyst-3's reference matches
`Err(error) if error == "cancelled"`, so a listener that itself returns `Err("cancelled")`
would skip the `error` publish. The spec does not require that shape; the implementer should
tell the token's outcome apart by construction (e.g. a distinct `select!` branch result), not
by the listener's message.

**Time margin (restated, not new):** 55–58 s against 120 s, with every planting a
`kache` hit. A genuine cache miss has much less room; the spec already says so.

Findings and concrete revisions: B4 closed (measured, no environment, both passes); N4 closed;
N5, N6 new and non-blocking.
Disposition: keep — proceed to implementation.
Validation: cwd `/private/tmp/claude-501/-Users-feb-dev-cartridge-cartridge-ctg/3f0d518f-742b-4556-9a24-6c5fa6dd7524/scratchpad/reviewer-cancel-3`;
block extracted with the `verificationBlocks()` regex; `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block>"`
from each clone root; exits base **1** (45 s), pass-1 sim **0** (55 s), pass-2 sim **0** (58 s).
`git -C cartridge.ctg merge-base --is-ancestor d1692932449c89106bb1928b717146ee8b0083a8 HEAD` exit 0;
live HEAD `d169293` and `status --porcelain` (`?? src/asp/`) identical before and after; no
worktree created; one `cartridge --dir` daemon before and after, untouched.
Reviewer identity: reviewer-cancel-3 (independent review sub-agent, Opus 5), round 3.
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **PASS** (91/100).
Unresolved blocking findings: none.
Recorded ceilings (unchanged, not blocking): `const2` defeats the discrimination step; the
`wedge` shape is review-held. Diff reading is the backstop for both.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation; re-pin `BASE` first if `cartridge.ctg` HEAD has moved
through `src/transport/` by then.
