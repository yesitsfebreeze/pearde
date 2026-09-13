---
complexity: medium
footprint:
- src/loader.rs
- .cartridge/tests/unit/src/tests/mod.rs
- .cartridge/tests/unit/src/tests/composition.rs
- .cartridge/docs/composition.md
---

# Share the active-generation replacement transaction at every depth

Source baseline8e514eac demonstrates two concrete lifecycle discrepancies through
the public Host API: root replace_node returns disposed oldUID4 after publishing
UID9, and returns Ok9 after rejecting a bad candidate; the nested equivalent
returns liveUID12 and Err. In both cases old service value2 survives rejection,
dependents keep their generations and shared router/PTY providers apply once.
The same prepare/drain/stage/switch/reject logic is duplicated in replace_entry
and swap_node. Fix this measured boundary; do not rewrite profile discovery,
resolver policy, SDK launch mediation or nesting to meet a grep-count quota.

Keep Host::load_component and Runtime context construction as the existing shared
creation primitives. Extract one private active-generation replacement helper
within loader.rs. It takes the resolved candidate, old handle, existing reload
transaction and composing context; both root and nested adapters use it. It owns
unique-process preparation, cancellation of prepared processes on refusal,
service-call draining, isolated candidate keys, settling/validation, atomic
Runtime::switch, candidate cleanup, transaction completion and old-generation
disposal. Publish caller bookkeeping synchronously at successful switch before
unlocking/disposing the old generation, preserving the root loaded-slot view.
Root keeps entry discovery/config/source stamps and failed-initial recovery;
nested keeps its existing rebuild closure and original parent/isolation/intercept
context. Those distinct adapters are required bookkeeping, not duplicate active
publication. Delete their duplicated active-publication blocks once routed
through the shared helper; identify both mapped callers in implementation proof.

Return Result with the actual current generation UID from replace_node at either
depth. Propagate candidate/rebuild/rejection failure rather than acknowledging it
as success; retain root diagnostic reporting and existing fire-and-forget reload
callers. Failed initial root entries still recover through the existing adapter.
Stable service references, parent and unrelated sibling generations, provided-key
validation and reload retry after a refused candidate remain unchanged. No caller
metadata changes scope, and no new arbitrary command or launch policy is added.

Preserve existing sharing and explicit isolation. One maintained fixture body
parameterized by depth0/1 composes the same provider/consumer logical entries,
uses explicit nested private realms, and calls the same public replace_node API.
It checks initial reachability; successful replacement returns the active new UID
and oldUID is retired; a second replacement using the returned UID works; failed
candidate returns Err and preserves the active UID/value; a corrected candidate
can then publish. At nested depth the private key is unavailable from root,
while the public adapter and shared router/PTY values remain reachable. Assert
shared providers apply once and dependent/parent/sibling generations stay stable.
Readiness uses bounded lifecycle waits, not fixed sleeps. Existing wire/process,
reload/migration refusal, isolation, recursive descendant teardown and foreground
fixtures remain required compatibility gates. The current shipped profile smoke
runs with actual providers and no user store mutation.

The referenced historical nested-entry memo is still active/unchecked and has no
canonical alias in the current work map. This plan resolves the needed current
replacement/private-scope behavior using actual source and fixtures; it does not
claim the historical memory bank/checkpoint/automatic child source-watch programme
complete. Those historical outcomes remain an independent follow-up for root to
map if within board scope. No bank, watcher, UID persistence or automatic provider
activation is introduced here. Current launch authority is preserved, without
claiming the separate launch-authority PRD is satisfied.

## Acceptance

- [x] The same parameterized real Host fixture reaches, replaces and refuses a bad replacement at depth0/1; successful replies name active generations, failed replies are errors, old values survive refusal, and recovery works without replacing dependents.
- [x] Explicit private child keys remain private while shared router/PTY providers apply once; parent/sibling generations and existing scope/isolation behavior remain intact.
- [x] Both root and nested active replacement adapters call one shared transaction; removed duplicate blocks have mapped callers and equivalent tests. Current default/foreground, Rust/Lua wire, reload and descendant teardown gates pass at the integrated source.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test runtime composition
just test runtime
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just check runtime
cargo build --manifest-path Cargo.toml --bin cartridge
bun test ./.cartridge/tests/integration/smoke.test.ts
```

Record exact source/binary hashes, parameterized fixture observations, changed
paths and shared-helper call-site map. Failed candidate checks must observe the
actual public reply and retained service value; a source grep alone cannot prove
semantic equivalence. Disposal remains owned by the runtime and no failed
candidate triggers automatic replay or import.
