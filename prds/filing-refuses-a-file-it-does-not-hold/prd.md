---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
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
  actual: 10.15h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
commit: c7a9f55 9df1035
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

## Report

spec01: exit 0
A. --also names a file that does not exist
  ok   A exit 1
  ok   A the refusal names the path
  ok   A ...and the directory it was resolved against
  ok   A ...and says nothing was written
  ok   A no commit was made
  ok   A the PRD is untouched
  ok   A the claim still stands
  ok   A no transition was recorded
  ok   A the worker's tick is still dirty, not staged
B. the whole call is refused
  ok   B exit 1
  ok   B neither PRD was committed
  ok   B finished untouched
  ok   B second untouched
  ok   B the refusal is printed once, not per PRD
  ok   B control: without --also both collect
  ok   B control: four commits land
C. resolution is against the board, the way --widen does it
  ok   C exit 0
  ok   C the file is on the commit
  ok   C the note is in the message
  ok   C from another cwd, exit 0
  ok   C from another cwd, the file is still on the commit
D. the caller's cwd is the second place a path is looked for
  ok   D exit 0
  ok   D the cwd's file is on the commit
  ok   D the note is in the message
  ok   D the PRD landed
  ok   D2 exit 1
  ok   D2 the refusal names the path as given
  ok   D2 ...the board place it was looked for
  ok   D2 ...the cwd place it was looked for
  ok   D2 ...and the board root
  ok   D2 nothing committed
  ok   D2 the PRD is untouched
I. precedence — the board's copy wins
  ok   I exit 0
  ok   I the board's copy is on the commit
  ok   I the cwd's copy is not
  ok   I the commit carries the board's bytes
  ok   I the cwd's copy is still untracked
E. absolute paths
  ok   E an absolute path that exists: exit 0
  ok   E ...and is on the commit
  ok   E an absolute path that does not exist: exit 1
  ok   E ...named in the refusal
  ok   E ...nothing committed
F. a directory that exists
  ok   F a directory on the board is not refused
  ok   F ...and its file rides the commit
  ok   F a directory the board does not hold is refused
  ok   F ...nothing committed
G. closing a container
  ok   G a container close with a bad --also exits 1
  ok   G ...naming the path
  ok   G ...and parent did not close
H. usage
  ok   H --also without --also-note is still usage, exit 2
  ok   H --also without a path is still usage, exit 2
  ok   H neither wrote a commit

52 checks · 52 pass · 0 fail
A. --also names a file that does not exist
  FAIL A exit 1
       got:  0
       want: 1
  FAIL A the refusal names the path
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit ad3680e · inherited 8 · record c02d165 · daemon down — report not posted · round file owed · as engineer
       want: contains: notes/nope.md
  FAIL A ...and the directory it was resolved against
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit ad3680e · inherited 8 · record c02d165 · daemon down — report not posted · round file owed · as engineer
       want: contains: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.mvabqgGAjN/a
  FAIL A ...and says nothing was written
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit ad3680e · inherited 8 · record c02d165 · daemon down — report not posted · round file owed · as engineer
       want: contains: nothing written
  FAIL A no commit was made
       got:  3
       want: 1
  FAIL A the PRD is untouched
       got:  done
       want: claimed
  FAIL A the claim still stands
       want: impl-1 2026-09-01 10:00
  FAIL A no transition was recorded
       got:  1
       want: 0
  ok   A the worker's tick is still dirty, not staged
B. the whole call is refused
  FAIL B exit 1
       got:  0
       want: 1
  FAIL B neither PRD was committed
       got:  5
       want: 1
  FAIL B finished untouched
       got:  done
       want: claimed
  FAIL B second untouched
       got:  done
       want: claimed
  FAIL B the refusal is printed once, not per PRD
       got:  0
       want: 1
  ok   B control: without --also both collect
  ok   B control: four commits land
C. resolution is against the board, the way --widen does it
  ok   C exit 0
  ok   C the file is on the commit
  ok   C the note is in the message
  FAIL C from another cwd, exit 0
       got:  1
       want: 0
  FAIL C from another cwd, the file is still on the commit
       want: contains: docs/x.md
