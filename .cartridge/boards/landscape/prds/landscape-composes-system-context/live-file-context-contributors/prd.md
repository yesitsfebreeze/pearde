---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context/live-file-context-contributors
needs:
- "@landscape/landscape-composes-system-context/live-file-context-contributors/file-kernel-evidence-adapter"
- "@memo/landscape-file-kernel-context-facade"
- "@landscape/landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters"
---

# File and live context retain owner and freshness

Roll-up only; claim a leaf. memo's `context` operation (`memo.ctg/src/context.rs`, providers per `memo.ctg/.cartridge/docs/context.md`) composes evidence from every `context.<kind>` event the composition covers. The file and kernel half is delivered: the file/kernel adapter and memo facade are done, and fs listens to `context.file` (fs.ctg transport branch `03f360e`). The live half remains. Session, terminal and route providers belong to sessions, pty and router as `context.<kind>` events, and each receives the trusted caller scope from `@memo/landscape-live-owner-context-facade`.

## Acceptance

- [ ] Each linked leaf is done with revision-bound proof and a passed review.
- [ ] At one pinned revision set, a single `context` prepare returns separately attributed `file`, `kernel`, `session`, `terminal` and `route` rows. Exact readback of each is `available`.
- [ ] After a source edit, the affected row's readback is `changed` while unchanged rows keep their references. A provider removed from the composition reports `absent`, and the other rows stay within the shared budget.

## Work items

- [File and kernel evidence use one attributed shared row contract](file-kernel-evidence-adapter/prd.md) (done)
- [Expose configured file and kernel evidence through native shared context](../../../../memo/prds/landscape-file-kernel-context-facade/prd.md) (done)
- [Live owners answer context with scoped metadata](live-owner-evidence-adapters/prd.md)

## Integration gate

From `/Users/feb/dev/cartridge`: `just test memo`, `just test fs`, and `bun test memo.ctg/.cartridge/tests/integration/context.test.ts`, plus the live leaves' gates. None has run for this plan.

## Review

[Review history](review.md). Rounds 1–2 are inherited from `landscape-composes-system-context`; round 3 rebased; five rounds maximum. Target board after rehoming: memo.
