# @root/one-daemon-.../sessions-runs-once-in-the-daemon-with-one-buffer-id-space review history

Plan: `@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/sessions-runs-once-in-the-daemon-with-one-buffer-id-space`,
`prd.ctg/.cartridge/boards/root/prds/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/sessions-runs-once-in-the-daemon-with-one-buffer-id-space/`.
Scope: leaf, one observable outcome — sessions is composed once in the daemon, so
one store and one buffer-id counter serve every attached instance. Prio 80,
`repo: sessions.ctg`, owner `sessions`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (this canonical ID has no predecessor).

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds without overwriting prior results. This record does not replace the
work item's implementation status.

## Round 1 — 2026-09-16

Presented revision: `sessions.ctg` at `b8961628af8f2377e4f1a02502bcda3ef6948381`
(clean, `git status --porcelain` empty), plus the unstaged planning records below.
Base binary: `cartridge.ctg` `04aae7f` (release build 14:29; `git merge-base
--is-ancestor 04aae7f HEAD` → 0, so the attach contract the spec requires is in it).

| Input | Content digest (SHA-256) |
| --- | --- |
| Plan | `prds/.../sessions-.../prd.md` `3c18631aadf6e54ac3c230c9d5ebce355956c9ee032d1581eaed55c1aaa7d7ba` |
| Specs | `prds/.../specs/spec01.md` `7cfc57a2e0e608d7e0c63c5250a440b7f72139aaa87c522d0addca594db21b69` (identical to the loop copy `.state/loop/.../spec01.md`, same digest) |
| Analyst report | `prds/.../analyst-1.md` `3a7d6527ba65fa6aeaa509c9fdaf08069905c73fd804eb67adeafaa3a7269cd7` |
| Prototype | `.state/loop/.../attempt-1.patch` `ca7d8916d7f9ebd935e0d3ff1915a316910f4e77f665093ebf9ed9dfdbefd2be` |
| Material source | `sessions.ctg/src/lib.rs` `97e0798f535d2b632295339e41df6df028bea84390a9a6b6db4a855fe3db9679`; `sessions.ctg/.cartridge/tests/integration/native.ts` `70044c5a59be5e43154011556774860129a08822dca2d872b81440c50d283955` |
| Material dependencies | `an-instance-attaches-to-the-daemon-and-never-composes-silently` (done); `mcp-keys-sessions-and-inflight-calls-by-attached-instance` (**specced, not done**); `cartridge.ctg/src/cli/mod.rs:101-115` at `04aae7f`; `mcp.ctg/src/service.rs:419-433`; `agent.ctg/src/lib.rs:273-278` |

### Re-derivation of the dissolution claim (not taken on trust)

Every line the Planning note cites was re-read at `b896162` and each claim holds:

- **Id space is the store's, not the process's.** `Store.next` is a field of
  `struct Store` (`src/lib.rs:101`); `install` seeds it from disk,
  `self.next = self.next.max(b.id + 1)` (`:344`); `execute` reserves exactly one id
  per operation under the store's write lock, before the operation runs
  (`:1061-1064`), and the transactional candidate carries that `next` (`:1088`),
  which is what `buffers open` hands out (`:868-869`).
- **One in-memory store per process, and only one process was ever possible per
  composition.** `grep -cF 'Store::load' src/lib.rs` = **1** (`:1214`, inside
  `start`); the result is installed in `static STORE: OnceLock<Arc<SharedStore>>`
  (`:1185`) and a second `start` is refused with `"sessions already started"`
  (`:1226`). `init.lua:11-12` registers exactly the two listeners onto it.
- **There is no rename op.** `grep -rn rename src/` (minus `rename_all`) returns
  only `std::fs::rename` in `Store::save` (`:394`), `mapping.rs:258`,
  `channels.rs:293`, `retention.rs:83`. `save` replaces `<session>.json`
  unconditionally; the `expected` CAS is reached only via `repair_empty` (`:465`).
  The user-facing op is `sessions update {id, name}` (`:695-700`), as the spec says.
