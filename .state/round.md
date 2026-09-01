# Round — the five answers became board state; five analysts are out

Written by session `f54db065`, 2026-09-02, resuming the previous round's
`ASK`. **The user answered all five forks of `.pearde/.state/ask.md`, every
answer was the recommended one, and this round turned all five into work on
the board.** The board is no longer drained.

`done 64/68 · 94% · derived 19/20 · open 1/90 · analyzing 4`. Four analysts
dispatched; `upgrade-leaves-the-memo-index-stale` left `open` and unclaimed
for the next window.

## The five answers, and what each became

| fork | the user said | landed as |
|---|---|---|
| Q1 | *Fix it — bringing a board forward should leave it exactly as healthy as creating one fresh.* | `release upgrade-leaves-the-memo-index-stale open`, then claimed — the parked PRD is back and out with an analyst |
| Q2 | *Refuse to file at all rather than write a record naming a file it does not hold.* | new PRD `filing-refuses-a-file-it-does-not-hold` p30 |
| Q3 | *Add it to the instructions, so following them produces something that is accepted.* | new PRD `the-brief-names-the-verdict-line-collect-requires` p30 |
| Q4 | *Bring each one back in line with how things work now, so a failure means something again.* | new PRD `four-stale-self-tests-are-re-aimed-at-the-code-that-moved` p20 |
| Q5 | *Run them a few at a time, so a failure is always a real one.* | new PRD `the-harness-sweep-is-capped-so-a-red-is-a-real-red` p40 |

Each of the four new PRDs carries the previous round's verified mechanism in
its body, with the line numbers and the 23:20/23:26 timestamps on it, plus the
fork the user rejected written as an explicit non-goal. **The analysts do not
need to re-establish any of it** — the bodies say so in as many words.

Three folds were made deliberately at filing time, and the next round must not
undo them:

- The **duplicated half-sentence at `references/parts/workers.md:155-156`** is
  folded into Q3's PRD, not filed separately — it is the same file and there
  is no second reading to choose between. *(Confirmed live this round: it is
  visible at lines 9-10 of every analyst brief `pearde brief` generates.)*
- The **`init-seeds-a-board-doctor-calls-green` TOCTOU** (`probe/verify.sh:35`
  binds port 0 and closes the socket before use) is in **Q5's** PRD, not Q4's.
  It is a port race, not a stale check. Q4's body says so explicitly so it is
  not fixed twice.
- The **vacuous sibling checks** — *"the real registry is untouched"* in both
  `collect-is-a-command` and `init-asks-nothing`, comparing empty to empty
  against the vanished `resources/board/state/serve.json` — are in Q4's scope.
  Re-aiming only the loud check leaves the harness green and blind.

`the-collect-and-brief-harnesses-are-carried-across-the-layout` is downstream
arithmetic over `collect-is-a-command` and is named a non-goal in Q4's body:
fix the sibling and it clears itself.

## The one constraint that is not ours to relax

Two of Q4's four stale checks pin **the view session's deliberate changes** —
`render.py:459` (`eaa11a1`) and `view.css:508` (`4ce11ec`). Q4's body forbids
editing either file to satisfy a check: the check moves to the code, never the
reverse, and a change that looks necessary there is a QUESTION, not an edit.
The view / ⌘K session owns those files. If an analyst comes back wanting to
touch them, that is a fork for the user, not an override.

## Five claims out — resume, never replace

| PRD | worker id |
|---|---|
| `the-harness-sweep-is-capped-so-a-red-is-a-real-red` | `analyst-the-harness-sweep-is-capped-so-a-red-is-a-real-red` |
| `filing-refuses-a-file-it-does-not-hold` | `analyst-filing-refuses-a-file-it-does-not-hold` |
| `the-brief-names-the-verdict-line-collect-requires` | `analyst-the-brief-names-the-verdict-line-collect-requires` |
| `four-stale-self-tests-are-re-aimed-at-the-code-that-moved` | `analyst-four-stale-self-tests-are-re-aimed-at-the-code-that-moved` |
| `upgrade-leaves-the-memo-index-stale` | `analyst-upgrade-leaves-the-memo-index-stale` |

