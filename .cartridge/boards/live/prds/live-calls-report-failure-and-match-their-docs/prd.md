---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/live.ctg"
footprint: ["src/control.ts", "mcp/**", ".cartridge/help.md", ".cartridge/docs/README.md", "init.lua"]
---

# Live calls report failure and match their docs

## Outcome

A refused or failed `cartridge call live …` exits non-zero, and the `live`
tool's documented ops and fields match `src/control.ts`.

Observed 2026-09-16: `cartridge call live {op:"delegate", …}` refused with
"config.lua has changed since it was trusted" yet exited 0 and created no
task; help lists a `work` op the tool does not have and never names
`delegate`'s `prompt` field.

## Acceptance

- [ ] A trust refusal or runtime error from `cartridge call live` exits non-zero (fix at the host if the exit code is lost there, and record where).
- [ ] `live/.cartridge/help.md`, `live/mcp/.cartridge/help.md` and the README list exactly the ops in `control.ts` with their required fields.
