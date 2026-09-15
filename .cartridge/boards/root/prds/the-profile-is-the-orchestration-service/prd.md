---
state: "done"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- ".cartridge/init.lua"
- ".cartridge/config.lua"
- ".gitmodules"
- "tui.ctg"
- ".cartridge/justfile"
- ".cartridge/memos/routine/cartridge-runtime.md"
- "live.ctg/src/launch.ts"
- "live.ctg/cartridge.json"
- ".cartridge/memos/decision/"
commit: "6ee17d9e8ad35d7525e4fae4cbcb40f9f61988ce"
---

# The profile is the orchestration service

## Outcome

The host runs one composition whose surface is the orchestrator's doors (text, MCP, voice). tui.ctg is deleted, memory.ctg leaves the profile untouched, and the profile starts with nothing that paints or recalls.

## Acceptance

- [x] `git submodule deinit -f tui.ctg && git rm tui.ctg` is committed; `rg -n 'tui\.ctg|run tui' --glob '!*.git*'` over the composed repo is empty except git history.
- [x] `.cartridge/init.lua` has no `tui` and no `memory` entry; `live.ctg` `needs` drops `memory`; harness config `memory = ""`; `cartridge settings` exits 0 with no `undeclared` key.
- [x] `just daemon` starts the host and `cartridge call live '{"op":"status"}'` answers `running` with no memory daemon on the machine; harness `ring` reports `disabled`.
- [x] One decision memo supersedes `the-agent-surface-preserves-the-visible-shell`, the UI half of `the-terminal-grid-lives-in-pty` and `desktop-is-a-later-client-over-the-same-core`: the surface is the orchestrator's doors; a UI attaches later over the same host.

## Folds

Deferred with `superseded-by` pointing here:

- @root/terminal-profile-starts-only-needed-services
- @root/the-terminal-is-drawn-from-pty
- @root/pty-encodes-input
- @root/the-sidebar-slides-over-the-shell
- @root/the-palette-and-exit
- @root/the-context-inspector-opens-from-the-chat-editor
- the whole `ui` board

## Result

2026-09-15, worked from the coordinator session, not yet collected.

- tui.ctg: last local state committed in its own history as `96bd624`; removed from the index and `.gitmodules`; work tree deleted. `/Users/feb/dev/cartridge-worktrees/ws/tui.ctg` (branch `transport`) still exists outside this repo and is left alone.
- `.cartridge/init.lua`: `tui` and `memory` entries removed; harness config no longer names `memory`. `live.ctg/cartridge.json` `needs` drops `memory`. `.cartridge/justfile` and `routine/cartridge-runtime.md` drop `tui` and `solo`; `routine/cartridge-development.md` drops `tui` from its owner lists; `live.ctg/src/launch.ts` no longer attaches a terminal.
- `cartridge trust` re-recorded 48 files; `cartridge settings` exits 0 with no `undeclared` key; `just isolation`: "Isolation passed for 17 cartridges."
- Decision `the-surface-is-the-orchestrators-doors` written and read back through `memo read`; `the-agent-surface-preserves-the-visible-shell`, `desktop-is-a-later-client-over-the-same-core`, `tui-and-tools-are-cartridges` marked superseded; `note/terminal-design-record.md` deleted.
- Since observed, later the same day, by the coordinator. Neither of those hosts was serving: 59778 and 92897 were both gone, and 62849 is an old release daemon on a different socket scheme that this binary never looks at. The current project socket held only a stale file left by a dead runtime. Clearing it and starting a host revealed the real blocker, which was not a host at all.
- `rg -n .tui\\.ctg|run tui.` over the composed repo: only git history and deferred board records mention it.
