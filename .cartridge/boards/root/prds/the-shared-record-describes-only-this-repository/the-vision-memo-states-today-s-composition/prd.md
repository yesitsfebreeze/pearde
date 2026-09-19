---
state: "done"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/memos/system/vision.md"
needs:
  - "the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository"
  - "the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so"
commit: "f5ec10d4580061e8a472af629a991fa653015f5b"
---

# The vision memo states today's composition

## Outcome

The "Where the composition actually stands" section of `system/vision.md` is re-measured on the day
it is written, names its date and commands (`just audit`, `just isolation`, the root
`.cartridge/init.lua`), and drops the claims the sibling children made false. It shares
`system/vision.md` with `the-isolation-gate-reads-the-composition-profile`, so the two land one after the other.

## Acceptance

- [x] The section names `just audit`, `just isolation` and `.cartridge/init.lua`, and carries a measurement date after 2026-09-16.
- [x] It no longer claims `live-record`/`live-mcp` profile entries, missing help pages, or foreign routines.

## Analysis

Split from `@root/the-shared-record-describes-only-this-repository` on 2026-09-19 by analyst-1 (coordinator-5c-3). No review rounds used before the split. Full analysis: `.state/loop/the-shared-record-describes-only-this-repository/analyst-1.md`.

Outcome: the "Where the composition actually stands" section of `system/vision.md` is re-measured
on the day it is written. It gives the date and the commands (`just audit`, `just isolation`, the root
`.cartridge/init.lua`) and drops the claims A and B made false.
Today's numbers, to re-measure on the day: `just audit` exit 0, 18 of 18 cartridges pass the hard
checks. The soft findings are stray root entries in memo.ctg (2) and memory.ctg (6). `just isolation`
exit 0, 18 cartridges. The root profile has 18 path entries, with no `live-record`/`live-mcp`. All 19
`*.ctg` ship `.cartridge/help.md` and `README.md`. memory.ctg has 40,778 source lines and prd.ctg has
4,462 tracked files. The isolation gate still reads `cartridge.ctg/.cartridge/init.lua`. Unless
@root/the-isolation-gate-reads-the-composition-profile has landed first, that bullet stays, re-dated.
Footprint: `.cartridge/memos/system/vision.md` (clean). Shared with the isolation-gate PRD, so the
two integrate one after the other.
Acceptance:
- [x] The section names `just audit`, `just isolation` and `.cartridge/init.lua`, and carries a measurement date after 2026-09-16.
- [x] It no longer claims `live-record`/`live-mcp` profile entries, missing help pages, or foreign routines.
Verify:
```sh
s=$(sed -n '/^## Where the composition actually stands/,/^## Where this is going/p' .cartridge/memos/system/vision.md)
for t in 'just audit' 'just isolation' '.cartridge/init.lua'; do
  if ! printf '%s\n' "$s" | grep -qF "$t"; then echo "section lacks a named measurement command"; exit 1; fi
done
d=$(printf '%s\n' "$s" | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' | sort | tail -1)
if [ -z "$d" ]; then echo "no date"; exit 1; fi
if [ "$d" \< "2026-09-17" ]; then echo "stale date"; exit 1; fi
if printf '%s\n' "$s" | grep -nE 'live-record|live-mcp|quality\.md|hygiene\.md'; then exit 1; fi
```
