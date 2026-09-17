# @live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars review history

Plan: `@live/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars`,
`prd.ctg/.cartridge/boards/live/prds/the-voice-runs-on-this-machine-with-no-network/live-speaks-and-listens-through-local-sidecars/prd.md`.
Scope: executable leaf — `live` gains a `provider` setting and a local
speech/brain/speech pipeline behind a transport seam. Accountable cartridge:
`live.ctg`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none observed. The leaf and its siblings were created
2026-09-17; no prior canonical ID, no prior `review.md`, no
`OPEN-WORK-REVIEW.json` entry for this scope.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: `prd.ctg` at `20d140de63e97ff6e50b3353617759c4172f5fc1`;
`live.ctg` at `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`. The reviewed plan and
spec are untracked/dirty working-tree files in `prd.ctg`. The code repository
`live.ctg` is dirty from another session on `.cartridge/docs/README.md`,
`.cartridge/help.md`, `cartridge.json`, `init.lua`, `src/service.rs`,
`src/store.rs`, plus an untracked `.DS_Store`.

| Input | Content digest |
| --- | --- |
| Plan | `…/live-speaks-and-listens-through-local-sidecars/prd.md` — `c169f3a853778a28a5ff4309a3d6fef1af6b728e80c11a14e32412d78605bce8` |
| Specs | `…/specs/spec01.md` — `388159253f2df385ef013a6b90f69334b3be4fa19ec1a3d0c5344d9e24b03c13` |
| Parent | `…/the-voice-runs-on-this-machine-with-no-network/prd.md` — `f82ba1f695bf682b51fd8e914ab9b509e16ff1faf4425eea72bbabc9a5b06c79` |
| Material contracts/dependencies | `live.ctg/src/service.rs` (worktree) `625d961b20f5c36109d15384fe38fa3199042bcf266b9e5bd03f02a6b4c39f78`, at `HEAD` `1c0fd641492f24ad9b76e327607fccbadf92d9e165b16238bef809dc7920735e`; `src/socket.rs` `4bd9f0e029b34401c4637cead4d88e06c806f05dfd7c532465afa84f4bd5cb1f`; `src/audio.rs` `976cf78d40bf39cd9bebc5d2600311e93263fbf6fd5f099d64820abefbddcd9d`; `src/lib.rs` `506094581506da7c8eb7b1d10ee80c1fb81c1d411ccfc3b1a94987c7969995f3`; `cartridge.json` (worktree) `0ee7bb2a924f48a6169ad7299c34d5444723d31727bea4018660a84ed0812ccc`, at `HEAD` `f4454e6ba24c9caab14b13ae6195dce504c516ef752e6edf6767b9c37e08e08f`; `Cargo.toml` `4123da8f59a3b8ee38d16ac9500dadcb68ed0b91e021b8639fea6137e3919d8f`; engine facts from `prd.ctg/.cartridge/templates/spec.md` and `prd.ctg/src/lifecycle.ts`, `prd.ctg/src/planner.ts`; grant enforcement from `cartridge.ctg/src/sandbox/mod.rs`, `cartridge.ctg/src/loader/document.rs` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | One observable outcome, one accountable cartridge, a real parent carrying measured budgets, 250 words in the leaf — inside the 150–300 target. The seam idea is correct and the reuse story is honest. −2: the outcome quietly includes *creating* `live.ctg/README.md`, which does not exist (`git ls-files` lists no root `README.md`; only `.cartridge/help.md` and `.cartridge/docs/README.md` are tracked), while the acceptance box reads as an edit to an existing file. −2: the local path's failure behaviour is not in scope anywhere — a dead sidecar, a refused brain endpoint or non-PCM audio has no named event, no acceptance box and no step, although `Service::event` already has an `"error"` arm waiting for one. |
| Ownership and reuse | 17 | Correct owner and repo. Genuine reuse verified by reading: `audio.rs` already hands PCM16@24 kHz to a callback and owns the speaker queue, so the local path needs no capture change; `store.rs` fragments already carry both transcript roles; `Service::delegated` and the `watch`/`reply` path are transport-agnostic; `socket::pcm` is plain base64 and survives the split. Sidecars stay commands and URLs — nothing vendored. Spec footprint is unioned with the PRD footprint by `prd.ctg/src/planner.ts:7`, so `.cartridge/tests/integration/local.test.ts` is authorized even though the PRD footprint omits `.cartridge/tests`. −1: the spec footprint omits `src/socket.rs` although step 2 edits it (`impl` of the new trait); it passes collection only because the PRD reserves all of `src`. −1: this leaf reserves all of `src` and all of `tools`, the widest lock on the board, and collides with every sibling's footprint; correct only because the four siblings carry `needs` edges. −1: a compiled Swift sidecar under `tools/stt/` would be an untracked file *inside* the footprint (`live.ctg/.gitignore` is `target` only, and is in neither footprint), so collect would commit the binary or abort. |
| Dependencies and implementable slices | 13 | Seven ordered steps, each real and each small. The two load-bearing code claims I could confirm are true: `src/socket.rs:14` is `const URL: &str = "wss://api.openai.com/v1/live/sessions"`, and `socket::connect` is called from exactly one site. −3: step 4's "pick the transport from configuration; nothing else changes" is false at the one line that decides whether the feature works — `start_voice` calls `let key = socket::credential(&self.config.credentials)?` (`src/service.rs:236`; `HEAD` 228) *before* any transport choice, and in local mode that returns `Err("No OpenAI API key…")`, so the conversation never opens. `Live { session: Arc<Session> }` (`:50`) and `use crate::socket::{self, Session}` (`:5`) also change type, and `stop_voice`/`reply` reach the session through that field. −2: `Session`'s surface is four things, not three. `pub id` is read at `:249` immediately after `connect` and becomes the key of `self.live` and of every `Fragment.live` and `lifecycle` row; the spec's constructor signature ("taking the session configuration and an event callback") never says the local transport must mint one. −2: the line anchors are wrong for the stated base. The spec says the lane is cut from `HEAD`, but `service.rs:242`/`:503` are the *dirty worktree's* lines; at `HEAD` they are 233 and 397. Also: step 3 says "stream the brain" and the footprint carries `Cargo.toml`/`Cargo.lock`, but no HTTP client exists in the manifest today (no `reqwest`, `hyper` or `ureq` in `Cargo.lock`) and the plan never names the dependency it is about to add. |
| Observable acceptance and baseline evidence | 6 | Boxes 2, 6 and 7 are checkable in principle. The rest are not, and the Verify section does not hold. **Box 3 is vacuous**: `.cartridge/tests` contains one empty `unit/` directory and zero tracked files, so "every existing test in `.cartridge/tests` passes unchanged" is true of the empty set; the actual GPT-path regression guard is the `#[cfg(test)]` modules in `src/socket.rs` and `src/audio.rs`, which no box names. **Box 4 names two unobservable events**: `Service::event` (`src/service.rs:503`) has arms for `session.output_audio.delta`, `session.input_transcript.delta`, `session.output_transcript.delta`, `session.delegation.created`, `session.usage.updated`, `session.closed` and `error` — there is **no `session.started` arm** (the GPT path consumes it inside `socket::connect` before the callback is installed), and `session.output_audio.delta` returns early into `voice.playback` with no record write, no return value and no event-stream op on the cartridge (`call` dispatches only `status`, `conversations`, `open`, `voice`, `state`, `context`, `agents`, `attach`, `delegate`, `watch`, `reply`, `note`, `cancel`; `bridge.rs` has no emit). With no audio device `entry.voice` is `None` and the delta is discarded outright. Two of the five ordered observations have no named channel. **Box 1's grant clause is not expressible**: `grant` is static manifest data with no per-setting conditioning, and `cartridge.ctg/src/sandbox/mod.rs:305` compiles any non-empty `grant.net` to blanket `(allow network*)`. **Box 5 asserts a field the service ignores**: `Service::delegated` hard-codes `prompt: "Voice request"` (`:599`) and overwrites it from the transcript at `:308`. Verify: the negated greps use the correct `if grep -qn …; then exit 1; fi` idiom (credit), but blocks 2 and 3 both end in `… 2>&1 \| tail -20`, and under `sh -eu` a pipeline's status is the last command's — I confirmed `sh -eu -c 'false 2>&1 \| tail -2'` exits **0**, so a failing `cargo test` or `bun test` passes collection silently. Block 2's cold pass-1 build cannot fit 120 s (168 lockfile crates including `rusqlite` with `bundled` C SQLite, `mlua` with `lua54`, `ring`, `cpal` and `rustls`, plus the unplanned HTTP client; the existing `live.ctg/target` is 1.0 GB). Block 3 cannot work at all: a `bun test` against a Rust cartridge needs a built `lib<name>.dylib` under `target/debug` or `target/release` (the convention in `sessions.ctg/.cartridge/tests/integration/native.ts`), no block produces one, and block 2 deliberately builds into `$HOME/.cache/…` instead. |
| Failure, recovery and compatibility | 9 | Real credit: the endpoint-constant grep is a genuine regression guard (it matches today), and pinning `CARGO_TARGET_DIR` off the live target is the right instinct against the known hot-restart hazard. −4: `grant.exec` is `["tmux"]`, and `cartridge.ctg/src/sandbox/mod.rs:239-265` emits `(allow process-exec …)` per granted program, so the local provider **cannot spawn its Swift sidecar** — no acceptance box, no step and no verify line covers the grant. −3: the stated mitigation for the dirty tree is not something the engine implements. `prd.ctg/src/lifecycle.ts:144-157` commits every changed in-footprint path; the foreign edits to `src/service.rs`, `src/store.rs`, `cartridge.json`, `.cartridge/help.md` and `.cartridge/docs/README.md` are **all inside this footprint**, and the lane's `git merge --ff-only` (`lifecycle.ts:168`) onto a `repo` whose `src/service.rs` is dirty and which the lane also modified fails outright. "The collector must check and refuse to sweep" is advice to a reader, not a control. −2: no error or recovery story for the local pipeline; `error` and `session.usage.updated` are handled by the service and appear in neither event list. −2: the default when `provider` is absent in an existing profile is stated only in the spec's box 1, not in the PRD, so the compatibility promise for every already-configured install lives in the wrong document. |
| Reviewer total | **61** / 100 | FAIL (threshold 90). Eight blocking findings. |

### Findings and concrete revisions

Blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| **B1** | `specs/spec01.md` Verify blocks 2 and 3 swallow the exit status. `cargo test --lib 2>&1 \| tail -20` and `bun test … 2>&1 \| tail -20` are the last commands in their blocks; under `sh -eu` the pipeline's status is `tail`'s. | `sh -eu -c 'false 2>&1 \| tail -2; echo "block exit reached: $?"'` printed `block exit reached: 0`. As inert as a negated `grep`. | Capture the status: `cargo test --lib > "$out" 2>&1 || { tail -40 "$out"; exit 1; }; tail -20 "$out"`, with `$out` outside the footprint (e.g. under the pinned `CARGO_TARGET_DIR`). Same for the `bun` block. |
| **B2** | Verify block 2's cold pass-1 build exceeds the 120 s per-block limit. | 168 `name =` entries in `Cargo.lock`, including `rusqlite` with `bundled` (C SQLite), `mlua` with `lua54` (C Lua), `ring`, `cpal`, `rustls`, `tokio-tungstenite` — plus an HTTP client the plan has not yet named. The existing `live.ctg/target` is 1.0 GB. The lane pass starts cold on a fresh `$HOME/.cache/cartridge-verify/live-local`. | Either seed the pinned directory in a step before collection and say so in the block's comment, or drop the whole-crate build from Verify and prove the seam with a target that compiles in budget. Do not rely on warmth the first pass cannot have. |
| **B3** | Verify block 3 has no module to load. A `bun test` against a Rust cartridge needs the built `liblive.dylib` from `target/debug` or `target/release`; block 2 builds into `$HOME/.cache/…` instead, and no block builds a dylib. | `sessions.ctg/.cartridge/tests/integration/native.ts:17-28` is the in-repo convention: `CARTRIDGE_BIN` **and** `SESSIONS_MODULE`/`target/{debug,release}/libsessions.dylib`. `live.ctg` has no TypeScript source for a bun test to import (`git ls-files` is `src/*.rs` only). | Worse than failing: a stale `target/release/liblive.dylib` from an earlier manual build would make the block **pass against old code**. Prove the local pipeline with Rust `#[test]`s driving the transport and its event callback directly against loopback stubs, which needs no host, no dylib and no `CARTRIDGE_BIN` — and keeps pass 2 from rebuilding the running cartridge's dylib. |
| **B4** | `spec01.md` acceptance box 4 asserts an ordering of events, two of which are not observable through any surface. | `Service::event` (`src/service.rs:503-575`) has **no `session.started` arm**; the GPT path consumes that event inside `socket::connect` (`src/socket.rs:110-120`) before the callback exists. `session.output_audio.delta` returns early into `voice.playback` (`:511-519`) with no record write; with no audio device `entry.voice` is `None` and it is dropped. `call` (`:114-153`) exposes no event stream and `bridge.rs` has no emit. | Say where the ordering is observed. Either assert it at the transport's event callback in a Rust test, or change the box to the surfaces that exist: the `Fragment` rows the two transcript deltas write, the `lifecycle` row `session.closed` writes, and the PCM the test's own callback receives. Drop `session.started` from the "service already handles" list in both `prd.md` and `spec01.md` — it is a constructor handshake, not a dispatched event. |
| **B5** | `spec01.md` box 3 and `prd.md` box 4 ("the existing tests in `.cartridge/tests` still pass unchanged") are vacuous. | `.cartridge/tests` contains one empty `unit/` directory; `git ls-files` lists no file under it. The real GPT-path guard is the `#[cfg(test)] mod tests` in `src/socket.rs` (3 tests) and `src/audio.rs` (3 tests). | Name the actual guard: "`cargo test --lib` passes with the same test count as `HEAD`, and `src/socket.rs`'s endpoint constant is byte-identical." An acceptance box satisfied by the empty set is not a check. |
| **B6** | `spec01.md` box 1's clause "`grant.net` no longer requires `api.openai.com` when the provider is local" is not implementable and not checkable. | `grant` is static manifest data (`cartridge.ctg/src/loader/document.rs`), with no setting-conditional form; `cartridge.ctg/src/sandbox/mod.rs:305` turns any non-empty `grant.net` into blanket `(allow network*)`, and the local endpoints on loopback need it non-empty anyway. `grant.net` entries must be a bare host name or `*` (`document.rs:244-250`), so a URL setting cannot be interpolated into it. | Delete the grant clause and keep the property where it is actually testable — box 6's "the test fails if any request leaves loopback". If the intent is to drop the OpenAI env grant in local mode, say that instead and state what happens to `grant.env: ["OPENAI_API_KEY"]`. |
| **B7** | The Swift sidecar cannot be spawned: `cartridge.json`'s `grant.exec` is `["tmux"]`. | `cartridge.ctg/src/sandbox/mod.rs:237-265` builds the seatbelt profile from `grant.exec`, emitting `(allow process-exec <path>)` per granted program (or `(allow process-exec)` only for `*`). No acceptance box, step or verify line mentions `grant.exec`. | Add the sidecar to `grant.exec` in step 5, add it to box 1 beside the four settings, and add `grep -q '"exec"' … ` / a targeted check to Verify block 1. Note that editing the manifest untrusts the cartridge, so the host needs a re-trust before the local path can be exercised live. |
| **B8** | The spec's mitigation for the dirty `live.ctg` tree is not a control the engine implements, and the lane cannot integrate as planned. | `prd.ctg/src/lifecycle.ts:144-157` runs `git status --porcelain` scoped to the footprint and commits **every** changed in-footprint path. The foreign edits to `src/service.rs`, `src/store.rs`, `cartridge.json`, `.cartridge/help.md`, `.cartridge/docs/README.md` are all inside this PRD's footprint (`src`, `cartridge.json`, `.cartridge/help.md`, `.cartridge/docs`). `lifecycle.ts:168` then runs `git merge --ff-only` into `repo`, which fails when a dirty `src/service.rs` would be overwritten. | Resolve the foreign edits before this PRD starts — commit them under their own record or stash them — and say so as a prerequisite in `prd.md`, not as an instruction to the collector. Alternatively narrow the footprint from `src` to the four files this work touches, which removes `src/store.rs` from the sweep but not `src/service.rs`. |

