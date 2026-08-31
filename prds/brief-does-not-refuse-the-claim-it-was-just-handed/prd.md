---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 45        # higher first
complexity: 14      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.1h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# brief does not refuse the claim it was just handed

When this is done, the loop in `references/parts/loop.md` runs as written. Steps 4
and 5 (lines 42–43, and the paragraph at line 82) tell the orchestrator to run
`pearde claim <prd> <worker>` and then `pearde brief <prd>`, and the second
command stops refusing the state the first one just wrote. The orchestrator
dispatches an analyst or an implementer without appending `--force` to every
brief, and the header line the round logs stops saying `· forced` on runs where
nothing was actually forced. That matters because `--force` is not a narrow
override: it is the one switch past *every* gate, so using it as the routine
dispatch path silently disarms the checks that stop a worker being sent at a PRD
whose `needs:` are not done, whose footprint clashes with another claimed PRD,
whose `workflow:` slug names nothing, or which is in a state no worker should be
briefed on at all. The routine workaround and the emergency escape hatch are
currently the same keystroke, and the emergency one wins.

The gate is `resources/board/brief.py`, lines 284–299. Line 284 reads the claim
with `planlib.claim_of`; the condition at 285–286 is
`if state in ("analyzing", "claimed") or (held and state in ("open", "specced"))`
and sets `skip` to the `held — …` string at 287–288. That first arm never looks
at *who* holds the PRD — it refuses on the state alone, and `analyzing` and
`claimed` are exactly the two states `pearde claim` writes (`transitions.py:629`
maps `open → analyzing` and `specced → claimed`; the writes are at
`transitions.py:316–318`, `state` then `claim: <worker> <now>`; the pair is named
`CLAIM_STATES` at `transitions.py:769`). The refusal is doubly odd because the
role map immediately above it, at `brief.py:281–282`, already assigns those two
states a role — `analyzing` an analyst, `claimed` an implementer — so the file
knows precisely what brief to print for a PRD it then declines to brief. The
file's own docstring at `brief.py:16–19` states the intended contract:
"Dispatchable is @resources/board/transitions.py `gate_claim` — the same test
`claim` runs, imported and not re-implemented." The pre-check at 285–288 is a
second, stricter test re-implemented in front of it, and it is what fires on
every dispatch this session.

The fix must make brief accept a claim that names the worker it is briefing, and
that requires brief to learn the worker id, which today it cannot: the flag
declaration at `brief.py:357–358` carries the options `as`, `board`, `role`,
`consult`, `question`, `transcript` and the flags `force`, `check` — and `--as`
is the *persona* (`persona_line`, default `engineer`), not the worker named in
`claim:`. Note also that delegating to `gate_claim` alone is not sufficient:
`gate_claim` (`transitions.py:159–166`) is a thin wrapper over
`plan.dispatchable`, and `plan.py:1436` refuses *any* claim unconditionally with
`unclaimed: <rel> carries \`claim: …\``, which `brief.py:73` maps back to the
same skip word `held`. So whichever way the holder identity is threaded — a new
worker option on brief, or an optional holder argument through `gate_claim` into
`dispatchable` — the accept must be keyed on `claim_of(fm)["who"]`
(`plan.py:350`, which splits the value into `who` and `since`) matching the
worker being briefed, and nothing weaker.

Constraints and non-goals. `brief` writes nothing and must keep writing nothing —
it is a read command with no `--dry` for that reason; the fix is a gate change,
not a state change, and it must not clear, rewrite or refresh the `claim:` key.
What must still be refused, without `--force`: a PRD whose `claim:` names a
*different* worker (the multi-session case the sweep and `claim-ttl` exist for) —
the skip must still print `held` and the holder; a PRD in any state that is
neither `open`/`specced` nor a self-claimed `analyzing`/`claimed` — the
`state — …` skip at `brief.py:290–291` stays as it is; and every gate word
`dispatchable` produces for reasons other than the self-claim — `leaf`,
`container`, `needs`, `footprint`, `workflow` — must still stop a brief, so the
self-claim exemption must lift only the `unclaimed` gate and no other. A brief
run with no worker named should keep today's behaviour, so nothing that calls
`brief` without one gets quietly more permissive. `--force` itself stays exactly
as it is — the escape hatch, printing `pearde brief: forced past …` on stderr
(`brief.py:300–301`) and `· forced` on the header (`brief.py:325–326`); this PRD
removes the *need* to reach for it in the normal loop, it does not change it.
`claim`, `release`, `retry`, `sweep` and the view's `/edit` path are out of scope.

