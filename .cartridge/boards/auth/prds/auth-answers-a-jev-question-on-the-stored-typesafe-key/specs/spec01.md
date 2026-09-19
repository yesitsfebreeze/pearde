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

Base: `auth.ctg` at `c5e8871`, the collected pass leaf
(`@auth/auth-reads-every-secret-from-pass-and-lists-names-without-values`).
Every citation below is a line of that sha
(`git -C /Users/feb/dev/cartridge/auth.ctg show c5e8871:<path>`). The whole
change was built once in a `git archive c5e8871` copy, and its Verify blocks,
test block and six mutants were run there (see "Probe results"). The PRD
footprint includes `init.lua` (coordinator, D1). The PRD's Context points
here for the TypeSafe API facts, so "API facts" below is the full record.

r3 changes from r2, after plan review round 1:
- J1: the live probe is no longer an Acceptance box; it is a by-hand step.
- J2: two new named tests, and a 429-to-overloaded mutant.
- J3: host outcomes are documented.
- J4: the key is checked as a usable bearer.
- J5: the API facts are complete.
- Dimension 2: the docs say `grant.net` is declarative.

## What this spec calls from the landed pass leaf

Revalidate these lines if `src/pass.ts` changes again. Nothing else in it is
used; `list`, `available`, `insert` and `place` are not called.

- `entry(provider, field?)`, `src/pass.ts:23-28`, called as `entry("typesafe")`.
  The default field `"api-key"` makes it return `cartridge/typesafe/api-key`.
- `read(name, deps)`, `src/pass.ts:40-54`, returning
  `PassRead = { ok: true; value: string } | { ok: false; state: PassFailure; message: string }`
  (`:9`), with `PassFailure = "missing_entry" | "gpg_missing" | "no_answer" | "refused"`
  (`:8`). `deps` is `PassDeps = { env?, home?, timeoutMs? }` (`:7`), which
  `Dependencies` in `src/openai.ts:23` already satisfies. The store is
  `<home>/.cartridge/auth/store` (`:17-20`). gpg runs only when the entry file
  exists (`:42`), bounded by `deps.timeoutMs ?? 5000` (`:44`).
- `src/openai.ts:4` already imports `read as readPass` and `entry`.
  `OpenAIAuth.status("typesafe")` (`:118-125`) reports
  `state: "available_unverified"` when `read` succeeds, which is what the
  by-hand probe checks first.

**How a key-read failure maps to the six type words.** Each of the four
landed `PassFailure` states means no key, so no request is built. All four map
to **`unavailable`**, with the state and pass's own message kept:
`unavailable: cartridge/typesafe/api-key is <state>. <message>`.

| `read()` result | `auth.jev` outcome |
| --- | --- |
| `{ok:true, value}` | the request is sent with `Authorization: Bearer <value>` |
| `missing_entry` | `unavailable: … is missing_entry. No entry … Add it with: bun <door> typesafe api-key < value` |
| `gpg_missing` | `unavailable: … is gpg_missing. gpg is not on PATH; …` |
| `no_answer` | `unavailable: … is no_answer. gpg gave no answer … within 5000 ms …` |
| `refused` | `unavailable: … is refused. gpg refused to decrypt …` |
| `{ok:true, value}` where `value` fails `/^[\x21-\x7e]+$/` | `unavailable: cartridge/typesafe/api-key is not a usable bearer` (J4). The value is never quoted, and nothing is fetched. |

`secret()` (`src/pass.ts:30`) already keeps only the first line, trimmed.
The J4 test catches what survives that: an inner space, a tab, or a
non-ASCII character. `fetch` would either reject such a header value or
send a bearer TypeSafe can only answer with 401.

`available_unverified` and `missing_api_key` are status states, not read
results (`src/openai.ts:8`). `missing_api_key` comes only from the OpenAI
discovery path and cannot occur here. Pass's messages carry only paths and
entry names (`src/pass.ts:37,50,51,53`), never a value.

## API facts