D. the caller's cwd is the second place a path is looked for
  ok   D exit 0
  ok   D the cwd's file is on the commit
  ok   D the note is in the message
  ok   D the PRD landed
  FAIL D2 exit 1
       got:  0
       want: 1
  FAIL D2 the refusal names the path as given
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit a1df713 · inherited 8 · record 2d501ed · daemon down — report not posted · round file owed · as engineer
       want: contains: nope.md
  FAIL D2 ...the board place it was looked for
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit a1df713 · inherited 8 · record 2d501ed · daemon down — report not posted · round file owed · as engineer
       want: contains: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.mvabqgGAjN/d2/nope.md
  FAIL D2 ...the cwd place it was looked for
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit a1df713 · inherited 8 · record 2d501ed · daemon down — report not posted · round file owed · as engineer
       want: contains: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.mvabqgGAjN/d2/away/nope.md
  FAIL D2 ...and the board root
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit a1df713 · inherited 8 · record 2d501ed · daemon down — report not posted · round file owed · as engineer
       want: contains: board root /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.mvabqgGAjN/d2
  FAIL D2 nothing committed
       got:  3
       want: 1
  FAIL D2 the PRD is untouched
       got:  done
       want: claimed
I. precedence — the board's copy wins
  ok   I exit 0
  ok   I the board's copy is on the commit
  FAIL I the cwd's copy is not
       got:  .pearde/prds/finished/prd.md .pearde/prds/finished/specs/spec01.md away/dup.md src/lib.txt 
       want: without: away/dup.md
  FAIL I the commit carries the board's bytes
       want: the board copy
  FAIL I the cwd's copy is still untracked
       want: ?? away/dup.md
E. absolute paths
  ok   E an absolute path that exists: exit 0
  ok   E ...and is on the commit
  FAIL E an absolute path that does not exist: exit 1
       got:  0
       want: 1
  FAIL E ...named in the refusal
       got:  finished: inherited, not added — 8 path(s):
  .pearde/prds/parent/child/specs/spec01.md
  .pearde/prds/second/specs/spec01.md
  away/dup.md
  away/rider.md
  docs/x.md
  dup.md
  notes/lib.txt
  other/lib.txt
▸ finished: claimed → done · done 1/4 · 28% · open 1/4 · 25% · ready 0 · blocked 3 · collect 2 @1 workers · commit a1df713 · inherited 8 · record 2d501ed · daemon down — report not posted · round file owed · as engineer
       want: contains: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.mvabqgGAjN/e2/notes/gone.md
  FAIL E ...nothing committed
       got:  3
       want: 1
F. a directory that exists
  ok   F a directory on the board is not refused
  ok   F ...and its file rides the commit
  FAIL F a directory the board does not hold is refused
       got:  0
       want: 1
  FAIL F ...nothing committed
       got:  3
       want: 1
G. closing a container
  FAIL G a container close with a bad --also exits 1
       got:  0
       want: 1
  FAIL G ...naming the path
       got:  ▸ parent: open → done · done 2/4 · 44% · open 0/4 · 0% · ready 0 · blocked 2 · collect 2 @1 workers · container, 1 children · commit f49ed3a · record 441d4bf · daemon down — report not posted · round file owed · as engineer
       want: contains: notes/nope.md
  FAIL G ...and parent did not close
       got:  done
       want: open
H. usage
  ok   H --also without --also-note is still usage, exit 2
  ok   H --also without a path is still usage, exit 2
  ok   H neither wrote a commit

52 checks · 19 pass · 33 fail
can-fail: proven
A. collect finished
  ok   A exit 0
  ok   A two commits on top of the fixture — the code, then the record
  ok   A commit paths equal the footprint union plus the record
  ok   A prd.md carries commit: <sha>
  ok   A prd.md carries actual: <n>h
  ok   A state done
  ok   A claim cleared
  ok   A the progress line printed once
  ok   A the line carries the persona last
  ok   A the line says the pass file is owed
  ok   A the daemon being down is said, not fatal
  ok   A transition row appended
  ok   A git log -1 --format=%B matches commits.md line for line
  ok   A building left alone
  ok   A collecting a done PRD exits 1
  ok   A ...naming the state
