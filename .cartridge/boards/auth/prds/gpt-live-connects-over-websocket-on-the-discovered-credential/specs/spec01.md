---
complexity: small
footprint:
  - src/main.ts
  - .cartridge/tests/integration/live.test.ts
  - .cartridge/tests/integration/node.ts
  - .cartridge/tests/integration/wire.test.ts
---

# spec01 — Prove the WebSocket session over the wire against a GPT Live service on loopback

The relay, `send` and the bounded `close` already exist in `src/main.ts`
(`dd35669`). Nothing exercises them: every test in this cartridge imports
`src/openai.ts` and drives `OpenAIAuth` directly, so the whole `auth.live`
handler — the one surface those three behaviours live on — is unexecuted, and
"a test against a local mock WebSocket server" is unwritten. This spec adds the
seam that lets the real handlers run in a test, and the test.

## Acceptance

- [x] A test drives this cartridge's own `auth.live` handlers over the wire protocol against a GPT Live service on loopback: `create` with `transport:{type:"websocket"}`, `attach`, `send`, `close`.
- [x] Server events of that session arrive as `auth.live.event` frames carrying `session_id`, including one the service sent before any consumer had attached.
- [x] `send` puts the client event on the session socket unchanged: the service receives the `session.input_audio.append` the consumer passed.
- [x] `close` sends `session.close` and waits — the session ends when the service answers `session.closed`, and a service that never answers leaves the session usable rather than closed outright, for a bound of 15 s.
- [x] No `auth.live.event` frame and no diagnostic line carries the credential, and the diagnostic capture the clause is asserted against is **known to be non-empty**: the test drives one real `diagnostic()` line first and asserts it is there, so the clause is true of something rather than true of nothing. The mock service refuses every bearer but the fixture's dummy, so a real key on the machine fails the test instead of being spent.

## Steps

1. `src/main.ts`: wrap the handler registration in
   `export function serve(wire: Wire, make: (config: AuthConfig) => LiveAuth = config => new OpenAIAuth(config))`,
   move `auth`, `sockets` and `carriesAudio` inside it so each call owns its
   state, and end the file with `if(import.meta.main) serve(new Wire());` at
   column 0. No behaviour change in any handler; `apply` constructs through
   `make` (`new OpenAIAuth(config ?? {})` → `make(config ?? {})`) and `auth`'s
   declared type widens from `OpenAIAuth` to `LiveAuth`, which `tsc --noEmit`
   accepts because only `LiveAuth` members are used. `init.lua` spawns
   `bun src/main.ts`, for which `import.meta.main` is true, so the cartridge's
   own startup is unchanged — and Verify block 2 proves that by speaking to the
   entrypoint on stdio rather than by matching the line's text.
2. `.cartridge/tests/integration/node.ts` (new): move the `node()` node-playing
   harness out of `wire.test.ts` verbatim and export it, defaulting its `serve`
   argument to a thrower. Point `wire.test.ts` at the import; its test body is
   untouched. `bun test` only collects `*.test.ts`, so the helper is not a
   test file.
3. `.cartridge/tests/integration/live.test.ts` (new): a `Bun.serve` GPT Live
   service on `127.0.0.1:0` that answers `session.start` with
   `session.started` plus one `session.output_audio.delta` (sent before anyone
   attaches, so the `StartedSocket` hold is exercised), records every client
   event, and optionally answers `session.close` with `session.closed`. Its
   `fetch` refuses the upgrade with 401 unless the request presents
   `Bearer <dummy>`.
4. Same file: a `cartridge()` fixture that seeds a temp `credentials.json` with
   the dummy key, builds `new Wire(input, output)` on two `PassThrough`s,
   calls `serve(wire, config => new OpenAIAuth(config, { home, env: {},
   fetch: <thrower>, socket: (destination, key) => { record(destination, key);
   return new WebSocket(loopback, { headers: { Authorization: \`Bearer ${key}\` } }); } }))`,
   and swaps `process.stderr.write` for the test so diagnostics can be
   asserted on. `env: {}` and a temp `home` keep discovery off the machine.
   `process.stderr.write` is process-global and `bun test` runs every file in
   one process, so the restore is pushed onto `cleanup` **before** the swap is
   installed: nothing can throw in between and leave the process's stderr
   wrapped for the rest of the run.
