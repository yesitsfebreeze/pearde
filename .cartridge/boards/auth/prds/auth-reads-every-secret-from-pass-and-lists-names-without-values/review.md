# @auth/auth-reads-every-secret-from-pass-and-lists-names-without-values review history

Plan: `@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values`, at `prds/auth-reads-every-secret-from-pass-and-lists-names-without-values/prd.md` on the auth board.
Scope: one leaf. auth reads `cartridge/<provider>/<field>` from the pass store first, and answers `status` and `list` with names only.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md).

## Round 1 — 2026-09-19

Presented revision: `auth.ctg` base `d8751088bb8b0884ff641e027855d82257ee8ff0`, which was also the submodule HEAD. The plan and spec were uncommitted working files in `prd.ctg`.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `6d2657e0ef1fa26816edf5676766339f481334424aafd01032fa769e919efce4` |
| Specs | `specs/spec01.md` sha256 `67fdfcabf62f936f5e42bdd92f42b4706e7f91b9bb2b539460aeb07fa8f217e7` |
| Material contracts/dependencies | `cartridge.ctg/src/sandbox/mod.rs:231-338`, `cartridge.ctg/src/host/process.rs:22-35,115-122`, `prd.ctg/src/lifecycle.ts:93,111` (120 s per Verify block), `~/.gnupg/common.conf` on this machine |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Follows the user's 2026-09-19 direction; one owner, one outcome; spec boxes map onto the PRD boxes. −1: the PRD body is 550 words against the 400-word split line. −1: `list` decrypts every secret to answer a names-only question (F5). |
| Ownership and reuse | 19 | Reuses the `key()` rule at `openai.ts:63`, the `serve`/`node()` test seams and the `live.test.ts` stderr swap. −1: `entry()` does not say what it does with a non-string or `null` `field` (F6). |
| Dependencies and implementable slices | 15 | Root of the chain; spec footprint is a subset of the PRD's. −3: Step 2 taken literally fails the spec's own `bun run check`, and the public `state` value is undefined (F2). −2: fixture cost against the 120 s block limit is unstated (F3). |
| Observable acceptance and baseline evidence | 14 | Five named tests through JUnit; base census of 15 confirmed; the manifest gate is red on the base tree (run, exit 1); guards use the `if grep …; then exit 1; fi` form. −4: the probe the PRD calls "risk to probe first" ran on a gpg home that differs from the real one (F1). −1: suite wall time unmeasured. −1: the delivery-rules clause has no gate, and the `test` block calls bare `bun`. |
| Failure, recovery and compatibility | 15 | Three states, a bounded asynchronous spawn, stderr discarded, a name regex that refuses `..` and `/`, gpg spawned only after the entry file exists. −3: the keyboxd failure mode is missing from the diagnostic and docs, and the gate pins an incomplete remedy (F1). −1: F5. −1: F6 and F7. |
| Reviewer total | 81 / 100 | FAIL |

Findings and concrete revisions:

1. F1, blocking. The central probe did not run in the production gpg configuration. `~/.gnupg/common.conf` contains `use-keyboxd`; the analyst's fixture homes were made by `mkdtemp` and hold `pubring.kbx` and no `common.conf`. With `use-keyboxd`, gpg needs a running keyboxd before it asks the agent, and auth's grant has no write access with which to launch one. The reviewer inferred this and could not observe it: its scratch path exceeded the 104-byte `sun_path` limit. Revision: probe a home whose `common.conf` says `use-keyboxd`, with and without keyboxd running; fix the docs, the `locked` message and the gate; split `locked` three ways by `error.code === "ENOENT"`, `error.killed`, and anything else.
2. F2, blocking. `read()` returns `"available"`, which the widened `AuthStatus.state` union lacks, and the non-openai status object omits the required `chatgpt_login`, so the text fails `tsc`. Revision: define the public `state` strings, make `chatgpt_login` optional, assert `state` in test 2, and say what `status("openai", field)` does with `field`.
3. F3, non-blocking. Build the fixture once per file and record the suite's wall time against the 120 s block limit.
4. F4, non-blocking. The grep gates stand in for documentation. Accept them as the ceiling, name the diff reader as the backstop for the two delivery rules, and use `"${CARTRIDGE_BUN:-bun}"` in the `test` block.
5. F5, non-blocking. `list` brings every plaintext into the process to compute a boolean. Discard gpg's stdout for the availability check.
6. F6, non-blocking. A `null` or non-string `field` passes the regex through coercion. Require `typeof === "string"` and test `field: null` and `provider: 5`.
7. F7, non-blocking. `list` can return names `status` refuses. `list` skips any path whose parts fail `entry()`.
8. F8, non-blocking. The openai missing-key message does not mention pass.

