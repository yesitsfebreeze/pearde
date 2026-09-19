---
complexity: 3
footprint:
  - "cartridge.json"
  - "init.lua"
  - "package.json"
  - "tsconfig.json"
  - ".gitignore"
  - "bun.lock"
  - "README.md"
  - "src"
  - ".cartridge"
---

# spec01 — jev.ctg answers a declared judgement with a gated verdict and fails open

## Base

- **Repository.** The PRD's `repo` is `/Users/feb/dev/cartridge/jev.ctg`, its own
  repository. It is a submodule at superproject `ea8ecdb`. The lane is cut in
  `jev.ctg` from the seed `790fb65`, which is an empty commit with no files and
  no remote.
- **Paths.** Every path below is relative to the `jev.ctg` root.
- **Siblings.** Nothing here reaches a sibling, so the lane needs no sibling
  symlinks.
- **Revisions read.** `cartridge.ctg` `d04ab33`, `memo.ctg` `4f8903d` and
  `auth.ctg` `c5e8871`.

A note on the pinned line numbers. `plan.rs:324-333` and `mod.rs:390-399` are
at `cartridge.ctg` `d04ab33`. `document.rs:183` and `asp.txt:122` are also at
`d04ab33`. `record.rs:705-751` is at `memo.ctg` `4f8903d`.

## Load order: why the fixture comes first and the profile line waits

The base refuses to start a cartridge whose need names an event that no
cartridge declares, and that holds for an optional need too.
`cartridge.ctg/src/host/plan.rs:324-333` (`unmatched`) checks every entry in
`needs`, and the `?` has already been stripped by then. `src/host/mod.rs:390-399`
then marks the slot `Failed`.

So jev cannot start in a composition until `auth.jev` is declared, which
happens when `@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key` is
collected. This leaf is built and tested entirely against a fixture `auth.jev`.
The profile line and every live step belong to the coordinator's post-collect
section below.

## The contract jev codes against

This is pinned from the `auth.jev` spec01.

- **Request.** `auth.jev {state, questions, model?}`.
  - `questions` is a map keyed by the caller's ids, each value
    `{type: "noul"|"choice"|"score", instructions, criteria?}`.
  - jev never sends `model`.
- **Answer.** `{answers, usage}`, with `answers` a map under the same ids.
  - A noul answer is `{type: "noul", noul: p}` and has no `confidence`.
  - Choice and score answers carry `probabilities` and a `confidence`.
- **Failure.** A rejected ask whose message starts with `invalid`,
  `unavailable`, `unreachable`, `upstream`, `rate_limited` or `overloaded`.
  - The host's own outcomes arrive in host wording with no type word: schema
    refusal, `timed_out`, cartridge absent and cartridge untrusted.
  - jev uses the message as its `reason` unchanged, with no added prefix.
- **Timing.** `auth.jev`'s event `timeout_ms` is 20000 and its in-process
  deadline is 15000. Auth retries 429 and 529 itself, inside that deadline.

## jev's own time bound

- **The setting.** `timeout_ms`: integer, default `3000`, `min: 1`, `max: 8000`.
- **The event bound.** `events.jev.timeout_ms` is `10000`. Because the setting's
  max of 8000 sits below it, jev answers before the host reports `timed_out` to
  jev's caller.
- **The default is provisional.** 3000 allows auth's first 500 ms backoff and
  one doubling. Reset it from the latency that auth's live probe records in its
  evidence note. The value lives in `cartridge.json` only, never as a second
  copy in code.
- **One timer per `decide`.** It starts on entry and covers the memo read and the
  `auth.jev` call together. When it fires, the caller gets `verdict: "escalate"`
  with `reason: "timeout: no answer within <n> ms"`.
- **A late answer is dropped.** Its promise settles and nothing reads it. There
  is no second `jev.decided`, no retry, and the call's `usage` is not recorded.
  Auth keeps working until its own 15000 ms deadline, because a caller cannot
  cancel a cartridge call.

## Files

All files are new. The scaffolding is copied from `web.ctg` as text; nothing
imports, symlinks or reaches `../web.ctg`.

