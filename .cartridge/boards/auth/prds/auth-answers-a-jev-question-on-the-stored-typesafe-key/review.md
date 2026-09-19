# @auth/auth-answers-a-jev-question-on-the-stored-typesafe-key review history

Plan: `@auth/auth-answers-a-jev-question-on-the-stored-typesafe-key` on the auth board.
Scope: one leaf. `auth.jev {state, questions, model?}` posts to TypeSafe with the stored key and returns `{answers, usage}`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

## Round 1 — 2026-09-19

Presented revision: `auth.ctg` base `c5e8871`. Plan sha256 `e166f5558e19208133f6a909b24a077f4907eb6184c985ec1940f85b1cfad863`; spec sha256 `46cc1b9537460f4db541350f79c1305b3910630b5585dd639bfc563c4354b066`.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One fixed-destination call on the stored key; generic `auth.fetch` declined with a reason. −2: 528 words and 6 boxes. −1: a stale pre-draft bullet. |
| Ownership and reuse | 19 | Reuses `entry`/`read`, the `fetch` seam and the wire error path; seams are in-process only. −1: `grant.net` is declarative; the seatbelt grants `network*` to any non-empty net (`cartridge.ctg/src/sandbox/mod.rs:305`). |
| Dependencies and implementable slices | 14 | −5, blocking J1: the live-probe box cannot be closed before collect, and collect refuses open boxes (`prd.ctg/src/lifecycle.ts:179`). −1: J3. |
| Observable acceptance and baseline evidence | 16 | Reproduced 28 pass, 0 fail, all 11 `pass:` names. −3: J2, a mutant mapping 429 to `overloaded` survives; `Retry-After` in seconds and `unreachable` are untested. −1: the host schema refusal is checked by hand only. |
| Failure, recovery and compatibility | 18 | 15000 < 20000 < 60000 holds in code; error bodies never read; the key is proven absent even with an echoing fixture. −1: J4, an illegal header value reads as `unreachable`. −1: nothing records what a consumer sees if auth overshoots on a loaded host. |
| Reviewer total | 84 / 100 | FAIL |

Findings: J1 (blocking) move the live probe out of Acceptance. J2 test `rate_limited`, `Retry-After` in seconds and `unreachable`; add the 429 mutant. J3 document that host outcomes carry host wording. J4 refuse a bearer that is not a legal header value as `unavailable`. J5 move the API facts into the spec and drop the stale bullet.
Validation: digests match; every citation checks out at `c5e8871`; the reviewer's copy of the probe tree gave Block 1 and Block 2 exit 0 (doc grep red with docs unwritten), 28 tests 0 failures; mutants: ignoring `retry-after-ms` exit 1, forwarding the error body exit 1, 429 as `overloaded` exit 0 (survived). Copy removed.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 1.
User rating: not required under delegation; none was supplied.
Result: FAIL (84/100).
Unresolved blocking findings: J1.
Rounds used / remaining: 1 / 4.
Coordinator disposition of J1: the live probe leaves Acceptance and becomes a by-hand post-collect step recorded in `collection.md`, rather than a separate leaf; the user already holds the key.

## Round 2 — 2026-09-19

Presented revision: `auth.ctg` base `c5e8871`. Plan sha256 `78438f8db2a03ce714708bb7a547ad941457f861038e498e7accf3b86a1f699c`; spec sha256 `9c9500e613092650727c8b865407a2e49960e046b2efbdaa4ad158075b374404` (analyst revision 3).

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, five boxes, API facts moved to the spec. −1: 476 words; the excess is Decision bullets, none separable. |
| Ownership and reuse | 20 | Reuses pass's `entry`/`read`, the `fetch` seam and the stderr swap; `grant.net` documented as declarative (`cartridge.ctg@445a87f:src/sandbox/mod.rs:305-307`). |
| Dependencies and implementable slices | 19 | J1 resolved: the live probe has no box. −1: K1, commit `collection.md` after the probe. |
| Observable acceptance and baseline evidence | 19 | Nine new and five regression names pinned and reproduced; five reviewer mutants all exit 1, including 429→overloaded. −1: real `usage` and retry headers are observed only by hand. |
| Failure, recovery and compatibility | 19 | All six type words tested; an unusable bearer refused before any fetch; 15000 < 20000 < 60000 gated. −1: K2, auth's `unavailable:` and the host's `unavailable` share a word. |
| Reviewer total | 96 / 100 | PASS |

J1-J5 and the dimension-2 note are resolved in the text. Findings, none blocking: K1 commit `collection.md` after the live probe; K2 say how auth's `unavailable: cartridge/typesafe/api-key …` differs from the host's `unavailable`. Both were applied by the coordinator as one line each before `specced`.
Validation: digests match; a copy of the probe tree gave Block 1 and Block 2 exit 0 (doc grep red with docs unwritten), `bun test` under a 110 s alarm 31 tests 0 failures with all 14 `pass:` names, five mutants each exit 1, restored tree exit 0. Copy `/tmp/rv-jev2-JPM4` removed by the coordinator.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 2.
User rating: not required under delegation; none was supplied.
Result: PASS (96/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 5.
