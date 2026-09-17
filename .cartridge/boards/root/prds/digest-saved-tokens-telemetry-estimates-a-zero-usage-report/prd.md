---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/fs.ctg"
footprint:
  - "src/worker.rs"
  - ".cartridge/tests"
---

# digest saved-tokens telemetry estimates a zero usage report

## Outcome

A `digest` answer's `saved` block reports a real estimate when the worker model reports a zero-valued usage object, instead of `tokens_returned: 0` with `ratio: 1.0`.

## Reason

`fs.ctg/src/worker.rs:188-199` reads `reply["usage"]["completion_tokens"]` and falls back to `text.len() / 4` only when the field is missing. Endpoints that report a zeroed usage object (observed 2026-09-16 with the `glm-5.3-cloud` worker: `usage: {completion_tokens: 0, prompt_tokens: 0, total_tokens: 0}`) are trusted as literal zero, producing `tokens_returned: 0` and `ratio: 1.0` — a claim that reading nothing back saved everything, which an integration `digest` check (`worker.rs:227-229`, `ratio <= 0.0` fails) would also misread.

## Acceptance

- [ ] `completion_tokens` that is missing or zero falls back to the `text.len() / 4` estimate in `saved.tokens_returned`; a positive report is used as-is.
- [ ] The raw `usage` passthrough is unchanged — the estimate touches only the `saved` block.
- [ ] `fs.ctg` unit tests cover missing, zero and positive usage values.