Fetched 2026-09-19 as raw markdown with `curl`, HTTP 200 each:
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
  the API. `questions`: `map<string, Question>`, required, keyed by ids the
  caller chooses ("The key is not sent to the underlying model").
- `state` is "a plain string for text, or structured data (object/array)".
  The model accepts "Text only. String, JSON object, or array of text values."
- Every question has `type` (`"noul" | "choice" | "score"`) and
  `instructions` (`string | object | array`).
  - `noul`: `criteria` is optional, `{ "true"?: string, "false"?: string }`,
    describing what a yes (near 1) and a no (near 0) mean.
  - `choice`: `criteria` is required, a `map<string, string | null>` of
    option to description; `null` means the option needs no extra detail.
  - `score`: `criteria` is required, an ordered array of level descriptions,
    at least two.
  - Instructions, options, levels and noul criteria "all accept JSON
    structure". This is from the `llms.txt` index entry for
    `primitives/advanced.md`; that page itself was not fetched.
- Models (`models.md`):
  - Aliases: `jev-latest` points to `jev-1.13.0`, "the most recent stable,
    official release". `jev-preview` currently points to the same model, and
    "there is no preview build available right now".
  - All models use `POST /v1/systemone`.
  - Limits: 64k tokens per request; 32k for `state` plus the longest
    question; 250,000 tokens per second; 1,200 requests per minute. Limits
    are "adjusting dynamically" and "can change without notice".
  - A request over either rate limit returns `429`.
  - Pricing: input tokens only; "Output tokens are free".
  - "English is the primary training language and where accuracy is
    currently best."
  - The model returns typed answers, not generated text. This is from the
    PRD's original Context and `api.md`'s response shape, not a quoted
    sentence.

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

- `model` is "the model that performed the evaluation". `answers` is
  `map<string, Answer>` under the same ids. `usage` is
  `{input_tokens: integer, output_tokens: integer}`.
- Every answer carries a `type` matching its question.
  - `noul`: `noul`, a number from 0 (no) to 1 (yes), the probability of
    yes. It has no `confidence`.
  - `choice`: `choice`, the highest-probability option; `probabilities`,
    every option mapped to a float, summing to 1; `confidence`, 0 to 1,
    "derived from probabilities".
  - `score`: `score`, the probability-weighted value, which "can land between
    levels"; `legend`, each level index (a string key) mapped to its
    description; `probabilities`, each level index mapped to a float, summing
    to 1; `confidence`, 0 to 1.
  - `confidence` is "a statistic computed from the probability distribution".
    Its formula is unpublished: the example has a top probability of 0.85
    and a confidence of 0.82.
- Statuses: `401` missing or invalid key, `422` validation failure ("The body
  details the offending field"), `429` rate limit, `529` overloaded. For both
  `429` and `529`: "retry the request with exponential backoff instead of
  retrying immediately."
- `models.md:19`: the SDKs "honor the `retry-after` header when the response
  carries one". The JS `RetryPolicy` page names two headers, `Retry-After`
  and `retry-after-ms`. SDK defaults: first delay 500 ms, doubled up to a
  5000 ms cap, jitter 0.25, 2 retries; retried statuses 408, 429 and
  500–599; a server-asked delay honoured up to 60000 ms.
- Errors carry an `x-typesafe-request-id` header.
- `auth.jev` deliberately differs from the SDK defaults in three ways. It
  retries only 429 and 529, as the PRD's Decision says. It has no jitter.
  It retries until the 15 s deadline rather than a fixed count.

**Not documented, so assumed.**

- **The error body shape.** The docs say only "a JSON body describing what
  went wrong". The SDK types the body as `unknown`. This spec never parses or
  forwards an error body, which matches `src/openai.ts:140` and the landed
  test `failed upstream authorization is useful without echoing the upstream body`.
- **Whether a `429` or `529` carries a retry header.** The code reads both
  headers and falls back to its own backoff when neither parses. The by-hand
  probe records the headers if either status is ever seen.

**Noul confidence: the API does not give one.** `confidence.md:11`:
"(Noul answers don't carry one.)" `primitives/noul.md:302` is headed "Noul
does not return a separate confidence value". A noul answer is exactly
`{type, noul}`, where `noul` is P(yes). `auth.jev` returns it as given and
synthesizes nothing. The consumer's `max(p, 1-p)` is its own measure (D4, as
the coordinator recorded).

