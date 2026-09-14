---
complexity: medium
footprint:
- Cargo.toml
- src/main.rs
- src/context.rs
- .cartridge/tests/unit/context/tests.rs
- .cartridge/tests/integration/process.rs
- .cartridge/docs/context.md
---

# Observe one existing shared terminal without reading its payload

Baseline e8e6b319 includes the independently reviewed shell identity projection,
but native pty context_metadata returns unknown pty op. Existing readbacks carry
screen/command/output and path data, and there is no per-Shell generation or
minimal stable revision. Reuse that identity contract and existing control/exit
state; leave command waiting, input ownership and user-control behavior intact.
The hard prerequisite @pty/improve-pty-shell-identity must be collected before
source work. Six owner-local paths; no Runtime, UI or caller implementation.

Add native pty {op:"context_metadata",expected_revision?}. Strictly accept only
these keys; expected_revision, when supplied, is exactly64 lowercase hexadecimal
characters. Reject wrong shapes/types/extra fields with static errors and no echo.
There are no owner, start, input, path, session or output selectors. Existing host
permission to call the shared pty service is the access boundary. Return scope
shared_terminal; do not pretend request metadata establishes private session or
agent authority. No new grant, provider activation or unauthenticated/privileged
fallback is introduced.

Select the already existing Shell using a nonblocking try_lock on the current
Shell holder. The metadata branch is selected before the ordinary dispatch path
and never enters the control/start branch. Capture one Arc; in-flight readback
retains that Shell even if a later explicit restart replaces the current slot.
Each reply names that generation and is an observation, not a promise the selected
Shell remains current until delivery. Use only try_lock for the selected grid,
exit and control observations; release each before taking the next, with no
await, wait, child-process lock, spawn_blocking job or filesystem/process probe.
Busy/poisoned state returns a minimal unavailable envelope. There is no attempt
to steal a lock, change state, retry or start a replacement to answer the read.

Each successfully opened Shell has a context-only opaque generation:128 bits
from the already-used workspace getrandom0.4 API, rendered lowercase32hex. Mint
once per Shell creation/restart, never per read or UI replacement. It is neither
PID nor authorization. Entropy failure stores unavailable metadata identity but
must not fail shell startup, alter existing identity/readback or trigger retry.
Keep the existing spawn/config/bootstrap ownership unchanged. Add direct getrandom
and sha2 0.10 dependencies in the PTY manifest; coordinator owns exact shared lock
edges. Test the constructor's failure path without manipulating global entropy.

A successful reply has exactly schema:"pty.context.v1", status:"available" or
"exited", observed_at (seconds since epoch or null if unavailable),
revision_kind:"observed_metadata", revision, and terminal. terminal has exactly:
generation, scope:"shared_terminal", configured_dialect, observed_dialect,
dialect_source, integration, phase, control (agent/user), and exit_code (integer
or null). Reuse the reviewed identity projection's fixed dialect/source/integration
labels and phase; if the captured exit is known, phase/status are exited and the
actual captured code is included. These sequential observations do not claim an
atomic lifecycle/control snapshot or proof a foreground program is alive. Reuse
only the bounded identity snapshot, never commands(), screen(), viewport(),
frame(), read(), history iteration or input encoding to populate context.

Do not expose executable paths, cwd/initial cwd, command text/output, title,
transcript, screen/rows/chunks, cursor/version, tool_owner/invocation context,
environment, shell PID, prompts or diagnostics. Unknown dialect/integration stays
unknown/pending; arbitrary terminal markers remain untrusted observations. The
working identity projection may contain at most its existing32768 bytes; select
only the fixed metadata fields above into the context row. The entire encoded
context reply is capped at2048 bytes; inability to represent the bounded row
returns unavailable without affecting the terminal. No truncating a digest-bound
row or silently dropping required identity fields.

Revision is SHA256 of serde_json's serialized exact terminal object. It excludes
observed_at, screen/output/cwd changes and omitted private data. Unchanged metadata
has the same revision across reads and UI replacement. Phase/control/exit or
observed dialect/integration changes alter it; a new Shell generation changes it
even with identical configuration and metadata. expected_revision mismatch returns
only {schema:"pty.context.v1",status:"changed"}; no current/stale payload echo.
Missing generation or busy/unavailable state returns only schema/status unavailable.
An exited Shell remains observable with status exited and is never restarted by
metadata reads. A disposed/unloaded provider remains unavailable through existing
Host resolution; the caller must not activate it to obtain context.

## Acceptance

- [ ] Real native fixtures observe available metadata on a supported shell and honest unknown integration on unsupported shell; exact key allowlists exclude seeded command/output/title/cwd/owner secrets and stay within2048 bytes. Extra start/owner/input/selectors and malformed expected revisions fail without effects.
- [ ] Quiescent reads preserve revision; omitted output/title/cwd changes do not change the settled projection. Controlled phase/control/exit changes and explicit restart change it; stale expected_revision gives only changed. UI replacement preserves generation/revision and the live shell PID; restart creates a different generation while metadata reads of an exited shell never restart it.
- [ ] Metadata reads do not write input, change control, append command history, consume frame damage or move screen/scroll cursors. Pending native frame damage remains available after reads; no emitted events arise from the read. Held observation/holder locks and entropy failure return bounded unavailable without waiting, shell startup failure, retry or background work.
- [ ] Public PTY test/check pass with maintained native and unit fixtures, retaining identity, all real Nu/Zsh/Bash/sh, existing control/restart/editor/input and command behavior. All terminals are disposable; no live user shell is touched.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
command -v nu
command -v zsh
command -v bash
just test pty
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just check pty
```

Record source/native binary hashes, selected generation/revision observations,
absence/read-only proof and explicit entropy/busy behavior. Preserve the two
inherited review rounds; no credit is claimed for source implementation here.
The coordinator refreshes the prerequisite identity receipt after the additive
context module enters its imported source closure; no prior gate is removed.
