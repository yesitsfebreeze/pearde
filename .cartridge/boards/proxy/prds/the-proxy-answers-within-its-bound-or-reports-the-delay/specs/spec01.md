---
complexity: 5
footprint:
  - /Users/feb/dev/cartridge/proxy.ctg/cartridge.json
  - /Users/feb/dev/cartridge/proxy.ctg/src/service.rs
  - /Users/feb/dev/cartridge/proxy.ctg/src/notice.rs
  - /Users/feb/dev/cartridge/proxy.ctg/.cartridge/tests/unit/tests.rs
---

# spec01 — A proxy stall names its stage, its elapsed time and its bound

## Scope

This spec closes **the proxy's side only**. The PRD's evidence names two
stalls. `harness did not answer in time` is the proxy's own downstream wait and
is addressed here. `mcp did not answer in time` is the *same* mechanism — a
provider whose manifest declares no `timeout_ms` — but the manifest that needs
one belongs to the `mcp` cartridge, outside this PRD's `repo`. It is owned by
**`@mcp/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound`**
(the parent `@mcp/a-cartridge-call-is-cancellable-and-bounded` has been refined
into a rollup and no longer holds the work). An analyst on that child
independently confirmed the symmetry: `mcp.ctg/cartridge.json` declares its
`mcp` event with no `timeout_ms` either, so every MCP line inherits the same
60000 ms default and fails as a bare `mcp did not answer in time`. PRD
acceptance 1 is therefore met for proxy-routed requests only; the PRD body
records the same split, and nothing here should be read as closing the `mcp`
half.

One further honesty note on acceptance 1's "the bound it exceeded". For the
proxy's own deadline this spec quotes the bound literally
(`proxy.timeout_secs = {}s`). For a downstream cartridge stall it reports the
**measured elapsed ms plus the knob name** (`event_timeout_ms`) rather than the
host's configured value, because no host RPC exposes host settings — see
"Deliberately skipped" below. That is a deliberate reading of the clause, not
an oversight.

## Base and dependencies

**The lane builds at HEAD, but not hermetically.** At `0692c18`
`Cargo.toml:17` carries `evidence = { path = "../memo.ctg/evidence" }`. The
engine cuts a lane at `prd.ctg/.cartridge/boards/proxy/.lanes/<slug>`, and that
`.lanes/` directory already holds two sibling symlinks — `cartridge.ctg` and
`memo.ctg`, both pointing at the live submodules — precisely so `../memo.ctg`
resolves from a lane. Probed by the coordinator: a worktree of `0692c18` at
`boards/proxy/.lanes/probe-2e`, `cargo check --lib` with an isolated
`CARGO_TARGET_DIR`, **exit 0 in 4.42 s**. The "lone worktree needs siblings"
hazard is already mitigated by those symlinks, so this spec needs no
prerequisite and no lane-provisioning step.

The real consequence is that **the lane compiles against another submodule's
working tree, not a pinned revision**: `../memo.ctg` is a symlink to the live
`memo.ctg`, which currently carries 39 uncommitted files
(`git -C memo.ctg status --porcelain | wc -l` → 39). A change landing in
`memo.ctg/evidence` between pass 1 and pass 2 changes what this spec compiles
against, in both passes, with nothing in the lane pinning it. Treat a cargo
failure that mentions `evidence` as a sibling-tree problem, not a defect in
this work.

(Superseded claim, recorded so it is not repeated: an earlier draft of this
spec said `proxy.ctg` is "a self-contained workspace with no path
dependencies". That is true only of the **uncommitted** tree, where the
dependency is removed in favour of the untracked `src/evidence.rs`. At HEAD it
is false.)

## Working tree warning (read before starting)

`proxy.ctg` is **dirty at `0692c18`** and two of the four footprint files
already carry uncommitted work. `git status --porcelain` at spec time:
`.cartridge/tests/unit/tests.rs`, `.cartridge/tests/unit/wire/tests.rs`,
`Cargo.lock`, `Cargo.toml`, `src/context.rs`, `src/lib.rs`, `src/notice.rs`,
`src/service.rs`, `src/wire.rs`, plus **untracked `src/evidence.rs`**.

- Every baseline number in this spec is now measured **at `0692c18`**, on a
  `git archive` extraction with a `memo.ctg` sibling present, not on the
  working tree. At HEAD `cargo test --lib` is **exit 0, 55 passed, 0 failed**.