| File | Content |
| --- | --- |
| `cartridge.json` | below |
| `init.lua` | `web.ctg/init.lua` with the listen list `{ "jev" }` |
| `package.json`, `tsconfig.json` | as `web.ctg`, with the name `@cartridge/jev` |
| `.gitignore` | `/node_modules/`, `.env`, `.DS_Store` |
| `.cartridge/.gitignore` | `web.ctg`'s whitelist (`/*`, `!/.gitignore`, `!/docs/`, `!/help.md`, `!/memos/`, `!/tests/`, `/memos/.lock`) |
| `bun.lock` | written once by `bun install`, then committed, so Verify can install `--frozen-lockfile` |
| `src/wire.ts` | jev's own copy of `web.ctg/src/wire.ts` |
| `src/jev.ts` | `validate`, `confidenceOf`, `gate`, `render`, `decide` |
| `src/main.ts` | `export function serve(wire)` and `if (import.meta.main) serve(new Wire());` |
| `.cartridge/memos/type/judgement.md` | the kind declaration |
| `.cartridge/memos/judgement/example-needs-an-llm.md` | the one example instance |
| `.cartridge/tests/integration/node.ts` | jev's own fake node (see N1 below) |
| `.cartridge/tests/integration/decide.test.ts` | the named tests |
| `README.md`, `.cartridge/help.md` | The README has at least ten non-blank lines. The help page has `## Use` and `## Read next`, and names the `judgement` kind. |

All of these sit in the audit's allowed root set, so none shows up as a stray
root entry.

### `cartridge.json`

- **Identity.** `name: "jev"`, `entry: "init.lua"`, a `description`, and
  `listen: ["jev"]`.
- **`needs`.** Exactly `["auth.jev?", "memo?"]`, never `asp`. `asp` is the
  base's own key, so no cartridge may declare it (`cartridge.ctg/docs/asp.txt`,
  REACHING IT; `src/loader/document.rs:183`).
- **`events.jev`.**
  - Every event has a `description` and a `schema`.
  - `additionalProperties: false`.
  - `op` is `decide` or `declare`. `decide` requires `point`, `state` and
    `cwd`; `declare` requires `point`, `judgement` and `cwd`.
  - `state` is `{"type": ["string", "object", "array"]}`, as in auth.
  - `point` has the pattern `^(@[a-z0-9-]+/)?[a-z0-9-]+$`.
  - `timeout_ms: 10000`.
- **`events["jev.decided"]`.** jev emits it and does not listen to it.
  - `additionalProperties: false`.
  - The properties are exactly `decision_id`, `point`, `verdict` (enum `act`,
    `caution`, `escalate`), `confidence`, `answers`, `usage` (object or null),
    `latency_ms` and `reason`.
  - All are required except `reason`, which is optional.
  - There is no `state`.
- **`settings.timeout_ms`.** As in "jev's own time bound", with a `doc` line. No
  setting name contains `key`, `url`, `host`, `model`, `token` or `secret`.
- **`grant`.** `{ "exec": ["bun"] }` and nothing else.
- **`commands`.** `check` is `bun run check` and `test` is `bun test`, both with
  `cwd: "."`.

### The `judgement` kind

An instance's frontmatter holds these fields:

- `kind: judgement` and a `description`.
- `questions`: a non-empty map from an id matching `^[a-z0-9_]+$` to
  `{type, instructions, criteria?}`, in auth's exact shape.
- `gates`: exactly the same ids, each mapped to `{act, escalate}` with
  `0 <= escalate <= act <= 1`.
- `fallback`: non-empty text naming the path that decides today.

The body is a `## Criteria` section. The type memo also states jev's noul
measure (below): it is not the API's confidence, and a judgement that needs
the API's confidence asks a two-option `choice` instead.

`validate(j)` returns the first problem as text, or null. It is the one
function behind both `declare` and `decide`, and it catches:

- a missing or empty `questions` map;
- a question type other than the three;
- empty `instructions`;
- a question without a gate, or a gate without a question;
- a gate out of range, or one where `escalate > act`;
- an empty `fallback`.

memo enforces no fields of a kind (`memo.ctg/src/record.rs:705-751`), and a
kind that a cartridge ships supplies that kind's name for workspace writes.

### `declare`

1. Run `validate`. On a problem, throw `invalid judgement: <problem>`. This is
   the only op that throws.
