# @auth/gpt-live-connects-over-websocket-on-the-discovered-credential review history

Plan: `@auth/gpt-live-connects-over-websocket-on-the-discovered-credential`,
`prd.ctg/.cartridge/boards/auth/prds/gpt-live-connects-over-websocket-on-the-discovered-credential/prd.md`
(owner `auth.ctg`, prio 90).
Scope: executable leaf — one observable outcome, `auth.live` carries a GPT Live
session over the WebSocket transport on the credential auth discovers.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: `auth.ctg` `dd3566926bb3402ed619884d02be9931429c462c`
(confirmed HEAD, `git status --porcelain` empty; superproject gitlink
`160000 commit dd35669…` for `auth.ctg`), plus the unapplied prototype
`attempt-1.patch`. No dirty files in `auth.ctg`.

| Input | Content digest (SHA-256) |
| --- | --- |
| Plan | `prds/…/prd.md` `3cf8a5e42f7d0c67f0bbe1592f0003899db3288c76808d25dad1fd1b63c7b402` |
| Specs | `prds/…/specs/spec01.md` `2fa7d69890d0e55039e2373e22caed4810834fc9a90ffcf32154c776fdd1caf0` (byte-identical to the `.state/loop` draft — `diff` exit 0) |
| Prototype | `.state/loop/…/attempt-1.patch` `4faffafdb13f355659cbb9ffc63f21ec08e732bd0f12c4bd60dc10d83784c138` |
| Source of record | `auth.ctg@dd35669 src/main.ts` `cee3ac9c620ef8214f41a7f15047a309002bef6c49b0e76964160b9be75dc998`; `src/openai.ts` `0a5ed13575e3e8e35b4d0fef79f3428a8e929a6400faa988e5be82a3964af1db`; `.cartridge/help.md` `58bf64707a41d2f9062b700b50fa3dfe39943744d07a40add5039942219ce66d` |
| Material contracts | superproject `.cartridge/config.lua` `58497aea44bcbcdafa477858a51fab32f5b2c5a0a5c13c3ca05181c7527fb651` (`:59` router `config_dir`, `:63` auth `credentials_dir`); `router.ctg` `src/service.rs` `login`, `src/catalog.rs` `API_PROVIDERS`/`push_api`, `src/auth.rs` `env_name`, `src/settings.rs` `Paths::from`; `auth.ctg/init.lua`; `auth.ctg/cartridge.json` |
| Analyst record | `prds/…/analyst-1.md` `702e39b73a42f65b228e7287fe2675b6c930b4c369d9b96a56c047c5ba8e538d` |

### Re-derived box audit (not taken on the analyst's say-so)

**Box 1 — websocket `create` — HOLDS.** `src/openai.ts:114` sets
`websocket = body?.transport?.type==="websocket"`; `:115` makes the WebRTC SDP
guard conditional on `!websocket`, so for every non-websocket request the guard
is the same predicate as before the commit (`git show dd35669 -- src/openai.ts`
shows the old line replaced by `!websocket && (<old predicate>)`). `:118` routes
to `start()`; `:139` is the destination constant; `:151-154` sends
`{type:"session.start",session}` on `open`; `:160-163` resolves the id from
`session.started`; `:173` returns `{session:{id}},transport:{type:"websocket"}`.
The WebRTC branch is untouched in the diff (hunks jump `@@ -18,9 +19,39 @@` to
`@@ -80,9 +111,11 @@` to `@@ -99,6 +132,46 @@`, all additions), and its tests
pass at baseline (13 pass / 0 fail).

**Box 3 — discovery from the router's store — HOLDS, by inspection only, and not
because of `dd35669`.** `discover()` is genuinely absent from the commit: the
`src/openai.ts` diff never touches lines 55-110. The tick stands on a
cross-cartridge chain I re-traced myself:

1. `router.ctg/src/service.rs` `"login"` resolves
   `cat.providers.get(provider).map(|p| p.key.clone()).filter(non-empty)` else
   `auth::env_name(provider)`, then writes `{ <name>: key }` into
   `service.paths.credentials.join("credentials.json")`.
2. Both name sources give the same string: `catalog.rs` `push_api` sets
   `key: format!("{key}_API_KEY")` from `name.to_uppercase().replace('-',"_")`
   (`openai` is in `API_PROVIDERS`), and `auth.rs` `env_name` is the identical
   `format!("{}_API_KEY", name.to_uppercase().replace('-',"_"))`. Either path →
   **`OPENAI_API_KEY`**.
3. `router.ctg/src/settings.rs` `Paths::from` binds `credentials` to the
   `config_dir` setting, nothing else.
4. Superproject `.cartridge/config.lua`: router `config_dir = ".cartridge/credentials"`,
   auth `credentials_dir = ".cartridge/credentials"` — the same directory.
5. `auth.ctg/src/openai.ts:81-89` reads `<credentials_dir>/credentials.json` and
   accepts `OPENAI_API_KEY` or `openai`, recording the *path* as `source`;
   `:104-109` builds the status from paths only.

The auth half is guarded (`auth.test.ts:24-30` asserts `status.source` is the
path and `JSON.stringify(status)` does not contain the secret, for exactly the
key name and file shape router writes). The router half is guarded by nothing,
cannot be guarded from inside auth's footprint, and additionally depends on both
processes resolving the same *relative* `.cartridge/credentials` against the same
base. Analyst's qualification confirmed and sharpened; see F5.

**Box 4 — DOES NOT HOLD; the untick is correct.** At `dd35669`,
`grep -rn 'src/main' .cartridge/tests/` returns **nothing** (exit 1): no test
imports the module the relay, `send` and `close` live in. The added tests drive
`OpenAIAuth` through an in-process `FakeSocket` (`auth.test.ts:16-23`) — no
server, no port, no socket. Independently confirmed by mutation: with the
patch removed, the three shipped-code mutations below cannot fail anything,
because nothing executes that code at all.

**Box 2 — implemented, unproven.** Read `src/main.ts` at `dd35669`: `emit` at
`:12` carries `session_id`; the message listener at `:27-36` relays; `close` at
`:41-53` sends `{type:"session.close"}`, arms `setTimeout(()=>ws.close(),15000)`
and clears it on `session.closed`; `send` at `:55-59` forwards. Correct as
written; unexecuted by any test. One piece of work closing boxes 2 and 4
together is the right slice.

