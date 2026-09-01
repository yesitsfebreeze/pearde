# the-brief-names-the-verdict-line-collect-requires — analyst report

Verdict: SPECCED

The build went through end to end. Both defects are repaired in the tree,
uncommitted, and a probe harness holds them closed. Two specs, complexity 16
total, well under the board's 40/6 limits.

- `specs/spec01.md` — complexity 6 — the brief names the `Verdict:` line, and
  the rewrap's leftover continuation goes. Footprint
  `references/parts/workers.md`.
- `specs/spec02.md` — complexity 10 — a `briefs` check that fails on the
  defect it just found. Footprint `resources/board/brief.py`,
  `resources/doctor.sh`.

Union of footprints: `references/parts/workers.md`, `resources/board/brief.py`,
`resources/doctor.sh`.

**complexity: 16** — two edits to one prose file plus two rules in an existing
checker, with no data structure, no new file in the manifest, and no behaviour
change to any tool. The weight is in getting the wording exact, not in volume.

**blast-radius: mid** — `workers.md` is the single source of the brief handed
to every worker on every board, so a wrong edit misdirects all of them at
once; but the change is additive text, the tool it describes is untouched, and
both the `doctor` row and the probe go red immediately if it regresses.

**workflow: correct-a-documented-claim** — it fits and I took all six steps in
order: read-the-contract, capture-the-harness-baseline, edit-inside-the-
footprint, sweep-for-other-copies, re-run-the-harnesses, run-the-repo-gate.
The library holds it; I wrote no new file. Nothing in the run needed a step the
route does not have, and no back-edge was taken.

## What the build did

**The reproduction was my own brief**, as the dispatch said. Before the first
edit: `Verdict:` occurred **0** times in the rendered analyst brief, and the
duplicated half-sentence occurred **2** times.

**The fix went into `brief:every`, not the analyst block.** `brief.py:340`
appends `blocks["every"]` to the analyst's brief *and* the implementer's; the
consultant (`:361`) never receives it, and the consultant is the one role that
writes no report. So one edit covers exactly the two roles that need it and no
role that does not — verified: the consultant brief still carries no
`Verdict:` line. The PRD located the gap at the analyst block's "Return exactly
one verdict:" (`:163-164`); the implementer block has the identical gap, and
`brief:every` is the only place that closes both at once.

**Line 156 deleted**, as the PRD specified. The half-sentence now appears once.

**The doctor row was overstating.** `briefs` read `ok — 5 blocks · every
placeholder named` throughout, because `check()` read only the brief's frame:
marker pairs and placeholders. It now also reads content, and the row says so.

After: analyst brief `Verdict:` = 1, implementer = 1, consultant = 0, duplicate
= 1. Probe: 22 assertions, 0 FAIL.

## Finding — `verdict_of` tolerates less decoration than the tree claims

The PRD (citing `collect.py:258`) says `verdict_of` "is generous about
decoration — bold, headings". Measured across fifteen line shapes, that is
**half true**, and the exception is the shape a worker is most likely to
write. Emphasis *before* the colon is fine; a marker *between* the colon and
the word is not:

| shape | read as |
|---|---|
| `Verdict: SPECCED`, `## Verdict: SPECCED` | SPECCED |
| `**Verdict**: SPECCED`, `**Verdict: SPECCED**` | SPECCED |
| `**Verdict:** SPECCED` | **nothing** |
| `*Verdict:* SPECCED` | **nothing** |
| `- Verdict: SPECCED` | **nothing** |
| `> Verdict: SPECCED` | **nothing** |

`**Verdict:** SPECCED` and a bulleted `- Verdict: …` are ordinary markdown. The
regex `\*{0,2}([A-Za-z]+)` cannot cross the space between the closing `**` and
the word.

The PRD forbids loosening the tool, and I did not: `verdict_of` is
byte-identical to `HEAD`, asserted in the probe. Instead the brief now names
the shape that works — one word after the marker, nothing else on the line, not
in a list item and not in a block quote — and the probe pins the four refused
shapes, so the warning cannot go stale while still being printed.

**The docstring is a wrong claim in the tree.** Per the brief that is a
finding, not a fix: `collect.py:258` should not say "bold" without
qualification. It is one sentence in a file another PRD is currently editing.

## Findings outside my scope — not fixed, not filed

- **A harness asserts on my footprint file and was red before my first edit.**
  `.pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh` exits
  1, failing on a table row it expects in `references/parts/workers.md` and
  which the file does not contain (it looks for the phrase "any of the three,
  plus" beside a `## Workflow` slug row). Recorded failing before any edit of
  mine; identical output and exit code after. That harness is measuring a row
  someone removed or never added, not anything this PRD touched.
- **A machine-state failure, not a code one.**
  `.pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh` fails `H
  no fixture of this run reached Obsidian's vault list — got: 0`. It reads
  Obsidian's machine-wide vault register, which none of my three files touch;
  the harness's own comment calls that file "a machine-wide resource every
  session's probes write to". A fixture leaked there from another session.
- **A sibling session is editing `resources/board/collect.py` and
  `resources/board/init.py`** — an `--also` guard (`also_path`, `check_also`).
  Additive, and it does not touch `verdict_of`. It is why spec01's box compares
  only the `VERDICT_RE`…`scores_of` span to `HEAD` and not the whole file: a
  whole-file diff there would measure that session's work, not this one's
  restraint.

## The record

`knowledge.py query` returned 11 hits, 10 strong; the top hit
`[[260901-90ed]] collect-report-routes-the-verdict` already holds the routing
mechanism, so I cited it rather than re-deriving it. **No gap was enqueued** —
`.pearde/wiki/pending/` holds 6 entries, all dated before this run. Nothing was
learned outside this repo, so nothing was written back.

## Baseline and harnesses

Ten harnesses read `workers.md` or `brief.py`; all were run before the first
edit and again after. Every one returns its baseline exit code and its baseline
`ok` count — 53, 21, 104, 58, 60, 85, 47 unchanged; the only diffs are
`mktemp` directory names. `index.py check` exits 0 and `doctor.sh` exits 0,
both before and after, with `briefs` the single row whose text changed and
this PRD the reason it did.

## Scores

complexity: 16
blast-radius: mid
workflow: correct-a-documented-claim
