# analyst-1 — SPECCED

PRD `@root/one-daemon-.../sessions-runs-once-in-the-daemon-with-one-buffer-id-space`,
`analyzing`, prio 80. Repo `sessions.ctg` at the brief's source HEAD `b896162`
("Keep test daemons out of the real cartridge home and let mailbox credentials
through"), which is the submodule's HEAD and clean (`git status --porcelain`
empty). Declared footprint `src/lib.rs`.

Drafts:

- `.state/loop/one-daemon-.../sessions-runs-once-in-the-daemon-with-one-buffer-id-space/spec01.md`
- `.state/loop/one-daemon-.../sessions-runs-once-in-the-daemon-with-one-buffer-id-space/attempt-1.patch`

## The code, traced

Everything below is `sessions.ctg/src/lib.rs` at `b896162` unless said
otherwise.

**The store is opened once per process.** `Store::load(dir)` has exactly one
call site, `:1214`, inside `start`. `start` installs the result in
`static STORE: OnceLock<Arc<SharedStore>>` (`:1185`) and a second `start`
returns "sessions already started" (`:1226`). Every op goes through
`store()` → `SharedStore::execute` (`:1232`, `:1236`, `:1260`), and `init.lua`
registers exactly two listeners onto them (`init.lua:11-12`). So one process =
one in-memory store, and two in-memory stores need two processes, which needed
two compositions.

**The buffer-id counter is the store's, not the process's.** `Store.next`
(`:101`) is a plain field. `Store::install` seeds it from what is on disk,
`self.next = self.next.max(b.id + 1)` for every persisted buffer (`:344`), so a
restart resumes above the highest persisted id. `execute` reserves one id per
operation under the store's write lock, *before* running it and whether or not
it succeeds (`:1061-1064`), and the transactional candidate carries that `next`
(`:1088`). The allocation sites are `buffers open` (`:868-869`), `checkpoint`'s
transcript (`:767-769`) and `mailbox_buffer` (`:829-830`), all off the same
field. The audit's "a counter local to each process" is accurate only as a
consequence of the store being per-process.

**There is no rename op.** `grep -rn rename src/` finds only `std::fs::rename`
in `Store::save` (`:394`), `channels.rs:293`, `mapping.rs:258`,
`retention.rs:83`, plus serde `rename_all` attributes. `save` (`:359-403`)
writes a temp file, fsyncs, and renames it over `<session>.json`
unconditionally; the `expected` compare-and-swap is passed only by
`repair_empty` (`:465`, via `publish_checked` `:417`). The full-store copy each
process holds is what makes one process's commit clobber another's — the file
rename is the mechanism, not a user-facing rename. The op an instance can
actually call, and what box 2 has to mean, is `sessions update {id, name}`
(`:695-700`).

**Scoping is by session, not by caller.** `Buffer.session: Option<String>`
(`:55`); `buffers list {session}` filters on it in both the read path
(`:594-604`) and the mutating path (`:846-856`); `buffers open {session}` pushes
the new id onto that session (`:878-881`). With no `session` key, `list`
returns every buffer in the store — before the one daemon too, because both
compositions read the same directory.

**No instance identity reaches this layer.** `cartridge call` is
`client::ask(project, "bail", {name, data})`
(`cartridge.ctg/src/cli/mod.rs:108-114` at `04aae7f`); the args arrive at
`sessions_op`/`buffers_op` as caller-supplied JSON and nothing else. This
matches the specced sibling `mcp-keys-sessions-and-inflight-calls-by-attached-instance`,
which had to make the mcp *bridge* mint an id because nothing above the
cartridge has one, and which put that id only in mcp's own event payload.

**The test surface already runs a real daemon.** `.cartridge/tests/integration/native.ts`
spawns `cartridge --dir <home> daemon` in a temp project (`:67-70`), polls
`cartridge status` until `sessions` is `active` (`:81-95`), and sends each
request as its own `cartridge call` child process (`:123-136`). Nine
integration tests already use it. So "exactly one sessions node with the daemon
running" and "two attached instances" are both observable from inside
`sessions.ctg` — I checked before considering any narrowing.

## Verdict on the two findings

- **Id-space collision: dissolves under one daemon.** One node, one process,
  one `STORE`, one `next`. Nothing per-process is left to remove.
- **Last-rename-wins: dissolves under one daemon.** One node, one in-memory
  copy, per-session gates (`self.gate(key)`, `:976-986`) and a store-wide
  `mutation` RwLock (`:948`, `:1020-1021`). Also the audit's wording was a
  misreading: the "rename" is the snapshot commit, and there is no rename op.

So this is a proof-only PRD, like `agent-runs-key-per-attached-instance-not-per-process`:
a regression test plus a static guard, no Rust change.

## What I probed, and the exit codes

Scratch worktrees of `sessions.ctg` at `b896162` under
`<scratchpad>/sessions-one-buffer-id-space/` (`wt` = prototype, `clean` =
patch validation, `denywt` = denied worlds). Isolated
`CARGO_TARGET_DIR=<scratchpad>/sessions-one-buffer-id-space/target` for every
cargo command; the live daemon was never touched.

