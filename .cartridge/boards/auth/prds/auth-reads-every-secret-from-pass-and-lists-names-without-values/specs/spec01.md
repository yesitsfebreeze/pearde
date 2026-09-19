---
complexity: medium
footprint:
  - src/pass.ts
  - src/insert.ts
  - src/openai.ts
  - src/main.ts
  - cartridge.json
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/README.md
  - .cartridge/tests/integration/pass.test.ts
---

# spec01 (r4) — auth owns a pass-layout store under `~/.cartridge/auth`, fills it through one stdin door, and answers status and list with names only

Revision 4 is r3 with the round-2 findings N1-N7 applied. The coordinator
dropped the `password_store_dir` opt-in (N1): auth reads only its own store.

Base: `auth.ctg` at `d8751088bb8b0884ff641e027855d82257ee8ff0`. At that sha
discovery is one private, synchronous, OpenAI-only method
(`src/openai.ts:57-110`), the `auth` handler refuses everything but `status`
for `openai`/`live` (`src/main.ts:11-14`), and the manifest requires `op`,
`provider` and `capability` (`cartridge.json:10-14`), lists one `op`
(`:18-20`) and grants `exec: ["bun"]`, `read: ["/"]`, `net`, no `write`
(`:132-142`).

## Why this design (moved from the PRD's Decision)

- **No value travels in an event, in or out.** The transport keeps the last
  envelopes of every channel in memory (`HISTORY`, pushed in
  `cartridge.ctg/src/transport/cartridge.rs:474-486`), and the ASP ring will
  keep every published envelope on disk. So auth delivers a secret in only
  two ways: it makes the authenticated call itself, as `auth.live` does, or
  it writes a derived file for a consumer that must hold the key in its own
  process (@auth/auth-writes-the-router-s-credential-file-from-pass). A value
  enters only through the insert door, run by a person outside the daemon.