- The `ends_with("did not answer in time")` branch at `src/notice.rs:51-53` of
  the working tree is part of that uncommitted work (`git diff src/notice.rs`,
  `@@ -48,6 +48,9 @@`). It does **not** exist at `0692c18`. This spec therefore
  puts `src/notice.rs` in the footprint and pins that branch with its own
  Verify grep rather than assuming it is there.
- **Landing hazard.** Collect fast-forwards the lane into `repo` with
  `git merge --ff-only` (`prd.ctg/src/lifecycle.ts:166` at `3ef3426b`), which **aborts
  outright** while `src/service.rs` and `src/notice.rs` are locally modified in
  `repo`. This is a hard constraint on *when* this work can land, not a reason
  to change the plan: the unrelated diff must be committed or stashed before
  collection, or the fast-forward fails after the code is already written.

## Baseline

Every line number below is at `0692c18`. What already holds there:

- The request is bounded. `src/service.rs:302-317` wraps `self.run(...)` in
  `tokio::time::timeout(Duration::from_secs(self.config.timeout_secs), …)` and
  maps elapse to `"proxy request deadline exceeded"`. `src/usage.rs:248-250`
  classifies that prefix as 504 and `src/notice.rs:27-28` turns 504 into an
  assistant-turn notice instead of a bare 5xx the client silently retries.
  Acceptance 2 holds on the HTTP path and is covered by
  `.cartridge/tests/unit/tests.rs:829` (`deadline_and_dropped_request_cancel_the_exact_active_tool`,
  `config.timeout_secs = 1` at `:832`) and by the streaming case at `:2110`.
- A retry is not blocked by any latch: nothing in `service.rs` records a
  failed request, and `notice::applies` only changes the *shape* of the reply.
  Acceptance 3 holds.
- The downstream cartridge is already named. The host formats a listener
  timeout as `"{from} did not answer in time"`
  (`cartridge.ctg/src/transport/cartridge.rs:95`), so a stalled harness call
  reads `harness did not answer in time`. The hint branch that recognises that
  shape and names `event_timeout_ms` exists in the working tree but **not** at
  `0692c18`; see the warning above.

What does **not** hold at HEAD:

- **No bound is ever quoted.** `"proxy request deadline exceeded"`
  (`src/service.rs:317`) carries no number, so the caller cannot tell whether
  it waited 60 s or 30 min, nor which setting to raise. Acceptance 1's "and the
  bound it exceeded" fails.
- **No stage is named for the proxy's own waits.** `run()` propagates every
  downstream error with a bare `?` — the harness injection call
  (`src/service.rs:661-665`), the provider round (`src/service.rs:741` live /
  `:743-747` router) and the tool call (`src/service.rs:785-787`). A caller
  sees the cartridge id but not which of the three waits overran nor how long
  it actually ran. Acceptance 1's "names the stage that overran" is only
  incidentally satisfied by the cartridge id.
- **An event-bus caller can never reach the proxy's own deadline.**
  `cartridge.json` declares the `proxy` event (`"events"` opens at
  `cartridge.json:14`, `"proxy"` at `:15`) with no
  `timeout_ms`, so `cartridge.ctg/src/host/plan.rs:299-301` applies
  `settings::host().event_timeout_ms` — default **60000 ms**
  (`cartridge.ctg/.cartridge/settings.json:19-25`). The proxy's own
  `timeout_secs` default is **1800** (`cartridge.json:198`). A model
  request sent as `{op:"request"}` is therefore cut by the host at 60 s with a
  bare `proxy did not answer in time`, thirty times before the proxy's own
  diagnosed 504 could ever be produced. This is the mechanism the sibling PRD
  records: a caller-side `tokio::time::timeout` around a cartridge call is
  inert, and the only place a bound can be declared is `timeout_ms` in the
  **provider's** manifest. Here the proxy *is* the provider, so this one is
  ours to fix.

  **Every `cartridge.ctg` line number above is at that repo's HEAD `63ff234`,
  not its working tree** (which is also dirty, 18 paths). In the worktree the
  same `plan.rs` fallback sits at `:322-324` and `event_timeout_ms` at
  `settings.json:26-31`; a reader checking the citation from a lane would not
  find them there. The mechanism is identical either way.

## Design

Three edits, no new files, no new abstraction beyond one nine-line helper.

