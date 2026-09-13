---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: ci-proves-the-supported-terminal-matrix
---

# Repository CI runs the gates and reports terminal coverage explicitly

Replace the ignored builtin/memory bootstrap with recursive checkout of the current recorded submodules. Use explicit Linux/macOS jobs with Bash/Zsh/Neovim prerequisites and the current root forwarding gates. Pin action/tool inputs in the eventual CI spec; report kernel/shell/toolchain identities. A deliberate failing fixture must fail the full selected gate, not only an isolated test command.

## Acceptance

- [ ] Both supported host jobs initialize the same pinned composed revision and run the declared checks; absent required tools fail clearly and optional shells are counted as skips.
- [ ] Inject a failing test into a disposable checkout and assert the top-level gate returns nonzero and removes only that fixture.
- [ ] No kern archive/pin/bootstrap patch is fetched, and a clean job cannot obtain a sibling lane's artifacts from a shared target/cache.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [fresh-checkouts-can-run-the-gates](../../../../memos/work/root--fresh-checkouts-can-run-the-gates.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `ci-proves-the-supported-terminal-matrix`; maximum five rounds.
