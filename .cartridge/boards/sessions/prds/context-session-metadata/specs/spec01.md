---
complexity: low
footprint: ["src/main.rs","src/context.rs","src/mailbox.rs","src/roster.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/unit/main/roster_tests.rs",".cartridge/tests/integration/context.test.ts",".cartridge/docs/context.md","Cargo.toml"]
---
# Read one authorized session's bounded context metadata

Measured native baseline191e2b6: context_metadata is unsupported, roster exposes the private session name and free-form run identifier, and get exposes the private agent payload. Add a native sessions operation without changing either existing API or persistence format. Reuse mailbox::Authority authenticate/in_scope and extract the existing roster phase allowlist into a shared helper with unchanged behavior.

Accept only {op:"context_metadata",access_token,id?,expected_revision?}. Validate object/keys/types and lengths before hashing or copying: token32..4096 bytes, id1..255 ASCII alphanumeric/hyphen, optional expected_revision lowercase64hex. No arbitrary actor/scope/root/path/field selectors. The host supplies the existing credential binding; a model cannot acquire scope by naming a session. Authenticate even if id is absent, then default id to the bound actor. No legacy unauthenticated fallback. Invalid request and authentication errors are static, with no input echo.

Take one state read guard and perform only bounded direct BTreeMap lookups. The authenticated actor must still exist and belong to the credential scope. Select exactly one existing in-scope session; absent actor, missing/out-of-scope target all return the same unavailable envelope with no echoed id. Existing loaded state is an observation, not evidence the agent process is alive. Terminal lifecycle phases remain readable observations; an inactive/unloaded provider is reported by its caller rather than started here.

Return schema sessions.context.v1, status available, observed_at (existing seconds clock), revision_kind observed_metadata, revision (SHA256 of the serialized minimal session object), liveness unverified, and session:{id,parent,session_revision,phase,created,updated}. Parent is null unless the referenced parent exists, has a valid bounded id and is in the same authenticated scope. Validate selected id too for malformed persisted snapshots. Phase is the existing enum/not_started/unknown projection; never copy run, step or other arbitrary agent strings. All serialized results <=2048 bytes, including escaping/envelope. Missing metadata is not invented. No names, cwd, files, transcript, buffer text, mailbox bodies/counters/cursors, channel rows, agent objects, prompts, credentials or diagnostics.

Digest excludes observed_at and binds the exact selected session object including authorized parent projection; repeated unchanged reads have the same revision. A supplied expected_revision mismatch returns status changed, with no stale/current session payload. Strict missing/out-of-scope and changed envelopes contain schema/status only. Revision is observed metadata, not a store commit, process generation or authorization token. Actual session_revision changes also change the digest; loss of a visible parent changes it even without a child mutation. Return changed=None through native dispatch: no snapshot writes, directory IO, cursor advancement, events, new providers, model activity or retry. Disposal and native call scheduling retain existing SDK behavior.

## Acceptance proof

- [x] Actual credential-scoped native fixture reads self and authorized child, suppresses foreign parent/target, rejects forged scope and excludes seeded names/transcript/agent/mailbox/file markers with an exact DTO key assertion.
- [x] Phase/session updates and parent deletion change the digest; unchanged reads and native restart preserve it; expected_revision refuses stale evidence. Unknown phase is unknown and running is never process-liveness proof.
- [x] Missing/inactive actor and unknown/foreign session return identical bounded absence; malformed fields/limits/credentials fail statically. Reads emit nothing, alter no file bytes/metadata or cursor and do not parse a malformed mailbox/channel body.
- [x] Full existing Sessions test/check and native mailbox/roster/changes/retention contracts remain passing; new actual native fixture runs under the normal unit gate.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test sessions
just check sessions
```
