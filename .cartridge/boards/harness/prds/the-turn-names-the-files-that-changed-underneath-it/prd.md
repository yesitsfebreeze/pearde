---
state: "analyzing"
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
claim: "coordinator-5d5e-5 2026-09-19T13:04:51.516Z"
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
