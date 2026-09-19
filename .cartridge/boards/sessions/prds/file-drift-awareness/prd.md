---
state: "analyzing"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/sessions.ctg"
work-kind: leaf
canonical-scope: file-drift-awareness
claim: "coordinator-78-4 2026-09-19T12:17:30.979Z"
---

# A file changed outside the session is named before it is trusted

`sessions.ctg` records which files a session touched. It does not record what they looked like, so a file edited outside the session — by a person in an editor, by another agent, by a build — is read again from a stale belief, and an edit lands on top of a change nobody named.

Stamp each file when it is read, and at the start of the next turn name the touched files that have changed on disk since. A named drift is cheap and a silent one costs an overwrite, so the report is unconditional: it says what changed, not what to do about it.

## Acceptance

- [ ] Reading a file records a stamp for it against the session.
- [ ] A file changed on disk after being read is named at the next turn start, with the file and the fact that it changed since the session last read it.
- [ ] A file the session itself wrote is not reported as drifted by its own write.
- [ ] A file that was deleted after being read is named as gone, distinctly from one that changed.
- [ ] No touched file changing produces no report, rather than an empty one.
- [ ] Stamping and drift detection are tested offline in `just test sessions` against a disposable directory.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/file-touch-tracker.ts` (64 lines at survey, verified present) and the hidden `file-awareness` extension that consumes it, which stamps the modification time of every file read and injects a warning naming the files that changed since.

Baseline to re-verify at implementation: `sessions.ctg` records touched-file state today, so this may be a field on an existing record rather than a new one. Where the per-turn report is injected is `harness.ctg`'s context composition, and the report must not move the cached prompt prefix.

Gates, cwd `/Users/feb/dev/cartridge`: `just test sessions`, `just check sessions`. Not run for this plan.