## Acceptance

- [x] The named test `auth.jev posts to the fixed path with the stored bearer and returns answers and usage unchanged`: one `POST` to `/v1/systemone` with `Authorization: Bearer <fixture key>` and a body of exactly `{state, model:"jev-latest", questions}`. The destination the code chose is `https://api.typesafe.ai/v1/systemone`. The only entry it read is `cartridge/typesafe/api-key`. The result equals `{answers, usage}` of a fixture holding a noul, a choice and a score answer. A second call with `model:"jev-preview"` sends that model.
- [x] The named test `a request naming a url or a host or a key is refused and nothing is fetched`: `url`, `host` and `key` are each refused with `invalid:`. The fixture saw no request and no entry was read. The manifest schema has `additionalProperties: false` and exactly the properties `state`, `questions` and `model`.
- [x] The named test `a 429 then a 200 succeeds after one backoff`: two requests, the second no earlier than the fixture's `retry-after-ms`, and the answers come back.
- [x] The named test `a 529 on every attempt ends in a bounded overloaded failure`: an error starting `overloaded:` within the injected deadline plus 250 ms, after at least three requests whose gaps grow.
- [x] The named test `a 429 whose retry-after passes the deadline fails rate_limited after one request`: a `429` on every attempt carries `retry-after: 1`, with `deadlineMs: 400`. The call fails `rate_limited:` after exactly one request, in under 300 ms, without sleeping first. This covers the seconds header and failing at once (J2).
- [x] The named test `a destination that refuses the connection fails unreachable`: `fetch` dials a loopback port that was opened and then closed, and the call fails `unreachable:`. The destination the code chose is still `https://api.typesafe.ai/v1/systemone` (J2).
- [x] The named test `with no typesafe entry the call fails unavailable and nothing is fetched`: the real `read` on an empty `/tmp/ca-` home gives `unavailable: cartridge/typesafe/api-key is missing_entry`. `fetch` is never called and the home stays empty.
- [x] The named test `a stored value that is not a usable bearer fails unavailable and nothing is fetched`: for `two words`, a value with a tab, and a non-ASCII value, the message is exactly `unavailable: cartridge/typesafe/api-key is not a usable bearer`. The value is not in the captured stderr, and the fixture saw no request (J4).
- [x] The named test `an upstream error body that echoes the key never reaches the caller or the log`: the fixture answers `401` with the received bearer in its body. The error starts `upstream:`. The key is in no error, no loose frame and no captured stderr, and the capture is proven non-empty.
- [x] `cartridge.json` equals c5e8871 plus exactly the delta under step 5.
- [x] `README.md`, `.cartridge/help.md` and `.cartridge/docs/README.md` document `auth.jev` and its failure words. `.cartridge/docs/README.md` also states:
  - that the six words cover failures inside auth, and that host outcomes (schema refusal, `timed_out`, an absent or untrusted cartridge) arrive in the host's wording (J3);
  - that `grant.net` is declarative (dimension 2).

The live probe against the real API is deliberately not a box (J1). Collect
refuses an open box, and the probe needs the collected manifest trusted. It
is under "By hand after collect (coordinator)".

## Steps

