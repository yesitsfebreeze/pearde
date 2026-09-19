---
state: "analyzing"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/memos/routine/quality.md"
  - ".cartridge/memos/routine/hygiene.md"
  - ".cartridge/memos/routine/improve.md"
  - ".cartridge/memos/routine/legible.md"
  - ".cartridge/memos/routine/self-improve.md"
  - ".cartridge/memos/routine/new-routine.md"
  - ".cartridge/memos/routine/distill.md"
claim: "coordinator-5c-5 2026-09-19T12:28:35.279Z"
---

# The record's routines run in this repository

## Outcome

No routine in `.cartridge/memos/routine/` tells the reader to use `memos/SYSTEM.md`,
`lanes-not-a-shared-tree`, `kern`, or `just lane`/`just land`. A routine with no equivalent here is
deleted (git is the archive), and no memo wikilinks a routine that no longer exists.

## Acceptance

- [ ] No routine names the foreign layout (`memos/SYSTEM.md`, `lanes-not-a-shared-tree`, `kern` probes, `just lane`/`just land`).
- [ ] No memo wikilinks a routine that no longer exists.

## Analysis

Split from `@root/the-shared-record-describes-only-this-repository` on 2026-09-19 by analyst-1 (coordinator-5c-3). No review rounds used before the split. Full analysis: `.state/loop/the-shared-record-describes-only-this-repository/analyst-1.md`.

Outcome: no routine in `.cartridge/memos/routine/` tells the reader to use `memos/SYSTEM.md`,
`lanes-not-a-shared-tree`, `kern`, or `just lane`/`just land`. A routine that has no equivalent
here is deleted (the no-legacy-retention rule: git is the archive).
Recommendation: delete `quality.md` and `hygiene.md` outright. Every probe in them runs `kern`
or reads `src/`, `memos/intake`, or `.kern/data`, and none of those exist here. Rewrite or delete
`improve.md`, `legible.md` and `self-improve.md` on the same test. Remove the `just lane` bullet
from `new-routine.md`. Repoint or drop the `[[quality]]`/`[[hygiene]]` links in `distill.md`,
`improve.md` and `legible.md`.
Footprint: `.cartridge/memos/routine/quality.md`, `.cartridge/memos/routine/hygiene.md`,
`.cartridge/memos/routine/improve.md`, `.cartridge/memos/routine/legible.md`,
`.cartridge/memos/routine/self-improve.md`, `.cartridge/memos/routine/new-routine.md`,
`.cartridge/memos/routine/distill.md` (all clean).
Out of scope, noted: `decision/the-trunk-checkout-is-a-landing-pad.md` records `just lane`/`just land` as
history of a decision. The child's analyst decides whether that decision is superseded.
Acceptance:
- [ ] No routine names the foreign layout.
- [ ] No memo wikilinks a routine that no longer exists.
Verify:
```sh
if grep -rEn 'memos/SYSTEM\.md|lanes-not-a-shared-tree|kern (report|health|doctor|compact|audit|repair)|just lan[de]' .cartridge/memos/routine; then exit 1; fi
for leaf in quality hygiene; do
  if [ ! -e ".cartridge/memos/routine/$leaf.md" ]; then
    if grep -rn "\[\[$leaf\]\]" .cartridge/memos; then exit 1; fi
  fi
done
```
