# <Canonical plan ID> review history

Plan: <owner-qualified ID and relative source path>.
Scope: <one observable outcome; parent/leaf/standing record>.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: <prior canonical ID and used rounds, or none>.

Use the shared [review method](../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round <1–5> — <date>

Presented revision: <commit plus content digests; include dirty files>.

| Input | Content digest |
| --- | --- |
| Plan | <path and SHA-256> |
| Specs | <each path and SHA-256, or not yet applicable> |
| Material contracts/dependencies | <paths/revisions affecting this assessment> |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | | |
| Ownership and reuse | | |
| Dependencies and implementable slices | | |
| Observable acceptance and baseline evidence | | |
| Failure, recovery and compatibility | | |
| Reviewer total | / 100 | |

Findings and concrete revisions: <issue, evidence, recommendation, resolution>.
Disposition: <keep / revise / split / merge / rehome / retire recommendation>.
Validation: <actual commands, cwd, exit status and relevant limits>.
Reviewer identity: <actual agent ID or named reviewer>.
User rating: <not required under delegation; record only if actually supplied>.
User feedback/provenance: <message or reference and the revision it assessed>.
Result: <FAIL / pending agent review / PASS / stale; exhaustion if round 5 fails>.
Unresolved blocking findings: <list or none>.
Rounds used / remaining: <n / 5-n>.
Next action: <bounded revision, proceed to implementation, await agent review, or stop>.
