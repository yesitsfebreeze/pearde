---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
capability-owner: runtime
work-kind: leaf
footprint:
- "cartridge.ctg"
- "cartridge.ctg/src/host/process.rs"
- "cartridge.ctg/src/host/mod.rs"
- "cartridge.ctg/src/node"
- ".cartridge/tests/integration/takeover.test.ts"
---

# A node exits when its host dies

## Outcome

When a `cartridge daemon` ends for any reason, including SIGKILL or a crash, none of its
`cartridge node` children keeps running. A stop of a host with idle nodes also returns
promptly instead of waiting out `shutdown_timeout_secs`. Today every node runs in its own
process group (`cartridge.ctg/src/host/process.rs:146`), and the only reaper is
`Group::drop` (`:275-283`), which never runs when the daemon is SIGKILLed. On 2026-09-16,
test and smoke runs left 20 orphaned nodes (ppid 1, cwd in deleted temp roots).
Stop → `Running::stop` (`process.rs:255-261`) waits the full dispose timeout (15 s)
because nodes don't answer `dispose` promptly.

## Acceptance

- [ ] An isolated test SIGKILLs a daemon with running nodes and asserts no `cartridge node` of that root survives after a bounded wait (a few seconds), by EOF on the node's control pipe or a parent-death watch.
- [ ] SIGTERM to a daemon whose nodes are idle exits in well under `shutdown_timeout_secs`, asserted by the same test file.
- [ ] Stale per-pid runtime dirs of a killed host are swept on the next start.
- [ ] `just check cartridge`, `just test cartridge` and `just test lifecycle` exit 0.

## Proof and recovery

Found by the smoke implementer for `@root/smoke-passes-mcp-and-proxy`
(`.state/loop/smoke-passes-mcp-and-proxy/defect-stop-leaves-nodes.md` has the evidence).
The smoke fixture reaps its own processes in the meantime.