### Verdict on the `serve()` seam

**The seam is the right trade, and it does not have the sibling's reach.** The
sibling finding (`@root/…/router-refreshes-oauth-tokens…` review, F4) was that
`ROUTER_CODEX_TOKEN_URL` shipped in the daemon and let *anything able to set an
environment variable* — a launcher script, a shell profile, an inherited
environment — silently redirect a POST carrying a live refresh token. `serve`
has no analogous reach:

- It reads no environment variable and no setting. The only way to supply a
  different `make` is to `import` the module inside your own process, which
  already presupposes code execution in the auth process — and that already
  grants direct read of `credentials.json`. No new capability, no quiet path.
- The destination stays a constant in `openai.ts` (`start()` line 139) that the
  new test *asserts on* rather than replaces, preserving the property
  `.cartridge/help.md` sells verbatim: a consumer "cannot supply its own
  credential or destination URL". The spec's rejection of the base-URL/env
  option is grounded in that exact documented sentence — I verified the sentence
  exists.
- `deps.socket` and `new Wire(input,output)` are pre-existing seams already used
  by shipped tests, so the seam's surface grows by one exported function.

**`if (import.meta.main)` is genuinely behaviour-preserving for `init.lua`'s
spawn**, verified three ways rather than argued:
`init.lua` runs `cartridge.spawn({"bun", cartridge.root .. "/src/main.ts"})`;
a probe script executed as `bun /abs/path/probe.ts` prints `main= true`; the
same flag prints `false` when the module is imported under `bun test`; and the
**patched entrypoint answers over real stdio** — piping
`{"id":1,"call":"apply","args":{}}` and `{"id":2,"call":"auth.live","args":{"op":"bogus"}}`
into `bun src/main.ts` returned `{"id":1,"result":null}` and
`{"id":2,"error":"Voice session is not attached"}`. Per-call state
(`auth`/`sockets`/`carriesAudio` moving into the function) is equivalent for the
single production call, and `tsc --noEmit` is clean with `auth` widened to
`LiveAuth`.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Closes the two remaining boxes with one slice: 3 production lines (`export function serve(`, `if(import.meta.main) serve(new Wire());`, the `make(config ?? {})` call) plus ~150 test lines in 4 files, all inside the PRD's declared footprint (`src/**`, `.cartridge/**`). The value is real and measurable: at `dd35669` **no test imports `src/main.ts`** (grep exit 1), so the entire `auth.live` wire surface — the one the PRD's outcome is about — is unexecuted; three deliberate breaks of shipped code are invisible today and each fails the suite with the patch. −1: step 1 claims "No handler body changes", but the `apply` handler body does change (`new OpenAIAuth(config ?? {})` → `make(config ?? {})`) and `auth`'s declared type widens from `OpenAIAuth` to `LiveAuth`; harmless (tsc clean, only `LiveAuth` members are used) but the step text is what an implementer follows. |
| Ownership and reuse | 19 | Owner matches `repo:` and every touched path is in footprint; nothing is written outside `auth.ctg`. Climbs the reuse ladder correctly: `Wire(input,output)` and `deps.socket` already exist and are already used by shipped tests, `node()` is *moved* rather than copied so one harness survives, `Bun.serve` is the platform's own server (no new dependency — `bun install --frozen-lockfile` exit 0 with the unchanged lockfile). Both rejected options are argued against a documented security property that I verified in `.cartridge/help.md`, and the chosen one adds no runtime configuration (see the seam verdict above). −1: box 3's only unguarded leg — the router-writes-what-auth-reads contract, and its dependence on both cartridges resolving the same relative `.cartridge/credentials` — is named in the analyst report and the PRD's Planning note but **not recorded as a residual risk anywhere in the spec**, which is the document the implementer and the collect gate read (F5). |
| Dependencies and implementable slices | 19 | `git apply --check` exit 0 on a pristine `dd35669` worktree; applies clean; `git status --porcelain` after applying is exactly ` M .cartridge/tests/integration/wire.test.ts`, ` M src/main.ts`, `?? .cartridge/tests/integration/live.test.ts`, `?? .cartridge/tests/integration/node.ts` — the four declared files and nothing else. No `needs`, no cross-cartridge ordering, one slice. Verify blocks follow the engine facts: repo-root-relative paths, no `cd`, no cargo (so no `CARGO_TARGET_DIR` question), and both run well inside 120 s (block 1 <1 s, block 2 ≈4 s wall including install). −1: the spec dismisses the whole live-checkout question with "no cargo, so no `CARGO_TARGET_DIR` is needed here", but pass 2 does run `bun install --frozen-lockfile` *inside the live `auth.ctg` checkout*, writing `node_modules/`. It is in fact safe — `/node_modules/` is in `.gitignore` and is outside the PRD footprint, so `prd collect`'s dirty-footprint sweep cannot pick it up, and `cartridge.json`'s `commands` are not executed by the host — but the spec establishes none of that, which is the same omission the `verify-blocks-must-not-build-live-targets` lesson is about. |
| Observable acceptance and baseline evidence | 14 | Every claim in the spec and the analyst report reproduces (full command table below): baseline 13 pass, patched 15 pass, `bun run check` 0 both, guard block 0 patched / **1 on an unpatched tree**, all six deliberately-broken trees exit 1 and the restored tree 0, all three shipped-code mutations fail the suite (2 / 1 / 1 failures), and the safety mutation gives 0 pass / 2 fail. No guard is `!`-prefixed (the two negative guards use `if grep -qn …; then exit 1; fi`) and all four referenced paths are `test -f` guarded. Deductions: **−3, F1** — the box-4 clause "no log line carries the key" is **vacuous as written**: I instrumented the fixture and the captured stderr is `[]`, length 0, so `expect(errors.join("")).not.toContain(DUMMY)` passes because nothing ever logged, not because a log line was checked. That is the same class of defect — an assertion that could not fail — that got box 4 unticked in the first place. **−2, F2** — `grep -q 'if(import.meta.main) serve(new Wire());'` is satisfied by a *commented-out* line: with `// ` prefixed, the guard block exits **0**, the suite still passes **15 / 0**, and the entrypoint answers nothing on stdio. Both gates accept a cartridge that would never start, on the spec's one production change. **−1, F3** — the 15 s bound is pinned in one direction only: 15000→0 fails the suite (1 fail), but 15000→**150000** passes the suite 15/0 and is caught solely by the literal `grep -qE`. |
| Failure, recovery and compatibility | 18 | Isolation of the new test verified by reading it rather than trusting it: `env: {}` (so `discover()`'s first candidate, `env.OPENAI_API_KEY`, is unreachable), a `mkdtempSync` `home` (so `codex_home` falls back to `<temp>/.codex`, never `~/.codex`), `credentials_dir` set through `apply` to the temp directory, `fetch` replaced by a thrower (the WebSocket path must make no HTTP request), and `socket` dialling `ws://127.0.0.1:<ephemeral>`. The mock's `fetch` returns 401 unless `authorization === "Bearer <dummy>"`, and I confirmed the consequence: seeding the fixture store with `sk-not-the-fixture-key` gives **0 pass / 2 fail** with "OpenAI voice session connection failed", so a real key fails the test instead of being spent. Backward compatibility of the seam is proved, not asserted (see above). −1: `process.stderr.write` is swapped **process-globally** and restored only in `afterEach`; `bun test` runs files in one process, so any throw between the swap and the `cleanup.push` — or a future concurrent file — leaves the whole process's stderr wrapped. Cheap to make `try`/`finally`-shaped, and it becomes load-bearing once F1 is fixed and the capture is actually non-empty. −1: nothing in the plan records what silently breaks box 3 (a change to router's `config_dir`, to `catalog.rs`'s `{KEY}_API_KEY` naming, or to either cartridge's working directory), so the one unguarded contract in this PRD has no written recovery story. |
| **Reviewer total** | **89 / 100** | Below the 90 threshold, and one blocking finding (F1). |

