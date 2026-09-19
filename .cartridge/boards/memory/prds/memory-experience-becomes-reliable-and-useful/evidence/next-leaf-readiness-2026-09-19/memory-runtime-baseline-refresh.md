# Runtime source baseline refresh

Read-only inspection; no source edits, checkouts, tests, commits, claims, or external-owner messages. Routing evidence is reused from `/tmp/memory-stack-delivery-readiness/readiness.md`. Prompt output is `/tmp/memory-runtime-baseline-prompt.log`. Exact committed blob IDs and committed/live SHA-256 values are in `/tmp/memory-runtime-baseline-refresh-pins.json`.

## Current committed baseline

Base HEAD is `58a59366c5fc3d6d27959ff0861dc56838394868`, newer than the requested dd75e7fd reference. Root HEAD is `8c506c653475ef4bbdb9dec6a12dbc65efbeaae2` and already pins that base. Scope migration and subsequent finder/editor/command-leader changes are committed. They no longer require adopting dirty UI for this leaf. The optional-need prerequisite is also committed at 54749f4.

Recorder and its runtime hooks remain absent from HEAD. `src/trace/activity.rs`, `src/host/trace.rs`, `src/trace/activity_limit.rs`, and the activity unit tests are untracked. A new implementation worktree therefore cannot edit the claimed existing queue without first including a scoped existing-source dependency closure. Do not recreate a competing queue from committed HEAD.

## Necessary existing-source closure

1. Entire existing `src/trace/activity.rs`, `src/trace/activity_limit.rs`, and `.cartridge/tests/unit/src/trace/activity.rs`, plus the two module declarations in `src/trace/mod.rs`. The queue now depends on the new limiter; omitting it does not preserve the inspected source.
2. Entire `src/host/trace.rs`. In `src/host/mod.rs`, take only `mod trace`, the trace_queue OnceLock field and initialization, and lifecycle enqueue in publish. Preserve the two unrelated removals of asp_activity.dispatch in send_to/gather outside the selected baseline.
3. The Recorder installation line in `src/node/mod.rs`; the diagnostic Recorder additions in `src/host/process.rs`; and the trace RPC authorization/adapter branch in `src/host/socket.rs`. These are the only dirty hunks in those three paths at capture.
4. In `src/transport/cartridge.rs`, all currently inspected dirty hunks belong to existing Recorder integration: recorder field/init/methods, trace dispatch writer_request normalization, publish capture, and listener started/finished capture with recursion exclusions. These references close over committed redact/sensitive/now_ms and trust::digest_bytes helpers. No new Cargo dependency or Cargo.lock change is required for this closure: sha2, tokio, serde_json and tempfile are already committed dependencies.
5. In `src/asp/mod.rs`, only the observed-ASP trace append block is part of the sender baseline. Leave provider_timeout_ms parsing and deadline forwarding, and related ask/search/expand/tool/tests changes, with their owner. The committed ASP activity feed already exists and must remain intact.
6. Select only truthful Recorder and delivery paragraphs from `src/trace/README.md`, README.md and .cartridge/help.md. Do not import claims that the current memory provider exposes calendar compaction/raw originals. The next implementation must replace temporary string-parser claims with the reviewed negotiated contract and describe truncation honestly.

This is a proposed selection, not authorization to commit another owner's edits. The owner must preserve or approve these exact bytes/hunks, followed by independent verification before any scoped baseline commit. The root user's earlier crystallization-baseline authorization should not be silently treated as authority over newly changed runtime source.

## New dirty behavior since prior inventory

The existing owner has added activity_limit.rs. Admission, envelope construction, and dequeue now bound activity to 48 KiB with redacted truncation metadata. Direct trace append dispatch invokes writer_request, which stamps missing timestamps, redacts, and can convert oversized exchange envelopes into summarized activity envelopes. These are payload/identity-affecting semantics; freeze and review the exact source baseline rather than assuming the earlier inventory is current. Negotiation metadata must survive any envelope replacement and identities must remain stable across retry. This is a review requirement for the already requested contract, not a proposal to redesign retention.

The delivery loop now parses two error substrings (`activity exceeds 64 KiB` and `activity append requires stable ts`) and drops those records. This is not the required generic typed response contract. Expired inputs still do not match this parser; successful bodies are still discarded by node and host closures. Preserve this as prior work when adopting the baseline, then replace it through the reviewed runtime implementation. Do not claim the existing size/timestamp characterization proves the requested fix.

ASP's dirty observer now uses append(activity), so its missing-timestamp issue from the older report has changed. It still discards successful response bodies. No routing reinvestigation is needed.

## Launch fixture and unrelated changes

The untracked `.cartridge/tests/integration/launch.rs` is exclusively a fresh-project launch/bootstrap regression, not an activity delivery test. Its setup expectation depends on unrelated dirty src/cli/bootstrap.rs, args/mod/host changes and launch/passthrough behavior. Adopting it plus its Cargo.toml target would either pull unrelated features or yield an invalid baseline test. Do not take that fixture wholesale to satisfy this memory stack.

For runtime integration, either add a separate exactly named delivery integration target under the same existing runtime leaf, or add a separately selected delivery fixture using an explicitly prepared temporary composition without claiming the launch bootstrap test. This needs an exact reviewed Cargo.toml/test footprint; it does not require committing bootstrap. Preserve the owner's launch target hunk and file. A dedicated activity_delivery target avoids overlapping that untracked file and keeps compilation of unrelated bootstrap assertions out of default tests in the implementation lane.

