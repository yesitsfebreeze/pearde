---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/harness.ctg"
work-kind: leaf
needs:
  - '@harness/the-turn-names-the-files-that-changed-underneath-it'
footprint:
  - /Users/feb/dev/cartridge/harness.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/config.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/instructions.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/system_prompt.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/transcript.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/summarize.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/describe.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/ops.rs
  - /Users/feb/dev/cartridge/harness.ctg/src/host.rs
  - /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/unit/main/tests.rs
---

# harness src/lib.rs is one file per responsibility

## Outcome

`harness.ctg/src/lib.rs` is 1708 lines (`wc -l harness.ctg/src/lib.rs`,
verified 2026-09-19) — the largest single file in the composition — even
though the crate already factors most of its logic into siblings (`bridge`,
`compaction`, `evidence`, `inspection`, `limits`, `prompt`, `roster`,
`settings`, `working`). `lib.rs` itself still answers for at least eight
distinct jobs the module list below names. Serves ranking row 6 of
`.cartridge/memos/ranking/cartridges.md` (harness: "`cartridge help harness`
does not resolve; `src/lib.rs` 1708 lines; settings merge unvalidated" — the
help-resolution and settings-validation gaps are separate concerns and not
this PRD's scope).

## Responsibilities found in `lib.rs`, with target files

1. **Config** — `max_instruction_bytes`, `max_instructions_bytes`,
   `declared_config`, `Config` struct, `configure`, `CONFIG`, `configured`
   (`lib.rs:68-91, 99-142, 1626-1652`). Target: `src/config.rs`.
2. **Instruction file discovery** — `Instruction`, `read_instruction`,
   `discover_instructions`, `escape_frame` (`lib.rs:145-212`). Target:
   `src/instructions.rs`.
3. **System prompt composition** — `SystemPrompt`, `FALLBACK_TEMPLATE`,
   `noticed_problems`, `Composition`, `memo_template`, `Frame`,
   `build_system` (`lib.rs:216-407`). Target: `src/system_prompt.rs` (a new
   file distinct from the existing `src/prompt.rs`, which is the low-level
   `` ` `` -delimited template `render()` engine; this group is what decides
   *what* to render, `prompt.rs` is *how*). **`build_system` is the exact
   function `@harness/the-turn-names-the-files-that-changed-underneath-it`
   is claimed against today** (`lib.rs:349-406`, adding a drift-report tail
   block) — see Dependencies below.
4. **Transcript projection and wire assembly** — `project_messages`,
   `turn_boundaries`, `tail_start`, `prefix_hash`, `project_compacted`,
   `is_turn_boundary`, `Request`, `Request::frame`, `read_transcript`,
   `Wire`, `request_bytes`, `convert_tools`, `build_context`
   (`lib.rs:411-545, 650-781`). Target: `src/transcript.rs`.
5. **Compaction/summarization glue** — `summary_buffer`, `parse_summary`,
   `write_summary`, `summarize` (`lib.rs:550-646`; orchestrates the
   `Snapshot`/`History` types that already live in `src/compaction.rs`).
   Target: `src/summarize.rs`.
6. **Context-value rendering** — `resolve_environment`,
   `describe_environment`, `resolve_shell`, `terminal_output_bytes`,
   `describe_terminal`, `describe_anchor`, `group`, `describe_telemetry`
   (`lib.rs:1063-1315`). Target: `src/describe.rs`.
7. **Op handlers** — `ring`, `slim`, `slim_line`, `evict`, `resolve`,
   `resolve_date`, `utc_date`, `date_from_unix_days`, `injection`,
   `compact`, `context`, `refresh_context`, `selftest`, `integration`
   (`lib.rs:788-1055, 1319-1362, 1371-1471, 1479-1526, 1531-1598, 1603-1622`).
   Target: `src/ops.rs`, or split further into turn-lifecycle
   (`ring`/`slim`/`evict`/`resolve`), context (`injection`/`compact`/
   `context`/`refresh_context`) and diagnostic (`selftest`/`integration`)
   files if `ops.rs` would otherwise exceed the size bound below — the exact
   boundary is left to implementation, the constraint is that no file mixes
   turn-lifecycle, context and diagnostic handling.
8. **Lua host glue** — `init`, `on_harness`, `on_selftest`, `on_integration`,
   `harness` (Lua table) (`lib.rs:1654-1704`). Target: `src/host.rs`.

`lib.rs` retains: module declarations, `DOCUMENT`, `FRAME_CLOSE`,
`SUMMARY_BUFFER`, `SUMMARY_LABEL`, and whatever thin glue the split leaves
that Rust requires at the crate root.

## Acceptance

- [ ] `wc -l harness.ctg/src/lib.rs` reports 200 lines or fewer.
- [ ] `wc -l harness.ctg/src/{config,instructions,system_prompt,transcript,summarize,describe,host}.rs`
      (and whichever op-handler file(s) the split produces) reports no file
      over 400 lines.
- [ ] `just test harness` passes, naming the suites that already exercise
      this code as still green:
      `harness.ctg/.cartridge/tests/unit/main/tests.rs`,
      `.cartridge/tests/integration/ring.rs`,
      `.cartridge/tests/integration/slim.rs`,
      `.cartridge/tests/integration/working.rs`.
- [ ] `just check harness`, `just audit harness` and `just isolation` report
      nothing for harness.

## Proof and recovery

Starting file: `harness.ctg/src/lib.rs`. No fixture needs creating; the
integration tests already spawn a harness base and drive `ring`/`slim`/
`context` through the crate's real op surface, so they are the reproduction
harness for "nothing observably changed."

Before touching code, capture the baseline: `wc -l harness.ctg/src/lib.rs`
from `/Users/feb/dev/cartridge`, so the acceptance bound measures a real
move rather than restating today's number.

Gates, cwd `/Users/feb/dev/cartridge`: `just check harness`, `just test
harness`, `just audit harness`, `just isolation`. Compatible fallback: every
op name and its input/output shape is preserved exactly (`ring`, `slim`,
`evict`, `injection`, `compact`, `context`, `refresh_context`, `selftest`,
`integration`), so no caller cartridge (agent, proxy) or the host's
`cartridge help harness` resolution observes a behavior change from the
split itself.

## Dependencies and review

`@harness/the-turn-names-the-files-that-changed-underneath-it` is `state:
analyzing`, claimed (`coordinator-5d5e-5 2026-09-19T13:04:51.516Z`, priority
65), and its footprint is `src/lib.rs`, `src/working.rs`,
`src/inspection.rs`, `.cartridge/tests` — it is actively adding a drift-report
tail block inside `build_system` (today `lib.rs:349-406`, group 3 above:
"System prompt composition"). Splitting `lib.rs` first would land
`build_system` at a new path (`src/system_prompt.rs`) out from under that
claim mid-flight, forcing it to rebase against a file that no longer exists
at the location its own record cites. `needs` is set to that row so this
split lands only after it, and this PRD does not edit that row's claim,
state or footprint. Everything else in this PRD's footprint (`config.rs`,
`instructions.rs`, `transcript.rs`, `summarize.rs`, `describe.rs`, `ops.rs`,
`host.rs`) is untouched by that claim.

Two other live sibling rows name `lib.rs` in prose:
`@harness/the-harness-cartridge-ships-the-readme-its-audit-demands` is done,
footprint `README.md` only, no overlap. `@harness/reflex-tool-audit-loop` is
open with no `footprint` field at all in its frontmatter — an empty
footprint reserves the whole of `harness.ctg` rather than a named subset, so
it is not a targeted collision with this PRD specifically; it is a standing
board-hygiene gap on that row, not something this PRD's `needs` can fix
without editing that row's record, which this PRD does not do. No `needs` is
set for it.
