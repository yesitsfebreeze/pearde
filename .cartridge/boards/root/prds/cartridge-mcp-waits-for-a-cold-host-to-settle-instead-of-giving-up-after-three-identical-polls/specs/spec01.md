---
complexity: S
footprint:
  - cartridge.ctg
  - cartridge.ctg/src/cli/host.rs
---

# spec01 — the attach wait ends on the caller's listener, not on a repeated picture

## Context measured at HEAD (root `4684791`, `cartridge.ctg` `63ff234`)

The done sibling `@root/one-daemon/.../an-instance-attaches-to-the-daemon-and-never-composes-silently`
(`cartridge.ctg` `1aefee3`) rewrote `attach`, but it kept `settle_remote`. The defect
is intact and moved: the old `src/cli/host.rs:157` is now

- `attach` — `cartridge.ctg/src/cli/host.rs:59`
- the settle call — `cartridge.ctg/src/cli/host.rs:74`, `settle_remote(&found.0, settings.verify_timeout())`
- `settle_remote` — `cartridge.ctg/src/cli/host.rs:147`
- the three-identical-poll return — `cartridge.ctg/src/cli/host.rs:180`, `if stable >= 3 && !empty { return; }`

Measured cold-start timeline in an isolated project (scratch `CARTRIDGE_HOME`,
daemon spawned by `attach` itself): `{starting:10, waiting:7}` at 0.4 s,
`{active:13, starting:2, waiting:2}` at 1.2 s and *unchanged* through ~1.5 s,
`mcp` active at 1.6 s. That unchanged plateau is three identical 100 ms polls, so
`settle_remote` returns at ~1.5 s, `attach` hands back the peer, and
`client::bail(&peer, "mcp", …)` fails in ~2.0 s with exactly the PRD's message:
``service `mcp` unavailable: no active listener``.

**The baseline is probabilistic, not deterministic — corrected in round 2.** The
first analyst measured 5 failures of 5 and the PRD's Outcome reports 3 of 3, but
both counted runs that reused one project root, where only the first run is
genuinely cold. Against a *fresh* project root per run the defect is a real but
intermittent cold-start race: the round-1 reviewer measured **5 failures of 8**,
and this revision measures **31 failures of 108 cold runs (29 %)** with the
fixture below, on an unpatched binary built from `63ff234`. The patched binary is
**0 failures of 35** over the same fixture. What decides a single run is not the
size of the 300-400 ms plateau against the 1.6 s listener — it is whether any
~300 ms window happens to pass with no state change at all before `mcp` goes
active. Box 1 is sized for the measured rate, not for the margin; see
"Why box 1 discriminates".

**Which deadline is real.** `attach`'s own loop is bounded by
`startup_timeout_secs` (60 s), but the `Ok(Some(found))` branch calls
`settle_remote(…, settings.verify_timeout())` and returns from inside that
branch, so `attach`'s deadline never applies to the settle. The wait's only bound
today is `verify_timeout_secs`, whose declared default is 300 s and whose own doc
in `cartridge.ctg/.cartridge/settings.json` reads "How long `verify` waits for a
composition to settle before calling it stuck" — a `verify` budget, not a startup
one. The setting that documents startup is `startup_timeout_secs` (default 60,
"How long a cartridge has to serve and apply"). **Acceptance box 2's "documented
startup deadline" is `host.startup_timeout_secs`**, and this spec moves the settle
onto it. Nothing else changes: `verify_timeout()` keeps its three in-process
callers (`src/host/run.rs:37`, `src/host/run.rs:166`, `src/cli/setup.rs:649`).

## Option chosen

Every caller of `attach` already knows the event key it is about to send —
`run` has `key`, `launch` has `"proxy"`, `mcp` and the `Backend` re-attach have
`"mcp"` (`src/cli/host.rs:226,241,287,313`; there are no other callers). So the
fix is one guard in the shared function, not four guards in the callers, and it
repairs `cartridge run` and `cartridge launch` on a cold host at the same time.

