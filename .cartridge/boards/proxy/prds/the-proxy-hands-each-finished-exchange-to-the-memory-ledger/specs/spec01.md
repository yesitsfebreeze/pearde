---
complexity: low
footprint: ["cartridge.json","src/service.rs","src/wire.rs",".cartridge/tests/unit/tests.rs",".cartridge/tests/unit/wire/tests.rs",".cartridge/docs/README.md"]
---

# Send each completed exchange to the configured ledger key

Baseline at proxy.ctg `3380f34`: `Service::request_for_principal` records
usage, trace and context metadata, and sends nothing to memory beyond the
`memo context` recall.

## Contract

- **Setting.** `ledger: string` defaults to `""`. The `needs` list gains
  `${config.ledger}`, which the host drops when it is empty.
  `Config.ledger: String`.
- **Text.** `wire::output_text(response, wire) -> String` returns the
  assistant text of a final response:
  - Chat: `choices[].message.content`.
  - Anthropic: `content[]` blocks of type `text`.
  - Responses: `output[]` messages' `output_text` parts.

  `wire::last_user_text` already gives the request side.
- **Send.** When `ledger` is non-empty, `request_for_principal` takes the
  newest user text before `run` consumes the body. On `Ok(value)` it calls
  `tokio::spawn` with a 10-second timeout around
  `call(ledger, {op: "ledger", action: "append", ts, wire, user, response})`.
  `ts` is Unix milliseconds and `wire` is `chat`, `responses` or `anthropic`.
  It sends nothing when both texts are empty. An error or timeout prints one
  `{"type":"proxy_ledger_degraded"}` line. The response value is returned
  unchanged and never waits on the send.

## Acceptance

- [x] For each of chat, anthropic and responses, a completed request with
      `ledger = "memory"` produces exactly one `memory` call with action
      `append`, the request's user text and `"answer"` as response.
- [x] A `memory` call that errors leaves the returned response equal to the
      router's final response.
- [x] With the default configuration no `memory` call is made.
- [x] `output_text` extracts the text of all three wires.

## Verify

```sh
set -eu
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/proxy.ctg/target
cargo test ledger
cargo test output_text
```

```sh
set -eu
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/proxy.ctg/target
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
```
