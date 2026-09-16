# analyst-1 — SPECCED

Base: root `4684791`, `cartridge.ctg` `63ff234` (clean). Board `root`.
Draft: `.state/loop/<slug>/spec01.md`, prototype `.state/loop/<slug>/attempt-1.patch`.

## Verdict

**SPECCED.** The defect is intact at HEAD, reproduces 5 of 5, and a validated
41-line prototype fixes it.

## The premise survived the sibling rewrite

`@root/one-daemon/.../an-instance-attaches-to-the-daemon-and-never-composes-silently`
(`cartridge.ctg` `1aefee3`) did rewrite `attach`, but it kept `settle_remote`
unchanged. The line number moved; the logic did not. At **current HEAD**:

| what | old (`cdd3124`/`771e046`) | HEAD (`63ff234`) |
| --- | --- | --- |
| `attach` | — | `cartridge.ctg/src/cli/host.rs:59` |
| the settle call | — | `cartridge.ctg/src/cli/host.rs:74` |
| `settle_remote` | — | `cartridge.ctg/src/cli/host.rs:147` |
| the three-identical-poll return | `:157` | `cartridge.ctg/src/cli/host.rs:180` |

Callers of `attach`, all in the same file and all of which already know their
event key: `:226` (`run`, has `key`), `:241` (`launch`, `"proxy"`), `:287`
(`mcp`), `:313` (the `Backend` re-attach, `"mcp"`). There are no others.

`Status` carries `state` and `listen` (`cartridge.ctg/src/host/mod.rs:38-48`), so
a listener-aware wait needs no new RPC.

## Reproduction

Isolated project only: a scratch `CARTRIDGE_HOME` under `mktemp -d`, the profile
built from the live `.cartridge/init.lua` with `mcp.ctg`/`memo.ctg` snapshot
copies and the rest symlinked, every daemon reaped and the root removed. **The
live project daemon was never started, stopped, replaced or reloaded, and no
build ever used a live `target/`.**

First attempt was a **false reproduction** and is recorded as such: it omitted the
`cartridge trust <runtime>` step, so 15 of 17 cartridges failed with "is in no
trusted project" and `mcp` failed with "needs `sessions`, which no cartridge
declares". The observed error was ``mcp` is not provided`, not the PRD's message.
Discarded.

With `trust` added, the cold-host timeline (daemon spawned, `status` polled every
400 ms):

```
t=0.4s {"starting":10,"waiting":7}
t=0.8s {"active":12,"starting":1,"waiting":4}
t=1.2s {"active":13,"starting":2,"waiting":2}   <- harness/mcp starting, agent/proxy waiting
t=1.6s {"active":15,"starting":2}               <- mcp active
```

The picture at 1.2 s holds unchanged for ~300-400 ms. That is three identical
100 ms polls, `stable >= 3` fires, `settle_remote` returns while `mcp` is still
`starting`, and `client::bail(&peer, "mcp", …)` fails. Five cold `cartridge mcp`
runs, each answering `initialize` and `tools/list` on stdin:

```
RUN 1..5: code=0, 1.9-2.1s, ``service `mcp` unavailable: no active listener``
FAILS 5/5
```

That is verbatim the message in the PRD outcome. **The defect reproduces at HEAD.**

## What bounds the wait today