`attach` takes `key: &str` and passes it to `settle_remote`, which returns as
soon as an **active** cartridge lists `key` in its `listen` array (the field is
already in the `status` payload — `Status` at `src/host/mod.rs:38-48`). The
`stable`/`last` three-identical-poll shortcut is **deleted**: it exists only to
stop the loop when nothing more will happen, and the `!starting && !empty`
return already does that correctly and honestly.

The three other `verify_timeout()` callers are untouched and stay correct: they
all go through `Host::settled` (`src/host/run.rs:12`), an in-process
lifecycle-event wait with no poll shortcut of its own, used by `verify`,
contracts and `setup` — which genuinely want the verify budget.

**Accepted cost of deleting the shortcut.** One case gets slower. When the key is
never served *and* some cartridge stays `starting`/`waiting`, the old code
returned after ~300 ms; the new code polls to `host.startup_timeout_secs` (60 s)
and only then lets the caller fail. That is the point — a still picture is not an
answer — and it is bounded by the same budget a cartridge already has to serve.
It did not appear in either degraded composition measured (untrusted project:
1.6-2.8 s), because trust-refused cartridges go `failed`, leaving nothing
`starting`, so `!starting && !empty` still returns at once. Reaching the 60 s
worst case needs a cartridge that hangs in `starting` for its own full budget,
which is a cartridge bug the old shortcut hid behind a fast, wrong answer.

Rejected: keeping the shortcut and only raising the poll count — a cold host's
plateau is unbounded in length, so no count is safe. Rejected: waiting merely
until nothing is `starting`/`waiting` without knowing the key — it passes box 1
here but still hands the caller a peer that cannot serve it, and it is no
smaller.

**Bounding the poll itself.** `settle_remote`'s `while now < deadline` check only
runs *between* `peer.call("status", …)` calls, and `Peer::call`
(`cartridge.ctg/src/transport/rpc.rs:239-257`) awaits an untimed oneshot, so a
daemon that answers its socket and never its status hangs the loop forever
regardless of the deadline. Because the fix makes the loop poll for longer in the
normal case, the status call is wrapped in `tokio::time::timeout(left, …)` so the
deadline actually binds. This is deliberately *inside the footprint*: `rpc.rs` is
not in it. See "Overlap" below.

## Acceptance

- [ ] In an isolated project (scratch `CARTRIDGE_HOME`, no running daemon), `cartridge mcp` answers `initialize` and `tools/list` on **15 of 15** consecutive cold starts, each run in its **own freshly built project root** with its daemon reaped and the root removed before the next; and each cold `tools/list` is non-empty and exactly as long as the same call against the now-settled daemon.
- [ ] In the same isolated project with the composition left untrusted, so no cartridge serving `mcp` ever becomes active, `cartridge mcp` fails in under `host.startup_timeout_secs` (60 s) with a message naming `mcp`, and does not hang.
- [ ] `cartridge.ctg/src/cli/host.rs` contains no `stable >= 3` return and no `settle_remote(&found.0, settings.verify_timeout())`; the settle is called with the caller's key and `settings.startup_timeout()`.
- [ ] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

## Landing shape

**Collect with no lane.** This is a superproject PRD whose whole footprint is
inside the `cartridge.ctg` submodule. A superproject lane worktree has empty
submodules, so Verify pass 1 cannot build there (measured on a sibling:
`manifest path … does not exist`, exit 101). The implementer works in a worktree
of `cartridge.ctg` — with the sibling `*.ctg` directories symlinked next to it,
or `cargo build` cannot resolve the `../<sibling>.ctg` path deps — and the
coordinator fast-forwards the live submodule and collects with **no lane**. The
Verify blocks below therefore run **once, in `repo`**.

## Steps

