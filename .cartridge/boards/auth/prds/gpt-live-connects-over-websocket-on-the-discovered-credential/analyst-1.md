# analyst-1 — @auth/gpt-live-connects-over-websocket-on-the-discovered-credential

Verdict: **SPECCED**. Draft at
`.state/loop/gpt-live-connects-over-websocket-on-the-discovered-credential/spec01.md`
with `attempt-1.patch` beside it. Footprint unchanged.

## Base

`auth.ctg` HEAD is `dd35669` ("Carry a GPT Live session over the WebSocket
transport"), working tree clean, and the superproject gitlink is
`dd3566926bb3402ed619884d02be9931429c462c` — the landed work is the tip and is
integrated. All probing was done in detached worktrees under the scratchpad
(`gptlive-ws/wt`, `gptlive-ws/iso`, `gptlive-ws/base`); nothing was written to a
live checkout, no `prd` op was run, no daemon was touched.

`dd35669` touched five files: `.cartridge/help.md`, `cartridge.json`,
`src/main.ts` (+32/−8), `src/openai.ts` (+89/−3),
`.cartridge/tests/integration/auth.test.ts` (+45/−1). **`OpenAIAuth.discover()`
is not in the diff at all** — the whole credential-discovery path is unchanged
from before the commit.

## Per-box audit

### Box 1 — websocket `create` — ticked, **supported**

- `src/openai.ts:114` accepts `transport.type === "websocket"` and `:115` skips
  the SDP guard only in that case, so the WebRTC validation is byte-for-byte the
  old one for every other request.
- `src/openai.ts:118` routes to `start()`; `:139` is the destination
  `wss://api.openai.com/v1/live/sessions`; `:151-154` sends
  `{type:"session.start", session}` on `open`; `:160-163` resolves the id from
  `session.started`; `:173` returns `{session:{id}}, transport:{type:"websocket"}`.
- The WebRTC branch (`src/openai.ts:119-133`) is untouched, and its four tests
  still pass.
- Covered by `.cartridge/tests/integration/auth.test.ts:111-140`, which asserts
  the URL, the bearer, the `session.start` payload and the result shape.

Caveat, not a reason to untick: the test drives `OpenAIAuth` directly. The
`auth.live {op:"create"}` wire handler (`src/main.ts:15-21`) is a passthrough
plus one `carriesAudio.add`, and is unexecuted by any test. spec01 covers it.

### Box 3 — discovery from the router's store — ticked, **supported**, but not by `dd35669`

Traced end to end across two cartridges:

- `router.ctg/src/service.rs:195-214` — `login` resolves the credential name
  from `catalog.providers["openai"].key`, falling back to
  `auth::env_name("openai")`, then writes `{ <name>: key }` into
  `<config_dir>/credentials.json`.
- `router.ctg/src/catalog.rs:161` — `openai` is in `API_PROVIDERS`;
  `catalog.rs:259` sets that provider's `key` to `format!("{key}_API_KEY")`, i.e.
  **`OPENAI_API_KEY`**. `auth.rs:1217` gives the same string for the fallback
  path. Either way the stored name is `OPENAI_API_KEY`.
- `router.ctg/src/settings.rs:59-62` — `Paths.credentials` is exactly the
  `config_dir` setting.
- `.cartridge/config.lua:59` sets router `config_dir = ".cartridge/credentials"`;
  `.cartridge/config.lua:63` sets auth `credentials_dir = ".cartridge/credentials"`.
  **Same directory.**
- `auth.ctg/src/openai.ts:81-89` reads `<credentials_dir>/credentials.json` and
  accepts `OPENAI_API_KEY` or `openai`, recording the file path as `source`.
  `:104-109` builds the status from paths only; no candidate value is ever put in
  `source`, `checked`, `issues` or `message`.
- Covered by `auth.test.ts:24-30` (source is the path, `JSON.stringify(status)`
  does not contain the secret) for exactly the shape and key name the router
  writes.

So the tick stands on evidence. Two honest qualifications for the record:
(a) it was already true before `dd35669` — the commit's only contribution here is
the sentence in `.cartridge/help.md`; (b) the router-writes-what-auth-reads
contract holds by inspection, not by any test, and cannot be guarded from inside
`auth.ctg`'s footprint.

### Box 4 — "a test against a local mock WebSocket server" — ticked, **not supported. Untick it.**

The added tests use `FakeSocket` (`auth.test.ts:16-23`), an in-process
`EventTarget` injected through `deps.socket`. No server is started, no port is
bound, no socket is opened. Clause by clause:

| clause | status |
| --- | --- |
| local mock WebSocket server | **absent** — an in-process object double |
| start | covered (`auth.test.ts:122-126`) |
| relay | **not covered** — `auth.test.ts:129-134` exercises `StartedSocket`'s replay; the `auth.live.event` relay is `src/main.ts:27-36`, and no test imports `src/main.ts` |
| audio append | partly — `send` on the provider socket (`:135-136`), not the `auth.live {op:"send"}` op |
| close | **not covered** — `:137` closes the raw socket; the `session.close` / `session.closed` / 15 s path (`src/main.ts:41-53`) never runs |
| no event carries the key | **not asserted** — no `auth.live.event` is ever produced in any test |
| no log line carries the key | **not asserted** — `diagnostic()` (`src/wire.ts:19-21`) writes stderr, and nothing in the suite captures it |

Four of seven clauses have no evidence. This is a tick that could not fail.

### Box 2 — unticked — **implemented, unproven**

Every clause exists in `src/main.ts`:

- server events → `auth.live.event` with `session_id`: `emit` at `:12`, wired on
  attach at `:27-36`;
- `send` forwards client events: `:55-59`;
- `close` sends `session.close` and waits, bounded 15 s: `:41-53` —
  `ws.send({type:"session.close"})`, `setTimeout(()=>ws.close(),15000)`, and a
  listener that clears the deadline on `session.closed`.

Nothing missing in behaviour; everything missing in proof. It is the same gap as
box 4, seen from the other side, so one piece of work closes both.

The obstacle is real and is why the spec exists: `src/main.ts` is a top-level
script that builds `new Wire()` on `process.stdin` at import and gives
`OpenAIAuth` no `deps`, and `start()` hardcodes `wss://api.openai.com/...`.
There is no seam today that lets the shipped handlers meet a loopback server.

## Questions section — **answered by the code, not still open**

The section asks where the existing OpenAI Platform key lives and recommends
`router login {provider:"openai", key}`. The trace under box 3 establishes that
this recommendation already works with no code change: `router login` writes
`OPENAI_API_KEY` into `.cartridge/credentials/credentials.json`, and that is the
first configured store `auth`'s `discover()` reads. The remaining premise — that
the checked stores currently hold no API key — is a statement about the machine's
present contents, i.e. a user action (store the key once), not a product decision
and not a blocker on planning or on any Acceptance box. Deliberately not probed:
per the brief, no credential store, keychain or `~/.codex/auth.json` was opened.

## Plan

spec01: export the registration in `src/main.ts` as `serve(wire, make)`, move the
`node()` harness out of `wire.test.ts` into a shared helper, and add
`.cartridge/tests/integration/live.test.ts` — a `Bun.serve` GPT Live service on
`127.0.0.1:0` that refuses any bearer but the fixture dummy, driven through the
real handlers over a `PassThrough` wire. That closes box 2 and box 4 together.
Rejected alternatives (a configurable base URL, a stdio subprocess) and the
reasoning are in the spec's "Option chosen".

**Footprint: no change needed.** All four touched paths fall under the PRD's
existing `src/**` and `.cartridge/**`.

## Safety

No real credential was read, printed, copied or spent. No request left the
machine except `bun install --frozen-lockfile` against the package registry. The
mock service refuses every bearer but the fixture dummy — proved: seeding the
fixture store with a different key made both new tests fail
("OpenAI voice session connection failed"), so a real key on this machine would
fail the test rather than be used. `.cartridge/config.lua` was read for the
settings wiring; an attempt to list `.cartridge/credentials` was refused by the
safety net (`secret.basename.credentials`) and was not retried or worked around.

## Commands

All in scratchpad worktrees of `auth.ctg` at `dd35669` unless noted.

| # | command | cwd | exit |
| --- | --- | --- | --- |
| 1 | `git log --oneline -5; git status --porcelain` | `auth.ctg` | 0 — clean, tip `dd35669` |
| 2 | `git -C /Users/feb/dev/cartridge ls-tree HEAD auth.ctg` | super | 0 — gitlink `dd35669` |
| 3 | `git show --stat dd35669`, `git show dd35669 -- <paths>` | `auth.ctg` | 0 |
| 4 | `git worktree add --detach <scratch>/wt dd35669` | `auth.ctg` | 0 |
| 5 | `bun test ./.cartridge/tests/` (baseline, unmodified) | `wt` | **0** — 13 pass / 0 fail |
| 6 | `bun run check` (baseline) | `wt` | **0** |
| 7 | `bun test` after writing `serve()` + `live.test.ts` (first draft) | `wt` | **1** — 2 fail, my test omitted `session_id` on `send` and the mock never confirmed `session.close`; both were test bugs, not code bugs |
| 8 | `bun test ./.cartridge/tests/` after fixing those | `wt` | **0** — 15 pass / 0 fail |
| 9 | `bun run check` (first attempt) | `wt` | **2** — `TS2353`, DOM `WebSocket` has no `headers`; fixed with the same cast `src/openai.ts:140` already uses |
| 10 | `bun run check` (after the cast) | `wt` | **0** |
| 11 | mutation: `close` closes outright | `wt` | **1** — 2 fail |
| 12 | mutation: relay drops `session_id` | `wt` | **1** — 1 fail |
| 13 | mutation: `send` does not forward | `wt` | **1** — 1 fail |
| 14 | restore, re-run suite | `wt` | 0 |
| 15 | `git worktree add --detach <scratch>/iso dd35669` | `auth.ctg` | 0 |
| 16 | `git apply attempt-1.patch` | `iso` | **0** |
| 17 | `bun install --frozen-lockfile` | `iso` | **0** |
| 18 | `bun run check` | `iso` | **0** |
| 19 | `bun test ./.cartridge/tests/` | `iso` | **0** — 15 pass / 0 fail |
| 20 | safety mutation: fixture store seeded with a non-dummy key | `iso` | **1** — 0 pass / 2 fail, mock refused the bearer |
| 21 | spec Verify block 1 (guards), extracted, `sh -eu -c` | `iso` | **0** |
| 22 | spec Verify block 2 (install/check/test), `sh -eu -c` | `iso` | **0** — 15 pass / 0 fail |
| 23 | spec Verify block 1 on an unpatched `dd35669` worktree | `base` | **1** |
| 24 | guard block vs. 6 trees that must fail it: missing `node.ts`; mock on `0.0.0.0`; test reading `process.env`; test reading `homedir()`; the 15 s bound changed to 0; the provider destination changed | `iso` | **1, 1, 1, 1, 1, 1**; restored tree **0** |
| 25 | `git status --porcelain` after restoring each mutation | `iso`, `wt` | 0 — only the intended patch present |

## Recommendation to the coordinator

- Keep boxes 1 and 3 ticked.
- **Untick box 4.**
- Publish spec01; it closes boxes 2 and 4. `attempt-1.patch` is the whole change
  and applies clean to `dd35669`.