Non-blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| N1 | Step 4's "nothing else changes" is wrong on the one line that matters. | `src/service.rs:236` `let key = socket::credential(&self.config.credentials)?` runs before any transport choice; in local mode it errors "No OpenAI API key". `Live.session: Arc<Session>` (`:50`) and the `use` at `:5` change type. | Make step 4 explicit: move the credential lookup inside the GPT branch, and name the `Live.session` type change. |
| N2 | `Session` is four things, not three. | `pub id` is read at `src/service.rs:249` and keys `self.live`, `Fragment.live` and every `lifecycle` row. | Add the id to the seam's contract in box 2 and say how the local transport mints one. |
| N3 | Line anchors are the dirty tree's, not the stated base's. | `socket::connect` is `service.rs:242` in the worktree, `:233` at `HEAD`; `Service::event` is `:503` / `:397`. `socket.rs:14` is correct in both. | Re-anchor to `HEAD`, or say the anchors are worktree lines. |
| N4 | Box 5's "the tool's prompt" describes a field the service ignores. | `Service::delegated` sets `prompt: "Voice request"` (`:599`) and `dispatch` overwrites it with `self.spoken(&task)` (`:308`). `session.delegation.created` is read only for `delegation.target`, `delegation.id` and `offset_ms` (`:542-550`). | Assert what the code reads: target, id and the transcript-derived prompt that reaches `watch`. |
| N5 | Two handled events are in neither event list. | `Service::event` also handles `session.usage.updated` and `error`. | List them, and decide whether the local transport reports sidecar/endpoint failures through `error`. |
| N6 | `live.ctg/README.md` does not exist. | `git ls-files` in `live.ctg`. | Say "create"; `grep -q 'provider' README.md` in Verify block 1 fails today, which is correct but undocumented. |
| N7 | The spec footprint omits `src/socket.rs` although step 2 edits it. | Spec frontmatter lists `src/lib.rs`, `src/local.rs`, `src/service.rs`, `src/transport.rs`. | Add it, or rely explicitly on the PRD's `src`. |
| N8 | No `.gitignore` plan for a compiled sidecar. | `live.ctg/.gitignore` is `target`; `tools` is in the footprint, and collect uses `--untracked-files=all`. | Add the build output to `.gitignore` and put `.gitignore` in the footprint, or build into `target/`. |
| N9 | Verify's documentation checks are one-word greps. | `grep -q 'provider' README.md`, `grep -q 'provider' .cartridge/help.md`, for a box demanding both providers, three settings and the sidecar's stdin/stdout contract. | Grep for the setting names and the sidecar contract, or drop the pretence of proof. |
| N10 | The URL ban covers only `src/local.rs`. | `if grep -qn 'https\?://' src/local.rs` — `src/transport.rs` and `src/service.rs` are unguarded, and a default endpoint could live in either. | Extend to the new modules, or scope the check to what it means. |
| N11 | The HTTP client dependency is unnamed. | No `reqwest`/`hyper`/`ureq` in `Cargo.lock`; `Cargo.toml`/`Cargo.lock` are in the footprint. | Name it. `[lints.rust] warnings = "deny"` means the new modules must also be warning-free. |
| N12 | `CARTRIDGE_BIN` default differs from the in-repo convention. | Spec: `$HOME/.local/bin/cartridge`. `sessions.ctg/.cartridge/tests/integration/native.ts:16`: `../cartridge.ctg/target/release/cartridge`. | Moot if B3 is resolved by dropping the host-driven test. |

Disposition: **revise**. Keep the scope, the owner and the seam — the
architecture is right and the reuse claims mostly hold. One coherent revision
should (a) rewrite the Verify section so each block propagates its own exit
status and fits 120 s cold, (b) replace the host-driven `bun` test with Rust
tests against loopback stubs, (c) rewrite acceptance boxes 1, 3, 4 and 5 onto
surfaces that exist, (d) add the `grant.exec` gap to box 1 and step 5, and
(e) move the dirty-tree resolution out of the spec's prose and into a stated
prerequisite on `prd.md`. No split is warranted; the leaf is one outcome.

Validation: read-only. `cwd` = `/Users/feb/dev/cartridge` unless noted.
`cat` of the parent PRD, leaf PRD, `specs/spec01.md`,
`prd.ctg/.cartridge/workflows/review-plan.md`,
`prd.ctg/.cartridge/templates/review.md`,
`prd.ctg/.cartridge/templates/spec.md` — exit 0.
`cwd` = `live.ctg`: `git log --oneline -3`, `git status --porcelain`,
`git ls-files`, `wc -l src/*.rs`, `cat src/socket.rs src/lib.rs src/audio.rs
Cargo.toml build.rs .gitignore .cartridge/.gitignore cartridge.json`,
`sed -n` over `src/service.rs` at 200-300 / 495-700,
`git show HEAD:src/service.rs | grep -n`, `grep -c '^name = ' Cargo.lock` = 168,
`du -sh target` = 1.0G, `ls .cartridge/tests .cartridge/tests/unit` (one empty
directory) — all exit 0 except `ls` of the absent `README.md`/`tools`, exit 1
as expected.
`cwd` = `cartridge.ctg`: `grep -n` over `src/sandbox/mod.rs`,
`src/loader/document.rs` — exit 0.
`cwd` = `prd.ctg`: `grep -n footprint src/*.ts`, `sed -n '120,180p'
src/lifecycle.ts` — exit 0.
Idiom probe: `sh -eu -c 'false 2>&1 | tail -2; echo "block exit reached: $?"'`
→ `block exit reached: 0` (evidence for B1).
No cargo build, no cargo test, no daemon interaction, no write outside this PRD
directory.
Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context),
session `4c2735a1-d1de-4e8d-aa99-d593f257106d`, launched fresh with no
authorship of the reviewed revision.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (61/100, below the 90 threshold, eight blocking findings).
Unresolved blocking findings: B1, B2, B3, B4, B5, B6, B7, B8.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision addressing B1–B8 and, where cheap, N1–N12;
then re-review within the remaining allowance. Do not begin implementation:
B8 means collection cannot complete against the current `live.ctg` working tree
regardless of the code.

## Round 2 — 2026-09-17

Presented revision: `prd.ctg` at `b27a7cb3993c01f1735c6698fb8d871fa4402869`;
`live.ctg` at `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`. The plan and spec are
still untracked working-tree files in `prd.ctg`. Only `specs/spec01.md` changed
since round 1: `prd.md` is **byte-identical** to the round-1 revision
(`c169f3a853778a28a5ff4309a3d6fef1af6b728e80c11a14e32412d78605bce8` in both
rounds), so every round-1 finding written against `prd.md` is unresolved by
construction. `live.ctg` is unchanged and still dirty from another session on
`.cartridge/docs/README.md`, `.cartridge/help.md`, `cartridge.json`, `init.lua`,
`src/service.rs`, `src/store.rs`, plus an untracked `.DS_Store`.

| Input | Content digest |
| --- | --- |
| Plan | `…/live-speaks-and-listens-through-local-sidecars/prd.md` — `c169f3a853778a28a5ff4309a3d6fef1af6b728e80c11a14e32412d78605bce8` (unchanged from round 1) |
| Specs | `…/specs/spec01.md` — `d4f6a4b6e6a491b1319edab7e1f80999d4588f4cc3beb18ef9007ffb02248c6f` (was `3881592…`) |
| Parent | `…/the-voice-runs-on-this-machine-with-no-network/prd.md` — `f82ba1f695bf682b51fd8e914ab9b509e16ff1faf4425eea72bbabc9a5b06c79` |
| Material contracts/dependencies | `live.ctg/src/service.rs` (worktree) `625d961b20f5c36109d15384fe38fa3199042bcf266b9e5bd03f02a6b4c39f78`, at `HEAD` `1c0fd641492f24ad9b76e327607fccbadf92d9e165b16238bef809dc7920735e`; `src/socket.rs` `4bd9f0e029b34401c4637cead4d88e06c806f05dfd7c532465afa84f4bd5cb1f`; `src/audio.rs` `976cf78d40bf39cd9bebc5d2600311e93263fbf6fd5f099d64820abefbddcd9d`; `cartridge.json` (worktree) `0ee7bb2a924f48a6169ad7299c34d5444723d31727bea4018660a84ed0812ccc`, at `HEAD` `f4454e6ba24c9caab14b13ae6195dce504c516ef752e6edf6767b9c37e08e08f`; `Cargo.toml` `4123da8f59a3b8ee38d16ac9500dadcb68ed0b91e021b8639fea6137e3919d8f`; `prd.ctg/src/lifecycle.ts`, `prd.ctg/src/planner.ts`, `prd.ctg/.cartridge/templates/spec.md`; `cartridge.ctg/src/sandbox/mod.rs` |

### Round-1 blocking findings, checked against the files

| R1 | State | Evidence read this round |
| --- | --- | --- |
| B1 `\| tail` swallows the exit status | **resolved** | No `tail` remains. Block 2 is a bare `cargo test --lib`; block 3 ends `test -x "$out"; rm -f "$out"` under `sh -eu`, so a compile failure aborts the block. |
| B2 cold build cannot fit 120 s | **partial** | The build is unchanged; the mitigation is a comment ("the implementer builds into that same directory"). `$HOME/.cache/cartridge-verify` does not exist today, and `live.ctg/cartridge.json`'s own `commands.build`/`check`/`test` recipes set no `CARGO_TARGET_DIR`, so the ordinary developer path warms `target/`, not the pinned directory. No step seeds it. Not blocking — a timeout fails loudly and a rerun is warm — but the gate still rests on an out-of-band precondition. |
| B3 `bun test` with no dylib | **resolved** | The host-driven block is gone. Tests are `#[cfg(test)]` in `src/local.rs` driving `local::connect` against a stub speech command and two `127.0.0.1:0` listeners. No `CARTRIDGE_BIN`, no dylib, no daemon. |
| B4 unobservable events | **resolved in the spec, unresolved in `prd.md`** | The spec now states the transport callback is the channel and says why (`Service::event` has no `session.started` arm; the audio arm returns into playback). Confirmed at `HEAD`: `git show HEAD:src/service.rs` dispatches `session.output_audio.delta` (405), `session.input_transcript.delta`/`session.output_transcript.delta` (416), `session.delegation.created` (436), `session.usage.updated` (445), `session.closed` (452), `error` (460) — no `session.started`. `prd.md` still lists `session.started` among the events "the service already handles". See B10. |
| B5 vacuous "existing tests pass" | **resolved in the spec, unresolved in `prd.md`** | Spec box 3 names `cargo test --lib` and the `src/socket.rs`/`src/audio.rs` modules. `prd.md` box 4 still says "the existing tests in `.cartridge/tests` still pass unchanged"; `git ls-files` in `live.ctg` lists no file under `.cartridge/tests`, which holds one empty `unit/` directory. See B9. |
| B6 conditional `grant.net` | **resolved** | The clause is gone. Correctly so: `cartridge.ctg/src/sandbox/mod.rs:304-306` turns any non-empty `grant.net` into `(allow network*)` + `(allow system-socket)`, so the existing `["api.openai.com"]` already permits the loopback endpoints and nothing needs conditioning. |
| B7 `grant.exec` misses the sidecar | **resolved** | Box 1 requires `grant.exec` to name the sidecar path, with the right citation: `sandbox/mod.rs:238-265` resolves each granted program and emits `(allow process-exec (literal …) …)`, `(allow process-exec)` only for `*`. Verify block 1 greps `sttd` in `cartridge.json`. Weak proof (see N5) but present. No step carries it, and the re-trust a manifest edit forces is still unmentioned. |
| B8 "the collector must check git status" | **partial** | Replaced by a stated landing precondition, which is the right kind of object. Its mechanism is imprecise (see N1), and it lives in the spec rather than in `prd.md`, which round 1 asked for. |
| N7 `src/socket.rs` not in the footprint | resolved | Spec footprint line 7. |
| N8 compiled sidecar not gitignored | resolved | Box 7 plus `grep -q 'sttd' .gitignore`; `.gitignore` is in the spec footprint, and `prd.ctg/src/planner.ts:5-9` unions spec and PRD footprints, so it is authorized even though `prd.md` omits it. |
| N1, N2, N3 | resolved | Box 2 puts `socket::credential` on the GPT branch and `id` in the seam. The surviving anchors are correct at `HEAD`: `src/socket.rs:14` is the endpoint constant; `lifecycle.ts:144-157` is the footprint status/commit; `sandbox/mod.rs:239-265` is the exec emission (the loop opens at 238). |
| N4, N5, N9, N10, N11 | unresolved | See N2–N6 below. |

