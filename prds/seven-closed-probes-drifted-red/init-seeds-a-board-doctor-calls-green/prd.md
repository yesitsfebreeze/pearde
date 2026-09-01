---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 0        # higher first
complexity: 12      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.76h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
needs:
  - the-doctor-completes-without-a-home
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

# init-seeds-a-board-doctor-calls-green — a fresh `init --example` board passes doctor: the memo kind-index is regenerated after the copy, the knowledge graph is planted the way upgrade does it, and quickstart proves it running doctor under a HOME that holds no Obsidian config

a fresh `init --example` board passes doctor: the memo kind-index is regenerated after the copy, the knowledge graph is planted the way upgrade does it, and quickstart proves it running doctor under a HOME that holds no Obsidian config

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
575:        indexed = index_memos(board)
3
349:def index_memos(board):
395:def plant_graph(board):
A. init --example lands a board, and says what it seeded
  ok    A init --example exits 0
  ok    A ...and names the index it regenerated
  ok    A ...and the board verb of the knowledge layer
  ok    A ...and the relink that writes the graph
B. the memo kind-index exists and is not stale
  ok    B memos/README.md is on the board
  ok    B memo check exits 0
  ok    B ...and says nothing
  ok    B the index is the generated page, not a copied one
  ok    B ...and byte-identical to the example board's own page
  ok    B the failing-index mutation reached the copy
  ok    B a failing memo index is said, not swallowed
  ok    B ...naming what memos.py reported
  ok    B ...and the copy is restored
C. the knowledge graph is planted the way upgrade plants it
  ok    C wiki/.graphify/graph.json exists
  ok    C knowledge doctor exits 0
  ok    C ...and calls the graph in sync
D. doctor calls the fresh board green
  ok    D doctor exits 0
  ok    D ...and closes green
  ok    D the memos row reads ok
  ok    D the knowledge row reads ok
  ok    D init ran that same doctor and it closed green there too
E. doctor under a home that holds no Obsidian config
  ok    E doctor exits 0 there
  ok    E ...and closes green
  ok    E the vault row answers rather than faulting
  ok    E ...naming the machine, not the board
  ok    E the row reader read the whole report — 18 rows, not zero
  ok    E no row's verdict moves between the two homes
  ok    E doctor did not trip over an unset name
F. an empty board is still empty — no page written over nothing
  ok    F init exits 0
  ok    F memos/ holds no generated index — there is nothing to index
  ok    F ...and init claims none
  ok    F doctor calls the empty board green too
G. upgrade over the same board changes nothing it already has
  ok    G upgrade exits 0
  ok    G ...and finds the wiki seeded
  ok    G doctor is still green after it
H. the harness this unit's red surfaced in
  ok    H quickstart.sh exits 0
  ok    H ...and every check passed
  ok    H ...including the leg this unit owes it
  ok    H ...whose vault row answered there
  ok    H ...and whose doctor closed green there
I. nothing of this machine's was written to
  ok    I the live daemon's registry is untouched

41 checks · 41 pass · 0 fail · 0 skip
A. init --example lands a board, and says what it seeded
  ok    A init --example exits 0
  ok    A ...and names the index it regenerated
  ok    A ...and the board verb of the knowledge layer
  ok    A ...and the relink that writes the graph
B. the memo kind-index exists and is not stale
  ok    B memos/README.md is on the board
  ok    B memo check exits 0
  ok    B ...and says nothing
  ok    B the index is the generated page, not a copied one
  ok    B ...and byte-identical to the example board's own page
  ok    B the failing-index mutation reached the copy
  ok    B a failing memo index is said, not swallowed
  ok    B ...naming what memos.py reported
  ok    B ...and the copy is restored
C. the knowledge graph is planted the way upgrade plants it
  ok    C wiki/.graphify/graph.json exists
  ok    C knowledge doctor exits 0
  ok    C ...and calls the graph in sync
D. doctor calls the fresh board green
  ok    D doctor exits 0
  ok    D ...and closes green
  ok    D the memos row reads ok
  ok    D the knowledge row reads ok
  ok    D init ran that same doctor and it closed green there too
E. doctor under a home that holds no Obsidian config
  ok    E doctor exits 0 there
  ok    E ...and closes green
  ok    E the vault row answers rather than faulting
  ok    E ...naming the machine, not the board
  ok    E the row reader read the whole report — 18 rows, not zero
  ok    E no row's verdict moves between the two homes
  ok    E doctor did not trip over an unset name
F. an empty board is still empty — no page written over nothing
  ok    F init exits 0
  ok    F memos/ holds no generated index — there is nothing to index
  ok    F ...and init claims none
  ok    F doctor calls the empty board green too
