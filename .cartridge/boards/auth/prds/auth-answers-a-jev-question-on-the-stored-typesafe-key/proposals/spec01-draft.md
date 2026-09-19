---
complexity: medium
footprint:
  - src/jev.ts
  - src/openai.ts
  - src/main.ts
  - init.lua
  - cartridge.json
  - README.md
  - .cartridge/help.md
  - .cartridge/docs/README.md
  - .cartridge/tests/integration/jev.test.ts
---

# spec01 — `auth.jev` posts a state and typed questions to TypeSafe on the stored key and returns the answers

Pre-draft, written while the PRD is blocked on
`@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values`.
Base read: `auth.ctg` at `d8751088bb8b0884ff641e027855d82257ee8ff0`, working
tree clean. The prerequisite is specced and not implemented, so its
`specs/spec01.md` is the contract this draft builds on. Nothing here was
built. Every claim is source evidence or a fetched document unless it says
"inferred" or "assumed".

## Two things the coordinator settles before this is claimable

1. **`init.lua` is outside the PRD footprint and must be inside it.** The
   footprint is `src/**`, `cartridge.json`, the three docs and
   `.cartridge/tests/**`. `init.lua:12` registers each served event by name:
   `for _, name in ipairs({ "auth", "auth.live" }) do cartridge.listen(name, …)`.
   An event in the manifest's `listen` that `init.lua` never registers has no
   listener. There is no way around the one-word edit, so the PRD footprint
   gains `init.lua`.
2. **`questions` and `answers` are maps, not lists.** See "API facts". The
   consumer draft (`jev-answers-a-declared-judgement…/proposals/spec01-draft.md`)
   describes a judgement's `questions` as "a non-empty list … each with an
   `id`". `auth.jev` passes `questions` through untouched, so the consumer
   either stores a map keyed by id, or converts its list before it calls. The
   choice is the consumer's. This spec only fixes that `auth.jev` takes and
   returns the API's maps.

## What this spec calls from the prerequisite

Revalidate these four lines when `src/pass.ts` lands. Nothing else of the
prerequisite is used, and `list(deps)` is not called at all.

- `entry("typesafe")` from `src/pass.ts`, relying on the default field
  `"api-key"`, returning the string `cartridge/typesafe/api-key`.
- `read(name, deps)` from `src/pass.ts`, returning
  `{ state: "available" | "missing_store" | "missing_entry" | "locked"; value?: string; message: string }`,
  with `deps` being `{ env?, home?, timeoutMs? }` and gpg spawned only after
  the entry file exists.
- `Dependencies` in `src/openai.ts` already carrying `env`, `home`, `fetch`
  and, after the prerequisite, `timeoutMs`.
- `grant.exec` being `["bun","gpg"]` after the prerequisite. This spec leaves
  it alone and asserts it.

## API facts

Fetched 2026-09-19 as raw markdown with `curl` (HTTP 200 each):
`api.md`, `models.md`, `confidence.md`, `primitives/noul.md`,
`sdk/javascript/api/interfaces/RetryPolicy.md`,
`sdk/javascript/api/classes/APIError.md`, `sdk/python/api/exceptions.md`,
`cookbooks/consistency_noul_cookbook.md`, all under `https://docs.typesafe.ai/`.

**Confirmed from the documents.**

Request, `POST https://api.typesafe.ai/v1/systemone`, headers
`Authorization: Bearer <API_KEY>` and `Content-Type: application/json`:

```json
{
  "state": "Help! My payouts have been failing for 3 days.",
  "model": "jev-latest",
  "questions": {
    "is_urgent":   { "type": "noul",   "instructions": "Does this convey urgency?",
                     "criteria": { "true": "Explicitly time-sensitive", "false": "No urgency expressed" } },
    "department":  { "type": "choice", "instructions": "Which team should handle this?",
                     "criteria": { "billing": "Payments, invoicing, refunds", "technical": "Bugs, outages, integrations", "sales": null } },
    "frustration": { "type": "score",  "instructions": "How frustrated is the customer?",
                     "criteria": ["Calm", "Frustrated", "Very angry"] }
  }
}
```

- `state`: `string | object | array`, required. `model`: string, required by
  the API. `questions`: `map<string, Question>`, required. The caller chooses
  each key; "The key is not sent to the underlying model."