### Verify blocks against a lane cut from `HEAD`

Block 1 (shape) would **pass** given the described implementation. Every `test -f`
target is created by steps 1–4; `grep -q 'wss://api.openai.com/v1/live/sessions'
src/socket.rs` matches today; the negated greps use the `if grep -q …; then exit
1; fi` idiom throughout; `README.md` is created, not edited. The one constraint
worth naming is `if grep -qn 'socket::connect' src/service.rs; then exit 1; fi`,
which forbids the dial in `service.rs` while box 2 keeps `socket::credential`
there — consistent, but the block's comment ("or fetches a credential") claims a
check it does not make.

Block 2 (`cargo test --lib`) would **pass only on a warm
`$HOME/.cache/cartridge-verify/live-local`**, which does not exist. `Cargo.lock`
carries 168 packages including `rusqlite` with `bundled`, `mlua` with `lua54`,
`ring`, `rustls` and `cpal`; a cold dev build of that closure against a 120 s
limit is a coin flip on this machine. It is at least a loud failure, not a silent
pass. Two facts in its favour that I confirmed: `live.ctg/Cargo.toml` declares
its own `[workspace]` and has no path dependencies, so a lone lane worktree
builds (unlike the sibling-dependent cartridges); and pinning `CARGO_TARGET_DIR`
outside the repository is correct for pass 2, which runs in the live checkout
where a `target/debug` write would hot-restart the running cartridge.

Block 3 (`swiftc`) would **probably pass**: `/usr/bin/swiftc` exists,
`xcode-select -p` is `/Library/Developer/CommandLineTools`, the output goes to
`${TMPDIR}` outside the footprint, and the exit status propagates. Two caveats.
`-parse-as-library` links an executable, so `sttd.swift` must carry `@main` or
the block fails on an undefined `_main` — unstated. And no collection in this
repository has ever run `swiftc` in a Verify block (`grep -rl swiftc` over the
boards matches only this spec), whereas `cargo` is well precedented — for
example `root/prds/smoke-passes-mcp-and-proxy/collection.md` records a cargo
block finishing in 0.04 s.

All three blocks are moot in pass 2 until the foreign work lands: pass 1 runs in
the lane, then `lifecycle.ts:168` runs `git merge --ff-only` into a `live.ctg`
whose `src/service.rs` is dirty and which the lane also rewrote, and that fails.

### Footprint

Complete and not over-wide for the described work, once the union is taken. The
spec adds `src/socket.rs`, `tools/stt/sttd.swift`, `.gitignore` and
`.cartridge/docs/README.md`; `prd.ctg/src/planner.ts:5-9` unions spec and PRD
footprints into `feet`, so `.gitignore` is authorized although `prd.md` omits it.
Nothing in the spec footprint is untouched by the plan. The width comes from
`prd.md`, which still reserves all of `src` and all of `tools` — the widest lock
on the board, correct only because the four siblings carry `needs` edges.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Same correct scope as round 1, and the spec now carries the measured sidecar numbers (SIGUSR1 finalisation proved over two turns, 25–47 ms first token, 0.119 s first audio) that make the seam's shape falsifiable. −2: the local path's failure behaviour is still in scope nowhere — a dead sidecar, a refused brain endpoint or non-PCM audio has no event, no box and no step, although `Service::event` has an `error` arm at `HEAD:460`. −2: `prd.md` is unchanged and still describes a set of events the service does not all handle, so the plan's two documents now contradict each other on the same fact. |
| Ownership and reuse | 17 | Correct owner and repo; the reuse claims I re-checked all hold. `Cargo.toml` is self-contained (`[workspace]`, no path deps), so the lane builds alone. Footprint gaps from round 1 closed. −1: `prd.md`'s `src` + `tools` reservation remains the widest lock on the board. −1: the HTTP client is still unnamed although `Cargo.toml`/`Cargo.lock` are in the footprint and `[lints.rust] warnings = "deny"` makes a new module's warnings fatal. −1: `granted_exec` (`sandbox/mod.rs:151-176`) resolves a multi-component grant against the cartridge root and returns `None` when the file is absent, so `grant.exec: ["tools/stt/sttd"]` silently grants nothing until `build-stt` has run — the ordering is unstated. |
| Dependencies and implementable slices | 15 | Six ordered steps, each small and each real; the surviving line anchors are correct at `HEAD` (verified individually). −2: no step names the HTTP dependency the brain and mouth calls need, and no step decides whether they are hand-rolled on `tokio` or a new crate. −2: no step seeds the pinned `CARGO_TARGET_DIR` that block 2 depends on, and `cartridge.json`'s own build recipes point the other way. −1: `grant.exec` and the re-trust it forces appear in box 1 only, not in any step. |
| Observable acceptance and baseline evidence | 13 | The largest gain. The proof is now Rust tests against a stub command and two loopback listeners — no host, no dylib, no model, no network — and the spec explains, correctly, why the service is not the observation channel. Exit statuses propagate. −3: `prd.md`'s boxes 3 and 4 remain unobservable and vacuous respectively (B9, B11). −2: box 5 observes SIGUSR1 "on the stub's own stdout", which is the NDJSON pipe the transport owns and parses — the test never sees it (B12). −1: box 3 calls the guards "test modules (`pcm`, `resample`)" when both modules are `mod tests` and `pcm`/`resample` are the functions under test, and it omits `src/service.rs`'s own `mod tests` (5 tests at `HEAD:963-1042`) although `service.rs` is the file this work rewires. −1: the documentation proof is still `grep -q 'provider' README.md` and `grep -q 'provider' .cartridge/help.md` for a box demanding two providers, four settings and the stdin/stdout/SIGUSR1 contract, and `grep -q 'sttd' cartridge.json` matches the `build-stt` recipe rather than proving `grant.exec`. |
| Failure, recovery and compatibility | 14 | `grant.exec` is in scope, the dirty tree is a stated precondition rather than an instruction to the collector, and the target directory is pinned off the live `target/`. −2: still no error or recovery story for the local pipeline; `error` and `session.usage.updated` appear in no box, step or event list. −2: the `provider` default (`"gpt"`) lives only in the spec, so the compatibility promise for every configured install is still in the wrong document. −1: the precondition's mechanism is misstated (N1) and sits in the spec rather than in `prd.md`, where round 1 asked for it. −1: block 2's warm-cache dependency is unenforced and contradicted by the cartridge's own recipes. |
| Reviewer total | **75** / 100 | FAIL (threshold 90). Four blocking findings. |

### Findings and concrete revisions

Blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| **B9** | `prd.md` acceptance box 4 is still the vacuous claim round 1 raised as B5: "With `provider: "gpt"` the existing tests in `.cartridge/tests` still pass unchanged." | `prd.md` is byte-identical to the round-1 revision. `git ls-files` in `live.ctg` lists no path under `.cartridge/tests`; the directory holds one empty `unit/`. The claim is true of the empty set. | Replace it with the spec's box 3: `cargo test --lib` passes and `src/socket.rs:14` still holds `wss://api.openai.com/v1/live/sessions`. Edit the box in place; do not rewrite `prd.md`. |
| **B10** | `prd.md`'s Outcome still lists `session.started` among "the same events the service already handles", which round 1 raised as B4 and which `spec01.md` now explicitly contradicts. | `git show HEAD:src/service.rs` dispatches `session.output_audio.delta`, the two transcript deltas, `session.delegation.created`, `session.usage.updated`, `session.closed` and `error` — no `session.started` arm. `src/socket.rs:121` consumes `session.started` inside `connect`, before any callback exists. `spec01.md` says so in its own prose. | Drop `session.started` from `prd.md`'s list and add `error` and `session.usage.updated`, which the service does handle and which the local transport will have to produce. |
| **B11** | `prd.md` acceptance box 3 — "A recorded utterance played into the pipeline produces a spoken reply and a transcript in the record" — has no proof path in any step or Verify block. | The spec's tests use a stub speech command and two loopback listeners; nothing plays a recorded utterance, nothing exercises the real Swift sidecar beyond `swiftc` compiling it, and no step produces a fixture. The end-to-end conversation is already the parent PRD's box 2. | Either name the observation (which command plays which fixture, and which `Fragment` row is read back) or delete the box and let the parent carry it. An acceptance box with no named check is the defect this method exists to catch. |
| **B12** | `spec01.md` box 5 asserts SIGUSR1 "the stub reports the signal it received on its own stdout" — a channel the test cannot read. | The stub's stdout is the NDJSON pipe `local::connect` owns and parses; an unrecognised line is dropped by the transport, so nothing reaches the test. This repeats round-1 B4's defect class: asserting through a channel that does not reach the observer. | Have the stub write the signal to a scratch file the test names (`$TMPDIR`, outside the footprint) and assert on the file, or emit a transport-level event for it. |

Non-blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| N1 | The landing precondition misstates the mechanism it cites. | `lifecycle.ts:145` runs `git status` in `tree`, which is the **lane** when a lane exists, so collect never commits the foreign edits sitting in `live.ctg` itself. The real blockers are the `git merge --ff-only` at `:168` and the `source footprint changed during integrated verification` check at `:176`. | Say that: the lane pass is unaffected, and collection fails at integration. The conclusion ("collectable only once that work is committed or reverted") is right either way. |
| N2 | The precondition lives in the spec, not in `prd.md`. | Round 1's B8 asked for a prerequisite on `prd.md`; `prd.md` is unchanged. | Move or mirror it into `prd.md`'s Outcome, where the board reads it. |
| N3 | The HTTP client is unnamed (round-1 N11, unresolved). | No `reqwest`/`hyper`/`ureq` in `Cargo.lock`; `Cargo.toml`/`Cargo.lock` are in the footprint; `[lints.rust] warnings = "deny"`. Loopback needs no TLS, so hand-rolling on `tokio` is viable — but the plan should say which. | Name it in step 2. |
| N4 | The URL ban still covers only `src/local.rs` (round-1 N10, unresolved). | `if grep -qn 'https\?://' src/local.rs` — `src/transport.rs` and `src/service.rs` are unguarded, and a default endpoint could live in either. | Extend the two negated greps to `src/transport.rs`. |
| N5 | `grep -q 'sttd' cartridge.json` does not prove `grant.exec`. | The same string appears in the `build-stt` recipe box 1 also requires, so the grep passes with the grant absent. | Grep the grant specifically, or check the composed manifest. |
| N6 | The documentation greps are one-word (round-1 N9, unresolved). | `grep -q 'provider' README.md` for a box demanding two providers, four settings and the stdin/stdout/SIGUSR1 contract. | Grep the setting names and `SIGUSR1`, or drop the pretence. |
| N7 | Box 6's "the tool's prompt" is a field the service ignores (round-1 N4). | `Service::event` reads only `delegation.target`, `delegation.id` and `offset_ms`; `Service::delegated` hard-codes the prompt and `dispatch` overwrites it from the transcript. Harmless in a transport-level test, but it is not a service contract. | Say the assertion is on the emitted event, not on what the service stores. |
| N8 | `grant.exec` resolution is ordered against the build. | `sandbox/mod.rs:151-176`: a multi-component grant resolves against the cartridge root and yields `None` when the file is absent, so the grant is silently empty until `build-stt` has run. Editing the manifest also untrusts the cartridge. | Say the sidecar is built before the host loads the local provider, and that a re-trust follows the manifest edit. |
| N9 | Block 2's comment claims a check block 1 does not make. | "The service no longer dials a transport, or fetches a credential, by default" — only `socket::connect` is grepped, and box 2 deliberately keeps `socket::credential` in `service.rs`. | Fix the comment. |
| N10 | `sttd.swift` must carry `@main` for `-parse-as-library`. | Otherwise block 3 fails at link on an undefined `_main`. | State it in step 4. |

Disposition: **revise**. The spec is materially better — the verification section
is now honest, the proof needs no host and no model, and six of the eight round-1
blockers are closed in it. The remaining work is small and mostly not in the spec
at all: `prd.md` was never touched, and three of the four blockers are its
unedited round-1 boxes. One bounded revision should (a) edit `prd.md`'s boxes 3
and 4 and its event list in place, (b) move the landing precondition into
`prd.md` with the corrected mechanism, (c) give box 5's SIGUSR1 assertion a
channel the test can read, and (d) promote the warm `CARGO_TARGET_DIR` from a
comment to a step. No split is warranted.

Validation: read-only. `cwd` = `/Users/feb/dev/cartridge` unless noted.
`cat` of `prd.md`, `specs/spec01.md`, `review.md`, the parent PRD,
`prd.ctg/.cartridge/workflows/review-plan.md`,
`prd.ctg/.cartridge/templates/review.md`,
`prd.ctg/.cartridge/templates/spec.md` — exit 0.
`shasum -a 256` over the plan, spec, parent and five `live.ctg` inputs; plan
digest equals round 1's exactly.
`cwd` = `live.ctg`: `git log --oneline -3`, `git status --porcelain`,
`git ls-files`, `cat .gitignore Cargo.toml cartridge.json build.rs`,
`ls -R .cartridge`, `grep -n 'cfg(test)' src/*.rs` (audio 243, service 1110,
socket 190), `sed -n` over the three test modules,
`git show HEAD:src/service.rs | grep -n '"session\.'` (no `session.started`
arm; `mod tests` at 963 with five `#[test]`), `grep -n delegation src/service.rs`
(`:543` checks `delegation.target != "client"`), `grep -n 'session.started'
src/socket.rs` (`:121`), `du -sh target` = 1.0G — exit 0.
`cwd` = `cartridge.ctg`: `sed -n '230,270p'` and `'295,315p'` of
`src/sandbox/mod.rs`, `grep -n 'fn granted_exec' -A 25`,
`grep -n 'fn installation_outside' -A 20` — exit 0.
`cwd` = `prd.ctg`: `sed -n '1,20p' src/planner.ts` (`feet` unions spec and PRD
footprints), `sed -n '120,200p' src/lifecycle.ts`, `grep -n 'async function
verify' -A 25`, `sed -n '240,275p' cartridge.json` — exit 0.
Environment probes: `which swiftc` = `/usr/bin/swiftc`; `xcode-select -p` =
`/Library/Developer/CommandLineTools`; `ls $HOME/.cache/cartridge-verify` —
exit 1, absent; `grep -rln cargo --include=collection.md` over the boards
(cargo is precedented in collections), `grep -rl swiftc` (only this spec).
No cargo, no swiftc, no daemon interaction, no write outside this PRD directory.
Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context),
session `4c2735a1-d1de-4e8d-aa99-d593f257106d`, fresh for round 2 with no
authorship of round 1 or of the reviewed revision.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (75/100, below the 90 threshold, four blocking findings).
Unresolved blocking findings: B9, B10, B11, B12. Round-1 B2 and B8 are partially
addressed and carried as N1, N2 and the block-2 deduction; B1, B3, B4, B5, B6 and
B7 are resolved in `spec01.md`, and B4 and B5 remain open in `prd.md` as B10 and
B9.
Rounds used / remaining: 2 / 3.
Next action: one bounded revision addressing B9–B12 — three of the four are
in-place edits to `prd.md`, which this revision never touched — then re-review
within the remaining allowance. Implementation may start in a lane; collection
still cannot complete until the foreign uncommitted work in `live.ctg` lands.

