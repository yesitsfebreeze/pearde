---
state: open
origin: requested
priority: 60
complexity: 0
blast-radius:
needs:
  - the-manifest
  - the-resolver
---

# The sandbox

Every cartridge is a child process, so every cartridge gets a policy derived
from its own manifest: `sandbox-exec` on macOS — present on this machine,
deprecated but functional, verified working — and Landlock with seccomp on
Linux.

This is the newest requirement and the one the existing system does not have at
all. It is what turns "a sandboxed tool belt of things we can vibe code" from an
intention into a property of the machine. A cartridge written carelessly is
contained by what it declared, not trusted to behave, and the person writing it
does not have to be careful for the system to stay safe.

[[the-manifest]] is the policy. There is no second file and no separate grant:
what a cartridge asked for is both what it gets and the wall it hits.

Must not change: a cartridge that declares nothing gets nothing. The empty
manifest is the tightest sandbox, not the loosest.

At the end, a cartridge reaching outside its declared capabilities is stopped by
the operating system rather than by review.

## Questions

### Q1: What a network grant means when the wall cannot name a host

A network grant is all-or-nothing on this machine: the wall can leave
networking off or open it to every host, but it cannot name one host and keep
the rest shut. A cartridge asking for one service would get every host — more
than it declared. What should a network grant mean?

1. **Open when named** — whatever the grant names, the network opens; an empty one keeps it shut. The gap is stated where the wall is built. (recommended)
2. **Refuse to run** — a cartridge naming hosts does not start; nothing gets more than it declared, and network users wait for a finer wall.
3. **Pin at spawn** — the host resolves each named host once and opens only those; precise, but it breaks when an address changes.

<!-- for the board: src/sandbox.rs profile() renders net as `(allow network*)` + `(allow system-socket)` when grant.net is nonempty; src/loader.rs Grant.net carries the declared hosts verbatim; `sandbox-exec` remote filters reject any host but * and localhost ("host must be * or localhost in network address"). The answer decides whether the loader refuses documents whose net names hosts, and lands in the-sandbox spec01. -->

### Q2: Who starts a nested cartridge when a wall cannot build a wall

A cartridge that hosts cartridges is itself confined, and this machine's wall
refuses to apply a second, different policy from inside one — the nested child
cannot even be started, so every recursion fails today. What should a hosting
cartridge's children be?

1. **The host starts every child** — a nested cartridge asks the host above it to start its children, each keeping its own policy. (recommended)
2. **Children inherit the wall** — a child runs inside its parent's policy, no second wall; the declaration binds only direct children.
3. **Nested runs bare** — a hosting cartridge starts children unconfined, as the code does today; recursion works, but every grandchild is trusted, not contained.

<!-- for the board: the two spawn paths are src/cartridge.rs start (sandbox::spawn, walled) and src/sdk.rs host.spawn (plain tokio spawn, never walled — a contract hole this answer closes either way); the six red wire recursion tests in the lane tree (src/tests/wire.rs) are the manifestation; probe/the-nest-fork.sh facts 3 and 4 pin the platform (same profile re-applies, any different profile is sandbox_apply EPERM); the answer decides whether a spawn frame joins the wire (the-wire) and lands in the-sandbox's nest spec. -->

## Answers

**Q1** *(answered 2026-09-12 20:37)* — Open when named — the wall on this
platform cannot name a host (a remote filter rejects every host but `*` and
`localhost`), so a nonempty `net` opens the network and an empty one keeps it
shut. The gap is stated in the wall's own module doc; the hosts a grant names
are recorded and carried, not enforced. Settled by the answerer's delegation
("what would you do, do research") and pinned by `probe/net.sb` and
`probe/the-nest-fork.sh` fact 1.

**Q2** *(answered 2026-09-12 21:12; delegated decision resolved 2026-09-12)* —
The trusted host starts every cartridge, including discovery and nested
cartridges, from a host-resolved installed identity and its own manifest.
Service calls still follow the logical nested wire, and disposing a parent
stops its descendants. A child cannot supply a replacement policy or ask the
host to launch an arbitrary program. The physical process tree may be owned
by the host while the dependency and lifecycle tree stays nested.

The user delegated this choice to research. The local broker probe passed six
checks with distinct parent and child policies; applying a different sandbox
inside a confined macOS process still fails. Linux restrictions inherit and
only tighten, which also prevents a nested process from acquiring a grant its
parent lacks. Host-owned spawning preserves each cartridge's own manifest
without widening the parent. Evidence: `probe/broker.py`,
`probe/the-nest-fork.sh`, and record [[260912-9ec4]].

## Children

| child | contract | needs |
|---|---|---|
| `command-adapter` | A shared fail-closed command constructor carries manifest policy into synchronous and asynchronous launches without changing existing callers. | — |
| `macos-policy` | macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests. | command-adapter |
| `linux-policy` | Linux commands install Landlock and seccomp before execution, enforce declared capabilities, and refuse unsupported confinement. | command-adapter |
| `launch-authority` | Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown. | command-adapter |
