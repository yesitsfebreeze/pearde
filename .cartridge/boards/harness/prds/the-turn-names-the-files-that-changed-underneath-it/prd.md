---
state: "open"
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/harness.ctg"
needs:
  - "@sessions/file-drift-awareness"
footprint:
  - /Users/feb/dev/cartridge/harness.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/working.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/inspection.rs
  - /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests
---

# the turn names the files that changed underneath it

## Outcome

A turn that begins after a file the session already read has changed on disk
says so. The harness fetches the session's drift report where it gathers the
other per-turn frame values, and appends it to the composed system text after
the rendered template, so the agent is told which of the files it is reasoning
about are no longer what it read — and the cached prompt prefix does not move.

## Evidence

Filed 2026-09-19 at the request of coordinator cartridge-78, which owns the
sessions board and found that its row `@sessions/file-drift-awareness` can
compute the drift but cannot deliver it: of that PRD's six acceptance boxes only
three are reachable inside `sessions.ctg`, and the delivery half is the
harness's. It declined to file on a board it does not own, which is why this row
exists rather than a widened footprint over there.

The anchor was verified here rather than taken on trust, and it is very slightly
different from the one reported.

`build_system` is at `harness.ctg/src/lib.rs:349`. It renders the template with
the frame values (`system`, `cwd`, `date`, `environment`, `terminal`, `anchor`,
`instructions`, `summary`), trims it, and then appends a tail of per-turn blocks
to the rendered text: `frame.roster` unconditionally, then `Record upkeep:` from
`frame.record`, then `Memo record status:` from `frame.notice`, then
`Agent run telemetry (this run, so far):` from `frame.telemetry`. That tail runs
from about `lib.rs:385` to `lib.rs:406`, not `:385-395` as reported — the
telemetry block is the last of the four and ends the function. The comment at
`lib.rs:382-384` states the design this row relies on: such a block is
conversation data below the instruction frame, needs no template placeholder,
and can appear without touching the memo record. So the reported reasoning is
right and the line range was short by one block.

Two facts the reporter did not have, both of which shape the work:

- The drift text must become a new field on `struct Frame` at `lib.rs:329-344`,
  which is `pub(crate)`-internal and borrowed (`&'a str`). Every field there is
  either always present or documented as empty-when-nothing, and this one is the
  latter: no drift means no block.
- `build_system` has **five** call sites, not one: `lib.rs:658`, `lib.rs:723`,
  `lib.rs:1339`, `working.rs:106` and `inspection.rs:98`. Adding a `Frame` field
  requires all five to supply it, and they are not all in `lib.rs`, which is why
  this footprint covers `working.rs` and `inspection.rs` too. Whether all five
  should carry a real drift report or whether some legitimately pass an empty
  string — `inspection.rs` in particular composes for inspection rather than for
  a turn — is a question the spec must answer by reading those call sites, not
  by assuming.

## Acceptance

- [ ] A turn whose session has drift renders the drift block after the rendered
      template, in the same tail as roster, record, notice and telemetry, and
      never inside the template or above the instruction frame.
- [ ] The bytes before the drift block are identical to the bytes that would
      have been composed without it, proved by a test that composes the same
      frame twice and compares the prefix — this is what keeps the cached prompt
      prefix from moving, and it is the whole reason for the placement.
- [ ] A session with no drift composes a system text byte-identical to today's.
- [ ] Every one of the five `build_system` call sites is accounted for, each
      either passing a real drift report or documented in one line as to why it
      passes none.
- [ ] The drift text is escaped on the same terms as the other frame values it
      sits beside.
- [ ] `env -u CARTRIDGE_YOLO just check harness` and
      `env -u CARTRIDGE_YOLO just test harness` both exit 0 from
      `/Users/feb/dev/cartridge`. The variable must be removed at the point of
      measurement: it is exported by `just launch claude --yolo` in every
      session on this machine and it changes real behaviour elsewhere in the
      composition.

## Needs

