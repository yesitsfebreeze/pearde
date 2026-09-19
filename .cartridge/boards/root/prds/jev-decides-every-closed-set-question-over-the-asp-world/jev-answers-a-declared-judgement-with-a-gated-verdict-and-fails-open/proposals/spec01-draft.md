---
complexity: 3
footprint:
  - jev.ctg/**
  - .cartridge/init.lua
---

# spec01 — jev.ctg answers a declared judgement with a gated verdict and fails open

Pre-draft, written while the PRD is still blocked on
`@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key`. Base read:
superproject `801aa8e`, `cartridge.ctg` `7af748a`, `auth.ctg` `d875108`.
Nothing here was built; every claim below is source evidence unless it says
"inferred".

## Four corrections to the PRD text the coordinator must make first

1. **`needs` cannot name `asp`.** `cartridge.ctg/docs/asp.txt:96` says
   "`asp` is the base's own service key, so no cartridge may need or listen to
   it"; `src/loader/document.rs:183` refuses `events.asp`; `src/host/mod.rs:856`
   answers a bail to `asp` before it looks for a listener, so no `needs` entry
   is required to reach it. A need nobody can listen to keeps the cartridge
   from starting (inferred from `needs` = "must have a listener before this
   cartridge starts", `docs/creating-cartridges.txt:147`; not probed). This PRD
   never calls ASP anyway; the sibling that pulls slices reaches it with
   `wire.host("asp", …)`. The rollup Decision line "names `auth.jev` and `asp`
   in its `needs`" needs rewording.
2. **jev needs `memo`.** A judgement is a memo, and consumers will ship theirs
   in their own records (`@harness/judgement/…`), which only memo's merged
   record resolves. jev reads with `memo {op:"read", path, cwd}` (returns the
   parsed `frontmatter`, `memo.ctg/.cartridge/docs/README.md:87`). Every
   existing caller passes a `cwd` from its own request (`harness.ctg/src/lib.rs:283`),
   so `decide` takes `cwd` too: `jev {op:"decide", point, state, cwd}`.
3. **Memo refuses nothing about a kind's fields.** `memo.ctg/src/record.rs`
   `validate` checks the kind is declared, the folder, the description and the
   links; `type/decision.md` says outright "the cartridge does not enforce".
   `memo.ctg` is outside this footprint. So "a write that lacks a gate or a
   fallback is refused" is delivered by jev's own door:
   `jev {op:"declare", point, judgement, cwd}` validates, then writes through
   `memo {op:"write"}`. A judgement written around that door is caught on read:
   `decide` escalates with reason `invalid judgement`. That is fail-open, so
   nothing is lost, but the box should say "a `declare` that lacks…".
4. **Submodule or plain directory** — see "Step 0". This spec is written for
   the plain directory, which is what the footprint `jev.ctg/**` on a
   superproject PRD can actually collect, and drops `.gitmodules` from its
   footprint. Acceptance box 1 of the PRD ("is a submodule") must be reworded
   or the PRD split; that is a user decision.

## Step 0 — how `jev.ctg` comes to exist

Evidence: all 18 entries in `.gitmodules` are separate repositories under
`https://github.com/yesitsfebreeze/<name>.git` (`git config -f .gitmodules --list`;
`git -C auth.ctg remote -v`). `gh repo view yesitsfebreeze/jev.ctg` answers
"Could not resolve to a Repository", so no remote exists. `web.ctg` — the PRD's
own named precedent — is **not** a submodule: it has no `.git`, no `.gitmodules`
entry, and its files are tracked by the superproject (`git ls-files -s web.ctg`
shows mode 100644 blobs, where `auth.ctg` is a 160000 gitlink). It landed as
commit `3dba7f2` from a root-board PRD with footprint `web.ctg` +
`.cartridge/init.lua`.

**Path B (this spec, default): plain tracked directory, like `web.ctg`.** The
implementer creates `jev.ctg/` in the lane, collect commits it in the
superproject, `.gitmodules` is untouched. No remote, no user. `just audit` and
`just isolation` find it because both enumerate `*.ctg` directories holding a
`cartridge.json`, not `.gitmodules`.

**Path A (what the PRD text asks): a real submodule.** Needs, in order: the
user creates (or explicitly authorises `gh repo create` for) the empty remote
`yesitsfebreeze/jev.ctg`, choosing its visibility; a seed commit is pushed;
`git submodule add https://github.com/yesitsfebreeze/jev.ctg.git jev.ctg` in
the superproject; a `jev` board with `repo: /Users/feb/dev/cartridge/jev.ctg`;
this PRD retargeted there with the `jev.ctg/` prefix stripped from every path
below; and a two-line root PRD for the `.cartridge/init.lua` entry and the
gitlink bump. A root-board lane is a worktree of the superproject cut from
HEAD, where `jev.ctg` is not yet a gitlink, and collect's receipt commits in
`repo`, which cannot hold files inside a submodule (inferred from the template's
lane notes and the memory notes on lanes; not probed). So under Path A this PRD
is a SPLIT, not one leaf. `gh` on this machine is logged in with `repo` scope,
so an agent *can* create the remote; it must not without the user saying so.

Converting B to A later is one mechanical PRD (`git subtree split -P jev.ctg`,
push, `git rm -r`, `git submodule add`), and loses no history.

## Files (all new, all under `jev.ctg/` except the last)

Copy the scaffolding from `web.ctg` as a starting text, then own it — no
import, symlink or path reaching `../web.ctg` (isolation law 3).

| File | Content |
| --- | --- |
| `cartridge.json` | below |
| `init.lua` | `web.ctg/init.lua` with the listen list `{ "jev" }` |
| `package.json`, `tsconfig.json`, `.gitignore`, `.cartridge/.gitignore` | as `web.ctg`, name `@cartridge/jev` |
| `src/wire.ts` | jev's own copy of the helper wire (121 lines, unchanged) |
| `src/jev.ts` | the logic: `validate(judgement)`, `verdict(judgement, answers)`, `decide(...)` |
| `src/main.ts` | `export function serve(wire, deps?)` + `if (import.meta.main) serve(new Wire());` |
| `.cartridge/memos/type/judgement.md` | the kind declaration (`kind: type`, `type: judgement`) |
| `.cartridge/memos/judgement/example-needs-an-llm.md` | the one example instance |
| `.cartridge/tests/integration/node.ts` | jev's own copy of the fake node |
| `.cartridge/tests/integration/decide.test.ts` | the named tests |
| `README.md` (≥10 non-blank lines), `.cartridge/help.md` | help has `## Use`, `## Read next`, and names the `judgement` kind |
| `/.cartridge/init.lua` | one line, after `auth`/`memo`: `{ id = "jev", path = "jev.ctg" },` |

### `cartridge.json`

- `name: "jev"`, `entry: "init.lua"`, a `description`.
- `needs: ["auth.jev?", "memo?"]`. The `?` is the host's optional need
  (`cartridge.ctg/src/host/plan.rs:21-24`; precedent `live.ctg` `"memo?"`): jev
  may send the event and starts without waiting for its provider, which is what
  "unavailable means today's path runs" requires. **No `asp`.**
- `listen: ["jev"]`.
- `events.jev`: `timeout_ms` set above the `timeout_ms` setting; schema
  `{op: "decide"|"declare", point, state?, judgement?, cwd}` with `required`
  per op via `allOf/if/then` as `web.ctg/cartridge.json` does. No `url`, `key`,
  `model` or `host` property, `additionalProperties: false`.
- `events["jev.decided"]`: description + schema with exactly
  `decision_id, point, verdict, confidence, answers, usage, latency_ms, reason`
  and `additionalProperties: false`. No `state`. Not in `listen` (jev emits it).
- `settings.timeout_ms`: `integer`, default `3000`, `min: 1`, with a `doc`
  line: how long `decide` waits for `auth.jev` before it escalates. The call it
  abandons keeps running in auth, bounded by auth's own manifest `timeout_ms`
  (a caller cannot cancel a cartridge call). No second copy of `3000` in code.
- `grant: { "exec": ["bun"] }`. No `net`, no `env`, no `read`/`write`. No
  setting that holds a key, URL or model.
- `commands.check` / `commands.test` as `web.ctg`.

### The `judgement` kind

Frontmatter of an instance: `kind: judgement`, `description`, `questions`
(a non-empty list in `auth.jev`'s own question shape, each with an `id`),
`gates` (a map from every question `id` to `{act, escalate}`, numbers with
`0 <= escalate <= act <= 1`), `fallback` (non-empty text: the path that decides
today). Body `## Criteria`: what the questions are judged against. `validate`
refuses: no questions, a question with no gate, a gate out of order or out of
range, an empty fallback. One function, used by both `declare` and `decide`.

### `decide` — the whole algorithm

1. `decision_id = crypto.randomUUID()`, start a clock.
2. `memo read` `judgement/<point>.md` (a `point` starting `@` is used as the
   path as given). Missing → escalate, reason `unknown point`. `validate`
   fails → escalate, reason `invalid judgement: <what>`.
3. `Promise.race` of `wire.call("auth.jev", {state, questions})` and a timer of
   `timeout_ms`. Rejection → reason `unavailable: <message>`; timer → reason
   `timeout`.
4. Confidence per answer: `choice` and `score` carry `confidence`; a `noul`
   answer `p` has confidence `max(p, 1 - p)`. **Unverified**: confirm against
   https://docs.typesafe.ai/confidence.md and the live probe recorded by the
   auth PRD's evidence note before coding it; an answer with no readable
   confidence counts as `0`.
5. Per question: `>= act` → `act`; `< escalate` → `escalate`; else `caution`.
   The result's `verdict` is the worst of them, its `confidence` the minimum.
6. Every exit, failure included, goes through one `finish()` that
   `wire.notify("jev.decided", {...})` without `state` and returns
   `{answers, confidence, verdict, decision_id, reason?}`. Failures return
   `answers: []`, `confidence: 0`, `verdict: "escalate"`. The handler body is
   one `try`; the `catch` also calls `finish()`. It never throws to the caller.

`serve(wire, deps)` follows `web.ctg/src/main.ts`: handlers registered on the
wire so the test's fake node answers `auth.jev` and `memo` asks. No other seam.

Not built (say so in the README, one line each): retries (auth owns backoff),
caching, ASP slices, a `decision:` entity, gate tuning, a `tool.jev` envelope.
The two sibling PRDs own the middle three.

## Acceptance

- [ ] `jev.ctg/cartridge.json` exists, the profile lists `jev`, and
      `just audit jev` and `just isolation` exit 0. *(Path A adds: `.gitmodules`
      names `jev.ctg`.)*
- [ ] `needs` is exactly `auth.jev?` and `memo?`; `grant` has no `net` and no
      `env`; no setting names a key, URL or model.
- [ ] `type/judgement.md` and one `judgement/*.md` instance ship, and the
      shipped instance passes jev's own `validate`.
- [ ] The eleven named tests below pass.
- [ ] `jev.decided` is declared with `additionalProperties: false` and no
      `state` property.
- [ ] `README.md` has at least ten non-blank lines; `.cartridge/help.md` has
      `## Use` and names the `judgement` kind.

## Verify and Proof

Both passes run from the superproject root (lane, then live checkout). No
cargo anywhere, so no `CARGO_TARGET_DIR`. No block writes inside the footprint:
`bun test` needs no install (the tests import only `bun:test`, `node:stream`
and jev's own `src/`), and `tsc` is deliberately not run here because it would
need `bun install` to write `jev.ctg/node_modules`. `just check jev` /
`just test jev` are not used: `.cartridge/justfile:100-101` hardcode target
lists without `jev` and that file is outside the footprint (same as `web`).
`just isolation` is called explicitly because no owner gate runs it.
`cartridge help jev` is not run: a new manifest is untrusted and the picker
never returns in a non-tty. No guard is `! grep` or an `a && b` list.

### Block 1 — declaration, profile, record, documentation, gates

```sh
test -f jev.ctg/init.lua
test -f jev.ctg/src/main.ts
test -f jev.ctg/src/jev.ts
test -f jev.ctg/src/wire.ts
test -f jev.ctg/.cartridge/tests/integration/node.ts
test -s jev.ctg/.cartridge/help.md
test "$(awk 'NF' jev.ctg/README.md | wc -l | tr -d ' ')" -ge 10
grep -q '^## Use' jev.ctg/.cartridge/help.md
grep -q 'judgement' jev.ctg/.cartridge/help.md
grep -q 'id = "jev", path = "jev.ctg"' .cartridge/init.lua
grep -q '^type: judgement$' jev.ctg/.cartridge/memos/type/judgement.md
grep -q '^kind: type$' jev.ctg/.cartridge/memos/type/judgement.md
# A cartridge includes no sibling's file.
if grep -rqnE '\.\./[a-z]+\.ctg' jev.ctg/src jev.ctg/.cartridge/tests jev.ctg/init.lua jev.ctg/package.json jev.ctg/tsconfig.json; then exit 1; fi
bun -e '
  const fs = require("node:fs");
  const m = JSON.parse(fs.readFileSync("jev.ctg/cartridge.json", "utf8"));
  const bad = (why) => { console.error("manifest: " + why); process.exit(1); };
  if (m.name !== "jev" || !m.description) bad("name or description");
  const needs = JSON.stringify([...(m.needs || [])].sort());
  if (needs !== JSON.stringify(["auth.jev?", "memo?"])) bad("needs is " + needs);
  if (JSON.stringify(m.listen) !== JSON.stringify(["jev"])) bad("listen");
  const g = m.grant || {};
  for (const k of ["net", "env", "read", "write"]) if ((g[k] || []).length) bad("grant." + k + " is not empty");
  if (JSON.stringify(g.exec) !== JSON.stringify(["bun"])) bad("grant.exec");
  for (const [n, e] of Object.entries(m.events || {})) if (!e.description || !e.schema) bad("event " + n + " lacks a description or a schema");
  const d = (m.events || {})["jev.decided"];
  if (!d) bad("jev.decided is not declared");
  if (d.schema.additionalProperties !== false) bad("jev.decided admits undeclared fields");
  if ("state" in (d.schema.properties || {})) bad("jev.decided declares state");
  for (const [n, s] of Object.entries(m.settings || {})) {
    if (!s.type || !s.doc) bad("setting " + n + " lacks a type or a doc");
    if (/key|url|host|model|token|secret/i.test(n)) bad("setting " + n + " names a credential, a destination or a model");
  }
  if (!(m.settings || {}).timeout_ms) bad("no timeout_ms setting");
  const dir = "jev.ctg/.cartridge/memos/judgement";
  const shipped = fs.readdirSync(dir).filter((f) => f.endsWith(".md"));
  if (shipped.length < 1) bad("no example judgement ships");
'
env -u CARTRIDGE_YOLO just audit jev
env -u CARTRIDGE_YOLO just isolation
```

### Block 2 — the named tests

Test names are the contract; the bodies are the diff reviewer's. Each body must
assert on what `serve()` returned through the fake node, never on a value the
test built itself, and the three failure tests must `await` the call without a
`try` around it, so a throw into the caller fails them.

```test
run: bun test ./jev.ctg/.cartridge/tests/integration/decide.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: a confidence above act returns act
pass: a confidence between the gates returns caution
pass: a confidence below escalate returns escalate
pass: the weakest answer decides the verdict and the confidence
pass: an unavailable auth.jev returns escalate with a reason and does not throw
pass: an auth.jev that never answers returns escalate with reason timeout
pass: an unknown point returns escalate with a reason and asks auth.jev nothing
pass: jev.decided is published for every decision and carries no state
pass: declare refuses a judgement with a question that has no gate
pass: declare refuses a judgement with no fallback
pass: the shipped example judgement is valid
```

The timeout test applies `{timeout_ms: 20}` and a fixture `auth.jev` that never
answers; it must finish well inside bun's 5 s default. The `carries no state`
test sends a `state` holding a marker string and asserts the marker appears
nowhere in `JSON.stringify` of any frame the fake node collected in `loose`.

### By hand after collect (not gateable from a block)

`cartridge trust` the project again (a new manifest and a changed profile
untrust it, and `just launch`'s prompt never waits), then
`cartridge help jev`, then
`cartridge call jev '{"op":"decide","point":"example-needs-an-llm","state":"…","cwd":"'$PWD'"}'`
with auth's TypeSafe entry absent: it must answer `verdict: "escalate"`,
`reason: "unavailable: …"`, exit 0. Then `just audit` across all cartridges
and `cd jev.ctg && bun install && bun run check` for the type check.

## Dependencies and base

- Hard: `@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key` done, so
  the answer shape in the fixture is the recorded one, not a guess.
- The ASP need on the PRD is satisfied by `cartridge.ctg` `7af748a`; this leaf
  uses nothing from it.
- Shared file that forces serial integration: `.cartridge/init.lua` (one line)
  — it is modified in the live checkout today (`git status`), so the
  coordinator checks for a foreign staged or dirty hunk before collect.
- Both sibling PRDs share `jev.ctg/**` and therefore serialize behind this one.