B. red verify
  ok   B exit 1
  ok   B the output printed
  ok   B the exit named
  ok   B git log unchanged
  ok   B prd.md unchanged
  ok   B nothing written, said
  ok   B --fail exits 1
  ok   B --fail sets failed
  ok   B --fail clears the claim
  ok   B --fail writes ## Failure
  ok   B ## Failure holds the output
  ok   B --fail commits nothing
  ok   B --fail prints the line
C. inherited
  ok   C exit 0
  ok   C listed as inherited
  ok   C listed once
  ok   C not added
  ok   C still dirty after
  ok   C collected all the same
  ok   C the count on the line
  ok   C --widen <path> exits 0
  ok   C --widen commits it
  ok   C --widen names it in the message
  ok   C --widen names it on the line
D. no argument
  ok   D exit 0
  ok   D finished collected
  ok   D building left alone
  ok   D one line
  ok   D nothing left: exit 0
  ok   D nothing left: said
E. --dry
  ok   E exit 0
  ok   E no commit
  ok   E prd.md unchanged
  ok   E prints what 3 would add
  ok   E prints what 4 would say
  ok   E .transitions.jsonl not written
F. --trust
  ok   F exit 0 with a red verify
  ok   F the line says trusted
  ok   F done
G. gate
  ok   G red gate exits 1
  ok   G the gate's output printed
  ok   G no commit
  ok   G green gate: exit 0
  ok   G the gate ran and is in the report
H. clean tree
  ok   H exit 0
  ok   H two commits — the record lands on a clean tree too
  ok   H commit: names the record, never none
  ok   H done
I. riders
  ok   I the record is not owed — it is in its own commit
  ok   I the next collect is not stopped by the last one's record
  ok   I finished's record is not on building's commit
  ok   I nothing rides on the line
  ok   I building's own record is not owed either
  ok   I2 exit 0
  ok   I2 a foreign dirty prd.md is inherited without a baseline
J. open boxes
  ok   J exit 1
  ok   J names the file
  ok   J names the box
  ok   J no commit
  ok   J2 an open spec box exits 1
  ok   J2 names the spec
  ok   J3 building (1/2) exits 1
  ok   J4 a done PRD exits 1
  ok   J5 no such PRD exits 1
K. --also
  ok   K --also without --also-note is usage
  ok   K exit 0
  ok   K the file is on the commit
  ok   K named in the message
L. flags
  ok   L unknown flag is usage
  ok   L --widen without a path is usage
  ok   L --as sets the persona term
N. baseline hunks
  ok   N --snapshot exits 0
  ok   N the diff recorded
  ok   N exit 0
  ok   N the file is on the commit
  ok   N the worker's hunk landed
  ok   N the inherited hunk did not
  ok   N the inherited hunk is still in the tree
  ok   N the file stays dirty by exactly that hunk
  ok   N said on the line
O. the stop
  ok   O exit 1
  ok   O the path listed
  ok   O no commit
  ok   O prd.md unchanged
  ok   O --widen takes it
  ok   O and it is on the commit
  ok   O2 a tracked file whose every hunk predates the claim stops
  ok   O2 named
  ok   O3 no baseline: mtime before the claim stops
  ok   O3 named
P. gate baseline
  ok   P the gate recorded
  ok   P a red gate whose every line is in the baseline is green
  ok   P said
  ok   P2 a new line is red
  ok   P2 printed
  ok   P2 no commit
Q. rename
  ok   Q exit 0
  ok   Q the new name is on the commit
  ok   Q the old name is gone from HEAD