## Round 3 — 2026-09-17

Presented revision: `prd.ctg` at `148302f6` (the plan, spec and this review are
untracked working-tree files under
`.cartridge/boards/live/prds/the-voice-runs-on-this-machine-with-no-network/`);
`live.ctg` at `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`. **Both** documents
changed this round — `prd.md` was rewritten (round 2's decisive finding was that
it had not been) and `specs/spec01.md` was patched. `live.ctg` is unchanged and
still dirty from another session on `.cartridge/docs/README.md`,
`.cartridge/help.md`, `cartridge.json`, `init.lua`, `src/service.rs`,
`src/store.rs`, plus an untracked `.DS_Store`.

| Input | Content digest |
| --- | --- |
| Plan | `…/live-speaks-and-listens-through-local-sidecars/prd.md` — `9d01da320fedad6a6b2a9f7053e4f65219cc7a0ae0363db54fc5555e935bae0f` (was `c169f3a…` in rounds 1 and 2) |
| Specs | `…/specs/spec01.md` — `20f404f10c1fcd95e01ca5a0e2df49fe0c41828ca394f3105477ebbcd6ded734` (was `d4f6a4b…`) |
| Parent | `…/the-voice-runs-on-this-machine-with-no-network/prd.md` — `f82ba1f695bf682b51fd8e914ab9b509e16ff1faf4425eea72bbabc9a5b06c79` (unchanged) |
| Material contracts/dependencies | `live.ctg` at `HEAD`: `src/service.rs` `1c0fd641492f24ad9b76e327607fccbadf92d9e165b16238bef809dc7920735e`, `src/socket.rs` `4bd9f0e029b34401c4637cead4d88e06c806f05dfd7c532465afa84f4bd5cb1f`, `src/audio.rs` `976cf78d40bf39cd9bebc5d2600311e93263fbf6fd5f099d64820abefbddcd9d`, `cartridge.json` `f4454e6ba24c9caab14b13ae6195dce504c516ef752e6edf6767b9c37e08e08f`, `Cargo.toml` `4123da8f59a3b8ee38d16ac9500dadcb68ed0b91e021b8639fea6137e3919d8f`; `prd.ctg/src/lifecycle.ts`, `prd.ctg/src/planner.ts`, `prd.ctg/.cartridge/templates/spec.md`; `cartridge.ctg/src/sandbox/mod.rs`, `cartridge.ctg/src/loader/document.rs`; macOS 26.2 CommandLineTools SDK |

### Carried findings, checked against the files

| # | State | Evidence read this round |
| --- | --- | --- |
| B9 vacuous `.cartridge/tests` box | **resolved** | No acceptance box in either document names `.cartridge/tests`. `prd.md` box 4 is now "`cargo test --lib` passes, including the `mod tests` already in `src/socket.rs`, `src/audio.rs` and `src/service.rs`, and `src/socket.rs` still holds the GPT Live endpoint constant." The empty `.cartridge/tests/unit/` is no longer load-bearing anywhere. |
| B10 `session.started` claimed as an arm | **resolved** | `prd.md` now reads "…`session.closed` are the arms `Service::event` already dispatches, and `session.started` is consumed by the transport itself, as the GPT transport consumes it inside `connect` today." Both halves are true at `HEAD`: `git show HEAD:src/service.rs` dispatches `session.output_audio.delta` (405), the two transcript deltas (416), `session.delegation.created` (436), `session.usage.updated` (445), `session.closed` (452) and `error` (460), with no `session.started` arm; `src/socket.rs:121` matches `Some("session.started")` inside `connect`. The second half of the recommendation — add `error` and `session.usage.updated` to the list — was not taken; carried as a deduction, not a blocker. |
| B11 unprovable `prd.md` boxes / honest deferral | **partially resolved** | The unprovable "recorded utterance" box is gone, replaced by a stub-driven box that maps onto spec boxes 4 and 6, and by an explicit deferral paragraph. The deferral is **honest**: the parent's box 2 does carry the real-device claim ("A conversation held with `provider: "local"` covers, in one session: a spoken question answered from the repository, an interruption…, a floor claim…, and an answer that required the internet"), and its box 1 is "Every child is done". Four of the five `prd.md` boxes now have a discriminating check. Box 1's `grant.exec` half does not — see **B13**. |
| B12 SIGUSR1 observed on the transport's own pipe | **resolved** | Spec box 5 now reads "the stub traps SIGUSR1 and appends a line to a file the test names in its environment, which the test reads — not to its stdout, which the transport owns and parses." A spawned child inherits the test process's environment, so the channel exists. The scratch *location* is still unnamed — see N4. |
| B2 pinned `CARGO_TARGET_DIR` only a comment | **partially resolved** | It is now a step: step 4 sets "`commands.test` … to run `cargo test` with `CARGO_TARGET_DIR` pinned to the same path the Verify block uses". `.cartridge/justfile:54` fans `just test <owner>` out to the owner's `commands.test`, so the ordinary developer path would in fact warm `$HOME/.cache/cartridge-verify/live-local`, and dependency artefacts in a shared target directory are reused across the lane worktree and `repo`. Two gaps remain — see N1. |
| B8 landing-precondition mechanism | **partially resolved** | The prose mechanism is now right; **two of its three line citations are wrong** — see **N2**. And the precondition still lives only in `spec01.md`; round 1 (B8) and round 2 (N2) both asked for it on `prd.md`, which the board reads. Its conclusion holds: `src/service.rs`, `cartridge.json`, `.cartridge/help.md` and `.cartridge/docs/README.md` are dirty in `live.ctg` **and** in this footprint, so `git merge --ff-only` into `repo` fails and collection cannot complete until that work lands. |

### Claims checked directly

- **Test-module counts are true at `HEAD`.** `git show HEAD:src/<f>.rs | grep -c '#\[test\]\|#\[tokio::test\]'` gives `socket.rs` 3, `audio.rs` 3, `service.rs` 5, with `#[cfg(test)]` at `audio.rs:243`, `service.rs:963`, `socket.rs:190`. Spec box 3's "three, three and five" is exact.
- **`src/socket.rs:14`** is `const URL: &str = "wss://api.openai.com/v1/live/sessions";` at `HEAD`. Both the box and Verify block 1's grep are anchored correctly.
- **`cartridge.ctg/src/sandbox/mod.rs:239-265`** is the exec-grant block: `239` opens `for program in &grant.exec`, `granted_exec` resolves each, and the tail emits `(allow process-exec (literal …) (subpath …))`, with `(allow process-exec)` only for `*`. The citation in spec box 1 is accurate.
- **`SpeechAnalyzer.finalize(through:)` exists in this machine's SDK.** `Speech.framework/Modules/Speech.swiftmodule/arm64e-apple-macos.swiftinterface` declares `func finalize(through: CoreMedia.CMTime?)`. The SDK ships `arm64e`/`x86_64` interfaces only, which is the norm here (`SwiftUI.swiftmodule` is the same), so an `arm64` `swiftc` resolves it. Verify block 3's premise is real.
- **`cargo test` on an mlua-module `cdylib` is established here**, not a gamble: fourteen of the fifteen Rust cartridges are `crate-type = ["cdylib"]` with `mlua`, and all but one carry `#[cfg(test)]` modules that `commands.test` runs. No collection receipt in the repository has yet run `cargo test` in a Verify block (receipts show `cargo-nextest`, `cargo fmt`, `cargo clippy`), but `live.ctg`'s own `commands.test` is already `cargo test`.

### Footprint

`prd.md` and `spec01.md` now carry **identical** thirteen-path lists, so the
`feet` union (`prd.ctg/src/planner.ts:5-9`) adds nothing and there is no hidden
authorization. Checked for completeness against the described work by reading
the code the steps touch:

- `src/audio.rs` is correctly **absent**. `Voice::start(self.config.duplex, move |pcm| speaking.audio(&pcm))` (`src/service.rs:243`) is the whole capture wiring, so swapping the session type is a `service.rs` edit; `audio.rs` is only a regression guard.
- `init.lua` is correctly absent: it passes `cartridge.config` wholesale to `live.start`, so four new settings need no Lua change.
- `build.rs`, `src/bridge.rs`, `src/store.rs` are untouched by any step.
- The compiled `tools/stt/sttd` is a build artefact outside the footprint; the status sweep and the integrated check are both pathspec-scoped to the footprint, so it can neither be swept nor abort collection. Box 8's `.gitignore` requirement is belt-and-braces, not load-bearing.

I found nothing the described work would touch that is not listed. The
narrowing also dropped `src/store.rs` and `init.lua` out of the sweep, which
shrinks the collision with the foreign dirty tree without changing the
precondition's conclusion.

### Verify blocks against a lane cut from `HEAD`

Block 1 (shape) would **pass** given the described implementation: every
`test -f` target is created by steps 1–4, the endpoint grep matches today, the
negated greps all use `if grep -q …; then exit 1; fi`, and `README.md` is
created rather than edited. Its comment still overclaims (N5), and two of its
checks do not discriminate (B13, N3).

Block 2 (`cargo test --lib`) would **pass warm and is a coin flip cold**, as in
round 2, but the warmth now has a named producer (step 4) instead of a comment.
`live.ctg/Cargo.toml` declares its own `[workspace]` with no path dependencies,
so the lone lane worktree builds.

Block 3 (`swiftc`) would **pass** if `sttd.swift` carries `@main`
(`-parse-as-library` links an executable); the SDK carries the API it uses, the
output goes to `${TMPDIR}` outside the footprint, and the status propagates.

All three remain moot in pass 2 until the foreign work in `live.ctg` lands.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome, one accountable cartridge, a real parent carrying the measured budgets, and the two documents no longer contradict each other on any fact I could check. The deferral paragraph is the right shape and the parent genuinely carries what it defers. −1: the local path's failure behaviour is still in scope nowhere — a dead sidecar, a refused brain endpoint or non-PCM audio has no named event, no box and no step, although `Service::event` has an `error` arm at `HEAD:460` waiting for one. −1: the rewrite grew the leaf to 358 body words, past the 150–300 target (still inside the 400 split threshold), and the growth is prose about the GPT transport rather than acceptance. |
| Ownership and reuse | 18 | Correct owner and repo. Every reuse claim I re-read holds, and the footprint is now a thirteen-path list that is complete for the described work and no longer the widest lock on the board. −1: the HTTP client the brain and mouth calls need is still unnamed after three rounds, although `Cargo.toml`/`Cargo.lock` are in the footprint and `[lints.rust] warnings = "deny"` makes a new module's warnings fatal. −1: `granted_exec` (`sandbox/mod.rs:151-176`) resolves a multi-component grant against the cartridge root and returns `None` when the file is absent, so `grant.exec: ["tools/stt/sttd"]` grants nothing until `build-stt` has run; that ordering, and the re-trust a manifest edit forces, are still unstated. |
| Dependencies and implementable slices | 16 | Six ordered steps, each small and each real; the `CARGO_TARGET_DIR` pin is a step now, and the surviving `live.ctg` and `cartridge.ctg` anchors are all correct at `HEAD` (checked individually). −2: the landing-precondition paragraph's line citations are wrong — see N2. −1: the pin cannot be written as the step implies; `Command` is `{argv, cwd, description}` with `deny_unknown_fields` (`cartridge.ctg/src/loader/document.rs:53-58`), so it has to ride in `argv` (`["env", "CARGO_TARGET_DIR=…", "cargo", "test"]`), and only `commands.test` is pinned while `build` and `check` still write `target/`. −1: no step names the HTTP dependency, and no step carries `grant.exec`. |
| Observable acceptance and baseline evidence | 16 | The strongest part of the revision. Four of the five `prd.md` boxes map onto a spec box and a check; the SIGUSR1 observation moved to a channel the test can read; the asserted test counts are exact at `HEAD`; the proof needs no host, no dylib, no model and no network. −2: box 1's `grant.exec` half has no discriminating check — `grep -q 'sttd' cartridge.json` is satisfied by the `build-stt` recipe the same box requires, so the box passes with the grant absent and the sidecar unspawnable (**B13**). −1: the documentation proof is still one-word greps of two of the three documents box 5 names; `.cartridge/docs/README.md` is in both footprints, in box 5 and in box 9, and is never checked. −1: the URL ban still covers only `src/local.rs`, while box 2's subject is "the transport" and `src/transport.rs` is unguarded. |
| Failure, recovery and compatibility | 15 | `grant.exec` is in scope, the target directory is pinned off the live `target/`, the footprint narrowed away from the foreign dirty paths it did not need, and the precondition's conclusion is right. −2: still no error or recovery story; `error` and `session.usage.updated` appear in no box, step or event list, which is B10's unrepaired half. −1: the precondition still lives only in the spec after three rounds of asking for it on `prd.md`. −1: the `provider` default (`"gpt"`) is still only in the spec, so the compatibility promise for every already-configured install is in the wrong document — `prd.md` says only that the setting is `"gpt"` or `"local"`. −1: the scratch location for the stub script and the SIGUSR1 file is unstated, and round 2's own recommendation named `$TMPDIR` precisely to keep it outside the footprint. |
| Reviewer total | **83** / 100 | FAIL (threshold 90). One blocking finding. |

