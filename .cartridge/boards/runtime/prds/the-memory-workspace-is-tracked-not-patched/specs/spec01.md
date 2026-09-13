---
complexity: small
footprint:
  - .cartridge/tests/integration/source-layout.test.ts
  - .cartridge/tests/unit/src/tests/folders.rs
---

# spec01 — Prove the recorded separate memory checkout

Clone the composed Git HEAD and initialize all recorded submodules recursively
using each existing local repository as an object source. Keep .gitmodules and
its remote URLs intact; fixture-local URL overrides avoid network dependence.
Verify memory's HEAD matches the root gitlink, its Cargo adapter dependency
resolves to sibling cartridge.ctg, and builtin/memory resolves to memory.ctg.
No vendor import, source patches, global Git configuration or existing stores.

The ordinary runtime test includes a metadata/layout probe. An explicit full
proof builds memory_cartridge from the fresh snapshot with the existing public
recipe, locked dependencies and cartridge feature, wrappers disabled and a
fixture-owned target. Record root/memory revisions, module count, SDK owner,
binary digest and build duration. Clean up only the temporary clone.

## Acceptance

- [x] Recursive fixture checkout retains the pinned memory commit and sibling SDK dependency with no legacy source bootstrap.
- [x] The full proof builds memory_cartridge from that checkout through just build memory --locked --features cartridge --bin memory_cartridge.
- [x] Original memory worktree registrations and source revisions remain unchanged; runtime test selection includes the cheap layout fixture.

## Verify and Proof

```sh
CARTRIDGE_SOURCE_LAYOUT_BUILD=1 bun test ./.cartridge/tests/integration/source-layout.test.ts
cargo test --lib recorded_memory_layout_uses_the_separate_submodule
```

The source-layout assertion is included in `just test runtime`. Network provider
or memory store access is unnecessary; only build dependency retrieval may occur.
