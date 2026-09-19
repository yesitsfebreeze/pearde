---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/memos/routine/check-cartridge-isolation.md"
needs:
  - "the-isolation-gate-reads-the-composition-profile/prd-declares-the-memory-call-it-makes"
---

# The isolation gate measures events and the profile's config

## Outcome

`just isolation` checks the rule against what the host actually loads: keys a
cartridge provides are its manifest `events`, its declared keys are its
`needs` (optional `?` needs included, `${config.X}` needs resolved from the
root profile entry's `config` or the manifest setting's default), and the
profile is `.cartridge/init.lua` at the repository root.

## Evidence

Split from `@root/the-isolation-gate-reads-the-composition-profile` on 2026-09-19 by analyst-1 (coordinator-5c-2). No review rounds used before the split. The parent's box 4 (vision.md) is left to `@root/the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition`. Full analysis, working gate patch and fixture: `.state/loop/the-isolation-gate-reads-the-composition-profile/` (analyst-1.md, analyst-1-gate.diff, analyst-1-verify.sh).

At 801aa8e the key half of the gate checks nothing: it builds the owner map
from `m.provide`, and no manifest has a `provide` field (the host's
`Cartridge` struct, `cartridge.ctg/src/loader/document.rs`, has `events`, and
`deny_unknown_fields`). It reads the profile from
`cartridge.ctg/.cartridge/init.lua` (`return {}`) and looks for `inject =`,
which the host's profile `Entry` (`cartridge.ctg/src/loader/mod.rs`: id, path,
config, disabled) no longer has; the live equivalent is `config` resolving
`${config.X}` needs (`cartridge.ctg/src/host/plan.rs`, `configured`). It also
does not strip `?` from optional needs.

## Acceptance

- [ ] The routine reads the profile at `.cartridge/init.lua` (repository root)
      and credits a cartridge with each `${config.X}` need resolved from its
      entry's `config`, falling back to the manifest setting's default.
- [ ] Provided keys come from manifest `events`; optional `?` needs count as
      declared.
- [ ] A fixture composition proves it by execution: a profile-configured and an
      optional need pass; an undeclared key fails with
      `<consumer>: <file>:<line> names <key> (provided by <owner>)`; the same
      need without the profile's config fails. The fixture fails on the gate
      at 801aa8e.
- [ ] `just isolation` exits 0 on the composition (18 cartridges at 801aa8e).

Footprint: `.cartridge/memos/routine/check-cartridge-isolation.md` only. Draft
Verify and a working patch: analyst-1.md and scratchpad `gate.diff`.