1. **`cartridge.json` — declare the event's bound.** Add
   `"timeout_ms": 1860000` to `events.proxy`, and extend the `timeout_secs`
   doc to state the coupling. 1 860 000 ms is the 1800 s default plus a 60 s
   grace, so the proxy's own deadline fires first and the caller receives the
   diagnosed 504 rather than the host's bare message. It stays a real backstop:
   a wedged handler is still cut at 31 minutes, which is what acceptance 2
   asks for. `lsp.ctg/cartridge.json:96` already declares `timeout_ms: 600000`,
   so a large value is an established shape.

   **This residual cannot be fully closed, and the spec says so rather than
   implying otherwise.** `timeout_secs` has max 86400 (s) and `event_timeout_ms`
   has max 86400000 (ms) — the same ceiling — so no manifest value can strictly
   exceed a maximally raised `timeout_secs`. Any `timeout_secs` above 1860 s
   restores the undiagnosed host timeout for event-bus callers. The mitigation
   is therefore documentation, and because a doc sentence is the whole
   mitigation it gets its own acceptance box and its own Verify grep: the
   `timeout_secs` doc string must name `events.proxy.timeout_ms` and say that
   raising it past that bound puts the host's `event_timeout_ms` back in front.

2. **`src/service.rs:317` — quote the bound.** Replace the constant with

   ```rust
   .map_err(|_| {
       format!(
           "proxy request deadline exceeded: the request ran past \
            proxy.timeout_secs = {}s",
           self.config.timeout_secs
       )
   })?
   ```

   The `starts_with("proxy request deadline exceeded")` contract at
   `src/usage.rs:248` and `src/notice.rs:49` is a prefix match, so appending is
   safe and `.cartridge/tests/unit/tests.rs:2527` keeps passing unchanged.

3. **`src/service.rs` — name the stage and the elapsed time.** Add one helper
   **as an associated function inside `impl Service`**, next to `run()`, so the
   four call sites read `Self::staged(...)`. (Placement is stated because a free
   function and an associated one differ at every call site; either compiles,
   but pick one and be consistent.)

   ```rust
   /// A host event timeout (`<id> did not answer in time`,
   /// cartridge.ctg/src/transport/cartridge.rs:95) says which cartridge
   /// stalled but not which of this request's three waits it was, nor how
   /// long it ran. Every other message is a contract someone matches on --
   /// `usage::UPSTREAM_PREFIX` above all -- and passes through untouched.
   async fn staged<T>(
       stage: &str,
       call: impl std::future::Future<Output = Result<T, String>>,
   ) -> Result<T, String> {
       let started = std::time::Instant::now();
       call.await.map_err(|error| match error.ends_with("did not answer in time") {
           true => format!(
               "proxy {stage} stage stalled after {}ms: {error}",
               started.elapsed().as_millis()
           ),
           false => error,
       })
   }
   ```

   Wrap exactly four awaits with it: `"harness"` at `src/service.rs:661-665`
   (stage `harness`), `live.round(...)` at `:741` and the `"router"` call at
   `:743-747` (stage `provider route`), and `self.execute(...)` at `:785-787`
   (stage `cartridge call`).

   The rewritten message **ends with** the original, so the
   `ends_with("did not answer in time")` hint branch keeps matching. That
   branch exists in the working tree at `src/notice.rs:51-53` but not at
   `0692c18` (see the warning above), so `src/notice.rs` is in the footprint:
   if the branch is absent when the work starts, add it there, worded as in the
   working tree. The guard on `ends_with` is load-bearing:
   `usage::classify` (`src/usage.rs:219-260`) strips `UPSTREAM_PREFIX`
   (`"model request ("`, `src/usage.rs:210`) and `UPSTREAM_STREAM_PREFIX`
   (`src/usage.rs:213`) from the **front** of the message at `:221-222`, so a
   blanket wrap would turn every upstream 429 and 4xx into a 500. This is the
   spec's main hazard and it is pinned by an executable test that drives an
   upstream error through `run()`, not by a literal `classify` call — see
   Acceptance.

Deliberately skipped: reading the host's `event_timeout_ms` to print its value.
No host RPC exposes settings — `cartridge.ctg/src/host/socket.rs` serves only
`auth`, `status`, `snapshot`, `cartridges`, `bail`, `gather`, `reload`,
`subscribe`, `stop`. The measured elapsed time plus the knob name in the
`notice.rs` hint is the honest equivalent.

Also deliberately skipped: a timing probe of the 60000 ms / 1800 s mismatch.
It is a static three-link chain — `events.proxy` declares no `timeout_ms`,
`cartridge.ctg/src/host/plan.rs:299-301` (at `63ff234`) falls back to
`settings::host().event_timeout_ms`, and
`cartridge.ctg/.cartridge/settings.json:19-25` defaults it to 60000 — and
Verify block 1 pins the manifest side deterministically.

