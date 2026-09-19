---
complexity: medium
footprint:
  - src/materialize.ts
  - src/openai.ts
  - src/main.ts
  - cartridge.json
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/README.md
  - .cartridge/tests/integration/materialize.test.ts
---

# spec01 — `auth {op:"materialize"}` pushes pass-managed api-keys into the router by calling it, never by opening its file

Base: `auth.ctg` at `fa3490b6ed4229d09687e6183b6430870a854c8` (the PRD's source
HEAD). Every citation below is a line of that sha. The whole change was built
and run once in a `git archive fa3490b6` copy at
`/private/tmp/claude-501/-Users-feb-dev-cartridge/5c846381-13af-4f63-97ae-8d81864388ce/scratchpad/e4-auth/tree`;
see "Probe results".

Coordinator note, folded in after the brief: collect's `assertFootprint`
(`prd.ctg/src/lifecycle.ts`) treats a footprint entry as a literal path
prefix, not a glob — `src/**` never prefix-matches `src/main.ts`. The
coordinator retargeted the PRD's own footprint from `src/**` /
`.cartridge/tests/**` to the literal directory prefixes `src` and
`.cartridge/tests`. Every entry in this spec's frontmatter above is already
an exact file path with no `*` in it, so each one prefix-matches itself under
that same rule, and every entry falls under one of the PRD's now-literal
prefixes; nothing here needed to change for that fact.

## Design decision: call the router, never open its file

The PRD's Context reads "auth instead writes the router's `credentials.json`
from the pass store. … The router does not change." Read literally that has
auth open and rewrite a file that belongs to `router.ctg`. The workspace rule
(`system/isolation.md`, from `just prompt`): "A cartridge crosses a boundary
only by a declared need or an event and includes no sibling's crate, script,
fixture or file." Two independent facts say the literal reading cannot stand:

1. **The sandbox already refuses it.** `auth.ctg/cartridge.json`'s `grant.write`
   is `["$HOME/.cartridge/auth/.gnupg"]` — nothing under router's
   `credentials_dir` is writable by this node today. Widening `write` to reach
   a sibling's state directory is itself the isolation violation `just
   isolation` exists to catch.
2. **A door already exists and needs no router change.** `router {op:"login",
   provider, key}` (`router.ctg/src/service.rs:200-220`) reads
   `credentials.json`, merges in one `{name: key}` pair keyed by
   `auth::env_name(provider)` or the catalog's configured key name, and writes
   it back atomically at mode `0600` (`router.ctg/src/auth.rs:1066-1080`,
   `atomic_json`: `create_new().write(true).mode(0o600)`). `router
   {op:"logout", provider}` (`service.rs:248-264`) removes exactly that
   provider's key via `remove_key` (`router.ctg/src/auth.rs:572-583`, reads,
   removes one map key, atomic-writes only if it was present). Both ops exist
   today; neither needs a router code change, so "the router does not change"
   still holds — only the *mechanism* the PRD Context names changes, not the
   outcome.

**Decision:** auth declares `needs: ["router"]` in `cartridge.json` and, on
`auth {op:"materialize"}`, calls `router {op:"login", provider, key}` for
every stored `cartridge/<provider>/api-key` entry and `router {op:"logout",
provider}` for a provider this cartridge previously materialized that pass no
longer holds. auth never opens `credentials.json`. This is the same
cross-cartridge mechanism `fs.ctg` already uses for `router`
(`fs.ctg/cartridge.json:5-8` declares `needs: ["sessions","router"]`,
`fs.ctg/init.lua:20` calls `cartridge.bail("router", step.router)`): a TS
cartridge's spawned process reaches it as `wire.call(name, args)`
(`auth.ctg/src/wire.ts:55`, `call(name,args) { return this.ask({bail:name,
args}); }`), which needs nothing beyond `needs` in the manifest — auth's
`init.lua` (`cartridge.spawn` + `app:request`, unchanged) already forwards any
`ask` frame the spawned process writes, so `init.lua` does not change.

Because `login` is a read-merge-write on one key and `logout` removes one
named key, an entry the router itself wrote for OAuth (`chatgpt`,
`claude-code`, which are never pass-managed providers) is left untouched by
either call — satisfying "keeps the entries the router wrote for OAuth"
without auth ever reading the file to check.

**Proposed PRD amendment** (for the coordinator, not applied by this spec):
the Context sentence "auth instead writes the router's `credentials.json`
from the pass store" should read "auth instead calls `router {op:\"login\"}`
and `router {op:\"logout\"}` with the pass store's current contents; the
router still owns and writes its own `credentials.json`." The Outcome
("pass is the source of truth and the file is a derived cache with mode
`0600`") and "The router does not change" both still hold under this reading
— only the sentence naming the mechanism is stale.

## Detecting a removed key

`router {op:"credentials"}` (`service.rs:232-235`) lists key **names**
(`OPENAI_API_KEY`, …), not provider ids, and a provider's key name can be
overridden per-catalog (`service.rs:203-208`), so reversing name→provider
client-side would be a guess. Instead auth remembers, in its own state
directory, the set of provider ids it materialized last time
(`~/.cartridge/auth/materialized.json`, plain JSON array of provider ids, no
secret value). Each call diffs pass's current provider set against that
record: anything dropped from the record gets `router {op:"logout"}`; the
record is atomically-simple to write with, then overwritten with the new set.
This never calls `logout` for a provider auth did not itself add, so it
cannot clear OAuth state `logout` also drops for `provider`
(`service.rs:260-261`, `remove_oauth`/`clear_pending`) — that risk exists only
for a provider that is *both* pass-managed and previously materialized, which
this design guarantees by construction.

A missing or corrupt record reads as `[]` (nothing known yet); the next
successful materialize repairs it. `# ponytail: the record write is not
atomic — a crash between the router calls and the write can delay one
provider's removal by one materialize cycle; upgrade to a temp-file-and-rename
like `auth::atomic_json` if that delay ever matters.`

## Error handling across the `router` need

Coordinator note, folded in after the brief: a failure that crosses a Lua
listener arrives wrapped as `<id>: runtime error: <message>` plus a stack
traceback, not the bare message a Rust `Err` string would be on router's own
side. `wire.call` (`src/wire.ts:55`, `ask({bail:name,args})`) already turns
whatever `frame.error` the host sends back into a plain `new Error(...)`
(`wire.ts:77`) — `materialize()` never inspects, parses or prefix-matches
that text itself; it lets a `router` call's rejection propagate as
`materialize()`'s own rejection unchanged, the same way `auth.jev` already
treats an unreachable dependency as an opaque failure rather than a string to
classify. Nothing in `materialize.ts` does `error.message.startsWith(...)` or
any other match against router's wording, wrapped or not, and the Verify
block does not gate on that wording either — the two named tests only
exercise the success path (the fake router in the harness always answers),
so no test claims anything about the wrapped text's exact shape.

## Files and functions

1. **`src/materialize.ts`** (new). Exports `materialize(deps: PassDeps, call:
   (name:string,args:unknown)=>Promise<unknown>): Promise<{materialized:
   string[]; removed: string[]}>`. Uses `list`, `read as readPass`, `place`
   from `./pass` (`src/pass.ts:17` `place`, `:23` `entry`, `:40` `read`, `:67`
   `list`; none of these three functions need to change). Steps: list every
   pass entry, keep only `field === "api-key"`; for each, `read` the value —
   an entry that fails to decrypt is skipped this round, not fatal; call
   `router {op:"login", provider, key}` for each readable entry and collect
   its provider into `current` (sorted); read the previous provider set from
   `~/.cartridge/auth/materialized.json` (via `place(deps).state`), compute
   `removed = previous - current`, call `router {op:"logout", provider}` for
   each; write `current` back to the record file (`mkdirSync` the state dir
   first, mode `0700`, matching `src/pass.ts:87`'s existing convention);
   return `{materialized: current, removed}` — provider strings only, never a
   key. Doc-comment the file's purpose without the literal string
   `credentials.json` in `src/materialize.ts` itself (say "the router's
   credential file" instead) — the Verify block below greps that exact
   string in that one file as a negative check, and a comment naming it
   would be a false positive caught and fixed while building this spec.
2. **`src/openai.ts`**: import `materialize` and its two types; add
   `materialize(call: Call): Promise<MaterializeResult>` to the `LiveAuth`
   interface (`:17-24`) beside `list`; add `materialize(call: Call) {  return
   materialize(this.deps, call); }` to `OpenAIAuth` beside `list()`
   (`:129-130`) — the same one-line-delegation pattern `list()` and `jev()`
   already use.
3. **`src/main.ts`**: in the `wire.on("auth", …)` handler (`:11-15`), add
   `if(args?.op==="materialize") return
   auth.materialize((name,callArgs)=>wire.call(name,callArgs));` before the
   `throw`, and extend the throw's text to name `materialize`.
4. **`cartridge.json`**:
   - add top-level `"needs": ["router"]`.
   - add `"materialize"` to the `auth` event's `op` enum
     (`cartridge.json` line ~17-20) and extend the event `description` to
     document `{op:"materialize"}` → `{materialized, removed}`.
   - widen `grant.write` from `["$HOME/.cartridge/auth/.gnupg"]` to
     `["$HOME/.cartridge/auth"]` (covers the existing `.gnupg` subdirectory
     and the new `materialized.json`; it still reaches nothing outside
     auth's own state directory, so `just isolation` still reports nothing
     for it — router's directory is never named).
5. **`README.md`** and **`.cartridge/help.md`** (Acceptance box 4): replace
   the "Needs — nothing. It stands alone in any composition." line with
   "Needs — `router`, to materialize a pass-managed api-key into its
   credential store." Add a bullet: `` `auth`: `{"op":"materialize"}` logs
   every stored `api-key` entry into the router (`router {op:"login"}`) and
   logs out a provider pass no longer holds that this cartridge previously
   materialized (`router {op:"logout"}`); returns `{materialized, removed}`
   as provider names, never values. `` and state plainly that `router
   {op:"login", provider, key}` run directly (without pass) is superseded by
   `pass insert` (the door, `bun src/insert.ts <provider> [field]`) plus
   `auth {op:"materialize"}`.
6. **`.cartridge/docs/README.md`** (in footprint, not separately gated):
   update the "Sandbox" paragraph's quoted `write` grant to
   `["$HOME/.cartridge/auth"]`, and add a `materialize` row to "Service
   contracts" alongside `list`.
7. **`.cartridge/tests/integration/materialize.test.ts`** (new): see "Test
   plan".

## Test plan

Follow the harness `.cartridge/tests/integration/pass.test.ts` and
`node.ts` already use: a real `Wire` over a `PassThrough` pair running the
real `serve()` handlers, with the `node()` test helper's `serve` callback
answering `{ask, bail:"router", args}` frames in place of a real router
(`node.ts:14-16` already handles any `bail`/`host` ask generically — no
change to that helper). This proves the real `materialize()` code path end to
end without a live router.

Two named tests (both run and passed in the prototype, see "Probe results"):

- **"materialize logs in every stored api-key entry and returns names only,
  never the fixture value"** — insert `openai` and `typesafe` api-key entries
  and one entry under a *different field* on `openai`; materialize; assert
  the router received exactly one `{op:"login",provider,key}` per api-key
  provider with the real decrypted value (defeats a stub that never reads
  pass, or that materializes every field indiscriminately); assert the
  response is exactly `{materialized:["openai","typesafe"],removed:[]}`
  (defeats a lazy implementation that echoes the entry name, the raw key, or
  an extra field); assert neither fixture secret appears anywhere in the
  response or in any stray (`host.loose`) frame (defeats a lazy
  implementation that logs or broadcasts the key it just read).
- **"a key removed from pass is logged out on the next materialize and an
  untouched provider is left alone"** — materialize once with two providers,
  delete one entry's `.gpg` file directly (simulating "removed from pass"),
  materialize again; assert the second round's router calls are exactly one
  `login` for the surviving provider and one `logout` for the dropped one,
  in that order, and the response is
  `{materialized:["openai"],removed:["typesafe"]}` (defeats a lazy
  implementation that never diffs and only ever calls `login`, or that
  logs out every provider on every call, or that logs out the wrong one).

Both tests were also run against two mutants of the prototype `materialize.ts`
to confirm they fail on a lazy implementation, not just pass on a correct one
(see "Probe results"): (a) adding the raw entry names to the response turned
the first test red; (b) deleting the `logout` loop turned the second test red.
Restoring the correct file turned both green again.

## Verify and Proof

<!--
Both blocks run under `sh -eu -c`, no injected environment, per the engine
contract in `spec.md`. No cargo or a live cartridge's build dir is involved:
this is a bun-only footprint, so no `CARGO_TARGET_DIR` pin is needed. The
structural block only inspects source text (grep) and runs `tsc --noEmit`
through the cartridge's own `check` command, never a network call or a router.
The test block runs the real suite with a JUnit report, per
`bun-test-names-are-not-in-its-log`.
-->

```sh
grep -q '"needs"' cartridge.json
grep -q '"router"' cartridge.json
grep -q '"materialize"' cartridge.json
grep -q '"$HOME/.cartridge/auth"' cartridge.json
if grep -q '"$HOME/.cartridge/auth/.gnupg"' cartridge.json; then exit 1; fi
grep -q 'router' README.md
grep -q 'materialize' README.md
grep -q 'materialize' .cartridge/help.md
grep -q 'superseded' README.md
# auth must never itself open router's file; it may only call it.
if grep -q 'credentials.json' src/materialize.ts; then exit 1; fi
if grep -q 'router_data_dir' src/materialize.ts; then exit 1; fi
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" install --frozen-lockfile
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" run check
```

```test
run: env -u CARTRIDGE_YOLO "${CARTRIDGE_BUN:-bun}" test ./.cartridge/tests/ --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: materialize logs in every stored api-key entry and returns names only, never the fixture value
pass: a key removed from pass is logged out on the next materialize and an untouched provider is left alone
pass: a stored entry decrypts inside the process and the value reaches only the authenticated call
pass: the insert door round-trips a value that status reports as source pass without the value
pass: list returns every cartridge entry and no response or frame carries the value
pass: shared credentials are discovered without leaking them into status
```

## Probe results

All run in the throwaway copy named above, `auth.ctg` at `fa3490b6`, 2026-09-19:

```
$ env -u CARTRIDGE_YOLO bun install --frozen-lockfile
5 packages installed [25.00ms]
$ env -u CARTRIDGE_YOLO bun run check
$ tsc --noEmit          # exit 0, no output
$ env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/integration/materialize.test.ts
2 pass, 0 fail, 7 expect() calls
$ env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/
34 pass, 0 fail, 177 expect() calls   # full existing suite plus the two new tests, no regression
```

Mutant 1 (response leaks the entry names: `return {materialized, removed,
keys: entries.map(e=>e.name)}`): `bun test` on
`materialize.test.ts` → 0 pass, 2 fail (`toEqual` catches the added `keys`
field). Mutant 2 (drop the `logout` loop entirely): 1 pass, 1 fail (the
second test's `expect(calls).toEqual([...])` catches the missing `logout`
call). Restoring the file: 2 pass, 0 fail again.

## Acceptance

- [ ] `auth {op:"materialize"}` calls `router {op:"login", provider, key}`
      for every `cartridge/<provider>/api-key` entry pass holds (atomic,
      mode `0600` — both guaranteed by the router's own `atomic_json`, not
      by auth), calls `router {op:"logout", provider}` for a provider pass no
      longer holds that this cartridge previously materialized (never
      touching the router's own OAuth entries), and returns
      `{materialized, removed}` as provider names only.
- [ ] The named test "a key removed from pass is logged out on the next
      materialize and an untouched provider is left alone" shows a key
      removed from pass disappears from the router's state on the next
      materialize, without disturbing an untouched provider.
- [ ] The named test "materialize logs in every stored api-key entry and
      returns names only, never the fixture value" asserts the response and
      every published envelope (including stray wire frames) are free of the
      fixture's value.
- [ ] `README.md` and `.cartridge/help.md` tell the user to add a key with
      `pass insert` (the door, `bun src/insert.ts <provider> [field]`) and
      say that `router {op:"login"}` run directly with a `key` is superseded
      by `pass insert` + `auth {op:"materialize"}`.

## Dependencies and base

- The lane base is `auth.ctg` `fa3490b6ed4229d09687e6183b6430870a854c8`. The
  declared prerequisite
  `@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values` is
  collected (it landed `src/pass.ts`'s `list`/`read`/`entry`/`place`, which
  this spec calls unchanged).
- No PRD needs this one yet.
- Manifest changes collector note: because `cartridge.json` changes
  (`needs`, the `auth` event schema, `grant.write`), the coordinator must run
  `cartridge trust /Users/feb/dev/cartridge/auth.ctg` (auth only) and
  `cartridge reload auth` immediately after collect, and this PRD is not a
  fast-path candidate under `review-plan.md` (it changes a manifest surface
  and touches more than two files), so it goes through the normal plan
  review.
- Reusable attempt artifact: the prototype tree at
  `/private/tmp/claude-501/-Users-feb-dev-cartridge/5c846381-13af-4f63-97ae-8d81864388ce/scratchpad/e4-auth/tree`
  is `fa3490b6` with steps 1–7 applied and both tests green; it is a
  throwaway copy (`git archive`, no `.git`), so a worker re-does the edit in
  the real lane rather than copying files across, but the diff is small and
  every line above cites it exactly.