Exclude all CLI/prompt-recall changes, justfile deletion, ASP deadline feature and its tests, UI uv.lock, broad ASP documentation rewrite, and launch bootstrap/passthrough documentation from the Recorder baseline. The documentation files require hunk selection and concurrent-edit guards.

## Claims and bounded strategy

A fresh canonical claim scan found no active runtime or root claim on the selected base paths. The old listener PRD remains failed and unclaimed. Active claims found belong to auth, live, agent, sessions, harness and the current memory status leaf; their source footprints do not own these base files. This is absence of a checked claim, not proof that existing dirty work is ownerless. The parent already coordinates active Scope and other owners; no external owner was contacted here. Recheck checked footprint conflict resolution immediately before claiming.

Recommended sequence: obtain owner reconciliation for the pinned Recorder/hook closure; preserve unrelated dirty files/hunks with hashes; independently verify a selected existing baseline using isolated external targets; commit only that baseline; pin its commit in root; then create the existing rejected-delivery implementation lane from committed HEAD after the memory contract is collected. Alternatively, if the existing source owner commits this exact closure first, consume that commit without copying dirty work. Do not spend a new PRD on this baseline and do not expand into the launch or ASP deadline features.

The later runtime leaf still needs the earlier reviewed multi-repository strategy for proxy direct sender negotiation and root config pins. Proxy's original sender is already committed and can receive its minimal rename/negotiation directly from its HEAD. No parallel baseline feature adoption is necessary there. The memory response contract must be frozen before the runtime spec names version/disposition fields.

## Pinned files

| Path | HEAD blob (absent means untracked) | Live SHA-256 |
| --- | --- | --- |
| `src/trace/activity.rs` | `absent` | `1065e300c8c8b8a996e7a6c8430f7ee3ff3eda9e846ed908d762d5181357e5e2` |
| `src/trace/activity_limit.rs` | `absent` | `7187dd157aa44bf17050e69d85b88aab620d5f19ce5f8f79c8d0b9a3f7b8ec26` |
| `src/trace/mod.rs` | `91d25c0de2268b2f743ab60c3b368361dfb53927` | `c62213ed1fbfec10ab2bd967e2f20f62401900bc7d5d2aef605f5f4c8f1d67f9` |
| `src/host/trace.rs` | `absent` | `bb7a6bccb868d04fb865ee6d90995f07ab651d4914096dff74e2c487a0da8ca3` |
| `src/host/mod.rs` | `4f534a28bc8471729018ce8c16d78615aba62875` | `7b8e7a7328969ab3d01f89e8860ae6a0d5692fc0398ec607f14d9a216da0e300` |
| `src/host/process.rs` | `7895810cb93593772aaa0528181a1f2e8b1c8c87` | `40ffe8f2168a8a1efabc2072edd8030ea21ff2a82b1d063cb2b359af991a1f13` |
| `src/host/socket.rs` | `25b17f6beb586c72cb61bb20265d8b021ac9bd9b` | `9ccf1ef76354fe1c11a7bf68d73af645679ff730c7be30a28c52f6ce7c37b23c` |
| `src/node/mod.rs` | `cefe9e406a2affccba17cc4fc3a216c46d97cb67` | `35f77ca53b09b2cb2c45def73bb8e24ad664e44e28f2954364cca528f5eac8b7` |
| `src/transport/cartridge.rs` | `eace2cb05b1cbca9fc56422fe9eb8726c6c6b703` | `d93b7ffdc8c7195f4e7e82a9af913590229bdc9fcebd48e53a2128ffb8d61663` |
| `src/asp/mod.rs` | `213408b1e17b540b98d746287d6e60a55c6a6076` | `df8013c530e7393818ffe823d7ea0d5a66d4a1497025ebe9bff5e6557c29ef47` |
| `.cartridge/tests/unit/src/trace/activity.rs` | `absent` | `bfd2c181d727fd9ef0e64087457b257e7c6fc5fb30e452f11aa39fcc591126bb` |
| `.cartridge/tests/integration/launch.rs` | `absent` | `3362635263fdf5bc757d8370477211620b423598e54289de32b7777c85afbceb` |
| `Cargo.toml` | `40fef7bc9c657e56a438ec9d8289b86eaf839ecb` | `4508a9b67ec1332782746ac225a9e9c9e86bf45c1b7bfa6a5fc8070d1aecc600` |
| `Cargo.lock` | `f01ff0511ff3021d8e81ac15132c09c6e118753a` | `896732590aaae296f2ce57ab3de945d3800e9bf36d3a62636feadfaa4343045b` |
| `src/trace/README.md` | `164fa944f028d9c4c2c985d68f1ceb866517298e` | `3b6551ad7e10ebdf9b9f90acbcaa460728ebd20f198830e107a97b496d80943b` |
| `README.md` | `1c1c0f4f61842c763dc4cdfdaf6543713feecc0e` | `d941e1996a72513a29d39f46c0de1e0fb70b94eaa0e5402bb0a6e5503ca0fafb` |
| `.cartridge/help.md` | `80e06fa5d8beea68a9fbc78e25369f6db7e28f50` | `fae8c2e0e87ee18125fb54cd03889a60f4a1e7a983cc4da157058acee96268a1` |