2. A qualified `@owner/…` point is refused as
   `invalid judgement: declare writes the workspace record only`.
3. `render` builds the memo text. Each frontmatter field is written as
   `key: <JSON.stringify(value)>`, which is YAML flow, so no YAML dependency
   is needed. The body is `## Criteria`.
4. Call `wire.call("memo", {op: "write", cwd, path: "judgement/<point>.md", body})`.

### `decide`

1. `decision_id = crypto.randomUUID()`. Start the clock and the one timer.
2. Call `memo {op: "read", cwd, path}`, where `path` is `judgement/<name>.md`,
   or `@owner/judgement/<name>.md` for a qualified point.
   - If memo rejects the read, the reason is
     `unknown point: <point> (<memo message>)`.
   - If the judgement fails `validate`, the reason is
     `invalid judgement: <problem>`.
3. Call `wire.call("auth.jev", {state, questions})`. If the ask is rejected, its
   message is the reason, unchanged.
4. **Shape check (B2).** This check runs before any gate.
   - If the reply is not a non-null object whose `answers` is a non-null
     object that is not an array (`!Array.isArray`), the reason is `upstream: auth.jev gave no answers`.
   - Otherwise take each declared id in declaration order. If `confidenceOf`
     returns null for it, the reason is
     `upstream: auth.jev gave no answer for <id>`.
   - Either reason produces `escalate`, whatever the gates say.
5. **`confidenceOf(answer)`.**
   - For `type: "noul"` with a finite numeric `noul` p, it returns
     `p >= 0.5 ? p : 1 - p`. This is jev's own measure: it matches TypeSafe's
     symmetric yes, uncertain and no band on p, but it is on a different scale
     from the API's `confidence`.
   - For `choice` and `score`, it returns a finite numeric `confidence`.
   - For anything else, it returns null.
6. **`gate(c, g)`.** `act` when `c >= g.act`, `escalate` when `c < g.escalate`,
   and `caution` otherwise.
7. **The weakest answer decides.** Write it as exactly these two lines, with
   `VERDICTS = ["act", "caution", "escalate"] as const`. `src/jev.ts` holds no
   other `Math.max(` or `Math.min(`.

   ```ts
   const verdict = VERDICTS[Math.max(...rows.map(r => VERDICTS.indexOf(r.verdict)))];
   const confidence = Math.min(...rows.map(r => r.confidence));
   ```
8. **Exit.** Steps 2 to 7 run as one `async` body raced against the timer.
   Every outcome passes through one `finish()`, which does two things:
   - emits `jev.decided` with `{decision_id, point, verdict, confidence,
     answers, usage, latency_ms, reason?}` and no state;
   - returns `{answers, confidence, verdict, decision_id, reason?}`.

   A failure gives `answers: {}`, `usage: null`, `confidence: 0` and
   `verdict: "escalate"`. `decide` never throws.

**`apply` (N2).** It keeps the settled config. It throws
`jev: config.timeout_ms must be an integer` unless `timeout_ms` is an integer.
The host always settles the declared value, so this guards against a missing
config rather than re-checking the declared bound.

**`node.ts` (N1).** It is jev's own copy of the fake node, with one change:
when the `serve` callback it is given returns a promise, it awaits that promise
before it writes `{ask, result}` or `{ask, error}`. That is how a fixture
`auth.jev` can answer late or reject asynchronously.

**Not built.** The README gives one line each to what this leaf leaves out:
- retries, which auth owns;
- caching;
- ASP slices and the `decision:` entity, which belong to sibling PRDs;
- tuning the gates;
- a `tool.jev` envelope.

## Acceptance

These map one to one onto the PRD's five boxes.

- [x] **Box 1: the manifest.**
  - `needs` is exactly `auth.jev?` and `memo?`, and `grant` is exactly
    `{exec: ["bun"]}`.
  - `jev.decided` is declared with `additionalProperties: false`, an optional
    `reason` and no `state`.
  - No sibling's file is included.
  - Every hard check of the audit passes except the profile entry: the manifest
    parses; there is a description; every event has a description and a schema;
    every setting has a type and a doc line.

  Checked by Block 1.
- [x] **Box 2: declare and the example.** `declare` refuses a judgement without
  a gate or without a fallback, and the shipped example is valid. Checked by
  the named tests in Block 2, plus the kind declaration grep in Block 1.