1. **`src/jev.ts`** (new, 37 lines as built in the probe copy, with J4; imports only
   `./pass` and the `Dependencies` type):
   - `const DESTINATION = "https://api.typesafe.ai/v1/systemone"` is not
     exported and not configurable. `export const JEV_DEADLINE_MS = 15000`.
   - `export async function jev(args: any, deps: Dependencies = {}): Promise<{answers: unknown; usage: unknown}>`.
   - First, every key of `args` must be `state`, `questions` or `model`;
     otherwise throw `invalid: auth.jev takes state, questions and an optional model`.
     The host already refuses such a payload at the sender and again on
     arrival (`cartridge.ctg/docs/transport.txt:40-44`). This check is the
     same refusal for a driver that bypasses the host, and it is the form the
     box can execute.
   - Start the clock, then
     `const found = await (deps.read ?? readPass)(entry("typesafe"), deps)`.
     If `!found.ok`, throw
     `unavailable: ${name} is ${found.state}. ${found.message}`. Then, once,
     `if (!/^[\x21-\x7e]+$/.test(found.value))` throw
     `unavailable: ${name} is not a usable bearer`, without quoting the value
     (J4). No request has been built yet, and the gpg read counts inside the
     deadline.
   - Loop. Call `(deps.fetch ?? fetch)(DESTINATION, …)` with `POST`,
     `signal: AbortSignal.timeout(max(1, time left))`, the two headers, and
     the body `{state, model: args.model ?? "jev-latest", questions}`.
     - A thrown fetch gives `unreachable: TypeSafe did not answer.`
     - A 2xx without an object `answers` and an object `usage` gives
       `upstream: TypeSafe returned an unreadable answer.`
     - A 2xx returns `{answers, usage}` and nothing else.
     - Any other status except 429 and 529 gives
       `upstream: TypeSafe refused the request (HTTP <n>).` The body is never
       read.
   - On 429 or 529: `asked` is `retry-after-ms`, else `retry-after` × 1000,
     else 0 (an HTTP-date parses to `NaN`, so it becomes 0).
     `pause = max(wait, asked)`. If `elapsed + pause >= deadline`, throw
     `rate_limited: …` for 429 or `overloaded: …` for 529 at once. Otherwise
     sleep, then `wait = min(wait * 2, 5000)`. `wait` starts at
     `deps.jev?.backoffMs ?? 500`. The deadline is
     `deps.jev?.deadlineMs ?? JEV_DEADLINE_MS`.
   - One comment:
     `// ponytail: no jitter and no key cache; one gpg read per call. Add a TTL cache if the live probe's latency says so.`
   - The six type words, as message prefixes, because a wire error is a
     string (`src/wire.ts:95-98`, `init.lua:7`): `invalid`, `unavailable`,
     `unreachable`, `upstream`, `rate_limited`, `overloaded`.
2. **`src/openai.ts`**:
   - `:4`: add `import { jev } from "./jev";`.
   - `:23`: `Dependencies` gains `read?: typeof readPass` and
     `jev?: { deadlineMs?: number; backoffMs?: number }`. Both are in-process
     test seams, in the sense of the `apiKey` comment at `:105`.
   - `:16-22`: `LiveAuth` gains
     `jev(args: unknown): Promise<{ answers: unknown; usage: unknown }>`.
   - After `:126` (`list()`): `jev(args: unknown) { return jev(args, this.deps); }`.

   The destination is not a dependency. The tests inject `fetch`, record the
   URL the code chose and dial loopback, as `live.test.ts:62` does with
   `socket`. `make` stays the only seam of `serve()` (`src/main.ts:4-7`).
3. **`src/main.ts`**: after the `auth` handler (`:11-15`), before `:16`:
   `wire.on("auth.jev",args=>auth.jev(args));`.
4. **`init.lua:12`**: `{ "auth", "auth.live" }` becomes
   `{ "auth", "auth.live", "auth.jev" }`. Nothing else changes. The helper's
   per-request bound stays 60000 ms (`init.lua:3`,
   `cartridge.ctg/src/node/mod.rs:636-638,754`). `request` is an async method,
   so a call waiting in backoff does not hold auth's node.
