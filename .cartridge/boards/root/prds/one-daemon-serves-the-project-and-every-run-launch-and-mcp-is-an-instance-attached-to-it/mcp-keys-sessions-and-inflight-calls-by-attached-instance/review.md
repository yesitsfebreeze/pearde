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