- [x] **Box 3: each verdict and the weakest answer.** Named tests against the
  fixture `auth.jev` cover act, caution and escalate, and a request whose
  weakest answer decides the result. They are in Block 2, and Block 4, the
  mutant, proves the weakest-answer test would catch a wrong fold.
- [x] **Box 4: fail-open.** An unavailable, late, null or partial `auth.jev`
  answer, and an unknown `point`, each return `escalate` with a reason and
  never throw. Checked by the named tests in Block 2.
- [x] **Box 5: documentation.** `README.md` has at least ten non-blank lines, and
  `.cartridge/help.md` is non-empty, has `## Use` and names the `judgement`
  kind. Checked by Block 1. `bun run check` passing is checked by Block 3.

## Verify and Proof

- **Where the blocks run.** Every block runs from the `jev.ctg` root, first in
  the lane cut from `790fb65` and then in the live `jev.ctg`. Each runs as
  `sh -eu -c` with no injected environment.
- **What they write.**
  - No cargo runs, so `CARGO_TARGET_DIR` never comes up.
  - Block 3 writes only `node_modules/`, which `.gitignore` ignores. Collect
    counts only tracked diffs and non-ignored untracked files
    (`prd.ctg/src/lifecycle.ts:242`, `--exclude-standard`).
  - Block 4 writes only under `${TMPDIR:-/tmp}`.
- **What they leave out (B3).**
  - `just audit jev` and `just isolation` do not run here. Block 1 covers their
    hard checks and the check for included sibling files, and the coordinator
    runs both after collect.
  - `just check` and `just test` do not resolve `jev` yet.
  - `cartridge help` never waits for a terminal, so it is not used.
- **Guards.** No guard is written as `! grep` or `a && b`.

### Block 1: declaration, record, documentation, audit's hard checks, isolation

```sh
test -f init.lua
test -f bun.lock
test -f src/main.ts
test -f src/jev.ts
test -f src/wire.ts
test -f .cartridge/tests/integration/node.ts
test -f .cartridge/tests/integration/decide.test.ts
test "$(awk 'NF' README.md | wc -l | tr -d ' ')" -ge 10
test -n "$(tr -d '[:space:]' < .cartridge/help.md)"
grep -q '^## Use' .cartridge/help.md
grep -q 'judgement' .cartridge/help.md
grep -q '^type: judgement$' .cartridge/memos/type/judgement.md
grep -q '^kind: type$' .cartridge/memos/type/judgement.md
grep -q '^/node_modules/$' .gitignore
if grep -rqnE '(\.\./)+[a-z0-9-]+\.ctg' src .cartridge/tests init.lua package.json tsconfig.json cartridge.json; then echo "jev includes a sibling's file" >&2; exit 1; fi
if find . -path ./node_modules -prune -o -path ./.git -prune -o -type l -print | grep -q .; then echo "jev ships a symlink" >&2; exit 1; fi
bun -e '
  const fs = require("node:fs");
  const bad = (why) => { console.error("manifest: " + why); process.exit(1); };
  let m;
  try { m = JSON.parse(fs.readFileSync("cartridge.json", "utf8")); } catch (e) { bad("does not parse: " + e.message); }
  if (m.name !== "jev") bad("name");
  if (m.entry !== "init.lua") bad("entry");
  if (!m.description) bad("no description");
  const needs = JSON.stringify([...(m.needs || [])].sort());
  if (needs !== JSON.stringify(["auth.jev?", "memo?"])) bad("needs is " + needs);
  if (JSON.stringify(m.listen) !== JSON.stringify(["jev"])) bad("listen");
  if (JSON.stringify(m.grant) !== JSON.stringify({ exec: ["bun"] })) bad("grant is " + JSON.stringify(m.grant));
  for (const [n, e] of Object.entries(m.events || {})) {
    if (!e || typeof e !== "object") bad("event " + n + " is not a declaration");
    if (!e.description) bad("event " + n + " declares no description");
    if (!e.schema) bad("event " + n + " declares no schema");
  }
  const j = (m.events || {}).jev;
  if (!j) bad("jev is not declared");
  if (j.schema.additionalProperties !== false) bad("jev admits undeclared fields");
  if (JSON.stringify(j.schema.properties.state.type) !== JSON.stringify(["string", "object", "array"])) bad("jev.state type");
  const d = (m.events || {})["jev.decided"];
  if (!d) bad("jev.decided is not declared");
  if (d.schema.additionalProperties !== false) bad("jev.decided admits undeclared fields");
  const props = Object.keys(d.schema.properties || {}).sort();
  if (JSON.stringify(props) !== JSON.stringify(["answers", "confidence", "decision_id", "latency_ms", "point", "reason", "usage", "verdict"])) bad("jev.decided properties are " + props);
  if ((d.schema.required || []).includes("reason")) bad("reason must be optional");
  for (const [n, s] of Object.entries(m.settings || {})) {
    if (!s || typeof s !== "object") bad("setting " + n + " is not a declaration");
    if (!s.type) bad("setting " + n + " declares no type");
    if (!s.doc) bad("setting " + n + " declares no doc line");
    if (/key|url|host|model|token|secret/i.test(n)) bad("setting " + n + " names a credential, a destination or a model");
  }
  const t = (m.settings || {}).timeout_ms;
  if (!t) bad("no timeout_ms setting");
  if (!Number.isInteger(t.max)) bad("timeout_ms has no integer max");
  if (!Number.isInteger(j.timeout_ms)) bad("events.jev has no integer timeout_ms");
  if (t.max >= j.timeout_ms) bad("setting max " + t.max + " is not below events.jev.timeout_ms " + j.timeout_ms);
  if (fs.readdirSync(".cartridge/memos/judgement").filter((f) => f.endsWith(".md")).length < 1) bad("no example judgement ships");
'
```

