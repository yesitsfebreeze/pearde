---
kind: work
description: "Budget context with cached prefix summaries"
status: done
needs:
  - "[[@prd/work/harness--harness-plugin.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["Conversation context exceeds its budget or a summary must preserve complete tool-call groups without rewriting history"]
---

# safe-transcript-compaction

## Do

Extend harness with `compact {session,descriptors}` and automatic compaction during context assembly. Inject router for summarization only. Persist summaries as replaceable derived context in a separate session buffer. Transcript remains authoritative. Keep complete recent turns and tool-call/result groups; never split a pair to fit a byte limit. Summary content is conversation data, not new system instructions. Budget includes system, tools, tail, summary and response reserve. No tokenizer dependency or additional plugin.

This memo owns only the bounded unit below; linked prerequisites own their implementations. Agent separation follows [[agent-is-a-separate-plugin]].

## Spec

Planning status: proposed specification based on source inspection. No implementation probe or code tests have run. Keep every acceptance box unchecked until verified. File footprint: `plugins/harness/`.

Choose a closed prefix ending at a completed conversational turn, retaining at least the latest configured number of complete turns (default 4). Never compact an incomplete tool group. Summarize through router request on Chat with tools omitted and explicit delimiters; ask for facts, decisions and unresolved work, not obedience to quoted instructions. Store derived summary metadata with the exact prefix endpoint and content hash. Preserve journal bytes. Reuse only summaries matching that prefix; stale or malformed metadata forces regeneration.

Insert summary as labelled conversation context below system/project instructions, then the untouched tail. Bound summarization to one attempt per context call and a deadline. A single oversized turn or still-oversized summary returns context_over_budget; no infinite retries, chopped tool JSON or dropped history. Failure may fall back to original context only when it fits. Cancellation must not persist a half-summary. Concurrent appends do not invalidate a prefix summary but must be included in the final projection; reread the revision and rebuild the tail before returning.

## Check

- [x] Complete recent turns and every tool-call/result group remain intact.
- [x] Transcript bytes remain identical after success, cancellation and summarizer failure.
- [x] Matching prefix summaries are reused; changed prefixes force regeneration; concurrent appends remain in returned context.
- [x] Projected request plus reserve fits budget or fails after at most one summary attempt.
- [x] Huge single turns, malformed summaries and router timeouts fail without history loss; summary never becomes a system instruction.

Verification commands (future implementation gate; not run during planning):

```sh
set -eu
cargo test --manifest-path plugins/harness/Cargo.toml
cargo clippy --manifest-path plugins/harness/Cargo.toml --all-targets -- -D warnings
```

## Result

2026-09-09 21:55 — compaction landed on work/safe-transcript-compaction (629c78e); 5/5 checks, 19 harness tests, just all green
