---
repo: /Users/feb/dev/cartridge/tools.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-tools-preflight
footprint:
- /Users/feb/dev/cartridge/tools.ctg/src/service.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/unit/service/tests.rs
- /Users/feb/dev/cartridge/tools.ctg/.cartridge/tests/integration/lane.test.ts
---

# Preview workspace-tool effects before execution

The tools cartridge can say what `bundle`, `lane`, `land` or `lane-rm` would do without doing it. `dispatch` in [service.rs](../../../../../../tools.ctg/src/service.rs) mutates straight away: it creates worktrees and branches, provisions `.cargo`, deletes artefacts and replaces `dist/cartridge`, and reports only failures. The old `scripts/workspace.py` home is gone. Per [tui-and-tools-are-cartridges](../../../../../../.cartridge/memos/decision/tui-and-tools-are-cartridges.md), this tooling is the tools cartridge.

Recommended default: an optional `"preview": true` on each op returns `{op, paths, refs, effects[], missing[], digest}`. The digest covers trunk HEAD, the worktree list and the relevant status output. Apply may pass `"expect": digest` and is refused on mismatch. A preview grants nothing.

## Acceptance

- [ ] A preview of each of the four ops leaves refs, worktrees and files byte-identical in a temporary repository, and lists the effects apply would perform, including artefacts `lane-rm` would delete.
- [ ] A missing prerequisite (`git`, `cargo`, a Rust binary) is named by the preview, not first discovered at apply.
- [ ] Apply with a stale `expect` (the trunk moved, or a file was added to the lane) is refused before any creation or deletion.
- [ ] Requests without `preview`/`expect`, including the string form `"bundle debug"`, behave exactly as today.

## Proof and recovery

First capture a byte-level snapshot of the fixture repository around a preview in [lane.test.ts](../../../../../../tools.ctg/.cartridge/tests/integration/lane.test.ts). Gates, cwd `/Users/feb/dev/cartridge`: `just test tools`, `just check tools`. Not run. Rollback: remove the fields. There is no second executor: apply and preview share each op's checks.

## Dependencies and review

No hard prerequisites. Same file as the lane-release and bundle-provenance leaves, so land them one after another. Board placement under @runtime is historical (see the `tools` board). [Review](review.md): inherits 2 rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-tools-preflight.md` (status open). The PRD state above is authoritative.

### Outcome

Each mutating workspace operation can report inputs, paths, prerequisite tools and planned effects without creating files or refs.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [lane-rm-refuses-after-the-gates-run](../../../root/prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../../root/prds/lanes-do-not-poison-each-others-builds/prd.md).

### Footprint

Workspace tools; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `tools.ctg/service.rs`
- `tools.ctg/tests/test_lane.py`
- `cartridge.ctg/scripts/workspace.py`
- `cartridge.ctg/repositories.json`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Preflight for bundle/worktree creation changes no refs or files and reports a missing binary/layout dependency clearly.
- [ ] Changing a target after preview forces revalidation; apply performs only the reviewed operation.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Add a machine-readable plan using existing command semantics. Bind apply to the checked repository revision and relevant filesystem state; distinguish validation from authorization. Avoid parallel development of a new generic executor while the document architecture remains a proposal.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test tools
just check tools
just links
```


### Compatibility and recovery

Use temporary roots and preserve existing development commands. Preflight does not authorize or execute. Cleanup is limited to artifacts owned by the operation; no ancestry-only or blanket deletion of lanes.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