### Block 2: the named tests

```test
run: bun test ./.cartridge/tests/integration/decide.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: a confidence above act returns act
pass: a confidence between the gates returns caution
pass: a confidence below escalate returns escalate
pass: the weakest answer decides the verdict and the confidence
pass: a noul confidence is p or one minus p whichever is larger
pass: an unavailable auth.jev returns escalate with its message as the reason and does not throw
pass: an auth.jev that answers after timeout_ms returns escalate with a timeout reason
pass: an auth.jev that answers null returns escalate with a reason
pass: an auth.jev answer missing a declared question returns escalate with a reason naming it
pass: an unknown point returns escalate with a reason and asks auth.jev nothing
pass: jev.decided is emitted for every decision and carries no state
pass: declare refuses a judgement with a question that has no gate
pass: declare refuses a judgement with no fallback
pass: the shipped example judgement is valid
```

What each body must pin. The diff reviewer is the backstop.

- **Every test.** Each one applies `{timeout_ms: <integer>}` first (N2), and
  asserts on what `serve()` answered through the fake node.
- **Fail-open tests.** They `await` the call without a `try` around it.
- **Verdicts.** One `choice` question with gates `{act: 0.8, escalate: 0.4}`,
  answered at 0.9, 0.6 and 0.2.
- **Weakest answer.** A choice at 0.95 and a choice at 0.5 with gates 0.8 and
  0.3 must give `caution` with confidence 0.5. Run it with the weak question
  listed second, then again listed first.
- **Noul.** `noul: 0.1` under `{act: 0.85, escalate: 0.5}` gives confidence 0.9
  and `act`.
- **Unavailable.** The fixture rejects with
  `unavailable: no cartridge/typesafe/api-key entry`, and `reason` equals that
  string exactly.
- **Timeout.** Apply `{timeout_ms: 20}`, with a fixture that answers after
  200 ms. The call must come back in under 200 ms with a `timeout:` reason.
  After the late answer arrives, `loose` must hold exactly one `jev.decided`
  for that `decision_id`.
- **Null.** The fixture resolves `null`: `escalate`, and `reason` starts with
  `upstream:`. Resolving `{answers: []}` gives the same.
- **Partial.** Two declared ids, where the fixture answers one with
  `confidence: 0.99` and omits the other. Gates `{act: 0, escalate: 0}` would
  otherwise give `act`. The result must be `escalate`, with a `reason`
  containing the missing id. Repeat with the second id present but its
  `confidence` a string.
