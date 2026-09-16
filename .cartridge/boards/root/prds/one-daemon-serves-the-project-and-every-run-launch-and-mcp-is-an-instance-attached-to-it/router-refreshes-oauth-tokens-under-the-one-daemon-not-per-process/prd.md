---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/router.ctg"
capability-owner: router
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/auth.rs"
- ".cartridge/tests/unit/auth/tests.rs"
commit: "effe3c5f57b634996a810c98bef756c90c630682"
---

# Router refreshes OAuth tokens under the one daemon, not per process

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies router as a bound
exclusive resource: its OAuth refresh lock only works inside one process
(`auth.rs:282`), so two hosts both spend the same refresh token. Under the
one-daemon shape there is one router node, so the lock holds again — but any
refresh initiated by an attached instance must go through that node.

## Outcome

Every refresh **that router.ctg performs** happens in the daemon's single
router node, where the in-process lock is the right lock. An attached instance
never refreshes on its own path.

This outcome deliberately stops short of "one refresh token is never spent
twice" — round 1 (F1) established that the stronger claim is **false and cannot
be made true from this board**. Two spenders live outside every composition: the
`codex` CLI on `~/.codex/auth.json` and the `claude` CLI on its keychain entry.
`src/auth.rs:367-369` concedes this in shipped source. Router can guarantee its
own refreshes are serialised; it cannot guarantee a token it does not solely
own. Saying otherwise in the Outcome while the boxes said the opposite was the
contradiction F1 named.

## What changes

- With the host-attach contract in force there is one router node; verify
  attached instances' routing requests flow through it.
- If any refresh path can still run outside the daemon (e.g. a CLI-side
  refresh), route it through the daemon or hold a file lock instead.

## Acceptance

- [x] Two concurrent refresh-triggering requests against one router node's
      `Auth` spend the refresh token exactly once: one POST to the token
      endpoint, one rotation of the stored refresh token, and both callers get
      working headers back. (The "through the daemon" leg — that two attached
      instances' requests land on the *same* router node — is a cartridge.ctg
      property, delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by `the-composed-acceptance-test-…`.)
- [x] No refresh code path in router.ctg can run outside a router node: the
      `auth` module is private to the crate, `Auth::from_path` has exactly one
      call site, that call site is `service::start`, its only caller is the Lua
      module entry, and the crate ships no binary.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. **The premise held fully**,
like the `mcp` sibling and unlike the other three. `src/auth.rs:686-687` (the
audit's `auth.rs:282` at revision `d5ce669`) is a per-`Auth` `tokio::sync::Mutex`,
in-process only. It guards `codex_headers`, which POSTs the stored refresh token
and **rotates** it; the compare-and-write guards at `:718`/`:732` protect the
*file*, not the *spend* — the POST is already done by the time the compare runs.
Two router nodes coexist on this project **by configuration**:
`.cartridge/config.lua:56-62` sets `listen = { "127.0.0.1:0" }` so concurrent
chats can coexist over one shared `data_dir`. Only the attach contract removes
the second node.

No out-of-node refresh path exists inside router.ctg — `mod auth;` is
crate-private (`lib.rs:9`), `Auth::from_path` has one call site (`service.rs:51`)
reachable only from the Lua entry, and there is no binary — so the PRD's
file-lock branch is not triggered and the spec adds none.

**Box 2 was narrowed but not delegated, and that distinction is the point.**
Memory's equivalent box could be delegated because a writer lock refuses a second
holder; a token is simply spent by whoever POSTs it. Two spenders remain outside
every composition — the `codex` CLI on `~/.codex/auth.json` and the `claude` CLI
on the keychain entry — and no board PRD can reach them. `auth.rs:365-377`
already concedes this in prose. Claiming "no refresh code path runs outside the
daemon's router node" would therefore have been false, so the box now claims only
what router.ctg can enforce about itself.

Two coordinator edits: the footprint gained `.cartridge/tests/unit/auth/tests.rs`
(already wired in by `#[cfg(test)] #[path]` at `src/auth.rs:1238-1239`, and the
only file besides `src/auth.rs` the spec changes, so collect would have refused
it), and both acceptance boxes were replaced with the analyst's proposed wordings
verbatim.

Residual, outside this repo: `.cartridge/config.lua:59` is what keeps the double
spend reachable at all. It belongs to the attach sibling or the composed test,
not here.

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, after round 2 (PASS 97) and verifier-1.

Box 1 is proven by execution: one POST to the token endpoint across two
concurrent callers (`tests.rs:225`), both callers' `authorization` equal to
`Bearer <rotated>` and to each other (`:233`, `:238`), and the stored refresh
token rotated once (`:242`). The audit's own shape — each caller given its own
gate, simulating two processes — fails `left: 2 / right: 1`.

Box 2 is a **structural** claim and is proven leg by leg, re-measured
independently: `mod auth;` private (`lib.rs:9`), one `Auth::from_path`
(`service.rs:51`), one `service::start(` caller in the Lua entry
(`module.rs:26`), no `src/bin`, `crate-type = ["cdylib","rlib"]`.

The security property behind the test seam was proven, not inferred: injecting
`compile_error!` into the `#[cfg(test)]` body gives `cargo build` exit 0 and
`cargo test --lib --no-run` exit 101, so the test endpoint cannot exist in a
shipped build. A whole-crate sweep found the five remaining env reads and
confirmed none reaches the token endpoint; there is no `set_var` anywhere.

The guard protecting that property was itself weak once, and the record should
keep it: round 2 showed the guards pinned the env variable's *name*, so
rewriting the shipped half as `std::env::var("ROUTER_TOKEN_ENDPOINT")
.unwrap_or_else(|_| CODEX_TOKEN.to_owned())` restored the full original
capability while every guard passed — `CODEX_TOKEN.to_owned()` survived as a
substring. The anchored `grep -qx` closes it, and the verifier reproduced both
directions. It also found a second, independent gate the implementer had not
claimed: `cargo fmt --check` fails the one-line-body variant because rustfmt
reflows it.

Two non-blocking observations recorded rather than fixed, both pre-existing and
outside what either box claims: the test leaks its scratch directory on failure,
and `reqwest::Client::builder()` (`auth.rs:169`) omits `.no_proxy()`, so
`HTTPS_PROXY` still applies to the refresh POST.