5. Same file, test one: `apply` → `create` → `attach` → `send` → `close`,
   asserting the recorded destination is `wss://api.openai.com/v1/live/sessions`
   and the bearer is the dummy, the `session.start` payload, the two
   `auth.live.event` frames (`auth.attached`, then the held delta), a live
   relayed event, the forwarded client event as the service received it,
   `{closing:true}` with `session.close` on the wire, `auth.detached` after
   `session.closed`, and that neither the collected node frames nor the
   captured stderr contains the dummy. Before that last pair of assertions the
   test makes one **`id`-less** failing call —
   `host.send({call:"auth.live",args:{op:"send",session_id:"live_ws",event:null}})`
   — which has nowhere to answer, so `Wire.answer`'s catch writes a real
   `diagnostic()` line, and the test asserts the capture **contains**
   `auth.live failed:` as well as **not** containing the dummy. Without that
   call the capture is empty and the disclosure clause is vacuous: it would
   pass because nothing ever logged, which is the same shape of unfailable
   assertion that unticked box 4.
6. Same file, test two: the service ignores `session.close`. `close` answers
   `{closing:true}`, and 100 ms later there is no `auth.detached` and `send`
   still answers `{sent:true}` — the session is waiting out the bound, not
   closed outright.

## Option chosen

`src/main.ts` hardcodes `wss://api.openai.com/v1/live/sessions` inside
`OpenAIAuth.start()` and constructs its provider with no `deps`. Three ways to
put a loopback service behind it:

- **A base-URL setting or env var read by `OpenAIAuth`.** Rejected: `help.md`
  states as a security property that a consumer "cannot supply its own
  credential or destination URL". A configurable destination is a second way to
  aim a discovered key at a host, which is exactly the property the cartridge
  sells.
- **Spawn `bun src/main.ts` as a subprocess and speak the protocol on its
  stdio.** Rejected: it cannot reach a loopback service at all without option A,
  so it buys process fidelity at the price of the invariant.
- **Export the registration as `serve(wire, make)` and let the test supply the
  provider.** Chosen. It reuses two seams that already exist and are already
  used by the shipped tests — `Wire`'s `(input, output)` constructor arguments
  and `OpenAIAuth`'s `deps.socket` — adds no runtime configuration, and leaves
  the destination a constant in `openai.ts` that the test asserts on rather than
  replaces. The diff is one `export function` line, one `if (import.meta.main)`
  line and an indentation change.

Splitting `node()` into its own module rather than copying it keeps one harness;
it is the same twenty-five lines `wire.test.ts` already had.

`attempt-2.patch` in `.state/loop/…` is the whole change (it supersedes
`attempt-1.patch`, adding the `id`-less failing call and the stderr-restore
ordering), applied and validated on a clean `dd35669` worktree: `git apply
--check` 0, `git apply` 0, `bun install --frozen-lockfile` 0, `bun run check` 0,
`bun test ./.cartridge/tests/` 0 with 15 pass / 0 fail. Three mutations of
`src/main.ts` — closing outright instead of sending `session.close`, dropping
`session_id` from the relayed frame, and dropping the `ws.send` in the `send` op
— each failed the suite (exit 1), so the boxes can fail. Two further mutations
pin the disclosure clause itself: removing the `id`-less call leaves the capture
empty and the suite exits 1, and a stray `process.stderr.write` of the bearer in
`OpenAIAuth.start()` also exits 1, on `not.toContain` — the clause fails both
when it has nothing to be about and when a key-bearing line is logged.

## Remaining risk