### Findings

| # | Finding | Evidence | Recommendation |
| ---: | --- | --- | --- |
| **F1** | **BLOCKING.** The "no diagnostic line carries the key" clause asserts against an empty capture. Ticking box 4 on it would repeat exactly the defect that unticked box 4. | Instrumented `live.test.ts` at the assertion: `STDERR_CAPTURE_LEN=0 CONTENT=[]`, test still 2 pass. Nothing in the happy path writes a diagnostic. | Two lines, proved to work: before the assertion, drive one handler failure with no `id` so `Wire.answer`'s catch calls `diagnostic()` — `host.send({call:"auth.live",args:{op:"send",session_id:"live_ws",event:null}}); await Bun.sleep(30);` yields `["{\"t\":…,\"src\":\"wire\",\"msg\":\"auth.live failed: …\"}\n"]`. Then assert the capture is non-empty *and* free of the dummy. Add a guard that the test asserts on a non-empty capture. |
| **F2** | The `import.meta.main` guard is satisfied by a commented-out line, so neither gate can tell a working cartridge from one that never starts. | With `// if(import.meta.main) serve(new Wire());`: guard block exit **0**, `bun test` **15 pass / 0 fail**, `printf '{"id":1,"call":"apply","args":{}}' \| bun src/main.ts` produces **no output**. | Replace the string pin with the smoke I ran — it needs no network and no credential: pipe one `apply` frame into `bun src/main.ts` and require a `{"id":1,"result":` line. Or at minimum anchor the grep (`grep -qE '^if\(import\.meta\.main\)'`), which the comment defeats. |
| **F3** | The 15 s bound is pinned downward by behaviour and upward only by a literal grep. | 15000→0: suite 1 fail. 15000→150000: suite **0**, 15 pass; only `grep -qE 'setTimeout…15000'` fails. | Acceptable trade (a real 15 s wait does not belong in a unit suite) — but say so in the spec, in one line, instead of presenting the bound as behaviourally proven. Or drive the bound through a test-visible constant. |
| **F4** | Step 1 says "No handler body changes"; the `apply` handler body and `auth`'s declared type both change. | `attempt-1.patch`: `let auth:OpenAIAuth` → `let auth:LiveAuth`; `auth=new OpenAIAuth(config ?? {})` → `auth=make(config ?? {})`. | Reword to "no behaviour change in any handler; `apply` constructs through `make`". `tsc --noEmit` exit 0 confirms the widening is safe. |
| **F5** | Box 3's only unguarded leg is not recorded as a residual risk in the spec. | The chain (`service.rs` `login` → `env_name`/`catalog.rs` `OPENAI_API_KEY` → `settings.rs` `Paths.credentials` → `config.lua:59`/`:63` → `openai.ts:81-89`) is guarded on the auth side only; both ends also assume the same base for the relative path `.cartridge/credentials`. | Add a Remaining-risk line to spec01 naming the three things that break it (router `config_dir`, the `{KEY}_API_KEY` naming, a differing working directory) and where a guard could live (router's board or a composed test), so the PRD does not collect with the contract silently unrecorded. |
| **F6** | Verify pass 2 writes `node_modules/` into the live `auth.ctg` checkout, and the spec does not say why that is safe. | Block 2 runs `bun install --frozen-lockfile`. Verified safe: `.gitignore` has `/node_modules/`; it is outside the footprint `src/**`, `.cartridge/**`, `cartridge.json`, `init.lua`; `cartridge.json` `commands` are not host-executed (no `sandbox/macos.rs`; `commands` appear only in `cli/manual.rs`). | One line in the spec stating it, replacing "no cargo, so no `CARGO_TARGET_DIR` is needed here" — the question the lesson asks is what the block writes into the live checkout, not whether it uses cargo. |
| **F7** | `process.stderr.write` is patched process-globally in a shared `bun test` process. | `live.test.ts` `cartridge()`; restoration is an `afterEach` cleanup entry. | Keep the cleanup, but note it in the spec; once F1 makes the capture load-bearing it is worth asserting the restore. |

F1 is the only blocking finding: it would let a PRD acceptance box be ticked on a
clause that cannot fail. F2 is one line from the same category and should be
fixed in the same edit — the underlying behaviour is *correct today* (I proved
the entrypoint answers over stdio), so it is drift protection, not a defect.
F3–F7 are accuracy and record-keeping.

Disposition: **revise** — keep the plan, the seam and the prototype; fix F1 (and
F2 with it), then apply the F3–F7 wording. No split, merge, rehome or retire.
The boxes as written are the right boxes; one of them is not yet checkable.

