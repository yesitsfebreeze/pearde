Verdict: SPECCED

# a claim names the process that holds it

## What the build did

Attempted the build in full, not just far enough for a spec. All four pieces
the contract names now stand, in this session's tree, uncommitted:

- `resources/board/prdfile.py` — `claim_of` gains a `session` field.
  `claim: <worker>[@s<pid>] <since>` parses back to
  `{"who", "since", "session"}`; the session pattern anchors to the very end
  of the pre-timestamp text so a worker name that is itself an email address
  (`mail@example.com`) is not mistaken for one.
- `resources/board/transitions.py` — a new `claim_value(worker)` writes the
  session half via `session.my_id()` when this process runs inside a
  session, and the old bare shape otherwise. `sweep_rows` asks
  `session_liveness_of` per claim; a `.pass.md` shield no longer protects a
  claim whose session already reads dead; `## Failure` on a swept `claimed`
  PRD names "the session holding this claim is gone" when that is why, and
  the old ttl wording only when it is not.
- `resources/board/silence.py` — new `session_liveness_of(board, claim)`
  asks `session.liveness` for the claim's pid (plus the ledger's recorded
  start time, when a row exists — the pid-reuse guard). `silent_of` now
  reads `dead` as silent at once regardless of mtime, `alive` as never
  silent regardless of mtime, and only `unknown` (no session on the claim,
  or `ps` that will not answer) falls back to the old `claim-ttl` rule.
- `resources/board/plan.py` — re-exports `session_liveness_of`.

Probe: `prds/the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it/probe/probe.sh`,
run through the committable wrapper
`prds/the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it/verify.sh`
(both left in the tree uncommitted, per the route). 17 assertions, green:
`probe: 17 pass, 0 fail`. Two probe wording bugs found and fixed along the
way — `"lane committed"` and `"idle 0m"` never matched the tool's real
output shapes (`"… path(s) committed as <sha>"`, `"silent <n>m"`) — these
were checks that could not pass as spelled, not defects in the tool.

The verify block ran exactly as `collect` will (`bash -e -o pipefail`),
green on the built tree, and reddened (exit 1) under a one-line mutation to
`silence.py`'s dead-branch, restored and confirmed with `cmp`.

## Regression check

`python3 resources/index.py check`: two pre-existing findings
(`resources/common.py` unlisted, a dangling `hotreload-test.js` reference),
neither touching this footprint.

Ran every harness that mentions `claim_of`/`silent_of`/`sweep`/`transitions`
found by name. Two matter:

- `an-unknown-flag-refuses` — 182/196 pass here vs 183/196 on the unmodified
  checkout. The one new failure is `prdfile.py:140`
  (`D …claim written`, wants `w1`, got `w1@s<pid>`) — see Findings.
- `a-session-start-brings-the-board-up` — 40/46 both before and after;
  unrelated, unchanged.

`resources/board/dispatch.py` shows modified in this session's tree — not my
edit; another PRD's uncommitted work sharing this session, left untouched.

## Findings

`prds/an-unknown-flag-refuses/probe/verify.sh:140` reads a claim's raw
frontmatter and cuts the first whitespace-separated field, asserting it
equals the bare worker name (`w1`). Run inside a live session — the ordinary
way this repo's own harnesses run — the claim it wrote now legitimately
carries a session id, so the cut sees `w1@s<pid>`. The read should go
through `prdfile.claim_of(...)["who"]`, which already strips the session
half correctly; this belongs to whoever owns that PRD, not to this one's
footprint.

No knowledge gap auto-enqueued: `knowledge.py query` on the claim/session
question returned no strong match but was not flagged as a hard gap by the
tool's own threshold.

## Scores

complexity: 20
blast-radius: high
workflow: probe-then-spec
