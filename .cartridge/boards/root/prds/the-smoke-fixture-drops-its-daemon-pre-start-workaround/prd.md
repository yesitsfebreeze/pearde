---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
footprint:
- ".cartridge/tests/integration/smoke.test.ts"
needs:
- "cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls"
---

# the smoke fixture drops its daemon pre-start workaround

## Outcome

`.cartridge/tests/integration/smoke.test.ts` exercises the cold path it was
written for: it no longer starts the daemon itself before running `cartridge
mcp`, because `cartridge mcp` waits for a cold host on its own.

## Evidence

Found 2026-09-16 by the analyst of
`@root/cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls`.

That PRD's defect — `settle_remote` ending the wait after three identical status
polls while cartridges are still starting — made the first `cartridge mcp` of a
fresh project fail 5 times out of 5. The smoke fixture works around it by
pre-starting the daemon, and the workaround names that PRD in a comment.

Once the wait is fixed, the workaround is not merely redundant: it means the
smoke suite never exercises a genuinely cold start, so a regression of the same
defect would not be caught there.

## Acceptance

- [ ] The smoke fixture no longer pre-starts a daemon before `cartridge mcp`,
      and `just smoke` passes.
- [ ] The comment naming the cold-host PRD is removed with the workaround.
- [ ] Reverting the cold-host fix makes this suite fail, so the cold path is
      genuinely covered here.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed separately on the analyst's own
recommendation rather than folded into the cold-host PRD: that PRD's footprint is
`cartridge.ctg` plus one file inside it, and it must collect with **no lane**
because a superproject lane worktree leaves submodules empty. Adding a
superproject path such as `.cartridge/tests/integration/smoke.test.ts` to its
footprint would break that landing shape. `needs` points at the cold-host PRD, so
this row cannot start before the fix it depends on.
