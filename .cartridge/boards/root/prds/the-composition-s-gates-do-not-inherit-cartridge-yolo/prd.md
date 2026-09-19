---
state: "open"
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge"
footprint:
  - /Users/feb/dev/cartridge/.cartridge/justfile
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/cartridge-development.md
---

# the composition's gates do not inherit CARTRIDGE_YOLO

## Outcome

`just check <target>` and `just test <target>` report the same verdict whatever
the terminal that invoked them was launched with. The gate removes
`CARTRIDGE_YOLO` from the environment before it spawns cargo, so a gate result
means one thing for every session, and a green or a red is a fact about the code
rather than about the shell.

## Evidence

Measured 2026-09-19 by two independent sessions, in two different cartridges.

`just launch claude --yolo` exports `CARTRIDGE_YOLO=1`. Every coordinator and
worker session on this machine currently carries it, including the one the user
is reading. It is not a property of a worker or of a cartridge: it is a property
of the terminal, and it changes behaviour rather than merely relaxing a prompt.
The host merges `yolo: true` into every cartridge declaring that setting
(`cartridge.ctg/src/settings/mod.rs:15-16`,
`cartridge.ctg/src/transport/settings.rs:188-192`).

Two measured consequences, both with the tree and the tests unmodified:

- `agent.ctg`: `agent.ctg/src/lib.rs:634` skips the entire policy branch, so a
  call the policy would deny simply runs and journals `result.error == false`.
  `env -u CARTRIDGE_YOLO cargo test -p agent --test loop` exits 0 with 13
  passed; `CARTRIDGE_YOLO=1 cargo test -p agent --test loop` exits 1 with 12
  passed and 1 failed. `env -u CARTRIDGE_YOLO just test agent` exits 0.
- `cartridge.ctg`: an untrusted file becomes trusted, so
  `lua::tests::each_file_is_evaluated_in_a_state_of_its_own` gives 0 passed and
  1 failed under `just test cartridge`, and 1 passed under
  `env -u CARTRIDGE_YOLO`.

The cost is already recorded rather than hypothetical: a PRD was filed against a
non-existent `agent.ctg` defect on the strength of a red gate, and had to be
retargeted once the variable was found
(`@agent/a-denied-tool-call-journals-its-error-flag`). A second session reported
a pristine-clone failure count with the right number and the wrong cause from
the same variable.

The alternative to fixing the gate is five coordinators remembering a workaround
forever, and every hand-run gate in every terminal still being wrong. Removing
the variable once, inside the gate, makes the composition's own instrument
honest. The precedent for the pattern is already in the tree:
`memory.ctg/src/hub/src/lib.rs:121` and `memory.ctg/src/hub/src/commands_hub.rs:454`
strip `TAKEOVER_ENV` at their spawn sites for exactly this reason.

## Acceptance

- [ ] `_fan`, `_one` and any other recipe in `.cartridge/justfile` that spawns
      cargo or a nested `just` removes `CARTRIDGE_YOLO` from the child's
      environment.
- [ ] `just test agent` exits 0 from a shell with `CARTRIDGE_YOLO=1` exported,
      with no change to `agent.ctg`, and the same command exits 0 with the
      variable unset. The two runs agree.
- [ ] `just test cartridge` behaves the same way for
      `lua::tests::each_file_is_evaluated_in_a_state_of_its_own`.
- [ ] A run that legitimately needs the variable can still get it, or the PRD
      records that no such run exists. The gate must not make a real capability
      unreachable in order to make a measurement stable.
- [ ] `.cartridge/memos/routine/cartridge-development.md` states that a gate
      result is only evidence when the environment it was taken in is named, and
      that the gate now strips this variable itself.

## Landing note

`.cartridge/justfile` was dirty in the shared checkout when this PRD was filed,
with an edit belonging to another session. `collect` commits every dirty path
inside the footprint, so whoever implements this must run
`git -C /Users/feb/dev/cartridge status --porcelain -- .cartridge/justfile`
first and wait for, or attribute, that edit rather than sweeping it into the
receipt.

## Provenance

Filed 2026-09-19 by coordinator cartridge-eb, which owns the agent and harness
boards, at the proposal of coordinator cartridge-78, which found the same
problem from the opposite direction and declined to widen an unrelated row's
footprint to fix it. The root board owns the superproject gates, so the row
belongs here rather than on either of theirs.

## Handoff (2026-09-19, coordinator cartridge-4b, session ending)

- State: `open`, unclaimed. Spec `specs/spec01.md` is at revision 1. Review rounds used: 2 of 5 (see `review.md`). Round 1 failed at 80 because the lane needs `CARTRIDGE_BIN`; that is fixed. Round 2 failed at 86 with one blocker: both agent blocks run the whole `just test agent` suite, and it contains a load-sensitive flake, `streaming_cancel_mid_stream_releases_once_without_append` at `agent.ctg/.cartridge/tests/integration/loop.rs:1236`, which failed 2 of 6 gate runs under load. The fix for round 3 is to scope the agent blocks to the named yolo-sensitive test (`multiple_tool_calls_execute_and_persist_in_response_order`) and assert that it ran.
- The foreign `_fan` isolation hunk is no longer dirty. The user committed it in superproject `5831e2a`. So `.cartridge/justfile` is clean at HEAD, and the earlier landing-order constraint is moot. The spec and `justfile.patch` were written against the pre-`5831e2a` `_fan`; re-check that the patch applies before implementing.
- `@root/an-owner-check-runs-the-isolation-gate-and-says-so` (f4, `open`, unreviewed) says its documentation box belongs in `.cartridge/memos/routine/cartridge-development.md`, which is in this row's footprint. Decide whether that text joins this row.
- Analyst report and patches: `.state/loop/the-composition-s-gates-do-not-inherit-cartridge-yolo/`.