- Every question has `type` and `instructions` (`string | object | array`).
  `criteria` is optional `{true?, false?}` for `noul`, a required
  `map<string, string | null>` for `choice`, and a required array of at least
  two level descriptions for `score`.
- Models: `jev-latest` and `jev-preview`, both currently `jev-1.13.0`. Limits:
  64k tokens per request, 32k for `state` plus the longest question, 250,000
  tokens per second, 1,200 requests per minute, "adjusting dynamically".

Response, all three top-level fields required:

```json
{
  "model": "jev-latest",
  "answers": {
    "is_urgent":   { "type": "noul", "noul": 0.92 },
    "department":  { "type": "choice", "choice": "technical",
                     "probabilities": { "billing": 0.08, "technical": 0.85, "sales": 0.07 }, "confidence": 0.82 },
    "frustration": { "type": "score", "score": 1.6,
                     "legend": { "0": "Calm", "1": "Frustrated", "2": "Very angry" },
                     "probabilities": { "0": 0.05, "1": 0.3, "2": 0.65 }, "confidence": 0.78 }
  },
  "usage": { "input_tokens": 312, "output_tokens": 48 }
}
```

- `answers` is `map<string, Answer>` under the same ids. `usage` is
  `{input_tokens, output_tokens}`, both integers.