1. In a worktree of `cartridge.ctg` at `63ff234` with sibling `*.ctg` symlinks,
   apply `attempt-1.patch` (beside this spec; validated, see Proof). It is the
   whole change: 41 insertions, 19 deletions, one file.
2. Change `attach(project: &Project)` to `attach(project: &Project, key: &str)`
   and update the four call sites at `src/cli/host.rs:226,241,287,313`
   (`key`, `"proxy"`, `"mcp"`, `"mcp"`).
3. In `attach`, call `settle_remote(&found.0, key, settings.startup_timeout())`.
4. Rewrite `settle_remote(peer, key, timeout)`: bound each `peer.call("status",
   …)` with `tokio::time::timeout(left, …)` where `left` is the remaining budget;
   keep the untrusted-reload branch as is; return when `serves(&status, key)`;
   keep the `!starting && !empty` return; delete `stable`, `last` and the
   `stable >= 3` return.
5. Add `fn serves(status: &Value, key: &str) -> bool` — an `active` entry whose
   `listen` array contains `key`. It mirrors the existing `explain`
   (`src/cli/host.rs:~195`), which already reads `state` and `listen` the same
   way; do not generalise either into a shared helper for two three-line uses.
6. Run the gates of box 4 with an isolated `CARGO_TARGET_DIR`.

Nothing outside `cartridge.ctg/src/cli/host.rs` changes. In particular
`.cartridge/tests/integration/smoke.test.ts` is **not** touched: it is outside
this footprint. Its mcp case still pre-starts the daemon and carries a comment
naming this PRD as the owner of that workaround — removing it needs a separate
PRD or a footprint widening, and is listed as remaining work below.

## Why box 1 discriminates

The round-1 version of this box did **not**. It built one temp project root
before the loop and reaped only the daemon between runs, so runs 2-5 were
page-warm and could not fail; the whole box rested on run 1. Run against an
**unpatched** binary it gave `1 of 5 wrong`, then `5/5 ok`, then `5/5 ok` — it
passed the tree it exists to reject in 2 of 3 attempts. The revision fixes that
and sizes the box for the measured failure rate:

- **Every run builds its own project root, inside the loop.** `makeRoot()` mints
  a fresh `mktemp -d`, writes `init.lua`/`config.lua`, re-copies the snapshot
  cartridges with their dylibs, and the run's `finally` reaps the daemon *and*
  removes the root. No run inherits another's page cache or daemon state. The
  proof this matters: with the revised fixture, unpatched failures land on run 1,
  2, 3, 4 and 5 across attempts, not only on run 1.
- **Fifteen cold runs, because five is not enough.** The measured per-run failure
  rate on an unpatched binary is 31 of 108 (29 %). Five independent cold runs
  would therefore still pass an unpatched tree with probability 0.71⁵ ≈ 18 %;
  fifteen give 0.71¹⁵ ≈ 0.6 %, under the 1 % the box needs to be a gate.
  Measured, not argued — blocks 4 and 5 extracted verbatim and run against a
  binary built from a clean `63ff234` archive, three paired attempts:

  | attempt | block 4 (8 runs) | block 5 (7 runs) | box 1 |
  | --- | --- | --- | --- |
  | 1 | exit 1, `1 of 8 wrong` | exit 1, `1 of 7 wrong` | RED |
  | 2 | exit 1, `2 of 8 wrong` | exit 1, `2 of 7 wrong` | RED |
  | 3 | exit 1, `3 of 8 wrong` | exit 1, `1 of 7 wrong` | RED |

  Five further paired attempts against an unpatched binary that block 2 built
  from the live checkout were RED 5 of 5 as well. One of those block-5
  invocations passed on its own (`7/7 ok`) — which is exactly why box 1 needs
  **both** blocks: a 7-run block alone lets an unpatched tree through about 9 %
  of the time. On the patched binary both blocks exited 0 (`8/8 ok` in 31 s,
  `7/7 ok` in 26 s), and the earlier 5-run version of this same fixture exited 0
  in 1 of 5 attempts against the unpatched binary — the ~18 % the arithmetic
  predicts.
