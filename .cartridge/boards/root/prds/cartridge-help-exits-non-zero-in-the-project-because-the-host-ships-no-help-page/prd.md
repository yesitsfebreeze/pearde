---
state: open
origin: requested
priority: 45
repo: "/Users/feb/dev/cartridge"
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/cli/manual.rs"
---

# cartridge help exits non-zero in the project because the host ships no help page

## Outcome

`cartridge help` run inside the project prints its overview and exits 0. A
cartridge that ships no `.cartridge/help.md` is reported as such without making
the whole command fail.

## Evidence

Found 2026-09-16 by the analyst of `@gitfs/gitfs-is-back-in-the-composition`
while writing a Verify block around the overview line.

`cartridge help` in `/Users/feb/dev/cartridge` prints the correct overview
(`19 cartridges enabled, 0 installed and not enabled`) and then exits **1**,
because the `host` cartridge ships no `.cartridge/help.md` and
`print_overview` returns the broken count (`cartridge.ctg/src/cli/manual.rs:345-355`).

The exit status is wrong, not the output. Any Verify block or script that gates
on `cartridge help` must currently tolerate a non-zero status and grep the text
instead, which is exactly the kind of "tolerate the failure" habit that hides a
real regression later.

Related observation, same investigation: `cartridge help` run from outside a
project (`/tmp`) exits 0 but reports `0 enabled, 9 installed and not enabled`
from the global-home fallback. That is arguably correct, but it means the exit
status says nothing about whether the command found the project.

## Acceptance

- [ ] `cartridge help` inside the project exits 0 and still prints the enabled
      and not-enabled counts.
- [ ] A cartridge with no `.cartridge/help.md` is still reported in the
      overview, with no change to the counts.
- [ ] A genuine failure (an unreadable or malformed help page) still exits
      non-zero, so the status stays meaningful.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed separately rather than folded into
the gitfs PRD: it is a `cartridge.ctg` CLI defect, outside that PRD's footprint
(`.gitmodules` and `.cartridge/init.lua`), and it predates today's work. Low
priority — the output is right and only the status is wrong — but it taxes every
spec that wants to assert something about the composition.
