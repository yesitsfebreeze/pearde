# @mcp/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound review history

Plan: `@mcp/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound`,
`prd.ctg/.cartridge/boards/mcp/prds/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound/prd.md`.
Scope: leaf. One observable outcome: `mcp.ctg`'s `mcp` event declares its own `timeout_ms`, and a check keeps it declared.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none recorded for this child (parent `@mcp/a-cartridge-call-is-cancellable-and-bounded` has no review.md).

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: prd.ctg HEAD `dc0afb8e` with a dirty `prd.md` and an untracked `specs/`
(analyst-bound-2 output). Source: mcp.ctg HEAD `5a7c54c` (clean), cartridge.ctg HEAD `beb8213`.

| Input | Content digest |
| --- | --- |
| Plan | `the-mcp-event-declares-its-own-bound/prd.md` sha256 `0e0d87edcd43ac538e1283c7889a4608a07bf2d083c7b59b0f366cb383fee97f` |
| Specs | `specs/spec01.md` sha256 `a417787c92f0f19316b0199de2980d7fbfe49be0384051417b0b4f0c931b75ed` |
| Material contracts/dependencies | parent `prd.md` `11c99f87…00b0`; `mcp.ctg/cartridge.json` @`5a7c54c` `1ca4fbd4…a7c7`; analyst report `analyst-bound-2.md` `7ba041a7…3f16`; cartridge.ctg @`beb8213`: `src/host/plan.rs:322-324`, `.cartridge/settings.json:26-32` (`event_timeout_ms` default 60000, min 1, max 86400000), `src/loader/document.rs:179-181` (per-event `timeout_ms` only rejects 0), `src/transport/cartridge.rs:95,389-393`, `src/cli/host.rs:376-429` (bridge); collected sibling `@proxy/the-proxy-answers-within-its-bound-or-reports-the-delay` (spec01 + collection.md, commit `94979b7`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | The value is derived, not just big. The host bridge (`cli/host.rs`) sends each line with `bail`, which is cut by the `mcp` event's bound (`transport/cartridge.rs:389-393`). Inside, `invoke` awaits one inner `tool.*` bail, which has its own bound. So the outer bound has to exceed the slowest legitimate inner bound (lsp 600000 ms). Then the caller gets the inner, named failure (`lsp did not answer in time`) instead of the bare `mcp did not answer in time`. That serves the Outcome, and no message change is needed for this leaf's Outcome. Diagnosing a wedged line belongs to the runtime children. −3: the 3x headroom over the 600000 floor is argued from nearby things (agent approval, proxy symmetry, providers that might raise their bounds later), not from an MCP line. The spec also does not weigh the cost: with the Lua listener serialising lines (parent note, unobserved), a line queued behind a wedged one now waits up to 30 min silently instead of failing at 60 s. |
| Ownership and reuse | 18 | One field in the cartridge's own manifest. Correctly leaves `proxy.ctg` and every `tool.*` provider's manifest alone. −2: B1's persistent guard can reuse `service::DOCUMENT` (`src/service.rs:29`, already `include_str!("../cartridge.json")`) and the existing unit module `.cartridge/tests/unit/tests.rs` (22 tests). The spec does not look for either. |
| Dependencies and implementable slices | 18 | Can land today, has no prerequisite, and does not overlap the runtime children. −2: the spec's Scope says `plan.rs:299-301` holds the fallback "at `cartridge.ctg` HEAD `beb8213`". At `beb8213` it is `:322-324` (`git show beb8213:src/host/plan.rs`, lines 322-324), and `:299-301` is the `63ff234` citation. The spec's own Baseline section says `:322-324`, so the spec contradicts itself. |
| Observable acceptance and baseline evidence | 12 | The baseline is real. At `5a7c54c`, `events.mcp` has no `timeout_ms`, and the reproduced run gives base exit 1. −8, blocking B1: PRD Acceptance 2 is "A check fails if the declaration is removed, **so the bound cannot be lost silently again**". The only check is the Verify block, and `prd.ctg/src/lifecycle.ts` runs Verify blocks only during collect (`verify()` at :137 and :167). After collection, nothing in `mcp.ctg` fails when the field is deleted: no test or check reads it (`grep` of `.cartridge/tests` and `src` finds no `timeout_ms` assertion; inferred, not executed). The spec's mutant proves the collect gate is red on a removed field. It does not prove that later loss is caught, which is what the clause is for. |
| Failure, recovery and compatibility | 16 | A finite backstop well under the host's ceiling. A wrong type, a smaller value and a missing field all fail the gate (reproduced below). −4: editing `cartridge.json` changes its trust hash (`src/trust/README.md`: "every `cartridge.json`, because the manifest carries the grant"). The mcp cartridge, which serves every agent's MCP surface, then stays unloaded until someone re-trusts it. The proxy sibling's spec states that consequence and the `cartridge trust` + reload step; this spec does not (N2). The silent-queueing trade-off is also unstated (N1). |
| Reviewer total | 81 / 100 | |

Findings and concrete revisions:

- **B1 (blocking): the "cannot be lost silently again" clause has no lasting guard.** Evidence: Verify runs only in collect (`prd.ctg/src/lifecycle.ts:137,167`). `mcp.ctg`'s `test`/`check` commands would stay green with the field removed. Revision: widen the footprint by `.cartridge/tests/unit/tests.rs`. Add one test, e.g. `the_mcp_event_declares_its_own_bound`, that parses `crate::service::DOCUMENT` and asserts `events.mcp.timeout_ms` is an integer `>= 1800000`. Extend the Verify block to run it by name with an isolated target dir, e.g. `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-bound-verify}"`, then `cargo test --lib the_mcp_event_declares_its_own_bound` with the `test tests::… ... ok` line grepped. Keep the python gate as the static half. The mutant must turn the named test red too.
- **N1 (non-blocking): say what the larger bound costs.** Add a sentence to "Choosing the value": the outer bound only matters when it is shorter than the inner bounds or when lines queue. The cost of 30 min is that a line queued behind a wedged one waits silently for up to 30 min. Recovery for that belongs to `@runtime/a-cartridge-call-can-be-cancelled` and `@runtime/a-wedged-call-reports-its-late-answer`. This keeps the value tied to what an MCP line takes, not to headroom alone.
- **N2 (non-blocking): trust and reload after landing.** State that the manifest edit invalidates trust for the `mcp` cartridge. Name the recovery (`cartridge trust`, then reload) and warn that pass 2 of collect fast-forwards live `mcp.ctg`, so run collect from the CLI rather than through the MCP surface it will drop.
- **N3 (non-blocking): fix the line citation.** Change the Scope sentence to `plan.rs:322-324` at `beb8213` (`:299-301` at `63ff234`).
- **N4 (non-blocking, optional):** the python gate sets no upper bound. A `<= 86400000` check (the host's own ceiling for the default it overrides) would keep "finite backstop" true under a later edit.

Disposition: revise (keep scope; widen footprint by one test file for B1).

Validation: all runs were in disposable `git clone --local` copies of mcp.ctg @`5a7c54c` under
`/private/tmp/claude-501/-Users-feb-dev-cartridge-cartridge-ctg/3f0d518f-742b-4556-9a24-6c5fa6dd7524/scratchpad/reviewer-mcpbound-1/`.
Each ran the spec's Verify block, extracted verbatim, as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "$(cat ../verify.sh)"` with cwd set to the clone root.

| tree | exit | output |
| --- | ---: | --- |
| base (HEAD, no field) | 1 | `events.mcp.timeout_ms is None; it must be an integer >= 1800000` |
| reference (`"timeout_ms": 1800000`, diff `cartridge.json \| 3 ++-`) | 0 | `ok: events.mcp.timeout_ms=1800000 >= 1800000` |
| mutant (declaration removed from reference, diff vs HEAD empty) | 1 | same as base |
| extra: `600000` | 1 | `is 600000; it must be …` |
| extra: `"1800000"` (string) | 1 | `is '1800000'; it must be …` |

Host facts at `beb8213`: `event_timeout_ms` default 60000, max 86400000 (`.cartridge/settings.json`). The fallback is at `src/host/plan.rs:322-324`. `cartridge help host` lists docs only; `docs/transport.txt:18` confirms that an absent `timeout_ms` falls back to the base's `event_timeout_ms`. Live `mcp.ctg` was untouched (`git status --short` empty).

Reviewer identity: reviewer-mcpbound-1 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (81/100, one blocking finding).
Unresolved blocking findings: B1.
Rounds used / remaining: 1 / 4.
Next action: bounded revision of spec01 (and PRD footprint) for B1, ideally folding N1–N3; then round 2.

## Round 2 — 2026-09-19

Presented revision: prd.ctg HEAD `dc0afb8e`, with `prd.md` dirty (unchanged since round 1, same digest) and `specs/spec01.md` revised by analyst-bound-3. Source: mcp.ctg HEAD `5a7c54c` (clean), cartridge.ctg HEAD `beb8213`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `0e0d87edcd43ac538e1283c7889a4608a07bf2d083c7b59b0f366cb383fee97f` (same as round 1) |
| Specs | `specs/spec01.md` sha256 `4e71646cada8603001703c34557553c36e43b8b3d1a63229a829ad4296478646` |
| Material contracts/dependencies | `analyst-bound-3.md` `42cde759…76b8cf`; mcp.ctg @`5a7c54c`: `cartridge.json` `1ca4fbd4…a7c7`, `.cartridge/tests/unit/tests.rs` `2c0ba0ab…dd96`, `src/lib.rs:9-11` (`#[cfg(test)] #[path = "../.cartridge/tests/unit/tests.rs"] mod tests;`), `src/service.rs:29` (`pub const DOCUMENT = include_str!("../cartridge.json")`), `rustfmt.toml` (`hard_tabs = true`); prd.ctg `src/planner.ts:5-9` (`feet()` = PRD footprint ∪ spec footprints) and `src/lifecycle.ts:127-174`; composition `.cartridge/memos/routine/cartridge-development.md:76-89` (`just test mcp` → `cargo test --manifest-path mcp.ctg/Cargo.toml -p mcp --all-targets`); cartridge.ctg @`beb8213` `src/host/plan.rs:322-324` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | N1 is resolved. "What the larger bound costs" now names the case that matters (lines queued behind a wedged one wait up to 30 min silently) and hands recovery to the two runtime children. −1: the 3x headroom over lsp's 600000 ms is still argued mostly from analogies (proxy symmetry, agent approval), not from an observed MCP line. That is acceptable for a backstop. |
| Ownership and reuse | 20 | The guard reuses `crate::service::DOCUMENT`, which is the `include_str!` the host loads, not a second copy. It goes in the existing unit module. No new file. No other cartridge is touched. |
| Dependencies and implementable slices | 19 | N3 is resolved. `plan.rs:322-324` at `beb8213` checked (`.unwrap_or(crate::settings::host().event_timeout_ms)`). The spec footprint adds `tests.rs` by absolute path. `feet()` unions it with the PRD's relative `cartridge.json`, so collect's `assertFootprint` and changed-path check both allow the two files. −1: the PRD frontmatter footprint still lists only `cartridge.json`. It is not wrong, since the engine unions spec footprints, but it is the only place a reader of `prd.md` sees the scope. Frontmatter is not the reviewer's to edit. |
| Observable acceptance and baseline evidence | 18 | B1 is resolved, with evidence. The test is compiled into mcp's lib test target through `src/lib.rs`'s `#[cfg(test)] #[path]` include, and `use super::*` brings `Value` into scope. In the removed-declaration mutant, the named test fails both on its own and in the full `cargo test -p mcp --all-targets` suite, which is what the composition's `just test mcp` runs. So the loss stays caught after collect. A tree with the test deleted also fails block 2 through the name grep. −2 (N5): the spec says the test runs under "`mcp.ctg`'s own `check`/`test` commands". The manifest's `test` command calls `just --justfile ../cartridge.ctg/justfile test mcp`, and that runs cartridge.ctg's nextest in cartridge.ctg's directory, not mcp's tests. The runner that actually covers this test is the composition's `just test mcp` / `just check mcp`. Name that one. |
| Failure, recovery and compatibility | 18 | N2 is resolved: the trust-hash invalidation, `cartridge trust` + reload, and "collect from the CLI" are all stated. Block 2 writes only under `CARGO_TARGET_DIR`, which defaults to `$TMPDIR`, outside the footprint and away from mcp.ctg's live `target/debug` dylib, so there is no hot-restart in pass 2. −2 (N6): the Rust snippet is indented with 4 spaces. mcp.ctg's `rustfmt.toml` sets `hard_tabs = true`, so pasting it verbatim makes `cargo fmt --check` (`just check mcp`) red. `cargo fmt` changes only the indentation. N4 (no upper bound) was not taken up, which is acceptable because it was optional. |
| Reviewer total | 94 / 100 | |

Findings and concrete revisions:

- **B1: resolved.** Details under the fourth dimension and in the validation below.
- **N1, N2, N3: resolved** as described above. No regression found. Block 1 is unchanged, and block 2 is additive.
- **N5 (non-blocking):** replace "`mcp.ctg`'s own `check`/`test` commands" with the composition's `just test mcp` (`cargo test -p mcp --all-targets`). The mcp manifest's `test` command runs cartridge.ctg's suite.
- **N6 (non-blocking, for the implementer):** write the test with tabs, or run `cargo fmt -p mcp`, so `just check mcp` stays green. Clippy (`-D warnings`) is already clean.
- **Observation, not this spec's:** `tests::initialized_live_client_inspects_real_policy_without_granting_writes` fails in a `git clone --local` copy at base too (`tests.rs:555`, `status.success()`). It depends on the environment or sibling checkouts and fails the same way in base, reference and mutant. It does not affect the named-test gate.

Disposition: keep; proceed.

Validation: I made disposable `git clone --local` copies of mcp.ctg @`5a7c54c` in
`/private/tmp/claude-501/-Users-feb-dev-cartridge-cartridge-ctg/3f0d518f-742b-4556-9a24-6c5fa6dd7524/scratchpad/reviewer-mcpbound-2/`:

- `base`: HEAD.
- `ref`: spec diff applied, `cartridge.json | 3 ++-` and `tests.rs | 11 +`.
- `mutant`: the test kept, the declaration removed.
- `notest`: the declaration kept, the test removed.

Both Verify blocks were extracted with collect's own heading and fence regex, verbatim. Each ran as `env -i PATH="$PATH" HOME="$HOME" TMPDIR=<scratch>/tmp sh -eu -c "$(cat blockN.sh)"`, with cwd at the clone root.

| tree | block 1 | block 2 | output |
| --- | ---: | ---: | --- |
| base | 1 | 1 | `timeout_ms is None…`; `running 0 tests` → `missing or failed: tests::the_mcp_event_declares_its_own_bound` |
| reference | 0 | 0 | `ok: …=1800000`; `1 passed` |
| mutant (declaration removed) | 1 | 1 | `None…`; the test itself `FAILED` |
| notest (test removed) | 0 | 1 | name grep catches the missing test |

Additional runs (`CARGO_TARGET_DIR` in scratch):

- Block 2 on `ref` with no compiler cache (`RUSTC_WRAPPER=""`, fresh target dir): exit 0 in 7 s, well under the 120 s limit.
- `cargo test -p mcp --all-targets` exits 101 on base, reference and mutant because of the pre-existing environment-dependent test. Only the mutant adds `the_mcp_event_declares_its_own_bound … FAILED`.
- `ref`: `cargo clippy -p mcp --all-targets -- -D warnings` exits 0. `cargo fmt -p mcp -- --check` exits 1 (indentation only, N6).

Live mcp.ctg was untouched (`git status --short` empty).

Reviewer identity: reviewer-mcpbound-2 (independent review sub-agent, Opus 5).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: PASS (94/100, no blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation of spec01, folding in N5 and N6 (tabs or `cargo fmt`). After landing, run `cartridge trust` for mcp.ctg and reload, and collect from the CLI.
