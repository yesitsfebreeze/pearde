---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
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