5. **`cartridge.json`**, the exact delta against c5e8871 (as applied and
   diffed in the probe copy):
   - `description` becomes: `Reads any provider's secrets from its own pass store, lists them by name without values, and makes the authenticated calls itself (GPT Live connections and JEV questions) without returning secrets to consumers.`
   - New `events["auth.jev"]`, after `auth.live.event`:

     ```json
     "auth.jev": {
       "description": "A JEV judgement on the stored TypeSafe key: {state, questions, model?} -> {answers, usage} as the API returns them; questions and answers are maps keyed by the caller's ids. The caller supplies no key and no destination.",
       "timeout_ms": 20000,
       "schema": {
         "type": "object",
         "required": ["state", "questions"],
         "additionalProperties": false,
         "properties": {
           "state": { "type": ["string", "object", "array"] },
           "questions": { "type": "object", "minProperties": 1,
             "additionalProperties": { "type": "object", "required": ["type", "instructions"],
               "properties": { "type": { "enum": ["noul", "choice", "score"] } } } },
           "model": { "type": "string" }
         }
       }
     }
     ```

   - `grant.net`: `["api.openai.com"]` becomes
     `["api.openai.com", "api.typesafe.ai"]`.
   - `listen`: `["auth", "auth.live"]` becomes `["auth", "auth.live", "auth.jev"]`.
   - Unchanged: `grant.exec` `["bun","gpg"]`, `grant.read` `["/"]`,
     `grant.write` `["$HOME/.cartridge/auth/.gnupg"]`, no `grant.env`, the
     three `settings`, `events.auth`, `events["auth.live"]`,
     `events["auth.live.event"]` and `commands`.
   - `timeout_ms` 20000 is above the 15000 in-process deadline, so auth
     answers with its own typed failure before the host reports `timed_out`.
   - A question stays open inside the schema because the API owns `criteria`.
6. **`.cartridge/tests/integration/jev.test.ts`** (new, 159 lines as built in
   the probe copy, with eight tests):
   - Built like `live.test.ts`: `Bun.serve({ port: 0, hostname: "127.0.0.1" })`
     answers from a scripted list of `{status, headers?}`, records
     `{method, path, auth, body, at}` per request, and echoes the received
     bearer into every error body.
   - `serve(wire, config => new OpenAIAuth(config, deps))` over `node()` from
     `./node`. The stderr swap has its restore registered first, as
     `live.test.ts:65-70` does.
   - `deps.fetch` records `String(url)` and forwards to
     `mock.url + new URL(url).pathname`.
   - `deps.read` is a fake. It records each name and answers
     `{ok:true, value: KEY}` only for `cartridge/typesafe/api-key`, and
     `{ok:false, state:"missing_entry", message:"absent"}` otherwise.
   - The `unavailable` test passes `read: undefined` and `home: mkdtempSync("/tmp/ca-")`,
     so the landed `read` runs and answers `missing_entry` without spawning
     gpg (`src/pass.ts:42`).
   - The backoff tests inject `jev: { backoffMs: 20 }`, plus
     `deadlineMs: 400` for the 529 test and the `retry-after: 1` test. The
     429-then-200 fixture carries `retry-after-ms: 70`.
   - The `unreachable` test opens a `Bun.serve` on port 0, stops it, and
     passes `{ url: <that closed address> }` as the mock. The connection is
     refused at once.
   - The bearer test overrides `read` with `async () => ({ ok: true, value })`
     for each bad value.
   - The file never reads `homedir()` or `tmpdir()`, never names `GNUPGHOME`,
     and never names a real key.
