---
complexity: medium
footprint:
- src/main.rs
- src/marks.rs
- src/tool.rs
- src/identity.rs
- .cartridge/tests/unit/identity/tests.rs
- .cartridge/tests/integration/process.rs
- .cartridge/docs/shell-identity.md
---

# Report configured shell, observed dialect and cwd on existing readbacks

Baseline cacd7e13 runs real Nu, Zsh, Bash and unsupported /bin/sh through the native
SDK in four disposable processes. Supported shells already report cwd/phase but
all tool/raw readbacks omit explicit executable, dialect and integration. The
separate environment scan contains only the configured executable and boot cwd;
its cwd remains stale after cd. Unsupported sh still accepts literal input and
renders the output, with empty cwd/unknown phase. Preserve these working paths,
including the reviewed user-control and explicit restart behavior at cacd7e13.

Add one pure identity projection in identity.rs. Each Shell retains its configured
executable, configured adapter enum and initial cwd at spawn; each replacement
Shell captures its own initial cwd. This is the program requested at spawn, not a
claim about the current foreground process, PATH resolution, binary hash or OS
identity. Keep the existing executable selection/config precedence and bootstrap
arguments. Recognized configured basenames are nu, zsh and bash; all others remain
unknown. Never infer an observed dialect from the basename or welcome text.

The existing bootstrap for each supported shell emits one bounded dedicated OSC
777;cartridge-shell;<nu|zsh|bash> marker when its hook setup completes. Existing
marks parsing consumes this allowlisted enum (no arbitrary strings retained), and
records whether an actual prompt A/B mark has been seen. Split input and unknown
marker values remain bounded/no-op. Do not change existing command records,
completion/wait behavior, OSC133/633 interpretation or literal-input dispatch.
Terminal output can be forged or emitted by a foreground/subshell process: this
is explicitly reported observation, never authority or authenticated executable
identity. A configured wrapper named bash that emits no marker remains pending;
an unsupported wrapper remains unknown even if it emits ordinary command marks.

The additive identity object is schema pty.shell.v1 with exactly:
configured_executable, configured_dialect, observed_dialect, dialect_source,
initial_cwd, cwd, cwd_source, phase, integration and truncated. Dialects are
nu/zsh/bash/unknown. dialect_source is terminal_marker or unknown. integration is
observed only for a recognized adapter with a matching dialect marker and an
observed prompt; pending for a recognized adapter before that evidence; unknown
for unsupported adapters or a contradictory observed dialect. An observed
integration is historical evidence, not a guarantee the next command will finish.
phase is the current existing prompt/running/unknown mark state, or exited when
this Shell's exit is known. Read phase and cwd together under the existing grid
lock; snapshot exit separately without holding the child wait lock. These are
bounded observations, not one globally atomic lifecycle transaction.

cwd is the latest OSC7 observation if it is bounded and absolute, or null when
that latest observation is invalid or absent; no previous directory is retained.
cwd_source is terminal_marker or unknown. initial_cwd is separately labelled
spawn-time information and must never masquerade as the current cwd when an
unsupported shell changes directory. Never probe a process, run pwd or source a
new command for a read. Configured executable/initial cwd/observed cwd retain at
most4096 UTF-8 bytes each and no control characters. Check before copying; a
missing value stays null, an over-limit/unrepresentable value becomes null with
truncated=true. Bound the complete serialized identity to32768 bytes. Invalid
metadata never breaks screen/input or alters the existing legacy cwd field.

Attach the same projection under additive identity to successful pty read,
commands, screen, viewport, frame and scroll readback objects. Read it even when
the emulator frame version is unchanged; identity can change independently of
screen rows. Keep every existing field and cursor/version behavior. environment
keeps its boot-scan fields and adds current identity from the existing shared
Shell holder, so explicit restart cannot return an old Shell's identity. The
legacy tool.shell content/error contract and exact command-result strings stay
unchanged. Add identity beside content/error to every successful tool call reply
(including typed error envelopes), and inside the JSON readback content used by
no-input/literal-input readbacks. Describe remains its current schema with a brief
explanation of identity observations; do not turn request metadata into scope.
No new native service, provider activation, input lease or readonly context API
is added. The separate context-terminal-metadata leaf depends on this projection.

Use existing locks without holding any across new awaits and avoid inversion:
observation captures grid and exit sequentially; it never acquires child/tool/
control locks while holding grid. Keep old shared Shell references valid for
in-flight calls. A reply from an old in-flight Shell is labelled with that Shell's
identity; no replay or automatic restart. UI replacement and reverting its code
continue to leave the single PTY and user's foreground process alive. Only the
existing explicit control start request can recreate an exited shell.

## Acceptance

- [x] Actual native Nu/Zsh/Bash fixtures, isolated from user rc/config, report configured executable separately from observed dialect, marked cwd after cd, phase and observed integration without parsing welcome text; all required shells execute in the collected proof, with missing prerequisites reported rather than counted as passes.
- [x] Unsupported /bin/sh and a named-but-unconfirmed wrapper report honest unknown/pending integration and unknown current cwd while literal split-token output and screen/input remain usable. Forged/unknown/oversized/split marks cannot alter configured identity or grant authority; bounds/truncation and exited readback are covered.
- [x] Existing raw read/screen/frame/viewport/commands and tool content/error fields remain compatible, including unchanged frame versions with fresh identity and exact command strings. A real Host fixture replaces and rolls back a disposable UI consumer while the PTY node/PID, shell variable and command history persist; explicit restart after exit uses a new Shell without affecting live-attachment behavior.
- [x] Public PTY test/check pass with all new cases in maintained process/unit gates, preserving current user takeover, restart, input serialization, emulator, command marks and real editor behavior. No existing live terminal is used or interrupted.

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

Record source and native binary hashes, actual four-shell observations, UI/PTy
identity continuity and exact gates. The command-wait and input-ownership leaves
retain their independent outcomes; this leaf changes observation only. No shell
version discovery, executable attestation, context sampling, new global event
journal, user shell replacement or lifecycle authority is claimed.
