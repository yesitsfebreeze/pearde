---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: needs-decision
---

# The shipped policy defaults to ask

## Outcome

A fresh composition does not run shell commands or write files on a model's say-so without a decision recorded somewhere. `.cartridge/config.lua` ships `policy.default = "allow"` with `shell`, `write`, `edit`, `gitfs`, and `ship` explicitly allowed, and the comment explains that approval is delegated to the client. That is the right posture for one developer's machine and the wrong default for a file that every command reads and new users copy.

## Acceptance

- [ ] `.cartridge/config.lua` ships `default = "ask"` with read-only tools (`read`, `glob`, `grep`, `search`, `docs`, `memo`, `memory`, `sessions`, `prd`) allowed and mutating tools left to the default.
- [ ] A developer who wants the permissive posture sets it in `~/.cartridge/config.lua`; `docs/settings.txt` shows the exact snippet.
- [ ] `cartridge settings policy` prints which file settled each tool's rule, so the permissive override is visible.
- [ ] The MCP and proxy entry points surface an `ask` decision to the client as they do today; a smoke test proves one `ask` round trip on `shell`.