- **Unknown point.** The `memo` fixture rejects, and no `auth.jev` ask is seen.
- **`jev.decided` (N3).** The test reads the declared property names from
  `cartridge.json` at run time. Each `jev.decided` frame's keys must be a
  subset of them, and a marker placed in `state` must appear in no frame in
  `loose`.
- **Declare.** The refusal starts with `invalid judgement:`, and the `memo`
  fixture saw no write.
- **Example.** Parse the shipped file's `key: <JSON>` frontmatter lines;
  `validate` must return null.

### Block 3: types

```sh
bun install --frozen-lockfile
bun run check
```

### Block 4: the weakest-answer mutant (N4)

This block proves that the weakest-answer test would fail if the fold kept the
strongest answer instead.

```sh
m="$(mktemp -d "${TMPDIR:-/tmp}/jevmut.XXXXXX")"
trap 'rm -rf "$m"' EXIT
cp -R . "$m/jev"
cd "$m/jev"
test "$(grep -c 'Math.max(' src/jev.ts)" -eq 1
test "$(grep -c 'Math.min(' src/jev.ts)" -eq 1
bun test ./.cartridge/tests/integration/decide.test.ts -t 'the weakest answer decides the verdict and the confidence'
cp src/jev.ts "$m/jev.ts.orig"
sed -e 's/Math\.max(/MATH_SWAP_A(/' -e 's/Math\.min(/Math.max(/' -e 's/MATH_SWAP_A(/Math.min(/' "$m/jev.ts.orig" > src/jev.ts
if cmp -s src/jev.ts "$m/jev.ts.orig"; then echo "the anchor did not match; the mutant changed nothing" >&2; exit 1; fi
test "$(grep -c 'Math.max(' src/jev.ts)" -eq 1
if bun test ./.cartridge/tests/integration/decide.test.ts -t 'the weakest answer decides the verdict and the confidence'; then echo "MUTANT SURVIVED: the weakest-answer test passes when the strongest answer decides" >&2; exit 1; fi
```

Each step rules out one way the block could pass for the wrong reason:

- The unmutated run passes first, so a failure after the swap comes from the
  swap and not from the environment.
- `cmp` catches an anchor that matched nothing.
- The `cd` goes into the temporary copy only, never into a checkout.
- The noul measure is written as a ternary (N7), so the fold holds the only
  `Math.max(`.

## Post-collect (coordinator, by hand, in order)

Do these only after both this PRD and
`@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key` are collected.

1. List every uncommitted `cartridge.json` and `*.lua` in the superproject and
   its submodules (`git status --porcelain -- '*.lua' '*/cartridge.json'` and
   `git submodule foreach --quiet 'git status --porcelain -- cartridge.json "*.lua"'`).
   A project trust records all of them, so any foreign half-done edit waits
   or is cleared by its owner first.
2. Announce a short window to every running session.
3. Add `{ id = "jev", path = "jev.ctg" },` after `memo` in the superproject's
   `.cartridge/init.lua`, and run `cartridge trust` for the project, with no
   path, straight after. Trusting `jev.ctg` alone is not enough: every CLI
   command re-checks `init.lua` against the project record
   (`cartridge.ctg` `src/cli/project.rs:23-28`, `src/trust/mod.rs:120-155`), so
   an untrusted `init.lua` stops `cartridge` for every session. Bump the
   `jev.ctg` gitlink.
4. Check status without a terminal. `cartridge status` prints a JSON array,
   and this must print `active`:
   `cartridge status | jq -r '.[] | select(.id=="jev") | .state'`.
5. Run `cartridge call jev '{"op":"decide","point":"@jev/example-needs-an-llm","state":"x","cwd":"/Users/feb/dev/cartridge"}'`.
   It must exit 0. Record which outcome came back: a real verdict when the
   TypeSafe entry is stored, or `verdict: "escalate"` with auth's
   `unavailable: …` reason when it is not.
6. Run `env -u CARTRIDGE_YOLO just audit jev` and
   `env -u CARTRIDGE_YOLO just isolation`, and record both in `collection.md`,
   then commit it in `prd.ctg`.

## Dependencies

- **ASP PRD.** Satisfied, and not used by this leaf.
- **Auth PRD.** Only the post-collect section needs it. The lane builds and
  tests without it.
- **Siblings.** The sibling PRDs, and the leaf that registers jev in the
  gates, come after this one.
