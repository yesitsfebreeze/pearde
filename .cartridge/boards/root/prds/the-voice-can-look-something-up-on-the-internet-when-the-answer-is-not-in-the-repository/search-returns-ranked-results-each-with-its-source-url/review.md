# @root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url review history

Plan: `@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url`, at `prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url/prd.md` with `specs/spec01.md`.
Scope: one executable leaf. `web.ctg` gains `{op:"search", query, limit?}` against the Brave Search API, with the key named by an optional setting.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: superproject `7a32a47` (the spec was measured on `ccb4348`; `git diff --stat ccb4348 7a32a47 -- web.ctg` is empty, so the base for this footprint has not moved). `cartridge.ctg` at `beb8213`. The planning records are uncommitted.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md`, SHA-256 `aa9b63dfbd63f52aeedb3ff1c84fd7078d4292815714ebf8c4e874e7a0a9ccd0` |
| Specs | `specs/spec01.md`, SHA-256 `787f175a63c2116b8a9319a2a2c095ef2a45f78d161d8ad2827bbbe9b21c1820` |
| Material contracts/dependencies | `web.ctg/cartridge.json` `4c776715…`; `cartridge.ctg/src/host/plan.rs` `bc044aaf…` (`configured`, `expand_grant`); `cartridge.ctg/src/host/process.rs` `56886772…` (`granted_env`, `env_clear`); `harness.ctg/cartridge.json` `04a3f790…` (the `roster` / `HARNESS_ROSTER_*` precedent); the analyst's reference diff (485 lines, SHA-256 `a605ea62…`); the sibling `web-ctg-exists-...` is done at `3dba7f2`. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The plan follows the user's answer of 2026-09-17 exactly: Brave only, `grant.net` gains exactly `api.search.brave.com`, and the key comes from an optional setting that defaults to `null` and names an environment variable. It has one operation and one cartridge, and `fetch` is untouched. −1: nothing tells the operator where to export the key. It must be in the environment of the cartridge daemon, not only the shell they happen to be in. |
| Ownership and reuse | 17 | It reuses the `deps` seam already present in `Web` and the existing `tool.web` refusal envelope. The `WEB_*` grant copies `harness.ctg`'s `roster` exactly: an optional null setting names a variable whose name must start with a static `grant.env` prefix (`HARNESS_ROSTER_*`). `sessions.ctg` uses the same shape (`SESSIONS_MAILBOX_*`). −3: the spec's rationale says `sessions.ctg`/`harness.ctg` "already use that exact mechanism" (`${config.X}` in a grant) "for their own per-operator env names". That is false. No cartridge in this composition puts `${config.…}` in `grant.env`. The same paragraph then calls the static prefix "the sessions.ctg/harness.ctg shape", which contradicts it. |
| Dependencies and implementable slices | 19 | The one hard `need` (the fetch sibling) is done. The footprint lists exactly six files, `web.ctg` is a plain tracked directory, and there is no submodule bump. The reference typechecks: `tsc --noEmit` exits 0 with the bun types linked into the scratch tree. −1: the spec names HEAD `ccb4348` when HEAD is now `7a32a47`. The footprint is unchanged between them, but the recorded revision is stale. |
| Observable acceptance and baseline evidence | 13 | Re-run by this reviewer: the base fails all three blocks and the reference passes all three, 11 pass / 0 fail / 71 `expect()`. Block 2 kills all three of the analyst's mutants. **But the manifest half of Acceptance is not pinned, and these gaps are static data, not the behavioural ceiling:** four `cartridge.json`-only mutants of the reference pass blocks 1, 2 and 3 with exit 0 (Validation, M1–M4). M1 leaves `required:["op","url"]` on the `web` event schema. The host checks a payload against its schema before sending it (`help host/docs/transport.txt` §Events), so `{op:"search", query}` on `web` would be refused at the sender, and Acceptance box 1 would fail with every block green. M2 sets `grant.env:["WEB"]` and M3 sets `grant.env:[""]`. `granted_env` treats an entry with no `*` as an exact name, so the key is never handed through, and search reports `NO_SEARCH_KEY` for ever in the real composition. Block 1's `"WEB_BRAVE_API_KEY".startsWith(p.replace(/\*$/,""))` accepts both. M4 sets `grant.env:["W*"]`, which is broader than the documented prefix and also passes. |
| Failure, recovery and compatibility | 16 | This part is sound. A missing setting, an unset variable and a 401/403 each throw a message naming `brave_api_key_env`, never a `{results:[]}`. Any other status reuses `fetch`'s wording. The key is sent in a header and never appears in an error URL. The tests use only a loopback `Bun.serve`. With the setting null, `web.ctg` still loads, because the static prefix never goes through `configured()`. I confirmed in `plan.rs:88-90` that `configured()` errors on a null `${config.X}`, so the analyst's claim holds. −2: in the reference `help.md`, "keep the first [`grant.net`] a subset of the second [`allow_hosts`]" is now false, because `api.search.brave.com` is in `grant.net` and not in `allow_hosts`. It also contradicts README line 77, which says the opposite direction. −2: a setting that names a variable without the `WEB_` prefix (say `BRAVE_API_KEY`, which the host strips) gets the generic `NO_SEARCH_KEY`. The error does name the setting, but it does not say why a variable the operator did export was not seen. |
| Reviewer total | 84 / 100 | |

Findings and concrete revisions:

- **B1 (blocking): block 1 does not pin `grant.env` to a prefix the host honours.** Evidence: M2, M3 and M4 pass all three blocks. Revision: replace block 1's `grant.env` checks with an exact assertion, `if (JSON.stringify(env) !== JSON.stringify(["WEB_*"])) bad(...)`. I measured this line: it fails on the base and on M2, M3 and M4, and passes the reference.
- **B2 (blocking): block 1 does not check that the `web` event schema admits a search.** Evidence: M1 passes all three blocks. Revision: add to block 1's `bun -e`: `required` contains neither `url` nor `query`; the `allOf` branch whose `if.properties.op.const` is `"search"` has `then.required` containing `"query"`; and the `"fetch"` branch has `then.required` containing `"url"`. I measured these checks together with B1's: base exit 1, M1–M4 exit 1, reference exit 0. The exact script is in Validation.
- N1 (non-blocking): correct the rationale paragraph. `harness.ctg` (`roster` / `HARNESS_ROSTER_*`) and `sessions.ctg` (`SESSIONS_MAILBOX_*`) use a static prefix, not `${config.X}`. Cite `harness.ctg`'s `roster` as the direct precedent. The one real alternative is worth one sentence: `configured()` skips an empty-string value (`plan.rs:91`), so `default: ""` plus `grant.env:["${config.brave_api_key_env}"]` would grant exactly one variable name. It is rejected because the user's answer fixes `null` as the unset value, and because the `harness` precedent uses a prefix. `WEB_*` leaks only variables the operator deliberately named `WEB_…` into the node, which is acceptable.
- N2 (non-blocking): in `help.md`'s `allow_hosts` line, reverse or drop "keep the first a subset of the second" so that it agrees with the README ("Keep `allow_hosts` a subset of `grant.net`"). Say that `api.search.brave.com` is the one `grant.net` host that is deliberately absent from `allow_hosts`.
- N3 (non-blocking): when `brave_api_key_env` names a variable that does not start with `WEB_`, make `search` say so in the refusal, for example "`brave_api_key_env` names `BRAVE_API_KEY`, which does not start with `WEB_`, so the base never hands it through". Add one line to README saying the variable must be in the cartridge daemon's environment.
- N4 (non-blocking): update "What was measured" to the current HEAD `7a32a47`. The footprint is unchanged, so this is only a record correction.

Disposition: revise. Keep the design. Only block 1 of the spec and its prose need to change, and the reference implementation is already correct against the stricter block 1.

Validation (every command run by this reviewer on 2026-09-19. Each block ran as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block>"` in detached superproject worktrees of `7a32a47` under `scratchpad/reviewer-search-1/`, whose sibling submodule directories were empty. `base` is the untouched tree and `wt` is the tree with the analyst's reference diff applied. Both worktrees were removed afterwards with `git worktree remove`, and nothing was written in the live `web.ctg`.):

