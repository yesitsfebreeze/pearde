---
complexity: 1
footprint:
  - README.md
  - .cartridge/help.md
  - "src/jev.ts"
  - ".cartridge/memos/judgement/example-needs-an-llm.md"
  - ".cartridge/memos/type/judgement.md"
  - ".cartridge/tests/integration/decide.test.ts"
---

# spec01 — validate checks criteria per type, and a failure reason is one line

Base: jev.ctg `78b7fe4`.

## Acceptance

- [x] `a judgement whose criteria the api would refuse is refused` and
      `the documented criteria shapes are accepted` pass.
- [x] `a wrapped auth failure reads as one line that starts with its type word` passes.
- [x] `the shipped example judgement is valid` still passes, and
      `type/judgement.md` names the three shapes.

## Steps

1. `src/jev.ts`, `validate`, inside the per-question loop after the
   instructions check: a `noul` has no `criteria`, or a non-array object whose
   only keys are `true` and `false`, each a string. A `choice` has a
   non-array object `criteria` with at least two keys, each value a string or
   null. A `score` has an array `criteria` of at least two strings. The
   problem text is `` question `<id>` has criteria the API refuses for a <type> ``.
2. `src/jev.ts`, `reasonOf`: from the message, return the first match of
   `/(invalid|unavailable|unreachable|upstream|rate_limited|overloaded): [^\n]*/`,
   otherwise the message's first line. The host wraps a Lua listener's error
   as `auth: runtime error: <message>` plus a traceback
   (observed live, 2026-09-19).
3. `.cartridge/memos/judgement/example-needs-an-llm.md`: `needs_llm` takes
   `criteria: {"true": …, "false": …}`; `stakes` takes
   `criteria: {"low": …, "high": …}`. The `## Criteria` body says the same.
4. `.cartridge/memos/type/judgement.md`: one sentence per type with its
   criteria shape.
5. `.cartridge/tests/integration/decide.test.ts`: the three named tests. The
   refusal test builds each bad judgement by hand and expects `validate` to
   return a string naming the question; the accepted test expects `null` for
   one judgement per documented shape; the reason test has the fixture
   `auth.jev` reject with the wrapped text observed live and expects
   `reason` to equal `upstream: TypeSafe refused the request (HTTP 422).`,
   and a second rejection `boom\nmore` to give `boom`.

## Verify and Proof

```sh
test -f src/jev.ts
grep -q '"true"' .cartridge/memos/judgement/example-needs-an-llm.md
for word in noul choice score; do
  grep -q "$word" .cartridge/memos/type/judgement.md
done
bun install --frozen-lockfile
bun run check
```

```test
run: env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/integration/decide.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: a judgement whose criteria the api would refuse is refused
pass: the documented criteria shapes are accepted
pass: a wrapped auth failure reads as one line that starts with its type word
pass: the shipped example judgement is valid
pass: the weakest answer decides the verdict and the confidence
```

## Post-collect (coordinator, by hand)

Bump the gitlink, `cartridge reload jev`, and call
`jev {op:"decide", point:"@jev/example-needs-an-llm"}` against the real API:
it must return a verdict with a non-empty `answers`. Record it beside the PRD
as `live-probe.md`.

## Recovery verification

An independent verifier reran the acceptance suite at efee7fdc37bd6a72402cf73bb3c6ce2c9befecb3: all 18 tests passed with 86 assertions. A separate declare, YAML parse, read and decide probe preserved all criteria shapes, quoted text and newlines. The footprint includes README.md and the help page to document the behavior in the same change.
