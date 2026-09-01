---
state: specced        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 30        # higher first
complexity: 8      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual:          # a record. Nothing reads it
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
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

# Filing refuses a file it does not hold

`collect --also <path>` files a commit that names a file the commit does not
contain. When this is done, `collect` refuses the whole call — nothing
written, nothing committed — when any `--also` path does not resolve to a file
that exists on the board, and the refusal names the path and the directory it
was resolved against.

**The user's decision, taken at the drill:** *"Refuse to file at all rather
than write a record naming a file it does not hold."* Not a warning, not a
partial commit — a refusal.

**The mechanism, established and verified 2026-09-01 23:20 — cite it, do not
re-derive it.**

- `resources/board/collect.py:853-858` resolves each `--also` entry with
  `os.path.abspath(a)` — against the **caller's cwd**, not `board_root` — and
  has **no existence guard**.
- The footprint loop **eight lines above** (`:845-852`) already does the right
  thing: `if not os.path.exists(full) and not tracked: raise Stop`.
- `--widen`, **two lines below** (`:860-862`), already joins `board_root`.
  `--also` is the odd one out of its own two neighbours.
- `planlib.repo_root()` on a path that does not exist inside a repo still
  returns the repo root, so the `if not root: raise Stop` that follows never
  fires. The unresolvable path is then named in the commit message at `:1079`
  anyway.
- `close_container()` (`:1227`) holds no `opts["also"]` reference at all.
  `"also"` appears in the file only at `:89, :91, :114, :122, :853, :1079`.

**Why this matters to what ships.** This is the exact mechanism behind commit
`ca29535` naming ten files it does not contain, and it has since left a
finished piece of work unfiled. Every board that runs `collect` inherits it.

**Constraints and non-goals.**

- Do not change `--widen` or the footprint loop; they are the two correct
  models to copy from.
- Do not make `--also` silently tolerant of a missing path — the user picked
  refusal over reporting.
- Resolve relative to the board, the way `--widen` does. A caller who passes
  a path relative to their own cwd and gets a refusal naming the board root is
  the intended outcome, not a bug to work around.
- The `.pearde/` prefix trap for `--also` is a known and separate sharp edge;
  a clear refusal is what makes it visible, so do not paper over it by
  guessing prefixes.

**Acceptance rides on a reproduction.** The PRD is not done on a code reading:
there must be a check that runs `collect --also` on a path that does not
exist, and asserts nothing was committed and the message names the path.

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
     the best one first and marked `(recommended)`. Only real forks the user
     must settle (naming, scope,
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