Pointers: `resources/board/brief.py` (the gate at 284–299, the SKIP word map at
73, the flag declaration at 357–358), `resources/board/transitions.py`
(`gate_claim` at 159–166, `transition` at 261, the claim writes at 316–318,
`CLAIM_STATES` at 769), `resources/board/plan.py` (`claim_of` at 350,
`dispatchable` at 1412 with the `unclaimed` gate at 1436 and its docstring's
note that a `claimed` PRD "is in flight, not refused"), and
`references/parts/loop.md` steps 4–5 (lines 42–43 and 82–85), which is the
documentation that must become true — and which should be checked for wording
that needs updating once the worker id is threaded through the dispatch.

## Acceptance sketch, for the analyst

- On a board with an `open` PRD, `pearde claim <prd> w1` followed by the brief
  command for worker `w1` exits 0 and prints the analyst brief, with no `· forced`
  on the header line and nothing on stderr; the same holds for a `specced` PRD
  claimed by `w1`, printing the implementer brief.
- The same brief run for a *different* worker on that same PRD still exits 1 with
  a `skipped <prd> — held —` line naming the state and the `claim:` value.
- With the self-claim accepted, a PRD held by its own worker that also fails a
  second gate — a `needs:` entry not `done`, a footprint clash with another
  `claimed` PRD, or a `workflow:` slug resolving to nothing — still exits 1 with
  the corresponding `gated`, `clash` or `workflow` skip word.
- A PRD in a state outside `open`, `specced`, `analyzing` and `claimed` still
  exits 1 with the `state — … not open or specced` skip, and `brief` still writes
  no file: the PRD's `state:` and `claim:` are byte-identical before and after.
- `references/parts/loop.md` steps 4 and 5 describe the exact commands that were
  run in the checks above, and a fresh run of the loop as documented needs no
  `--force`.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one round in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     one `(recommended)`. Only real forks the user must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such round never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a round that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the round above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
== case 1: open PRD claimed by w1, no --worker -> still held (today's behaviour, unchanged) ==
    pearde brief: skipped leaf1 — held — leaf1 is `analyzing`, `claim: w1 2026-08-31 18:00`
  - ok   no-worker still refused (exit 1)
  - ok   says held
== case 2: same PRD, --worker w1 (self-claim) -> accepted, no --force, no forced ==
    # brief leaf1 · analyst · as engineer · wf none · repo /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.Ct7ifXyEQr
  - ok   self-claim accepted (exit 0)
  - ok   no forced mark
  - ok   analyst role
== case 3: same PRD, --worker w2 (a different worker) -> still held ==
    pearde brief: skipped leaf1 — held — leaf1 is `analyzing`, `claim: w1 2026-08-31 18:00`
  - ok   other worker still refused (exit 1)
  - ok   leaf1's prd.md byte-identical across all three brief runs
== case 4: specced/claimed PRD, self-claim -> implementer brief, no forced ==
    # brief leaf2spec · implementer · as engineer · wf none · repo /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.Ct7ifXyEQr
  - ok   specced/claimed self-claim accepted (exit 0)
  - ok   implementer role
  - ok   no forced mark
== case 5: self-claimed, but needs: undone -> still refused, gated ==
    pearde brief: skipped needsleaf — gated — needs: needsdep is `open`, not done
  - ok   needs gate still fires (exit 1)
  - ok   says gated
== case 6: self-claimed, but footprint clashes with another claimed PRD -> still refused, clash ==
    pearde brief: skipped fpleaf — clash — footprint: fpother is claimed and holds `shared/thing.py`, which clashes with `shared/thing.py`
  - ok   footprint gate still fires (exit 1)
  - ok   says clash
== case 7: a state outside open/specced/analyzing/claimed, worker matches the claim -> still refused, state ==
    pearde brief: skipped blockedone — state — blockedone is `blocked`, not open or specced
  - ok   out-of-range state still refused (exit 1)
  - ok   says state
ALL CASES PASSED
--- the holder is briefed, unforced ---
ok  holder briefed clean, no force
--- a different worker is still refused ---
ok  other worker still held
--- no --worker at all is still refused ---
ok  bare brief still held
spec01 checks done
