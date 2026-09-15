---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
---

# Preserve actionable provider, quota, timeout, configuration, and lifecycle failures in answer responses.

## Do

Refactor `src/rpc/src/ask.rs` to preserve the error category and bounded safe message from completion, extraction, follow-up recall, and lifecycle refusal. Distinguish provider quota or rate limit, unavailable model, endpoint failure, timeout, invalid configuration, shutdown, and absent runtime. Do not leak credentials, signed URLs, or unbounded provider bodies. Keep partial-recall behavior only where the contract deliberately permits it; no silent empty result may conceal a failed dependency.

## Acceptance
Focused RPC tests inject every category and assert distinct, redacted responses. A provider 429 never returns the endpoint-up hint; shutdown never returns a provider error; malformed provider text remains bounded. Existing successful answer-loop tests pass.

Landed: `LlmError::category` and `llm::reported` — the bounded, URL-redacted
`safe_reason` paired with a stable category — in `src/llm/src/llm.rs`, and
`ask::invoke` naming the leg that failed in `src/rpc/src/ask.rs`. The extract
leg keeps the degrade its own doc states; a lifecycle refusal there and a
follow-up recall that errored now end the run instead of becoming an empty
fact set. The endpoint-up hint survives only for `endpoint_failed`. Seven
tests in `src/rpc/src/tests/ask_failure_test.rs`.
