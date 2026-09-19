---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/cartridge.ctg/src/sandbox", "/Users/feb/dev/cartridge/cartridge.ctg/src/host", "/Users/feb/dev/cartridge/cartridge.ctg/src/loader", "/Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests", "/Users/feb/dev/cartridge/cartridge.ctg/docs", "/Users/feb/dev/cartridge/cartridge.ctg/README.md", "/Users/feb/dev/cartridge/cartridge.ctg/.cartridge/help.md"]
---

# Contractor workers receive immutable job capabilities

The host launches a separate contractor composition under a minimal staged root, immutable grants and a private broker. This extends existing confinement rather than treating a session, worktree or prompt as a sandbox. The proposed native worker launch/status/cancel surface is host-owned; final naming is resolved against existing host APIs before code changes.

## Acceptance

- [ ] A worker reads and writes only declared staged inputs and outputs; direct, symlink, traversal and broker-mediated access to a second file is denied.
- [ ] The worker receives no generic host token, shared service sockets, provider credentials or external networking. Broker checks bind event, operation, parameters, resources and authenticated job identity.
- [ ] Unsupported confinement refuses launch. Expired grants, cancellation and deadlines stop only the owned process tree and revoke its broker access.
- [ ] A fake inference provider works through the broker while a direct network attempt fails; minimal runtime libraries are explicitly distinguished from project data.

## Proof and recovery

Start with `src/sandbox/mod.rs`, `src/sandbox/linux.rs`, `src/host/process.rs` and `src/host/socket.rs` in cartridge.ctg. The existing sandbox includes its root in readable paths, and macOS nonempty network grants permit broad access; staging and an empty network grant are mandatory. Create a disposable two-file fixture in the host integration suite, then add the native launch boundary and broker tests. Narrow the listed discovery footprint before implementation. Run `env -u CARTRIDGE_YOLO ./task test runtime`, `./task check runtime` and `./task isolation` from the composition root. Probe macOS first; each advertised platform must pass equivalent isolation tests, otherwise explicitly refuse that platform. Preserve a failed attempt's receipt; never fall back to an unrestricted process.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../../../root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
