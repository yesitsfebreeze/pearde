---
state: "question"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/sessions.ctg"
work-kind: leaf
canonical-scope: file-drift-awareness
footprint: ["/Users/feb/dev/cartridge/sessions.ctg/src/drift.rs","/Users/feb/dev/cartridge/sessions.ctg/src/lib.rs","/Users/feb/dev/cartridge/sessions.ctg/src/changes.rs","/Users/feb/dev/cartridge/sessions.ctg/src/limits.rs","/Users/feb/dev/cartridge/sessions.ctg/src/change_record.rs","/Users/feb/dev/cartridge/sessions.ctg/cartridge.json","/Users/feb/dev/cartridge/sessions.ctg/README.md","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/help.md","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/unit/main/drift_tests.rs","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/unit/main/tests.rs","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/unit/main/change_records_tests.rs","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/integration/change-records.test.ts","/Users/feb/dev/cartridge/sessions.ctg/.cartridge/docs/change-records.md"]
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

## State at 2026-09-19T16:10Z (coordinator cartridge-78, session ended)

Three review rounds are scored in `review.md`: 66, 71 and 74 out of 100, all
FAIL. A **round-4 revision was in flight when this session stopped, so
`specs/spec01.md` is partially newer than round 3's recorded score and no
reviewer has seen it.** Read round 3 in `review.md` before trusting the spec.

Round 3's verdict is the thing to act on: "circling on the defect class,
converging on the design". Its three open blockers are B6 (the re-stamp gate
executes only the `Store::load` caller while three passages claim all four),
B7 (the re-stamp absorbs drift in the *live* window — a `connect`/`mapping` op
re-baselines a session already resident in memory — and `install` can carry a
resident session's stamps forward in the same line, so it is not an unavoidable
cost) and B8 (the normalization contract is gated only against a relative path).

Two standing facts for whoever resumes it. The frontmatter still declares **no
footprint**, which reserves the whole of sessions.ctg and blocks four other
claimants on `src/lib.rs`; set the spec's list before any implementer claim.
And the answer shape is frozen — `report: null` when nothing moved, CHANGED and
GONE as two distinct lists, nothing rendered at all in the null case — because
`@harness/the-turn-names-the-files-that-changed-underneath-it` is being specced
against it.

## Footprint set by a departing owner's handover

Recorded 2026-09-19 by coordinator cartridge-eb, which does not own this board.

Coordinator cartridge-78 owned the sessions board and ended its session, releasing this row to `open` at 3 of 5 review rounds (scores 66, 71, 74). It did not fail out of its rounds: the reviewer judges the design sound. Its closing handover reported that the spec's footprint is the nine paths now in the frontmatter, while the frontmatter itself declared none — and an empty footprint reserves the whole repository, so this row was blocking four other claimants on `sessions.ctg` while nobody was working it.

I set the nine paths exactly as handed over, and verified each against the tree: seven exist today, and `src/drift.rs` and `.cartridge/tests/unit/main/drift_tests.rs` do not, because the spec creates them. Nothing else was touched — not `state`, not `claim`, not `commit`, not the body above this section.

Whoever picks this row up should check the footprint against `specs/spec01.md` before claiming, and correct it if the spec has moved. Two further facts from the same handover, both load-bearing:

A round-4 revision was in flight when that session stopped, so part of it is on disk and unscored. **Read `review.md` round 3 before trusting `specs/spec01.md`.**

The answer shape is frozen and nothing in rounds 3 or 4 touched it: `report: null` when nothing moved, CHANGED and GONE as two distinct lists, nothing rendered at all in the null case. `@harness/the-turn-names-the-files-that-changed-underneath-it` is specced against exactly that contract and carries `needs` on this row.

An open blocker on this row, from its own review: stamps live only in memory, and re-stamping on `Store::install` absorbs drift in the live window too, so a `connect` or `mapping` op silently re-baselines a session that is already resident. Until that is fixed a null report can mean "nothing changed" or "the store forgot", and no consumer can tell the two apart.


## Questions

Five independent plan reviews have failed (66, 71, 74, 88, 89); no automatic review allowance remains. The final technical plan resolves B6 through B9, but B10 identifies a completion cycle: this leaf requires actual file-read and next-turn evidence while both FS and Harness consumers require this leaf to be collected first. Neither mechanism tests nor future ownership mapping proves those original requirements.

Recommended decision: authorize a faithful decomposition retaining the original composed outcome and acceptance as an aggregate, with a separately collectable Sessions provider child and the existing FS/Harness consumers depending on that provider. Authorize an explicit additional review allowance for the revised decomposition; used rounds must remain in history. An alternative is to keep the current leaf and authorize a coordinated cross-owner plan with an executable completion order, also requiring further review. Without that authorization this scope remains in question; no original acceptance is waived, ticked or deleted, and no sixth automatic revision is started. Full fifth-round evidence is recorded in review.md and reviewer-codex-5.md.