- Statuses: `401` missing or invalid key, `422` validation failure ("The body
  details the offending field"), `429` rate limit, `529` overloaded. For
  `429`/`529`: "retry the request with exponential backoff instead of
  retrying immediately."
- `models.md:19`: the SDKs "honor the `retry-after` header when the response
  carries one". The JS `RetryPolicy` page names two headers, `Retry-After`
  and `retry-after-ms`, and the SDK defaults: first delay 500 ms, doubled, cap
  5000 ms, jitter 0.25, 2 retries, retry on 408, 429 and 500–599.
- Errors carry an `x-typesafe-request-id` response header.

**Not documented, so assumed.**

- **The error body shape.** `api.md` says only "a JSON body describing what
  went wrong". The SDK types the body as `unknown`: "Parsed JSON, response
  text, or `undefined` for an empty body". No field name is published. This
  spec therefore never parses an error body and never forwards one, which is
  also the house rule (`src/openai.ts:125`, and the base test `failed upstream
  authorization is useful without echoing the upstream body`).
- **Whether a `429` or `529` actually carries `Retry-After`.** The documents
  say "when the response carries one". The code reads both headers and falls
  back to its own backoff when neither parses.
- The live probe (last Acceptance box) is what turns both assumptions into
  observations.

**How a confidence is obtained for a `noul` answer: it is not.**
`confidence.md:11`: "(Noul answers don't carry one.)" `primitives/noul.md:302`
is headed "Noul does not return a separate confidence value". A noul answer is
exactly `{type, noul}`, where `noul` is the probability of yes. `max(p, 1-p)`
is not an API statistic. Two facts for the consumer:

- It is not on the same scale as a Choice `confidence`. The documented example
  has a top probability of 0.85 and a `confidence` of 0.82, so TypeSafe's
  statistic is not the top probability, and its formula is unpublished
  ("a statistic computed from the probability distribution").
- TypeSafe's own noul cookbook gates on `p` directly with a band: below 0.30
  is no, 0.30 through 0.70 is uncertain, above 0.70 is yes, and it calls the
  band "illustrative … neither a calibrated guarantee nor an optimized
  threshold". A symmetric band is the same thing as thresholding
  `max(p, 1-p)`, so the consumer's formula is a fair application-side rule. It
  must be documented as jev.ctg's own measure, and a judgement that needs the
  API's confidence asks a two-option `choice` instead of a `noul`.

`auth.jev` returns a noul answer as the API gave it and synthesizes nothing.

## Acceptance

- [ ] The named test `auth.jev posts to the fixed path with the stored bearer and returns answers and usage unchanged` drives `auth.jev {state, questions}` over the wire against a loopback fixture server. It asserts one `POST` to path `/v1/systemone` with `Authorization: Bearer <fixture key>`, a JSON body of exactly `{state, model:"jev-latest", questions}`, that the code chose `https://api.typesafe.ai/v1/systemone`, that the only pass entry it asked for is `cartridge/typesafe/api-key`, and that the result equals `{answers, usage}` of a fixture response holding one noul, one choice and one score answer. A second call with `model:"jev-preview"` sends that model.
- [ ] The named test `a request naming a url or a host or a key is refused and nothing is fetched` sends three requests, each adding one of `url`, `host`, `key`. Each is refused, the fixture server saw no request, and no pass entry was read. `events["auth.jev"].schema` has `additionalProperties: false` and exactly the properties `state`, `questions`, `model`.
- [ ] The named test `a 429 then a 200 succeeds after one backoff` sees exactly two requests, the second no earlier than the fixture's `retry-after-ms` after the first, and gets the answers.
- [ ] The named test `a 529 on every attempt ends in a bounded overloaded failure` gets an error starting `overloaded:` within the injected deadline plus 250 ms, after at least three requests whose gaps grow.
- [ ] The named test `with no typesafe entry the call fails unavailable and nothing is fetched` uses the real `read` against an empty temporary home, gets an error starting `unavailable:` that names `cartridge/typesafe/api-key`, and the injected `fetch` was never called.
- [ ] The named test `an upstream error body that echoes the key never reaches the caller or the log` has the fixture answer `401` with the received bearer in its body. The error starts `upstream:`, and the fixture key appears in no result, no error, no loose frame and no captured stderr line, with the capture proven non-empty.
- [ ] `cartridge.json`: `grant.net` is `["api.openai.com","api.typesafe.ai"]`, `grant.exec` is unchanged, there is no `env` and no `write` grant, `listen` contains `auth.jev`, and `events["auth.jev"].timeout_ms` is greater than the exported in-process deadline and less than 60000.
- [ ] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` document `auth.jev`, the entry name and the failure words.
- [ ] By hand after collect: one live probe against the real API, recorded in the evidence note with its latency and `usage`.

## Steps

1. `src/jev.ts` (new, about 45 lines, imports only `./pass` and the
   `Dependencies` type):
   - `const DESTINATION = "https://api.typesafe.ai/v1/systemone"`, not
     exported and not configurable. `export const JEV_DEADLINE_MS = 15000`.
   - `export async function jev(args: any, deps: Dependencies): Promise<{answers: unknown; usage: unknown}>`.
   - First statement: every key of `args` must be one of `state`,
     `questions`, `model`, otherwise throw
     `invalid: auth.jev takes state, questions and an optional model`. The
     host already refuses such a payload at the sender and again on arrival
     (`cartridge.ctg/docs/transport.txt:40-44`, `jsonschema` in
     `src/loader/document.rs:192`). This line is the same refusal for a
     driver that reaches the helper without the host, and it is the only form
     of the box a test inside this repository can execute.
   - Start the clock, then
     `const found = await (deps.read ?? read)(entry("typesafe"), deps)`. Any
     state but `available` throws
     `unavailable: no TypeSafe key at cartridge/typesafe/api-key. <found.message>`.
     No request has been built at that point.
   - The loop, probed below: `fetch` with `method: "POST"`,
     `signal: AbortSignal.timeout(<time left>)`, the two headers, and the body
     `{state, model: args.model ?? "jev-latest", questions}`. A thrown fetch
     is `unreachable: TypeSafe did not answer.` A 2xx whose JSON lacks an
     object `answers` or an object `usage` is
     `upstream: TypeSafe returned an unreadable answer.` A 2xx returns
     `{answers: body.answers, usage: body.usage}` and nothing else. A status
     other than 429 and 529 is
     `upstream: TypeSafe refused the request (HTTP <n>).`, body unread.
   - On 429 or 529: `asked` is `retry-after-ms`, else `retry-after` times
     1000, else 0 (an HTTP-date form parses to `NaN` and falls to 0).
     `pause = max(wait, asked)`. If `elapsed + pause >= deadline`, throw
     `rate_limited: …` for 429 or `overloaded: …` for 529 now, rather than
     sleep past the bound. Otherwise sleep, then `wait = min(wait * 2, 5000)`.
     `wait` starts at `deps.jev?.backoffMs ?? 500`; the deadline is
     `deps.jev?.deadlineMs ?? JEV_DEADLINE_MS`.
   - One comment: `// ponytail: no jitter and no key cache. One gpg spawn per
     call; add a short TTL cache if the live probe's latency says so, and
     jitter if more than a handful of callers ever retry together.`
   - Failure words, as the prefix of the message because a wire error is a
     string (`src/wire.ts:95-98`, `init.lua:7`): `invalid`, `unavailable`,
     `unreachable`, `upstream`, `rate_limited`, `overloaded`. No message
     holds the key, a header or an upstream body.
2. `src/openai.ts`: `Dependencies` gains
   `read?: typeof import("./pass").read` and
   `jev?: { deadlineMs?: number; backoffMs?: number }`, both test seams in the
   sense of the existing `apiKey` comment (`:98`). `LiveAuth` gains
   `jev(args: unknown): Promise<{answers: unknown; usage: unknown}>`, and
   `OpenAIAuth` gains the one-line `jev(args) { return jev(args, this.deps); }`.
   The destination is not among the dependencies: the test injects `fetch`,
   records the URL the code chose and dials loopback, exactly as
   `live.test.ts:62` does with `socket`. `make` stays the only seam of
   `serve()` (`src/main.ts:4-7`).
3. `src/main.ts`: `wire.on("auth.jev", args => auth.jev(args));` next to the
   `auth` handler.
4. `init.lua:12`: the list becomes `{ "auth", "auth.live", "auth.jev" }`.
   Nothing else. The helper's per-request bound stays 60000 ms (`init.lua:3`,
   `cartridge.ctg/src/node/mod.rs:636-638,754`), which is why the event's
   `timeout_ms` must stay under it. `request` is an async method and the host
   drives listeners with `call_async`, so a call waiting in backoff does not
   hold auth's node and does not stall `auth.live` audio.
5. `cartridge.json`:
   - `events["auth.jev"]` with a `description`, `"timeout_ms": 20000`, and

     ```json
     { "type": "object", "required": ["state", "questions"], "additionalProperties": false,
       "properties": {
         "state": { "type": ["string", "object", "array"] },
         "questions": { "type": "object", "minProperties": 1,
           "additionalProperties": { "type": "object", "required": ["type", "instructions"],
             "properties": { "type": { "enum": ["noul", "choice", "score"] } } } },
         "model": { "type": "string" } } }
     ```

     A question object stays open inside, because the API owns `criteria` and
     may add fields. The host names the failing field for a malformed
     question, which is the feedback the unread 422 body would have given.
   - `listen` gains `auth.jev`. `grant.net` becomes
     `["api.openai.com","api.typesafe.ai"]`. The manifest `description` gains
     one clause about JEV. No setting is added: no key, URL, host or model
     setting exists for this event.
   - 20000 > 15000 so that auth answers with its own typed failure before the
     host reports `timed_out`; a consumer that stops waiting earlier leaves a
     call that ends by itself inside 15 s.
6. `.cartridge/tests/integration/jev.test.ts` (new), built like
   `live.test.ts`: `Bun.serve({ port: 0, hostname: "127.0.0.1" })` answering
   from a scripted list of `{status, headers?}` and recording
   `{method, path, authorization, body, at}` per request; `serve(wire, config => new OpenAIAuth(config, deps))`
   with `node()` from `./node`; cleanup and the stderr swap registered as
   `live.test.ts:65-70` does.
   - `deps.fetch` is `(input, init) => { dialled.push(String(input)); return fetch(mock.url + new URL(String(input)).pathname, init); }`.
   - `deps.read` is a fake that records each name and answers
     `{state:"available", value: DUMMY}` only for `cartridge/typesafe/api-key`
     and `missing_entry` for anything else. That is what makes a build that
     reads the OpenAI entry for TypeSafe fail the first test. The
     `unavailable` test passes no `read`, `env: {}` and a temporary `home`, so
     the real `read` answers `missing_store` and gpg is never spawned.
   - The backoff tests inject `jev: { backoffMs: 20 }` and, for 529,
     `deadlineMs: 400`; the 429 response carries `retry-after-ms: 70`.
   - Every assertion is on what came back through the fake node or on what
     the fixture server recorded, never on a value the test built itself.
   - The test file never reads `homedir()` and never names a real key.
7. Docs, in the same change. `README.md`: the opening paragraph, the three
   lists under `## Events`, and one `auth.jev` bullet under `## Use`.
   `.cartridge/help.md`: the opening paragraph and the same bullet.
   `.cartridge/docs/README.md`: one row in the contract table, and a short
   section stating the fixed destination, the entry
   `cartridge/typesafe/api-key` and `pass insert cartridge/typesafe/api-key`,
   that `questions` and `answers` are maps keyed by the caller's ids, that a
   noul answer has no `confidence`, the six failure words, the retry rule
   (429 and 529 only, 500 ms doubling to 5 s, `Retry-After` honoured, 15 s in
   all, 20 s at the host), and that auth neither caches the key nor reads or
   forwards an upstream error body.
8. The implementer runs three mutants by hand and records each exit in the
   evidence note: `entry("openai")` in `jev.ts`; the key whitelist removed;
   the `elapsed + pause >= deadline` test removed. Each must turn the suite
   red.

Not built, one line each in the docs: a generic `auth.fetch` (the PRD's
Decision), a key cache, jitter, retry on 5xx other than 529, a request size
check (the API answers 422), forwarding `model` or `x-typesafe-request-id`
from the response, a `tool.*` envelope.

## Probe results the design rests on

Run 2026-09-19, bun 1.3.14, cwd the analyst scratch directory, inline
`bun -e`, no file written, exit 0.

- The loop of step 1 against a loopback `Bun.serve`: `429` with
  `retry-after-ms: 70` then `200` gave 2 requests 71 ms apart, the documented
  answer back unchanged, path `/v1/systemone`, the bearer on the request, and
  `https://api.typesafe.ai/v1/systemone` recorded as the chosen destination.
- `529` throughout with `deadlineMs: 400`, `backoffMs: 20`: 5 requests, gaps
  21, 41, 82, 161 ms, then `overloaded: …` at 305 ms, because the next pause
  of 320 ms would have crossed the bound. The fixture echoed the bearer in its
  error body; the message did not contain it.
- `bun -e 'await import(process.cwd() + "/src/wire.ts")'` in `auth.ctg`
  resolved a TypeScript export, exit 0, tree still clean. Block 1 reads
  `JEV_DEADLINE_MS` the same way.

## Remaining risk

- The manifest schema was not compiled by the host in this draft. `type` as
  an array and `enum` are plain JSON Schema and `jsonschema` 0.56 is the
  validator (inferred, not probed). The first `cartridge trust` after collect
  is the check.
- Editing `cartridge.json` untrusts auth in a running daemon until the user
  trusts it again. Voice loses `auth` for that interval.
- Each call spawns gpg once. If the agent shows a pinentry, the pass bound
  (5 s by default) is spent inside the 15 s.
- The consumer draft turns any rejection into `unavailable: <message>`. Auth's
  message already begins with its own word, so that reason would read
  `unavailable: overloaded: …`. The consumer should pass auth's message
  through as the reason. That is an edit to the consumer draft, not to this
  one.
- The prerequisite's own Verify block asserts `grant.net` equals
  `["api.openai.com"]`. It runs only when that PRD is collected, which is
  before this one, so the two do not collide. Re-running it afterwards would
  fail by design.
- The third `pass:` regression line below names a test the prerequisite has
  yet to write. If its implementer renames it, that line is updated when this
  spec is revalidated.
- No mutant runs inside a Verify block: the anchors do not exist until the
  code does. Step 8 and the diff reviewer are the backstop for the test
  bodies; the `test` block pins the names.

## Verify and Proof

No cargo, so no `CARGO_TARGET_DIR`. Pass 2 writes only `node_modules/`
(gitignored, outside the footprint) and temporary directories the tests
remove. Nothing here reads an environment variable without a default. No
guard is `! grep` or an `a && b` list. No block reaches the network: the
tests dial loopback only.

```sh
test -f src/jev.ts
test -f .cartridge/tests/integration/jev.test.ts
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" -e '
const m = JSON.parse(require("node:fs").readFileSync("cartridge.json", "utf8"));
const { JEV_DEADLINE_MS } = await import(process.cwd() + "/src/jev.ts");
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const e = (m.events ?? {})["auth.jev"];
const ok = !!e && typeof e.description === "string" && e.description.length > 0
  && e.schema.additionalProperties === false
  && same(Object.keys(e.schema.properties).sort(), ["model", "questions", "state"])
  && same([...e.schema.required].sort(), ["questions", "state"])
  && Number.isInteger(JEV_DEADLINE_MS) && Number.isInteger(e.timeout_ms)
  && e.timeout_ms > JEV_DEADLINE_MS && e.timeout_ms < 60000
  && m.listen.includes("auth.jev")
  && same(m.grant.net, ["api.openai.com", "api.typesafe.ai"])
  && same(m.grant.exec, ["bun", "gpg"]) && m.grant.write === undefined && m.grant.env === undefined
  && Object.keys(m.settings ?? {}).every(name => !/key|url|host|model|token|secret/i.test(name));
if (!ok) process.exit(1);
'
grep -q '"auth.jev"' init.lua
for doc in README.md .cartridge/help.md .cartridge/docs/README.md; do
  grep -q 'auth\.jev' "$doc"
  grep -q 'cartridge/typesafe/api-key' "$doc"
  grep -q 'unavailable' "$doc"
done
# The destination is written once, in the one file that makes the call.
test "$(grep -rl 'api\.typesafe\.ai' src | tr '\n' ' ')" = "src/jev.ts "
# The test never reaches this machine's home.
if grep -qn 'homedir(' .cartridge/tests/integration/jev.test.ts; then exit 1; fi
```

```sh
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" install --frozen-lockfile
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" run check
# The real entrypoint, no injected dependency, no pass store: the call is
# refused as unavailable before any request, so this block needs no network.
out="$(printf '{"id":1,"call":"apply","args":{}}\n{"id":2,"call":"auth.jev","args":{"state":"s","questions":{"q":{"type":"noul","instructions":"?"}}}}\n' | env -u CARTRIDGE_YOLO PASSWORD_STORE_DIR=/nonexistent-pass-store "$CARTRIDGE_BUN" src/main.ts)"
printf '%s\n' "$out" | grep -q '"id":2,"error":"unavailable: '
```

```test
run: env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/ --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: auth.jev posts to the fixed path with the stored bearer and returns answers and usage unchanged
pass: a request naming a url or a host or a key is refused and nothing is fetched
pass: a 429 then a 200 succeeds after one backoff
pass: a 529 on every attempt ends in a bounded overloaded failure
pass: with no typesafe entry the call fails unavailable and nothing is fetched
pass: an upstream error body that echoes the key never reaches the caller or the log
pass: a WebSocket session relays, forwards and ends over the wire without disclosing the key
pass: shared credentials are discovered without leaking them into status
pass: status answers for any provider with source pass and the entry name and never the value
```

### By hand after collect (not gateable from a block)

This machine has no pass store, so none of this was attempted. It needs the
user's store and the user's TypeSafe key.

1. `pass insert cartridge/typesafe/api-key`, with the gpg-agent started
   outside the daemon (`gpgconf --launch gpg-agent`, the prerequisite's
   operating fact).
2. `cartridge trust` the project again, since the manifest changed, then
   `cartridge reload auth`. Do not run `cartridge help auth` through a wrapped
   shell.
3. `cartridge call auth.jev '{"state":"Help! My payouts have been failing for 3 days.","questions":{"is_urgent":{"type":"noul","instructions":"Does this convey urgency?"}}}'`,
   timed. Record in the evidence note: wall-clock latency, the `usage`
   object, the answer, and whether the response carried
   `x-typesafe-request-id`. If a `429` or `529` is ever seen, record its
   headers and body shape: that is the observation the two assumptions above
   wait for.
4. The same call with `"url":"https://example.invalid"` added: the host
   refuses it at the sender and names the field.

## Dependencies and base

- Hard: `@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values`
  done. This spec edits `src/openai.ts`, `src/main.ts`, `cartridge.json` and
  the three docs after it, so its line references (`src/main.ts:11-14`,
  `init.lua:12`, `src/openai.ts:20,98`) are base-sha lines and move.
- Base for the lane: the `auth.ctg` commit that collects the prerequisite,
  not `d875108`.
- Downstream: the jev.ctg consumer PRD needs this one done so its fixture
  uses the recorded answer shape.
