---
state: "done"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge"
footprint:
- ".cartridge/tests/integration/smoke.test.ts"
needs:
- "cartridge-mcp-waits-for-a-cold-host-to-settle-instead-of-giving-up-after-three-identical-polls"
commit: "b7103e36c5a7ce9e45a3c844b6823a5d3efa0f84"
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

- [x] The smoke fixture no longer pre-starts a daemon before `cartridge mcp`,
      and every case in `.cartridge/tests/integration/smoke.test.ts` passes, the
      cold `mcp` case ten times in a row.
- [x] The comment naming the cold-host PRD is removed with the workaround.
- [x] Not gated: with the cold-host fix reverted, a cold `mcp` run fails about 1
      time in 5 (recorded: 2 of 12). The suite's cold runs catch such a revert
      about 91% of the time. This box is ticked from the recorded run in the
      spec plus the diff reviewer.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed separately on the analyst's own
recommendation rather than folded into the cold-host PRD: that PRD's footprint is
`cartridge.ctg` plus one file inside it, and it must collect with **no lane**
because a superproject lane worktree leaves submodules empty. Adding a
superproject path such as `.cartridge/tests/integration/smoke.test.ts` to its
footprint would break that landing shape. `needs` points at the cold-host PRD, so
this row cannot start before the fix it depends on.

## Scope note (2026-09-19, coordinator cartridge-5c)

Box 1 no longer says `just smoke` passes: `just smoke` also runs mcp.ctg's own
`.cartridge/tests/integration/refresh.test.ts`, which fails at `:93` (expects the tool list `['alpha']`,
gets `["alpha","asp"]`) since the ASP commits in cartridge.ctg. That is mcp's defect, owned by
`@mcp/the-mcp-refresh-test-expects-the-host-s-synthetic-asp-tool`, not this footprint's. Box 3 is a race that fails about one run in five with the
fix reverted, so a Verify gate cannot prove it; it rests on the recorded run and the diff reviewer
(analyst-1.md in the loop dir).

