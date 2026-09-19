---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/mcp.ctg"
footprint:
- ".cartridge/tests/integration/refresh.test.ts"
---

# The mcp refresh test expects the host's synthetic asp tool

## Outcome

`just smoke` is green again. `refresh.test.ts` asserts on the tools this
cartridge's own live catalog contributes, and is not broken by the host adding
a tool of its own to every plan.

## Evidence

Reported 2026-09-19 by coordinator session cartridge-5c and confirmed here by
reading the code.

`mcp.ctg/.cartridge/tests/integration/refresh.test.ts:93` asserts

    expect((await listed()).map((tool: any) => tool.name)).toEqual(['alpha']);

The host now owns and serves a tool of its own: `cartridge.ctg/src/asp/mod.rs:31`
declares `pub const TOOL: &str = "tool.asp";` and `cartridge.ctg/src/asp/tool.rs`
implements it ("`tool.asp`: ASP as one of the agent's tools"). It arrived with
the ASP work landed today, from `cartridge.ctg` `804a08b` onward; HEAD at the
time of filing is `324f36e`. So `tools/list` now answers `["alpha","asp"]`
where the test demands exactly `['alpha']`.

cartridge-5c reports `env -u CARTRIDGE_YOLO just smoke` exiting 1 on every run,
alone and after the daemon was replaced in place, which rules out both the
inherited `CARTRIDGE_YOLO=1` and a restart straddling the run as the cause.
Independently, the analyst of
`@mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool`
reported `refresh.test.ts` failing **identically on its modified and unmodified
trees**, which places the cause outside that change as well.

No open PRD owned this at the time of filing. It keeps `just smoke` red for
every session on this machine, and a red shared gate is worse than the defect
itself: it trains every worker to discount a failing smoke run.

## Acceptance

- [ ] `refresh.test.ts` passes against a host that serves `tool.asp`, and its
      assertion states what it actually means — that the live catalog
      contributes `alpha` — rather than that `alpha` is the only tool in the
      world.
- [ ] The test still fails if this cartridge's live catalog stops contributing
      `alpha`, or contributes a second tool of its own. Pinning the assertion
      to a fixed two-element list would satisfy the first box while destroying
      this one, and is denied.
- [ ] `just smoke` exits 0, run both plain and under `env -u CARTRIDGE_YOLO`.

## Planning note

Filed by coordinator session cartridge-cc (`coordinator-41b7-*`) as an
out-of-scope defect found while landing other `@mcp` work, rather than widening
a running PRD's footprint to absorb it.

The analyst should decide, with evidence, whether the right fix is to filter
the host's own tools out of the assertion or to assert containment of `alpha`.
**The sibling search is already done, so do not repeat it.** I ran
`grep -rn 'toEqual(\[|toStrictEqual(\[' mcp.ctg/.cartridge/tests/` and
`refresh.test.ts:93` is the **only** exact-list assertion anywhere in this
cartridge's tests. cartridge-5c independently reached the same conclusion.
One correction to its report, checked here: the `smoke.test.ts` it inspected is
not in `mcp.ctg` — this cartridge has no such file — so whatever it found there
belongs to another board and is not a sibling of this defect. The footprint is
therefore one file, and it is complete.

## Progress (2026-09-19, ASP coordinator)

The `asp` half is written in `refresh.test.ts` and uncommitted: `listed()`
now filters out the host's own `asp` tool, and one new assertion requires the
unfiltered list to be exactly `alpha` and `asp`. With it the test passes line
93 and the generation-2 steps, then fails deterministically at line 105
(three runs): after the fixture writes `error("rejected-fixture")` into
`alpha/init.lua`, the diagnostic never contains `rejected-fixture` within 20
seconds, only "starting the host for .cartridge". That is a reload or trust
behaviour and unrelated to ASP. A likely cause is that the host refuses the
changed, untrusted `init.lua` before running it, so the error the test waits
for never happens. It needs its own analysis before this row can collect.