Box recommendations to the coordinator: **box 1 holds** and **box 3 holds**
(by inspection, with the router leg unguarded — re-derived independently, not
taken from analyst-1); **box 4's untick is correct**; box 2 is implemented and
unproven exactly as recorded. Nothing in the Planning note needs correcting.

Validation: all commands run in private scratch worktrees of `auth.ctg` at
`dd35669` under this session's scratchpad (`…/scratchpad/rev1-gptlive/{base,iso}`),
created with `git worktree add --detach` and pruned afterwards. Nothing was
written to the live checkout, no `prd` op was run, no daemon was touched, and
the superproject was only read.

| # | command | cwd | exit / result |
| ---: | --- | --- | --- |
| 1 | `git log --oneline -3; git status --porcelain; git rev-parse HEAD` | `auth.ctg` | 0 — tip `dd35669`, tree clean |
| 2 | `git -C /Users/feb/dev/cartridge ls-tree HEAD auth.ctg` | super | 0 — gitlink `dd3566926bb…` |
| 3 | `git show dd35669 --stat`, `git show dd35669 -- src/openai.ts` | `auth.ctg` | 0 — `discover()` absent from the diff |
| 4 | `grep -rn 'src/main' .cartridge/tests/` | `base` | **1** — no baseline test imports `src/main.ts` |
| 5 | `bun install --frozen-lockfile`; `bun run check`; `bun test ./.cartridge/tests/` | `base` | 0 / **0** / **0** — 13 pass, 0 fail |
| 6 | `git apply --check attempt-1.patch` | `iso` | **0** |
| 7 | `git apply attempt-1.patch`; `git status --porcelain` | `iso` | 0 — exactly the 4 declared files |
| 8 | `bun install --frozen-lockfile`; `bun run check`; `bun test ./.cartridge/tests/` | `iso` | 0 / **0** / **0** — 15 pass, 0 fail |
| 9 | Verify block 1 verbatim, `sh -eu -c`, ≤120 s | `iso` | **0** (<1 s) |
| 10 | Verify block 2 verbatim, `sh -eu -c`, ≤120 s | `iso` | **0** — 15 pass, 0 fail (≈4 s) |
| 11 | Verify block 1 verbatim on unpatched `dd35669` | `base` | **1** |
| 12 | Verify block 2 verbatim on unpatched `dd35669` | `base` | 0 — 13 pass (block 2 alone is vacuous; block 1 is what makes the pair non-vacuous) |
| 13 | mutation: `close` closes outright (`if(false)`) | `iso` | **1** — 13 pass / 2 fail |
| 14 | mutation: relay drops `session_id` | `iso` | **1** — 14 pass / 1 fail |
| 15 | mutation: `send` does not forward | `iso` | **1** — 14 pass / 1 fail |
| 16 | restore; `bun test ./.cartridge/tests/` | `iso` | 0 — 15 pass / 0 fail |
| 17 | guard block vs. 6 broken trees: missing `node.ts`; mock on `0.0.0.0`; test reads `process.env`; test reads `homedir()`; bound 15000→0; provider destination → `wss://example.invalid/…` | `iso` | **1, 1, 1, 1, 1, 1**; restored tree **0** |
| 18 | safety mutation: fixture store seeded `sk-not-the-fixture-key` | `iso` | **1** — 0 pass / 2 fail, "OpenAI voice session connection failed" (mock refused the bearer) |
| 19 | `import.meta.main` probe: `bun <abs>/probe.ts` | scratch | 0 — `main= true` |
| 20 | `import.meta.main` under `bun test` (appended `console.error`) | `iso` | `MAIN_FLAG=false` — no stdin `Wire` during tests |
| 21 | entrypoint smoke: two frames piped into `bun src/main.ts` | `iso` | `{"id":1,"result":null}`, `{"id":2,"error":"Voice session is not attached"}` — handlers still register |
| 22 | F1 probe: instrumented stderr capture | `iso` | `STDERR_CAPTURE_LEN=0 CONTENT=[]`, 2 pass |
| 23 | F1 fix probe: one `id`-less failing call before the assertion | `iso` | capture non-empty (`…"msg":"auth.live failed: …"`), 2 pass |
| 24 | F2 probe: entrypoint line commented out | `iso` | guard **0**, suite **0** (15 pass), entrypoint stdout **empty** |
| 25 | F3 probe: bound 15000→150000 | `iso` | suite **0** (15 pass); guard **1** |
| 26 | `git status --porcelain` after every restore; `git worktree prune` | `iso`, `base`, `auth.ctg` | 0 — only the intended patch present; live checkout untouched |

Credential safety: no real credential was read, printed, copied, rotated or
spent. `~/.codex/auth.json`, the keychain, `security(1)` and
`.cartridge/credentials` were never opened; no request reached
`api.openai.com`, `auth.openai.com` or any real endpoint (the only network use
was `bun install --frozen-lockfile` against the package registry, and the
lockfile was already satisfied). The one probe that could have read a real store
— `auth {op:"status"}` on the live entrypoint — was deliberately **not** run,
because `discover()` reads `process.env` and `~/.codex/auth.json`; the smoke
used `apply` with an empty config and a bogus `auth.live` op instead. I hit no
safety-net block this round (the analyst's `secret.basename.credentials` block on
listing `.cartridge/credentials` was not re-attempted). The fixture's refusal
property was confirmed empirically, not assumed: a non-dummy key fails the test
rather than being used.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **FAIL — 89/100**, with one unresolved blocking finding.
Unresolved blocking findings: **F1** (the "no log line carries the key"
assertion is vacuous — captured stderr is empty).
Rounds used / remaining: 1 / 4.
Next action: bounded revision of `spec01.md` and `attempt-1.patch` — fix F1 and
F2 together (roughly four lines and one guard), then apply the F3–F7 wording;
re-present for round 2. Do not tick box 4 on the current revision.

## Round 2 — 2026-09-16

Presented revision: `auth.ctg` `dd3566926bb3402ed619884d02be9931429c462c`
(re-confirmed HEAD, `git status --porcelain` empty, `git worktree list` showing
only the live checkout; superproject gitlink `160000 commit dd3566926bb…`),
plus the unapplied prototype `attempt-2.patch`. No dirty files in `auth.ctg`.
`prd.md` is byte-identical to the round-1 digest — the revision touched the spec
and the prototype only, and no box was ticked.