### Findings and concrete revisions

Blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| **B13** | `prd.md` box 1 and `spec01.md` box 1 require `grant.exec` to name the speech sidecar, and no check in the spec can fail when it does not. | Verify block 1's only related line is `grep -q 'sttd' cartridge.json`. The same box requires a `commands.build-stt` recipe, whose `argv` necessarily contains `tools/stt/sttd.swift` and `-o tools/stt/sttd`, so the grep matches with `grant.exec` still `["tmux"]` (its value at `HEAD`). The consequence is round-1 B7 unchanged: `cartridge.ctg/src/sandbox/mod.rs:239-265` emits `(allow process-exec <path>)` per granted program, so with the grant absent the local provider cannot spawn its sidecar at all. No step carries `grant.exec` either, so nothing else in the plan would catch it. | Make the check discriminate: grep the grant, not the string — e.g. `python3 -c` / `bun -e` reading `cartridge.json` and asserting `grant.exec` contains the sidecar path, or a `grep -A` window anchored on `"exec"`. Add `grant.exec` to a step beside the `build-stt` recipe, and say there that editing the manifest untrusts the cartridge until the host re-trusts it. |

Non-blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| N1 | The `CARGO_TARGET_DIR` step cannot be written as an environment key, and warms only one of three recipes. | `cartridge.ctg/src/loader/document.rs:53-58`: `Command` is `{argv, cwd, description}` under `#[serde(deny_unknown_fields)]` — there is no `env`. `live.ctg/cartridge.json`'s `build` (`cargo build --release`) and `check` (`cargo clippy --all-targets`) still write `target/`. | Say the pin rides in `argv` (`["env", "CARGO_TARGET_DIR=…", "cargo", "test"]`), and decide whether `check` should be pinned too. |
| N2 | The landing-precondition paragraph cites three `lifecycle.ts` lines; two are wrong. | `:145` is correct — `git status --porcelain=v1 -z --untracked-files=all -- <scope>` in `tree`, which is the lane. The fast-forward is `git(code, ['merge', '--ff-only', candidate])` at **`:166`**, not `:168` (`:168` is `contractsUnchanged()`). The integrated-footprint abort — `throw Error('source footprint changed during integrated verification')` — is at **`:174`**, not `:176` (`:176` builds `specDigests`). The prose names the right two mechanisms; only the numbers are wrong. Round 2's N1 supplied these numbers and the revision copied them. | Re-anchor to `:145`, `:166`, `:174`. Also note the `:174` check is "the footprint in `repo` differs from the collected commit", which the foreign dirty edits trip on their own, not only a pass-2 write. |
| N3 | The URL ban still covers only `src/local.rs` (round-1 N10, round-2 N4 — three rounds). | `if grep -qn 'https\?://' src/local.rs` while `src/transport.rs` and `src/service.rs` are unguarded, and `prd.md` box 2 is about "the transport". | Extend both negated greps to `src/transport.rs`. |
| N4 | The stub script's and the SIGUSR1 file's scratch location is unstated. | Spec box 5 says "a file the test names in its environment"; round 2's recommendation said `$TMPDIR`, outside the footprint. A Rust test writing either into one of the thirteen footprint paths would trip `:174` in pass 2. | Name `std::env::temp_dir()` (or the pinned `CARGO_TARGET_DIR`) in step 5. |
| N5 | Verify block 1's comment claims a check it does not make (round-2 N9). | "The service no longer dials a transport, or fetches a credential, by default" — only `socket::connect` is grepped, and box 2 deliberately keeps `socket::credential` in `src/service.rs`. | Drop the credential clause from the comment. |
| N6 | The documentation greps are one-word and skip a named document (round-1 N9, round-2 N6 — three rounds). | `grep -q 'provider' README.md` and `grep -q 'provider' .cartridge/help.md` for a box demanding two providers, four settings and the stdin/stdout/SIGUSR1 contract; `.cartridge/docs/README.md` is in box 5, box 9 and both footprints and is never checked. | Grep the four setting names and `SIGUSR1`, and add the third document. |
| N7 | The HTTP client is still unnamed (round-1 N11, round-2 N3 — three rounds). | No `reqwest`/`hyper`/`ureq` in `Cargo.lock`; `Cargo.toml`/`Cargo.lock` are in the footprint; `[lints.rust] warnings = "deny"`. Loopback needs no TLS, so hand-rolling on `tokio` is viable. | Name it in step 2. |
| N8 | `error` and `session.usage.updated` are in no box, step or event list (B10's unrepaired half). | `Service::event` dispatches both at `HEAD:445` and `HEAD:460`; the local pipeline has three processes that can fail and no named failure event. | Add one sentence to the Outcome and one acceptance box: a dead sidecar or a refused endpoint emits `error`. |
| N9 | The precondition and the `provider` default live in the spec, not in `prd.md` (round-1 B8, round-2 N2). | `prd.md` names neither. The board reads `prd.md`. | Mirror both into the Outcome, in place. |
| N10 | `sttd.swift` must carry `@main` for `-parse-as-library` (round-2 N10). | Otherwise Verify block 3 fails at link on an undefined `_main`. | State it in step 4. |
| N11 | `grant.exec` resolution is ordered against the build (round-2 N8). | `sandbox/mod.rs:151-176`: a multi-component grant resolves against the cartridge root and yields `None` when the file is absent. | Say the sidecar is built before the host loads the local provider. |
| N12 | The leaf grew to 358 body words, past the 150–300 target. | `awk` over the body: 358 words. Round 1 measured ~250. | Trim the Outcome's recital of the GPT transport's behaviour; the spec already carries it. |

Disposition: **revise**. This is a real revision, not a re-presentation: all four
round-2 blockers are closed, the footprint is now a complete and narrow file
list, the deferral to the parent is honest, and every code claim I re-checked at
`HEAD` — the three test-module counts, the endpoint constant, the missing
`session.started` arm, the sandbox exec block, the SDK's `finalize(through:)` —
is true. One bounded revision should (a) give `grant.exec` a check that can
fail and a step that creates it, (b) fix the three `lifecycle.ts` anchors, (c)
extend the URL ban to `src/transport.rs` and the documentation greps to the
third document and the setting names, and (d) mirror the precondition and the
`provider` default into `prd.md`. No split is warranted; the leaf is one outcome.

Validation: read-only. `cwd` = `/Users/feb/dev/cartridge` unless noted.
`cat` of `prd.md`, `specs/spec01.md`, `review.md`, the parent PRD,
`prd.ctg/.cartridge/workflows/review-plan.md`,
`prd.ctg/.cartridge/templates/review.md`,
`prd.ctg/.cartridge/templates/spec.md`, `justfile`, `.cartridge/justfile` — exit 0.
`shasum -a 256` over the plan, spec and parent; the plan digest differs from
rounds 1 and 2, the spec digest from round 2, the parent's is unchanged.
`cwd` = `live.ctg`: `git status --porcelain`, `git log --oneline -1`,
`git show HEAD:src/{socket,service,audio,lib}.rs`, `git show HEAD:cartridge.json`,
`git show HEAD:Cargo.toml`, `git show HEAD:init.lua`, `cat build.rs .gitignore`,
`git grep -n 'cfg(test)' HEAD -- src/`, per-file `grep -c '#\[test\]\|#\[tokio::test\]'`
= 3/3/5, `ls -R .cartridge` — exit 0.
`cwd` = `prd.ctg`: `awk` over `src/lifecycle.ts` lines 144-146/167-169/175-177,
`grep -n "merge', '--ff-only\|source footprint changed during integrated\|function cleanIndex"`
(`:166`, `:174`, `:103`), `sed -n '1,20p' src/planner.ts`,
`grep -n 'async function verify' -A 30 src/lifecycle.ts`, `git log --oneline -1`,
`git status --porcelain` — exit 0.
`cwd` = `cartridge.ctg`: `sed -n '45,80p' src/loader/document.rs`
(`Command` has no `env`), `sed -n '236,268p' src/sandbox/mod.rs` — exit 0.
Repository survey: `crate-type`/`mlua`/`cfg(test)` across all fifteen Rust
cartridges; `grep -rho "cargo [a-z-]*" … --include=collection.md` over the boards.
Environment probes: `sw_vers` = macOS 26.2 on `arm64`; `xcrun --show-sdk-path`;
`ls` and `grep` of `Speech.framework/Modules/Speech.swiftmodule/` — `arm64e` and
`x86_64` interfaces, `func finalize(through: CoreMedia.CMTime?)` present;
`SwiftUI.swiftmodule` carries the same two architectures.
No cargo, no swiftc, no daemon interaction, no write outside this PRD directory.
Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context),
session `4c2735a1-d1de-4e8d-aa99-d593f257106d`, fresh for round 3 with no
authorship of rounds 1 and 2 or of the reviewed revision.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (83/100, below the 90 threshold, one blocking finding).
Unresolved blocking findings: B13. Round-2 B9, B10 and B12 are resolved; B11 is
resolved except for the `grant.exec` box, which B13 carries. Round-1 B2 and B8
remain partially addressed and are carried as N1, N2 and N9.
Rounds used / remaining: 3 / 2.
Next action: one bounded revision addressing B13 and, where cheap, N1–N12 —
all of it is small and none of it is architectural — then re-review within the
remaining allowance. Implementation may proceed in a lane; collection still
cannot complete until the foreign uncommitted work in `live.ctg` lands.

## Round 4 — 2026-09-17

Presented revision: `prd.ctg` at `148302f6` (the plan, spec and this review are
untracked working-tree files under
`.cartridge/boards/live/prds/the-voice-runs-on-this-machine-with-no-network/`);
`live.ctg` at `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`, unchanged since round 3
and still dirty from another session on `.cartridge/docs/README.md`,
`.cartridge/help.md`, `cartridge.json`, `init.lua`, `src/service.rs`,
`src/store.rs`, plus an untracked `.DS_Store`. Both documents changed again this
round.

| Input | Content digest |
| --- | --- |
| Plan | `…/live-speaks-and-listens-through-local-sidecars/prd.md` — `b72bfed0839450c330948f6fbeb8427e1c57add06b55ef76cc4da25724b9c8a1` (was `9d01da3…` in round 3) |
| Specs | `…/specs/spec01.md` — `95b6f646da3c35b05451b4715e3f812d39241831896e79e350a567431eb11043` (was `20f404f…`) |
| Parent | `…/the-voice-runs-on-this-machine-with-no-network/prd.md` — `f82ba1f695bf682b51fd8e914ab9b509e16ff1faf4425eea72bbabc9a5b06c79` (unchanged since round 1) |
| Material contracts/dependencies | `live.ctg` at `HEAD`: `src/service.rs` `1c0fd641492f24ad9b76e327607fccbadf92d9e165b16238bef809dc7920735e`, `src/socket.rs` `4bd9f0e029b34401c4637cead4d88e06c806f05dfd7c532465afa84f4bd5cb1f`, `src/audio.rs` `976cf78d40bf39cd9bebc5d2600311e93263fbf6fd5f099d64820abefbddcd9d`, `cartridge.json` `f4454e6ba24c9caab14b13ae6195dce504c516ef752e6edf6767b9c37e08e08f`, `Cargo.toml` `4123da8f59a3b8ee38d16ac9500dadcb68ed0b91e021b8639fea6137e3919d8f`; `prd.ctg/src/lifecycle.ts`, `prd.ctg/src/process.ts`, `prd.ctg/.cartridge/templates/spec.md`, `prd.ctg/cartridge.json`; `cartridge.ctg/src/sandbox/mod.rs`, `cartridge.ctg/src/loader/document.rs`, `cartridge.ctg/src/cli/manual.rs`, `cartridge.ctg/src/host/process.rs`, `cartridge.ctg/src/host/plan.rs`; `.cartridge/justfile`, `.cartridge/memos/routine/cartridge-development.md` |

### Carried findings, checked against the files

| # | State | Evidence read this round |
| --- | --- | --- |
| **B13** `grant.exec` box with no discriminating check | **resolved** | Verify block 1 now parses the manifest with `bun -e` instead of grepping. I extracted lines 131–147 of `spec01.md` verbatim and ran them under `sh -eu -c` against five manifest fixtures built from `git show HEAD:cartridge.json`: with `grant.exec` left at its `HEAD` value `["tmux"]` it prints `grant.exec does not name the speech sidecar: ["tmux"]` and exits **1**, both with and without the four settings present; with a missing `brain` setting it exits 1; with `tts.default` deleted it exits 1; with `provider.default` set to `"local"` it prints `provider must default to gpt` and exits 1; only the fully correct manifest exits **0**. The check discriminates on all four requirements the box states. Step 0 now also carries `grant.exec` ("`cartridge.json`: the four settings, `grant.exec` extended with the sidecar's path, and the build and test recipes"), which round 3 asked for. |
| `bun -e` safety in a collection block | **confirmed** | `bun` is at `/opt/homebrew/bin/bun` (1.3.14); `PATH` reaches the block because `runProcess` spawns with `{ ...process.env }` (`prd.ctg/src/process.ts:17`) and `PATH`, `HOME` and `TMPDIR` are all in the host's `PASSTHROUGH` allowlist (`cartridge.ctg/src/host/process.rs:22-35`); `bun` is one of prd.ctg's three `grant.exec` entries. The precedent is empirical, not inferred: `…/boards/router/prds/improve-router-programme/specs/spec01.md:52` opens a `bun -e '` block, its current digest `3f38e522…` is exactly the `spec-digests` value recorded in that PRD's `collection.md`, and the receipt records `exit 0`. The single-quoted literal survives `sh -eu -c`: the JavaScript contains double quotes and no single quote, which I confirmed by running the extracted block, not by reading it. |
| **B8** landing precondition | **resolved** | All three `lifecycle.ts` citations are now exact. `:145` is `Bun.spawnSync(['git', '-C', tree, 'status', '--porcelain=v1', '-z', '--untracked-files=all', '--', ...scope])` — the lane. `:166` is `git(code, ['merge', '--ff-only', candidate]);`. `:174` is the `throw Error('source footprint changed during integrated verification')`. The precondition is also mirrored onto `prd.md` as a `## Landing` section, which rounds 1, 2 and 3 each asked for. |
| **B2** pinned `CARGO_TARGET_DIR` | **not resolved — regressed to blocking, see B15** | The *form* is right: `Command` is `{argv: Vec<String>, cwd: String, description: Option<String>}` under `deny_unknown_fields` (`cartridge.ctg/src/loader/document.rs:53-58`, confirmed by line), so `["env", "CARGO_TARGET_DIR=…", "cargo", "test"]` is a structurally valid `argv` — though `cwd` is not `Option`, so the step's example must also carry `"cwd": "."`. The *mechanism* is fiction. See **B15**. |

