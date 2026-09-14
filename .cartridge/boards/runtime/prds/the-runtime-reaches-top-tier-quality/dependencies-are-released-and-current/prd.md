---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# Dependencies are released and current

## Outcome

`Cargo.toml` pins released versions on the current edition, and the crate builds with the lints that top-tier Rust projects keep on.

## Findings to close

- `notify = "9.0.0-rc.5"` is a release candidate in a production dependency list.
- `edition = "2021"` with `rust-version = "1.89"`; edition 2024 is available for that toolchain.
- `[lints.rust] warnings = "deny"` is set but no `[lints.clippy]` group; `pedantic` findings are not visible.
- `thiserror` is declared and used in one file (see `failures-carry-a-type`); `sha2` is used in two.

## Acceptance

- [ ] `notify` on a released 9.x or the latest stable 8.x, with the watcher tests passing.
- [ ] `edition = "2024"` with `cargo fix --edition` applied and reviewed.
- [ ] `[lints.clippy]` enables `pedantic = "warn"` with an explicit allow list and a one-line reason per allow; `just check runtime` stays green.
- [ ] `cargo deny check` or `cargo audit` runs in `just check runtime` and passes.
- [ ] Every dependency in `Cargo.toml` is used in more than a trivial way or removed.
