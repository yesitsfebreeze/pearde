---
state: open
origin: requested
priority: 60
complexity: 0
blast-radius:
needs:
  - command-adapter
---

# launch-authority — Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown.

Discovery, direct, resolver and nested launches use trusted host-resolved policies while preserving scoped wire behavior and descendant teardown.

## Implementation handoff

host-owned policy across discovery and every launch

Complexity 38; blast-radius high. Owns `src/cartridge.rs`, `src/loader.rs`,
`src/lua.rs`, `src/sdk.rs`, `src/main.rs`, optional `src/broker.rs`,
`src/tests/mod.rs`, `src/tests/process.rs`, `src/tests/sandbox.rs`,
`src/tests/wire.rs`, `src/tests/resolver.rs`, `src/tests/node.rs`, and
`src/tests/fixtures/nested_fixture.rs`. Backend files and Cargo manifests are
outside this owner. Apply launch-integration.patch here.

Route discovery hello, direct apply, resolver up/enter, and nested spawn through
trusted host-owned command creation. Resolve installed identities and grants
at the host; never accept caller-supplied policies or arbitrary commands for
privileged execution. Associate child requests with the caller's authenticated
logical scope. Preserve private child services, correlated replies, events,
reload, startup diagnostics, and descendant teardown on parent exit/disposal.
The physical process tree may be host-owned while dependencies stay nested.

The build hit this owner at six red recursion tests and independently reproduced
hello/up/enter bypasses. Completion requires the three real-binary bypass probes,
existing wire tests, distinct-grant nested tests, forged-request refusal, and
all applicable project tests. Python broker success closes no Rust integration
acceptance requirement.


Source snapshots and verified probes are listed in `../report.md` under Exact source handoff. Apply only this child's files from those patches; preserve unrelated changes.

## Port integration requirement

The user is porting real sibling cartridges from /Users/feb/dev/sys. builtin/agent/main.rs:46 and builtin/router/main.rs:288 require SDK Host::on_reload with Fn(bool) returning Future<Result<Value>>. Restore the public registration method over existing reload-map/dispatch machinery, preserve both prepare_reload behaviors, and add a meaningful dispatch regression test. This is explicitly authorized runtime integration, not unused speculative API. Coordinate with the quality correction lane before touching src/sdk.rs.
