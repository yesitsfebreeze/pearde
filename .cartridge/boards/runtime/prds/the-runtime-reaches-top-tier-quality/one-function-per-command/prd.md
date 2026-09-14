---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: passed
needs:
- "@runtime/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits"
---

# No host function outgrows eighty lines without a reason

## Outcome

`d2a761e` delivered the dispatcher half of the original outcome. `src/main.rs` is 8 lines, and each command lives in its own module under `src/cli/`. The audited long functions (`main`, `hosted_node`, `evidence::collect`, `socket::client`, `cartridge::handle`) are deleted. The size problem moved into the rewrite. Functions over 80 lines (origin `ba198f4` / local `e8a4da3`):

| Function | origin | local |
| --- | ---: | ---: |
| `src/node.rs` `install` | 192 | 148 |
| `src/host/process.rs` `start` | 139 | 139 |
| `src/cli/setup.rs` `run_setups` | 107 | 108 |
| `src/sandbox.rs` `profile` | 104 | 104 |
| `src/cli/setup.rs` `setup` | 94 | 94 |
| `src/transport/rpc.rs` `Peer::spawn` | 84 | 87 |
| `src/node.rs` `spawn` | 82 | — |
| `src/transport/cartridge.rs` `connection` | — | 87 |
| `src/transport/cartridge.rs` `handle` | — | 85 |

## Acceptance

- [ ] With `too-many-lines-threshold = 80` in `cartridge.ctg/clippy.toml`, `cargo clippy --all-targets -- -W clippy::too_many_lines` reports nothing. The only exceptions carry `#[allow(clippy::too_many_lines)]` with a one-line reason.
- [ ] `node::install` is split so that each `cartridge.*` family is installed by its own function. `host::process::start` is split into spawn, wait-until-serving, apply and monitor.
- [ ] `src/main.rs` stays a one-call entry point, and every `Command` arm in `src/cli/mod.rs` still calls a single function.
- [ ] `just test runtime` passes from `/Users/feb/dev/cartridge` with the same test count before and after.

## Proof and recovery

First run the clippy command on the reconciled head and record the list, because line counts differ between the two lines today. Each split is its own behavior-free commit and can be reverted alone. Do not split a function whose reason to stay whole is a single lock or a single `select!`. Mark it allowed instead.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