R. report posted
  ok   R the daemon came up on the spare port and registered the fixture
  ok   R ...under the board's declared name
  ok   R exit 0
  ok   R the line says report posted
  ok   R ...and not daemon down
  ok   R ## Report is in prd.md
  ok   R ## Report holds the verify's exit
  ok   R done
  ok   R the daemon knows the fixture
  ok   R the real board's registration is untouched
  ok   R the copied install holds no registration at all
S. snapshot
  ok   S the record is at, diff, gate, untracked
  ok   S --dry after the snapshot exits 0
  ok   S --dry lists the inherited path
  ok   S --dry writes nothing to prd.md
  ok   S --dry commits nothing
M. COMMANDS
  ok   M the module exposes COMMANDS['collect']
Z. .claims never committed
  ok   Z no path under .pearde/.claims/ on any commit above

133 checks · 133 pass · 0 fail
A. reproduced at e8b262d: the record staged by hunk
  ok   A1 the old collect exits 0
  ok   A1 ...and says by hunk on the board's own record
  ok   A1 HEAD's record says analyzing
  ok   A1 ...with the three ticks under it
  ok   A1 the tree says done
  ok   A1 ...and the folder is dirty after its own collect
A. the record lands whole, commit: in a second commit
  ok   A2 exit 0
  ok   A2 two commits on top
  ok   A2 HEAD is the record commit
  ok   A2 ...carrying only prd.md
  ok   A2 HEAD~1 carries the code and the record
  ok   A2 HEAD~1's record says done
  ok   A2 ...with the three ticks
  ok   A2 ...and actual:
  ok   A2 ...and no claim:
  ok   A2 ...and the analyst's paragraph, the baseline hunk, whole
  ok   A2 HEAD~1 does not carry commit:
  ok   A2 HEAD's commit: names HEAD~1
  ok   A2 the tree's commit: is the same
  ok   A2 the folder is clean
  ok   A2 the line does not say by hunk on the record
  ok   A2 the line names the record commit
  ok   A2 the line names the code commit
  ok   A2 nothing owed for the record
  ok   A2 one transition row
  ok   A3 clean tree: exit 0
  ok   A3 HEAD~1 is the record, alone
  ok   A3 commit: names it — never none
  ok   A3 the folder is clean
  ok   A4 --dry exit 0
  ok   A4 --dry names the record and the second commit
  ok   A4 --dry leaves the state
  ok   A4 --dry commits nothing
B. reproduced at e8b262d: the merged hunk goes as the worker's
  ok   B1 the diff is one merged hunk
  ok   B1 the old collect exits 0
  ok   B1 ...and commits the foreign line as the worker's
B. refused, named, nothing staged; --widen takes it; one line apart both land right
  ok   B2 exit 1
  ok   B2 named: file and line
  ok   B2 ...and the way out
  ok   B2 nothing committed
  ok   B2 the index is HEAD
  ok   B2 the PRD is still claimed
  ok   B2 the record is untouched
  ok   B2 --widen exits 0
  ok   B2 --widen commits both lines
  ok   B2 --widen said on the line
  ok   B3 one untouched line between: exit 0
  ok   B3 the worker's line is in HEAD~1
  ok   B3 the foreign line is not
  ok   B3 ...and stays in the tree
  ok   B3 by hunk on the line
  ok   B4 a merged insertion is refused
  ok   B4 named at the working line
  ok   B5 a baseline hunk undone before collect is not two authors
  ok   B5 the worker's line landed
  ok   B6 the record with adjacent hunks goes whole
  ok   B6 ...four ticks in HEAD~1
C. reproduced at e8b262d: a parent whose children are all done has no way to done
  ok   C1 the old collect refuses it
  ok   C1 ...on its state
  ok   C1 the old scan does not list it under collect
