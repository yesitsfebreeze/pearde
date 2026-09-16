# @root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/mcp-keys-sessions-and-inflight-calls-by-attached-instance review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/mcp-keys-sessions-and-inflight-calls-by-attached-instance`,
`prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/mcp-keys-sessions-and-inflight-calls-by-attached-instance/prd.md`.
Scope: executable leaf — the one mcp node keys each attached stdio client's
session, in-flight calls and restored tools by an instance id the bridge mints.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: superproject `fb44521` (dirty, see below); mcp.ctg `54e309c`
(= `main`), cartridge.ctg `906b39a` (= `main`). Prototype `attempt-1.patch`
(6 files, +403/-88) applied to scratch worktrees of both submodules.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../mcp-keys-sessions-and-inflight-calls-by-attached-instance/prd.md` SHA-256 `79fb6162636e60721f27a1f823fcb33d1f06c8a6a5f43020a87c476abfb3e449` |
| Specs | `specs/spec01.md` SHA-256 `e4418eafb4669a3fa9e274ae88fd71d00c4dcd17c50084629e0076bde2b66495` |
| Parent rollup | `.../one-daemon-.../prd.md` SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` |
| Prototype | `.state/loop/.../attempt-1.patch` SHA-256 `28ddd0f96795f818e6d16a7400ba654c61c9f1e627130602d9ef243112c002af` |
| Analyst report | `.state/loop/.../analyst-1.md` SHA-256 `1715b939aa4eb7da7110688599a8a05c8e23058ec4767ea9ab654755d564607e` |
| Material dependency | `an-instance-attaches-to-the-daemon-and-never-composes-silently` state `done`, commit `f364f46` |
| Material contract | `prd.ctg/src/lifecycle.ts` `claim`/`collect` (lane creation and the two verify passes) |

### The audit premise: VERIFIED, and it holds

Read at the base, not taken on trust:

- `mcp.ctg/src/service.rs:100-113` — `pub struct Service` holds `session:
  tokio::sync::OnceCell<String>` (`:105`), `sequence: AtomicU64` (`:106`),
  `inflight: Mutex<BTreeMap<String,(String,Value)>>` (`:109`) and `restored:
  Mutex<BTreeSet<String>>` (`:112`), all initialised once per node at `:175-178`.
  The `restored` doc comment states it outright: "One set per host process,
  shared by every attached client, never cleared until restart."
- `session()` (`:396-411`) `get_or_try_init`s one `sessions create` and hands
  every later caller the same id. `invoke` (`:552-562`) keys `inflight` by
  `id.to_string()` alone; `notified` (`:228-239`) looks that id up in the one
  map. Two clients that both count from 1 collide on `"1"`.
