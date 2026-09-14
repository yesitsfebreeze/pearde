---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: delivered-pending-verification
---

# The documents describe this checkout

## Outcome

Every path, command, count, and dependency named in `llms.txt`, `docs/*.txt`, and `.cartridge/README.md` exists in the checkout that ships them, and a test keeps it that way.

## Findings to close

- `docs/architecture.txt:15-19` names `scripts/`, `scripts/workspace.py`, `workspace/Cargo.toml`, and "13 Rust cartridge packages". None exist; the workspace is `.cartridge/workspace/Cargo.toml` with 12 members.
- `docs/architecture.txt:181` lists a `ui` cartridge; `builtin/` has `tui`. The INSTALLED CARTRIDGES list omits `auth`, `docs`, `live`, `prd`, `tui`.
- `docs/architecture.txt` describes "default, mcp, proxy, and tools profiles"; the profiles were collapsed into one `.cartridge/init.lua` in the current tree.
- `docs/development.txt:4` requires Python 3.9+; `.cartridge/memos/routine/cartridge-development.md` says there is no Python dependency. `docs/development.txt:43` again names `scripts/workspace.py`.
- `docs/development.txt` documents `just isolation`, `just layout`, `just describe fabric`; the first two live in the parent repository's justfile, not this one.
- `.cartridge/README.md` says host keys are declared in `src/settings.rs`; `llms.txt` and `docs/architecture.txt` say `settings.json`. One is right.
- `docs/creating-cartridges.txt:76` describes a `ui` manifest field pointing to a JS module; verify against `src/loader.rs`.

## Acceptance

- [ ] Every finding above is corrected or the code is changed to match the document, with the choice recorded.
- [ ] A test in `.cartridge/tests/integration/` extracts every relative path and `just <recipe>` from `llms.txt`, `docs/*.txt`, and `.cartridge/README.md` and asserts each resolves in this checkout or in the parent justfile.
- [ ] The INSTALLED CARTRIDGES list is generated from `cartridge help --json` or removed in favor of pointing at it.