- **The 15 runs are split across two blocks (8 + 7).** Each `sh` block has a
  hard 120 s engine limit; 8 runs measured 31-41 s and 7 runs 27-32 s here, so
  one 15-run block at ~60 s would leave no headroom on a slower host. Both blocks
  must exit 0.
- **`tools/list` is counted, not grepped.** `out.includes('"tools"')` is
  satisfied by `{"tools":[]}`. The fixture parses the `id: 2` response, requires
  a non-empty array, and compares its length with the same call made against the
  now-settled daemon in the same root — so a short list handed back before the
  composition finished fails the run. Measured: 19 tools cold and 19 settled on
  every passing run; a failing cold run reports `cold=-1 settled=19`.
- **After the fix, load cannot cause a failure, only a slower pass.** The wait
  ends on the listener, so a loaded machine makes each run take longer, not fail.
  The fixture's per-run kill timeout is therefore **90 s**, above
  `startup_timeout_secs` (60 s) plus slack, so a slow machine yields a slow pass.
  A run that exceeds 90 s is a real regression, not load.
- **The one genuine load failure is legible.** If a cartridge exceeds its own
  60 s budget it goes `failed`, the composition stops changing, `settle_remote`
  returns through `!starting && !empty`, and `cartridge mcp` fails with a message
  naming `mcp`. The fixture prints the last `status` on any failure, so that case
  is diagnosable rather than a mystery flake.

## Proof already gathered (prototype, not the implementation)

`attempt-1.patch`, built with `CARGO_TARGET_DIR=$HOME/.cache/cartridge-smoke-target/cartridge.ctg`
in a detached worktree of `cartridge.ctg` at `63ff234`:

| probe | HEAD | patched |
| --- | --- | --- |
| 5 `cartridge mcp` runs, trusted project, **one reused root** (round 1) | 5/5 fail, ~2.0 s, ``service `mcp` unavailable: no active listener`` | **0/5 fail**, 2.8-3.1 s, `tools/list` answered |
| 2 cold runs, untrusted project (`mcp` never active) | fails ~2.0 s | fails 2.6 s and 2.8 s, message names `mcp`, no hang |
| `cargo clippy --all-targets --all-features -- -D warnings` | — | exit 0 |

Round 2, with the revised fixture below (**a fresh project root per run**), both
binaries built from `63ff234` into isolated `CARGO_TARGET_DIR`s outside every
live `target/`:

| probe | HEAD (unpatched) | patched |
| --- | --- | --- |
| cold runs, trusted | **31 failures of 108 (29 %)** | **0 failures of 35** |
| block 4 verbatim, 8 runs | exit 1 ×8 of 8 | exit 0, `8/8 ok`, 31 s |
| block 5 verbatim, 7 runs | exit 1 ×7, exit 0 ×1 | exit 0, `7/7 ok`, 26 s |
| box 1 (blocks 4 **and** 5) | **RED in 8 of 8 attempts** | GREEN |
| the same fixture at only 5 runs | exit 1, 1, 1, 1, **0** — 5 runs is not a gate | exit 0, `5/5 ok`, 20 s |
| `tools/list` length, cold vs settled | `cold=-1` on a failed run | 19 and 19, every run |
| block 6 (untrusted) | — | exit 0, fails in 2.0 s and 2.0 s naming `mcp` |
| block 1 (source guards) | exit 1, names the shortcut | exit 0, `source guards ok` |

## Verify and Proof

<!-- No lane: these blocks run once, with cwd = `repo` (the superproject root).

