# @mcp/deferred-tool-band review history

Plan: `@mcp/deferred-tool-band`, `prd.ctg/.cartridge/boards/mcp/prds/deferred-tool-band/prd.md` with `specs/spec01.md`.
Scope: one observable outcome — `tools/list` withholds deferred tool schemas behind a one-line listing and a restore call; leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg HEAD `3253b72a` with `prd.md` modified and `specs/` untracked (dirty); code base mcp.ctg `6f06acd`.

| Input | Content digest |
| --- | --- |
| Plan | `boards/mcp/prds/deferred-tool-band/prd.md` SHA-256 `418e878bf6a5052980f6eccadf7c28cc912b00200fb778b264c372d8e2f6bd7a` |
| Specs | `boards/mcp/prds/deferred-tool-band/specs/spec01.md` SHA-256 `7ed45b5213340cdf63562448f9ee006c9e7a09c92c8e19ef08763b68d75ae2e2` |
| Material contracts/dependencies | `boards/harness/prds/reflex-tool-audit-loop/prd.md` (dirty) SHA-256 `22c8ae95871647b917ec982522983f56bf5a968bb7057b3aa444e5a5e62a3f9c`; mcp.ctg `6f06acd` `src/service.rs`, `.cartridge/tests/unit/tests.rs`, `cartridge.json`, `Cargo.toml`; `harness.ctg/src/lib.rs` `convert_tools`; `prd.ctg/src/lifecycle.ts` verify/collect rules (as stated by coordinator); analyst report `boards/mcp/.state/loop/deferred-tool-band/analyst-1.md` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 14 | Real cost problem; spec is small and bounded (one source file, six named tests). −3: `band` defaults to `false` and the stdio bridge cannot push `tools/list_changed`, so no current client (Claude Code does not re-list) gains anything until an unfiled cartridge-board follow-up lands. −3: PRD says "every tool the composition exposes costs its full schema on every request"; the proxy (`proxy.ctg/cartridge.json` `tools`), agent (`agent.ctg` `tools`) and harness (`convert_tools`) surfaces are out of scope, and neither PRD nor spec says so. |
| Ownership and reuse | 15 | Good reuse: the single `registry()`/`describe` choke point in `src/service.rs`, the existing `config.tools` allowlist, the existing `duplicate tool name` guard, the `content()` helper, and the upstream `band.ts` semantics (hot set, 100-char snippet, no description fallback, opt-out, kill switch). −5: the disposition (hot/deferred/restored) stays private to the mcp `Service`, while the dependent plan's Decision says harness box 3 needs "the band's disposition" and notes `harness.ctg/src/lib.rs` `convert_tools` passes descriptors straight through. The mcp service is not on that path, so the dependency owner is wrong or the contract is missing. |
| Dependencies and implementable slices | 14 | No `needs`; steps map cleanly to the footprint of four paths. −3: the downstream `@harness/reflex-tool-audit-loop` is told to "land this first", but this spec gives it nothing it can consume (see Ownership). −2: the follow-up that makes the band useful (bridge push, then flipping the default) is only described in prose, with no PRD ID. −1: step 2 misidentifies the `Config` literals. The full literals are in `fixture` (tests.rs:49), `an_empty_profile_exposes_no_tools_…` (:127) and `diagnostic_inspection_…` (:414). The two at :338 and :477 use `..Config::default()`. Because of `deny_unknown_fields`/`Default::parse`, these still compile after the settings are declared, so the impact is low. |
| Observable acceptance and baseline evidence | 11 | Six named tests with concrete sentinels (`PLAIN-DESCRIPTION-SENTINEL`, exact hot set, independently computed byte sums) are strong. Baseline gates were measured by the analyst and rechecked here. −5 (blocking): every Verify block starts with `cd /Users/feb/dev/cartridge/mcp.ctg`, so the lane pass verifies the shared checkout instead of the lane worktree, and a lane with a broken change can pass. −2: "fmt and clippy are clean" is checked with `cargo clippy --all-targets` without `-D warnings`. `[lints.rust] warnings = "deny"` does not cover clippy lints, so that block cannot fail on a clippy warning. −1: acceptance box 2 can pass without a working restore, because the spec (step 6) keeps unrestored deferred tools callable through `tools/call`. Only the `tools/list` half separates restored from unrestored. −1: PRD box 6 and the Gates name `just test mcp`, which the analyst measured red at base (2 live-fixture failures). Verify uses `cargo test --lib band_` instead, and neither the PRD nor the spec records that substitution. |
| Failure, recovery and compatibility | 15 | Band off is required to be byte-identical (no meta-tool, no `_meta`), and `band_disabled_sends_every_schema` guards it. Unknown restore names return `isError`. `hot` validation is specified. −2: a provider tool named `tools` with the band on makes `registry()` return `Err`, which fails the whole `tools/list` rather than only the colliding tool. Today no `tool.tools` exists, but neither the refusal nor the recovery (rename, or disable the band) is documented. −2: `restored` is shared by every attached client for the life of the host process, never cleared and has no un-restore. The PRD's "session" wording hides this. −1: the PRD's "Proof and recovery" section has no rollback statement (setting `band=false` is the rollback; say so). |
| Reviewer total | 69 / 100 | |