- **The router half of the credential contract is unguarded, and this spec does
  not guard it.** Box 3 holds by inspection across two cartridges: `router.ctg`
  `service.rs` `login` writes `{OPENAI_API_KEY: key}` into
  `<config_dir>/credentials.json`, the name coming from `catalog.rs`'s
  `{KEY}_API_KEY` (or `auth.rs` `env_name`, the same string), and
  `auth.ctg/src/openai.ts:81-89` reads it back. Three things break it silently:
  a change to router's `config_dir` setting, a change to the `{KEY}_API_KEY`
  naming, or the two processes resolving the **relative** path
  `.cartridge/credentials` (superproject `.cartridge/config.lua:59` and `:63`)
  against different working directories. The auth side is guarded
  (`auth.test.ts:24-30`); the router side cannot be guarded from inside this
  PRD's footprint. A guard belongs on router's board or in a composed test that
  runs `router login` and then `auth {op:"status"}`, and is out of scope here.
- **The 15 s close bound is pinned downward by behaviour and upward only by a
  literal.** Test two proves the session is *not* closed outright (15000→0 fails
  the suite), but 15000→150000 passes the suite and is caught solely by the
  `grep -qE` on the `setTimeout` literal. A real 15 s wait does not belong in a
  unit suite, so this is a deliberate trade, not a proven bound; driving the
  bound through a test-visible constant would close it.

## Verify and Proof

Guards first. Both blocks are repo-root-relative and run in the lane and then in
`repo`. No cargo, so no `CARGO_TARGET_DIR` applies; the question the lesson
actually asks is what pass 2 writes into the live checkout, and the answer is
`node_modules/` from `bun install --frozen-lockfile` — safe because
`/node_modules/` is in `auth.ctg`'s `.gitignore` and sits outside this PRD's
footprint (`src/**`, `.cartridge/**`, `cartridge.json`, `init.lua`), so
`prd collect`'s dirty-footprint sweep cannot pick it up. Block 2 also runs the
entrypoint for one frame; that process reads stdin, answers and exits, and
touches no daemon.

```sh
test -f src/main.ts
test -f src/openai.ts
test -f .cartridge/tests/integration/node.ts
test -f .cartridge/tests/integration/live.test.ts
# The registration is a seam the test can drive.
grep -q 'export function serve(' src/main.ts
# Anchored, so a commented-out entrypoint does not satisfy it; the stdio smoke
# in the next block is what actually proves the program starts.
grep -qE '^if\(import\.meta\.main\) serve\(new Wire\(\)\);' src/main.ts
# The key-disclosure clause asserts on a capture known to be non-empty.
grep -q 'expect(errors.join("")).toContain("auth.live failed:")' .cartridge/tests/integration/live.test.ts
# The mock GPT Live service is bound to loopback.
grep -q 'hostname: "127.0.0.1"' .cartridge/tests/integration/live.test.ts
# It never reaches this machine's environment or home, so no real store is read.
if grep -qn 'process\.env' .cartridge/tests/integration/live.test.ts; then exit 1; fi
if grep -qn 'homedir(' .cartridge/tests/integration/live.test.ts; then exit 1; fi
# The destination stays a constant in the provider, not a setting.
grep -q 'wss://api.openai.com/v1/live/sessions' src/openai.ts
# The close handshake keeps its bound.
grep -qE 'setTimeout\(\(\) *=> *ws\.close\(\), *15000\)' src/main.ts
```

```sh
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
"$CARTRIDGE_BUN" install --frozen-lockfile
"$CARTRIDGE_BUN" run check
"$CARTRIDGE_BUN" test ./.cartridge/tests/
# The entrypoint really starts: one `apply` frame in, one answer out. A
# commented-out or otherwise inert `serve(new Wire())` registers no handler and
# answers nothing. `apply` only constructs the provider, so no store is read.
printf '{"id":1,"call":"apply","args":{}}\n' | "$CARTRIDGE_BUN" src/main.ts | grep -q '"id":1,"result":'
```
