---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
capability-owner: root
wave: 2
date: "2026-09-15"
needs:
- "@proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger"
- "@root/one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it"
footprint:
- ".cartridge/config.lua"
- ".cartridge/init.lua"
- ".cartridge/memos/decision/"
---

# Every exchange reaches the memory ledger and condenses on the one daemon

## Outcome

Every composed cartridge runs, memory included. The user decided this on
2026-09-15, reversing the "nothing that recalls" part of
`the-profile-is-the-orchestration-service`. Every model exchange through the
proxy lands in memory's ledger (`@memory/the-exchange-ledger-…`, done), and the
one project daemon condenses it per UTC day, week, month and year with
`glm-5.3-flash:cloud`.

State on 2026-09-15:

- memory is in `.cartridge/init.lua`, and `config.lua` sets its reason model
  and `ledger.chunk_bytes = 64000`. Neither is committed.
- The legacy `ledger.jsonl` is fully imported: 7,234 exchanges, 85.7 MB of
  raw text, one day record condensed.
- The proxy hand-off is implemented in its lane (proxy `f77ed64`, claimed).
  Collection is blocked by another session's uncommitted `yolo` edits to the
  same proxy.ctg files.

## Acceptance

- [ ] A decision memo records that every composed cartridge runs, memory
      included, and supersedes the recall half of
      `the-surface-is-the-orchestrators-doors`' consequences.
- [ ] `@proxy/the-proxy-hands-each-finished-exchange-to-the-memory-ledger` is
      collected, and `proxy.ledger = "memory"` is set in `config.lua`.
- [ ] With the daemon running, one proxied request adds one `raw/` row
      (`cartridge call memory '{"op":"ledger","action":"status"}'`), and after
      five quiet minutes a pass closes Sep 6–9 into day records, then weeks.
- [ ] `.cartridge/memory/data.mdb` shows `ledger/day/…` thoughts in the graph
      (`memory query` with source prefix `ledger/`).
