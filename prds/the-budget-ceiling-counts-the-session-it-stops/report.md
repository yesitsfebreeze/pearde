# Report — the-budget-ceiling-counts-the-session-it-stops

Verdict: **DONE** · spec01 9/9 boxes · Verify block exits 0

## The fix, as it stands in the tree

`resources/guard.py`, +22/-2 against HEAD, two hunks and no more:

- `dispatched(data)` at `resources/guard.py:496` — `bool(data.get("agent_id")
  or data.get("agent_type"))`.
- one early return at the top of `budget()` (`resources/guard.py:518`), before
  `budget_of()`, `context_now()`, the 70/85% note band and the `ESCAPE` check.

Both defects the PRD names close on that single return. A worker is not
measured against the round's ceiling; and because it is never denied by the
ceiling, it is never shown the deny text that names `.pearde/.state/round.md`
as the one file still open — the mechanism that had a worker overwrite the
orchestrator's round file today.

## The concurrent-edit question — nothing was lost

Checked before touching anything. `git diff resources/guard.py` is exactly two
hunks: a docstring path fix (`prds/` -> `.pearde/prds/` at `guard.py:351`,
another PRD's work, intact) and this PRD's fix. Because the diff against HEAD
contains no deletions beyond those two lines, **no committed fix was reverted**
— including `the-guard-finds-the-board-the-way-the-scan-does`, which is in
HEAD. I also re-checked `one-definition-of-the-board-not-two/specs/spec01.md`,
the other spec whose prose mentions `guard.py`: its `footprint:` does not list
`guard.py` and it expects no edit there. I reapplied nobody's work.

I re-verified the diff was still those two hunks at the end of my run. It was.

## Re-verification of the analyst's 8 pre-ticked boxes

All 8 independently re-run against disk. **None untick.** Two corrections to
what they *claimed*, both in my writable paths:

1. Box 1 asserted the probe prints `9 of 9 checks pass`. It printed exactly
   that — but ten `check()` calls actually ran; the total was hardcoded. The
   count is now computed (`len(ran)`), and box 1 reads `13 of 13`.
2. The `## Verify and Proof` block ended on a bare `echo done`, so it exited 0
   **whatever the probe did** — an acceptance block that could not fail. Now
   `... || exit 1` on both commands, still ending on an explicit `echo`, so it
   satisfies the collect rule and can still fail.

## The load-bearing fact, verified independently

The whole fix rests on one empirical claim, and every fixture box would pass
even if it were false — the probe fed only synthetic payloads. So I measured it
myself, as a dispatched worker, with a temporary payload dump in `guard.py`
(inserted atomically with a compile-check, removed afterwards; the restore
refused to run unless the file on disk was byte-for-byte the one I patched, and
it was). 11 live payloads from one round:

- the orchestrator's own calls (captured concurrently, working *other* PRDs)
  carry **neither** `agent_id` nor `agent_type` — the control the analyst's
  report asserted but did not demonstrate;
- every worker's calls carry **both** (`pearde-implementer` x2 distinct
  `agent_id`s, `pearde-analyst` x1);
- all of them share one `session_id` (`2f52d04a-...`), confirming it cannot be
  the signal.

The analyst's claim holds. Those real key sets are now pinned as three probe
checks (8-10), so the fix fails loudly if the payload shape ever drifts, and
the finding is on record as `sources/260831-6630.md` via `knowledge.py
remember` — it is a Claude Code fact, not a fact about this tree.

## The checks are load-bearing

Ran the fixture against a copy of `guard.py` with the early return neutralised:
the dispatched worker over cap **is** denied, reproducing the original defect.
With the fix it is not. The boxes are not vacuously green.

## Defect found outside this scope — not fixed

`bash resources/doctor.sh` reports `guard broken — does not refuse a
hand-walked board`. **This is not the guard and not this fix.** `doctor.sh:249`
still finds the board by walking up for `<d>/prds`, the pre-`.pearde` layout.
This repo no longer has a root `prds/`, so the walk leaves the repo and latches
onto a *different project's* board at `/Users/feb/dev/infra/prds`. It then
probes the guard with `cwd=/Users/feb/dev/infra/.claude`, where there is no
`.pearde` board, so the guard correctly allows — and doctor calls that broken.

Pointed at the real repo the guard denies exactly as intended:

```
$ echo '{"tool_name":"Bash","tool_input":{"command":"find prds -name prd.md"},
         "cwd":"/Users/feb/dev/infra/pearde/.claude"}' | python3 resources/guard.py pre
{"hookSpecificOutput": {... "permissionDecision": "deny",
 "permissionDecisionReason": "The board is not walked by hand — ..."}}
```

The same doctor probe against the fix-neutralised copy is byte-identical, so it
is pre-existing. It belongs to `the-doctor-checks-the-path-a-board-is-on`
(claimed by impl-7, in flight). `doctor.sh` is outside my footprint — reported,
not touched. The other broken rows (`skills`, `origin`) are likewise unrelated
and pre-existing.

## Left to the orchestrator

`.pearde/settings.md:8` still reads `context-budget: off`. **I did not touch
it**, per the dispatch instruction — it is the workaround for this defect and
the flip is the orchestrator's call once the fix is verified. It is verified.
The flip is also a judgment about the orchestrator's own remaining window: the
moment a number goes back, that session is measured against it on its very next
call, and only that session is.

The PRD's last acceptance line — "a full round with dispatched workers
completes without a worker being refused" — can only be observed after that
flip, by a round. Everything a fixture can establish is established.

## Proof

```
13 of 13 checks pass
---
guard: /Users/feb/dev/infra/pearde/.pearde
  stamp 1788194483.769
  state /Users/feb/dev/infra/pearde/resources/board/state/guard
  scan  python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan
done
BLOCK EXIT=0
```

Footprint touched: `resources/guard.py` (unchanged by me — the analyst's fix,
verified intact). Written by me: this PRD's `probe/verify.py` and
`specs/spec01.md`, plus the KB source note. Nothing committed.