7. **Docs**, in the same change:
   - `README.md`: `## Events` lists `auth.jev` under Defines and Listens to,
     plus one `auth.jev` bullet under `## Use`.
   - `.cartridge/help.md`: the same bullet.
   - `.cartridge/docs/README.md`: one row in the contract table (`:119` area),
     and a short `auth.jev` section stating:
     - the fixed destination `api.typesafe.ai`, and the entry and its door
       (already documented at `:33-38`)
     - that `questions` and `answers` are maps keyed by the caller's ids
     - that a noul answer carries no `confidence`
     - the six failure words, and that every `read()` failure state and an
       unusable stored value are `unavailable`
     - J3: the six words cover failures inside auth. Host outcomes arrive
       in the host's wording, not with one of the six words: a schema
       refusal at the sender naming the failing field, `timed_out` after the
       event's 20000 ms, and an absent or untrusted auth cartridge
       (`unavailable` in the host's own sense,
       `cartridge.ctg/docs/transport.txt:46-52`). A consumer maps both kinds;
       auth's own form is always `unavailable: cartridge/typesafe/api-key …`,
       while the host's `unavailable` means auth could not be reached.
     - Dimension 2: `grant.net` lists `api.typesafe.ai` as a declaration,
       not an enforced allowlist. The macOS seatbelt grants `network*` to any
       cartridge whose `net` is non-empty
       (`cartridge.ctg/src/sandbox/mod.rs:305-307`, at cartridge.ctg
       `445a87f`). The fixed destination therefore rests on the code: one
       constant in `src/jev.ts`, with no argument, setting or dependency that
       can change it.
     - the retry rule: 429 and 529 only, 500 ms doubling to 5 s,
       `Retry-After`/`retry-after-ms` honoured, 15 s in all, 20 s at the host
     - that auth neither caches the key nor reads or forwards an upstream
       error body

   One line each for what is not built: a generic `auth.fetch` (the PRD's
   Decision), a key cache, jitter, retry on other 5xx, a request size check,
   forwarding `model` or `x-typesafe-request-id`, a `tool.*` envelope.
8. **Mutants.** The implementer reruns the six mutants from "Probe
   results" and records each exit in the evidence note. Each run must be
   under a hard bound:
   `env -u CARTRIDGE_YOLO perl -e 'alarm 40; exec @ARGV' bun test ./.cartridge/tests/integration/jev.test.ts`.
   This machine has no `timeout` command. Mutant 3 leaves an orphaned retry
   loop that keeps bun alive after its test fails. A non-zero exit, 1 or
   142 (SIGALRM), counts as caught.

## Probe results the design rests on

Run 2026-09-19, bun 1.3.14. Nothing was written outside the analyst
directory.

- `git archive c5e8871 | tar -x` into `analyst-auth-jev/tree/`. Steps 1–6
  were applied there with anchor-checked replacements; every anchor matched.
  `diff -u` against `c5e8871:cartridge.json` gives exactly the step 5 delta,
  with the description worded differently in the copy.
- In that copy:
  - Block 1's manifest and import script printed
    `ok=true deadline=15000 timeout_ms=20000`. `grep '"auth.jev"' init.lua`
    and the destination-once check passed. The doc greps were not run
    because the docs were not written.
  - Block 2: `bun install --frozen-lockfile`, and `bun run check` (`tsc`)
    exited 0, including the new test file.
  - The entrypoint with `HOME=/nonexistent-auth-home` answered
    `{"id":2,"error":"unavailable: cartridge/typesafe/api-key is missing_entry. No entry cartridge/typesafe/api-key in /nonexistent-auth-home/.cartridge/auth/store. Add it with: bun …/src/insert.ts typesafe api-key < value"}`
    and created no directory. A request adding `url` answered
    `invalid: auth.jev takes state, questions and an optional model`.
  - r3, with J2 and J4 applied: `tsc` exits 0. The test block command with
    a JUnit report exits 0. The report header reads
    `<testsuites name="bun test" tests="31" assertions="168" failures="0" skipped="0">`,
    so 31 pass and 0 fail across 5 files in 10.5 s. All eight new names and
    every regression name below appear as test cases.
