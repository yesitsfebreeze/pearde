---
complexity: 3
footprint:
  - /Users/feb/dev/cartridge/mcp.ctg/cartridge.json
  - /Users/feb/dev/cartridge/mcp.ctg/.cartridge/tests/unit/tests.rs
---

# spec01 — The `mcp` event declares its own `timeout_ms`

## Scope

One manifest edit plus one persistent unit test. `mcp.ctg/cartridge.json`
declares `timeout_ms` on its `mcp` event so a slow MCP line is cut by a bound
this cartridge chose, not by the host's silent `event_timeout_ms` default
(60000 ms — `cartridge.ctg/src/host/plan.rs:322-324` at `cartridge.ctg` HEAD
`beb8213`; the PRD body's `:299-301` is the citation at the older
`63ff234`, same `.unwrap_or(crate::settings::host().event_timeout_ms)`
fallback either way). README.md and `.cartridge/help.md` in `mcp.ctg` do not
mention per-event timeouts today (checked by grep), so neither needs updating
for this change.

**Round-1 review (81/100, blocking B1):** a Verify block alone only proves the
gate is red at collect time; nothing in `mcp.ctg` kept failing afterward if the
field were later deleted, so PRD Acceptance 2's "cannot be lost silently
again" was not actually held. Revision: add a named `#[test]` that reads the
same shipped manifest the running host parses
(`crate::service::DOCUMENT`, `src/service.rs:29`,
`include_str!("../cartridge.json")`) and fails if `timeout_ms` on `events.mcp`
is absent or too small, in the existing `.cartridge/tests/unit/tests.rs`
(reused, not a new file). The Verify block now runs it by name and reads the
name back out of the runner's own output, so a test that silently vanished
from the suite is caught too.

## Baseline (mcp.ctg HEAD `5a7c54c`, cartridge.ctg HEAD `beb8213`)

`mcp.ctg/cartridge.json`'s `events.mcp` block declares `description` and
`schema` only — no `timeout_ms`. Every MCP line (`{op:"message", line,
instance}`) therefore inherits the host default of 60000 ms, and the mechanism
established by analyst-1 (`prd.ctg/.../mcp/.state/loop/.../analyst-1.md`)
still holds unchanged at current HEAD: `handle`'s `event` arm applies
`event.timeout_ms.unwrap_or(crate::settings::host().event_timeout_ms)`
(`cartridge.ctg/src/host/plan.rs:322-324`), and a caller-side timeout only
drops the caller's own future (`transport/cartridge.rs`, `Waiting::drop`,
`rpc.rs:292-304`) — it never reaches the provider. A slow MCP line fails as a
bare `mcp did not answer in time` with no diagnosis, which is the failure the
sibling `@proxy/the-proxy-answers-within-its-bound-or-reports-the-delay`
records for the `proxy` side of the identical mechanism.

## Choosing the value

`mcp.ctg`'s `invoke` (`src/service.rs`) awaits exactly one inner `tool.*`
event dispatch synchronously per `tools/call` line, insert-under-id then
remove (unchanged shape from analyst-1's and analyst-cancelled-1's reads).
That inner dispatch is itself bounded by the **provider's own** declared
`timeout_ms`, or the same 60000 ms host default when the provider declares
none. So the `mcp` event's own bound must exceed the slowest tool it may
legitimately wait on, or the outer line is cut before a genuinely slow but
legitimate tool call can finish — the same mistake this spec is fixing, one
level up.

Surveyed every `tool.*` provider reachable through `mcp.ctg`'s wildcard need
(`needs: ["tool.*"]`), by `event.timeout_ms` declared in its manifest:

| provider | event | `timeout_ms` |
|---|---|---|
| `lsp.ctg` | `tool.lsp` | **600000** (10 min, matching its own `install_timeout_ms` default/max — a language-server install is the evidenced longest single `tool.*` call in this repo today) |
| `fs.ctg` | `tool.read/write/edit/glob/grep/search/digest/draft/gitfs/ship` | none declared (60000 ms host default) |
| `pty.ctg` | `tool.shell` | none declared (60000 ms default; the shell tool itself is non-blocking — `input.timeout_ms` only bounds a readback poll, "does not kill the program" — so a long build/test run does not hold this call open the way a synchronous tool does) |
| `prd.ctg` | `tool.prd` | none declared (60000 ms default) |
| `docs.ctg`/`memory.ctg`/`memo.ctg`/`web.ctg`/`live.ctg` | `tool.docs`/`tool.memory`/`tool.memo`/`tool.web`/`tool.live*` | none declared (60000 ms default) |

600000 ms (lsp's install bound) is today's evidenced floor for a legitimate
`tool.*` call reachable from `mcp`. Two things push the chosen bound above
that bare floor rather than exactly matching it:

- Every other `tool.*` provider today defaults to the host's 60000 ms, which
  is itself under-declared for anything but a quick call (a build/test driven
  through `tool.shell`, or a multi-stage `tool.ship` gate-then-push each
  budgeted 300000 ms by `fs.ctg`'s own `ship.gate_timeout_ms`/
  `ship.push_timeout_ms` settings, commonly runs several minutes). Fixing
  those providers' own manifests is out of this footprint (a cartridge
  declares its own surface — the same rule this PRD's Evidence section
  invokes against folding the proxy side in here), but `mcp`'s bound should
  not sit so close to the one known floor that the next provider to declare a
  correct bound of its own immediately re-triggers this exact failure.
- `agent.ctg`'s own scale precedent: `approval_timeout_secs` defaults to 900 s
  (15 min) for one human-gated step, and a turn permits up to 500 model round
  trips (`max_steps`) with no per-turn cap — evidence that a single
  legitimately long-running step in this system is measured in minutes, not
  seconds, well before it is considered wedged.

**Chosen value: `1800000` ms (30 minutes).** Three times the current 600000 ms
floor, the same order of magnitude the sibling PRD used for the symmetric
`proxy` event (`proxy.ctg/cartridge.json` declares 1860000 ms, its own 1800 s
inner deadline plus a 60 s grace), and comfortably inside the host's declared
range for a per-event override (`events.<name>.timeout_ms` validates only
`> 0`; the host's own `event_timeout_ms` *setting* — the default this
overrides — validates `max: 86400000`). It is a real, finite backstop: a
genuinely wedged MCP line is still cut and reported at 30 minutes, not left to
hang forever, while comfortably covering the slowest tool call evidenced in
this repo today.

**What the larger bound costs.** The outer bound only matters when it is
shorter than an inner bound, or when lines queue behind one another. The
parent PRD's own analysis (unobserved, not this leaf's to settle) is that the
Lua listener serialises `mcp` lines against each other; if that holds, a line
queued behind one wedged provider call now waits up to 30 minutes in silence
instead of failing fast at the old 60 s default. This spec accepts that cost
because a bound this cartridge chose that occasionally makes a caller wait
longer is strictly better than a bound that fails a legitimate 10-minute `lsp`
install every time — but the trade-off is real, and recovery for a caller
stuck behind a wedged line (freeing it, or reporting the eventual late answer)
belongs to `@runtime/a-cartridge-call-can-be-cancelled` and
`@runtime/a-wedged-call-reports-its-late-answer`, not to this leaf.

## Design

Two edits, no new files.

1. **`mcp.ctg/cartridge.json`.** `events.mcp` gains `"timeout_ms": 1800000`
   alongside its existing `description` and `schema`.

   ```diff
              "instance": {
                "type": "string"
              }
            }
   -      }
   +      },
   +      "timeout_ms": 1800000
        }
   ```

   **Trust and reload after landing.** Editing `cartridge.json` changes the
   manifest's trust hash (`trust/README.md`: "every `cartridge.json`, because
   the manifest carries the grant"). The daemon drops a cartridge whose
   manifest changed without a matching trust record, and `mcp` serves every
   attached MCP client's tool surface — after this change lands, an
   implementer or the coordinator runs `cartridge trust` for `mcp.ctg` and
   reloads before exercising the new bound live. No Verify block below depends
   on a live host, so this affects manual/operational follow-up only, but
   because pass 2 of collect fast-forwards straight into the live `mcp.ctg`
   checkout, **collect for this spec from the CLI**, not through the `mcp`
   MCP surface this same edit will drop mid-collection.