**Editing `cartridge.json` untrusts the cartridge.** The daemon drops a
cartridge whose manifest changed and the error names the consumer, so after
this lands the implementer needs `cartridge trust` and a reload before any live
exercise of the new bound. No Verify block depends on a live host, so this
affects manual checking only.

## Acceptance

- [x] The `proxy` event declares a `timeout_ms` strictly greater than the
      `timeout_secs` default in milliseconds, so the proxy's own deadline
      reaches an event-bus caller before the host's `event_timeout_ms` cuts it.
- [x] A request that exceeds `proxy.timeout_secs` fails with a message naming
      `proxy.timeout_secs` and its value in seconds.
- [x] A downstream stall names the stage (`harness`, `provider route` or
      `cartridge call`) and how many milliseconds that stage ran, while still
      ending in the host's original `… did not answer in time` so the notice
      hint at `src/notice.rs` keeps firing.
- [x] `src/notice.rs` carries the `ends_with("did not answer in time")` hint
      branch naming the host's `event_timeout_ms`, whether it was already in
      the working tree or had to be added.
- [x] An upstream rejection **driven through `run()`** reaches the caller with
      its `model request (` prefix still at the front of the message and still
      classifying 429 — that is, the stage wrapper did not swallow it.
- [x] The `timeout_secs` doc string in `cartridge.json` names
      `events.proxy.timeout_ms` and records that raising `timeout_secs` past it
      puts the host's `event_timeout_ms` back in front.
- [x] The existing suite stays green (55 passed at `0692c18`), including the two
      deadline tests that already pin "a stalled request yields a failure"
      (`:829`, `:2110`) and the classify assertion at `:2527`.

Three new tests in `.cartridge/tests/unit/tests.rs`, named exactly:

- `deadline_message_names_the_bound` — drive a request with
  `config.timeout_secs = 1` against a `self.call` that returns
  `std::future::pending()` for `"router"`, assert the failure message contains
  `proxy.timeout_secs = 1s` and that `usage::classify` of it is still 504.
- `a_stalled_stage_names_the_stage_and_how_long_it_ran` — with a `self.call`
  that returns `Err("harness did not answer in time".into())` for `"harness"`,
  assert the failure message starts with `proxy harness stage stalled after`
  and ends with `did not answer in time`.
- `an_upstream_rejection_survives_the_stage_wrapper` — **the proof of this
  spec's main hazard, and it must be able to fail.** With a `self.call` that
  returns `Err("model request (429 Too Many Requests): {}".into())` for
  `"router"`, assert the `Failure` the service produces still has
  `message.starts_with("model request (429")` and `status == 429`. The fixtures
  already permit this: `service.call = Arc::new(move |key, args| …)` is how
  `tests.rs:829` and `:2110` install their own stubs.

  Why a third test rather than an assertion in the second: every existing 429
  assertion in the suite (`tests.rs:2497`) calls `classify` on a **literal**,
  which passes at HEAD and would keep passing under a blanket wrap — it cannot
  fail in the world it denies. Only an error that actually travels through
  `staged` proves the `ends_with` guard. An implementer can check the test is
  real by deleting the guard (making the wrap unconditional): this test must go
  red, and the other two must stay green.

## Verify and Proof

<!--
Engine facts honoured here (prd.ctg/.cartridge/templates/spec.md):
each block is `sh -eu -c`, 120 s, run once in the lane worktree and again in
`repo`; every path is relative to the repo root; no `cd` to an absolute
checkout; every cargo command exports an isolated CARGO_TARGET_DIR.
The target dir is under TMPDIR rather than `$PWD/target` on purpose: it is
outside the footprint and outside the live `target/` the host watches, and
the same warm dir serves both passes, which keeps each block inside 120 s.
No block writes inside the footprint.

Pass 1 runs in a lane at boards/proxy/.lanes/<slug>, where the sibling
symlinks cartridge.ctg and memo.ctg already exist, so the HEAD Cargo.toml's
`evidence = { path = "../memo.ctg/evidence" }` resolves. Measured at HEAD with
that sibling present: cargo test --lib 5.9 s cold, cargo clippy --lib 0.6 s
warm, rustfmt instant -- all far inside the engine's 120 s limit.
-->

The manifest declares a bound larger than the proxy's own deadline.