Findings and concrete revisions:

1. **BLOCKING — Verify runs in the wrong tree.** All four spec Verify blocks `cd /Users/feb/dev/cartridge/mcp.ctg`. The lifecycle already runs each block with cwd = lane root and then cwd = mcp.ctg, so the absolute `cd` makes the lane pass check the shared checkout. Revision: delete the `cd` lines, so every command runs relative to the engine-provided cwd.
2. **BLOCKING — The dependent plan's contract is not met.** `@harness/reflex-tool-audit-loop` ## Decision requires a band disposition that harness (`convert_tools`) can outrank. This spec creates the disposition only inside mcp's private `Service`. Revision: pick one. (a) Make the descriptor fields `summary`/`defer` plus the `hot`/deferred decision the shared contract, and state in the spec's Remaining section which surface harness reads. (b) Scope this PRD explicitly to the MCP surface and amend the harness Decision/`needs` to the PRD that actually owns the harness or proxy disposition. Either way, state in the PRD which exposure surfaces are in scope.
3. Non-blocking — the clippy check cannot fail. Use `cargo clippy --all-targets -- -D warnings`. Probe: clean at base, exit 0.
4. Non-blocking — the value is gated on an unfiled follow-up. File, or reference by ID, the cartridge-board PRD for the `tools/list_changed` push and the default flip, or give a reason for shipping off-by-default without it.
5. Non-blocking — box 2 is weak. Assert that before the restore `memo` has no `inputSchema` in `tools/list`, and that after one restore it has one on both later lists. Drop "two `tools/call memo` succeed" as evidence of the restore, or state that it proves only that calls are not disabled.
6. Non-blocking — the gate named in the PRD is red at base. Record in the PRD that `just test mcp` has 2 pre-existing live-fixture failures and that `cargo test --lib band_` plus `just check mcp` is the proof. Otherwise keep box 6 as "tested offline by the unit suite".
7. Non-blocking — correct the step 2 `Config` literal list: `fixture`, `an_empty_profile_exposes_no_tools_and_an_unknown_one_is_refused` and `diagnostic_inspection_is_optional_scoped_and_cannot_grant_authority`.
8. Non-blocking — document the collision and restore scope. The README should say that a provider tool named `tools` fails the listing while the band is on, that the restored set is host-wide across clients and lasts until the host restarts, and that `band=false` is the rollback.

Disposition: revise (spec Verify + scope/contract with the harness dependent); keep as one leaf.

Validation (reviewer, 2026-09-16):
- `git worktree add --detach <scratchpad>/mcp-lane 6f06acd` with `CARGO_TARGET_DIR=<scratchpad>/mcp-target` (cold target, no `RUSTC_WRAPPER`):
  - `cargo fmt --all --check` exited 0 in about 0 s.
  - `cargo clippy --all-targets` exited 0 in 5 s.
  - `cargo test --lib band_` exited 0 in 3 s. Output: `0 passed; 13 filtered out`, as expected before implementation.
  - `cargo clippy --all-targets -- -D warnings` produced no warnings.
  - The worktree was removed with `git worktree remove`.
- All blocks are far below the 120 s cap. The build needs no sibling submodule: `build.rs` only sets macOS link args, and all dependencies come from crates.io.
- `just check mcp`, cwd `/Users/feb/dev/cartridge`: exit 0, 6 s.
- `just test mcp` was not re-run. Its red base (11 passed, 2 failed) comes from analyst-1.
- `shasum -a 256` on prd.md, spec01.md and the harness prd.md gave the digests in the table above.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (69/100, 2 blocking findings).
Unresolved blocking findings: 1 (Verify `cd` to the shared checkout); 2 (unmet disposition contract with `@harness/reflex-tool-audit-loop`, and undeclared surface scope).
Rounds used / remaining: 1 / 4.
Next action: make one bounded revision of `prd.md`/`spec01.md` (and the harness Decision if option 2b is chosen) that addresses findings 1–2 and preferably 3–8, then run Round 2 review.

## Round 2 — 2026-09-16

Presented revision: prd.ctg `762fe9a2` ("… re-scope the band"). prd.md and spec01.md are committed and clean; review.md is untracked. Code base is mcp.ctg `6f06acd`.