Block budget: the engine kills each block at 120 s. Measured here — guards <1 s,
host build 8.9 s, dylib builds 11.5 s, cold block A (8 runs) 31-41 s, cold block
B (7 runs) 27-32 s, untrusted 4 s, `just check` 11.5 s, `just test cartridge`
18.1 s, `just test lifecycle` 42.2 s. **The build numbers assume this machine's
`rustc-wrapper = "kache"`**, which lives in `~/.cargo/config.toml` and **not** in
this repo: 8.9 s is a *cold-target* build only because that cache is warm. On a
host or CI without it, blocks 2 and 3 are a full dependency build and will exceed
120 s; there the implementer must pre-warm `$C` outside the block (the blocks are
idempotent and skip work when `$C` is already built).

Blocks 2 and 3 set `CARGO_TARGET_DIR` **unconditionally**, not in the template's
`${CARGO_TARGET_DIR:-…}` form, on purpose: the cold fixture must run the binary
these blocks just built, so an inherited target dir would silently hand it a
different one, and the `$C` cache is what makes the 120 s budget hold across
re-runs. Block 2 also passes `--locked`, because `cartridge.ctg/Cargo.lock` is
inside this footprint and a lock refresh during pass 2 aborts collection with
"source footprint changed"; `--locked` fails loudly instead of writing it. Blocks
6-8 keep the template form, since `just` owns those builds. -->


```sh
set -eu
f=cartridge.ctg/src/cli/host.rs
test -f "$f"
# `set -e` does not fire for a `!`-prefixed command, so every negative guard is
# an explicit `if grep …; then exit 1; fi`.
if grep -qn 'stable >= 3' "$f"; then
  echo "settle_remote still ends the wait on three identical polls" >&2; exit 1
fi
if grep -qn 'settle_remote(&found.0, settings.verify_timeout())' "$f"; then
  echo "the attach settle still runs on verify_timeout_secs (300 s)" >&2; exit 1
fi
if grep -qn 'pub(crate) async fn attach(project: &Project) -> Result<Attached>' "$f"; then
  echo "attach still takes no listener key" >&2; exit 1
fi
grep -qn 'settle_remote(&found.0, key, settings.startup_timeout())' "$f"
grep -qn 'fn serves(status: &Value, key: &str) -> bool' "$f"
grep -qn 'tokio::time::timeout(left, peer.call("status"' "$f"
grep -qn 'attach(project, "mcp")' "$f"
grep -qn 'attach(project, "proxy")' "$f"
echo "source guards ok"
```

```sh
set -eu
# One persistent cache, isolated from every live `target/`: a build in a live
# target dir hot-restarts the running cartridges of this project.
C="$HOME/.cache/cartridge-cold-mcp"
mkdir -p "$C"
export CARGO_TARGET_DIR="$C/host"
# `--locked`: `cartridge.ctg/Cargo.lock` is inside the footprint, and a refresh
# of it during pass 2 aborts collection.
cargo build --locked --bin cartridge --manifest-path cartridge.ctg/Cargo.toml
test -x "$C/host/debug/cartridge"
echo "host built at $C/host/debug/cartridge"
```

```sh
set -eu
C="$HOME/.cache/cartridge-cold-mcp"
export CARGO_TARGET_DIR="$C/mcp"
cargo build --lib --manifest-path mcp.ctg/Cargo.toml
mkdir -p "$C/built/mcp.ctg/debug"
cp "$C"/mcp/debug/lib*.dylib "$C/built/mcp.ctg/debug/"
export CARGO_TARGET_DIR="$C/memo"
cargo build --lib --manifest-path memo.ctg/Cargo.toml
mkdir -p "$C/built/memo.ctg/debug"
cp "$C"/memo/debug/lib*.dylib "$C/built/memo.ctg/debug/"
ls "$C/built/mcp.ctg/debug" "$C/built/memo.ctg/debug"
```