| Input | Content digest (SHA-256) |
| --- | --- |
| Plan | `prds/…/prd.md` `3cf8a5e42f7d0c67f0bbe1592f0003899db3288c76808d25dad1fd1b63c7b402` (**unchanged from round 1**) |
| Specs | `prds/…/specs/spec01.md` `18f2b993150d421be17b84889a5c5274b838c9ade6203f16b8d723c474b9a960` (was `2fa7d698…`; byte-identical to the `.state/loop` draft — `diff` exit 0) |
| Prototype | `.state/loop/…/attempt-2.patch` `910c8f80036258f2e9c3a857f6c14801b5016121a36efc4dae0fc6e55dff51f6` (round-1 `attempt-1.patch` `4faffafd…` left intact, so the round-1 digest still resolves) |
| Source of record | `auth.ctg@dd35669 src/main.ts` `cee3ac9c620ef8214f41a7f15047a309002bef6c49b0e76964160b9be75dc998`; `src/openai.ts` `0a5ed13575e3e8e35b4d0fef79f3428a8e929a6400faa988e5be82a3964af1db` (both unchanged from round 1) |
| Material contracts | unchanged from round 1 (superproject `.cartridge/config.lua` `:59`/`:63`; `router.ctg` `service.rs`/`catalog.rs`/`auth.rs`/`settings.rs`; `auth.ctg/init.lua`, `cartridge.json`, `.gitignore`) |
| Revision record | `prds/…/analyst-2.md` `f10d9eee95edac277158ef3710187d379bbe3145f9b2f996ff0f4c6b4434fb5d` |

`attempt-2.patch` differs from `attempt-1.patch` in exactly two places
(`diff` of the two patches, 11 changed lines, all in the new `live.test.ts`
hunk): the `cleanup.push` of the stderr restore moves **above** the swap (F7),
and the `id`-less failing call plus `expect(errors.join("")).toContain("auth.live failed:")`
are added before the disclosure assertions (F1). No production line changed
between the two prototypes; the three `src/main.ts` lines are the same.

### F1 — the blocking finding — CLOSED, reproduced in both directions

Round 1's defect was that the box-4 clause "no log line carries the key" was
**vacuous**: captured stderr was `[]`, so `not.toContain(DUMMY)` passed because
nothing had ever logged. I re-ran the analyst's three probes myself on a private
scratch worktree, not on its say-so:

| probe | expectation | observed |
| --- | --- | --- |
| **A** — instrument the capture (`console.log` of `errors.length` and content, then reverted) | capture is genuinely non-empty | `STDERR_CAPTURE_LEN=1 CONTENT=["{\"t\":…,\"src\":\"wire\",\"msg\":\"auth.live failed: Voice session is not attached\"}\n"]`, file **2 pass / 0 fail** (round 1: `LEN=0 CONTENT=[]`) |
| **B** — leak mutation: `process.stderr.write(\`dialling ${url} as ${key}\`)` added to `OpenAIAuth.start()` (`src/openai.ts:139`) | the clause fails when a key-bearing line **is** logged | suite **exit 1**, failing exactly on `expect(errors.join("")).not.toContain(DUMMY)` — `Expected to not contain: "fixture-live-secret"`; 14 pass / 1 fail across the suite (1 pass / 1 fail for the file alone, which is the count `analyst-2` quotes) |
| **C** — delete the `id`-less call | the clause fails when the capture is empty, i.e. it is load-bearing | suite **exit 1**, 14 pass / 1 fail, failing on `expect(errors.join("")).toContain("auth.live failed:")` |

Restored tree after B and C: **exit 0**, 15 pass / 0 fail, **74** `expect()`
calls (13 pass / 55 expects at baseline). The clause now fails both when it has
nothing to be about and when a key-bearing line is present — which is exactly
what round 1 asked for, and what makes it a clause that *could* fail.

Two things I checked beyond the reported probes, because "assertion has a
subject" is easy to satisfy accidentally:

- **The diagnostic really comes from the wire's failure path, not from noise.**
  `Wire.answer`'s catch calls `diagnostic("wire", …)` (`src/wire.ts:19-21`,
  writing to `process.stderr`); the `id`-less frame has nowhere to reply, so the
  catch logs. The preceding failing call (line 108) carries an `id`, so it
  answers over the wire and logs nothing. Probe C confirms the `id`-less call is
  the **only** source: remove it and the capture is empty again.
- **The clause is robust to the close behaviour it sits behind.** The `id`-less
  call is placed after `close`, so today it fails with "Voice session is not
  attached". Had the session still been attached, `event:null` fails the
  `send` validation at `src/main.ts:60` instead — still a diagnostic, still
  prefixed `auth.live failed:`. The non-empty half does not silently depend on
  an unrelated behaviour.
- **The guard is pinned individually, not only by the whole block.**
  `analyst-2` ran block 1 against the unpatched base (exit 1), which fails for
  many reasons at once. I isolated it: delete **only** the
  `toContain("auth.live failed:")` line from an otherwise fully patched tree and
  Verify block 1 exits **1**. The new guard is what catches it.

### F2 — CLOSED, and the smoke is not a second grep

| tree | block 1 | block 2 | `bun test` | entrypoint stdout |
| --- | ---: | ---: | ---: | --- |
| patched, intact | **0** | **0** | 0 (15 pass) | `{"id":1,"result":null}` |
| `// if(import.meta.main) serve(new Wire());` | **1** | **1** | 0 (15 pass) | *(empty)* |
| entrypoint intact, `wire.on("apply",…)` deleted | **0** | **2** | — | ``{"id":1,"error":"`apply` is not served here"}`` |

Round 1's commented-out tree scored **0 / 0**; both gates now catch it. The
anchored `grep -qE '^if\(import\.meta\.main\) serve\(new Wire\(\)\);'` is what
fires in block 1, and the stdio smoke is what fires in block 2.

One correction to `analyst-2`'s reading of its own probe: on the dropped-`apply`
tree, block 2's exit **2** comes from `bun run check` (`tsc --noEmit`, four
`TS2454: Variable 'auth' is used before being assigned` errors), which under
`sh -eu` aborts the block **before** the smoke runs. So that particular exit
code is not evidence for the smoke. I therefore ran the smoke line **on its
own** against the same tree: `printf '{"id":1,"call":"apply","args":{}}' |
bun src/main.ts | grep -q '"id":1,"result":'` exits **1** on the dropped-`apply`
tree and **0** on the restored one. The claim holds — the smoke independently
distinguishes a registered handler from an inert one — but it holds for a
different reason than the report gives. Non-blocking; noted as F8 below.