`attach`'s own loop is bounded by `startup_timeout_secs` (60 s,
`cartridge.ctg/src/cli/host.rs:63`), but the `Ok(Some(found))` arm calls
`settle_remote(&found.0, settings.verify_timeout())` at `:74` and returns from
inside that arm, so the attach deadline never applies to the settle. The settle's
only bound is `verify_timeout_secs`, whose declared default is **300 s** and whose
doc in `cartridge.ctg/.cartridge/settings.json` is "How long `verify` waits for a
composition to settle before calling it stuck" — a `verify` budget. The setting
that documents startup is `startup_timeout_secs` (default 60, "How long a
cartridge has to serve and apply"). `event_timeout_ms` (60000) is unrelated: it
bounds a sender waiting on a listener, not the attach.

**Box 2's "documented startup deadline" is `host.startup_timeout_secs`.** The spec
moves the settle onto `settings.startup_timeout()` and leaves `verify_timeout()`
to its three in-process callers (`src/host/run.rs:37`, `:166`,
`src/cli/setup.rs:649`).

## The fix, prototyped and validated

`attempt-1.patch` (one file, +41/-19): `attach` takes `key: &str` and passes it
through; `settle_remote` returns as soon as an `active` cartridge lists `key`;
the `stable`/`last` shortcut is deleted; the status call is wrapped in
`tokio::time::timeout(left, …)` so the deadline actually binds; a three-line
`serves()` helper. One guard in the shared function, so `run` and `launch` are
fixed with `mcp`.

Built in a detached worktree of `cartridge.ctg` at `63ff234` with sibling `*.ctg`
symlinks, `CARGO_TARGET_DIR=$HOME/.cache/cartridge-smoke-target/cartridge.ctg`.

| probe | HEAD | patched |
| --- | --- | --- |
| 5 cold runs, trusted | **5/5 fail** in ~2.0 s | **0/5 fail**, 2.8-3.1 s, `tools/list` answered |
| 2 cold runs, untrusted (`mcp` never active) | fails ~2.0 s | fails 2.6 s / 2.8 s, message names `mcp`, no hang |

The untrusted case matters: it shows the fix does not turn a missing listener
into a 60 s stall — `!starting && !empty` still ends the wait as soon as the
composition stops moving.

## Commands run, with observed exit codes

| cwd | command | exit |
| --- | --- | --- |
| repo | `git rev-parse HEAD`, `git -C cartridge.ctg rev-parse HEAD`, `git -C cartridge.ctg status --porcelain` (clean) | 0 |
| repo | `bun run <scratch>/coldprobe.ts` (no `trust`, HEAD binary) — **invalid fixture, discarded** | 1 |
| repo | `bun run <scratch>/trace.ts` (no `trust`) — showed 15 failed, trust cause | 0 |
| repo | `bun run <scratch>/trace.ts` (with `trust`) — timeline above | 0 |
| repo | `RUNS=5 bun run <scratch>/coldprobe.ts`, HEAD binary — **FAILS 5/5** | 0 (script prints `FAILS 5/5`) |
| `cartridge.ctg` | `git worktree add --detach <scratch>/wt/cartridge.ctg HEAD` | 0 |
| worktree | `cargo build --bin cartridge` (`CARGO_TARGET_DIR` = smoke cache) | 0, 3.33 s |
| repo | `RUNS=5 bun run <scratch>/coldprobe.ts`, patched binary — **FAILS 0/5** | 0 |
| repo | `SKIP_TRUST=1 RUNS=2 bun run <scratch>/coldprobe.ts`, patched — fails fast, names `mcp` | 0 |
| worktree | `cargo clippy --all-targets --all-features -- -D warnings` | 0 (`Finished`, no warnings) |
| repo (unpatched) | the spec's guard block via `sh -eu -c` | **1** — "settle_remote still ends the wait on three identical polls" |
| `<scratch>/wt` (patched) | the same guard block via `sh -eu -c` | **0** — "source guards ok" |

Each of the eight guard patterns was additionally matched against both trees
individually; all eight discriminate (3 present only unpatched, 5 present only
patched). No guard is unfailable.

Not run, left to the implementer: `just check cartridge`, `just test cartridge`,
`just test lifecycle` (box 4) — they are Verify blocks in the spec with an
isolated `CARGO_TARGET_DIR`.

## Box 1 designed against flake

Argued in full in the spec. In short: the baseline failure is deterministic
(5/5 in ~2.0 s, with a 300-400 ms plateau against a 1.6 s listener — an
order-of-magnitude margin, not a race), so a 5/5 pass is signal. After the fix,
machine load can only make a run slower, never failing, so the per-run kill
timeout is 90 s — above `startup_timeout_secs` (60) plus slack. The one genuine
load failure (a cartridge exceeding its own 60 s budget) surfaces as `failed`
with a message naming `mcp`, and the fixture prints the last `status`, so it is
diagnosable rather than a mystery. Five runs share one root with the daemon
reaped between them: every run is a cold *host*, while run 1 is genuinely cold
and runs 2-5 are warm, which is the only real timing variable.

## Footprint

**No change needed.** `cartridge.ctg` + `cartridge.ctg/src/cli/host.rs` covers the
whole edit; the Verify fixture is self-contained and writes only to
`$HOME/.cache/cartridge-cold-mcp` and `mktemp -d`.

One follow-up is disclosed instead of folded in:
`.cartridge/tests/integration/smoke.test.ts` still pre-starts the daemon for its
mcp case with a comment naming this PRD as the owner of that workaround. That
path is free (it was the entire footprint of the now-`done`
`@root/smoke-passes-mcp-and-proxy`), but adding a superproject path here would
break the no-lane submodule landing shape, so it is recommended as its own PRD.

## Landing shape

Superproject PRD, submodule-only footprint: **collect with no lane**. A
superproject lane worktree has empty submodules and Verify pass 1 cannot build
there. The implementer works in a worktree of `cartridge.ctg` with the sibling
`*.ctg` directories symlinked beside it (without them `cargo build` cannot
resolve the `../<sibling>.ctg` path deps — confirmed necessary here); the
coordinator fast-forwards the live submodule and collects with no lane. The spec
says so, and its Verify blocks are written to run once, in `repo`.

## Overlap with `@root/an-attach-gives-up-on-a-daemon-that-answers-its-socket-but-never-its-status`

Real and disclosed. Both touch `settle_remote`'s status call.

- That PRD (prio 70, open) owns `cartridge.ctg/src/transport/rpc.rs` and fixes
  `Peer::call`'s untimed oneshot at `rpc.rs:239-257` for every caller.
- `settle_remote`'s `while now < deadline` only runs *between* calls, so today
  the deadline does not bind at all against a socket that answers and never
  replies. This fix increases the number of status polls on a cold host, so it
  would make that hang easier to hit — hence the local
  `tokio::time::timeout(left, …)` wrapper, which is the in-footprint way to bound
  it (`rpc.rs` is not in this footprint).
- They do not fight. The `rpc`-layer fix makes the local wrapper redundant but
  harmless, and the coordinator can drop the wrapper when it lands. If the
  coordinator wants one coherent change instead, widen this footprint to include
  `cartridge.ctg/src/transport/rpc.rs` and drop the wrapper — but that makes this
  PRD wait on a fix it does not need. **Recommendation: ship both, this one
  first.**

## Remaining uncertainty

- `just check/test cartridge` and `just test lifecycle` were not run; only
  `cargo clippy --all-targets --all-features -D warnings` (exit 0) on the patched
  worktree.
- The Verify build blocks are modelled on `@root/smoke-passes-mcp-and-proxy`'s
  persistent-cache pattern; a genuinely cold cache may exceed the 120 s block
  limit on the first collect, as it can for that sibling. Warm, the host build
  measured 3.3 s.
- The fixture symlinks the non-snapshot modules from the live tree (as the
  existing smoke does) and so requires `sessions.ctg/target/debug/libsessions.dylib`
  to exist; the block asserts that explicitly rather than skipping.