- **No instance identity reaches this cartridge.** `cartridge call` is
  `client::ask(project, "bail", json!({"name": event, "data": …}))`
  (`cartridge.ctg/src/cli/mod.rs:108-114`) — name and data, nothing else. I also
  confirmed the negative the narrowing rests on: `grep -rn 'sessions'
  cartridge.ctg/src` returns **0 lines**.
- **Scoping is by session record.** `Buffer.session: Option<String>` (`:55`);
  the read path filters on `args["session"]` (`:594-604`) and the mutating path
  on `session` (`:846-856`).

So the "no Rust change" conclusion is correct, and the delivery being a regression
test plus static guards is the right shape for it.

### The denied worlds, reproduced independently

All of these were built in my own private scratch trees (`git archive b896162`
extracted, never a worktree of the live checkout), with
`CARGO_TARGET_DIR=$TMPDIR/sessions-one-id-space-verify` — outside every repo.

- **Two daemons over one store dir** (the world the PRD says one daemon removes):
  reproduced exactly, exit **1**. Both nodes handed out buffer id **2** for two
  different sessions, and the second daemon's copy of the first's session still
  read `"name":"alpha","buffers":[]` after the first had renamed it and opened a
  buffer in it. This is what makes the dissolution claim evidence, not argument.
- **Block 1's two denied worlds**, plus two more I invented: `STORE` as a
  per-caller `Mutex<BTreeMap<…>>`, a second `Store::load` in `start`, the
  reservation line replaced by `state.next += 1`, and a `std::process::Command`
  added to `src/` — exit **1** in all four. Block 1 on the *unpatched* base also
  exits 1 (no `instances.test.ts`), so the `test -f` guards are load-bearing too.

### The box 1 narrowing — judged hard

**Verdict: honest, and the narrowed clauses are all load-bearing.** Reasons, in
the order this board's three earlier failures happened:

1. *Is the premise false (the mcp F13 trap)?* No. The premise is "no instance
   identity reaches this cartridge" and "an unfiltered `buffers list` returns
   every buffer, as it always did". Both verified above from source
   (`cli/mod.rs:108-114`; zero `sessions` references in the base; the two list
   filters). Unlike the mcp round-3 failure, nothing here is justified by an
   unobservability claim that the PRD's own fixture disproves.
2. *Does it still assert something a regression would break (the "passed at zero"
   trap)?* Yes — measured, not argued. I built a tree whose `buffers list` ignores
   the `session` key (both `:597` and `:852`) and ran block 2 verbatim: exit **1**,
   `toEqual` failed with `Received +3` — i.e. each filtered listing is genuinely
   3 ids, not 0, and it fails the moment the filter stops filtering. I also built a
   tree where the shared counter never advances: exit **1**, `new Set(ids).size`
   was 1 against an expected 6. Neither assertion is vacuous inside one node.