### Claims checked directly

- **`src/socket.rs:14`** is `const URL: &str = "wss://api.openai.com/v1/live/sessions";` at `HEAD`; `src/socket.rs:121` is `Some("session.started") => {`.
- **`Service::event` arms at `HEAD`**: `session.output_audio.delta` (405), the two transcript deltas (416), `session.delegation.created` (436), `session.usage.updated` (445), `session.closed` (452), `error` (460). No `session.started` arm. `socket::credential` at 228 and `socket::connect` at 233.
- **Test-module counts** `3 / 3 / 5` for `socket.rs`, `audio.rs`, `service.rs` at `HEAD` — spec box 3's "three, three and five" is still exact.
- **`cartridge.ctg/src/sandbox/mod.rs:239-265`** is the exec-grant block, emitting `(allow process-exec (literal …) (subpath …))` per granted program.
- **The footprints are the same thirteen paths** in `prd.md` and `spec01.md` (compared as sets). `live.ctg/README.md` does not exist at `HEAD`, so block 1's `grep -q 'provider' README.md` depends on step 6 creating it; `Cargo.lock` and `.cartridge/docs/README.md` are tracked; `.gitignore` is the single line `target`.
- **BRE `\?` works here.** `/usr/bin/grep` is "BSD grep, GNU compatible 2.6.0-FreeBSD" and matches `https\?://`; the negated guards are not inert.
- **The 120 s block limit and `sh -eu -c` are real**: `prd.ctg/src/lifecycle.ts:45` is `runProcess(['sh', '-eu', '-c', block.command], { cwd, signal, timeout: 120_000, cap: 65536 })`.

### New findings this round

- **Nothing in this composition executes a manifest command.** The only consumer of `doc.commands` in the whole repository is `cartridge.ctg/src/cli/manual.rs:538-550`, which *prints* them under `commands:  (run from <dir>)`. `just test live` does not reach `commands.test`: `.cartridge/justfile:54` → `_fan test` → `_one test` (`:133`) → `memo-run .cartridge/memos/routine/cartridge-development.md test live` → its `_cargo` recipe, which runs `cargo test --manifest-path "$repos/live.ctg/Cargo.toml" -p live --all-targets` with no `CARGO_TARGET_DIR` at all. Round 3's partial resolution of B2 rested on the opposite claim and was wrong. Recorded as **B15**; it also means the planned `commands.build-stt` recipe builds the sidecar on no automated path, which is N11's unrepaired half.
- **Three acceptance boxes have no check that can fail.** Verify block 1's only statement about `src/local.rs` is `test -f src/local.rs`; Verify block 2 is `cargo test --lib`. An implementation that ships `src/local.rs` with zero `#[cfg(test)]` tests passes all three blocks, and spec boxes 4 (the four events in order), 5 (the brain body and the SIGUSR1 file) and 6 (the delegation) are then unproven. These three boxes *are* the contract this PRD says it adds. Recorded as **B14**.
- **Verify block 1 can fail a correct implementation.** `if grep -qn 'https\?://' src/local.rs; then exit 1; fi` bans URL literals from the same file step 5 puts the tests in, and the spec's own prose says those tests bind `tokio` listeners on `127.0.0.1:0` and hand the addresses to the transport. If `brain` and `tts` are configured as OpenAI-shaped base URLs — which is what boxes 1 and 7 and the "`chat/completions` endpoint" prose describe — the `#[cfg(test)]` module must write `http://127.0.0.1:{port}` and the block exits 1 in the lane pass. The only design that escapes it is a hand-rolled `TcpStream` client taking `host:port`, and step 2 still does not name the HTTP dependency (N7, now its fourth round), so the block's outcome is undetermined. Recorded as **B16**.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One outcome, one accountable cartridge, a real parent carrying the measured budgets, an honest deferral, and two documents that agree on every fact I re-checked. −1: the local path's failure behaviour is still in scope nowhere — three processes that can die, and no named event, box or step, although `Service::event` has an `error` arm at `HEAD:460` (N8, fourth round). −2: the leaf is now **443 body words**, past the 400 words at which the workflow says to split, and 369 of them before the new `## Landing` section; round 3 measured 358 and round 1 ~250. The growth is prose, not acceptance. |
| Ownership and reuse | 16 | Correct owner and repo; the thirteen-path footprint is identical in both documents, complete for the described work, and narrower than the foreign dirty tree. −1: the HTTP client is unnamed for a fourth round and is now load-bearing, because it decides whether Verify block 1 passes (B16). −1: `grant.exec` resolution is still ordered against a build nothing runs — `granted_exec` returns `None` while `tools/stt/sttd` is absent (`sandbox/mod.rs:151-176`), and no automated path builds it (N11). −2: the plan reuses `commands.test` and `commands.build-stt` as if the composition executed them; it does not (B15). |
| Dependencies and implementable slices | 13 | Seven ordered steps, each small and real; the three `lifecycle.ts` anchors are now exact; the `argv` form of the pin is structurally valid. −3: **B15** — the named producer of a warm `CARGO_TARGET_DIR` does not exist, and `live.ctg`'s `Cargo.lock` carries 168 packages including `rusqlite` with `bundled` (compiles SQLite), `mlua` with `lua54`, `rustls`/`ring` and `cpal`, so a cold `cargo test --lib` cannot finish inside the 120 s block limit. Verify block 2's pass now rests entirely on a sentence in an HTML comment asking the implementer to build into that directory by hand. −2: **B16** — step 5 and Verify block 1 contradict each other, and step 2 still names no HTTP dependency to settle it. −1: N13 — the target directory is `$HOME/.cache/…`, outside prd.ctg's `grant.write`. −1: N15 — box 2's constructor takes "the session configuration and an event callback", with no credential, while the same box keeps `socket::credential` in `src/service.rs`; one of the two has to give. |
| Observable acceptance and baseline evidence | 13 | B13 is genuinely and verifiably closed — I ran the block, not just read it, against five fixtures. The spec's `HEAD` anchors are all exact. The proof still needs no host, dylib, model or network. −4: **B14** — boxes 4, 5 and 6, the whole observable contract, pass with no test written; `cargo test --lib` cannot tell an implemented local transport from an untested one, and `test -f src/local.rs` is the only other check on that file. −1: the documentation proof is still two one-word greps (`grep -q 'provider'`) of two of the three documents box 9 names; `.cartridge/docs/README.md` is in box 9 and in both footprints and is never checked (N6, fourth round). −1: the URL ban still omits `src/transport.rs` while box 7's subject is the transport (N3, fourth round). −1: box 3's "three, three and five tests … with their assertions unchanged" has no check; `cargo test --lib` passes with the tests deleted. |
| Failure, recovery and compatibility | 14 | The precondition is now on `prd.md` with three correct citations, `grant.exec` is in a step, the footprint is narrow and the target directory is off the live `target/`. −2: still no error or recovery story; `error` and `session.usage.updated` appear in no box, step or event list (N8). −2: the `"gpt"` default is still only in the spec — `prd.md` box 1 says "with documented defaults" and the Outcome says `"gpt"` or `"local"`, so the compatibility promise for every configured install is in the document the board does not gate on (N9, fourth round). −1: the scratch location for the stub script and the SIGUSR1 file is still unnamed in step 5, while `:174` aborts pass 2 on any footprint write (N4, third round). −1: `grep -q 'tools/stt/sttd' .gitignore` is satisfied by a `.gitignore` line reading `tools/stt/sttd.swift`, which would hide the source from collection entirely, and `@main` is still unstated so Verify block 3 can still fail at link (N10, N16). |
| Reviewer total | **73** / 100 | FAIL (threshold 90). Three blocking findings. |

### Findings and concrete revisions

Blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| **B14** | `spec01.md` boxes 4, 5 and 6 — the four events in order, the brain request body, the SIGUSR1 file, the delegation — have no check that can fail. | Verify block 1 says only `test -f src/local.rs`; Verify block 2 is `cargo test --lib`, whose status is unaffected by tests that were never written. An `src/local.rs` with the transport and no `#[cfg(test)]` module passes all three blocks and collects. This is B13's shape at a larger scale: the box passes with the requirement absent. | Add an existence check to Verify block 1 that names the tests, e.g. `test "$(grep -c '#\[tokio::test\]' src/local.rs)" -ge 3` plus `grep -q 'session.output_audio.delta' src/local.rs` and `grep -q 'SIGUSR1' src/local.rs`; or name the three tests in step 5 and assert each with `cargo test --lib -- --exact local::tests::<name>` in block 2 (each is its own command, so `sh -eu` propagates the failure). |
| **B15** | `spec01.md` step 4 justifies the `CARGO_TARGET_DIR` pin with a mechanism that does not exist, leaving Verify block 2 a cold build against a 120 s limit. | Step 4: "so the ordinary developer path — `just test live` fans to it — warms the directory collection depends on". It does not. `.cartridge/justfile:54` → `_fan test` → `_one test` (`:133`) → `memo-run … cartridge-development.md test live` → `_cargo`, which runs `cargo test --manifest-path "$repos/live.ctg/Cargo.toml" -p live --all-targets` with no `CARGO_TARGET_DIR`. The only consumer of `doc.commands` in the repository is `cartridge.ctg/src/cli/manual.rs:538-550`, which prints them; nothing executes a manifest command anywhere. `live.ctg/Cargo.lock` has 168 packages including `rusqlite` `bundled`, `mlua` `lua54`, `rustls`/`ring` and `cpal`, so the cold closure does not build in 120 s. The same error makes the planned `commands.build-stt` recipe a recipe nothing runs, so `grant.exec: ["tools/stt/sttd"]` resolves to `None` until someone builds the sidecar by hand. | Drop the false claim. Either warm the directory from the repository's real developer path (`CARGO_TARGET_DIR` in `cartridge-development.md`'s `_cargo`, which is outside this footprint and this owner, so probably not), or make step 4 an explicit implementer instruction — "before requesting collection, run `CARGO_TARGET_DIR=… cargo test --lib` once so the closure is warm" — and say in the Verify comment that block 2 times out otherwise. Keep `commands.test`/`commands.build-stt` if they are wanted as documentation, but say that is what they are. |
| **B16** | `spec01.md` Verify block 1's `https\?://` ban over `src/local.rs` can fail a correct implementation, because step 5 puts the loopback tests in that same file. | Step 5: "`#[cfg(test)]` tests in `src/local.rs` with the stubs described above"; the prose above: "the two endpoints are `tokio` listeners the test binds on `127.0.0.1:0`". If `brain` and `tts` are base URLs — which boxes 1 and 7 and "any OpenAI-shaped `chat/completions` endpoint" describe — the test writes `format!("http://127.0.0.1:{port}")` into `src/local.rs` and the block exits 1 in the lane pass, aborting collection on correct code. The only escape is a hand-rolled `TcpStream` client over `host:port`, and step 2 still names no HTTP dependency (N7, fourth round). `Cargo.lock` carries no `reqwest`, `hyper` or `ureq`. | Name the client and the configured endpoint's string shape in step 2, then scope the ban to the code it means: check the region above `#[cfg(test)]` (e.g. `awk '/#\[cfg\(test\)\]/{exit} {print}' src/local.rs > "${TMPDIR:-/tmp}/local-$$.rs"` then grep that scratch file, which is outside the footprint), and extend the same ban to `src/transport.rs` (N3). |

Non-blocking (N1–N12 from round 3 are re-stated only where still open):

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| N3 | The URL ban still covers only `src/local.rs` (rounds 1, 2, 3). | `src/transport.rs` and `src/service.rs` unguarded; box 7's subject is "the transport". | Fold into B16's fix. |
| N4 | The stub script's and SIGUSR1 file's scratch location is still unnamed (rounds 2, 3). | Step 5 says nothing; `:174` aborts pass 2 on a footprint write. | Name `std::env::temp_dir()` in step 5. |
| N5 | Verify block 1's comment still claims a credential check it does not make (rounds 2, 3). | "The service no longer dials a transport, or fetches a credential, by default" over a block that greps only `socket::connect`. | Drop the clause. |
| N6 | Documentation proof is still one-word greps of two of three documents (rounds 1, 2, 3). | `grep -q 'provider' README.md`, `grep -q 'provider' .cartridge/help.md`; `.cartridge/docs/README.md` never checked. | Grep the four setting names and `SIGUSR1`, and add the third document. |
| N7 | The HTTP client is still unnamed (rounds 1, 2, 3) — now load-bearing via B16. | No `reqwest`/`hyper`/`ureq` in `Cargo.lock`; `[lints.rust] warnings = "deny"`. | Name it in step 2. |
| N8 | `error` and `session.usage.updated` are in no box, step or event list (rounds 2, 3). | `HEAD:445` and `HEAD:460`. | One Outcome sentence and one box: a dead sidecar or a refused endpoint emits `error`. |
| N9 | The `provider` default is still only in the spec (rounds 1, 2, 3); the precondition half is now fixed. | `prd.md` box 1 says "documented defaults" without naming `"gpt"`. | Add `(default `"gpt"`)` to `prd.md` box 1, in place. |
| N10 | `sttd.swift` must carry `@main` for `-parse-as-library` (rounds 2, 3). | Otherwise block 3 fails at link on an undefined `_main`. | State it in step 4. |
| N11 | `grant.exec` resolution is ordered against a build nothing runs (rounds 2, 3; worsened by B15). | `sandbox/mod.rs:151-176` returns `None` for an absent multi-component grant. | Say the sidecar is built before the host loads the local provider, and that editing `cartridge.json` untrusts the cartridge until the host re-trusts it. |
| N12 | The leaf is 443 body words, past the 400-word split threshold (round 3: 358). | `awk` over the body. | Trim the Outcome's recital of the GPT transport; the spec carries it. |
| **N13** | Verify block 2's `CARGO_TARGET_DIR` is `$HOME/.cache/cartridge-verify/live-local`, outside prd.ctg's declared `grant.write`. | `prd.ctg/cartridge.json` grants `write: ["$PROJECT", "$TMPDIR"]`; `cartridge.ctg/src/host/plan.rs:211-238` expands `$PROJECT`, `$TMPDIR` and `$HOME/...` (the last only when the grant is written that way), and `sandbox/mod.rs:291-301` emits `(allow file-write* …)` for those subpaths and `/dev/null` alone. Every cartridge node is spawned through `sandbox::command` (`cartridge.ctg/src/host/process.rs:112`) and descendants inherit the profile. Of the 75 collected specs in this repository that set `CARGO_TARGET_DIR`, none uses a `$HOME` path; they use `$PWD/target/<slug>-verify`, an absolute `<owner>.ctg/target/…`, or `${TMPDIR:-/tmp}/…`. | Use `${TMPDIR:-/tmp}/cartridge-verify/live-local`, which is granted, shared between both passes, and matches Verify block 3's own `${TMPDIR:-/tmp}`. Costs nothing. |
| **N14** | Box 3's "three, three and five tests … with their assertions unchanged" has no check. | `cargo test --lib` passes with those modules deleted. | Add `test "$(grep -c '#\[test\]\|#\[tokio::test\]' src/socket.rs)" -eq 3` and the two siblings to block 1. |
| **N15** | Box 2's seam constructor and its credential story disagree. | Box 2: a constructor "taking the session configuration and an event callback", and "`src/service.rs` selects by setting, with `socket::credential` reached only on the GPT branch". A constructor with no credential parameter cannot receive what `service.rs` fetched. | Say which: the credential is a constructor argument, or `socket::credential` moves behind the seam. |
| **N16** | `grep -q 'tools/stt/sttd' .gitignore` is satisfied by the wrong line. | A `.gitignore` reading `tools/stt/sttd.swift` matches the grep while hiding the source file from `git status --untracked-files=all` at `:145`, so the footprint path would never be committed. | Anchor it: `grep -qx 'tools/stt/sttd' .gitignore`. |