Also recorded: every citation in the spec is correct at `d875108`. No consumer of the status shape exists outside `auth.ctg` (`live.ctg/src/socket.rs:34` reads keys itself), so an optional `capability` and a wider `state` break nothing. The only callers of `discover()` are `status()` and `create()`, both already async. A fixture `gpgconf --kill gpg-agent` that omits `GNUPGHOME` would kill the user's real agent, so every test gpg call goes through one wrapper.

Disposition: revise. Keep the scope, the owner and the slices.
Validation: `shasum -a 256 prd.md specs/spec01.md` in the PRD directory, exit 0, both match. `git archive d875108 | tar -x` into the reviewer's scratch copy, exit 0. The spec's manifest gate body run there with bun, exit 1, as it should. Five runs of the stdin smoke against the base `main.ts`, exit 0 each. `env -u CARTRIDGE_YOLO true`, exit 0. No gpg or sandbox probe was run by the reviewer.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 1.
User rating: not required under delegation; none was supplied.
User feedback/provenance: after this round was dispatched the user redirected the design in the same session: "For point one can't we use the pass system for the harness so we don't have to set anything up manually? The harness or the agent itself (like the cartridge we create) can hold its own settings and its own pass integration rather than tying it to the user". The feedback assessed the round 1 design, which read the user's own `~/.password-store`. Round 2 presents an auth-owned store.
Result: FAIL (81/100).
Unresolved blocking findings: F1 and F2.
Rounds used / remaining: 1 / 4.

## Round 2 — 2026-09-19

Presented revision: `auth.ctg` base `d875108`. Plan `prd.md` sha256 `3ad09592b27b1b61400c412a5571115478e4554d3e6b5b20650ebe9b7f8c66ef`; spec `specs/spec01.md` sha256 `64b7a60ede501d02522104406d6775748e7bcc9367cdb65fd5fc68f65ea9dd7c` (analyst revision 3: the auth-owned store plus F1-F8). Material inputs: `cartridge.ctg/src/sandbox/mod.rs:17-45,121-139,151-180,231-338`, `src/host/plan.rs:225-268`, `src/trust/mod.rs:19-37`, `router.ctg/cartridge.json:355-358`, `prd.ctg/src/lifecycle.ts:93,111`, and the analyst's probe artifacts.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Follows the user's redirect: zero setup, auth holds its own pass integration. −2: the body is 773 words with 6 boxes. −1: "the one cartridge that holds secrets" overstates the sandbox (N4). |
| Ownership and reuse | 19 | The departure from `$PROJECT/.cartridge/<folder>` is argued; `~/.cartridge` is the host's per-user home. −1: the `missing_entry` hint names a relative path (N6). |
| Dependencies and implementable slices | 17 | −2: the `password_store_dir` opt-in is a separable outcome that brings a second fixture home, a pinentry stub and two production paths (N1). −1: PRD box 1 still says "temporary `GNUPGHOME`", which the spec forbids (N2). |
| Observable acceptance and baseline evidence | 18 | Seven named tests through JUnit, fixture once per file, two named mutants, gate ceiling stated. −1: concurrent cold `list` untested (N5). −1: an empty inserted value is unspecified (N7). |
| Failure, recovery and compatibility | 17 | Seven-value state union, 0700 modes tested, no plaintext in `available()`, test wrapper asserts the homedir. −2: the write grant is wider than needed (N3). −1: other cartridges that can read the key are not named (N4). |
| Reviewer total | 88 / 100 | FAIL, no blocking finding |

F1-F8 are all resolved in the spec, not only mentioned.

Findings, none blocking:

1. N1. Split out or drop the `password_store_dir` opt-in; reach the `no_answer` and `refused` paths with a `gpg` stub on `PATH`; move Decision rationale into the spec so the PRD is under 400 words and 5 boxes.
2. N2. PRD box 1: "a temporary gpg home reached through `HOME`".
3. N3. Narrow the grant to `write: ["$HOME/.cartridge/auth/.gnupg"]`. The reviewer probed it: a sandboxed cold decrypt with keyboxd and the agent started inside the sandbox exited 0, and a sandboxed encrypt into `store/` exited 2 with `Operation not permitted`. The insert door creates the key and every entry outside the sandbox before any decrypt.
4. N4. Eleven other cartridges hold `read: ["/"]`; `router` writes `$HOME/.cartridge`. State it in the docs and Remaining risk, and record a host follow-up.
5. N5. Kill the agent before `list` in test 4 and assert every valid row is available.
6. N6. Build the insert hint from `import.meta.dir`.
7. N7. The door refuses an empty value with a public message; test it.

Validation: digests match; `HOME=/tmp/rv2-probe-home bun -e 'console.log(require("node:os").homedir())'` printed the fixture path; the `.gnupg`-only sandbox probe as above, fixtures removed afterwards; `wc -w` on the body, 773.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 2.
User rating: not required under delegation; none was supplied.
Result: FAIL (88/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Coordinator disposition of N1: drop the opt-in rather than split it. The user asked for auth's own store "rather than tying it to the user"; no one asked for the user's store, so no follow-up PRD is added.

## Round 3 — 2026-09-19

Presented revision: `auth.ctg` base `d875108`. Plan `prd.md` sha256 `85ebe723149889191c1cc3125f412b696b526e180de99b1c33e6d1aac375037e`; spec `specs/spec01.md` sha256 `19a1e8dd943c76741b3118bd111fd7237dab9c17a6220756f17d02d514d6dbb2` (analyst revision 4). The first run of this round stopped on an API usage limit and was rerun from the start on the same inputs.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, five boxes, the opt-in dropped with its reason recorded. −1: 444 words; the excess is the user's verbatim quote, which stays. |
| Ownership and reuse | 19 | auth owns it; the `~/.cartridge` departure is argued; no settings surface and no second class. −1: `CARTRIDGE_HOME` does not move auth's state. |
| Dependencies and implementable slices | 19 | Both dependants still need this leaf; every step names its file. −1: the manifest check hangs off spec box 1 (R3-1), and the `auth.jev` pre-draft still reasons about a pinentry (R3-2). |
| Observable acceptance and baseline evidence | 18 | Seven new named tests map onto the five boxes; the `test` block pins them and three base tests, and a non-zero exit guards the rest. −1: delivery rules and the reader list rest on grep and the diff reading. −1: suite wall time is known only after implementation. |
| Failure, recovery and compatibility | 19 | Six public states; no plaintext in `available()`; a read creates nothing; the narrowest working grant. −1: the keyboxd and gpg-agent started inside the sandbox outlive the node (R3-3). |
| Reviewer total | 94 / 100 | PASS |

N1-N7 are resolved in the text of revision 4, and dropping the opt-in broke nothing (`rg` for `password_store_dir`, `password-store`, `opt-in` and `pinentry` across this PRD, its spec and both dependent PRDs). The reviewer probed the stub bound: a `sleep 20` stub was killed at 1007 ms by `execFile` and at 1003 ms by `spawn` with `stdio:"ignore"`.

Findings, none blocking: R3-1, move the manifest check to its own line after the five boxes. R3-2, the `auth.jev` pre-draft (`proposals/spec01-draft.md:320`) replaces its pinentry reasoning with this leaf's states before that PRD is specced. R3-3, the implementer records in the evidence note whether `gpgconf --kill all` on `dispose` is wanted.

Validation: digests recomputed, unchanged; no leftover `/tmp/rv2-*` or `/tmp/rv3-*` fixture or agent; `bun stub-bound.ts` in the reviewer's scratch directory, exit 0, stub directory removed; `sed -n 42,62p cartridge.ctg/src/sandbox/mod.rs` confirms how a missing grant path is rendered; `wc -w` on the body, 444.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 3.
User rating: not required under delegation; none was supplied.
Result: PASS (94/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 5.