```sh
set -eu
C="$HOME/.cache/cartridge-cold-mcp"
test -x "$C/host/debug/cartridge"
test -d "$C/built/mcp.ctg/debug"
# `mcp` needs `sessions`, which has no snapshot here and is symlinked from the
# live tree, exactly as `.cartridge/tests/integration/smoke.test.ts` does. Fail
# loudly rather than skipping if that tree is not built.
test -f sessions.ctg/target/debug/libsessions.dylib
cat > "$C/cold.ts" <<'TS'
import fs from "node:fs"; import os from "node:os"; import path from "node:path";
const runtime = process.env.CARTRIDGE_RUNTIME!;
const binary = process.env.CARTRIDGE_BIN!;
const built = process.env.CARTRIDGE_BUILT!;
const skipped = new Set(["target", ".git", "node_modules"]);
const trusted = !process.env.SKIP_TRUST;
const init = fs.readFileSync(path.join(runtime, ".cartridge", "init.lua"), "utf8");
const modules = [...new Set([...init.matchAll(/path\s*=\s*"([^"\n]+)"/g)].map(m => m[1]))]
  .sort((a, b) => a.split("/").length - b.split("/").length);
// Every run gets its OWN project root, built inside the loop. A root reused
// across runs keeps its snapshot dylibs page-warm and its daemon state dir
// populated, so only the first run is genuinely cold and the box stops
// discriminating the fix: the round-1 fixture built one root up front and an
// unpatched binary passed it in 2 of 3 attempts.
function makeRoot() {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "cold-mcp-")));
  const directory = path.join(root, "mcp"), builtin = path.join(directory, "builtin");
  const inner = path.join(directory, ".cartridge");
  fs.mkdirSync(builtin, { recursive: true }); fs.mkdirSync(inner, { recursive: true });
  fs.writeFileSync(path.join(inner, "init.lua"), init);
  for (const module of modules) {
    const destination = path.join(builtin, module);
    if (fs.existsSync(destination)) continue;
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    const snapshot = path.join(built, module, "debug");
    if (fs.existsSync(snapshot)) {
      fs.cpSync(fs.realpathSync(path.join(runtime, module)), destination,
        { recursive: true, filter: s => !skipped.has(path.basename(s)) });
      fs.mkdirSync(path.join(destination, "target/debug"), { recursive: true });
      for (const lib of fs.readdirSync(snapshot).filter(f => f.endsWith(".dylib")))
        fs.copyFileSync(path.join(snapshot, lib), path.join(destination, "target/debug", lib));
    } else fs.symlinkSync(fs.realpathSync(path.join(runtime, module)), destination);
  }
  const prdRoot = path.join(directory, "prd-fixture");
  fs.mkdirSync(path.join(prdRoot, ".cartridge/boards/root"), { recursive: true });
  fs.writeFileSync(path.join(prdRoot, ".cartridge/boards/root/settings.md"), "# cold board\n");
  fs.writeFileSync(path.join(inner, "config.lua"), `return {
  sessions={dir=".cartridge/sessions"},memory={dir=".cartridge/memory",reason={url=""},tick={interval_secs=0},queue={enabled=false}},
  prd={root=${JSON.stringify(prdRoot)},default_board="root"},
  router={listen={"127.0.0.1:0"},config_dir=".cartridge/credentials",data_dir=".cartridge/router"},
  auth={credentials_dir=".cartridge/credentials",router_data_dir=".cartridge/router"},
  proxy={listen="127.0.0.1:0",cwd=".",key_env="CARTRIDGE_PROXY_KEY"},
  live={port=0,dir=".cartridge/live-data"},["live-record"]={dir=".cartridge/live-data"},
  mcp={cwd="."},policy={default="ask",tools={read="allow",docs="allow",write="ask"}},harness={max_bytes=262144},fs={store_dir=".cartridge/gitfs"}}`);
  return { root, cwd: directory, command: [binary, "--dir", builtin],
    env: { ...process.env, CARTRIDGE_HOME: root } as Record<string, string | undefined> };
}
const alive = (pid: number) => { try { process.kill(pid, 0); return true; } catch { return false; } };
async function reap(root: string) {
  const pids = (p: string) => Bun.spawnSync(["pgrep", "-f", p]).stdout.toString().split("\n").filter(Boolean).map(Number);
  const inside = (pid: number) => Bun.spawnSync(["lsof", "-a", "-p", String(pid), "-d", "cwd", "-Fn"]).stdout.toString()
    .split("\n").some(l => l.startsWith("n") && (l.slice(1) + "/").startsWith(root + "/"));
  const ours = [...new Set([...pids(root), ...pids(binary).filter(inside)])].filter(p => p !== process.pid);
  for (const pid of ours) try { process.kill(pid, "SIGTERM"); } catch {}
  for (const d = Date.now() + 5000; ours.some(alive) && Date.now() < d;) await Bun.sleep(100);
  for (const pid of ours.filter(alive)) try { process.kill(pid, "SIGKILL"); } catch {}
  await Bun.sleep(500);
}
const msgs = [
  { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "cold", version: "0" } } },
  { jsonrpc: "2.0", id: 2, method: "tools/list", params: {} },
].map(m => JSON.stringify(m) + "\n").join("");
// `out.includes('"tools"')` is satisfied by `{"tools":[]}`, so count them.
const tools = (out: string) => {
  for (const line of out.split("\n")) {
    if (!line.trim()) continue;
    let message: any; try { message = JSON.parse(line); } catch { continue; }
    if (message?.id === 2 && Array.isArray(message?.result?.tools)) return message.result.tools.length;
  }
  return -1;
};
async function mcpRun(ctx: ReturnType<typeof makeRoot>, ms: number) {
  const t0 = Date.now();
  const child = Bun.spawn([...ctx.command, "mcp"], { cwd: ctx.cwd, env: ctx.env, stdin: new Blob([msgs]), stdout: "pipe", stderr: "pipe" });
  const kill = setTimeout(() => child.kill("SIGKILL"), ms);
  const [out, err] = await Promise.all([new Response(child.stdout).text(), new Response(child.stderr).text()]);
  await child.exited; clearTimeout(kill);
  return { out, err, dt: (Date.now() - t0) / 1000 };
}
// 15 cold runs split 8 + 7 over two blocks: the engine kills a block at 120 s
// and 8 runs measured 31-41 s here.
const runs = trusted ? Number(process.env.RUNS ?? 8) : 2;
let bad = 0;
for (let i = 0; i < runs; i++) {
  const ctx = makeRoot();                 // a fresh, genuinely cold project root
  try {
    if (trusted) {
      const t = Bun.spawnSync([...ctx.command, "trust", runtime], { cwd: ctx.cwd, env: ctx.env, timeout: 20000 });
      if (t.exitCode !== 0) { console.error("trust failed: " + t.stderr.toString()); process.exit(1); }
    }
    // Above startup_timeout_secs (60 s) plus slack: a loaded machine must make
    // this slower, never failing.
    const { out, err, dt } = await mcpRun(ctx, 90_000);
    if (trusted) {
      const cold = tools(out);
      // The same question asked of the now-settled daemon: a cold answer that is
      // short because the composition had not finished is a failure too.
      const settled = tools((await mcpRun(ctx, 90_000)).out);
      const ok = cold > 0 && cold === settled && !out.includes("no active listener");
      if (!ok) { bad++;
        const s = Bun.spawnSync([...ctx.command, "status"], { cwd: ctx.cwd, env: ctx.env, timeout: 5000 }).stdout.toString();
        console.error(`run ${i + 1} FAILED after ${dt.toFixed(1)}s cold=${cold} settled=${settled}\n out=${out.slice(0, 400)}\n err=${err.slice(-400)}\n status=${s.slice(0, 1500)}`);
      } else console.log(`run ${i + 1} ok in ${dt.toFixed(1)}s, ${cold} tools cold and settled`);
      if (dt > 90) { bad++; console.error(`run ${i + 1} took ${dt.toFixed(1)}s, over the 90 s ceiling`); }
    } else {
      const named = (out + err).includes("mcp");
      if (!named || dt >= 60) { bad++; console.error(`run ${i + 1}: named=${named} ${dt.toFixed(1)}s out=${out.slice(0, 300)}`); }
      else console.log(`run ${i + 1} failed as designed in ${dt.toFixed(1)}s, naming mcp`);
    }
  } finally { await reap(ctx.root); fs.rmSync(ctx.root, { recursive: true, force: true }); }
}
if (bad) { console.error(`${bad} of ${runs} runs wrong`); process.exit(1); }
console.log(`${runs}/${runs} ok`);
TS
RUNS=8 CARTRIDGE_RUNTIME="$PWD" CARTRIDGE_BIN="$C/host/debug/cartridge" CARTRIDGE_BUILT="$C/built" \
  bun run "$C/cold.ts"
```

