---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
---

# Memory tool refuses reads while a live writer holds the bank; attach instead.

cartridge_memory query fails with "another memory writer holds this data dir
(cartridge memory pid 72544)". A live memory_cartridge process owns the store,
but the tool opens the data dir in Local mode and is refused on the exclusive
writer lock instead of connecting to the running writer. A running writer
should be an invitation to attach, not a wall.

The design already intends attachment: memory.ctg/cartridge.json declares
settings.owner = {endpoint, timeout_ms} — "Attach to another host's bank instead
of opening one… naming its local socket". transport/owner.rs provides
read_observed (read-only, validates the owner's identity against the configured
store); transport/typed.rs Endpoint::memory() derives the socket path
(/tmp/memory-<tag>-<user>.sock). But ServiceConfig is Local when no owner is
set, and Local open errors on a held lock.

## Outcome

cartridge_memory query returns recalled facts while a live writer holds the
bank, without erroring on the lock — by attaching to (or otherwise routing
through) the running writer rather than fighting it for the file.

## Acceptance

- [ ] With a live memory_cartridge holding the bank, cartridge_memory query
      returns matching facts instead of the writer-lock error.
- [ ] When no live writer holds the bank, reads still work through the local
      path as today (no regression).
- [ ] The attached path validates the owner's identity (same store dir) before
      serving; a mismatched owner is refused, not silently read.
- [ ] The running writer actually serves its socket (currently pid 72544 binds
      none), so attach has an endpoint to reach; confirm the writer runs a
      serve surface or make the tool discover/bind it.
- [ ] Writes (ingest) remain correct and non-conflicting under a live writer.

## Proof and recovery

Decide between (a) auto-attach: when Local open hits Availability::Held, derive
Endpoint::memory() for the pinned root and route reads through transport::owner;
(b) wiring tool.memory with owner pointing at a shared writer. Confirm which
surface the live writer serves before choosing. Start at memory.ctg/src/cartridge.rs
(ServiceConfig decision) and transport/src/owner.rs.