| Tree | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| base | 1 | 1 (`noKey.search is not a function`) | 1 |
| reference | 0 (`audit: 1 of 1 cartridges pass the hard checks`, `isolation composition pass`, 2 s) | 0 | 0 (`11 pass`, `0 fail`, `71 expect() calls`, 25 ms) |
| M1 reference + `events.web.schema.required=["op","url"]` | 0 | 0 | 0 |
| M2 reference + `grant.env=["WEB"]` | 0 | 0 | 0 |
| M3 reference + `grant.env=[""]` | 0 | 0 | 0 |
| M4 reference + `grant.env=["W*"]` | 0 | 0 | 0 |

- Proposed B1+B2 check, run the same way: base 1, reference 0, M1 1, M2 1, M3 1, M4 1. Script:
  ```sh
  bun -e '
    const m = JSON.parse(require("node:fs").readFileSync("web.ctg/cartridge.json", "utf8"));
    const bad = (why) => { console.error("manifest: " + why); process.exit(1); };
    const env = (m.grant || {}).env || [];
    if (JSON.stringify(env) !== JSON.stringify(["WEB_*"])) bad("grant.env is not exactly [\"WEB_*\"]: " + JSON.stringify(env));
    const s = m.events.web.schema;
    if ((s.required || []).includes("url") || (s.required || []).includes("query")) bad("the web schema requires url or query for every op");
    const when = (op) => (s.allOf || []).find((b) => ((((b.if || {}).properties || {}).op || {}).const) === op);
    if (!((when("search") || {}).then || {}).required?.includes("query")) bad("op search does not require query");
    if (!((when("fetch") || {}).then || {}).required?.includes("url")) bad("op fetch does not require url");
  '
  ```