Disposition: **revise**. The revision is real — B13 is closed with a check I executed rather than read, the three `lifecycle.ts` anchors are exact, the precondition is on `prd.md`, and `grant.exec` is in a step. The score fell because rounds 1–3 did not test the Verify blocks against the repository's actual wiring: `commands.test` is documentation, not a hook (B15); `cargo test --lib` cannot see a test that was never written (B14); and the URL ban and the in-file tests contradict each other (B16). All three are bounded edits to `spec01.md`, and one of them (B16) resolves N3 and N7 with it. No split is warranted; the leaf is one outcome, though it should be trimmed under 400 words. One round remains, so the next revision should take every open N with the three blockers rather than leave a fifth round to spend on N6 and N9 again.

Validation: read-only outside this PRD directory. `cwd` = `/Users/feb/dev/cartridge` unless noted.
`cat` of `prd.md`, `specs/spec01.md`, `review.md`, the parent PRD,
`prd.ctg/.cartridge/workflows/review-plan.md`, `prd.ctg/.cartridge/templates/review.md`,
`prd.ctg/.cartridge/templates/prd.md`, `prd.ctg/.cartridge/templates/spec.md`,
`.cartridge/justfile`, `.cartridge/memos/routine/cartridge-development.md` — exit 0.
`shasum -a 256` over the plan, spec and parent; plan and spec digests differ from round 3, the parent's is unchanged.
`cwd` = `live.ctg`: `git log --oneline -1`, `git rev-parse HEAD`, `git status --porcelain`,
`git show HEAD:{cartridge.json,src/service.rs,src/socket.rs,src/audio.rs,Cargo.toml}`,
per-file `grep -c '#\[test\]\|#\[tokio::test\]'` = 3/3/5, `grep -c '^name = ' Cargo.lock` = 168,
`git ls-files`, `cat .gitignore`, `ls README.md` (absent) — exit 0 except the deliberate `ls`.
Executed check, in a scratch directory under the session scratchpad: extracted
`specs/spec01.md` lines 131–147 with `sed` and ran them verbatim as
`sh -eu -c "$(cat check.sh)"` in five fixture directories built from
`git show HEAD:cartridge.json` — `["tmux"]` → exit 1 (twice, with and without settings),
missing `brain` → exit 1, missing `tts.default` → exit 1, `provider.default = "local"` → exit 1,
correct manifest → exit 0. `grep`/BRE probe: `/usr/bin/grep --version`, `grep -c 'https\?://'` = 2.
No cargo, no swiftc, no daemon interaction, no host call, and no write outside
this PRD directory and the session scratchpad.
`cwd` = `prd.ctg`: `sed -n '140,180p' src/lifecycle.ts` (`:145`, `:166`, `:174` each read by line),
`grep -n runProcess src/*.ts` and `src/process.ts:9-17`, `bun -e` over `cartridge.json` for the grant,
survey of `CARGO_TARGET_DIR` across every board spec with its collection status (75 collected),
`shasum` of `boards/router/prds/improve-router-programme/specs/spec01.md` against its receipt's `spec-digests` — exit 0.
`cwd` = `cartridge.ctg`: `sed -n '45,62p' src/loader/document.rs`, `sed -n '236,268p' src/sandbox/mod.rs`,
`sed -n '280,310p' src/sandbox/mod.rs`, `sed -n '530,550p' src/cli/manual.rs`,
`sed -n '85,125p' src/host/process.rs`, `sed -n '205,245p' src/host/plan.rs`,
repository-wide grep for any other consumer of `doc.commands` — none — exit 0.
Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context),
session `4c2735a1-d1de-4e8d-aa99-d593f257106d`, fresh for round 4 with no
authorship of rounds 1–3 or of the reviewed revision.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (73/100, below the 90 threshold, three blocking findings).
Unresolved blocking findings: B14, B15, B16. Round-3 B13 is resolved; round-1 B8
is resolved. Round-1 B2 is **not** resolved and is now B15. Round-3 N3, N4, N5,
N6, N7, N8, N9 (its default half), N10, N11 and N12 are all still open.
Rounds used / remaining: 4 / 1.
Next action: one bounded revision to `spec01.md` and `prd.md` taking B14, B15,
B16 and every open N together — this is the last available round. Implementation
may proceed in a lane; collection still cannot complete until the foreign
uncommitted work in `live.ctg` lands.

## Round 5 — 2026-09-17

Presented revision: `prd.ctg` at `148302f6` (the plan, spec and this review are
untracked working-tree files under
`.cartridge/boards/live/prds/the-voice-runs-on-this-machine-with-no-network/`);
`live.ctg` at `f8082627c21e4e1107360e51bc7792cd1d8ff0d7`, unchanged since round 3
and still dirty from another session on `.cartridge/docs/README.md`,
`.cartridge/help.md`, `cartridge.json`, `init.lua`, `src/service.rs`,
`src/store.rs`, plus an untracked `.DS_Store`. **Only `specs/spec01.md` changed
this round**: `prd.md` is byte-identical to the round-4 revision, so every
round-4 finding written against `prd.md` (N9, N12) is unresolved by construction,
as is the divergence B17 records below.

| Input | Content digest |
| --- | --- |
| Plan | `…/live-speaks-and-listens-through-local-sidecars/prd.md` — `b72bfed0839450c330948f6fbeb8427e1c57add06b55ef76cc4da25724b9c8a1` (**unchanged from round 4**) |
| Specs | `…/specs/spec01.md` — `5af183a4f7852fa65eb57a560171a69fd2e303f27315c3a5f6c167f5bf6006be` (was `95b6f646…`) |
| Parent | `…/the-voice-runs-on-this-machine-with-no-network/prd.md` — `f82ba1f695bf682b51fd8e914ab9b509e16ff1faf4425eea72bbabc9a5b06c79` (unchanged since round 1) |
| Material contracts/dependencies | `live.ctg` at `HEAD`: `src/service.rs`, `src/socket.rs`, `src/audio.rs`, `cartridge.json`, `Cargo.toml`, `.gitignore`; `prd.ctg/src/lifecycle.ts`, `prd.ctg/src/process.ts`, `prd.ctg/cartridge.json`, `prd.ctg/.cartridge/templates/spec.md`; `cartridge.ctg/src/sandbox/mod.rs`, `cartridge.ctg/src/host/plan.rs`, `cartridge.ctg/src/cli/manual.rs`; `.cartridge/justfile`, `.cartridge/memos/routine/cartridge-development.md`; collection receipts under `boards/memory` and `boards/proxy` for real `cargo test` output |

### Round-4 blocking findings, checked by execution

| # | State | Evidence read or run this round |
| --- | --- | --- |
| **B14** boxes with no check that can fail | **resolved for boxes 3–6** | Verify block 2 now greps cargo's own output for six named tests. **The format is right**: this repository's own receipts carry `test ledger::ledger_tests::<name> ... ok` (e.g. `boards/memory/prds/the-exchange-ledger-lives-in-memory-s-store-…/collection.md`), which is exactly `test <module path>::<name> ... ok`, so `grep -q "local::tests::$t \.\.\. ok"` matches a passing lib test. I extracted the three blocks with the engine's own parser (`verificationBlocks`, `lifecycle.ts:34`) and ran block 2 under `sh -eu -c` against four simulated `cargo` outputs on `PATH`: six passing → exit **0**; the six absent → exit **1** (`missing or failing test: a_session_starts`); `running 0 tests` with exit 0 → exit **1**; one test `... FAILED` with cargo exit 101 → exit **1**. A test that exists but fails is caught twice (the `\|\|` on cargo's status, and the absent `... ok` line); a test that does not exist is caught by the grep. |
| **B15** the warm `CARGO_TARGET_DIR` had no producer | **resolved, and the mitigation is honest** | Both halves of step 8's claim are true. `just test live` → `.cartridge/justfile:54` `_fan test` → `_one test` (`:133`) → `memo-run .cartridge/memos/routine/cartridge-development.md test live` → `_cargo` (`cartridge-development.md:45-71`), which exports `CARGO_PROFILE_*` and **no `CARGO_TARGET_DIR`**; `grep -rn CARGO_TARGET_DIR` over `justfile`, `.cartridge/justfile`, `cartridge-development.md` and `live.ctg/cartridge.json` matches only an unrelated `verify` recipe. And `doc.commands` is consumed only by `cartridge.ctg/src/cli/manual.rs:538-550`, which prints it. The mitigation works because the lane is not fresh at collection time: `lifecycle.ts:225` creates the worktree at **claim**, and `:175` removes it only after the receipt, so the implementer's step-8 run happens in the same lane path pass 1 then re-runs in — pass 1 is a warm no-op. Pass 2 runs in `repo`, a different path, so cargo re-fingerprints the `live` package alone while the 168-package dependency closure is reused from the shared pinned directory. "Step 8 warms it, so collection recompiles one crate" is accurate. |
| **B16** the URL ban could fail correct code | **removed, not replaced** | No `http` string appears anywhere in `spec01.md` or `prd.md` any more; the false-failure risk is gone. What replaced it — box 7 — has no check at all, and `prd.md` box 2 still carries the old absolute. See **B17**. |
| **N13** `$HOME/.cache` outside `grant.write` | **resolved** | Blocks 2 and 3 now use `${TMPDIR:-/tmp}`. `prd.ctg/cartridge.json` grants `write: ["$PROJECT", "$TMPDIR"]`; `cartridge.ctg/src/host/plan.rs:227-238` expands `$TMPDIR` to `std::env::temp_dir()` and `sandbox/mod.rs:291-301` emits `(allow file-write* (subpath …))` for it. `TMPDIR` reaches the block through the host's passthrough, so the block names the granted directory. (`/tmp` is *not* granted, so the `:-/tmp` fallback would be denied — theoretical only, since `TMPDIR` is always set here.) |
| **N6** documentation greps | **resolved** | Block 1's `bun -e` now checks all three documents for `provider`, `stt`, `tts`, `brain` and `SIGUSR1`. |
| **N16** `.gitignore` grep matched the wrong line | **resolved** | `grep -qx 'tools/stt/sttd' .gitignore`. |
| **N7** the HTTP client | **resolved** after four rounds | Step 2 names `reqwest`, `default-features = false`, `rustls-tls`/`json`/`stream`, reusing the `rustls 0.23` already in `Cargo.toml`. |
| **N3, N5** | resolved | The URL ban is gone with B16; block 1's comment is now just `# Shape and manifest.` |
| **N4** scratch location | resolved in the blocks | Both scratch paths are under `${TMPDIR:-/tmp}`, outside the footprint, so `:174` cannot trip on them. Step 7 still does not say where the Rust test writes its SIGUSR1 file, but spec box 5 says "a file the test names in its environment", and the only sane home is `std::env::temp_dir()`. |
| **N9, N12, N15, N11** | **unresolved** | `prd.md` is byte-identical to round 4: still 443 body words (the workflow splits above 400) and still says "documented defaults" without naming `"gpt"`. Box 2's constructor still takes "the session configuration and an event callback" while `socket::credential` stays in `src/service.rs`. Nothing builds `tools/stt/sttd`, so `granted_exec` (`sandbox/mod.rs:151-176`) returns `None` for it — and the spec now *documents* that its own `build-stt` recipe is never executed. |

### Claims checked directly at `HEAD`

- `src/socket.rs:14` is `const URL: &str = "wss://api.openai.com/v1/live/sessions";`. Block 1's grep matches.
- Test modules: `#[cfg(test)] mod tests` at `socket.rs:190/191`, `audio.rs:243/244`, `service.rs:963/964`, with **3, 3 and 5** `#[test]`/`#[tokio::test]` — box 3's "three, three and five" is exact, and the module is literally named `tests`, so the `socket::tests::` / `audio::tests::` / `service::tests::` greps resolve.
- `Service::event` at `HEAD`: `session.output_audio.delta` (405), the two transcript deltas (416), `session.delegation.created` (436), `session.usage.updated` (445), `session.closed` (452), `error` (460), and a `_ => {}` catch-all (468) — so an unhandled `session.started` is harmlessly ignored, as both documents say. `socket::credential` at 228, `socket::connect` at 233.
- `live.ctg/README.md` does not exist at `HEAD`; `.gitignore` is the single line `target`; `grant.exec` is `["tmux"]`; `Cargo.toml` has no HTTP client.
- `cartridge.ctg/src/cli/manual.rs:538` opens the `doc.commands` block and only writes them to `out`.