C. scan lists it, collect closes it in one commit
  ok   C2 scan lists big under collect — compute_plan's one list, the row without a why
  ok   C2 ...and not big/first
  ok   C2 --dry exit 0
  ok   C2 --dry says the phrase
  ok   C2 --dry names the sum and the sha
  ok   C2 --dry writes nothing
  ok   C2 exit 0
  ok   C2 done
  ok   C2 actual is the children's sum
  ok   C2 commit: is the last child's
  ok   C2 one commit
  ok   C2 its subject
  ok   C2 its paths: the parent's prd.md alone
  ok   C2 clean under it
  ok   C2 the line
  ok   C2 a transition row
  ok   C2 collecting it again is refused
  ok   C3 a parent with its own spec is not listed under collect
  ok   C3 ...and collect refuses it
  ok   C3 ...on its state — ordinary held work, the specs decide
  ok   C3 nothing written
  ok   C4 a parent with an open box of its own is refused
  ok   C4 nothing written
  ok   C5 a child still open: refused
  ok   C5 ...and not listed
  ok   C6 a parent that finished its own work goes the ordinary way
  ok   C6 ...two commits
  ok   C6 ...the record commit last
  ok   C6 ...never as a container
D. the posted report is in the commit
  ok   D the daemon came up on a spare port
  ok   D exit 0
  ok   D report posted
  ok   D ## Report is in HEAD~1
  ok   D ...holding the verify's exit
  ok   D the folder is clean
  ok   D the real registry is untouched
Z. hygiene
  ok   Z no path under .pearde/prds/.claims/ on any commit above
  ok   Z the bare collect exits 0
  ok   Z ...and closes finished
  ok   Z ...and big
  ok   Z two lines

101 checks · 101 pass · 0 fail
pearde doctor — /Users/feb/dev/infra/pearde

  skills      ok      16 well-formed · pearde-doctor pearde-drill pearde-grammar pearde-graph pearde-knowledge pearde-master pearde-memo pearde-persona-ask pearde-persona-create pearde-persona pearde-report pearde-scout pearde-update pearde-view pearde-workflow pearde 
                      installed where your agent looks — @references/install.md, then: bash /Users/feb/dev/infra/pearde/resources/install.sh --apply <skills-dir>
  plugins     ok      4 suggested · all installed on this machine
  index       ok      130 files · 33 keywords · every anchor resolves
  statusline  ok      ~/dev/infra/pearde board-wiki-obsidian-work-together *17 ↑4
                      ▸pearde 66/69 97% · +3d · open 3 3% · ▸board · ▸vault
                      wire it where your setup runs a command for one — @references/install.md
  guard       ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json · MAX_THINKING_TOKENS=8000 · skill tree guarded
  board       ok      /Users/feb/dev/infra/pearde/.pearde/prds · 95 PRDs · language English
  vault       ok      /Users/feb/dev/infra/pearde/.pearde/.obsidian · registered with Obsidian — ▸vault opens this board
  vision      ok      1 terminal · 0 on · 6 off · longest chain 0
  origin      broken  3 derived in flight vs 3 requested — the board is working on itself
                      fix: put the split to the user: continue, defer the derived tree, or drop it
  memos       ok      27 memos · frontmatter checks out
  workflows   ok      5 workflows · 13 atomics · the library checks out
  grammar     ok      170 terms · the vocabulary checks out
  knowledge   ok      18 notes on record · graph in sync · pending honest
  briefs      ok      5 blocks in references/parts/workers.md · every placeholder named · the verdict line named
  questions   ok      1 PRD carries a pass · each asks and offers an answer
  view        ok      watching · http://127.0.0.1:8443/board/pearde
  plan        ok      planned 2026-09-02
  harnesses   off     53 harnesses · not run — this row costs tens of seconds
                      fix: harnesses: on in /Users/feb/dev/infra/pearde/.pearde/settings.md, or one run: bash /Users/feb/dev/infra/pearde/resources/doctor.sh --harnesses /Users/feb/dev/infra/pearde
  jstests     off     not run — opt in: bash /Users/feb/dev/infra/pearde/resources/doctor.sh --harnesses /Users/feb/dev/infra/pearde

pearde: something is installed and not working — the fixes are above.
doctor rows this footprint answers for, ok: 4 of 4
fatal: ambiguous argument 'HEAD~1': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
fatal: path 'dup.md' exists on disk, but not in 'HEAD~1'
