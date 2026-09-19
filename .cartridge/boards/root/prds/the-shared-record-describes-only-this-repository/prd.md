---
state: "open"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
footprint:
  - ".cartridge/memos/routine/quality.md"
  - ".cartridge/memos/routine/hygiene.md"
  - ".cartridge/memos/system/vision.md"
  - ".cartridge/memos/decision"
---

# The shared record describes only this repository

## Outcome

Every memo in the shared record describes this repository. A routine an agent
resolves here runs here, and a link in the record resolves to a file that
exists.

## Evidence

Measured 2026-09-17.

**Two routines describe a different project.** `routine/quality.md` and
`routine/hygiene.md` both instruct the reader to start from `memos/SYSTEM.md`,
treat `memos/` as its own repository shared by every lane, and follow
`lanes-not-a-shared-tree`. None of those exist here: the record lives at
`.cartridge/memos/`, there is no `SYSTEM.md`, and lanes are the PRD engine's
worktrees. An agent that resolves either routine is handed instructions for a
layout this repository does not have.

**Two links in the decision record are dead.** Of twenty PRD links across
`memos/decision/`, eighteen resolve. The two that do not both point at a `ui`
board that no longer exists:
`prd.ctg/.cartridge/boards/ui/prds/copy-mode-interacts-with-the-text/prd.md` and
`prd.ctg/.cartridge/boards/ui/prds/the-gutter-is-the-boundary/prd.md`. Both are
consistent with `tui.ctg` having been deleted.

**The vision memo's own measurements have drifted.** `system/vision.md` is the
authority on intent, and its "Where the composition actually stands" section is
stale on three counts: it reports the profile entries `live-record` and
`live-mcp` naming directories that do not exist, but the root profile no longer
declares either; it reports `cartridge help` finding three cartridges with no
readable page, but all seventeen ship a `.cartridge/help.md`; and it reports
sixteen of seventeen audit findings as the missing README, where `just audit`
now reports seventeen of seventeen.

## Acceptance

- [ ] `quality.md` and `hygiene.md` each describe this repository's layout and
      commands, or are deleted — git is the archive, and a routine nobody can
      run is worse than no routine.
- [ ] Every PRD link under `memos/decision/` resolves to a file that exists, or
      the reference is removed with the reason recorded.
- [ ] The vision memo's "Where the composition actually stands" section states
      what `just audit`, `just isolation` and the root profile report on the day
      it is rewritten, with the date and the commands in the section.
- [ ] A check that a link in the record resolves runs next to the other gates,
      so this cannot drift again silently.