| # | command | exit |
|---|---------|------|
| 1 | `git -C sessions.ctg status --porcelain` (clean at `b896162`) | 0 |
| 2 | `cargo build` in `wt`, `CARGO_TARGET_DIR` isolated | 0 |
| 3 | `bun test ./.cartridge/tests/integration/instances.test.ts` in `wt`, `CARTRIDGE_BIN` = cartridge.ctg debug (`04aae7f`) | 0 (1 pass, 30 expects, 617 ms) |
| 4 | **denied world:** same assertions with two daemons over one store dir (`zz-denied.test.ts`, scratch, not shipped) | **1** |
| 5 | `git apply --check attempt-1.patch` in a fresh `clean` worktree of `b896162` | 0 |
| 6 | `git apply attempt-1.patch` in `clean` | 0 |
| 7 | `bun test …/instances.test.ts` in `clean` | 0 (465 ms) |
| 8 | Verify **block 1** verbatim, `sh -eu -c`, cwd `clean` | 0 |
| 9 | Verify **block 2** verbatim, `sh -eu -c`, cwd `clean` (release `CARTRIDGE_BIN`, cargo 3.35 s, test 432 ms) | 0 |
| 10 | **denied world:** block 1 with `STORE` replaced by `Mutex<BTreeMap<String, Arc<SharedStore>>>` | **1** |
| 11 | **denied world:** block 1 with a second `Store::load(config.dir.clone())` added to `start` | **1** |

Probe 4 is the evidence that the audit's findings were real and that one daemon
is what fixes them. Two `Native` daemons, each in its own cartridge home and
project, both configured with the same sessions store `dir`:

```
ids 2 2
rename through the other instance: {"reply":3,"data":{...,"buffers":[],
  "id":"18d5cd0eea0b23b8-2","name":"alpha",...}}
(fail) two compositions collide on ids and lose the rename
```

Both nodes handed out buffer id **2** for two different sessions — a real
collision, from two stores loaded at start and counted forward independently.
And the second daemon's copy of the first's session still read `name: "alpha"`
with `buffers: []` after the first had renamed it to `renamed` and opened a
buffer in it: a stale full-store copy whose next snapshot commit would clobber
the other's. The assertion block failed at the id set (exit 1) before reaching
the rename assertion; the rename evidence is the logged record above. Under one
daemon the same calls give six distinct ids and read `renamed` back (probe 3).

I did **not** construct a second sessions *slot* inside the fixture's profile
for box 3. The mcp sibling already measured that world (same id breaks the
daemon; a different id leaves the second slot `failed`), and `state ===
"active"` is what stops the assertion passing with the node absent — the trap
that burned the board twice. I also did not assume the count was unobservable
here: the fixture runs a real daemon and a real `cartridge status`, which is
the third trap, and the spec's box 3 uses it.

## Footprint change needed

The delivery is two files, both outside the declared footprint:

- `.cartridge/tests/integration/instances.test.ts` (new)
- `.cartridge/tests/integration/native.ts` (drop `private` from `cli`, one word)

`src/lib.rs` is not modified. A test cannot live in it — sessions' unit modules
are `#[path]`-attributed out to `.cartridge/tests/unit/main/` (`:1282-1304`),
also outside the footprint — and an in-file `#[cfg(test)]` module could not
reach a real daemon or a second attached instance anyway. `collect` refuses a
change outside the declared footprint, so the coordinator must widen it to the
three paths in the spec's frontmatter before this lands.

## Boxes, and the one proposed narrowing

- Box 1's first clause (one id space) and third (isolation by session) are
  proven. Its literal second clause — "do not see each other's buffers unless
  they ask for them", read as *instance* isolation — is **not provable and not
  deliverable here**, because no instance identity reaches this cartridge and
  an unfiltered `buffers list` returns every buffer in the store, as it did
  before the one daemon. The spec proposes replacement wording that names the
  session as the scope and says plainly that an unfiltered listing is how an
  instance asks for everything; the test asserts that unfiltered listing too,
  so the behaviour is recorded rather than hidden. If instance-scoped listing
  is actually wanted, it needs caller identity in the host call protocol — the
  runtime-wide change the mcp sibling rejected for one consumer — and should be
  its own PRD under the parent.
- Box 2 is proven, with "rename" read as `sessions update {id, name}` (sessions
  has no rename op).
- Box 3 is proven at this cartridge's composed scope: one real daemon, real
  `cartridge call` instances, exactly one `id === "sessions"` entry in
  `cartridge status`, in state `active`. The whole-project count over all 20
  cartridges stays where the PRD's own box puts it — the done attach sibling,
  re-proven by the composed acceptance test.

## Remaining uncertainty

- `next` is seeded from *persisted* buffers, so closing the highest-id buffer
  and restarting reuses that id. Pre-existing, unchanged by the one daemon,
  outside these boxes. Flagged in the spec's risks.
- `CARTRIDGE_BIN` has to be named absolutely (the template's sanctioned form),
  because `../cartridge.ctg` does not resolve from a lane. It must carry the
  attach contract (`04aae7f` or later); an older binary composes per `call` and
  the test fails on the id assertions, which is the correct failure.
- `native.ts` is shared by nine integration tests; the one-word change is
  inert for them, but the file joining this footprint means anything else dirty
  in it rides in on the collection receipt.