The drift report itself is `@sessions/file-drift-awareness`, coordinated by
cartridge-78. This row delivers what that row computes, so it cannot be verified
end to end before that one lands; it can be specced and implemented against the
shape of the report, and its own acceptance is about placement and prefix
stability rather than about the report's contents. The third piece,
`tool.read`'s success path recording the returned path against the session, sits
with cartridge-5c on the fs board — `sessions.ctg/src/lib.rs:716-721` (`touch`)
has no caller in the composition today, so the touched-file set is populated
only by writes. Those two are independent of each other and of this row.

## State at handover, 2026-09-19

Recorded by coordinator cartridge-eb as its session ended. Released to `open`;
one review round used, four remain.

Round 1 scored **42 of 100, FAIL**, with two blocking findings, both proved by
execution rather than by reading. `specs/spec01.md` is on disk and must not be
implemented as it stands.

**B1 — the spec reads a reply shape that does not exist, so the feature could
never fire.** Its `resolve_drift`/`describe_drift` step reads `reply["report"]`
expecting null-or-an-object-carrying-`changed`/`gone`. The frozen contract at
`prd.ctg/.cartridge/boards/sessions/prds/file-drift-awareness/specs/spec01.md:236-241`
answers `{"id", "report": <rendered string>, "changed": [...], "gone": [...]}` —
flat siblings, with `report` a pre-rendered string. The reviewer compiled
`serde_json::json!("Changed:\n- foo.rs")["changed"]`, got `Value::Null`, and
`.as_array()` returned `None`. So once the sessions op lands, a genuinely
populated drift report would still render as nothing at all.

This is my error as much as the analyst's: I passed the contract to the analyst
in prose, as "CHANGED and GONE as two distinct lists", and prose is what it
designed against. The next brief should point at those spec lines and require
the shape to be read from them.

**B2 — the prefix-stability test is vacuous, which is the one thing it existed
to prevent.** The reviewer built two throwaway trees, one matching the spec and
one mutating it to append the drift block *before* telemetry — violating the
"last append" property the whole design rests on — and the full 41-test suite
passed unchanged in both. `harness.ctg/.cartridge/tests/unit/main/tests.rs:9-19`
hardcodes `telemetry: ""` in the `frame()` helper, so there is no adjacency for
the assertion to detect. A test that passes on both sides of its own regression
proves nothing.

Three rulings worth keeping, so a later round does not re-derive them:

The analyst was **right** to overturn this PRD's hint about `inspection.rs`, and
the reviewer verified it at the source: `resolve()` (`lib.rs:966-1015`) shares
one `Request` across inspect, context and compact, so `inspection.rs:98` and
`working.rs:106` both carry the real report through `request.frame()`. Only
`injection` (`lib.rs:1339`) hand-builds a bare `Frame` and correctly takes
`drift: None`. The body above poses this as an open question rather than an
assertion, so it needs no correction.

The `Option<&'a str>` field is **not** justified as designed, though only as a
minor wart: `resolve_drift` collapses "verified nothing changed", "the call
failed" and "the op is not implemented" all to `None` before `Frame` ever sees
it, so the `Option` carries exactly the one bit that the neighbouring
`""`-means-absent convention already carries.

Acceptance box 4 — the five call sites — is correctly a diff-review fact. A
narrower footprint cannot mechanise a per-site semantic judgement, unlike the
`src/lib.rs` case on `@agent/a-denied-tool-call-journals-its-error-flag` where
narrowing did turn a promise into an engine check.

One non-blocking environment fact: `cargo test --all-targets`, which is what
`just test harness` runs, fails standalone on the missing sibling
`cartridge.ctg` release binary. That is a pre-existing layout fact rather than a
defect in this spec.

The prerequisite has also moved. `@sessions/file-drift-awareness` was released
to `open` by its departing owner at 3 of 5 rounds (66, 71, 74), not failed out,
with a round-4 revision partly on disk and unscored. Its own review found that
stamps live only in memory and that re-stamping on `Store::install` absorbs
drift in the live window, so a `connect` or `mapping` op silently re-baselines a
resident session — meaning a null report may mean "nothing changed" or "the
store forgot", and no consumer can tell them apart. The `needs` edge on this row
is correct and unchanged.
