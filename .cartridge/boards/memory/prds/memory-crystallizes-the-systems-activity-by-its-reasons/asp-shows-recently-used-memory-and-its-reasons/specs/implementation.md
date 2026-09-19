---
footprint:
  - src/cartridge/src/asp
  - src/rpc/src/experience/view.rs
  - src/rpc/src/server.rs
  - cartridge.json
---

# Implementation contract

The reviewed parent PRD owns the behavior and failure semantics. Changes stay inside the listed memory-owned paths and the behavioral test fixtures that exercise them.

## Acceptance

- [ ] The acceptance checks in ../prd.md are verified on the integrated checkout.
- [ ] Concurrent edits remain intact, and the standalone package boundary is preserved.

## Verify

```sh
cargo test -p memory_cartridge asp
cargo test -p rpc experience
```