```sh
set -eu
C="$HOME/.cache/cartridge-cold-mcp"
test -x "$C/host/debug/cartridge"
test -f "$C/cold.ts"
# Runs 9-15 of box 1, in a second block because the engine kills one block at
# 120 s. Same fixture, same fresh-root-per-run rule.
RUNS=7 CARTRIDGE_RUNTIME="$PWD" CARTRIDGE_BIN="$C/host/debug/cartridge" CARTRIDGE_BUILT="$C/built" \
  bun run "$C/cold.ts"
```

```sh
set -eu
C="$HOME/.cache/cartridge-cold-mcp"
test -x "$C/host/debug/cartridge"
# The same fixture the previous block wrote, with the composition left untrusted
# so nothing serving `mcp` ever becomes active: box 2.
test -f "$C/cold.ts"
SKIP_TRUST=1 CARTRIDGE_RUNTIME="$PWD" CARTRIDGE_BIN="$C/host/debug/cartridge" \
  CARTRIDGE_BUILT="$C/built" bun run "$C/cold.ts"
```

```sh
set -eu
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/.cache/cartridge-cold-mcp/gates}"
just check cartridge
```

```sh
set -eu
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/.cache/cartridge-cold-mcp/gates}"
just test cartridge
```

```sh
set -eu
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$HOME/.cache/cartridge-cold-mcp/gates}"
just test lifecycle
```