**The smoke reads no credential, confirmed from source rather than assumed.**
`OpenAIAuth`'s constructor body is empty (`src/openai.ts:57`
`constructor(private config: AuthConfig = {}, private deps: Dependencies = {}) {}`),
and `discover()` (`:57`) is called from exactly two places — `status()` (`:111`)
and `create()` (`:116`). `apply` does nothing but `auth = make(config ?? {})`
(`src/main.ts:10`), and `args:{}` supplies no `credentials_dir`, `codex_home` or
`router_data_dir`. So block 2 in the **live** checkout reads no store, no
environment key and no `~/.codex/auth.json`. This is the same `apply`-plus-bogus-op
shape round 1 used deliberately in place of `auth {op:"status"}`, and I kept to
it: **`auth {op:"status"}` was not run against any entrypoint this round.**

### F3–F7 — each checked against the spec text and, where it makes a claim, re-measured

| # | where it landed | verified |
| ---: | --- | --- |
| **F3** | `## Remaining risk`, bullet 2 — the bound is "pinned downward by behaviour and upward only by a literal", with the upgrade path (a test-visible constant) | Re-measured: `15000`→`150000` leaves the suite at **exit 0, 15 pass**, and Verify block 1 exits **1** on the `setTimeout` literal alone. The spec's description of the residual is accurate, not softened. |
| **F4** | Step 1 reworded to "No behaviour change in any handler; `apply` constructs through `make` … and `auth`'s declared type widens from `OpenAIAuth` to `LiveAuth`, which `tsc --noEmit` accepts because only `LiveAuth` members are used" | Matches the patch (`let auth:LiveAuth`, `auth=make(config ?? {})`); `bun run check` exit 0 on the patched tree. |
| **F5** | `## Remaining risk`, bullet 1 — the router leg, the three silent breakers (router's `config_dir`, the `{KEY}_API_KEY` naming, the two processes resolving the **relative** `.cartridge/credentials` differently), that the auth side is guarded by `auth.test.ts:24-30` and the router side cannot be guarded from this footprint, and where a guard belongs | Text matches the chain I re-derived in round 1, including the relative-path clause F5 specifically asked for. |
| **F6** | The `CARGO_TARGET_DIR` sentence is gone; the `## Verify and Proof` preamble now names `node_modules/` from `bun install --frozen-lockfile` as what pass 2 writes into the live checkout, and why it is safe | Re-verified the two load-bearing facts: `auth.ctg/.gitignore` line 1 is `/node_modules/`, and `node_modules/` is outside the PRD footprint (`src/**`, `.cartridge/**`, `cartridge.json`, `init.lua`), so `prd collect`'s dirty-footprint sweep cannot pick it up. The preamble also records that the smoke's process reads stdin, answers and exits, touching no daemon — which I confirmed by running it. |
| **F7** | **Scoped and noted.** `live.test.ts:68-70`: `const write = process.stderr.write.bind(…)`, then `cleanup.push(() => { process.stderr.write = write; })`, then the swap. Step 4 records why. | Read in the applied patch; the ordering is exactly as described, and it is the only difference between `attempt-1` and `attempt-2` outside the F1 lines. |

Acceptance clause 5 in the spec was also strengthened to require the capture be
"known to be non-empty", so the box an implementer ticks is the one F1 makes
checkable. The spec's two ```sh blocks are the blocks I ran: I extracted them
from `spec01.md` with `awk` and executed the extracted files verbatim under
`sh -eu -c`, which is a stronger check than diffing against the analyst's
private copies — every exit code below is the spec's own text.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Unchanged and still correct: one slice closes boxes 2 and 4 together — 3 production lines, ~160 test lines, 4 files, every path inside the declared footprint. Round 1's only deduction (F4, step 1's inaccurate "No handler body changes") is reworded verbatim as recommended, and the reworded text matches the patch. No scope drift between rounds: `prd.md`'s digest is byte-identical, no box was ticked, and the patch's production diff is unchanged from `attempt-1`. |
| Ownership and reuse | 20 | Unchanged: owner matches `repo:`, nothing written outside `auth.ctg`, `Wire(input,output)` and `deps.socket` reused rather than invented, `node()` *moved* (I diffed the `wire.test.ts` hunk — the twenty-five lines are lifted verbatim, gaining only a defaulted `serve` argument), `Bun.serve` in place of a dependency (`bun install --frozen-lockfile` exit 0, "no changes"). Round 1's deduction (F5, the unguarded router leg recorded nowhere the implementer reads) is closed by a `## Remaining risk` bullet that names all three breakers and the two places a guard could live. |
| Dependencies and implementable slices | 20 | `git apply --check attempt-2.patch` exit **0** on a pristine `dd35669` worktree; `git apply` exit **0**; `git status --porcelain` afterwards is exactly the four declared files and nothing else. No `needs`, no cross-cartridge ordering. Both Verify blocks obey the engine facts: repo-root-relative paths, no `cd`, no absolute checkout, no cargo (so no `CARGO_TARGET_DIR`), and each finishes in **≤1 s** against the 120 s limit. Round 1's deduction (F6) is closed with a rationale whose two facts I re-verified rather than accepted. |
| Observable acceptance and baseline evidence | 19 | Every reported number reproduces: baseline 13 pass / 55 expects, patched 15 pass / 74 expects, `bun run check` 0 both, block 1 **0** patched and **1** unpatched, block 2 **0** patched. The three shipped-code mutations each fail — `close` closing outright **exit 1, 13 pass / 2 fail**; relay dropping `session_id` **exit 1, 14 / 1**; `send` not forwarding **exit 1, 14 / 1** — and the restored tree returns to **exit 0, 15 / 0**. The F1 clause is now proven load-bearing in both directions (probes B and C above) and individually guarded. No guard is `!`-prefixed (both negatives are `if grep -qn …; then exit 1; fi`, and I confirmed the `process.env` one fires: introducing `process.env` into `live.test.ts` takes block 1 to **1**), and all four referenced paths are `test -f` guarded. −1: the 15 s bound is still pinned upward by a `grep` on a literal only — `15000`→`150000` passes the suite 15/0. This is now **honestly recorded** as a deliberate trade with its upgrade path rather than presented as proven, which is what F3 asked for, but it remains an evidence gap rather than a closed one. |
| Failure, recovery and compatibility | 19 | Isolation re-verified by reading the applied file, not the report: `env: {}`, a `mkdtempSync` home, `credentials_dir` pointed at that temp directory through `apply`, `fetch` a thrower, `socket` dialling `ws://127.0.0.1:<ephemeral>`, and the mock's `fetch` returning 401 unless `authorization === "Bearer fixture-live-secret"`. **The refusal property still holds after the revision** — seeding the fixture store with `sk-not-the-fixture-key` gives **exit 1, 0 pass / 2 fail**, "OpenAI voice session connection failed", so a real key fails the test instead of being spent. F7 is scoped as recommended (restore pushed onto `cleanup` before the swap, so no throw can leave the process's stderr wrapped) and noted in step 4. The seam's compatibility is unchanged from round 1 and now additionally proven by the stdio smoke inside the Verify block itself. −1: two residuals remain open rather than closed — the stderr capture is still process-global for the duration of each test (the reorder removes the leak-on-throw, not the sharing; it is safe only because `bun test` runs files sequentially in one process), and the F5 router leg is recorded but has no tracked follow-up on router's board or a `needs` edge, so the one unguarded contract in this PRD still depends on someone reading the spec's risk section. |
| **Reviewer total** | **98 / 100** | At or above the 90 threshold, with no blocking finding. |

### Findings

| # | Finding | Evidence | Recommendation |
| ---: | --- | --- | --- |
| **F1** | **CLOSED.** The disclosure clause now asserts against a capture proven non-empty, and fails in both directions. | Probe A `STDERR_CAPTURE_LEN=1` with a real `auth.live failed:` wire line; probe B (key-bearing write in `OpenAIAuth.start()`) suite exit 1 on `not.toContain("fixture-live-secret")`; probe C (`id`-less call removed) suite exit 1 on `toContain`; new block-1 guard isolated — deleting only that assertion takes block 1 to exit 1. | None. Do not remove the `id`-less call without replacing the subject it creates. |
| **F2** | **CLOSED.** Both gates now reject a commented-out entrypoint, and the smoke is behavioural rather than textual. | Commented-out tree: block 1 **1**, block 2 **1** (was 0 / 0), suite still 15/0, entrypoint stdout empty. Dropped-`apply` tree: smoke line alone exits **1**; restored **0**. | None. |
| **F3–F7** | **CLOSED as recommended.** F3 and F5 as `## Remaining risk` bullets, F4 as reworded step 1, F6 as the `node_modules/` rationale, F7 scoped in the patch and noted in step 4. | See the table above; each claim re-measured or re-read against the applied tree. | None. |
| **F8** | **Non-blocking, record accuracy.** `analyst-2` cites block 2's exit **2** on the dropped-`apply` tree as evidence that "the smoke is not merely a second grep". That exit comes from `tsc --noEmit` failing first under `sh -eu`; the smoke never runs in that block. | Block 2 log on that tree ends at `$ tsc --noEmit` with four `TS2454` errors. Running the smoke line alone on the same tree gives the intended **exit 1**. | The conclusion is right, the cited evidence is not. If the report is carried forward, cite the standalone smoke run instead. No change to the spec or the patch is needed — the guard behaves as claimed. |
| **F9** | **Non-blocking, follow-up.** The F5 residual is now written down but not tracked: no PRD on router's board and no `needs` edge exists for the composed `router login` → `auth {op:"status"}` guard the spec names. | `## Remaining risk` bullet 1 names the guard's home but nothing references it. | Coordinator's call after this PRD lands: open a small leaf on router's board for the composed guard, or accept the inspection-only contract explicitly. Not a condition of this gate. |

Disposition: **keep** — the plan, the seam and `attempt-2.patch` are ready to
implement as written. No split, merge, rehome or retire.

Box recommendations to the coordinator, unchanged from round 1 and re-confirmed
against the same commit: **box 1 holds**, **box 3 holds** by inspection with the
router leg unguarded, **box 4's untick is correct**, and box 2 is implemented
and unproven. Nothing here ticks a box; boxes 2 and 4 become tickable once
`attempt-2.patch` lands and its Verify blocks are collected. The Planning note
still needs no correction.

Validation: all commands run in two private detached scratch worktrees of
`auth.ctg` at `dd35669`, created under a **private subdirectory** of this
session's scratchpad (`…/scratchpad/rev2-review-gptlive/{base,iso}`) so no other
agent's block files could be reused or overwritten. Both Verify blocks were
extracted from `spec01.md` by `awk` and executed verbatim as `sh -eu -c "$(cat
block.sh)"`, each bounded to 120 s by `perl -e 'alarm 120; exec @ARGV'` (neither
`timeout(1)` nor `gtimeout(1)` exists on this machine). Nothing was written to
the live checkout, no `prd` op was run, no board state changed, no commit, no
`git add`, no push, and the live project daemon was neither started, stopped,
replaced nor reloaded. Both worktrees were removed with `rm -rf` plus
`git worktree prune` (`git worktree remove --force` was not attempted — it is
rule-blocked); `git worktree list` afterwards shows only the live checkout, and
`auth.ctg` is clean at `dd35669`.

| # | command | cwd | exit / result |
| ---: | --- | --- | --- |
| 1 | `git rev-parse HEAD; git status --porcelain; git worktree list` | `auth.ctg` | 0 — `dd3566926bb…`, clean, only the live checkout registered |
| 2 | `git ls-tree HEAD auth.ctg` | super | 0 — gitlink `dd3566926bb…` |
| 3 | `shasum -a 256` on plan, spec, both patches, `analyst-2.md`, `src/main.ts`, `src/openai.ts` | board / `auth.ctg` | 0 — digests as tabled; plan and sources unchanged from round 1 |
| 4 | `diff specs/spec01.md .state/loop/…/spec01.md` | board | **0** — published spec and draft byte-identical |
| 5 | `diff attempt-1.patch attempt-2.patch` | `.state/loop` | 1 — 11 changed lines, all in the `live.test.ts` hunk (F1 + F7); no production line differs |
| 6 | `git worktree add --detach …/{iso,base} dd35669` | `auth.ctg` | 0 / 0 |
| 7 | `bun install --frozen-lockfile`; `bun run check`; `bun test ./.cartridge/tests/` | `base` | 0 / 0 / **0** — 13 pass, 0 fail, 55 expects |
| 8 | `grep -rn 'src/main' .cartridge/tests/` | `base` | **1** — still no baseline test imports `src/main.ts` |
| 9 | Verify block 1 verbatim (`sh -eu -c`, ≤120 s) | `base` | **1** (<1 s) |
| 10 | Verify block 2 verbatim (`sh -eu -c`, ≤120 s) | `base` | **0** (1 s, 13 pass) — block 2 alone stays vacuous on an unpatched tree; block 1 is what discriminates |
| 11 | `git apply --check attempt-2.patch` | `iso` (pristine) | **0** |
| 12 | `git apply attempt-2.patch`; `git status --porcelain` | `iso` | 0 — exactly the 4 declared files |
| 13 | `bun install --frozen-lockfile`; `bun run check`; `bun test ./.cartridge/tests/` | `iso` | 0 / **0** / **0** — 15 pass, 0 fail, **74** expects |
| 14 | Verify block 1 verbatim | `iso` | **0** (<1 s) |
| 15 | Verify block 2 verbatim | `iso` | **0** (1 s, 15 pass) |
| 16 | F1 probe A: instrumented capture, `bun test …/live.test.ts` | `iso` | 0 — `STDERR_CAPTURE_LEN=1`, real `auth.live failed:` line, 2 pass |
| 17 | F1 probe C: `id`-less call deleted; `bun test ./.cartridge/tests/` | `iso` | **1** — 14 pass / 1 fail on `toContain` |
| 18 | F1 probe B: key-bearing `process.stderr.write` in `OpenAIAuth.start()`; `bun test ./.cartridge/tests/` | `iso` | **1** — fails on `not.toContain("fixture-live-secret")`, 14 pass / 1 fail |
| 19 | restore; `bun test ./.cartridge/tests/` | `iso` | **0** — 15 pass / 0 fail |
| 20 | F1 guard isolated: delete only `toContain("auth.live failed:")`; Verify block 1 | `iso` | **1** |
| 21 | F2 probe: `// if(import.meta.main) serve(new Wire());` → block 1 / block 2 / suite / entrypoint stdio | `iso` | **1** / **1** / 0 (15 pass) / *(empty stdout)* |
| 22 | restore entrypoint; block 1 / block 2 | `iso` | **0** / **0** |
| 23 | inert-registration probe: `wire.on("apply",…)` deleted → block 1 / block 2 / entrypoint stdio | `iso` | **0** / **2** (from `tsc`, see F8) / ``{"id":1,"error":"`apply` is not served here"}`` |
| 24 | smoke line alone on the dropped-`apply` tree, then on the restored tree | `iso` | **1** / **0** — the smoke discriminates on its own |
| 25 | F3 probe: `setTimeout(…,15000)`→`150000`; suite / block 1 | `iso` | **0** (15 pass) / **1** |
| 26 | negative-guard probe: `process.env` introduced into `live.test.ts`; block 1 | `iso` | **1** |
| 27 | mutation: `close` closes outright (`if(false)`) | `iso` | **1** — 13 pass / 2 fail |
| 28 | mutation: relay drops `session_id` | `iso` | **1** — 14 pass / 1 fail |
| 29 | mutation: `send` does not forward | `iso` | **1** — 14 pass / 1 fail |
| 30 | safety mutation: fixture store seeded `sk-not-the-fixture-key`; `bun test …/live.test.ts` | `iso` | **1** — 0 pass / 2 fail, "OpenAI voice session connection failed" (mock refused the bearer) |
| 31 | restore everything; `bun test ./.cartridge/tests/`; `diff` against saved originals; `git status --porcelain` | `iso` | **0** — 15 pass / 74 expects, files identical, only the 4 intended paths |
| 32 | `cat .gitignore`; footprint comparison | `iso` | `/node_modules/` on line 1, outside the PRD footprint — F6's rationale holds |
| 33 | `rm -rf …/{iso,base}`; `git worktree prune`; `git worktree list`; `git status --porcelain`; `git rev-parse HEAD` | `auth.ctg` | 0 — only the live checkout, clean, `dd35669` |

Credential safety: no real credential was read, printed, copied, rotated or
spent. `~/.codex/auth.json`, the macOS keychain, `security(1)` and
`.cartridge/credentials` were never opened or invoked; no request reached
`api.openai.com`, `auth.openai.com` or any real endpoint. The only network use
was `bun install --frozen-lockfile` against the package registry, with the
lockfile already satisfied ("Checked 5 installs across 6 packages (no changes)").
Following round 1, **`auth {op:"status"}` was deliberately not run against any
entrypoint**, because `discover()` reads `process.env` and `~/.codex`; every
entrypoint probe used `apply` with an empty config — whose handler only
constructs, as shown from source above — and, where an error answer was wanted,
a bogus op. The single credential literal anywhere in this round is the
fixture's `fixture-live-secret` plus the fabricated `sk-not-the-fixture-key`
used to re-confirm the mock's refusal property. I hit **no safety-net block**
this round; the two the analyst hit (`sh -eu $P/block1.sh` unverifiable-source,
and `git.worktree-remove-force`) I avoided rather than re-triggered — blocks
were run as `sh -eu -c "$(cat …)"` and worktrees removed with `rm -rf` plus
`git worktree prune`.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not required under delegation; none supplied.
User feedback/provenance: none this round.
Result: **PASS — 98/100**, with no unresolved blocking finding.
Unresolved blocking findings: **none**.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation of `spec01` from `attempt-2.patch` on
`auth.ctg` `dd35669`; tick boxes 2 and 4 only after the work lands and its
Verify blocks collect green. F8 (a citation in `analyst-2.md`, not in the plan)
and F9 (a follow-up leaf for the router leg) are the coordinator's to dispose of
and gate nothing. This rating binds to spec01
`18f2b993150d421be17b84889a5c5274b838c9ade6203f16b8d723c474b9a960` and
`attempt-2.patch`
`910c8f80036258f2e9c3a857f6c14801b5016121a36efc4dae0fc6e55dff51f6`; a
substantive change to either makes it stale and needs round 3.