G. upgrade over the same board changes nothing it already has
  ok    G upgrade exits 0
  ok    G ...and finds the wiki seeded
  ok    G doctor is still green after it
H. the harness this unit's red surfaced in
  skip  the readme quickstart is left to the sweep's own run of it — it runs that harness directly, and running it twice buys nothing
I. nothing of this machine's was written to
  ok    I the live daemon's registry is untouched

37 checks · 36 pass · 0 fail · 1 skip
0
0

spec02: exit 0
113:OUT="$(env -u XDG_CONFIG_HOME HOME="$NOOBS" bash "$COPY/resources/doctor.sh" "$PROJ" 2>&1)"; RC=$?
111:rows() { printf '%s\n' "$1" | sed -nE 's/^  ([a-z]+) +(ok|broken|off) .*/\1 \2/p'; }
120:    "$(printf '%s\n' "$OUT" | sed -nE "s/^  vault +(ok|broken|off) .*/\\1/p")" "ok"

$ python3 <repo>/resources/pearde.py install --apply /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills
pearde install — /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde → /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills

                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-doctor
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-drill
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-graph
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-knowledge
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-master
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-memo
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-persona-ask
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-persona-create
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-persona
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-report
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-scout
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-update
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-view
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde-workflow
                          ✓ built /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/skills/pearde
                          ✓ /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/agents/pearde-analyst.md -> references/agents/pearde-analyst.md
                          ✓ /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/agents/pearde-implementer.md -> references/agents/pearde-implementer.md
                          ✓ /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/agents/pearde-round.md -> references/agents/pearde-round.md
                          ✓ dataview 0.5.68 -> /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/board/obsidian/plugins/dataview
                          ✓ obsidian-local-rest-api 5.1.0 -> /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/board/obsidian/plugins/obsidian-local-rest-api

pearde install: built.
  add to your shell, nothing here writes it — one word for every tool, and who is working:
  alias pearde='python3 /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/pearde.py'
  export PEARDE_AS=engineer

$ pearde init --example
board example · language English — pearde settings language=<l> changes it
init: wrote /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/settings.md and vision.md from the example board
init: .gitignore += .pearde/.state/ .pearde/wiki/ .obsidian/
init: regenerated memos/README.md, the memo index by kind — the copy carries the memos, `memo index` writes the page over them
init: knowledge layer at .pearde/wiki/ — .graphifyignore, Dashboard.md, WORKFLOW.md, conclusions/_index.md, sources/_index.md, sources/.absorbed/_index.md · Dashboard.md is the vault's front page, WORKFLOW.md its configuration
init: knowledge board — board: 8 PRD note(s), 2 memos scanned
init: knowledge relink — relink: 0 nodes, 0 edges -> /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/wiki/.graphify/graph.json
init: obsidian vault at .pearde/ (its own root, so every board folder shows) — plugins: dataview, obsidian-local-rest-api · dataview serves the live views from the first open, local-rest-api (local-rest-api with MCP) answers on 127.0.0.1:27124 (key: .pearde/wiki/.obsidian-api-key) after Obsidian loads the vault once
init: registered .pearde/ with Obsidian — but Obsidian is running, and it rewrites its vault list from memory when it quits, which erases this. Run: pearde vault --wait --open, then quit Obsidian — the entry is written the moment it exits and the vault opens
serve: started on http://127.0.0.1:54622
serve: registered example · /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde · live view http://127.0.0.1:54622/board/example
pearde doctor — /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj

  skills      ok      15 well-formed · pearde-doctor pearde-drill pearde-graph pearde-knowledge pearde-master pearde-memo pearde-persona-ask pearde-persona-create pearde-persona pearde-report pearde-scout pearde-update pearde-view pearde-workflow pearde 
                      installed where your agent looks — @references/install.md, then: bash /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/install.sh --apply <skills-dir>
  plugins     ok      4 suggested · all installed on this machine
  index       ok      125 files · 32 keywords · every anchor resolves
  statusline  ok      /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj
                      ▸pearde 2/8 15% · open 3 38% · ▸board · ▸vault
                      wire it where your setup runs a command for one — @references/install.md
  guard       off     not wired in /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.claude/settings.json
                      fix: pearde guard on — writes the block of @references/parts/guard.md into /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.claude/settings.json, then /hooks or restart (python3 /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/pearde.py guard on)
  board       ok      /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/prds · 8 PRDs · language English
  vault       ok      /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/.obsidian · registered with Obsidian — ▸vault opens this board
  vision      ok      vision declared · no terminals — no axis
  origin      ok      8 requested · nothing derived
  memos       ok      1 memos · frontmatter checks out
  workflows   ok      1 workflow · 2 atomics · the library checks out
  knowledge   ok      0 notes on record · graph in sync · pending honest
  briefs      ok      5 blocks in references/parts/workers.md · every placeholder named
  questions   ok      1 PRD carries a round · each asks and offers an answer
  view        ok      watching · http://127.0.0.1:54622/board/example
  plan        ok      planned 2026-09-01
  harnesses   off     no verify.sh under /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde — a PRD gets one when it is specced
  jstests     off     not run — opt in: bash /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/pearde/resources/doctor.sh --harnesses /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj

