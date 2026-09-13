---
state: open
origin: requested
priority: 60
complexity: 0
blast-radius:
needs:
  - command-adapter
---

# linux-policy — Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.

Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement.

## Implementation handoff

install Landlock and seccomp before cartridge execution

Complexity 30; blast-radius high. Owns `src/sandbox/linux.rs`, `Cargo.toml`, and
`Cargo.lock`, with tests inside the backend module. Replace Unsupported with
kernel policy installation before untrusted instructions run. Cover filesystem
operations, execution, inherited descriptor handling, empty-network TCP/UDP
restrictions, and syscalls that could bypass the filesystem policy. Set
no-new-privileges and refuse unsupported facilities or failed policy setup.
Do not silently weaken required guarantees to fit an older kernel. Preserve
Q1's declared network semantics.

The build hit this owner at the unconditional refusal and unavailable Linux
runner. Require actual Linux positive/negative filesystem, execution and
network tests, deliberately unsupported-facility refusal, and recorded kernel
and Landlock ABI. A cross compile is a separate check, never enforcement proof.


Source snapshots and verified probes are listed in `../report.md` under Exact source handoff. Apply only this child's files from those patches; preserve unrelated changes.
