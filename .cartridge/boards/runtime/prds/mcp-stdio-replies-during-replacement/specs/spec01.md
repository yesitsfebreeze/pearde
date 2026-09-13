---
complexity: small
footprint: ["src/main.rs",".cartridge/tests/unit/stdio.rs","src/loader.rs"]
---

# spec01 — Preserve request correlation on bridge failure

Factor a reply selector used by the actual stdio bridge. Preserve successful
non-null provider replies. On bridge failure retain stderr diagnostics, and
return JSON-RPC -32603 for a request with its original non-null ID. Notifications
and incoming responses receive no response. Malformed JSON receives -32700 with
null ID. Send through the existing single stdout writer; never replay the call.

## Acceptance

- [x] Focused tests cover string/numeric IDs, successful replies, null results, notifications, responses and malformed input.
- [x] The existing live MCP fixture observes addition/removal without a dropped response after this source change is integrated.

## Verify and Proof

```sh
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= cargo test --manifest-path Cargo.toml --bin cartridge mcp_bridge
```

The dependent MCP leaf runs its full real stdio integration gate after this
source commit is integrated. Its fixture initially proved this exact failure.
