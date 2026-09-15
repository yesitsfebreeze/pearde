---
kind: work
description: "Preview workspace-tool effects before execution"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["preview workspace-tool effects before execution", "implementing tools cartridge improvements"]
---

# Preview workspace-tool effects before execution

## Outcome

Each mutating workspace operation can report inputs, paths, prerequisite tools and planned effects without creating files or refs.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [lane-rm-refuses-after-the-gates-run](../../prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../prds/lanes-do-not-poison-each-others-builds/prd.md).

## Footprint

Workspace tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `tools.ctg/service.rs`
- `tools.ctg/tests/test_lane.py`
- `cartridge.ctg/scripts/workspace.py`
- `cartridge.ctg/repositories.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Preflight for bundle/worktree creation changes no refs or files and reports a missing binary/layout dependency clearly.
- [ ] Changing a target after preview forces revalidation; apply performs only the reviewed operation.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Add a machine-readable plan using existing command semantics. Bind apply to the checked repository revision and relevant filesystem state; distinguish validation from authorization. Avoid parallel development of a new generic executor while the document architecture remains a proposal.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test tools
just check tools
just links
```


## Compatibility and recovery

Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
