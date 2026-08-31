# Report — the-knowledge-loop-runs-in-the-round

Verdict: DONE.

Implementer re-verification pass (impl-17). The analyst's pass had already
applied both halves and pre-ticked all 7 boxes; this session re-measured every
box against what is on disk right now, ran both spec verify blocks verbatim
under `bash -e -o pipefail`, and ran the repo's gate. All 7 held; none
unticked. Scan: `the-knowledge-loop-runs-in-the-round · boxes 7/7`.

## State note — the work is committed, not "in the tree"

The specs describe the probe's edits as uncommitted. They no longer are:
another PRD's collect (`eef2dba`, a-route-is-written-at-spec-time, 18:40,
before this PRD's 19:21 claim) committed the whole code repo, including this
PRD's then-uncommitted footprint edits. `git status` shows
`references/parts/loop.md` and `references/parts/workers.md` clean. The
changes are on disk and correct; the whole-repo-commit attribution is
collect's own behaviour, reported only.

## Per-spec box status (each re-run independently)

spec01 — 4/4:
- [x] "Eight steps, in order." — grep hit (line 3).
- [x] `^| 7 knowledge ` and `^| 8 drill, then stop ` both hit, in order.
- [x] steps 1–6 unchanged by the knowledge edit — proven against the
      pre-change blob `96231df` (the image `eef2dba`'s diff was cut from):
      rows 1–3, 5, 6 identical; row 4's command column (`--worker <worker>`)
      changed in the same commit by the *other* PRD's spec01, not the
      knowledge step, which only added row 7 and renumbered 7→8.
- [x] `**7 · Knowledge.**` (line 138) precedes `**8 · Drill, then stop.**`
      (line 146).

spec02 — 3/3:
- [x] `<!-- brief:analyst -->` opens with `Query the record first` (line 133)
      before the `Read .pearde/prds/<prd>/prd.md` line (line 139); the
      workflow-route sentence another PRD added between them does not affect
      this ordering.
- [x] `<!-- brief:every -->` carries `A fact learned outside this repo`
      (line 61); token dump holds only `<language>`, `<prd>` — no unnamed
      placeholder, `brief.py --check` clean.
- [x] `python3 resources/board/brief.py --check` exit 0 (re-run, no output).

## Verify output (both blocks verbatim)

```
spec01: loop.md carries eight steps, 7 knowledge before 8 drill — ok
spec01-block-exit: 0
spec02: workers.md queries first, writes findings back — ok
spec02-block-exit: 0
```

## Repo gate (`.pearde/settings.md ## Deliverable`)

```
index-check: 0
memos-check: 0
doctor-exit: 0
pearde: every part this repo owns checks out.
```

## Findings (updated this pass)

- The analyst's reported `brief_prd()` arity bug is fixed by commit `0849795`
  (collect-commits-the-code-repo-not-the-board-repo-twice): brief.py now
  calls `collectlib.repo_of(prd, board, board_root)`, matching collect.py's
  signature. spec02's note updated. Nothing left on this PRD's side.
- Stale PRD wording, unchanged: the contract says a gap lands in
  `prds/knowledge/pending/`; `resources/knowledge.py` `default_root()`
  writes `.pearde/wiki/pending/` (`auto_enqueue: True`, line 52). The specs
  use the real path.
- `<the PRD's question>` / `<title>` literal safety against `TOKEN_RE`
  (`<[a-z][a-z_/]*>`) still holds; the suggested placeholder-section line in
  workers.md stays report-only (widens the contract).

---

# Prior analyst pass (superseded by the DONE above, kept for history)

## What the build did

`resources/board/brief.py` composes every worker's brief from
`<!-- brief:<role> -->` blocks in `references/parts/workers.md`, filling
only its named placeholder table. `resources/knowledge.py query` already
auto-enqueues a gap into `.pearde/wiki/pending/` (`auto_enqueue` default
true) — no new verb, no tool-surface change, per the PRD's constraint.

Applied directly, in the tree, uncommitted, both closed and verified:
- `references/parts/loop.md` — spec01. Eight steps now, a new `7 knowledge`
  step before the renumbered `8 drill, then stop`: query the record for a
  fork about to be drilled, answer it under `## Answers` on a strong hit
  instead of asking the user, change nothing on a gap or thin hit (the gap
  is already queued). No other step reordered.
- `references/parts/workers.md` — spec02. `<!-- brief:analyst -->` opens
  with `python3 resources/knowledge.py query "<the PRD's question>"` before
  reading the PRD. `<!-- brief:every -->` adds: a fact learned outside the
  repo is written back with `knowledge.py remember`/`conclude`, never left
  standing only in the report. `brief.py --check` exits 0.

## Findings

- **`<title>` is not a safe literal placeholder.** `brief.py`'s `TOKEN_RE`
  matches any `<all-lowercase-letters>`, so a first draft of the `every`
  block ("`remember <title>`") tripped `brief.py --check` ("not in the
  placeholder table"). Fixed by naming the verb with no bracketed argument.
  `<the PRD's question>` (space, apostrophe) and `<dir-name>` (hyphen)
  survive because they don't match the pattern — worth a line in
  `references/parts/workers.md`'s own placeholder section for the next
  editor, but that's widening this PRD's contract, so report only.
- **Pre-existing bug, out of this PRD's footprint (now fixed):**
  `brief_prd()` called `collectlib.repo_of(prd, board_root)` with 2 args
  against `repo_of(prd, board, board_root)` — a `TypeError` on every real
  render. Fixed by commit `0849795`; brief.py now passes three args.
- The PRD's own contract text says a gap "lands in `prds/knowledge/pending/`";
  the tool actually writes `.pearde/wiki/pending/`
  (`resources/knowledge.py` `default_root()`, and `.pearde/wiki/` already
  exists on this board). Specs use the real path; the PRD's wording is
  stale.
- A job that may recur: hand-editing a `<!-- brief:role -->` blockquote
  block in `workers.md` by exact old/new text match, and knowing which
  literal `<...>` shapes are safe against `TOKEN_RE`. Small now; worth a
  workflow if briefs get touched often.

## Scores

complexity: 11
blast-radius: mid — workers.md and loop.md are read by every dispatch and
  every round; the edits are additive and gated by `brief.py --check`,
  which passes clean.
workflow: none fit