### Verify blocks, executed

- **Syntax.** All three blocks pass `sh -n` (extracted with the engine's own `verificationBlocks` regex, so what I checked is what collect would run).
- **Block 1 against `HEAD`** (a `git archive HEAD` export of `live.ctg`, run as `sh -eu -c "$(cat block1.sh)"`): exit **1**, as the author reports. It fails silently at the first `test -f src/transport.rs`, before any message — correct, but the failure output in the receipt will be empty.
- **Block 1 against a synthetic correct tree** (empty `src/transport.rs`, `src/local.rs`, `tools/stt/sttd.swift`; `.gitignore` with `tools/stt/sttd`; `socket::connect` renamed out of `service.rs`; the four settings and `grant.exec` added; three documents carrying the five words): exit **0**. It does not false-fail. Reverting `grant.exec` to `["tmux"]` alone: exit **1**, `grant.exec does not name the speech sidecar: ["tmux"]`.
- **Block 2**: the four-case matrix above. Note that `grep -q 'socket::tests::'` and its two siblings only require one surviving line per module, so box 3's "three, three and five … unchanged" still has no counting check (N14, unresolved).
- **Block 3** not run (`swiftc` is out of scope for this review). Its premises were confirmed in rounds 2 and 3 (the SDK declares `finalize(through:)`, `/usr/bin/swiftc` exists) and step 6 now states `@main`, closing N10. It remains the only `swiftc` block in any board.

### New finding this round

`Service::event`'s `session.closed` arm (`HEAD:452-458`) sets `entry.closed = true`
and writes `lifecycle(… {"finalized": true})`. **It reads no reason.** The arm that
keeps a reason is `error` (`HEAD:460-467`), which stores it in `entry.error`, which
`status` reports at `HEAD:158-160` as `{"ready": !closed, "error": …}`. Spec box 7
routes a refused endpoint through `session.closed` "carrying the reason", so the
reason is discarded at the service and `live status` shows `ready: false,
error: null`. Rounds 2, 3 and 4 each asked (N8/N5) for the `error` arm to carry the
local pipeline's failures; the revision finally added a failure sentence and sent
it down the one arm that drops it. Recorded with the missing check as **B17**.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One outcome, one accountable cartridge, a real parent that carries the measured budgets and the device-level acceptance this leaf defers, and a spec whose every `HEAD` anchor I re-verified. −2: `prd.md` box 2 still reads "it carries no host or URL literal" — the absolute the spec deliberately dropped this round — so the two documents now describe different contracts for the same property and neither is checked. −1: `prd.md` is byte-identical to round 4, so the leaf is still **443 body words**, past the 400 at which the workflow says to split (round 1 measured ~250). |
| Ownership and reuse | 17 | Correct owner and repo; the thirteen-path footprint is identical in both documents and complete for the described work; `reqwest` is named at last and reuses the tree's `rustls 0.23`. −1: `grant.exec: ["tools/stt/sttd"]` still resolves to `None` until the sidecar exists, and the spec now says in its own comment that `doc.commands` are only printed — so step 1's `build-stt` recipe is documentation the plan relies on nothing to run, and no step, block or document says who builds the binary. −1: N15 unresolved — a constructor taking "the session configuration and an event callback" cannot receive the credential `src/service.rs` is required to keep fetching. −1: editing `cartridge.json` untrusts the cartridge until the host re-trusts it; unstated for a fifth round. |
| Dependencies and implementable slices | 17 | Eight ordered steps, each small and real. B15's replacement is the strongest part of the revision: the false mechanism is gone, the two negative claims are true as written, and the warm path is real because the lane worktree is created at claim (`lifecycle.ts:225`) and removed only after the receipt (`:175`). −1: the mitigation silently assumes the implementer's `TMPDIR` is the collector's; true on this machine, unstated, and the whole gate rests on it. −1: nobody has yet measured pass 2, which recompiles the `live` package cold inside a 120 s block — the estimate is sound, the number is unknown. −1: no step implements the failure path box 7 promises; step 4 stops at "emit the events". |
| Observable acceptance and baseline evidence | 15 | The best verification section of the five rounds, and I established it by running it rather than reading it: block 2 discriminates on all four cases, block 1 exits 1 at `HEAD` and 0 on a correct tree and still fails on `grant.exec` alone, the documentation check covers all three documents and five words, `.gitignore` is anchored with `-qx`, and the `test <path> ... ok` format is confirmed against this repository's own receipts. −4: **B17** — box 7 has no check that can fail. An `src/local.rs` that `unwrap()`s a refused endpoint and panics satisfies all three blocks and every other box; this is round-4 B14's shape surviving on the one box B14 did not name. −1: N14 unresolved — `grep -q 'socket::tests::'` passes with two of the three socket tests deleted while box 3 asserts a count. |
| Failure, recovery and compatibility | 15 | The landing precondition is on `prd.md` with three exact citations, the scratch and target directories are inside `prd.ctg`'s actual `grant.write`, and the pin stays off the live `target/` the host loads from. −3: the failure story is routed through `session.closed`, whose arm discards the reason, instead of `error`, whose arm keeps it and surfaces it in `status` — see the new finding above. −1: no test and no step for that path, so it is prose in an acceptance box. −1: the `"gpt"` default is still only in the spec after five rounds; `prd.md` box 1 says "documented defaults" and the board gates on `prd.md`. |
| Reviewer total | **81** / 100 | FAIL (threshold 90). One blocking finding. |

The total is below round 3's 83 and well above round 4's 73. Round 3's score was
assigned before rounds 4 and 5 tested the blocks against the repository's actual
wiring and by execution; round 4 said so explicitly. Against the stricter,
executed standard this revision is the strongest of the five.

### Findings and concrete revisions

Blocking:

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| **B17** | `spec01.md` acceptance box 7 has no check that can fail, and the behaviour it names is routed through the event arm that discards it. | The box: "Every endpoint comes from configuration … and an endpoint that will not answer closes the session with `session.closed` carrying the reason instead of panicking." No Verify block mentions it; none of the six named tests covers it; step 4 stops at "emit the events". An implementation that `unwrap()`s a refused `reqwest` response passes blocks 1, 2 and 3 and every other box. Its first half is *indirectly* forced (tests 2–6 can only drive loopback stubs through injected endpoints), but its second half is unguarded in every direction — and as specified it is also wrong: `Service::event`'s `session.closed` arm (`HEAD:452-458`) reads no reason and writes `{"finalized": true}`, while `error` (`HEAD:460-467`) stores the reason in `entry.error`, which `status` reports at `HEAD:158-160`. A dead sidecar would leave the user with `ready: false, error: null`. Rounds 2, 3 and 4 asked for the `error` arm by name (N8/N5). | Two edits, both small. (a) Name a seventh test in box 3 and add it to Verify block 2's loop — e.g. `a_refused_endpoint_closes_the_session`, driven by binding a listener and closing it, or by pointing `brain` at a port nothing listens on. (b) Rewrite box 7's second half onto the arm that carries the reason: the transport emits `error` with `error.message`, then `session.closed`. Optionally add the cheap positive guard the removed URL ban was reaching for, in block 1's `bun -e`, which already parses the manifest: assert `settings.brain.default` and `settings.tts.default` are loopback (`^http://(127\.0\.0\.1\|localhost)[:/]`). That cannot fail a correct implementation, because the defaults are manifest data, not code. |

Non-blocking (only those still open):

| # | Issue | Evidence | Recommendation |
| --- | --- | --- | --- |
| N9 | The `"gpt"` default is still only in the spec (rounds 1–4). | `prd.md` box 1 says "with documented defaults"; the board gates on `prd.md`. | Add `(default `"gpt"`)` to `prd.md` box 1, in place. |
| N11 | Nothing builds `tools/stt/sttd`, so `grant.exec` resolves to `None` (rounds 2–4, worsened by the spec now documenting `doc.commands` as inert). | `sandbox/mod.rs:151-176`; `manual.rs:538-550`; block 3 compiles to `${TMPDIR}` and deletes the result. | One sentence in step 6: the sidecar is built into `tools/stt/sttd` before the host loads the local provider, and editing `cartridge.json` untrusts the cartridge until the host re-trusts it. |
| N12 | The leaf is 443 body words, past the 400-word split threshold (rounds 3, 4). | `awk` over the body; `prd.md` unchanged since round 4. | Trim, or split — see the disposition. |
| N14 | Box 3's "three, three and five … unchanged" has no counting check (round 4). | `grep -q 'socket::tests::' "$out"` passes with one of three surviving. | `test "$(grep -c 'socket::tests::.* \.\.\. ok' "$out")" -eq 3`, and the two siblings. |
| N15 | The seam constructor and the credential story still disagree (round 4). | Box 2: a constructor taking "the session configuration and an event callback", while `socket::credential` stays in `src/service.rs`. | Say which: a constructor argument, or the credential moves behind the seam. |
| N17 | Block 1 fails silently against a tree missing the new files. | Run against a `HEAD` export it exits 1 with no output, so the collection failure names nothing. | Give the `test -f` group a message, or drop them — `grep` on a missing file already fails loudly. |
| N18 | Step 8's warm-up depends on the implementer's `TMPDIR` being the collector's. | True on this machine (per-user `/var/folders/…/T`), unstated, and the whole 120 s budget rests on it. | One clause in step 8. |
| N19 | Block 2 requires the test module to be named exactly `tests`; no acceptance box says so. | The grep is `local::tests::<name>`; a `mod test` or a nested module fails a correct implementation. | Say "a `mod tests` in `src/local.rs`" in box 3. |

Disposition: **revise — but the allowance is exhausted; this is a user decision.**
The revision is real and the three round-4 blockers are genuinely closed, two of
them by checks I executed rather than read. One acceptance box out of nine still
cannot fail, and the behaviour it names is pointed at the wrong event arm.

Validation: read-only outside this PRD directory and the session scratchpad.
`cwd` = `/Users/feb/dev/cartridge` unless noted.
`cat` of `prd.md`, `specs/spec01.md`, `review.md` (all four rounds), the parent PRD,
`prd.ctg/.cartridge/workflows/review-plan.md`, `prd.ctg/.cartridge/templates/review.md`,
`prd.ctg/.cartridge/templates/spec.md`, `.cartridge/justfile`,
`.cartridge/memos/routine/cartridge-development.md` — exit 0.
`shasum -a 256` over the plan, spec and parent: the plan digest is **identical** to
round 4's, the spec digest differs, the parent's is unchanged since round 1.
`cwd` = `live.ctg`: `git rev-parse HEAD`, `git status --porcelain`,
`git show HEAD:{src/service.rs,src/socket.rs,src/audio.rs,cartridge.json,Cargo.toml}`,
per-file `grep -c '#\[test\]\|#\[tokio::test\]'` = 3/3/5, `grep -n '#\[cfg(test)\]'`
= 190/243/963, `cat .gitignore`, `ls README.md` (absent) — exit 0 except the deliberate `ls`.
Executed, in `…/scratchpad/r5`: extracted all three Verify blocks with the engine's own
`verificationBlocks` regex via `bun -e` (3 blocks); `sh -n` on each — all OK;
`git -C live.ctg archive HEAD | tar -x` into a scratch tree and `sh -eu -c` of block 1
there — exit **1**; the same block against a synthetic correct tree — exit **0**;
with `grant.exec` reverted to `["tmux"]` — exit **1** with the expected message;
block 2 under a stub `cargo` on `PATH` for four output shapes — 0 / 1 / 1 / 1.
No real `cargo`, no `swiftc`, no daemon interaction, no host call.
`cwd` = `prd.ctg`: `sed -n '1,60p'` and `'135,235p'` of `src/lifecycle.ts`
(`:145`, `:166`, `:174`, `:175`, `:225` each read by line), `sed -n '1,30p' src/process.ts`,
`bun -e` over `cartridge.json` for the grant (`write: ["$PROJECT","$TMPDIR"]`,
`exec: ["bun","git","sh"]`), `grep -rh '\.\.\. ok$' --include=collection.md` over
`boards/memory` and `boards/proxy` for the real cargo line format — exit 0.
`cwd` = `cartridge.ctg`: `sed -n '230,275p'` and `'285,315p'` of `src/sandbox/mod.rs`,
`grep -n 'fn granted_exec' -A 30`, `'fn installation_outside' -A 25`,
`'fn granted_paths' -A 20`, `sed -n '530,552p' src/cli/manual.rs`,
`grep -n TMPDIR -B4 -A12 src/host/plan.rs` — exit 0.
Reviewer identity: independent reviewer subagent (Claude Opus 5, 1M context),
session `4c2735a1-d1de-4e8d-aa99-d593f257106d`, fresh for round 5 with no
authorship of rounds 1–4 or of any reviewed revision.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (81/100, below the 90 threshold, one blocking finding).
**Round 5 is the last the method allows: the allowance is exhausted.** Automatic
revision of this plan stops here.
Unresolved blocking findings: **B17**. Round-4 B14, B15 and B16 are resolved;
round-3 B13 and round-1 B8 stay resolved. Round-4 N13, N6, N16, N7, N3, N5, N10
and N4 are resolved. Round-4 N9, N11, N12, N14 and N15 remain open, joined by
N17, N18 and N19.
Rounds used / remaining: 5 / 0.
Next action: **stop automatic revision and put the plan to the user.** Two
decisions are needed and neither is the reviewer's to make: (1) close B17 with
the two small edits above and grant one more round, or (2) split the leaf —
the Swift sidecar, its `grant.exec`/`build-stt` manifest keys, `.gitignore` and
the unprecedented `swiftc` block into their own sibling, leaving a Rust-only leaf
that blocks 1 and 2 fully prove — and say whether the children inherit these five
used rounds or start a new allowance (the workflow makes them inherit unless the
user says otherwise). Independently of either: collection still cannot complete
until the foreign uncommitted work in `live.ctg` (`src/service.rs`,
`cartridge.json`, `.cartridge/help.md`, `.cartridge/docs/README.md`, all four in
this footprint) is committed or reverted by its owner — unchanged through all
five rounds. Note also that `prd release … question` requires a `## Questions`
section, which `prd.md` does not have (`lifecycle.ts:229`).
