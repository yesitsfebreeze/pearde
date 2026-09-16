---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: process-introspection-cartridge
---

# A live process is inspectable from the agent

Debugging a running process from this composition means shelling out to whatever the machine happens to have and parsing its output by hand. Port pi's `mem` as `proc.ctg`: memory maps, reads, writes and searches against a live process, register reads, attach and detach, child process inspection, and a leak-checker runner, behind one surface that works the same on Linux and macOS.

The platforms differ underneath — `/proc` on Linux, the system memory and debugger tools on macOS — and the surface hides that. Where a platform cannot answer an operation, it fails open with a message naming the operation and the platform, never a silent empty answer that reads as "nothing found".

Writing to another process's memory and stopping another process are the dangerous half. Both are decided by `policy.ctg` before they happen, and neither is available without that decision.

## Acceptance

- [ ] Map, read, search, register and child-process operations answer against a fixture process on the running platform, and each names the platform mechanism it used.
- [ ] An operation the running platform cannot support reports that with the operation and platform named; no operation returns an empty answer to mean unsupported.
- [ ] Attach stops the target and detach resumes it, verified by the target making no progress while attached and resuming after.
- [ ] A memory write and an attach are each refused unless `policy.ctg` allows them, and the refusal names the operation.
- [ ] The leak-checker runner reports its status and its findings, and reports the checker being absent from the machine as absent rather than as a clean run.
- [ ] Every operation is tested against a disposable fixture process in `just test proc`, and the suite skips with a named reason on a platform that cannot host it.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/mem/` (1132 lines at survey, verified present: `index.ts`, `darwin.ts`, `linux.ts`, `procs.ts`, `shared.ts`). Renamed from upstream's `mem` because `memory.ctg` already owns that word in this composition and two surfaces answering to the same name is the collision this composition refuses elsewhere.

Lowest priority of the new cartridges: the mechanism is valuable and nothing else in the composition offers it, but no other child depends on it.

Gates, cwd `/Users/feb/dev/cartridge`: `just test proc`, `just check proc`. Not run for this plan.
