---
state: open
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/proxy.ctg"
work-kind: leaf
footprint:
  - "src/service.rs"
  - "src/config.rs"
  - "src/request.rs"
  - "src/recording.rs"
  - "src/reports.rs"
  - "src/run.rs"
  - "src/execute.rs"
  - ".cartridge/tests/unit/tests.rs"
---

# proxy src/service.rs is one file per responsibility

## Outcome

`proxy.ctg/src/service.rs` is 1013 lines (`wc -l proxy.ctg/src/service.rs`,
verified 2026-09-19) and mixes at least six jobs behind one `impl Service`
block, even though `context.rs`, `trace.rs`, `usage.rs` and `continuation.rs`
already exist as siblings that most of `service.rs`'s methods only thinly
wrap. Serves ranking row 5 of `.cartridge/memos/ranking/cartridges.md`
(proxy: "`src/service.rs` 1013 lines; 8 uncommitted files" — the uncommitted
files are a separate, unrelated concern and not this PRD's scope).

## Responsibilities found in `service.rs`, with target files

1. **Config** — `Config` struct, `default`, `parse`, `validate`
   (`service.rs:25-132`). Target: `src/config.rs`. (Distinct from the
   existing `settings.rs`, which is the generic declared-defaults/merge
   helper shared across cartridges; `Config` is proxy's own typed settings
   built from it.)
2. **Request assembly** — `request`, `request_with_stream`,
   `request_for_principal`, `enrich`, `staged`, `session`
   (`service.rs:232-351, 544-599`). Target: `src/request.rs`.
3. **Turn recording** — `append_to_ledger`, `remember`, `observe`
   (`service.rs:354-374, 532-537, 963-1012`). Target: `src/recording.rs`.
4. **Reporting surface** — `begin_context`, `context_report`,
   `context_observation`, `prepare_context`, `inspect_context`,
   `begin_trace`, `trace_report`, `usage_report`, `continuation_id`
   (`service.rs:375-530`). Target: `src/reports.rs`. This is the thinnest
   group — most of it already delegates into `context.rs`/`trace.rs`/
   `usage.rs`/`continuation.rs` — but it is still a distinct "what a caller
   can ask about a turn" responsibility from request assembly or recording.
5. **The request/response loop** — `run` (`service.rs:601-858`, 257 lines on
   its own, the largest single function in the file). Target: `src/run.rs`.
6. **Tool execution** — `execute` (`service.rs:864-957`). Target:
   `src/execute.rs`.

`service.rs` retains: the `Call` type alias, `Service`/`Tool`/`Reports`/
`Invocation` struct definitions and their small helpers (`descriptor_revision`,
`operation`, `Invocation::drop`, `Service::new`), and module wiring.

## Acceptance

- [ ] `wc -l proxy.ctg/src/service.rs` reports 250 lines or fewer.
- [ ] `wc -l proxy.ctg/src/{config,request,recording,reports,run,execute}.rs`
      reports no file over 300 lines.
- [ ] `just test proxy` passes, naming `proxy.ctg/.cartridge/tests/unit/tests.rs`
      (2890 lines, exercises `Service` via `use super::*`) explicitly as
      still green, along with `.cartridge/tests/unit/context.rs`.
- [ ] `just check proxy`, `just audit proxy` and `just isolation` report
      nothing for proxy.

## Proof and recovery

Starting file: `proxy.ctg/src/service.rs`. No fixture needs creating;
`.cartridge/tests/unit/tests.rs` already builds a `Service` and drives it
through `request`/`run`/`execute`, so it is the reproduction harness for
"nothing observably changed" as long as every method's signature and
visibility is preserved across the split.

Before touching code, capture the baseline: `wc -l proxy.ctg/src/service.rs`
from `/Users/feb/dev/cartridge`, so the acceptance bound measures a real
move rather than restating today's number.

Gates, cwd `/Users/feb/dev/cartridge`: `just check proxy`, `just test proxy`,
`just audit proxy`, `just isolation`. Compatible fallback: this is a pure
internal reorganization — `Service`'s public methods keep their exact
signatures, so `lib.rs` (the only caller of `Service` inside `proxy.ctg`)
and the host `launch --passthrough` consumer observe no change.

## Dependencies and review

`rg -l "service\.rs" prd.ctg/.cartridge/boards/proxy/prds/*/prd.md` names
eight sibling PRDs; all eight are `done` or `deferred`
(`the-proxy-cartridge-ships-the-readme-its-audit-demands`,
`improve-proxy-programme`, `proxy-turns-carry-recall-and-reflex-tools`,
`improve-proxy-total-usage`, `improve-proxy-continuation-recovery`,
`improve-proxy-tool-trace`, `the-proxy-answers-within-its-bound-or-reports-the-delay`
are `done`; `proxy-document-client` is `deferred`,
`review-status: superseded-recommend-retire`). No live PRD holds a claim or
an open footprint on `service.rs` today, so no `needs` is set.
