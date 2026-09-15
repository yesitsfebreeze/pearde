---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: passed
needs:
- "@runtime/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits"
---

# Dependencies are released and current

## Outcome

`cartridge.ctg/Cargo.toml` pins released versions on the current edition and builds with the lints mature Rust projects keep on. On both `origin/main` `ba198f4` and local `e8a4da3`:

- `notify = "9.0.0-rc.5"` is a release candidate. The local registry cache also holds `8.2.0`.
- `edition = "2021"` with `rust-version = "1.89"`, although edition 2024 is supported by that toolchain.
- `[lints.rust] warnings = "deny"` is set, but there is no `[lints.clippy]`, so `pedantic` findings are invisible.
- No dependency policy check runs; `cargo-deny 0.20.2` and `cargo-machete 0.9.2` are installed locally.
- `sha2` exists only on local `main` (trust store) and is unused on `origin/main`.

## Acceptance

- [ ] `notify` pins a released 9.x if published, otherwise `8.2`. No unit test covers `src/host/watch.rs` today, so a new test in `.cartridge/tests/unit/src/tests/host.rs` proves that `Host::watch` restarts a cartridge whose source changed, both before and after the bump.
- [ ] `edition = "2024"`, with `cargo fix --edition` applied as its own commit.
- [ ] `[lints.clippy]` sets `pedantic = "warn"` with an explicit allow list and a one-line reason per allow.
- [ ] `cartridge.ctg/justfile` `check` runs `cargo deny check bans licenses sources` (offline) and `cargo machete`, both clean, and `just check runtime` passes from `/Users/feb/dev/cartridge`.

## Proof and recovery

Probe first on the reconciled head: `cargo tree -d`, `cargo machete` and `cargo deny check bans licenses sources` in `cartridge.ctg`. Record the output. Land the edition, the `notify` bump and the lints as three separate commits. If a released `notify` breaks the watcher, keep the rc pin and record why, and the other commits still land. `cargo deny check advisories` needs the network, so it stays out of the offline gate.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
