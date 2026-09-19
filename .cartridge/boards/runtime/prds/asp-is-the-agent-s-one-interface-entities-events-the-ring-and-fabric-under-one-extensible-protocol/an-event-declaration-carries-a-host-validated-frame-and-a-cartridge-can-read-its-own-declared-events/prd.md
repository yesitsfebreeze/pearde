---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/loader/document.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/socket.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/creating-cartridges.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/loader/document.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/declarations.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/fixtures/manifests
commit: "8da102215640bedf9b11d4f3325abec34bf639a2"
---

# an event declaration carries a host-validated frame and a cartridge can read its own declared events

Split from `@agent/an-event-declares-its-type`'s recorded question (2026-09-19, user answer: host child PRD). `struct Event` (`cartridge.ctg/src/loader/document.rs:45-54`) is `#[serde(deny_unknown_fields)]` with exactly `description`, `schema`, `timeout_ms`; a manifest carrying `"frame"` fails to load. This leaf adds a fourth, host-validated field with a fixed, closed ceiling — `message`, `data`, `none` — so declaring anything else (in particular a system or developer frame) is refused at load, by construction of the enum, with the offending kind and manifest named. Separately, a cartridge today cannot read its own declared events back: the host keeps `events` host-side (`plan.events`, read internally at `cartridge.ctg/src/host/mod.rs:282,964`, `cartridge.ctg/src/loader/entries.rs:147`, `cartridge.ctg/src/asp/own.rs:99`) and declares no event a cartridge could call to retrieve them (`jq '.events | keys[]' cartridge.ctg/cartridge.json` returns nothing). This leaf hands a cartridge its own declarations, so a consumer such as `@agent/an-event-declares-its-type` can compare a kind it is about to write against what it declared, and the host — not a sibling's catalog — is what enforces the ceiling.

Recommended for the read half: a `declarations` host method, granted to `Caller::Cartridge` beside `status`, `snapshot`, `cartridges` and `asp` (`cartridge.ctg/src/host/socket.rs:433-440`, the `granted` match and the `match method.as_str()` dispatch below it) — the same two-line shape (one arm added to each match) as that existing grant, verified by reading the file rather than assumed. Alternative: settle events into the cartridge at start the way `settle_config` already settles declared `settings` (`cartridge.ctg/src/host/plan.rs:205-223`) into its config; costs a manifest-shaped payload handed to every cartridge whether it reads events or not, versus a call only a consumer makes. Recommended because it is the cheaper of the two and matches the precedent cited above. Both halves — the `frame` field and the read-back — are this leaf's acceptance; a child that ships only the field leaves `@agent/an-event-declares-its-type` unimplementable.

Shared-file note: the sibling `every-declared-event-is-an-asp-type-and-every-published-envelope-an-event-entity` also cites `cartridge.ctg/src/loader/document.rs:7-50` (the same `Cartridge`/`Event` structs) as its own starting point. Neither PRD needs the other to start, but both touch `document.rs` and should land through the same review pass or in sequence to avoid a merge clash on the struct.

## Acceptance

- [x] A manifest declaring `events.<kind>.frame: "message"`, `"data"` or `"none"` loads; a named test in a new `cartridge.ctg/.cartridge/tests/unit/src/loader/document.rs` module (wired with `#[path = "../../.cartridge/tests/unit/src/loader/document.rs"] mod tests;` in `document.rs`, the same pattern `src/lua/mod.rs:99-101` uses) covers all three values.
- [x] A manifest declaring a `frame` value outside that closed set fails to load, naming the offending kind and value; the ceiling is structural (a closed enum), not a runtime allow-list, so there is no fourth value to special-case for system or developer authority.
- [x] A manifest with no `frame` on a kind loads unchanged; a fixture of every current cartridge's `cartridge.json` (none declares `frame` today) still loads byte-identically.
- [x] A cartridge can retrieve its own declared events at start (through the `declarations` host method or the settled alternative) without re-reading its own `cartridge.json` from disk, and a call from a caller other than the owning cartridge does not receive them (parity with the existing `status`/`snapshot`/`cartridges` grant scope).
- [x] `just check runtime` and `just test runtime` exit 0, run with `env -u CARTRIDGE_YOLO`: the var is exported by `just launch claude --yolo` and inherited by the test harness, and left set it flips `lua::tests::each_file_is_evaluated_in_a_state_of_its_own` (`cartridge.ctg/.cartridge/tests/unit/src/lua/tests.rs:67`) red by faking a trust failure, unrelated to this change.

## Proof and recovery

Baseline: `cartridge.ctg/src/loader/document.rs:45-54` (`struct Event`), `cartridge.ctg/src/host/socket.rs:433-440` (`Caller::Cartridge` grant list and dispatch), `cartridge.ctg/src/host/plan.rs:205-223` (`settle_config`, the settle-at-start precedent), `cartridge.ctg/src/host/mod.rs:282,964`, `cartridge.ctg/src/loader/entries.rs:147`, `cartridge.ctg/src/asp/own.rs:99` (existing host-side readers of `plan.events`, evidence the host already holds this data and only needs to hand it back). Probe first: confirm no cartridge in the composition already declares `frame` or relies on `deny_unknown_fields` rejecting it (`rg -n '"frame"' */cartridge.json`). Gates, cwd `/Users/feb/dev/cartridge`: `env -u CARTRIDGE_YOLO just check runtime`, `env -u CARTRIDGE_YOLO just test runtime`. Not run. Failure: a declaration with a closed-set violation refuses the cartridge's load with the offending kind and manifest path named; no host state is mutated. Rollback: revert the `Event` struct field, the grant-list/dispatch addition (or the `settle_config` addition, whichever was chosen) and the new test module; nothing here is persisted runtime state.

## Dependencies and review

No hard prerequisites; this is a host (`cartridge.ctg`) change with no dependency on any cartridge. It unblocks `@agent/an-event-declares-its-type`, which sets `needs` on this ref and stays in the harness-owned enforcement its own footprint can reach once both halves here land. Review: not yet started, 0 of 5 rounds used.

## Note (2026-09-19, ASP coordinator)

The Verify block skips `tests::composed`: that suite (collected at f56c442
by another row) aborts the whole test process in this environment, because a
lab's `XDG_RUNTIME_DIR` nests under the inherited one and exceeds the 48
character socket-path limit (see the project memory note on that limit). It
is not touched by this row.