- `tsc --noEmit -p .` in the scratch `web.ctg`, using a temporary symlink to the existing `auth.ctg/node_modules`: reference 0, base 0.
- The live superproject at `7a32a47`, run as `env -i … sh -eu -c 'just audit web; just isolation'`, exits 0 (`Isolation passed for 18 cartridges.`). This is the repo-pass shape. The change is not present there.
- Source reading: `configured()` at `plan.rs:78-96` errors on a non-string `${config.X}` and skips an empty string. `granted_env` at `process.rs:59-73` treats an entry ending in `*` as a prefix and any other entry as an exact name, and rejects a bare `*`. `process.rs:116` calls `env_clear()`, and the Lua `cartridge.spawn` child inherits the node's environment. No cartridge's `grant.env` uses `${config.…}`: `harness` has `HARNESS_ROSTER_*`, `sessions` has `SESSIONS_MAILBOX_*`, and `live` has `OPENAI_API_KEY`.

Reviewer identity: reviewer-search-1 (independent review sub-agent, Opus 5).
User rating: not required under delegation.
User feedback/provenance: the user's answer of 2026-09-17 in `prd.md` ("Brave Search API, the key from a declared optional setting that names an environment variable, and no second backend"). The plan honours it.
Result: FAIL (84/100, two blocking findings).
Unresolved blocking findings: B1 (the `grant.env` value is not pinned) and B2 (nothing checks that the `web` event schema admits a search).
Rounds used / remaining: 1 / 4.
Next action: a bounded revision of `spec01.md` block 1 (add the measured check above), plus the N1–N4 prose fixes. Then re-run blocks 1–3 against the base, the reference and M1–M4, and present round 2.

## Round 2 — 2026-09-19

Presented revision: superproject `ec2b1d6`, with `cartridge.ctg` at `beb8213`. The planning records are uncommitted. I checked the dependency drift since the spec's round-1 base `ccb4348`. `git diff --stat ccb4348 ec2b1d6 -- web.ctg` is empty. Inside `cartridge.ctg`, `git diff --stat d169293 beb8213 -- src/host/plan.rs src/host/process.rs` is empty; only `src/transport/cartridge.rs` moved.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md`, SHA-256 `aa9b63dfbd63f52aeedb3ff1c84fd7078d4292815714ebf8c4e874e7a0a9ccd0` (unchanged from round 1) |
| Specs | `specs/spec01.md`, SHA-256 `9029f87868109d61f7b31b1cdbe29df8e03c07c7a577f49c68c7a26b633a1a1a` |
| Material contracts/dependencies | `web.ctg/cartridge.json` `4c776715…` (unchanged); `cartridge.ctg/src/host/plan.rs` and `process.rs` (unchanged since round 1); `cartridge.ctg/src/transport/cartridge.rs:258` + `Cargo.toml` `jsonschema 0.56` (full validator, so `allOf`/`if`/`then` are honoured; `docs.ctg` and `memo.ctg` already use `allOf`); the analyst's round-2 reference diff, taken from `analyst-search/r2/wt` (515 lines, SHA-256 `c8fafc19…`). |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | It still follows the user's answer of 2026-09-17 exactly: Brave only, one host added to `grant.net`, and an optional null setting that names a variable. The round-1 deduction is resolved: the reference README and `help.md` now say the variable has to be in the cartridge daemon's own environment. |
| Ownership and reuse | 19 | N1 is resolved. The rationale now names `harness.ctg`'s `roster`/`HARNESS_ROSTER_*` as the precedent, lists `SESSIONS_MAILBOX_*` and `OPENAI_API_KEY` correctly, and weighs and rejects the `default:""` + `${config.X}` alternative with the reason I gave. −1: the paragraph still describes `expand_grant` as "the mechanism wrongly attributed" at some length, when one sentence would do. This is style only. |
| Dependencies and implementable slices | 19 | The footprint is still exactly six files, `web.ctg` is still a plain directory, and the need is done. N4 is resolved, since HEAD `ec2b1d6` is recorded. −1: the spec's evidence that `plan.rs`/`process.rs` did not move is a superproject `git diff -- cartridge.ctg/src/host/…`. That command is empty whatever happens, because the superproject cannot see paths inside a submodule. I checked inside the submodule and the claim is true, but the command it cites proves nothing. |
| Observable acceptance and baseline evidence | 18 | B1 and B2 are resolved. I re-ran the checks independently and the results are below. Block 1 now fails every manifest mutant from round 1 (M1–M4). It also fails four more I added this round: M5 drops the `search` `allOf` branch, M6 sets `default: ""`, M7 drops `api.search.brave.com` from `grant.net`, and M8 is a `web.ts` mutant, covered next. Blocks 2 and 3 fail the analyst's `web.ts` mutants (a)–(c), and fail M8, which deletes the `WEB_` prefix check in `search()`. −2: nothing pins `main.ts`'s `DESCRIPTOR.input_schema`. A tree that keeps `required:["op","url"]` there would pass every block and would advertise a schema to the model that forbids a url-less search. This is a diff-reading item and does not block. |
| Failure, recovery and compatibility | 19 | N2 is resolved. The `help.md` line now reads "keep `allow_hosts` a subset of `grant.net`", which agrees with the README, and it names `api.search.brave.com` as the host that is deliberately left out. N3 is resolved. `KEY_NOT_GRANTED` names both `brave_api_key_env` and the offending variable, and it fires before any request. Block 2 checks this, and so does a new suite test. The key still travels only in a header. The null setting still loads, because the static prefix never reaches `configured()`. −1: `search()` silently caps `count` at 20, and neither the README nor `help.md` says so. |
| Reviewer total | 95 / 100 | |

