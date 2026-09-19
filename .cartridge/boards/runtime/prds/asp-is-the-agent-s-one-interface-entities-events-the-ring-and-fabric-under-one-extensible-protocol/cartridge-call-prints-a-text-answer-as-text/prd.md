---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/client.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
commit: "d03409e6c9fc8aaf6f0da18f0aefed0614a17fd3"
---

# cartridge call prints a text answer as text

## Outcome

`cartridge call` prints a string answer as plain text rather than as a quoted JSON string, so `cartridge call asp '{"op":"search","query":"...","format":"text"}'` reads as one line per hit with no `jq -r` in between. Every other answer still prints as JSON. No script in the workspace parses a string answer of `cartridge call` (searched on 2026-09-19).

## Acceptance

- [x] A string answer prints unquoted; an object answer prints as JSON (verified live against the daemon with the built binary).
- [x] `docs/transport.txt` says so.
