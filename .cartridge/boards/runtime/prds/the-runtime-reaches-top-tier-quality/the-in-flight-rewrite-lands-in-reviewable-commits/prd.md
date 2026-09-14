---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# The in-flight rewrite lands in reviewable commits

## Outcome

The working tree of `cartridge.ctg` is committed. On 2026-09-14 it carried 56 modified files, about 2200 changed lines, four untracked source modules (`src/evidence.rs`, `src/fabric.rs`, `src/graph.rs`, `src/settings.rs`), the rename of `src/turn.rs` to `src/trace.rs` and of `landscape` to `fabric`, deleted profile directories, and new tests. None of it is reviewable or bisectable while uncommitted, and every other child of this container would diff against a moving base.

## Acceptance

- [ ] `git status --porcelain` in `cartridge.ctg` is empty apart from ignored paths.
- [ ] The rewrite is split into commits that each build and pass `just check runtime`: at minimum, the rename commits, the settings layer, the fabric/graph/evidence modules, and the profile collapse.
- [ ] Each commit message states what changed and why in normal prose; no commit mixes a rename with a behavior change.
- [ ] `docs/` and `.cartridge/README.md` changes travel with the code they describe.

## Proof and recovery

Start with `git diff --stat` and `git status --short`. Use `git add -p` to separate concerns. Do not rewrite already-pushed history. If a split cannot build on its own, note the dependency in the commit message rather than squashing everything.