- **Superseded first design.** r1 read the person's own `~/.password-store`
  with their own `~/.gnupg`, and the grant gained `exec: ["gpg"]` and nothing
  else. The probe showed that the sandboxed node then cannot start gpg-agent
  or keyboxd (no write on the gpg home) and needs a login-time agent, a gpg
  key, `pass init` and `pinentry-mac` set up by hand. The user replaced it on
  2026-09-19 ("The harness or the agent itself … can hold its own settings
  and its own pass integration rather than tying it to the user"). The
  opt-in back to the person's store was then dropped: nobody asked for it.
- **State directory.** `~/.cartridge/auth/` holds `store/` (pass layout) and
  `.gnupg/`. `~/.cartridge` is the host's per-user home: trust store and
  catalog live there (`cartridge.ctg/src/trust/mod.rs:19-37`,
  `src/cli/args.rs:41`). The documented state convention is the project's
  `.cartridge/<folder>` (`cartridge.ctg/docs/creating-cartridges.txt:195-200`);
  this departs from it on purpose, because a secret store must not sit in a
  git checkout and one person's keys serve every project. Grants expand
  `$HOME`, `$PROJECT`, `$TMPDIR`, `${config.<key>}`
  (`cartridge.ctg/src/host/plan.rs:225-268`), not `$CARTRIDGE_HOME`, so the
  code derives the directory from `HOME` only.
- **gpg creates its own home.** auth runs gpg with `HOME=~/.cartridge/auth`
  and no `GNUPGHOME`, so gpg treats `~/.cartridge/auth/.gnupg` as its default
  home and creates it `0700` with `common.conf` = `use-keyboxd`, as a real
  `~/.gnupg` has. A `GNUPGHOME` naming a missing directory is not created by
  gpg (probe below). Socket paths on this machine: `…/.gnupg/S.gpg-agent` 45
  bytes, `…/S.keyboxd` 43; `sun_path` holds 104.

## Acceptance

Each box is one PRD Acceptance box, in order.

- [x] **PRD 1.** The named test `a stored entry decrypts inside the process and the value reaches only the authenticated call` stores `cartridge/openai/api-key` in a fixture gpg home reached through `HOME`, sets `OPENAI_API_KEY` in the injected environment as well, and observes the stored value as the `Authorization` bearer of auth's own session request (so pass comes first), and in no response or frame. `cartridge.json` carries exactly the manifest delta below.
- [x] **PRD 2.** The named test `the insert door round-trips a value that status reports as source pass without the value` pipes a value to the door on stdin, then gets `state:"available_unverified"`, `source:"pass"`, `entry:"cartridge/typesafe/api-key"` and no value from `auth {op:"status", provider:"typesafe"}` over the wire; the door's stdout and stderr do not contain the value, and it refuses an empty value and a whitespace-only value with `A secret value is required on stdin` and writes no entry. The named test `a provider or field name cannot leave the cartridge subtree` gets a refusal for `provider:"../x"`, `field:"a/b"`, `provider: 5` and a non-string `field`, treats `field: null` as `api-key`, from both the wire and the door, and gpg is never spawned for the refusals.
- [x] **PRD 3.** The named test `list returns every cartridge entry and no response or frame carries the value` kills the owned home's keyboxd and agent (`gpgconf --kill all` through the wrapper), sends `auth {op:"list"}` over the wire, gets one `{name, provider, field, available: true}` row per valid `cartridge/**` entry (cold, concurrent), none for an entry outside `cartridge/` and none for `cartridge/Bad Name/`, and asserts that the concatenation of every response, every loose frame and every captured diagnostic line is non-empty and contains no fixture value.
- [x] **PRD 4.** The named test `first use creates the store and the key with 0700 modes` finds `.cartridge/auth`, `.cartridge/auth/store` and `.cartridge/auth/.gnupg` at mode `0700`, `common.conf` in the gpg home, one `sec` line in the secret-key census, and both socket paths under 100 bytes. The named test `a read on a home with no store reports a missing entry and creates nothing` gets `state:"missing_entry"` whose message names the absolute path of `src/insert.ts`, and `list` `[]`, and `.cartridge` does not exist afterwards. The named test `gpg missing and no answer and refused are three bounded diagnostics` gets `gpg_missing`, `no_answer` (under 3000 ms on an injected 1000 ms bound) and `refused`, with three different messages.
- [x] **PRD 5.** `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` each describe the layout, the insert door, the public states and the two delivery rules; the docs name who else can read the key.

The 15 base tests still pass with their files unmodified; the `test` block
pins three of them by name.

## Manifest delta (`cartridge.json`)

```json
"grant": {
  "exec": ["bun", "gpg"],
  "read": ["/"],
  "write": ["$HOME/.cartridge/auth/.gnupg"],
  "net": ["api.openai.com"]
}
```

- `write` is the gpg home only (N3). gpg needs it to start keyboxd and
  gpg-agent. The node never writes into `store/`: the door is the only
  writer and runs outside the sandbox. The reviewer probed this grant: a
  sandboxed cold decrypt exited 0 with keyboxd and the agent started inside
  the sandbox, and a sandboxed encrypt into `store/` exited 2,
  `Operation not permitted`. A grant path that does not exist yet (before
  the first insert) is kept and rendered through its deepest existing
  ancestor (`cartridge.ctg/src/sandbox/mod.rs:17-45`).
- `exec` stays `["bun","gpg"]`. keyboxd is at `<prefix>/libexec/keyboxd`, not
  on `PATH`, so a grant naming it would resolve to nothing
  (`mod.rs:151-180`). keyboxd and gpg-agent are admitted by the
  install-prefix rule (`mod.rs:121-139`, `:247-265`),
  `/opt/homebrew/Cellar/gnupg/2.5.21` here. The docs state that requirement.
- No `grant.env`, no settings. The code reads only `HOME` and `PATH`, which
  the host passes (`cartridge.ctg/src/host/process.rs:22-35`).
- `events.auth.schema`: `required` becomes `["op"]`, the `op` enum becomes
  `["status","list"]`, `field` is added as a string property. The manifest
  and `auth` `description` strings say any provider, names without values.
  No wording claims auth is the only holder of secrets (N4).

## Public states

`AuthStatus.state` is exactly one of:

| state | meaning |
| --- | --- |
| `available_unverified` | a credential was found (pass or a legacy store); validity is checked when used |
| `missing_api_key` | openai only: no credential in any checked store |
| `missing_entry` | auth's store has no `cartridge/<provider>/<field>` |
| `gpg_missing` | gpg is not on `PATH` (`error.code === "ENOENT"`) |
| `no_answer` | gpg gave no answer within the bound and was killed (`error.killed`) |
| `refused` | gpg exited non-zero for any other reason |

Messages name only paths and entry names, never gpg's stderr. `<insert>` is
`join(import.meta.dir, "insert.ts")`, an absolute path (N6).

- `missing_entry`: `No entry <name> in <store>. Add it with: bun <insert> <provider> [field] < value`
- `gpg_missing`: `gpg is not on PATH; auth needs GnuPG to read <name>.`
- `no_answer`: `gpg gave no answer for <name> within <n> ms and was stopped.`
- `refused`: `gpg refused to decrypt <name>; run gpg --decrypt on the entry with HOME=<home> in a terminal to see why.`

## Steps

1. `src/pass.ts` (new; `node:fs`, `node:path`, `node:os`,
   `node:child_process`, `node:util` only):
   - `type PassDeps = { env?: Record<string,string|undefined>; home?: string; timeoutMs?: number }`.
   - `place(deps)`: `{ state: <home>/.cartridge/auth, store: <state>/store }`,
     `home` from `deps.home ?? homedir()`. Every gpg call gets
     `env: { PATH: env.PATH, HOME: state }` and nothing else, never
     `GNUPGHOME`. A test that injects `home` cannot reach the real `~/.gnupg`.
   - `entry(provider, field)`: `provider` must be a string; `field` a string
     or `undefined`/`null` (meaning `api-key`); both parts match
     `/^[a-z0-9][a-z0-9._-]*$/`; anything else throws
     `Invalid provider or field name`. The name becomes a path; this is the
     trust boundary.
   - `read(name, deps): Promise<{ ok: true; value: string } | { ok: false; state: PassFailure; message: string }>`,
     `type PassFailure = "missing_entry" | "gpg_missing" | "no_answer" | "refused"`.
     `missing_entry` when `<store>/<name>.gpg` is not a file, which covers a
     store that does not exist yet (first use is normal; a read creates
     nothing). **gpg is spawned only after the entry file exists**, so every
     base test, all on an empty temporary `home`, stays away from gpg.
     Decrypt: `promisify(execFile)("gpg", ["--batch","--quiet","--no-tty","--decrypt", file], { timeout: deps.timeoutMs ?? 5000, encoding: "utf8", env })`,
     asynchronous because this process also relays live audio. The value is
     the first line of stdout under the rule of `src/openai.ts:63`. Rejection:
     `error.code === "ENOENT"` is `gpg_missing`, `error.killed` is
     `no_answer`, anything else is `refused`.
   - `available(name, deps)`: the same checks, but gpg runs as
     `spawn("gpg", [same args], { stdio: "ignore", timeout, env })` awaited
     on `close`/`error`, so no plaintext enters the process. `-o /dev/null`
     does not work: gpg writes `/dev/null.part` and fails (probed).
   - `list(deps)`: `readdirSync(join(store, "cartridge"), { recursive: true })`,
     keep exactly `<provider>/<field>.gpg`, drop any whose parts make
     `entry()` throw, return `{ name, provider, field, available }` from
     `available()`, all in one `Promise.all`. No store gives `[]`.
   - `insert(name, value, deps)`: applies the `src/openai.ts:63` rule to
     `value` and throws `A secret value is required on stdin` when it yields
     "" (N7). It refuses when `<state>/.gnupg/S.keyboxd` is 100 bytes or
     longer, creates `<state>`, `store/` and the entry's directory with
     `mkdirSync(..., { recursive: true, mode: 0o700 })`, does **not** create
     `.gnupg` (gpg does, with `common.conf`), generates the key when
     `gpg --batch --quiet --no-tty --list-secret-keys --with-colons` prints
     no `sec` line
     (`--batch --quiet --no-tty --pinentry-mode loopback --passphrase "" --quick-generate-key "cartridge auth <auth@cartridge.invalid>" default default never`;
     `ed25519 default` makes a sign-only key), then encrypts with
     `--batch --yes --quiet --no-tty --trust-model always -r auth@cartridge.invalid -e -o <file>`,
     the value on the child's stdin, never an argument.
2. `src/insert.ts` (new, about 15 lines): the one door.
   `bun src/insert.ts <provider> [field]`, value on stdin, first line. It
   calls `entry` then `insert`, prints `pass:<name>` and nothing else, and
   exits non-zero with the public message on refusal. It works before the
   daemon has ever run.
   `// ponytail: a terminal echoes a typed value; the docs pipe it (pbpaste | bun src/insert.ts typesafe). Add a no-echo prompt if people type keys.`
3. `src/openai.ts`: `Dependencies` gains `timeoutMs?: number`; `AuthStatus`
   becomes
   `{ provider: string; capability?: "live"; configured: boolean; state: "available_unverified" | "missing_api_key" | PassFailure; source: string | null; entry?: string; chatgpt_login?: boolean; checked: string[]; issues: string[]; message: string }`.
   `discover()` becomes `async` and tries `read(entry("openai"))` before the
   environment step, pushing `pass:cartridge/openai/api-key` onto `checked`;
   `ok` is the first candidate with `source:"pass"` and
   `entry:"cartridge/openai/api-key"`; `gpg_missing`, `no_answer` and
   `refused` push their message onto `issues`; `missing_entry` pushes
   nothing, so the base test `an absent default store is not an issue…`
   stays green. The `missing_api_key` message becomes
   `No OpenAI Platform API key was found in the checked stores. Add it with: bun <insert> openai < value, or OPENAI_API_KEY in the shared credential store.${trouble}`.
   `LiveAuth` becomes `status(provider?: string, field?: string | null)` plus
   `list()`. `status()`, `status("openai")` and `status("openai","api-key")`
   are today's answer plus the pass step; any other field or provider is
   answered from `read` alone as
   `{ provider, configured: ok, state: ok ? "available_unverified" : failure.state, source: ok ? "pass" : null, entry, checked: ["pass:" + entry], issues: [], message }`,
   because the legacy stores hold only the OpenAI API key.
4. `src/main.ts:11-14`: `op:"list"` returns `auth.list()`; `op:"status"`
   returns `auth.status(args.provider, args.field)` and lets `entry()`'s
   refusal propagate; anything else throws
   `Supported requests: status {provider, field?} and list`. No insert op.
5. `cartridge.json`: the manifest delta above.
6. `.cartridge/tests/integration/pass.test.ts` (new), reusing `node()` and
   `serve` as `live.test.ts` does.
   - One wrapper `gpg(home, cmd, args, input?)` for every gpg and gpgconf
     call: `spawnSync(cmd, args, { env: { PATH: process.env.PATH, HOME: home }, input, encoding: "utf8", timeout: 60000 })`,
     throwing on non-zero exit. It sets `HOME`, never `GNUPGHOME`, and asserts
     once per home that `gpgconf --list-dirs homedir` answers
     `<home>/.gnupg`, so no call can reach the person's `~/.gnupg` or kill
     their agent. Cleanup runs `gpgconf --kill all` through it (probed: it
     reaps keyboxd and gpg-agent) before `rmSync`.
   - One fixture per file in `beforeAll`: an owned home
     `mkdtempSync("/tmp/ca-")` filled through the door subprocess (the
     `.cartridge/auth` state under it is the `HOME` the wrapper and `read`
     use) with `openai/api-key`, `typesafe/api-key`, a `store/other/x.gpg`
     outside `cartridge/` and an empty `store/cartridge/Bad Name/`. Never
     `tmpdir()`; the fixture asserts both socket paths are under 100 bytes.
   - Failure states without a second home (N1): stub directories
     `mkdtempSync("/tmp/cs-")` holding a `chmod 755` `gpg` that runs
     `sleep 20` (`no_answer`, `timeoutMs: 1000`) or `exit 2` (`refused`),
     reached by `env: { PATH: <stub dir>:/bin }`; `gpg_missing` uses
     `PATH: "/nonexistent-bin"`. Probed under bun: `execFile` resolves `gpg`
     from the child `env.PATH`, giving `ENOENT` in 4 ms, `killed:true` at
     1007 ms and exit `2` in 118 ms respectively.
   - The `list` test runs `gpgconf --kill all` on the owned home through the
     wrapper first, then asserts every valid row `available: true` (N5).
   - Measured components (sandboxed probe): key generation 609 ms, encrypt
     17 ms, cold decrypt starting keyboxd and agent 976 ms, warm decrypt
     12 ms, cold key census 784 ms. One home and about fifteen gpg calls put
     the suite near 5 s; the implementer records the actual wall time in the
     evidence note against the 120 s block limit
     (`prd.ctg/src/lifecycle.ts:93,111`). Each test takes `60000` as its
     third argument. A missing `gpg` throws in the fixture; nothing skips.
   - For the disclosure clause the test swaps `process.stderr.write` as
     `live.test.ts` does (restore pushed before the swap), drives one
     `id`-less failing `auth` call and asserts the capture contains
     `auth failed:`.
7. Docs, same change: `README.md` and `.cartridge/help.md` replace "This is
   the only request it accepts" with the `status` and `list` forms and the
   door. `.cartridge/docs/README.md` puts pass at position 1 of the
   precedence list, adds the operations to the contract table, and states
   the layout, the state directory and modes, the door, the states table,
   the two delivery rules, that `pass:cartridge/typesafe/api-key` is safe to
   write into a profile, the install-prefix requirement for gpg's helpers,
   and the protection statement with the readers named in Remaining risk.
   "This implementation doesn't query the OS keychain" stays.
8. The implementer runs two mutants by hand and records both exits: `list`
   no longer dropping paths `entry()` refuses (the `Bad Name` row appears),
   and pass moved after the environment step in `discover()`. Each must turn
   the suite red.

## Probe results the design rests on

gpg 2.5.21, bun 1.3.14, 2026-09-19. Profile from
`cartridge.ctg/src/sandbox/mod.rs:231-338` for auth's grant: `deny default`,
`process-exec` for bun, gpg and gpg's install prefix, `file-read*` on `/`,
`network*`, `file-write*` on `/dev/null` plus the directory named.
`GNUPGHOME` unset, `HOME` = the state directory, nothing pre-running.

| Write grant | Action from sandboxed bun | Exit | Time |
| --- | --- | --- | --- |
| state | first use: gpg creates `.gnupg` (`common.conf` = `use-keyboxd`), generates key | 0 | 609 ms |
| state | encrypt, value on stdin | 0 | 17 ms |
| state | decrypt | 0 | 197 ms |
| state | after `gpgconf --kill all`, decrypt cold: gpg starts keyboxd and gpg-agent | 0 | 976 ms |
| state | secret-key census, cold | 0 | 784 ms |
| `.gnupg` only (reviewer, round 2) | decrypt cold, keyboxd and agent started inside | 0 | — |
| `.gnupg` only (reviewer, round 2) | encrypt into `store/` | 2 | `Operation not permitted` |
| state | `GNUPGHOME=<missing dir>` instead of `HOME` | 2 | 13 ms |
| none | decrypt cold | 2 | 13 ms, `No secret key` |

Earlier r1 probes, which motivated dropping the person's store: with an
agent already running outside, sandboxed gpg decrypted with no write grant;
with none running it failed with `failed to create temporary file …
Operation not permitted`; a 128-byte gpg home path failed with
`File name too long`.

## Remaining risk

- **A passphrase-less key beside its ciphertext protects no better than a
  mode-0600 file.** Anything that reads `~/.cartridge/auth` as this user can
  decrypt every entry. Directories are `0700`, which stops other users, not
  this user's processes. In this composition's working trees on 2026-09-19,
  thirteen other cartridges grant `read: ["/"]`: docs, fs, harness, live,
  lsp, mcp, memo, memory, prd, proxy, pty, router and tools. `router` also
  writes `$HOME/.cartridge` (`router.ctg/cartridge.json:355-358`), which
  covers `~/.cartridge/auth`. The owned store buys the pass layout, one door
  for values, names safe to list, and zero setup; it is not isolation from
  other nodes.
- **Out of scope, host follow-up:** denying `~/.cartridge/auth` in every
  other node's seatbelt profile belongs to `cartridge.ctg`'s sandbox, not to
  this cartridge.
- The keyboxd and gpg-agent that gpg starts inside the sandbox outlive the
  node; gpg reuses or replaces them.
- `CARTRIDGE_HOME` does not move auth's state; a grant cannot name it.
- gpg's helpers are admitted through the install-prefix rule, unprobed
  outside Homebrew.
- The doc gates are greps and stand in for reading; the diff reader is the
  backstop for the two delivery rules and the states table.
- No mutant runs inside a Verify block; step 8 and the diff reviewer are the
  backstop for test bodies.
- Collecting edits `cartridge.json`, and a grant change untrusts auth in a
  running daemon until the user trusts it again; voice loses `auth` for that
  interval.

## Verify and Proof

No cargo. Pass 2 writes only `node_modules/` (gitignored, outside the
footprint) and `/tmp/ca-*`, `/tmp/cs-*`, which the tests remove. No block
reads a variable without a default, and none uses `timeout`, which this
machine lacks.

```sh
test -f src/pass.ts
test -f src/insert.ts
test -f .cartridge/tests/integration/pass.test.ts
command -v gpg >/dev/null
command -v gpgconf >/dev/null
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
"$CARTRIDGE_BUN" -e '
const m = JSON.parse(require("node:fs").readFileSync("cartridge.json", "utf8"));
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const auth = m.events.auth.schema;
const ok = same(m.grant.exec, ["bun", "gpg"]) && same(m.grant.write, ["$HOME/.cartridge/auth/.gnupg"])
  && m.grant.env === undefined && same(m.grant.read, ["/"]) && same(m.grant.net, ["api.openai.com"])
  && m.settings?.password_store_dir === undefined
  && same(auth.required, ["op"]) && same(auth.properties.op.enum, ["status", "list"])
  && auth.properties.field?.type === "string";
if (!ok) process.exit(1);
'
for doc in README.md .cartridge/help.md .cartridge/docs/README.md; do
  grep -q 'cartridge/<provider>/<field>' "$doc"
  grep -q 'src/insert.ts' "$doc"
  grep -q '"op":"list"' "$doc"
done
for state in missing_entry gpg_missing no_answer refused; do
  grep -q "$state" .cartridge/docs/README.md
done
grep -q 'no better than a mode-0600 file' .cartridge/docs/README.md
if grep -qn 'password_store_dir' src/pass.ts src/openai.ts cartridge.json; then exit 1; fi
# The test never reaches this machine's home or gpg home.
if grep -qn 'homedir(' .cartridge/tests/integration/pass.test.ts; then exit 1; fi
if grep -qn 'tmpdir(' .cartridge/tests/integration/pass.test.ts; then exit 1; fi
if grep -qn 'GNUPGHOME' .cartridge/tests/integration/pass.test.ts; then exit 1; fi
```

```sh
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" install --frozen-lockfile
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" run check
# The entrypoint still starts, and list on a home with no store is an empty
# answer: not a hang, not an error, nothing created.
out="$(printf '{"id":1,"call":"apply","args":{}}\n{"id":2,"call":"auth","args":{"op":"list"}}\n' | env -u CARTRIDGE_YOLO HOME=/nonexistent-auth-home "$CARTRIDGE_BUN" src/main.ts)"
printf '%s\n' "$out" | grep -q '"id":2,"result":\[\]'
```

```test
run: env -u CARTRIDGE_YOLO "${CARTRIDGE_BUN:-bun}" test ./.cartridge/tests/ --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: a stored entry decrypts inside the process and the value reaches only the authenticated call
pass: the insert door round-trips a value that status reports as source pass without the value
pass: a provider or field name cannot leave the cartridge subtree
pass: list returns every cartridge entry and no response or frame carries the value
pass: first use creates the store and the key with 0700 modes
pass: a read on a home with no store reports a missing entry and creates nothing
pass: gpg missing and no answer and refused are three bounded diagnostics
pass: shared credentials are discovered without leaking them into status
pass: an absent default store is not an issue and a store is read once however it is named
pass: the WebSocket transport starts a session on the credential and holds nothing back
```
