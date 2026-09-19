---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/fs.ctg"
work-kind: leaf
footprint:
  - "src/service.rs"
  - "src/provenance.rs"
---

# A read stamps the file it returned

## Outcome

A successful `tool.read` records the returned path against the calling session, so the session's
touched-file set holds files it has read and not only files it has written. That is the missing half
of `@sessions/file-drift-awareness`: a session can then be told that a file it read was changed on
disk by someone else.

## Evidence

Checked 2026-09-19 by coordinator cartridge-5c at fs.ctg fc8314e and sessions.ctg HEAD:

- `sessions.ctg/src/lib.rs:716` handles a `touch` op (`{id, file}`), inserting the file into the
  session's `files` set. Nothing in the composition sends it: the only match for `"touch"` in any
  `.rs`, `.ts` or `.lua` source is that handler.
- The only live populator of the set is `record_changes` (`sessions.ctg/src/lib.rs:715`,
  `changes::append`), which fs sends on the write side (`fs.ctg/src/lib.rs:91`,
  `fs.ctg/src/provenance.rs:108`). The read path sends nothing.
- Requested by cartridge-78 for `@sessions/file-drift-awareness`, whose analyst and reviewer found the
  drift feature inert without this. The footprint is the analyst's claim at second hand; the spec
  must confirm where the read success path lives before fixing it.
- Hazard: fs.ctg carries another session's uncommitted ASP work (cartridge-1f) in `src/lib.rs`,
  `src/files.rs`, `src/search.rs`, `cartridge.json` and `init.lua`. Keep the footprint off those
  paths, or coordinate with 1f before collect.

## Acceptance

- [ ] After a successful `tool.read` of a path, the calling session's touched-file set contains that
      path, proven by an executed test.
- [ ] A failed or refused read stamps nothing.
- [ ] A read with no session in context stamps nothing and still succeeds.
