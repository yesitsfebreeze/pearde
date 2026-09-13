---
complexity: medium
footprint:
  - init.lua
  - .cartridge/tests
  - .cartridge/memos/routine/policy-tests.md
  - .cartridge/docs/policy.md
---

# spec01 — Optional operation rules with explicit deny precedence

Add operations={tool={operation=decision}} to the existing pure policy config.
Validate the complete configuration before publishing. Tool deny and operation
deny win; otherwise a specific operation overrides the tool rule, then existing
built-in/default decisions apply. Known GitFS/memo/memory operation names are
validated; unknown operations are denied even under blanket tool allow. Existing
profiles retain existing defaults; additional supported memory operations remain
denied until explicitly configured. No runtime containment change.

## Acceptance

- [x] Table fixtures prove operation/tool/default precedence, unknown operations, unchanged legacy profiles and independent memory mutation rules.
- [x] Real policy decisions used by MCP, proxy and the native Agent driver agree for read allow/write deny; a denial executes zero tool mutations.
- [x] Invalid replacement configuration leaves the prior valid policy callable, with no partially installed rules.

## Verify and Proof

```sh
bash .cartridge/tests/run
```

A policy-owned Rust test crate uses the real runtime/Lua policy, actual MCP/proxy
processes and native Agent library with a deterministic driver. Fake services own
only session persistence, harness/router and mutation counting. No model service
or user data is accessed. The runner builds from local sibling sources into its
own target with compiler wrappers disabled, and the package lock is committed.
