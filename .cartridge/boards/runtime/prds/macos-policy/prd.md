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
canonical-scope: macos-policy
---

# macos-policy — macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests.

The wall ships already. `src/sandbox.rs` builds a `(deny default)` profile for
`sandbox-exec` from the grant. It writes canonical path spellings, escapes them
in `literal()`, documents all-or-nothing networking, and allows the implicit
runtime lines. The proof is thin: only `the_synchronous_command_enforces_the_empty_grant`
runs a real child, and every other test in
`.cartridge/tests/unit/src/sandbox/tests.rs` checks profile text. This item
supplies the missing behavioral proof and justifies each runtime exception.

## Acceptance

- [ ] Real children prove: a granted write succeeds and an ungranted one is denied, a read outside the grant is denied, a granted exec runs and an ungranted one is denied, and a script runs through its interpreter.
- [ ] An empty `net` denies a real TCP connect; a nonempty grant allows it (the documented coarse limit); a path containing a quote or backslash yields a profile `sandbox-exec` accepts, without widening access.
- [ ] Each implicit allowance (`/usr/lib`, `/System/Library`, `/dev`, `/etc`, metadata, semaphores, `sysctl-read`, `mach-lookup`, `process-fork`) is tied to a child operation that fails without it, or gets a recorded reason. A boot failure never counts as a denial pass.

## Proof and recovery

Add cases to `.cartridge/tests/unit/src/sandbox/tests.rs` using the existing
`wall_fixture` pattern. Gates, from `/Users/feb/dev/cartridge` on macOS:
`just test runtime` and `just check runtime` (not yet run). Record the `just smoke` baseline first: mcp and proxy already fail
(release-status note). Remove an unjustified allowance only if smoke shows no
new failure against that baseline. Otherwise it stays, with its reason recorded.

## Dependencies and review

No hard prerequisite. [Review](review.md): round 3/5.