Each analyst was fenced to its own files at dispatch, so the five do not
collide: `resources/doctor.sh` + the port-racing harnesses (Q5),
`resources/board/collect.py` (Q2), `references/parts/workers.md` (Q3), four
stale harness checks (Q4), `resources/board/init.py` (Q1). Every one was told
the mechanism is already established and is not to be re-derived, and was
handed the fork the user rejected as an explicit non-goal.

All five were confirmed alive after dispatch and again mid-run — transcripts
growing, `API Error` count 0 on each. Their briefs are staged at
`/private/tmp/claude-501/-Users-feb-dev-infra-pearde/f54db065-9498-4db2-b176-a7f14d5ea4b5/scratchpad/brief-<slug>.txt`;
regenerate rather than reuse if that scratch is gone.

This file names all four, so `sweep --apply` leaves them. A worker its
infrastructure killed is **resumed**, not swept — it holds the context.
`brief` on a claimed PRD takes `--worker <the claim's id>`, which is the row
above.

## Carried, uncommitted, and still owed

`.pearde/report.md` and this file are modified in the board worktree and NOT
committed — the previous round rewrote the report to contract
(`references/report.md` + `templates/report.md`), taking
`one-page-that-says-whats-up` from `26 pass · 5 fail` to `29 pass · 2 fail`.
Both are tracked; `.state/ask.md` is ignored. **Carry them on the first
collect that opens.**

`memos/one-typo-crashes-every-round.md` is the only memo at `status: open` and
is **stale, not undecided** — it describes a non-numeric `complexity` crashing
`scan` board-wide, and that crash is fixed: `spec_data` is `plan.py:479` and
reads `num(fm, "complexity", where) or dur(…)`; `num` at `:733` is documented
*"Never raises"* and returns `0.0` after `bad_value()`. **It wants closing,
not answering.** Close it on the next collect that opens the memo dir.

## Owed, none of it blocking

`a-probe-that-prints-no-count` (`run-all.sh` `printf "" "$out"` twice — every
row reads `pass=0 fail=0`). `spec01` box 8 of the init PRD wants an existence
anchor. `memos.py index` could print a path it did not write. graph-probe
spec02 check A is a spelling-grep and its `prd.md` is still the unfilled
template. The `18`-row doctor tripwire lives in two committed harnesses.
`reportParts()` in view.js parses 3 of 4 parts. `doctor.sh --harnesses .`
renders the board name `?` from a relative path.

## Settled — cite, do not re-establish

- `doctor` exits 0; `knowledge` was fixed last round by
  `python3 resources/knowledge.py relink` (11 nodes, 14 edges). `graph.json`
  is gitignored.
- `doctor.sh:46` is verbatim `START="${1:-$PWD}"` under `set -uo pipefail`
  (`:33`) — correct as recorded, low risk.
- **Retired, do not carry forward**: the `ignore_patterns("README.md")`
  consequence (already fixed — `index_memos()` at `init.py:349` regenerates
  after the copy); the `doctor.sh:743` "analyst hunk adopted" claim (never
  true — `:700-798` landed whole in `7809756`); the node_modules paragraph.
- `.state/round.HANDOFF-collect1-will-fail.md` — the alarming name is stale
  and the file says so. Ignore it.

## Sessions and traps

`jstests` is `off` because *its* `playwright-core` is missing, not our doing.
`pearde-eb` and `pearde-19` are stood down. The view / ⌘K session's files are
not ours.

Traps that still hold: `--also` needs the `.pearde/` prefix **until Q2's PRD
lands** — after which a bad path is refused outright, which is the point; a
spec's own `footprint:` has the same trap and is still not checked; after any
collect `git show --stat` the commits AND `git status` the board; SPECCED
commits nothing; **sonnet 402s, bare inherit 429s, pin `model: "opus"`**;
every board command needs a persona — `PEARDE_AS=engineer`, or `sweep`
refuses.
