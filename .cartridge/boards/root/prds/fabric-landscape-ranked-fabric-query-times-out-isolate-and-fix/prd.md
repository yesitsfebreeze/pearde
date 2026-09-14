---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
---

# fabric/landscape Ranked fabric query times out; isolate and fix.

Calling cartridge_memo with op=landscape AND a query consistently hangs and is
cancelled after 600000ms (the MCP tools/call timeout). Plain landscape (no
query) returns fine, and op=resolve (usage+query over the same record) works.
So the ranked graph/entry query path — the intended "narrow the fabric to what
I need" entry point — is broken while the cheap paths are not.

## Outcome

A ranked fabric query returns scoped, relevant records (cartridges, tools,
memos) in normal latency instead of hanging until the MCP timeout.

## Acceptance

- [ ] Reproduce the 600000ms hang against a clean rebuild of memo_cartridge
      (cartridge_memo {op:"landscape", query:"…"}), confirm it is reproducible
      and not intermittent.
- [ ] Land/commit the landscape->fabric rename in the memo cartridge, which is
      currently uncommitted WIP, then retest.
- [ ] Isolate the hang: ranking projection, entry paging, or the announce
      gather. Compare against op=resolve which works.
- [ ] Ranked landscape returns within normal latency; confirm plain landscape
      (no query) and cursor paging still return.
- [ ] Assert the returned rows and node/edge counts match the live composition
      (the plain-landscape view) for the same profile.

## Proof and recovery

Start at the memo cartridge (memo.ctg) fabric/landscape source and the record's
landscape memo. If the hang is in the ranking query specifically, it shares a
path with op=resolve's working matcher — find the divergence.