pearde: every part this repo owns checks out.
pearde guard on — optional, refuses the waste the loop's rules name
http://127.0.0.1:54622/board/example
pearde add "<title>"
pearde

$ pearde add "Ship the quickstart"
▸ ship-the-quickstart: — → open · done 2/9 · 14% · open 4/9 · 44% · ready 2 · blocked 5 · collect 1 @1 workers · as engineer

$ pearde
board: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde · 9 PRDs · workers=1 · asking 1 over 1 PRD
vision: <one sentence — the destination>
counts: open 4 · done 2 · claimed 2 · question 1
progress: done 2/9 · 14% · open 4/9 · 44%

collect — 1 finished, waiting to be closed
  claimed   · finished · p55 · w0 · boxes 3/3 · claim worker-finished since 2026-08-28 12:00

waiting on you — 1
  question  · asking · p65 · w15

in flight — 1 held by a worker
  claimed   · building · p60 · w8 · wf fix-a-line · boxes 3/5 · claim worker-building since 2026-08-28 13:49 · silent 48.5h

ready — 2 dispatchable now, in order
  open      · big/second · p62 · w9
  open      · ship-the-quickstart · p0 · w13

gated — 2, as their gates clear
  open      · big · p62 · w0 · needs second
  open      · next · p58 · w12 · needs building

round: /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/.state/round.md  (not written)

$ pearde view
serve: watching example · /private/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde · live view http://127.0.0.1:54622/board/example

$ HOME=<a home with no Obsidian config> pearde doctor
  vault       ok      /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.RCW41lp8ZL/proj/.pearde/.obsidian · Obsidian not installed here, so nothing to register
  memos       ok      1 memos · frontmatter checks out
  knowledge   ok      0 notes on record · graph in sync · pending honest
pearde: every part this repo owns checks out.

37 checks · 37 pass · 0 fail
FAIL: G index.py check is silent — got '115', want '0'
74 checks · 73 pass · 1 fail
0
A. init --example lands a board, and says what it seeded
  ok    A init --example exits 0
  ok    A ...and names the index it regenerated
  ok    A ...and the board verb of the knowledge layer
  ok    A ...and the relink that writes the graph
B. the memo kind-index exists and is not stale
  ok    B memos/README.md is on the board
  ok    B memo check exits 0
  ok    B ...and says nothing
  ok    B the index is the generated page, not a copied one
  ok    B ...and byte-identical to the example board's own page
  ok    B the failing-index mutation reached the copy
  ok    B a failing memo index is said, not swallowed
  ok    B ...naming what memos.py reported
  ok    B ...and the copy is restored
C. the knowledge graph is planted the way upgrade plants it
  ok    C wiki/.graphify/graph.json exists
  ok    C knowledge doctor exits 0
  ok    C ...and calls the graph in sync
D. doctor calls the fresh board green
  ok    D doctor exits 0
  ok    D ...and closes green
  ok    D the memos row reads ok
  ok    D the knowledge row reads ok
  ok    D init ran that same doctor and it closed green there too
E. doctor under a home that holds no Obsidian config
  ok    E doctor exits 0 there
  ok    E ...and closes green
  ok    E the vault row answers rather than faulting
  ok    E ...naming the machine, not the board
  ok    E the row reader read the whole report — 18 rows, not zero
  ok    E no row's verdict moves between the two homes
  ok    E doctor did not trip over an unset name
F. an empty board is still empty — no page written over nothing
  ok    F init exits 0
  ok    F memos/ holds no generated index — there is nothing to index
  ok    F ...and init claims none
  ok    F doctor calls the empty board green too
G. upgrade over the same board changes nothing it already has
  ok    G upgrade exits 0
  ok    G ...and finds the wiki seeded
  ok    G doctor is still green after it
H. the harness this unit's red surfaced in
  ok    H quickstart.sh exits 0
  ok    H ...and every check passed
  ok    H ...including the leg this unit owes it
  ok    H ...whose vault row answered there
  ok    H ...and whose doctor closed green there
I. nothing of this machine's was written to
  ok    I the live daemon's registry is untouched

41 checks · 41 pass · 0 fail · 0 skip
