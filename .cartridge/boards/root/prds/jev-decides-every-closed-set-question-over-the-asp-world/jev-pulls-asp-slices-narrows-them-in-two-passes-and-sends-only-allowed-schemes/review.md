# Independent JEV ASP verification

Reviewer: /root/sessions_asp, independent of the JEV implementation worker /root/jev_verify.

Verdict: PASS for candidate 215007548e4d26907ba51893b8084aa63d662c90, branch finish/jev-slices, at /Users/feb/dev/cartridge/.worktrees/jev-slices. The candidate worktree was clean during final verification. Revised specification review score: 96/100. There are no remaining implementation or specification blockers in the assigned JEV slice acceptance. The real credential-backed combined system check remains explicitly coordinator-owned.

## Specification and boundary review

The revised specification at /tmp/jev-slices-spec.md corrects material problems in the saved draft. ASP is an authenticated host method, not an event need. The unchanged auth.jev? and memo? needs are the declared service boundary. The actual host accepts helper host:asp frames and refuses act for cartridge tokens. The implementation neither reads sibling source nor executes ASP actions.

The previous criteria validation and one-line auth failure normalization remain intact. The plain-state path still issues one auth request. The tests for rejected API criteria and accepted documented criteria passed.

The corrected deadline guards run before and after retrieval and auth awaits. A late reply cannot launch another ASP lookup or another paid model request. The first-pass filter now requires the noul type and a finite probability within zero and one. Explicit stale or absent entities cannot be restored by search. The complete serialized auth request, including question keys and envelope, is budgeted. The selection is capped by k.

The initial draft allowed attributes of disallowed schemes to leave the machine. With the actual trace provider, memory.trace contains complete nested activity records. I independently reproduced both nested content markers in both model requests. The final candidate changes disallowed cards to ID-only and passes the independent negative test. This is the appropriate combined-system contract; an arbitrary attributes object is not inherently safe metadata. Caller-supplied state remains intentionally unfiltered, as documented.

The revised default schemes are symbol, event, agent and memo, following the current PRD. File, range, trace and unknown schemes are ID-only unless explicitly allowed. Scheme filtering is reported for first-pass candidates even when relevance later rejects them.

## Independent evidence at the final commit

All commands returned zero:

1. From the candidate: env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/integration/ passed 32 tests and 190 assertions. bun run check passed TypeScript checking. The output is retained at /tmp/jev-asp-final-tests.log.
2. bun test /tmp/jev-asp-adversarial.ts passed five independent tests and 19 assertions: late first-pass answers cannot launch pass two; late expansion cannot launch another expansion or auth; invalid ranking types/probabilities cannot survive; search cannot restore an explicitly stale entity; nested attributes on a disallowed trace entity cannot appear in either auth request.
3. python3 /tmp/jev-asp-host-probe.py passed against the current /Users/feb/.local/bin/cartridge. This starts the actual JEV Bun helper in a disposable composition with declared memo/auth/ASP fixtures. Both about and search were admitted by the real host and returned act. The probe observed three real provider ASP requests and four auth requests, verified the k cap, and checked that excluded file text did not reach the model fixture. This proves authenticated host transport, not merely a mocked Wire.host method.
4. python3 /tmp/jev-asp-mutants.py passed. Each test was green before mutation; forcing every scheme open made the egress assertion fail, and removing the k cap made the top-k assertion fail. Mutations were applied only to temporary copies.
5. git diff --check passed before the final commit; the final worktree is clean.

The first suite run occurred while the implementation was still being written and reported 26 passes plus the missing new example file. That was an incomplete artifact, not a remaining defect; the final complete suite passes. The trace-attribute regression was observed failing before its correction and passing afterward.

## Combined live gate review

I reviewed .cartridge/tests/integration/asp-system.test.ts and sent concrete improvements to the coordinator. The updated gate does substantially more than checking service states:

- It verifies the root ASP tree, trace scheme, cycle telemetry and scope's exact activity endpoint.
- It calls real JEV with ASP selectors and requires two completed passes.
- It searches the exact returned decision_id with a bounded asynchronous wait. It matches a trace finished record whose event is jev and whose outcome.response.decision_id equals that unique decision. This proves durable result storage and avoids attributing a concurrent caller's event to this decision.
- It expands the matching record and checks instance-of to event:jev and originated-by to cartridge:jev.
- It feeds live host, ASP, trace, cycle and activity data through the actual scope State, Navigation and dashboard renderer and renders all four tabs without an unavailable or attention state.

A small optional strengthening is to feed decisionTree into scope's asp_tree input as well and assert the exact trace record id appears in Activity rows. The current renderer check proves that live JEV activity reaches scope, while the preceding ASP assertions separately prove the exact durable record and graph edges.

The worker did not execute the real TypeSafe endpoint, restart the user's host, alter PRD state, or modify JEV source. The coordinator owns actual credential-backed latency/usage evidence, host activation, audit/isolation and collection. Estimated token budgeting is explicitly documented as an estimate; the live probe should retain actual usage and both pass latencies.
