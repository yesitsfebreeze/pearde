---
complexity: medium
footprint:
  - .cartridge/tools/memo-run
  - .cartridge/memos/routine/cartridge-development.md
  - .cartridge/tests/integration/memo-run.test.ts
---

# spec01 — Build and execute each lane's own source

The public development recipe recognizes a Git worktree by its `.git` file.
For those checkouts it overrides inherited shared Cargo target paths with the
lane's own target directory and disables both Rust compiler wrapper settings.
Ordinary source checkouts keep their configured build behavior. Memo execution
resolves the nearest `.cartridge` owner, including PRD lanes nested beneath
another repository's `.cartridge` directory. No global configuration changes.

Use two disposable Git worktrees of a dependency-free crate named cartridge.
They share crate metadata but commit distinct output strings. Build each twice
through the actual development routine with a shared target environment and a
wrapper that would fail if invoked; execute the emitted binaries and require
the correct worktree output. Record cold/warm timings, source commit/tree,
source digest, binary digest and toolchain identity. A separate opt-in run uses
the configured real wrapper and direct isolated targets for comparison; a small
passing fixture does not prove the wrapper correct for the historical workspace.
The safe public path disables it because that broader property remains unproven.

## Acceptance

- [x] Nested memo paths select the lane owner and preserve command arguments and failures.
- [x] Both divergent worktrees execute their own outputs on cold and warm public builds, despite inherited shared target and wrapper settings; no shared output or global configuration is changed.
- [x] Real-wrapper comparison and wrapper-disabled results retain timing, source and binary identities; an incorrect safe build fails the test.

## Verify and Proof

```sh
bun test ./.cartridge/tests/integration/memo-run.test.ts
```

The runtime development gate already executes this file. Keep disposable build
outputs inside each fixture and remove only the fixture root at cleanup. Retain
the optional comparison JSON in the linked PRD evidence after measurement.