- No instance identity exists above it. `Backend::message`
  (`cartridge.ctg/src/cli/host.rs:302-317`, within the spec's cited `283-317`)
  sends `json!({ "op": "message", "line": line })` and nothing else;
  `src/host/socket.rs:437-441` passes `params["data"]` through verbatim; the
  only caller notion is the `Caller::{Host,Cartridge}` grant check
  (`socket.rs:424-430`). `grep -rni instance cartridge.ctg/src` returns only
  Windows named-pipe instances (`transport/typed.rs`). The bridge really is the
  only possible producer of the key.

Reproduced live, twice, with two real `cartridge mcp` children on one daemon in
a scratch `CARTRIDGE_HOME`:

- node-wide module + patched binary → `expect(two).not.toBe(one)` fails,
  `Expected: not "session-1"` (exit 1).
- unpatched live-base binary (`906b39a`) + patched module → same failure,
  both clients on `session-1` (exit 1). This is the analyst's command 9,
  independently reproduced, and it is also the compatibility proof the spec
  claims for an old binary against a new module.

Unlike the agent sibling, the premise does not dissolve. The plan is aimed at a
real defect.

### Non-vacuity: VERIFIED

Patching `Service::instance()` to ignore its id (node-wide again) and rerunning
verify block 1: `test result: FAILED. 18 passed; 2 failed`, and the two
failures are exactly `tests::two_instances_keep_separate_sessions_and_in_flight_calls`
and `tests::a_restored_tool_stays_with_the_instance_that_restored_it`. The
composed block fails in the same state. Reverted; 20 pass again.

The pre-existing reds are also as claimed:
`bun test refresh.test.ts` with fully unpatched artifacts (mcp `54e309c`,
cartridge `906b39a`, both built from clean worktrees) fails after 23.5 s at its
`until(…)`, `Live catalog did not settle: starting the host for .cartridge` —
pre-existing, not caused here. `cargo test --lib` without the skip fails only
`initialized_live_client_{inspects_real_policy…,observes_catalog_replacements}`,
with `error: no base binary: build cartridge.ctg or set CARTRIDGE_BIN` — an
artifact problem, exactly as recorded.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Real, verified defect (above); one observable outcome; PRD is 3 acceptance boxes and well inside the length target. −2: the PRD body's opening still cites `mcp.ctg/src/service.rs:88-92`; the fields are at `100-113` at the base (the Planning note has it right, the body does not). −2: **F3** below — "What changes" bullet 2 promises behaviour the spec deliberately omits. |
| Ownership and reuse | 16 | Cross-submodule footprint is correctly judged one slice, not a SPLIT (see verdict below); follows the done sibling's superproject pattern; `instances.test.ts` is built from `approval.test.ts`'s existing fixture; the code change is minimal and idiomatic (`Arc<Instance>`, `#[derive(Default)]`, no lock held across an await, no new abstraction). −2: **F4** — `cartridge.ctg/src/cli/host.rs` is dirty *right now* with unrelated work, and the spec carries no pre-collection precondition. −2: the directory entries make the receipt commit whatever each submodule's HEAD is; unavoidable for a gitlink, but unstated in the spec. |
| Dependencies and implementable slices | 9 | `needs` on the done host-attach sibling is right; `git apply --check -p2` exits 0 against both current live HEADs, so the patch survives cartridge.ctg's move to `906b39a`; steps 1–7 match the prototype exactly. −9: **F1** — the spec's execution model for its own Verify blocks is provably wrong; in the lane pass every block fails. −2: the refresh red has a named open owner, `@mcp/the-mcp-live-catalog-tests-settle-at-base` (state `open`, prio 50, acceptance "`just test mcp` exits 0 on two consecutive runs"), which the Remaining risk speculates about ("if it is someone's open PRD") instead of citing. |
| Observable acceptance and baseline evidence | 15 | Strong proof design: the unit test holds two `tools/call`s genuinely concurrent under the *same* JSON-RPC id 1 and asserts the cancel lands on exactly one context and never the other; the composed test drives two real bridges on one daemon; non-vacuity reproduced exactly (18/2); premise reproduced live. −4: **F2** — verify block 4's third assertion is both factually false against the intended implementation and inert under `sh -e`. −1: acceptance box 3 ("exactly one mcp node") is only partly observable here, which the spec says honestly but still leaves as an unproven box at collect. |
| Failure, recovery and compatibility | 14 | `instance` is optional in the schema (`required: ["op"]` only, verified), so `{op:"ready"}` and any other sender stay valid; the old-binary/new-module pairing fails loudly (reproduced); `CARGO_TARGET_DIR` is redirected outside both repos, so no live cartridge is hot-restarted — the correct lesson from `a-verify-build-never-restarts-a-live-cartridge`; the composed fixture is fully isolated (`mkdtemp` root, `CARTRIDGE_HOME=root`, `--dir profile`, `finally` closes both children, runs `stop` and removes the root), so pass 2 in the live checkout is safe. −3: the `instances` map is never pruned and the new `Instance` doc comment ("never cleared while the instance is attached") is misleading — the instance is never *detached*, so it is never cleared at all. −2: `sequence` staying node-wide means one instance's `run`/`call` ids advance with the other's traffic, so a client can infer another client's call volume from gaps; acceptable, but unnamed. −1: no spec-level guard on the dirty-submodule precondition. |
| **Reviewer total** | **70 / 100** | FAIL (threshold 90). Three blocking findings. |

### Findings

**F1 (BLOCKING) — the lane pass cannot run a single Verify block, and the spec
asserts that it can.**

`prd claim` on a `specced` PRD creates the lane with a plain
`git worktree add -b <branch> <dir> HEAD` on `repo`
(`prd.ctg/src/lifecycle.ts:225`), and `collect` runs pass 1 in that lane when it
exists (`:125`, `:139`). `repo` here is the **superproject**, and a superproject
worktree does not populate submodules — there is no `submodule.recurse` set
(`git config --get submodule.recurse` exits 1). Observed in a worktree of
`/Users/feb/dev/cartridge` at `fb44521`: `mcp.ctg`, `cartridge.ctg` and
`policy.ctg` are all **empty directories**. Running the spec's literal blocks
there:

- block 1 → exit **101**, `error: manifest path \`mcp.ctg/Cargo.toml\` does not exist`
- block 4 → exit **2**, `grep: mcp.ctg/src/service.rs: No such file or directory`

Blocks 2 and 3 fail identically for the same reason. So a collection taken
through `specced → claim → collect` aborts at pass 1 before it reaches anything.

The spec is not merely silent on this; its Remaining risk states the opposite:
"The two cargo blocks build both crates cold into the shared target dir **on the
lane pass**… the artifacts still survive for the integrated pass". That cannot
happen. The analyst's own commands 13–16 were run in `$S/root` with `mcp.ctg`
and `cartridge.ctg` **symlinked** — a tree shape the lane does not have — so the
lane pass was never exercised.

The done sibling `an-instance-attaches-…` did not hit this: its `collection.md`
records each of its six blocks exactly once, so verify ran once, meaning it
collected with **no lane** (state `specced` is an accepted collect state,
`lifecycle.ts:113`). That is the path this PRD needs too.

Recommendation: state it in the spec, above the Verify blocks — this PRD is
collected from `specced` with no lane, so the blocks run once, in `repo`; do not
`claim` it into a lane (or remove the lane before collecting). Alternatively add
a first block that populates the submodules (`git submodule update --init
mcp.ctg cartridge.ctg policy.ctg`), but that writes inside the footprint in pass
1 and is the worse answer. Either way the Remaining-risk paragraph about "the
lane pass" must be corrected.

**F2 (BLOCKING) — verify block 4's "no node-wide client state left behind"
assertion is false and cannot fail.**

The line is

```sh
! grep -n 'self\.session\b\|self\.inflight\|self\.restored' mcp.ctg/src/service.rs
```

Against the intended implementation it **matches**: `self.session(instance)`
survives at `service.rs:484` and `:541` (the method is kept, it just takes an
instance now). Run in my patched tree, the block printed both lines — and still
exited **0**, because POSIX `set -e` is explicitly ignored for a command
prefixed by the `!` reserved word. Proven directly:

```
$ sh -eu -c '! true; echo "reached line 2"; ! false; echo "reached line 4"'
reached line 2
reached line 4
$ echo $?  → 0
```

So the assertion contributes nothing: reintroducing `self.inflight` node-wide
would pass this block. (Only the *last* `!` line gates, because its status
becomes the script's.) The analyst recorded this block as "exit 0" without
noticing that its third line had failed and been swallowed.

Recommendation: make each negative check its own gating statement, e.g.
`if grep -q … ; then exit 1; fi`, or `grep -c … | grep -qx 0`, and fix the
pattern so it means what it says — `! grep -n 'self\.inflight\|self\.restored\|self\.session\.' …`
(the node-wide field accesses), not every mention of `self.session`.

**F3 (BLOCKING) — the PRD promises disconnect behaviour the spec deliberately
does not build.**

`prd.md` "What changes" bullet 2: "Session lifecycles: an instance disconnecting
drops only its own session and cancels only its own in-flight calls." The spec's
"Deliberately **not** in this spec" says there is no `closed` event, and the
prototype has none: on disconnect nothing is dropped (the `Instance` stays in
the map forever) and nothing is cancelled (the tool call runs to completion).
The acceptance box — "one closing does not affect the other's session or calls"
— is satisfied; the PRD bullet is not. A reader of the collected PRD would
believe disconnect-cancellation shipped.

Recommendation: edit that bullet in place to match what is built, e.g.
"Session lifecycles: one instance's session and in-flight calls are its own, so
a client closing never touches another's. A closing client is not itself
noticed: its entry stays until the daemon stops, and its running call is not
cancelled." Note this is a `prd.md` **body** edit only — do not touch the
frontmatter.

**F4 (non-blocking, but a hard precondition) — `cartridge.ctg` is dirty in the
footprint right now.**

`git -C cartridge.ctg status --porcelain` at review time:

```
 M .cartridge/tests/unit/src/trust/tests.rs
 M src/cli/host.rs
 M src/trust/mod.rs
```

`src/cli/host.rs` is inside this PRD's footprint and is the file spec step 1
edits; the live change is an unrelated `--yolo` propagation in `spawn_daemon`
(≈`:116`), which does not collide with the `283-317` hunk but would be committed
along with it by a wholesale `git add src/cli/host.rs`. The Planning note's risk
("check again before collecting") is therefore already realised. `mcp.ctg` is
clean. Both submodule HEADs are on `main` (`54e309c`, `906b39a`) — the lane
branch names in `git submodule status` are stale leftovers of collected work,
so there is no cross-PRD entanglement in the pointers themselves.

Recommendation: record the precondition in the spec (both submodules clean in
the footprint before collection, checked at collection time, not when the
footprint was widened), and have the coordinator confirm the `cartridge.ctg`
work has landed or been parked before implementation starts.

**F5 (non-blocking) — stale line citation.** `prd.md` body cites
`mcp.ctg/src/service.rs:88-92`; the fields are at `100-113` at the base. Inherited
from the parent's Findings. Fix in the body.

**F6 (non-blocking) — name the refresh owner.** The Remaining risk's "if it is
someone's open PRD, this one does not wait on it" can be made concrete:
`@mcp/the-mcp-live-catalog-tests-settle-at-base` (open, prio 50) owns exactly
this red and names the same two `initialized_live_*` tests.

**F7 (non-blocking) — `in_flight` spin-wait.** `tests.rs`'s `in_flight(n)` helper
loops on `tokio::task::yield_now()` with no deadline. It did not bite in the
non-vacuity run (the assertion tripped first), but a regression that never
reaches the tool would hang the suite rather than fail it. A `tokio::time::timeout`
around the wait costs one line.

### The two deliberate omissions

- **No `closed` event: acceptable.** The acceptance only needs isolation, which
  per-instance keying gives for free, and a killed bridge cannot send a notice
  anyway. The retained cost is correctly scoped — a map entry per `cartridge mcp`
  that ever attached, not a per-process `sessions` record regression, because
  before the one daemon each bridge composed its own node and created its own
  session too. Two corrections: the `Instance` doc comment ("never cleared while
  the instance is attached") should say the entry is never released at all, and
  the PRD body must stop promising the drop/cancel (F3).
- **`sequence` stays node-wide: acceptable.** The reasoning is right — one
  counter keeps `run`/`call` unique across instances, where two counters would
  collide on `call: "0"`. One consequence is unnamed: `run` is `mcp-{n/1024}` and
  `call` is `n`, both node-wide, so one client's ids advance with the other's
  traffic and gaps reveal the other's call volume. Small, and the fix (put the
  instance in the run id) can wait; worth one sentence in the spec.

### The cross-submodule footprint

**Verdict: one PRD, not a SPLIT. The coordinator's move is right.** The bridge's
`instance` field has no consumer without the node change, and the node's keying
is unobservable without the bridge — verified, not assumed: with the unpatched
binary and the patched module the composed test fails on `session-1`, i.e. the
node half alone delivers nothing. Splitting would create two PRDs neither of
which owns an observable outcome, which is precisely what the refinement rule
forbids. Retargeting `repo` to the superproject follows the done sibling
`an-instance-attaches-to-the-daemon-and-never-composes-silently` (`f364f46`,
same shape).

**The directory entries are required, and the risk the Planning note names is
real.** `collect` scopes its sweep with `git status --porcelain -- <footprint>`
run in the superproject (`lifecycle.ts:145-146`); a submodule appears there as
one entry, `mcp.ctg`, and `git add -- mcp.ctg` stages the **gitlink at that
submodule's current HEAD**. So the paths cannot be narrowed to files — a gitlink
can only be staged by the submodule's own path — and whatever another session
has committed inside either submodule before collection rides in on this
receipt. F4 shows that is not hypothetical today. The mitigation is procedural,
and belongs in the spec: check both submodules clean in the footprint
immediately before collecting, and record each submodule's HEAD in the
collection.

### Validation

All commands run from scratch worktrees under the session scratchpad, with
`CARGO_TARGET_DIR` redirected outside every repo. The live project daemon was
never started, stopped, replaced or reloaded; nothing was written to the live
submodule checkouts; no `prd` state operation was run.

Setup: `git worktree add --detach $S/mcp 54e309c` (in `mcp.ctg`) and
`git worktree add --detach $S/cartridge 906b39a` (in `cartridge.ctg`), both
clean; `$S/root/{mcp.ctg,cartridge.ctg,policy.ctg}` symlinked so the blocks run
repo-root-relative.

| # | command (cwd) | exit |
| --- | --- | ---: |
| 1 | `git -C $S/mcp apply --check -p2 --exclude='src/cli/*' attempt-1.patch` | 0 |
| 2 | `git -C $S/cartridge apply --check -p2 --include='src/cli/host.rs' attempt-1.patch` — patch still applies at the moved HEAD `906b39a` | 0 |
| 3 | `git -C $S/mcp apply -p2 --exclude='src/cli/*' attempt-1.patch` | 0 |
| 4 | `git -C $S/cartridge apply -p2 --include='src/cli/host.rs' attempt-1.patch` | 0 |
| 5 | verify block 1, `sh -eu -c`, cwd `$S/root`, cold target dir — 20 passed, 0 failed, 2 filtered; **7.1 s** | 0 |
| 6 | verify block 2, `sh -eu -c`, cwd `$S/root` — 198 crates checked cold; **10.9 s** | 0 |
| 7 | verify block 3, `sh -eu -c`, cwd `$S/root` — builds both crates, `1 pass 0 fail`, 9 expects; **7.5 s** | 0 |
| 8 | verify block 4, `sh -eu -c`, cwd `$S/root` — **exits 0 while printing `service.rs:484` and `:541` matches (F2)** | 0 |
| 9 | verify block 3 repeated ×3 with a fresh `mkdtemp` `CARTRIDGE_HOME` each time — 1 pass each; no flake seen | 0,0,0 |
| 10 | verify block 1 in a **lane-shaped** superproject worktree (`git worktree add --detach $S/lanetest HEAD`) — `manifest path mcp.ctg/Cargo.toml does not exist` (**F1**) | 101 |
| 11 | verify block 4 in the same lane-shaped worktree — `grep: mcp.ctg/src/service.rs: No such file or directory` (**F1**) | 2 |
| 12 | non-vacuity: `Service::instance()` keyed on `String::new()`, verify block 1 — `18 passed; 2 failed`, exactly the two new tests | 101 |
| 13 | non-vacuity: same state, verify block 3 — `expect(two).not.toBe(one)`, `Expected: not "session-1"` | 1 |
| 14 | `cargo test --manifest-path mcp.ctg/Cargo.toml --lib` (no skip) — only the two `initialized_live_*` fail, `error: no base binary: build cartridge.ctg or set CARTRIDGE_BIN` | 101 |
| 15 | `bun test refresh.test.ts`, mcp `54e309c` + cartridge `906b39a`, **both unpatched**, built from clean worktrees into `$S/t-base` — `Live catalog did not settle` after 23.5 s; pre-existing at the base | 1 |
| 16 | compatibility: unpatched `906b39a` binary + patched module, `bun test instances.test.ts` — both clients on `session-1`; the audit premise observed live | 1 |
| 17 | `sh -eu -c '! true; echo reached; ! false; echo reached'` — proof that `set -e` ignores `!` (**F2**) | 0 |
| 18 | `git config --get submodule.recurse` — unset, so a superproject worktree never populates submodules (**F1**) | 1 |

Timing caveat: this machine has `rustc-wrapper = "kache"` in `~/.cargo/config.toml`,
so the cold-build timings above are cache-assisted. They do **not** refute the
spec's own 120 s-per-block risk on a cold cache; they only show the blocks are
comfortably inside the limit here.

Disposition: **revise** (keep the scope, the footprint and the design; fix the
Verify contract and the PRD body).
Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL — 70/100**.
Unresolved blocking findings: F1 (lane pass cannot run any Verify block, and the
spec asserts it can), F2 (verify block 4's third assertion is false and inert),
F3 (PRD "What changes" promises disconnect drop/cancel the spec omits).
Rounds used / remaining: 1 / 4.
Next action: one bounded revision — correct the spec's Verify execution model
and its Remaining risk (F1), rewrite verify block 4's negative assertions so
they gate and so they name the node-wide accesses rather than every
`self.session` (F2), edit the PRD "What changes" bullet 2 in place (F3), and
fold in F4–F7. Then present for round 2. The audit premise, the design, the
footprint decision and the test design all survive this round unchanged.

## Round 2 — 2026-09-16

Presented revision: superproject `65a1810` (dirty, see below); mcp.ctg `345871e`
(= `main`), cartridge.ctg `04aae7f` (= `main`) — both unmoved since the revision
was written. Prototype `attempt-2.patch` (6 files), the round-1 `attempt-1.patch`
rebased onto those two heads.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../mcp-keys-sessions-and-inflight-calls-by-attached-instance/prd.md` SHA-256 `e551dff403b7e849074c329fcd5b772a86722a21f1f7553d9b11d784afeaa38d` |
| Specs | `specs/spec01.md` SHA-256 `39b594d4c6847d0ae2cdf476ef577b5c83b25f4f1f8eb5dd4b544f5c725d5983` |
| Parent rollup | `.../one-daemon-.../prd.md` SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` (unchanged from round 1) |
| Prototype | `.state/loop/.../attempt-2.patch` SHA-256 `6c41ef56db69af939e09ed121cf3651a167fb366aff1550f1b917bb1cdb4f997` |
| Revision report | `.state/loop/.../analyst-2.md` SHA-256 `6934e74c4e179c0fb6408f530924b276ac3dcc555cad846cb7a3c4e6a133c20c` |
| Material dependency | `an-instance-attaches-to-the-daemon-and-never-composes-silently` state `done` (re-read) |
| Material contract | `prd.ctg/src/lifecycle.ts` `:112`, `:125`, `:137`, `:145`, `:163-167`, `:225`, `:236`; `prd.ctg/src/process.ts:126` |

The audit premise, the cross-submodule footprint verdict and the design all
passed round 1 and were not re-derived. Everything below was re-measured, not
taken from `analyst-2.md`.

### F1 — CLOSED, and the engine really does behave as the spec now says

Read at the source, not from the report:

- `lifecycle.ts:112` — `['claimed', 'specced'].includes(prd.state)`; `specced`
  is an accepted collect state.
- `:125` — `const tree = fs.existsSync(work.directory) ? work.directory : code`.
- `:137` — `let evidence = await verify(prd, tree, signal)`. That is the only
  unconditional pass.
- `:163-167` — the second pass is inside `if (tree !== code && candidate !== initialHead)`,
  i.e. only after a lane has been fast-forwarded into `repo`. With no lane,
  `tree === code` and there is exactly one pass, in `repo`.
- `:225` — `claim` on a `specced` PRD runs `git worktree add -b <branch> <dir> HEAD`
  on `repo`, plain, with no `--recurse-submodules`.

Measured at the **current** superproject HEAD, not round 1's `fb44521`:
`git worktree add --detach $S/lanetest HEAD` (`65a1810`) leaves `mcp.ctg` and
`cartridge.ctg` as empty directories (`ls -A` → 0 entries each);
`git config --get submodule.recurse` exits 1. All four blocks, extracted
verbatim from the spec's `## Verify and Proof` section by the same rule
`verificationBlocks` uses, run there under `sh -eu -c`:

| block in the lane-shaped tree | exit | first line |
| --- | ---: | --- |
| 1 | **101** | `error: manifest path \`mcp.ctg/Cargo.toml\` does not exist` |
| 2 | **1** | `\`cargo metadata\` exited with an error: … does not exist` |
| 3 | **101** | `error: manifest path \`cartridge.ctg/Cargo.toml\` does not exist` |
| 4 | **1** | (fails on its first `test -f`, silently) |

The done sibling's `collection.md` carries **6** `exit 0` lines for the **6**
`sh` blocks in its `specs/spec01.md` — one per block, not two. It collected with
no lane, exactly as this spec proposes to.

### F2 — CLOSED, re-measured against trees that must fail

Four disposable trees beside the patched one: `g-base` (both submodules
unpatched at the bases), `g-inflight` (patched plus a node-wide
`self.inflight.lock()`), `g-session` (patched plus a node-wide `self.session.get()`),
`g-inject` (patched plus `std::process::Command::new` in `src/base.rs`).

| guard | failing tree | exit |
| --- | --- | ---: |
| `test -f mcp.ctg/src/service.rs` | lane-shaped | 1 |
| `test -f mcp.ctg/src/lib.rs` | lane-shaped | 1 |
| `test -f cartridge.ctg/src/cli/host.rs` | lane-shaped | 1 |
| `test -d mcp.ctg/src` | lane-shaped | 1 |
| `grep -q 'instances: Mutex<BTreeMap<String, Arc<Instance>>>' …` | `g-base` | 1 |
| `grep -q '"instance": self.instance' …` | `g-base` | 1 |
| `if grep -n 'self\.inflight\|self\.restored' …` | `g-base` | 1 |
| " | `g-inflight` | 1 |
| " | patched | 0 |
| `if grep -n 'self\.session' … \| grep -v 'self\.session(' …` | `g-base` | 1 |
| " | `g-session` | 1 |
| " | patched | 0 |
| `if grep -rn 'Command::new\|std::process\|cartridge daemon' mcp.ctg/src/` | `g-inject` | 1 |
| " | patched | 0 |

Every guard fires on a tree that should fail it and is silent on the intended
implementation. The whole block, round 1's version against the revised one, same
trees, same shell:

| block 4 | patched | unpatched base | lane | `self.inflight` back | `self.session` back | process injection |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| round 1 | 0 | 1 | 2 | **0** | **0** | 1 |
| revised | 0 | 1 | 1 | **1** | **1** | 1 |

So the F2 defect is real and is now fixed: round 1's block let both node-wide
regressions through. Two corrections to `analyst-2.md`'s contrast table, neither
affecting the spec: round 1's block did catch the process injection (exit 1, not
0 — its last `!` line is the one whose status becomes the script's), and it
exited **2** in the lane, not 1, because a non-negated `grep -q` on a missing
file errors. The revised block's `test -f` makes that a clean 1.

The `self.session` guard is sound for the regression it names: the node-wide
cell is reached as `self.session.get…`, which the `grep -v 'self\.session('`
filter does not remove, while the surviving method calls `self.session(instance)`
are removed. Confirmed in both directions above.

### The base, the patch and the footprint's current state

| check | exit |
| --- | ---: |
| `git -C mcp.ctg rev-parse HEAD` → `345871e`, `cartridge.ctg` → `04aae7f` — both the spec's `Base:` | — |
| `git apply --check -p2 --exclude='src/cli/*' attempt-2.patch` on a pristine `345871e` worktree | 0 |
| `git apply --check -p2 --include='src/cli/host.rs' attempt-2.patch` on a pristine `04aae7f` worktree | 0 |
| `git apply --check -p2 --exclude='src/cli/*' attempt-1.patch` on `345871e` — the rebase was necessary | 1 (`tests.rs:751`) |
| `git apply --check …` of `attempt-2.patch` against the **live, dirty** `mcp.ctg` working tree | 0 |

`cartridge.ctg` is clean now (round 1's F4 instance has landed). `mcp.ctg` is
dirty instead, and **one of the dirty paths is inside this footprint**:
`.cartridge/tests/unit/tests.rs` (+3), plus `.cartridge/tests/integration/{approval,refresh}.test.ts`
and an untracked `.cartridge/tests/integration/policy-fixture/`. The patch still
applies over it, so this is a receipt-hygiene problem and not an apply problem —
which is exactly what the spec's Remaining risk now says. `git status
--porcelain -- mcp.ctg cartridge.ctg …` in the superproject returns the single
entry ` M mcp.ctg`, confirming the spec's reasoning that the footprint cannot be
narrowed below the submodule directory.

### The "collects with no lane" instruction — verdict

**It is a sound instruction, correctly derived, and the only sound one on
offer — but it is a constraint on the coordinator that the spec cannot
enforce, and the spec should say what to do when it is broken.**

Sound: the engine facts above are all confirmed at source, and the done sibling
collected this way. The alternative round 1 floated — a first block running
`git submodule update --init` — writes inside the footprint during the pass that
commits, which is worse.

Unenforceable: nothing in `prd` reads the paragraph. `claim` does not consult the
spec; `collect` does not check for a lane, it just prefers one when the directory
exists (`:125`).

What happens if someone claims it from `specced` anyway — derived from the
engine, with the block half measured:

1. `claim` creates `prd.ctg/.cartridge/boards/root/.lanes/<slug>` with
   `git worktree add -b lane/root-<slug> <dir> HEAD` on the superproject
   (`:225`). `submodule.recurse` is unset, so `mcp.ctg` and `cartridge.ctg` are
   empty directories there — measured at `65a1810`.
2. `collect` then sets `tree` to that lane (`:125`) and runs the only pass there
   (`:137`). Block 1 exits 101 — measured. `runProcess` returns state `failed`
   for any non-zero exit (`process.ts:126`) and `verify` throws
   `verification failed: …` (`lifecycle.ts:46`).
3. That throw happens at `:137`, **before** the footprint status sweep at `:145`
   and before any `git add` or `git commit`. So the wrong path cannot commit
   source, cannot write `collection.md` and cannot move the PRD to `done`. It
   fails loudly and destroys nothing.
4. Critically, **no block passes vacuously in a lane**: 101, 1, 101, 1 measured,
   including the guard block, which round 1's version would have reached only as
   a grep error. There is no silent-green failure mode.
5. The cost is recovery, and the spec does not state it. The lane worktree and
   its branch survive; `claim` refuses a pre-existing lane (`:224`); `release`
   from `claimed` offers only `blocked`/`failed` (`:230`); and `specced` cannot
   be republished from `claimed` (`:236`). The cheap way out is
   `git worktree remove <lane>` plus `git branch -D lane/root-<slug>`, after
   which `prd collect` runs from `claimed`, which `:112` accepts and `:125` then
   resolves to `repo`. One sentence in the spec would close this; round 1's
   recommendation contained it ("or remove the lane before collecting") and the
   revision dropped that half.

Mitigating the whole concern: this PRD is in `analyzing`, and `specced` is
reachable from `analyzing` (`:236`), so the natural next transitions are
`prd specced` then `prd collect`. Reaching a lane requires a deliberate extra
`prd claim` that the spec tells the coordinator in bold not to issue.

Net: −2 in "Dependencies and implementable slices". Not blocking — an
unenforceable instruction whose violation is loud, non-destructive and
recoverable is a plan risk, not a plan defect.

### The block-3 retry — judged

The fixture retries `initialize` while the reply carries no `result`, at most 50
times, 200 ms apart, then asserts on the reply.

- **Is the bound honest?** Yes, and exercised rather than assumed. With `mcp`
  removed from the composition so no listener can ever appear, the block fails
  on the assertion after **11.8 s** at attempt 51 (`"id":51`), exit 1, no hang.
  The error surfaced in my run was `` `mcp` is not provided `` rather than the
  analyst's `no active listener`, which is the same retry condition (a reply with
  no `result`) reached by a slightly different route; the bound is what matters
  and it held. `request` additionally carries its own 30 s per-call rejection, so
  a silent daemon is bounded too.
- **Does it mask a real race?** It masks a real one, but not one this PRD owns.
  The daemon composes the mcp node while the first bridge is already talking, so
  a cold start can answer `initialize` with an error once. A real MCP client does
  not retry `initialize`; it would see the failure. That is a defect of the
  attach path (the parent's audit / the `closed`-and-readiness territory), not of
  per-instance keying, and nothing in this slice makes it worse. The spec records
  the retry in step 6 as a fixture detail and never as a risk with an owner —
  worth one bullet. −1 in "Failure, recovery and compatibility".
- Not flaky here: block 3 ran green 4 times in a row after the change, with zero
  `no active listener` occurrences.

Related: the fixture declares `}, 240_000)`, but `verify` gives each block 120 s
(`lifecycle.ts:45`) and block 3 must also fit two cargo builds inside that. The
test's own timeout can never fire under collect; the collector's kill is the real
bound. Harmless but incoherent. −1, same dimension.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Real, verified defect (round 1, not re-derived). F3 closed: the PRD body's "What changes" bullet 2 now says session lifecycles are **not** in this slice and names the `closed` event as its own PRD, which matches what the prototype builds. F5 closed: the body cites `service.rs:100-113`, the correct lines at the base. One outcome, three boxes, well inside the length target. −1: the accepted cost — one `Instance` entry per `cartridge mcp` that ever attaches, never released, for the life of a long-lived project daemon — is deferred with no owner and no threshold ("only if … ever measured as a problem"). Honest, but unowned. |
| Ownership and reuse | 18 | Cross-submodule footprint verdict stands (round 1). The gitlink mechanism is now stated correctly and I confirmed it: `git status --porcelain -- <footprint>` in the superproject yields the single entry ` M mcp.ctg`, so the footprint genuinely cannot be narrowed to files. Prototype stays minimal and idiomatic (`Arc<Instance>`, `#[derive(Default)]`, `entry/or_default/clone`, no lock across an await, `instance` optional in the schema, fixture reused from `approval.test.ts`). −1: the F4 precondition is recorded but currently **violated** — `mcp.ctg` is dirty in `.cartridge/tests/unit/tests.rs`, a footprint file, plus two integration tests and an untracked `policy-fixture/`; all of it rides in on this receipt unless cleared first. −1: the spec's own requirement that the `Instance` doc comment say the entry is never released lives only in Remaining risk, not in Steps, and the prototype's comment still does not say it — nothing carries it into implementation. |
| Dependencies and implementable slices | 17 | F1 closed and independently re-derived: `:112`, `:125`, `:137`, `:163-167`, `:225` all read at source; lane-shaped worktree at the current HEAD gives empty submodules and 101/1/101/1; the done sibling's `collection.md` has 6 exit lines for 6 blocks. `needs` sibling re-read as `done`. `attempt-2.patch` applies at both current heads and over the live dirty tree; heads have not moved since the revision. Steps 1–7 match the prototype. −2: the no-lane landing instruction (verdict above) — sound and mitigated by loud failure, but unenforceable and missing its one-sentence recovery. −1: the base is live-moving (mcp.ctg moved once mid-review and is dirty again), so the plan carries a rebase that will likely need repeating before implementation. |
| Observable acceptance and baseline evidence | 19 | F2 closed and re-measured guard by guard (table above): 11 of 11 fire against a tree that should fail them, and the revised block catches both node-wide regressions that round 1's let through. Non-vacuity re-derived at the **rebased** base, not inherited: with `Service::instance()` keyed on `String::new()`, block 1 gives `FAILED. 19 passed; 2 failed` and the two are exactly `two_instances_keep_separate_sessions_and_in_flight_calls` and `a_restored_tool_stays_with_the_instance_that_restored_it`; block 3 fails on `Expected: not "session-1"`. Restored, all four blocks green. No block writes inside the footprint: after every run the scratch worktrees show only the five patched paths and no `target/` in either repo. −1: acceptance box 3 ("exactly one mcp node") is still delegated to two siblings rather than proven here; the spec says so honestly, but it is a box ticked on evidence from outside this collection. |
| Failure, recovery and compatibility | 17 | `CARGO_TARGET_DIR` discipline verified empirically, not just read; the fixture is fully isolated (`mkdtemp` root, `CARTRIDGE_HOME=root`, `--dir profile`, `finally` closes both children, runs `stop`, removes the root), so the one pass in the live checkout is safe. `instance` optional in the schema keeps `{op:"ready"}` and any other sender valid. Retry bound honest and exercised (11.8 s to a real failure, no hang); block 3 green ×4 with no flake. Cold `CARGO_TARGET_DIR` run of all four blocks: 5 s / 10 s / 5 s / 0 s — comfortably inside 120 s here, and the spec is right that block 2 is the slowest, though this machine's `rustc-wrapper = "kache"` means these numbers do not refute the spec's own cold-cache risk elsewhere. −1: the cold-start `initialize` race is waited out in the fixture and never named as a risk with an owner, although a real MCP client does not retry. −1: the fixture's `240_000` timeout is dead under a 120 s block that must also fit two cargo builds. −1: F7 (`in_flight()` spin-waits on `yield_now()` with no deadline) is recorded rather than fixed, so a regression that never reaches the tool still hangs the unit block until the collector kills it. |
| **Reviewer total** | **90 / 100** | PASS (threshold 90). No blocking findings. |

### Findings

All three round-1 blockers are closed, each verified independently of the
revision report:

- **F1 — closed.** The spec's "How this collects" paragraph states the engine
  facts correctly and every citation checks out. See the verdict above for the
  one residual, carried as a deduction rather than a blocker.
- **F2 — closed.** Every guard now gates and every guard fires. Re-measured.
- **F3 — closed** by the coordinator in the PRD body; the bullet now matches what
  ships. **F5 — closed** (line citation corrected). **F6 — closed**
  (`@mcp/the-mcp-live-catalog-tests-settle-at-base` named). **F4 — recorded** as a
  collection-time precondition, and currently unsatisfied. **F7 — recorded**, not
  fixed, which the spec says plainly.

New, all non-blocking:

- **F8 — state the lane recovery.** One sentence: if the PRD is claimed into a
  lane by mistake, collection fails at pass 1 without committing; remove the lane
  worktree and its branch and collect from `claimed`, which `lifecycle.ts:112`
  accepts. Round 1 recommended this half and the revision dropped it.
- **F9 — the cold-start `initialize` race deserves a Remaining-risk bullet with a
  route.** The fixture's retry is a fixture fix; a real client does not retry.
  Say that it is not this slice's defect and where it belongs.
- **F10 — the fixture's `240_000` timeout is unreachable under collect** (120 s
  per block, `lifecycle.ts:45`). Either lower it or note that the collector is
  the real bound.
- **F11 — precondition, unsatisfied right now.** `mcp.ctg` is dirty in
  `.cartridge/tests/unit/tests.rs`, inside this footprint, plus two integration
  tests and an untracked `policy-fixture/`. The patch still applies over it, so
  the risk is the receipt, not the apply. Clear or park that work before
  collecting, and record both submodule HEADs in the collection.
- **F12 — report correction, no spec impact.** `analyst-2.md`'s contrast table
  gives round-1 block 4 exit 0 for the process-injection tree and 1 for the lane;
  measured, they are 1 and 2. Round 1's block was inert for the two node-wide
  regressions only — which is still exactly the defect F2 named.

### Validation

All commands run from scratch worktrees under the session scratchpad
(`$S = …/0b0c3ecc-…/scratchpad/r2`), with `CARGO_TARGET_DIR` redirected outside
every repo (`$S/target-verify`, and `$S/target-cold` for the cold run). The live
project daemon was never started, stopped, replaced or reloaded; every
`cartridge mcp` child ran under the fixture's own `mkdtemp` `CARTRIDGE_HOME` and
`--dir profile`; nothing was written to the live submodule checkouts; no `prd`
state operation was run. The four blocks were extracted from `specs/spec01.md`
by the same rule `verificationBlocks` applies (```sh fences under
`## Verify and Proof`) and run verbatim as `sh -eu -c "$(cat blockN.sh)"`.

| # | command (cwd) | exit |
| --- | --- | ---: |
| 1 | `git -C mcp.ctg worktree add --detach $S/tree/mcp.ctg 345871e`; same for `cartridge.ctg` `04aae7f`; `ln -s` live `policy.ctg` beside them | 0 |
| 2 | `git -C $S/tree/mcp.ctg apply --check -p2 --exclude='src/cli/*' attempt-2.patch` | 0 |
| 3 | `git -C $S/tree/cartridge.ctg apply --check -p2 --include='src/cli/host.rs' attempt-2.patch` | 0 |
| 4 | `git -C $S/mcp-base apply --check -p2 --exclude='src/cli/*' attempt-1.patch` — the rebase was necessary | 1 |
| 5 | `git -C mcp.ctg apply --check -p2 --exclude='src/cli/*' attempt-2.patch` against the **live dirty** tree (read-only) | 0 |
| 6 | apply `attempt-2.patch` into both scratch worktrees | 0, 0 |
| 7 | `git -C /Users/feb/dev/cartridge worktree add --detach $S/lanetest HEAD` (`65a1810`); `ls -A mcp.ctg`, `ls -A cartridge.ctg` → 0 entries each | 0 |
| 8 | `git config --get submodule.recurse` | 1 |
| 9 | blocks 1–4, cwd `$S/lanetest` (lane-shaped) | **101, 1, 101, 1** |
| 10 | blocks 1–4, cwd `$S/tree` (patched, repo-shaped), `$S/target-verify` | 0, 0, 0, 0 |
| 11 | block 1 detail — `21 passed; 0 failed; 2 filtered out`, 6.4 s | 0 |
| 12 | block 2 detail — fmt+clippy (mcp), fmt+`check --bin cartridge` (cartridge), 10.8 s | 0 |
| 13 | block 3 detail — `1 pass, 0 fail, 9 expect()`, 4.2 s warm | 0 |
| 14 | revised block 4 vs round-1 block 4 across `tree`/`g-base`/`g-inflight`/`g-session`/`g-inject`/`lanetest` (6×2 runs) | table above |
| 15 | each of the 11 guards individually against its failing tree | 1 each |
| 16 | the three negative guards individually against the patched tree | 0 each |
| 17 | non-vacuity: `Service::instance()` keyed on `String::new()` (and `id` → `_id`, since `-D warnings` rejects the unused binding), block 1 — `FAILED. 19 passed; 2 failed`, exactly the two new tests | 101 |
| 18 | same state, block 3 — `Expected: not "session-1"` | 1 |
| 19 | `service.rs` restored; blocks 1–4 again | 0, 0, 0, 0 |
| 20 | block 3 repeated ×3 more, fresh `mkdtemp` each time, 0 `no active listener` warnings | 0, 0, 0 |
| 21 | retry bound: `instances.test.ts` copied with `{id="mcp",path="mcp"}` removed from the composition, `bun test` — fails the assertion at attempt 51 after **11.8 s**, no hang | 1 |
| 22 | footprint-write check: `git status --porcelain -uall` in both scratch worktrees after every block — only the five patched paths; no `target/` inside either repo | 0 |
| 23 | cold `CARGO_TARGET_DIR` (`$S/target-cold` removed first), blocks 1–4 — 5 s, 10 s, 5 s, 0 s | 0, 0, 0, 0 |
| 24 | `git status --porcelain=v1 -uall -- mcp.ctg cartridge.ctg …` in the superproject — single entry ` M mcp.ctg` | 0 |
| 25 | done sibling: 6 `sh` blocks in `specs/spec01.md`, 6 `exit 0` lines in `collection.md` | — |

Timing caveat, unchanged from round 1: this machine has `rustc-wrapper = "kache"`,
so even the cold-target-dir numbers in row 23 are cache-assisted. They show the
blocks are comfortably inside 120 s here; they do not refute the spec's own
cold-cache risk on a host without it.

Scratch worktrees left in place for reconciliation: `$S/tree/{mcp.ctg,cartridge.ctg}`
(the patched pair that ran the blocks), `$S/{mcp-base,mcp-patched,cartridge-base,cartridge-patched}`,
`$S/lanetest`, `$S/g-{base,inflight,session,inject}`. `git worktree prune` in each
submodule and in the superproject clears them.

Disposition: **keep** — proceed to implementation. Fold F8–F11 in as text where
convenient; none of them gates the slice.
Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS — 90/100**.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation at mcp.ctg `345871e` / cartridge.ctg
`04aae7f` with `attempt-2.patch`, rebasing it if either head moves. Before
collecting: confirm both submodules clean in the footprint (F11 — `mcp.ctg` is
not, today), take the PRD to `specced` and collect **without claiming a lane**,
and record both submodule HEADs in the collection.

## Round 3 — 2026-09-16

Presented revision: **the box-3 reword only**. Superproject `308378b`, gitlinks
`mcp.ctg 345871e` / `cartridge.ctg 04aae7f`, superproject
`git status --porcelain -- mcp.ctg cartridge.ctg` → the single entry ` M mcp.ctg`
(the peer's uncommitted work). The implementation under review by verifier-1 is
`mcp.ctg 7a72f42` / `cartridge.ctg f445f60`, not yet collected. Rounds 1 and 2
are not re-litigated; nothing below re-derives the audit premise, the
cross-submodule footprint, the engine facts or the non-vacuity probes.

| Input | Content digest |
| --- | --- |
| Plan | `prds/.../mcp-keys-.../prd.md` SHA-256 `1fc498e82c19040728c9128b7c23e853af91d6366f0d4ac83cdef3f3b8f96a95` |
| Specs | `specs/spec01.md` SHA-256 `c0a4ce3e15fc08349ce47d93f517005e7d0d3521ed2228f8abd56e935b6f1c16` |
| Parent rollup | `.../one-daemon-.../prd.md` SHA-256 `0de5a65126506dd532e62bd102f6fd02e7af371384729d45f050f69eff1b9445` (unchanged from rounds 1–2) |
| Trigger | `.state/loop/.../verifier-1.md` SHA-256 `984360bd0ce0d9d7bac04111865778c073217045e83a57ad2755d855348b5ed7` |
| Implementation report | `.state/loop/.../implementer-1.md` SHA-256 `f036ab772b26d4f77a44955651ba9042e08ffa939be37f439bca05954804b554` |
| Material dependency | `an-instance-attaches-to-the-daemon-and-never-composes-silently` state `done` (re-read); `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances` state **`open`**, prio 85 (re-read) |
| Material contracts | `cartridge.ctg/src/host/socket.rs:46-84` (`base`, `tag`, `run_dir`, `host_dir`), `src/transport/typed.rs:337-346` (`path_tag`), `src/cli/mod.rs:130,140-145` (`status`, `socket`) |

### The delta is exactly what it is claimed to be — proven, not assumed

Both records are uncommitted in `prd.ctg`, so the round-2 revision cannot be read
back directly. It can be reconstructed, and it was:

- **`prd.md`**: the version at `prd.ctg` HEAD hashes to
  `e551dff403b7e849074c329fcd5b772a86722a21f1f7553d9b11d784afeaa38d` — byte for
  byte the digest round 2 recorded for the Plan. So `git diff HEAD` *is* the
  round-2 → now delta, and it is three things: `state: "analyzing"` → `"specced"`,
  the `claim:` line dropped (both coordinator state ops), and box 3 reworded.
  Boxes 1 and 2 are untouched; all three boxes are still `- [ ]`.
- **`specs/spec01.md`**: reverting exactly three edits from the current file —
  (a) the F8 lane-recovery sentence, (b) the F9 cold-start Remaining-risk bullet,
  (c) the box-3 reword — reproduces
  `39b594d4c6847d0ae2cdf476ef577b5c83b25f4f1f8eb5dd4b544f5c725d5983`, round 2's
  recorded Specs digest, exactly. (a) and (b) are round-2 findings F8/F9, which
  round 2 asked to be folded in; (c) is this round's delta. Therefore **no other
  box, no Step, and none of the four Verify blocks changed** since the PASS.

### Block 4 re-run verbatim, in my own tree

Own worktrees, independent of the implementer's and the verifier's:
`$S/r3/mcp.ctg` @ `7a72f42`, `$S/r3/cartridge.ctg` @ `f445f60`, `policy.ctg`
symlinked beside them, `CARGO_TARGET_DIR=$S/r3-target` (outside both repos). The
four blocks were re-extracted from the current `specs/spec01.md` by the rule
`verificationBlocks` uses (```sh fences under `## Verify and Proof`) — 4 found,
block 4 byte-identical to the spec's.

| # | command | exit |
| --- | --- | ---: |
| 1 | block 4 verbatim, `sh -eu -c`, cwd `$S/r3` (at `7a72f42`/`f445f60`) | **0** |
| 2 | its last guard alone — `if grep -rn 'Command::new\|std::process\|cartridge daemon' mcp.ctg/src/; then exit 1; fi` — in a worktree at the **base** `345871e` | **0** |

**What block 4 proves:** that no file under `mcp.ctg/src/` names `Command::new`,
`std::process` or `cartridge daemon`. **What it does not prove:** anything this
PRD changed — row 2 shows the same guard is green at the unpatched base, so the
surviving half of box 3 is a standing property of mcp.ctg, tickable before a line
of this slice was written. Its scope is also narrower than the box's sentence:
`mcp.ctg/src/` excludes `build.rs`, `init.lua` and `cartridge.json`, which ship
with the cartridge. (Checked by hand: none of them spawns anything today —
`grep -rniE 'os\.execute|io\.popen|Command::new|std::process|spawn'` over the
`*.lua`/`*.json`/`*.rs` files outside `src/` and outside `.cartridge/tests/`
returns nothing — so the claim is true; only the guard is narrower than it.)

### The run-directory assertion, measured

The fixture's line is
`fs.readdirSync(path.join(composition)).filter(entry => /^\d+$/.test(entry))`
then `expect(run.length).toBeLessThanOrEqual(1)`, with
`composition = <mkdtemp root>/.cartridge` (`instances.test.ts:111-112` at
`7a72f42`).

**Zero case, constructed and run** (`$S/r3probe/runbox.test.ts`, the same two
lines against three shapes of `.cartridge`): an empty directory gives
`run.length === 0` and passes; a directory of non-numeric entries gives 0 and
passes; only **two or more** numeric entries could ever fail it. `3 pass, 0 fail`,
exit 0.

It is worse than a weak upper bound. **Numeric directories cannot appear there at
all**, by construction: `host_dir` is `run_dir(descriptor).join(pid)` and
`run_dir` is `base().join(tag(descriptor))`, where `base()` is
`$XDG_RUNTIME_DIR/cartridge` or `/tmp/cartridge-<uid>`
(`cartridge.ctg/src/host/socket.rs:46-84`) — never the project's `.cartridge`.
Observed on this machine: `/tmp/cartridge-501` holds 992 tag directories, 94 of
them with exactly one numeric pid directory and 898 with none; the live project's
own `.cartridge` has no numeric entry, matching verifier-1.

**Observed live during the composed fixture** (probe copy of `instances.test.ts`
in my scratch worktree, same env as block 3, 2 s):

```
PROBE composition entries: ["init.lua","config.lua","daemon.log"]
PROBE numeric entries under the project .cartridge: []
PROBE `cartridge socket` -> /tmp/cartridge-501/88298f9ed8ab/host.sock exit 0
PROBE via CLI: pids ["29639"] sockets ["policy.sock","sessions.sock","echo.sock","mcp.sock"]
```

So while two real bridges talk to one daemon, the assertion evaluates `0 <= 1`
and the real run directory sits elsewhere, holding exactly one pid directory with
exactly one `mcp.sock`.

**What a strengthened version takes — implemented and passed, not imagined.**
Three routes, all inside the fixture this PRD already ships, all green on
`7a72f42` in the same ~2 s run (`15 expect() calls, 1 pass, 0 fail`):

1. Two lines, no filesystem layout knowledge:
   `cartridge --dir profile status` exits 0 and prints one JSON object per node,
   each with `id` and `socket` (observed: `sessions`, `policy`, `echo`, `mcp`).
   `expect(status.filter(n => n.id === 'mcp').length).toBe(1)` is literally box
   3's sentence, asserted from the fixture.
2. Five lines: `cartridge --dir profile socket` prints
   `<run dir>/host.sock`; `path.dirname` of it, filtered to numeric entries,
   gives exactly one pid directory, and that directory contains exactly one
   `mcp.sock`. Asserted `toBe(1)` twice — both passed.
3. Twelve lines without the CLI: the tag is a 12-hex FNV-1a of the canonical
   descriptor path (`typed.rs:337-346`); reimplemented in TS it reproduced the
   observed directory name exactly (`b5fcc3fb81f1`, matching the before/after
   diff of `/tmp/cartridge-501`).

All three are **base-passing** — one node per composed cartridge is the host's
doing, not this slice's — which is fine for an acceptance box, and is exactly the
status of the grep guard that was kept.

### Answers to the four questions put to this round

1. **Honest, or narrowed until it passes?** Narrowed, and narrowed further than
   the facts require. The surviving clause is true and proven (block 4, exit 0),
   but it is base-passing and it is not the box's title. The precedent cited —
   `agent-runs`, `memory-runs-once`, `prd-journals` — does not carry over
   unchanged: those three prove their share from *unit-level* evidence and none of
   them claims the daemon-wide count is unobservable (memory names a refused
   writer lock and its exact message; prd names one `Wire`, one `Service` and a
   refused second `apply`; agent gives a reason, "so a second node can only come
   from the host"). **This PRD's box is the only one that asserts "The daemon-wide
   count is not observable from this cartridge", and that sentence is false for
   this PRD's own footprint**: `mcp.ctg/.cartridge/tests/integration/instances.test.ts`
   already runs a real daemon, and two lines of `cartridge status` inside it
   assert exactly one mcp node — measured above, green. A box whose substantive
   half is deleted with a reason that its own fixture disproves is a box narrowed
   to fit.
2. **Is naming the unlanded re-proof enough, or should this PRD carry a `needs`?**
   Naming it is right and a `needs` would be wrong. `needs` gates implementation
   order; this slice's work is done, verified and independent of the composed
   test, and blocking a finished slice on an `open` sibling stalls landing for
   nothing — the same two siblings are named without a `needs` by `memory-runs-once`
   and `prd-journals`. The sentence "which is still `open` — that re-proof has not
   landed yet" is exactly the kind of thing that belongs in the record, and the
   PRD is better for it. It is not, however, a substitute for evidence that is
   available here (finding F13).
3. **Does keeping the vacuous assertion as a "smoke check" do harm?** Yes, small
   but real, and it should not be kept as-is. The disclaimer lives in
   `specs/spec01.md`; the person who next reads `instances.test.ts` sees
   `// Exactly one daemon, and mcp starts nothing of its own.` above a line that
   cannot fail — and I measured that it cannot: it passes on an empty directory,
   on any `.cartridge` of non-numeric entries, and during a real two-bridge run.
   "Smoke check" implies it smokes something out. **Remove it or strengthen it**
   (routes 1–3 above, all cheaper than the comment explaining why it is kept);
   the disclaimed-but-live third state also guarantees drift the moment someone
   fixes the test and not the spec, or the reverse.
4. **Do the records agree, and did any other box change silently?** No other box
   changed — proven by digest reconstruction above; the Verify blocks and Steps
   are byte-identical to the PASSed revision and no box is ticked. The two records
   agree on substance, with two small asymmetries: spec box 3 drops the PRD's "is
   still `open` — that re-proof has not landed yet", keeping only "re-proven by",
   which reads as delivered; and `implementer-1.md:139-140` still offers "block
   3's fixture asserts at most one numeric run directory" as evidence, which the
   spec now says asserts nothing. The second is a historical loop report and needs
   no edit, but nothing else in the loop directory records the correction except
   verifier-1.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The delta changes no scope: boxes 1 and 2 are byte-identical to the PASSed revision (digest reconstruction above) and both are proven by execution per verifier-1. −2: after the reword, box 3 asserts only a property that already held at the base — I measured the surviving guard green in a worktree at `345871e` — so the box can be ticked without any of this slice's work and carries no user-visible outcome of it. |
| Ownership and reuse | 19 | Delegation to a named `done` sibling plus a named composed test is the established shape across four children of this parent, and the `needs` question resolves correctly against it (no `needs`; see answer 2). Sibling states re-read: `done` and `open`. −1: the daemon-wide half is handed to an `open` sibling although the evidence sits inside this PRD's own footprint — `instances.test.ts` is a file this PRD creates, and two lines in it assert the box's sentence (measured, green). |
| Dependencies and implementable slices | 19 | The reword adds no dependency and removes none; landing stays blocked only by the peer's `mcp.ctg` dirt (verifier-1 Q1, measured there, unchanged here: superproject still shows ` M mcp.ctg`). The record names the unlanded re-proof rather than hiding it. −1: box 3 would be ticked against a re-proof that does not exist yet, and nothing back-references this PRD from the composed sibling, so if that sibling is descoped or re-scoped nothing revisits this box. |
| Observable acceptance and baseline evidence | 13 | Block 4 re-run verbatim in my own tree at `7a72f42`/`f445f60`: exit 0, reproduced. The zero case was constructed and run: `0 <= 1` passes, and only ≥2 numeric entries could fail — which the host's layout makes impossible in that directory (`socket.rs:72-84`; observed live, `[]` in `.cartridge` while `/tmp/cartridge-501/<tag>/29639/mcp.sock` existed). **−4 (blocking, F13):** the box's stated reason for the narrowing — "The daemon-wide count is not observable from this cartridge" — is disproven by this PRD's own fixture; `cartridge --dir profile status` inside it returns one node object per composed cartridge and `filter(id === 'mcp').length === 1` passes today, as do the run-directory and FNV-tag routes (all three implemented and green, 2 s). **−3 (F14):** the assertion that asserts nothing stays live in the shipped fixture, under a comment that still claims it checks one daemon, with the disclaimer in a different file. |
| Failure, recovery and compatibility | 19 | The delta is text-only: no Verify block, Step or footprint moved (digest-proven), so nothing about collection, `CARGO_TARGET_DIR` discipline or the no-lane path is disturbed, and block 4 is unchanged and still green. My probes ran in my own worktrees with their own `CARGO_TARGET_DIR`; the live daemon was never touched. −1: the record and the fixture now disagree by design (a live assertion documented as proving nothing), which is a guaranteed drift point, and `implementer-1.md` still cites that assertion as evidence. |
| **Reviewer total** | **88 / 100** | FAIL (threshold 90), one blocking finding. |

### Findings

- **F13 — BLOCKING. The reason given for narrowing box 3 is false for this PRD's
  own footprint.** Evidence: `instances.test.ts` (this PRD's new file) spawns a
  real daemon; in it `cartridge --dir profile status` exits 0 and prints one node
  object per composed cartridge, so `status.filter(n => n.id === 'mcp').length`
  is assertable in two lines and equals 1 on `7a72f42` (measured); the run-dir and
  FNV-tag variants also pass. Recommendation, either one closes it:
  (a) add the two-line `status` assertion (or the five-line run-directory one),
  restore the daemon-wide clause to box 3 for the composed fixture's scope, and
  keep the delegation sentence only for the live project; or
  (b) keep the delegation and correct the reason — say the count is not observable
  *from the node's Rust code*, state plainly that the fixture could observe it and
  that proving it is deliberately left to the composed sibling. (a) is preferred:
  it costs less than the prose defending (b). Cost measured: the fixture edit plus
  a re-run of blocks 1–4 is ~15 s warm here; it does mean a new `mcp.ctg` commit,
  so the verified sha moves and needs one more verification pass.
- **F14 — non-blocking, but do not leave it as it is. Delete or strengthen the
  dead assertion.** `expect(run.length).toBeLessThanOrEqual(1)` cannot fail in
  that directory. If F13 is closed by (a) it is replaced; if by (b) it should be
  deleted along with its comment, not disclaimed from another file.
- **F15 — non-blocking. Name what block 4 actually proves.** The guard is green at
  the base (measured, exit 0 at `345871e`) and scans only `mcp.ctg/src/`, while
  the box says "the cartridge". One clause in the spec — "a standing property,
  guarded against regression; `build.rs`, `init.lua` and `cartridge.json` are
  outside the guard's scope" — makes the box honest about its own strength.
- **F16 — non-blocking, cosmetic. Align the two records.** Spec box 3 says
  "re-proven by …" where PRD box 3 says "… which is still `open` — that re-proof
  has not landed yet". Carry the same six words into the spec.

Disposition: **revise** — one bounded edit to `instances.test.ts` and box 3 in
both records. The scope, the design, the footprint, the Verify blocks and boxes 1
and 2 all stand; nothing from rounds 1 and 2 is reopened.

Validation: all commands in my own scratch worktrees under
`$S = /private/tmp/claude-501/-Users-feb-dev-cartridge/0b0c3ecc-…/scratchpad`
(`$S/r3/mcp.ctg` @ `7a72f42`, `$S/r3/cartridge.ctg` @ `f445f60`, `policy.ctg`
symlinked), `CARGO_TARGET_DIR=$S/r3-target` outside both repos. Nothing was
written to the live `mcp.ctg`, `cartridge.ctg` or superproject working trees; the
live project daemon was never started, stopped, replaced or reloaded; every
`cartridge` process ran under the fixture's own `mkdtemp` `CARTRIDGE_HOME` and
`--dir profile`; no `prd` state operation was run; no acceptance box was ticked.

| # | command (cwd) | exit |
| --- | --- | ---: |
| 1 | `git -C mcp.ctg worktree add --detach $S/r3/mcp.ctg 7a72f42`; `git -C cartridge.ctg worktree add --detach $S/r3/cartridge.ctg f445f60`; `ln -s` live `policy.ctg` | 0, 0, 0 |
| 2 | re-extract the ```sh blocks under `## Verify and Proof` from the current `specs/spec01.md` — 4 found | — |
| 3 | block 4 verbatim, `sh -eu -c`, cwd `$S/r3` | **0** |
| 4 | `git -C mcp.ctg worktree add --detach $S/r3base/mcp.ctg 345871e`; the process guard alone, cwd `$S/r3base` | 0, **0** |
| 5 | `grep -rniE 'os\.execute\|io\.popen\|Command::new\|std::process\|spawn'` over `*.lua`/`*.json`/`*.rs` outside `src/` and `.cartridge/tests/` in `mcp.ctg` — no match | 1 |
| 6 | zero-case fixture `$S/r3probe/runbox.test.ts` — `3 pass, 0 fail, 6 expect()`; empty and non-numeric `.cartridge` both give `run.length === 0` and pass | **0** |
| 7 | `ls /tmp/cartridge-501` and per-tag numeric counts — 992 tags, 94 with exactly one pid dir, 898 with none; `XDG_RUNTIME_DIR` unset | — |
| 8 | `cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge` (9.2 s) and `cargo build --manifest-path mcp.ctg/Cargo.toml` (5.1 s), `CARGO_TARGET_DIR=$S/r3-target` | 0, 0 |
| 9 | probe copy of `instances.test.ts` (`.cartridge/tests/integration/probe.test.ts` in my worktree only), same env as block 3 — `1 pass, 0 fail, 15 expect()`, 1.9 s; output quoted above | **0** |
| 10 | inside 9: `expect(pidDirs.length).toBe(1)`, `expect(sockets.filter(e => e === 'mcp.sock').length).toBe(1)`, CLI and FNV-tag routes — all green | — |
| 11 | digest reconstruction: `prd.ctg` HEAD `prd.md` → `e551dff…` (= round-2 Plan digest); current `spec01.md` with F8, F9 and the box-3 reword reverted → `39b594d…` (= round-2 Specs digest) | — |
| 12 | sibling states re-read: `an-instance-attaches-…` `done`; `the-composed-acceptance-test-…` `open`, prio 85 | — |

Timing caveat, unchanged from rounds 1 and 2: this machine has
`rustc-wrapper = "kache"`, so row 8's numbers are cache-assisted and refute
nothing about a cold host.

Scratch left in place: `$S/r3/{mcp.ctg,cartridge.ctg}`, `$S/r3base/mcp.ctg`,
`$S/r3-target`, `$S/r3blocks/block{1..4}.sh`, `$S/r3probe/runbox.test.ts`, and
the probe file inside `$S/r3/mcp.ctg` (never in the live tree).
`git worktree prune` in each submodule clears the worktrees.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL — 88/100**.
Unresolved blocking findings: **F13** — box 3's stated reason for delegating the
daemon-wide count ("not observable from this cartridge") is disproven by this
PRD's own composed fixture, where the count is assertable in two lines and passes
today. **Box 3 must not be ticked as written.**
Rounds used / remaining: 3 / 2.
Next action: one bounded revision — close F13 by (a) asserting one mcp node in
`instances.test.ts` and restoring the composed-scope clause to box 3, or (b)
correcting the reason and deleting the dead assertion; fold in F14–F16; re-run
blocks 1–4 against the amended `mcp.ctg` commit and present the new sha for round
4. Boxes 1 and 2, the design, the footprint and the collection plan are unchanged
and need no further review.
