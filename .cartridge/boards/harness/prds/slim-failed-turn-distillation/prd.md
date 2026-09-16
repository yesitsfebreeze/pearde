---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/harness.ctg"
work-kind: leaf
canonical-scope: slim-failed-turn-distillation
---

# A failed turn leaves one retrievable line behind

When the context window moves past a turn, the turn is gone. That is right for a successful turn — its durable record is whatever was written down deliberately — and wrong for a failed one, because the next attempt at the same thing has no way to learn that it already failed and how.

At turn end, distil each failed tool-using turn into one line: the tools it called and its closing statement, stored so it is retrievable after the window has moved. Successful turns leave nothing; a per-turn tool log for work that worked is noise, and this is a retention rule, not a second transcript.

## Acceptance

- [ ] A failed tool-using turn is stored as one line naming the tools called and the turn's closing statement, retrievable by query after the turn has left the context window.
- [ ] A successful turn stores nothing.
- [ ] A turn that called no tool stores nothing, whether it failed or not.
- [ ] With the store unavailable, the turn completes unchanged and the failure to store is recorded, not raised.
- [ ] Distillation is disableable, and disabled it stores nothing.
- [ ] Storage, retrieval, the success and no-tool cases, and the unavailable-store case are tested offline in `just test harness`.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/slim/` (71 lines at survey, verified present) — a pure end-of-turn hook that fails open when its store is absent. Upstream writes to its own external knowledge tool; here the store is `memory.ctg`.

Reconcile at implementation with `@harness/safe-transcript-compaction` and `@harness/improve-harness-compaction-diff`, which own the rest of the compaction surface: this is the retention half and must not duplicate what compaction already drops or keeps.

Gates, cwd `/Users/feb/dev/cartridge`: `just test harness`, `just check harness`. Not run for this plan.