| Input | Content digest |
| --- | --- |
| Plan | `boards/mcp/prds/deferred-tool-band/prd.md` SHA-256 `32b8a2bed7b07eb86ec834429ed535b251f77bc5bf0de38e5e5742904e151ce3` (matches the hand-off prefix `32b8a2be`) |
| Specs | `boards/mcp/prds/deferred-tool-band/specs/spec01.md` SHA-256 `f102aa8444552b3e8f516b4f803e4e2c8970c04380f113d09c35f55d09ed0332` (matches the hand-off prefix `f102aa84`) |
| Material contracts/dependencies | `boards/harness/prds/reflex-tool-audit-loop/prd.md` SHA-256 `22c8ae95871647b917ec982522983f56bf5a968bb7057b3aa444e5a5e62a3f9c` (unchanged since round 1). mcp.ctg `6f06acd`: `src/service.rs` (`Config`, `validate`, `describe`, `registry`, `invoke`), `src/lib.rs` (a `static SERVICE: OnceLock`, one per process), `.cartridge/tests/unit/tests.rs`, `cartridge.json`, `.cartridge/docs/README.md`. `harness.ctg/src/lib.rs` `convert_tools`. `~/.cargo/config.toml` (`rustc-wrapper = "kache"`). |

Round-1 findings:

| # | Status | Evidence |
| --- | --- | --- |
| 1 BLOCKING | Resolved | All four Verify blocks are free of `cd`. The spec states the engine cwd order. Each block ran in a detached lane worktree (see Validation). |
| 2 BLOCKING | Resolved (option a) | PRD ¶Scope and spec §Scope make `summary`, `defer` and a consumer-side `hot` set, plus one disposition rule, the contract. Harness applies the rule in `convert_tools` and does not read mcp's `Service`. Probe: both mcp `describe` (service.rs:243) and harness `convert_tools` (lib.rs:679) read the same runtime descriptor JSON (`name`, `description`, `input_schema`) from the provider's `describe` op. The new optional fields therefore need no host manifest or schema change, and harness can read them directly. The proxy, agent and harness surfaces are declared out of scope in Remaining. |
| 3 | Resolved | `cargo clippy --all-targets -- -D warnings`. |
| 4 | Partly resolved | The spec and PRD Recovery now say why the band ships off by default. The bridge push is still "to be filed" and has no ID. |
| 5 | Resolved | Spec box 2 checks for no `inputSchema` before the restore, then for one on both of the next two lists. Step 6 says a call does not prove a restore. |
| 6 | Resolved | The PRD Gates and spec Verify record `just test mcp` as red at base, naming both failing tests. |
| 7 | Resolved | Checked: full literals are at tests.rs:49 (`fixture`), :127 and :414. The literals at :338, :370 and :477 use `..Config::default()`. |
| 8 | Resolved | Spec step 8 and box 7 cover the collision, host-wide restores and `band=false` as rollback. `lib.rs` confirms one `Service` per process, so "host-wide until restart" is accurate. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The scope is now declared: MCP listing only, with other surfaces named. −2: the band still ships off, and no current client (Claude Code does not re-list) benefits until an unfiled cartridge-board bridge push lands. Value is deferred to work with no ID. −2: the PRD body is 629 words (`awk 'NR>9' prd.md \| wc -w`). The method says a leaf should be split or trimmed before it exceeds 400 words. The excess is contract and recovery prose that duplicates spec §Scope and step 5, not a second outcome, so trimming is enough. |
| Ownership and reuse | 17 | Reuse is still strong: the `describe`/`registry` choke point, the `config.tools` allowlist, the `duplicate tool name` guard, `content()`, and `Config::default()` reading the declared settings. −2: the "composition-wide contract" lives only in mcp's `.cartridge/docs/README.md`. The proxy, agent and harness boards must treat another cartridge's README as their authority, and nothing is filed in cartridge.ctg, which owns the descriptor surface. −1: the harness `## Decision` is unchanged. It still says harness waits for the band to "land a disposition" and that its harness child "applies verdicts over the band's disposition". It does not record that under option (a) that child must also implement the disposition rule itself in `convert_tools`, so real scope moved to harness without being recorded there. |
| Dependencies and implementable slices | 17 | No `needs`. The four-path footprint matches steps 1–8, and the literal list is correct. −2: three follow-ups are only prose with no PRD ID: the bridge `tools/list_changed` push plus the default flip, the live-fixture red gate, and the other listing surfaces. The default flip, which delivers the value, has no owner record. −1: the harness `needs: @mcp/deferred-tool-band` is now a contract and documentation dependency only, and neither plan says so. |
| Observable acceptance and baseline evidence | 17 | Verify now runs in the lane. The test gate requires `ok. 6 passed` and the byte-report line, and it fails at base as it should (0 passed, 13 filtered out). The sentinels are concrete. −1: PRD box 1 says the declared schemas are "exactly the hot set plus anything restored", but spec box 1 expects `{pinned, hotname, tools}`, which includes the meta-tool. The two acceptance texts disagree. −1: spec box 7 claims the README documents the collision and restore scope, but the Verify greps check only `cartridge/band`, `defer` and `band=false`. −1: Recovery promises that band-off output is "byte-identical to today", but `band_disabled_sends_every_schema` only checks that the meta-tool and `_meta` are absent. No assertion compares against the pre-change listing. |
| Failure, recovery and compatibility | 18 | Rollback, collision recovery, host-wide restore lifetime and off-by-default are all stated. Unknown restore names return `isError`. `hot` validation refuses empty or duplicate names. −1: `tools/call tools` skips the policy round and changes a host-wide set. Any attached client can therefore change every other client's listing. This is documented as host-wide, but it is not justified as acceptable authority. −1: `hot` takes tool names (`memo`) while the sibling `tools` setting takes keys (`tool.memo`), and a `hot` name that matches no tool is accepted silently. A typo leaves the tool deferred with no signal. Refuse unknown names in the listing meta, or document the difference. |
| Reviewer total | 85 / 100 | |

