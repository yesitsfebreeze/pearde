---
complexity: medium
footprint:
  - src/roster.rs
  - src/channels.rs
  - src/mailbox.rs
  - src/main.rs
  - src/observations.rs
  - .cartridge/tests/unit/main/observation_tests.rs
  - .cartridge/tests/integration/observations.test.ts
  - .cartridge/docs/observations.md
---

# Report the retained observation window

Add optional immutable config.observations_path and native sessions reflex_report{limit,max_bytes}; requests never supply/override paths. Disabled by default. Read only the configured regular non-symlink file and its .1 rotation, maximum16MiB total, <=10000 complete JSONL rows, <=64KiB per line. Refuse nonregular/oversized input with explicit unavailable/oversized status; detect metadata change while reading as unstable evidence, with no implied complete window. Never create/repair/rotate/delete source files. Returned file revision SHA binds exact bytes inspected. Empty/missing files differ from zero successful tools. Report scanned/retained/omitted/malformed/unknown counters, oldest/newest observed timestamp (null if missing), truncated flag and coverage limitations. Default100/max200 rows; exact full reply budget default32KiB/max64KiB/min1024; retain only metadata allowlist and aggregate within read bounds.

Project adapter tool_attempt/tool_completion into distinct stages keyed by runtime observation ID, preserving rows without matching attempts/completions (rotation is not success). Actor/activity/outcome/dispatched/completion_known/time/duration/response_bytes/source generation/descriptor revision are nullable unless evidenced by a recognized valid field. Preserve unknown older observation rows; never infer success from presence, timestamps from file metadata or completion from cancellation. Optional historical verdict enum useful/situational/dead is separate from execution outcome. Verdict freshness reports unknown when required revisions/expiry are absent, expired when explicit expiry elapsed, stale when its cited provider/descriptor differs from latest observed revision for that tool, otherwise matches_last_observed (never claiming actual current deployment). No body/text/argument/response content passes through, even in old/malformed rows. Counts describe observed native work only; no productivity, usefulness or billing estimate is synthesized.

No second durable collector/API writes. Sessions is a reader of runtime diagnostics; explicit host configuration owns access, and existing native sessions APIs remain host-trusted. Latest observed revision is evidence local to retained records; reports cannot attest unseen tools, uninstrumented Lua/direct calls, historical omission or remote effect rollback. Runtime fault diagnostics unrelated to tool observations are excluded. Source read failure affects only report, never an execution operation.

## Acceptance

- [x] Actual runtime mixed native fixture produces a diagnostic file, then real sessions SDK process reports all actor/activity and outcome distinctions without bodies; collection requires verified runtime adapter.
- [x] Legacy missing fields/expired or changed-revision verdicts and orphan completions remain explicit unknown/stale; report never invents billing or time.
- [x] Row/file/output caps, malformed/trailing/rotated/symlink/unstable inputs and request path override preserve source bytes and return bounded explicit status.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just test sessions
```

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" just build sessions
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/sessions-mapping" cargo build --manifest-path .cartridge/workspace/Cargo.toml -p cartridge --bin cartridge
CARTRIDGE_TEST_BIN="$PWD/target/sessions-mapping/debug/cartridge" SESSIONS_BINARY="$PWD/target/sessions-mapping/debug/sessions" bun test ../sessions.ctg/.cartridge/tests/integration/observations.test.ts
```

Also run public just check sessions and verified-status @runtime/native-tool-observation-adapter before collection. Report source is host-configured; tests use disposable stores and synthetic secrets only.
