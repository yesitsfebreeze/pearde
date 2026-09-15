---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 4
date: "2026-09-15"
footprint:
- "README.md"
- "justfile"
- "cartridge.ctg setup/doctor"
- ".mcp.json"
needs:
- the-repository-answers-by-text
---

# A fresh checkout runs the daemon and the gates

## Outcome

Anyone with the toolchains can clone, build, gate and serve without inherited state.

## Acceptance

- [ ] `git clone --recurse-submodules` into a temp dir, then `just install && just check && just test && just daemon` succeed with no `builtin/`, no memory store and no trunk symlink.
- [ ] `cartridge doctor` names every missing toolchain by name and version, tmux included.

## Folds

Deferred with `superseded-by` pointing here:

- @root/fresh-checkouts-can-run-the-gates
- @runtime/development-clean-checkout

## Result

Not started.
