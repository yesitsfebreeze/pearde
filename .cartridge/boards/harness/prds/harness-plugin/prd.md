---
repo: /Users/feb/dev/cartridge/harness.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: harness
work-kind: leaf
needs:
- "@root/process-plugins-register-through-lua-lua-registration"
- "@sessions/session-transcript-durability-run-checkpoint"
---

# Deterministic instruction and Chat request projection

## Do

Provide harness from a Lua-registered Rust process. Inject sessions and buffers, not arbitrary tool keys. The agent gathers describe results from its configured injected tools and passes descriptors to `harness {op:"context",session,descriptors}`. Return `{system,messages,tools}`: system text is separate, messages excludes that system message, and tools uses Chat `{type:"function",function:{name,description,parameters:input_schema}}`. The agent prepends system exactly once. Raw descriptors are not already Chat-shaped.

Own instruction discovery, transcript projection and budget validation, not model execution, permissions or transcript mutation. Compaction is a later extension in safe-transcript-compaction; initially an oversized request returns context_over_budget. Read the journal defined by session-transcript-durability through buffers. Missing storage fails explicitly.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/harness/`, `plugins/harness.lua`, `Cargo.toml`, `Cargo.lock`.

Create the harness crate and wrapper. Get trusted cwd and transcript buffer via sessions/buffers. Read configured base system prompt, walk ancestors from cwd to filesystem root, collect existing CLAUDE.md and AGENTS.md, and order root-to-leaf. Label sections with canonical paths and deduplicate canonical files. Include cwd and current date from an injectable clock. Bound each instruction file at 64 KiB and all instructions at 256 KiB; unreadable, invalid UTF-8 or oversized discovered files yield named errors rather than silently stripping instructions.

For the nearest ancestor containing `.cartridge/memos/SYSTEM.md`, include SYSTEM and `.cartridge/memos/system/memo-layout.md` as required by this record's startup contract. Do not recursively load all links or the whole record. Read sources only; never regenerate indexes.

Project journal message records to Chat messages in order; ignore lifecycle records. Refuse malformed records and unresolved tool-call groups at a model request boundary. Convert raw descriptors into function tools without changing schemas; reject duplicate names or malformed schemas. Count serialized request bytes for a configured conservative budget, reserving output headroom, and return context_over_budget when exceeded. Bytes are not exact tokens. No persisted history rewrite.

Port selected agent-instructions behavior and regression cases from [[deepseek-plugin-port-map]]; preserve source/license notices for adapted code. Escape or encode repository-controlled framing delimiters while retaining readable source labels. Rebuilding context or resuming must not duplicate instruction blocks. Byte-limit checks handle multibyte UTF-8 correctly. Nested instructions discovered after file access are deferred; this slice covers session-cwd ancestry only, not arbitrary shell command inference.


For source or tests substantially adapted from [[deepseek-plugin-port-map]], include package-local UPSTREAM.md naming source paths/revision and UPSTREAM_LICENSE containing the full MIT notice; package/distribution checks must retain them.

## Acceptance
- [x] Framing-delimiter content remains labelled data; multibyte boundary tests stay valid UTF-8; repeated context/resume includes each instruction source once.

- [x] Temporary ancestor trees verify root-to-leaf order, labels, deduplication, supplied date and nearest-record startup files without unrelated memos.
- [x] Missing optional files are skipped; unreadable, binary or over-limit discovered files produce errors.
- [x] A journal with user, assistant tool call, tool result and final assistant projects valid ordered Chat messages without lifecycle records.
- [x] Descriptors become function tools with parameters=input_schema; duplicate names and malformed schemas fail.
- [x] Oversized context returns context_over_budget without changing transcript bytes.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/harness/Cargo.toml
cargo clippy --manifest-path plugins/harness/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-09 20:45 — harness plugin landed on work/harness-plugin (ecc1ac7, f7f1bba); 6/6 checks, 10 unit + 1 integration test, just all green