3. *Was it shaped to fit what the code happens to do?* Partly, and it says so out
   loud, which is the difference that matters. The unfiltered-listing clause
   records current behaviour rather than constraining it, and the spec names the
   residual outcome ("instances isolated without asking needs caller identity in
   the host protocol; that is a new PRD"). The clause that carries weight is the
   filtered one, and it is the one that fails when the code changes. That is the
   honest form of a narrowing.

**Box 3 checked too.** The spec does not claim unobservability; the fixture runs a
real `cartridge daemon` (`native.ts:67-70`), settles on a real `cartridge status`
(`:81-95`) and sends every request as its own `cartridge call` child (`:123-136`).
I proved the assertion cannot pass with the node absent: with `start` made to fail
unconditionally, block 2 exits **1** (`sessions failed: reviewer: node refuses to
start`). One caveat recorded below as F3: the fixture's own `active()` gate already
throws in that world, so the distinct content of the final assertion is
`nodes.length === 1`, and a second *slot* was not constructed here (delegated to
the mcp sibling's measurement, which the spec cites).

### Block hygiene and pass-2 safety

- Neither block uses a `!`-prefixed command; block 1's one negation is
  `if grep -rn …; then exit 1; fi`, and every path is `test -f` guarded before a
  grep (grep exits 2 on a missing file). Confirmed by reading and by the
  unpatched-base run exiting 1 rather than 0.
- Block 2 pins `CARGO_TARGET_DIR` to `${TMPDIR:-/tmp}/sessions-one-id-space-verify`
  before any cargo command — outside every repo, so pass 2 in the live submodule
  cannot hot-restart a live cartridge. (The template suggests `$PWD/target/<slug>-verify`;
  outside the repo is stricter, not weaker.)
- No `cd`, no absolute checkout path as cwd; the only absolute path is
  `CARTRIDGE_BIN` with an env default, which the template explicitly sanctions
  because `../cartridge.ctg` does not resolve from a lane.
- **Nothing is written inside the footprint.** Checksum of the whole patched tree
  (excluding `target/`) before and after a full block 1 + block 2 run:
  `92f6a0de281cf592a14d9fdcc4560f653dc2c52d` both times, and no `target/` directory
  was created in the repo at all.
- The fixture is self-contained: `CARTRIDGE_HOME` is its own `mkdtemp`, the project
  is its own temp dir, and the socket observed in the denied-world log was
  `/tmp/cartridge-501/9b6d753f8f19/host.sock` — a per-temp-project tag, not the
  live project's. `pgrep -fl "cartridge daemon"` returned nothing before, during
  and after this review: no live daemon was started, stopped, replaced or reloaded.

### Footprint

`src/lib.rs`, `.cartridge/tests/integration/native.ts`,
`.cartridge/tests/integration/instances.test.ts` — the PRD frontmatter and the
spec frontmatter agree, and `attempt-1.patch` touches exactly the latter two and
nothing else (`git apply --check` 0, `git apply` 0 at `b896162`). It covers
everything the spec touches. `src/lib.rs` is unmodified; keeping it is defensible
(it is the file the guards read and the cartridge's own source) but it is not
required by `collect`, and it widens the receipt sweep — see F2.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Critical-path row, one observable outcome, and the "no Rust change" conclusion is correct — I re-derived all four cited facts from source (`:101`, `:344`, `:1061-1064`, `:1185`, `:1214`, `:1226`, `:394`, `:465`). The proof-only shape converts an audit assumption into a guarded regression test, which is real value. **−2 (F1)**: the spec's bridge sentence from session scope to instance separation is false at this base — mcp creates **one session per node** today (`service.rs:419-433`, a `OnceCell` on the `Service`; per-instance keying is the sibling that is still `specced`), and `launch`/`run` name no session at all (0 `sessions` references in `cartridge.ctg/src`; the per-run `sessions create` lives in `agent.ctg/src/lib.rs:273-278`). Also, "What changes" still reads as if code may change ("removes any per-process assumption left in the code") while the Planning note says there is none. |
| Ownership and reuse | 19 | Owner `sessions`, repo `sessions.ctg`, footprint entirely inside the submodule — no cross-submodule gitlink problem like the mcp sibling. Strong reuse: the delivery is one new test on the existing nine-test `native.ts` fixture, and the new file mirrors the established `children`/`dirs`/`afterEach`/`data` shape of `channels.test.ts` verbatim. The `native.ts` change is one word. **−1 (F2)**: `src/lib.rs` stays in the footprint although unmodified, so any unrelated dirty edit in it rides in on the collection receipt; `native.ts` is shared by nine tests and carries the same exposure (the analyst flags the second, not the first). |
| Dependencies and implementable slices | 19 | `needs` names the attach sibling, which is `done`; nothing else is required. One small spec, one prototype that applies cleanly at the stated base, one test, two static-guard blocks. The binary-version dependency is real and I verified it is met (`04aae7f` is an ancestor of `cartridge.ctg` HEAD, release build present). **−1 (F4)**: block 2 hard-depends on a developer-local absolute path for `CARTRIDGE_BIN`; template-sanctioned and it fails loudly on `test -x`, but the gate is not portable off this machine. |
| Observable acceptance and baseline evidence | 19 | Every `## Verify` block run verbatim as `sh -eu -c` on the patched tree: block 1 exit **0**, block 2 exit **0** (1 pass, 30 expects, 435–648 ms, cargo isolated), reproduced three times. Six denied worlds constructed and run, all exit **1**: two daemons over one store dir (ids 2/2, stale `alpha`/`[]`), per-caller `STORE` map, second `Store::load`, reservation line removed, `std::process::Command` present, session filter ignored, counter frozen — plus the node-absent world. No assertion passes at zero (the filter world failed with `+3`, proving the filtered listings are non-empty). **−1 (F3)**: box 3's `state === "active"` is largely redundant with the fixture's own `active()` gate, so the assertion's distinct content is `nodes.length === 1`, whose failure mode (a second slot) is argued from the mcp sibling's measurement rather than constructed here. Honestly stated in Remaining risk, but still one box proven by reference. |
| Failure, recovery and compatibility | 18 | Blocks fail loudly and in the right direction: missing file → `test -f` fails, missing tool → `test -x` fails, older base binary → the id assertions fail (the correct failure). Pass-2 safety is airtight (isolated target dir, zero in-footprint writes, self-contained fixture, live daemon untouched). **−1 (F5)**: the static guards pin four exact source lines by `grep -qF`, so a whitespace-only or refactor-only change to any of them fails collection with a message that reads like a regression; `test "$(grep -cF 'Store::load' …)" = 1` additionally forbids a legitimate second load site (e.g. a future test helper). **−1 (F6)**: `next` is reseeded from *persisted* buffers (`:344`), so closing the highest-id buffer and restarting the daemon reuses that id — flagged in Remaining risk and correctly scoped out, but it is the one way "no id is handed out twice" can still be violated across a daemon's lifetime, and no guard records it. |
| Reviewer total | **93 / 100** | ≥ 90 and no blocking finding. |

Findings and concrete revisions:

- **F1 (non-blocking, correct before collect).** `specs/spec01.md`, "Option chosen":
  "Each attached instance works under its own session id — that is what `mcp`'s
  per-instance `sessions create` **now** produces, and what `launch` and `run`
  name." Both halves are false at this base. Evidence: `mcp.ctg/src/service.rs:419-433`
  creates one `"MCP"` session per `Service` (per node) — the per-instance version is
  the sibling `mcp-keys-sessions-and-inflight-calls-by-attached-instance`, whose
  `state` is `specced`; and `grep -rn 'sessions' cartridge.ctg/src` returns nothing,
  while the per-run `sessions create` is `agent.ctg/src/lib.rs:273-278`. Recommended
  replacement: "Each *caller* that creates a session works under its own session id
  — an agent run does (`agent.ctg/src/lib.rs:273-278`), and mcp will once
  `mcp-keys-sessions-and-inflight-calls-by-attached-instance` lands; `launch` and
  `run` name no session themselves." This does not change the narrowing's premise,
  the box wording, or any assertion, which is why it is not blocking — but left as
  written it tells a reader that per-instance session separation exists today when
  it is still one `specced` sibling away, and this board has been burned by exactly
  that kind of supporting sentence.
- **F2 (advisory).** Check `git -C sessions.ctg status --porcelain` is empty before
  `prd collect`: the footprint sweeps `src/lib.rs` (unmodified by this PRD) and
  `native.ts` (shared by nine tests). It was clean at review time.
- **F3 (advisory).** If the board wants box 3 proven rather than delegated, the
  cheapest addition is a second profile slot under a different id asserted `failed`
  — but the mcp sibling already measured that world, and the spec says so.
- **F4/F5/F6 (advisory).** Recorded above; all three are already named in the spec's
  Remaining risk except F5's `Store::load` count, which is new here.

Disposition: **keep**. Proceed to implementation on `attempt-1.patch` as prototyped,
with F1's one-sentence correction to `spec01.md` applied first.

Validation (all in a private scratch tree, never the live checkout; exit codes observed):

| # | command | cwd | exit |
| --- | --- | --- | ---: |
| 1 | `git -C /Users/feb/dev/cartridge/sessions.ctg rev-parse HEAD` → `b896162`, `status --porcelain` empty | repo | 0 |
| 2 | `git -C sessions.ctg archive b896162 \| tar -x -C <scratch>/trees/base` | — | 0 |
| 3 | `git apply --check -p1 attempt-1.patch` | `trees/patched` | 0 |
| 4 | `git apply -p1 attempt-1.patch` | `trees/patched` | 0 |
| 5 | Verify **block 1** verbatim, `sh -eu -c` | `trees/patched` | **0** |
| 6 | Verify **block 1** verbatim (unpatched base, no `instances.test.ts`) | `trees/base` | **1** |
| 7 | block 1 — denied world: `STORE` as `Mutex<BTreeMap<String, Arc<SharedStore>>>` | `trees/denyA` | **1** |
| 8 | block 1 — denied world: a second `Store::load(config.dir.clone())` in `start` | `trees/denyB` | **1** |
| 9 | block 1 — denied world: reservation replaced by `state.next += 1` | `trees/denyC` | **1** |
| 10 | block 1 — denied world: `std::process::Command` added to `src/lib.rs` | `trees/denyE` | **1** |
| 11 | Verify **block 2** verbatim, `sh -eu -c` (1 pass, 30 expects, 437 ms) | `trees/patched` | **0** |
| 12 | Verify **block 2** verbatim (rerun, final control after all denied builds, 435 ms) | `trees/patched` | **0** |
| 13 | denied world: two daemons over one store dir, same assertions (`zz-denied.test.ts`, scratch, not shipped) — logged `ids 2 2` and `"name":"alpha","buffers":[]` after the rename | `trees/denyD` | **1** |
| 14 | block 2 — denied world: `buffers list` ignores `session` at `:597` and `:852` (`toEqual` failed `Received +3`) | `trees/denyF` | **1** |
| 15 | block 2 — denied world: `start` returns an error unconditionally (`sessions failed: reviewer: node refuses to start`) | `trees/denyG` | **1** |
| 16 | block 2 — denied world: shared counter never advances (`new Set(ids).size` 1, expected 6) | `trees/denyH` | **1** |
| 17 | tree checksum excluding `target/`, before and after blocks 1+2 — identical `92f6a0d…`; no in-repo `target/` created | `trees/patched` | 0 |
| 18 | `pgrep -fl "cartridge daemon"` before and after every run — no match each time | — | 1 (no match) |
| 19 | `git -C cartridge.ctg merge-base --is-ancestor 04aae7f HEAD` | `cartridge.ctg` | 0 |

Notes on method: the scratch trees came from `git archive`, not `git worktree add`,
so nothing was written into the live `sessions.ctg` checkout (not even `.git/worktrees`).
Every cargo command ran with `CARGO_TARGET_DIR` outside all repos. Extracted block
scripts and probe files live in a private subdirectory named for this task. One probe
is recorded as inconclusive and rerun: gating the broken `start` behind an env var
(`REVIEWER_BREAK_START`) left block 2 at exit 0 because the node process does not
inherit the test runner's environment; making the failure unconditional gave exit 1
(row 15), which is the result relied on.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this round.
Result: **PASS — 93/100**.
Unresolved blocking findings: **none**.
Rounds used / remaining: **1 / 4**.
Next action: apply F1's one-sentence correction to `specs/spec01.md` (does not
change the plan, the boxes or any assertion, so it does not make this rating
stale), then proceed to implementation of `attempt-1.patch`; the coordinator owns
the state transition.
