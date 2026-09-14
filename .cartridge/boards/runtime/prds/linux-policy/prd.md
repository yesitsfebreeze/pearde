---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: linux-policy
---

# linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.

Today `src/sandbox_linux.rs` refuses every cartridge ("not implemented"), so no
cartridge runs on Linux. Implement `linux::command` to give the same grant
semantics as the macOS profile in `src/sandbox.rs`: implicit plumbing (the
binary, its interpreter, the cartridge folder, runtime libraries), the host's
socket directory, and System V/POSIX semaphores for LMDB (81a138e, 92b7a5d).
Everything else comes only from `read`/`write`/`exec`/`net`.

Runner: this workstation has an active OrbStack Docker context (`docker context ls`)
and Lima installed. Step one runs a disposable Linux container and records
`uname -r`, the Landlock ABI and seccomp availability. Stop condition: if the
ABI lacks filesystem rules, or TCP rules (ABI 4) for the network check, record
that and keep this item blocked. A compile-only result proves nothing.

## Acceptance

- [ ] A real Linux child proves allowed and denied read/write/exec, denied TCP/UDP under an empty `net`, a working socket in the host's socket directory, no inherited stray descriptors and no-new-privileges.
- [ ] An unsupported ABI or a failed policy install refuses before cartridge code executes; no partial policy is used.
- [ ] Cross-compilation results are reported apart from runtime enforcement.

## Proof and recovery

Add cases to `.cartridge/tests/unit/src/sandbox/tests.rs` under
`cfg(target_os = "linux")`. In the container run `cargo test --workspace` in
`cartridge.ctg`, and on the host run `just check runtime` from
`/Users/feb/dev/cartridge`. Record kernel, ABI, revision and output. Until
enforcement passes, the existing refusal stays the fallback.

## Dependencies and review

No hard prerequisite. [Review](review.md): round 3/5.