Findings and concrete revisions (none blocking):

1. The value has no owner record. File the cartridge-board PRD for the bridge `notifications/tools/list_changed` push and the `band` default flip, and the mcp-board PRD for the live-fixture red gate. Cite both IDs in spec Remaining and PRD Recovery.
2. Make PRD box 1 and spec box 1 agree. Either say "exactly the hot set, anything restored, and the `tools` meta-tool", or exclude the meta-tool in both.
3. Trim the PRD to at most about 400 words. Keep the outcome, the Scope sentence, Recovery and Gates, and leave the field-level contract to spec §Scope.
4. Home the contract. Reference, or file under cartridge.ctg, the descriptor-field definition (`summary`, `defer`) so that other surfaces do not cite mcp's README as the authority. Alternatively, state explicitly that mcp's README is the interim authority until then.
5. Amend the harness `## Decision` with one line: its harness child implements the disposition rule in `convert_tools` from descriptor `defer` and its own `hot` setting, and `needs` on the band is for the contract.
6. Add Verify greps for the collision and restore-scope text, so that spec box 7 is checked mechanically.
7. Add a band-off byte-identity assertion, for example by serialising `tools/list` with `band=false` and comparing it to the same fixture's listing under `Config::default()` before the new fields exist, or to a pinned expected JSON.
8. Specify what happens to `hot` names that match no tool (refuse, or report them in `cartridge/band`), and note in the README that `hot` takes names while `tools` takes keys. Add one sentence on why an unauthenticated host-wide restore is acceptable, since it grants no call authority.

Disposition: keep as one leaf. Make one small revision (findings 1–3 lift the score most). No split.

Validation (reviewer r2, 2026-09-16):
- `shasum -a 256` on prd.md, spec01.md and the harness prd.md gave the digests in the table.
- Ran `git -C mcp.ctg worktree add --detach <scratchpad>/r2-lane 6f06acd`. In that lane root (default target dir; global `kache` rustc wrapper active, as the engine would inherit), I ran the spec's commands:
  - `cargo fmt --all --check` exited 0 in about 0 s.
  - `cargo clippy --all-targets -- -D warnings` exited 0 in 2 s.
  - `cargo test --lib band_ -- --nocapture` exited 0 in 2 s with `0 passed; … 13 filtered out`, so the block's `grep -q 'test result: ok. 6 passed'` fails at base as intended.
  - `grep -q '"band"' cartridge.json` exited 1 at base, as intended.
  - The worktree was removed with `git worktree remove` (no `--force`).
- Blocks were run one command at a time through a script, not through `sh -eu -c`, because a local safety hook blocked dynamic `sh -c`. The grep logic was checked by reading it.
- All timings are far below the 120 s cap. A lane without the `kache` cache would build cold. Round 1 measured that path at 5 s for clippy and 3 s for tests, so the limit is not at risk.
- Code reads: service.rs:33–80 (`Config`, `validate`), :83–100 (`Service`, `Tool`), :243–291 (`describe`, `registry`), :380–420 (`invoke`); lib.rs `start` (one `OnceLock` service); tests.rs `Config {` at 49/127/338/370/414/477; harness.ctg lib.rs:679–704; README §Protocol and §Refresh.

Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (85/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: make one bounded revision of prd.md and spec01.md for findings 1–8, plus the one-line harness Decision amendment (finding 5), then run a Round 3 review.