- Mutants of `src/jev.ts`, each run with
  `bun test ./.cartridge/tests/integration/jev.test.ts`:
  1. `entry("typesafe")` changed to `entry("openai")`: exit 1.
  2. The key whitelist replaced by `false`: exit 1.
  3. The `elapsed + pause >= deadline` check replaced by `false`: exit 142
     under the 40 s alarm. `a 529 on every attempt ends in a bounded overloaded failure`
     failed at 15128 ms, and the orphaned loop kept the process alive.
  4. `res.status === 429 ? "rate_limited" : "overloaded"` replaced by
     `"overloaded"` (the reviewer's surviving mutant): exit 1.
     `a 429 whose retry-after passes the deadline fails rate_limited after one request`
     failed.
  5. The J4 bearer check replaced by `false`: exit 1. The bearer test failed.
  6. The `retry-after` seconds branch replaced by `0`: exit 1. The
     `retry-after: 1` test failed, because the call slept and sent more
     than one request.
  - Restored: exit 0.
- The earlier loopback probe of the loop alone:
  - 429 with `retry-after-ms: 70` then 200: two requests 71 ms apart.
  - 529 throughout with a 400 ms deadline: 5 requests, gaps 21, 41, 82 and
    161 ms, then `overloaded:` at 305 ms. The key was not in the message.

## Remaining risk

- The host has not compiled the new schema. `type` as an array and `enum`
  are plain JSON Schema for `jsonschema` 0.56 (inferred). The first
  `cartridge trust` after collect is the check.
- Editing `cartridge.json` untrusts auth in a running daemon until the user
  trusts it again. Voice loses `auth` for that interval.
- Each call reads the key with one gpg process, bounded at 5000 ms by
  `src/pass.ts:44`, inside the 15 s deadline. A slow read shows up as
  `unavailable: … is no_answer`.
- The consumer (jev.ctg) should pass auth's message through as its reason,
  not prefix it again (D3, recorded by the coordinator).
- No mutant runs inside a Verify block. Step 8 and the diff reviewer back the
  test bodies; the `test` block pins the names.

## Verify and Proof

No cargo, so no `CARGO_TARGET_DIR`. Pass 2 writes only `node_modules/`
(gitignored, outside the footprint) and `/tmp/ca-*`, which the tests remove.
No block reads a variable without a default. No guard is `! grep` or an
`a && b` list. No block reaches the network: the tests dial loopback, and the
entrypoint check fails before any request.

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
  && same(m.listen, ["auth", "auth.live", "auth.jev"])
  && same(m.grant.net, ["api.openai.com", "api.typesafe.ai"])
  && same(m.grant.exec, ["bun", "gpg"]) && same(m.grant.read, ["/"])
  && same(m.grant.write, ["$HOME/.cartridge/auth/.gnupg"]) && m.grant.env === undefined
  && Object.keys(m.settings ?? {}).every(name => !/key|url|host|model|token|secret/i.test(name));
if (!ok) process.exit(1);
'
grep -q '"auth.jev"' init.lua
for doc in README.md .cartridge/help.md .cartridge/docs/README.md; do
  grep -q 'auth\.jev' "$doc"
  grep -q 'unavailable' "$doc"
done
for word in api.typesafe.ai overloaded rate_limited unreachable noul timed_out untrusted 'network\*'; do
  grep -q "$word" .cartridge/docs/README.md
done
# The destination is written once, in the one file that makes the call.
test "$(grep -rl 'api\.typesafe\.ai' src | tr '\n' ' ')" = "src/jev.ts "
# The test never reaches this machine's home or gpg home.
if grep -qn 'homedir(' .cartridge/tests/integration/jev.test.ts; then exit 1; fi
if grep -qn 'tmpdir(' .cartridge/tests/integration/jev.test.ts; then exit 1; fi
if grep -qn 'GNUPGHOME' .cartridge/tests/integration/jev.test.ts; then exit 1; fi
```

```sh
export CARTRIDGE_BUN="${CARTRIDGE_BUN:-bun}"
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" install --frozen-lockfile
env -u CARTRIDGE_YOLO "$CARTRIDGE_BUN" run check
# The real entrypoint on a home with no store: the call is refused as
# unavailable before any request is built, so this block needs no network.
out="$(printf '{"id":1,"call":"apply","args":{}}\n{"id":2,"call":"auth.jev","args":{"state":"s","questions":{"q":{"type":"noul","instructions":"?"}}}}\n' | env -u CARTRIDGE_YOLO HOME=/nonexistent-auth-home "$CARTRIDGE_BUN" src/main.ts)"
printf '%s\n' "$out" | grep -q '"id":2,"error":"unavailable: cartridge/typesafe/api-key is missing_entry'
```

```test
run: env -u CARTRIDGE_YOLO "${CARTRIDGE_BUN:-bun}" test ./.cartridge/tests/ --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: auth.jev posts to the fixed path with the stored bearer and returns answers and usage unchanged
pass: a request naming a url or a host or a key is refused and nothing is fetched
pass: a 429 then a 200 succeeds after one backoff
pass: a 529 on every attempt ends in a bounded overloaded failure
pass: a 429 whose retry-after passes the deadline fails rate_limited after one request
pass: a destination that refuses the connection fails unreachable
pass: with no typesafe entry the call fails unavailable and nothing is fetched
pass: a stored value that is not a usable bearer fails unavailable and nothing is fetched
pass: an upstream error body that echoes the key never reaches the caller or the log
pass: a read on a home with no store reports a missing entry and creates nothing
pass: the insert door round-trips a value that status reports as source pass without the value
pass: a WebSocket session relays, forwards and ends over the wire without disclosing the key
pass: failed upstream authorization is useful without echoing the upstream body
pass: shared credentials are discovered without leaking them into status
```

### By hand after collect (coordinator)

This is not an Acceptance box and has no checkbox (J1). The coordinator runs
it after collect and records the result in the PRD's `collection.md`. It
needs the person's stored key, the real network, and a trusted, reloaded
auth. Run it from `/Users/feb/dev/cartridge`.

1. The key is already stored. Only if step 3 answers `missing_entry` does
   the person store it, piped and never typed:
   `pbpaste | bun /Users/feb/dev/cartridge/auth.ctg/src/insert.ts typesafe`.
   That prints `pass:cartridge/typesafe/api-key`; the door refuses an empty
   value.
2. `cartridge trust /Users/feb/dev/cartridge/auth.ctg` (auth only, never the whole project), because the manifest changed,
   then `cartridge reload auth`. Do not run `cartridge help auth`.
3. Status first. The answer must have `"state":"available_unverified"`,
   `"source":"pass"` and `"entry":"cartridge/typesafe/api-key"`:

   ```sh
   cartridge call auth '{"op":"status","provider":"typesafe"}'
   ```

4. One call with a small noul and choice question, timed:

   ```sh
   t0=$(python3 -c 'import time;print(time.time())')
   cartridge call auth.jev '{"state":"Help! My payouts have been failing for 3 days.","questions":{"is_urgent":{"type":"noul","instructions":"Does this convey urgency?"},"department":{"type":"choice","instructions":"Which team should handle this?","criteria":{"billing":"Payments, invoicing, refunds","technical":"Bugs, outages, integrations","sales":"Pricing, upgrades, new accounts"}}}}'
   python3 -c "import time;print(round((time.time()-$t0)*1000),'ms')"
   ```

   Record in `collection.md`, and commit it in `prd.ctg`: the wall-clock latency (it includes the gpg
   read), the whole `usage` object, both answers, and that `is_urgent` has no
   `confidence` field. If any call ever answers `rate_limited:` or
   `overloaded:`, record it. The headers of a real 429 or 529 are the
   observation the retry-header assumption waits for.
5. The refusal on the real host:

   ```sh
   cartridge call auth.jev '{"state":"s","questions":{"q":{"type":"noul","instructions":"?"}},"url":"https://example.invalid"}'
   ```

   The host refuses it at the sender and names the field. No request leaves.

## Dependencies and base

- The lane base is `auth.ctg` `c5e8871`. The prerequisite is done.
- Downstream: the jev.ctg consumer PRD uses the answer shape recorded by
  step 4 of the probe.
- A reusable attempt artifact: `analyst-auth-jev/tree/` in the analyst
  scratch directory is c5e8871 with steps 1–6 applied (r3, with J2 and J4),
  except the docs. `src/jev.ts` and
  `.cartridge/tests/integration/jev.test.ts` there are the probed versions.