## Implementer notes

- Do not touch the live project daemon or any live `target/` while iterating: use
  a worktree of `cartridge.ctg` and `CARGO_TARGET_DIR` under `$HOME/.cache/cartridge-cold-mcp`.

## Overlap with `@root/an-attach-gives-up-on-a-daemon-that-answers-its-socket-but-never-its-status`

They touch the same function and must land in a known order.

- That PRD fixes `Peer::call`'s untimed oneshot in `cartridge.ctg/src/transport/rpc.rs:239-257`,
  which is in *its* footprint and not in this one, and which fixes every caller.
- This spec adds `tokio::time::timeout(left, peer.call("status", …))` in
  `settle_remote` only, because without it this change strictly increases the
  number of status polls on a cold host and would make the hang easier to hit.
- They do not fight: a per-call timeout at the `rpc` layer makes this one
  redundant but harmless, and the coordinator can delete the local wrapper when
  the `rpc` fix lands. If the coordinator prefers one coherent change, the two
  can be merged by widening this footprint to `cartridge.ctg/src/transport/rpc.rs`
  and dropping the local wrapper — but that makes this PRD wait for a fix it does
  not need, so shipping both is recommended, this one first.

## Remaining work outside this PRD

`.cartridge/tests/integration/smoke.test.ts` still pre-starts the daemon for its
mcp case with a comment naming this PRD as the owner of that workaround. That
file is a repo-root path outside this footprint (it was the whole footprint of
the done `@root/smoke-passes-mcp-and-proxy`, so it is free). Removing the
workaround so `just smoke mcp` covers the cold path is a small follow-up PRD, or
a footprint widening here — but widening breaks the no-lane submodule landing
shape above, so a follow-up is recommended.