```sh
python3 - <<'PY'
import json, sys
m = json.load(open("cartridge.json"))
ms = m["events"]["proxy"].get("timeout_ms")
secs = m["settings"]["timeout_secs"]["default"]
if not isinstance(ms, int) or ms <= secs * 1000:
    sys.exit(f"events.proxy.timeout_ms is {ms!r}; it must be an integer > {secs * 1000}")
print(f"ok: events.proxy.timeout_ms={ms} > timeout_secs default {secs}s")
PY
```

The suite is green and both new tests ran and passed by name. A passing cargo
run prints one `test <name> ... ok` line per test, so the names are pinned
here rather than trusted to the summary count.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/proxy-timeout-verify}"
mkdir -p "$CARGO_TARGET_DIR"
log="$CARGO_TARGET_DIR/tests.log"
if ! cargo test --lib > "$log" 2>&1; then cat "$log"; exit 1; fi
for t in deadline_message_names_the_bound a_stalled_stage_names_the_stage_and_how_long_it_ran an_upstream_rejection_survives_the_stage_wrapper a_plain_retry_after_a_timeout_succeeds_on_the_same_service; do
  if ! grep -q "test tests::$t ... ok" "$log"; then
    echo "missing or failed: tests::$t"
    exit 1
  fi
done
tail -n 3 "$log"
```

The deadline message quotes its setting and the stage wrapper leaves the
upstream-status contract alone, read straight out of the source.

```sh
if ! grep -q 'proxy.timeout_secs = {}s' src/service.rs; then
  echo "src/service.rs: the deadline message does not quote proxy.timeout_secs"
  exit 1
fi
if ! grep -q 'ends_with("did not answer in time")' src/service.rs; then
  echo "src/service.rs: the stage wrapper does not guard on the host timeout shape"
  exit 1
fi
for stage in 'harness' 'provider route' 'cartridge call'; do
  if ! grep -q "staged(\"$stage\"" src/service.rs; then
    echo "src/service.rs: no stage wrapper for $stage"
    exit 1
  fi
done
if ! grep -q 'ends_with("did not answer in time")' src/notice.rs; then
  echo "src/notice.rs: the event_timeout_ms hint branch is missing"
  exit 1
fi
if ! grep -q 'event_timeout_ms' src/notice.rs; then
  echo "src/notice.rs: the hint does not name event_timeout_ms"
  exit 1
fi
echo "ok: deadline names its bound, three stages wrapped, guards in place"
```

The coupling doc is the entire mitigation for the residual raised-`timeout_secs`
case, which no code change can close, so it is pinned rather than trusted.

```sh
python3 - <<'PY'
import json, sys
doc = json.load(open("cartridge.json"))["settings"]["timeout_secs"]["doc"]
for needle in ("timeout_ms", "event_timeout_ms"):
    if needle not in doc:
        sys.exit(f"cartridge.json settings.timeout_secs.doc does not mention {needle}: {doc!r}")
print("ok: the timeout_secs doc records the coupling")
PY
```

Formatting and lints, **scoped to what this footprint may legally change**.

`cargo fmt --all --check` and `cargo clippy --workspace --all-targets` both
exit 1 at `0692c18` for reasons an implementer cannot fix inside this
footprint, so neither is used:

- `cargo fmt --all --check` reports drift at `.cartridge/tests/unit/tests.rs:699`
  **and** `.cartridge/tests/unit/wire/tests.rs:32`; the second is out of
  footprint, and formatting it would be an out-of-footprint write that collect
  rejects.
- `cargo clippy --workspace --all-targets` fails with
  `cloned_ref_to_slice_refs` at `.cartridge/tests/unit/wire/tests.rs:29`
  (`-D warnings` via `Cargo.toml [lints.rust]`) — also out of footprint. This
  one is masked in a plain `sh -eu` run because the `fmt` line aborts first.

`rustfmt` is therefore pointed at the footprint's own Rust files (it follows
`#[path] mod context_tests;` into `.cartridge/tests/unit/context.rs`, which is
clean at HEAD and stays clean), and clippy is scoped to `--lib`, which excludes
the `cfg(test)` targets that carry the unrelated lint. Verified at `0692c18`:
the scoped `rustfmt` exits 1 naming only `tests.rs:699` — in footprint, so the
implementer fixes it as part of this work — and `cargo clippy --lib` exits 0.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/proxy-timeout-verify}"
rustfmt --check --edition 2021 src/service.rs src/notice.rs .cartridge/tests/unit/tests.rs
cargo clippy --lib
```