2. **`mcp.ctg/.cartridge/tests/unit/tests.rs`.** One new `#[test]`, appended
   after the last existing test (`a_restored_tool_stays_with_the_instance_
   that_restored_it`), named `the_mcp_event_declares_its_own_bound`. It parses
   `crate::service::DOCUMENT` — the same `include_str!("../cartridge.json")`
   the running host reads, not a second copy — and asserts
   `events.mcp.timeout_ms` is an integer `>= 1_800_000`:

   ```rust
   #[test]
   fn the_mcp_event_declares_its_own_bound() {
       let manifest: Value =
           serde_json::from_str(crate::service::DOCUMENT).expect("cartridge.json parses");
       let declared = &manifest["events"]["mcp"]["timeout_ms"];
       assert!(
           declared.as_i64().is_some_and(|ms| ms >= 1_800_000),
           "events.mcp.timeout_ms is {declared:?}; it must be an integer >= 1800000"
       );
   }
   ```

   This is the persistent half of the guard: `cargo test` (part of `mcp.ctg`'s
   own `check`/`test` commands) fails from now on if the field is deleted,
   shrunk, or the manifest fails to parse — not only at collect time, closing
   B1.

## Acceptance

- [x] `mcp.ctg/cartridge.json` declares `events.mcp.timeout_ms` as an integer
      `>= 1800000`, so an MCP line is bounded by a value this cartridge chose
      rather than the host's 60000 ms default.
- [x] A named unit test in `mcp.ctg` (`the_mcp_event_declares_its_own_bound`)
      reads the shipped manifest and fails if `timeout_ms` on `events.mcp` is
      absent, null, too small, or the wrong type — so removing the
      declaration after landing is caught by `cargo test`, not only by a
      collect-time Verify block.

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block runs as
`sh -eu -c`, 120 s limit, empty stdin; twice — first with cwd = the lane
worktree at boards/mcp/.lanes/<slug>, then with cwd = repo itself after the
fast-forward. Paths below are relative to the repo root. The cargo block below
sets an isolated CARGO_TARGET_DIR per the engine's own convention (a warm dir
survives both passes and keeps the block inside the 120 s limit; measured
below at ~7 s cold, <1 s warm). No block writes inside the footprint.
-->

The manifest declares an `mcp` event bound at least the evidenced floor, so
the static check fails on a missing or too-small declaration and passes once
it is present.

```sh
python3 - <<'PY'
import json, sys
m = json.load(open("cartridge.json"))
ms = m["events"]["mcp"].get("timeout_ms")
if not isinstance(ms, int) or ms < 1800000:
    sys.exit(f"events.mcp.timeout_ms is {ms!r}; it must be an integer >= 1800000")
print(f"ok: events.mcp.timeout_ms={ms} >= 1800000")
PY
```

The persistent guard is a real, named test, and it actually ran (a passing
`cargo test` prints one `test <name> ... ok` line per test, so the name is
grepped rather than trusted to the summary count alone).

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-${TMPDIR:-/tmp}/mcp-bound-verify}"
mkdir -p "$CARGO_TARGET_DIR"
log="$CARGO_TARGET_DIR/tests.log"
if ! cargo test --lib the_mcp_event_declares_its_own_bound > "$log" 2>&1; then
  cat "$log"
  exit 1
fi
if ! grep -q "test tests::the_mcp_event_declares_its_own_bound ... ok" "$log"; then
  echo "missing or failed: tests::the_mcp_event_declares_its_own_bound"
  cat "$log"
  exit 1
fi
tail -n 3 "$log"
```
