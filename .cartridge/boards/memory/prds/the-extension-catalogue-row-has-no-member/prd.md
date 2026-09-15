---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "0.5h"
---

# `7b4df428` added `extension` to `[workspace.dependencies]` while no member inherits it, and `declared_dependencies::the_workspace_catalogue_lists_nothing_no_member_inherits` is red on main because of it

[extension-context-and-fiber](../extension-context-and-fiber/prd.md) landed `src/extension` as a workspace member and
wrote `extension = { path = "src/extension" }` into `[workspace.dependencies]` the
memo's `Do` asked for. Nothing depends on it yet — the crate is L0 and its
consumers are later children — so the catalogue carries a row no member
inherits, which the gate
`declared_dependencies::the_workspace_catalogue_lists_nothing_no_member_inherits`
exists to forbid. Found by [memory-mcp-never-answers-initialize](../memory-mcp-never-answers-initialize/prd.md)'s lane, which
reproduced it with its own two files reverted, so the red is this row and not
that lane.

## Do

Take the `extension` row out of `[workspace.dependencies]` and leave `src/extension`
in `members`. The row goes back the day a member writes
`compose.workspace = true`, which is the gate's whole point: the catalogue lists
what is inherited, not what exists. Do not satisfy the gate by giving a crate a
dependency it does not use.

## Acceptance
`cargo test --test declared_dependencies` is green from a fresh lane,
`cargo build -p extension` still builds, and `rg -n '^compose' Cargo.toml` shows
the member and no catalogue row.

The row is gone and `src/extension` stays in `members`. The three tests of
`cargo test --test declared_dependencies` pass from the lane, `cargo build -p
extension` finishes, and `rg -n 'compose' Cargo.toml` prints the `members` line
alone — the literal `^compose` of the `Check` now matches nothing, which is the
same fact said the other way.