Findings and concrete revisions:

- B1: resolved. Block 1 line 224 pins `grant.env` to exactly `["WEB_*"]`, and M2, M3 and M4 each fail it with `manifest: grant.env is not exactly ["WEB_*"]`.
- B2: resolved. Block 1 lines 206–211 check `required` and both `allOf` branches, and M1 fails with `the web schema requires url or query for every op`. The host's `jsonschema` 0.56 validator honours `if`/`then`, so the reference schema accepts `{op:"search", query}` at the sender.
- N1, N2, N3 and N4: resolved, as described above.
- N5 (non-blocking, new): the implementer should give `DESCRIPTOR.input_schema` in `main.ts` the same per-op `required` shape as the event schema, or at least keep `required:["op"]`, as the reference does. The diff reading is the backstop here.
- N6 (non-blocking, new): the implementer should mention the 20-result cap in `help.md`, and the spec's drift evidence should cite the in-submodule diff rather than the superproject path diff.

Disposition: keep. The plan is ready for implementation.

Validation (every command below was run by this reviewer on 2026-09-19). I made one detached superproject worktree of `ec2b1d6` at `scratchpad/reviewer-search-2/wt`, with the sibling submodule directories empty. Each variant was produced by applying the reference diff and/or a single mutation, then reverting with `git apply -R`. Every block was extracted byte-for-byte from `spec01.md` and run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block>"`. Afterwards I removed the worktree with `git worktree remove`. Nothing was written in the live `web.ctg`, which has a clean `git status`.

| Tree | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| base | 1 | 1 (`noKey.search is not a function`) | 1 |
| reference | 0 (`audit: 1 of 1 cartridges pass the hard checks`, `isolation composition pass`) | 0 | 0 (`12 pass`, `0 fail`, `75 expect() calls`) |
| (a) the analyst's `web.ts`, which never checks the key | 0 | 1 | 1 |
| (b) the analyst's `web.ts`, which returns `{results:[]}` on a 401 | 0 | 1 | 1 |
| (c) the analyst's `web.ts`, whose messages do not name the setting | 0 | 1 | 1 |
| M1 `events.web.schema.required=["op","url"]` | 1 | 0 | 0 |
| M2 `grant.env=["WEB"]` | 1 | 0 | 0 |
| M3 `grant.env=[""]` | 1 | 0 | 0 |
| M4 `grant.env=["W*"]` | 1 | 0 | 0 |
| M5 (new) the `search` `allOf` branch removed | 1 | 0 | 0 |
| M6 (new) `brave_api_key_env.default=""` | 1 | 0 | 0 |
| M7 (new) `api.search.brave.com` removed from `grant.net` | 1 | 0 | 0 |
| M8 (new) the `WEB_` prefix check in `search()` removed | 0 | 1 | 1 |

- `tsc --noEmit -p .` on the reference `web.ctg`, using a temporary symlink to the live `auth.ctg/node_modules`, exits 0.
- The live superproject, run as `env -i … sh -eu -c 'just audit web; just isolation'`: this is the repo-pass shape, with the change absent. It printed `Isolation passed for 18 cartridges.` and `isolation composition pass`.

Reviewer identity: reviewer-search-2 (independent review sub-agent, Opus 5).
User rating: not required under delegation.
User feedback/provenance: the user's answer of 2026-09-17 in `prd.md`. The plan still honours it.
Result: PASS (95/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation of `spec01.md`. Carry N5 and N6 as diff-reading checks for the implementation review.
