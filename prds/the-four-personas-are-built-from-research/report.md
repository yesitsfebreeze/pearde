# impl-personas — the-four-personas-are-built-from-research

Verdict: DONE

workflow: probe-then-spec
worker: impl-personas · as engineer · 2026-09-02
pass: two (the analyst's build was in the tree uncommitted; it was continued,
not rebuilt), plus one revision round on a collect hold

| spec | boxes | verify block |
|---|---|---|
| `specs/spec01.md` | 9 of 9 `[x]` | exit 0 |
| `specs/spec02.md` | 6 of 6 `[x]` | exit 0 |

`probe/check_personas.py` → `190 checks, 190 pass, 0 fail`.
`specced --check --as engineer` → ok · complexity 20.

**Read the limit before the number.** The 190 checks prove the four persona
files are internally consistent. They do not prove anyone ever said any of it.
Section "What 190/190 does not cover" below states that plainly and proposes
the wording the PRD's claim needs.

## What the revision round closed

### 1 — the block can no longer be reddened by a neighbour

Two reads reached outside the footprint. Both are gone; `spec01`'s block is now
hermetic, and the proof is mechanical rather than narrative.

- **`grep -q "| @$f |" references/files.md` — dropped.** `references/files.md`
  is not in this footprint and is ` M` under a sibling. It was a positive claim
  worth having and it was in the wrong place; no command's exit may be decided
  by a file outside the footprint, and that rule does not bend for a check that
  happens to be useful. Box 7 lost its manifest half with it, so no box is left
  standing on a check that no longer runs.
- **The probe no longer runs over the tree.** It runs over a fixture the block
  builds: the three footprint files copied in, and `engineer.md` and `INDEX.md`
  written by the block as stubs. A sibling renaming, `mv`-swapping or emptying
  either one cannot now produce an empty `out`, because neither is read. A
  `[ -n "$out" ]` guard sits in front of the greps anyway, failing with
  `the probe printed nothing — it died before its tally` rather than as a
  puzzling grep miss — `index()`'s `path.read_text` is unguarded and the probe
  prints nothing until every check has run, exactly as described.

Evidence, from the block's own text rather than from a run:

```
$ blk=$(awk '/^```sh/{f=1;next} /^```/{f=0} f' …/specs/spec01.md)
$ printf '%s\n' "$blk" | grep -nE 'engineer\.md|INDEX\.md|files\.md' | grep -v ':#'
44:sed 's/^@@ /## /' > "$tmp/base/references/personas/engineer.md" <<'STUB'
73:cat > "$tmp/base/references/personas/INDEX.md" <<'STUB'
```

Every remaining mention outside a comment is a **write into `$tmp`**.
`references/files.md` survives only in a comment. The three footprint paths are
the only tree paths the block hands to a reader. The stub is 644 bytes against
the tree's 3875 and is not a copy of it.

One incident worth recording, since the route's atomics do not list it: the
stub's `## How you work` and `## Built from` headings, sitting at line start
inside a heredoc inside the fenced block, ended the `## Verify and Proof`
section for `resources/board/specs.py` — which is line-based and fence-blind —
and `specced` refused with `spec01.md:45: ## Verify and Proof holds no fenced
sh block`. The stub now writes `@@ ` and raises it with `sed 's/^@@ /## /'`.
The workflow warns that the acceptance-box matcher is fence-blind; the section
matcher is too, and that is not written down anywhere.

**Box 7's flip.** Raised and left standing, deliberately: box 7 now asserts
only that `index.py check` names no footprint file, and no in-tree input makes
that go red without editing a footprint file's path out of the manifest, which
is a sibling's file. It is a weak box. It is honest about being weak, and the
strong version of it belongs to whoever owns `references/files.md`.

### 2 — what 190/190 does not cover

The reviewer is right and I am not going to paper over it. Stating it in the
words asked for: **the probe proves internal consistency, and the provenance
rests on the analyst's research and on nothing standing in the tree.**

What the 190 checks actually certify: the `## Built from` bullet shape parses,
the name a `## How you work` bullet traces to appears under `## Built from`,
the trait matches character for character, no practitioner backs zero bullets,
no gendered pronoun, `composite` in the first line, 3-6 behaviour bullets, one
`## Built from`. Every one of those is a relation between two parts of the same
file. An invented practitioner with an invented book satisfies all of them.

I did **not** take the knowledge-note route, and the reason is not cost.
`python3 resources/knowledge.py query` returns the three notes and they are
real — `.pearde/wiki/sources/260902-bf13.md` (designer),
`260902-498e.md` (skeptic), `260902-ae5c.md` (mentor), each a
`practitioner | trait taken | source` table with `provenance: "web research,
2026-09-02, dispatched worker"`. Tying each traced name to one of them would
be a genuine check of *something*. Two objections, and the second is the one
that decided it:

1. `.pearde/wiki/sources/` is outside this PRD's footprint. Gating on it puts
   back precisely the defect item 1 orders closed, one file further away.
2. Those notes were written by the same pass, by the same worker, from the same
   research. A fabricator fabricates both. The check would prove the persona
   file and the note **agree**, not that anyone said any of it — it raises the
   cost of *future* drift and says nothing about the original claim. Selling
   that as a provenance check would be the over-claim in a new place.

What I did instead, inside the footprint, is kill the specific hole that was
demonstrated. The only provenance-adjacent assertion was
`len(m.group("source")) > 8`, which `<the artefact>.` clears at 15 characters.
It now requires the source to name a year:

```python
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
…
check(bool(YEAR.search(src)),
      f"{pid}: {m.group('name')}'s source names a year — {src[:44]!r}")
```

All 28 sources across the four files already carried one, so the count did not
move: `190 checks, 190 pass, 0 fail`. `spec02` carries the flip — a fixture
source rewritten to `<the artefact>.` turns the probe red on
`source names a year` (`designer.md:46`). This is a **shape** check. It rejects
a placeholder and forces a citation to look like a citation. It does not prove
the artefact exists, and the probe's docstring now says so in the file.

**The wording the PRD's claim needs.** Yours to make on the transition; I have
not touched `prd.md`. The title "The four personas are built from research" is
a claim about how the files were produced, and it is true of this pass — three
research workers were dispatched, and their findings are on record in the wiki.
What is not true is that anything in the tree checks it. Two edits carry that:

- In `## What exists when this is done`, after the first bullet, add: "The
  check that backs this is a shape check — it reads the bullet's form and its
  internal consistency, never whether the artefact named exists. The research
  itself is recorded in `.pearde/wiki/sources/`, not enforced by any gate."
- In `## Non-goals`, add: "No in-tree proof that a practitioner or a source is
  real. Nothing in this repo can tell a researched trace from a fabricated one,
  and this PRD does not add it."

The thing that *would* close the gap is a committed
`resources/personas.py check` that resolves each `## Built from` row against a
knowledge note and each note against its `provenance:` key — a real PRD, with
`references/personas/`, `resources/` and `.pearde/wiki/` in one footprint. It
is outside this contract. Finding 3 already names the committed-checker half
of it.

### 3 — the two narrative demonstrations are gone

Taken. The in-place `designer.md` mutation and the `MARK.finditer` revert
proved nothing the standing checks in both blocks do not prove on every
collect, and the first of them mutated a tracked, sibling-adjacent file when a
fixture path already existed. Both are struck from this report. Every claim
below rests on a check that runs when `collect` runs the blocks.

## The re-aim of spec01's verify block

`pearde collect` warned `spec01:38: the verify block names no path under the
footprint — the whole-workspace smell`. The predicate is
`resources/board/specs.py:523`: no `footprint:` path appears literally in any
fenced block. The warning saw the spelling; three things were wrong.

**From:**

```sh
for f in designer mentor skeptic; do
  n=$(grep -c '^## Built from' "references/personas/$f.md")
  …
done
python3 resources/index.py check
echo "ok   index.py check silent"
out=$({ python3 …/probe/check_personas.py || true; })
printf '%s\n' "$out" | tail -1 | awk '{ if ($1 == $3 && $5 == 0) … }'
```

**To:**

1. A `FEET` variable holding the three paths spelled in full, so each appears
   literally in the block.
2. `index.py check` **captured and printed, never gated on** —
   `idx=$({ python3 resources/index.py check 2>&1 || true; })`, then a failure
   only on a line matching
   `references/personas/(designer|mentor|skeptic)\.md`.
3. A **sub-tally the block computes itself** over the probe's rows for its own
   three personas: `awk` counts `^(ok  |FAIL) (designer|mentor|skeptic):` and
   asserts `n > 0 && n == p`. No literal total anywhere; a check added
   elsewhere cannot move it.
4. A flip per footprint file, on the fixture — the block had none. Each file's
   first trace is found **at run time** (never a pinned practitioner name),
   rewritten to `[Nobody At All: …]`, and the probe must exit non-zero and
   print `FAIL <id>: 'Nobody At All' is under Built from`. Three files
   certified, three files executed.
5. A per-file source-year assertion, matching the probe's new bar.

`spec02` needed less: it already named its footprint literally and built a
fixture. It gained the `[ -n "$out" ]` guard, the year flip, and a run-time
lookup replacing a pinned `Rob Pike` — the flip now computes the **second**
trace on a bullet, which is the exact mutation a probe reading one trace per
bullet stays green on, and resolves to `engineer.md:19` today.

## Harnesses

| harness | baseline (11:50, before the first edit) | after |
|---|---|---|
| `probe/check_personas.py` | `190 checks, 190 pass, 0 fail` | `190 checks, 190 pass, 0 fail` |
| `spec01` block under `bash -e -o pipefail` | warned, whole-workspace | exit 0, hermetic |
| `spec02` block under `bash -e -o pipefail` | exit 0 | exit 0 |
| `the-board-runs-itself/brief-is-printed` | `verify: 104/104 checks pass` | `verify: 104/104 checks pass` |
| `the-board-runs-itself/the-next-line-runs` | `96 checks · 96 pass · 0 fail` | `96 checks · 96 pass · 0 fail` |
| `the-board-runs-itself/readme-in-three-rings` | `75 checks · 75 pass · 0 fail` | `75 checks · 74 pass · 1 fail` — **not this PRD's**, finding 1 |
| `python3 resources/index.py check` | silent, exit 0 | 2 problems, exit 1 — **not this PRD's**, finding 1 |
| `python3 resources/memos.py check` | silent, exit 0 | silent, exit 0 |
| `bash resources/doctor.sh` | `origin` broken, `knowledge` broken | `index` broken, `knowledge` broken; `origin` now ok — none is this PRD's |

Those three harnesses are the only ones on the board whose text names
`personas`; no `verify.sh` reads a footprint path of this PRD. `HEAD` moved
during the run, `d646168` → `3457e2d` (`collect-stages-a-shared-file-whole`, a
sibling). The three persona files are still ` M` — the sibling's commit did not
carry them, and this PRD's hunks are intact and uncommitted. Nothing was
staged; nothing was written outside
`.pearde/prds/the-four-personas-are-built-from-research/` and the three
persona files.

## Findings

### 1 — `readme-in-three-rings` and doctor's `index` row went red on a sibling's file, mid-run

`readme-in-three-rings/probe/verify.sh:110` runs
`eq "G index.py check is silent" … "0"` over the whole live checkout. Green at
baseline; at the re-run, `FAIL: G index.py check is silent — got '1', want
'0'`. Nothing changed in that PRD or in this one — a sibling added
`resources/board/all.py` (untracked, mtime 11:57) with no manifest row, and
`resources/board/serve.py` now references `@references/parts/all.md`, not on
disk. Doctor's `index` row flipped `ok → broken` for the same reason; its
`origin` row flipped `broken → ok` for another sibling's reason.

That exact line is already named as owed work in
`@.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`.
This is the second recorded instance of it firing on a neighbour. Outside this
footprint; left alone. Had `spec01` kept its bare `index.py check`, this PRD
would be red right now on another session's in-flight file.

### 2 — the section matcher is fence-blind, and nothing says so

`resources/board/specs.py`'s `## Verify and Proof` section reader stops at the
next line beginning `## `, including one inside a fenced block, including one
inside a heredoc inside a fenced block. `specced` then refuses with `holds no
fenced sh block`, which names the symptom and not the cause. The workflow's
`write-the-specs` atomic warns that the **acceptance-box** matcher is
line-based and fence-blind; the section matcher has the same property and no
warning. Worked around here with `@@ ` and `sed`. Proposed atomic text is under
`### Edits`.

### 3 — nothing committed enforces the persona grammar (carried forward)

The analyst's finding 2. `INDEX.md` states the grammar in prose; the only
enforcement is `probe/check_personas.py`, under `.pearde/prds/` and uncommitted
by design. The next persona written by hand or by `persona create` can break
every rule with every gate green. A committed `resources/personas.py check`
with an `@index.md` row, a `@references/files.md` row and a `doctor` row is the
fix; section 2 above says what else it should carry. Outside this footprint and
this contract. Still open.

### 4 — `INDEX.md` says one trace per bullet; three files carry two (carried forward)

The analyst's finding 4. `engineer.md` has two such bullets, `designer.md` one
(`Alan Cooper` + `Steve Krug`), `skeptic.md` one (`Hendrickson` + `Miller`).
`INDEX.md` reads "A `## How you work` bullet ends with `[<Name>: <trait>]`";
"one or more" closes it. `INDEX.md` is a sibling's file and was not touched.

### 5 — `knowledge` is broken and is not this PRD's (carried forward)

The analyst's finding 5. `graph.json` is behind notes written by other sessions
today, including this PRD's three. `knowledge.py relink` clears the backlog and
belongs to whoever owns that row. `origin` was broken at the analyst's pass and
at my baseline and is now `ok` — a sibling closed it, not this run.

### 6 — the knowledge layer held nothing on personas before this PRD (carried forward)

The analyst's finding 6. This PRD's three `remember` notes are the first
persona provenance on record, and they are the only provenance that exists —
see section 2. Nothing was learned outside the repo in this pass, so nothing
new was written back.

### 7 — `trace` is still not a word the grammar defines (carried forward)

`python3 resources/grammar.py show` has 176 terms and none is **trace** — the
`[<Name>: <trait>]` marker closing a `## How you work` bullet, tying a
behaviour to the practitioner it was taken from. Used throughout `INDEX.md`,
the probe, both specs and this report. `resources/grammar.py` is untracked and
under a sibling right now, so the row was not added.

### 8 — `spec01`'s "what already stands" cites a rewrite git cannot show

`spec01` says the behaviours are "as the 2026-09-02 rewrite left them". That
rewrite is itself uncommitted, so `git show HEAD:references/personas/<id>.md`
returns the 2026-08-25 intuition text and every bold lead, `## Voice` and
`description:` differs. The claim is unfalsifiable from git in this tree. What
**is** verifiable and was checked: `name:` and `profession:` are byte-identical
to `HEAD` in all three files, three frontmatter keys throughout, and no
behaviour bullet reads as bent to fit its citation — each trait is narrower
than the bullet it backs, which is the right direction.

### 9 — `spec02`'s green case still reads two files outside its footprint

`spec02`'s footprint is the probe alone; its `engineer green` row and its
closing tally read `references/personas/engineer.md` and `INDEX.md`. Boxes 1-3
name `engineer.md` by contract — the two-trace defect lived there — so
re-aiming them onto a synthetic corpus would redefine the spec rather than
repair it. The `[ -n "$out" ]` guard now catches the empty-read case, which was
the sharp edge. Whoever re-opens this unit can build a synthetic two-trace
fixture and drop the live-corpus read entirely.

## Health

No file in the footprint is under the health floor — the brief said "none under
the floor" and `doctor`'s `health` row reads `146 files · 5 under 40`, none of
them mine. Nothing was refactored.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ran. `prd.md`, both specs, the probe, the analyst's `report.md`, the memo and the three persona files read. `git status --short` and `HEAD` recorded before the first edit |
| 2 | `capture-the-harness-baseline` | ran. 56 harnesses on the board, 3 name `personas`, 0 name a footprint path; all three baselined green, plus `index.py check`, `memos.py check`, `doctor.sh` and the probe |
| 3 | `attempt-the-build` | **not entered.** `## Fails when` row 1 of this step: the specs exist and the build is in the tree, so this is the route's second pass. No flip is claimed for the personas themselves — the analyst's pass earned those |
| 4 | `re-run-the-harnesses` | ran twice, once per round. Every count equal or explained; the two that moved are a sibling's `resources/board/all.py` |
| 5 | `write-the-specs` | **partially entered**, by instruction: the specs were the analyst's. `spec01`'s block was re-aimed and made hermetic, `spec02` gained a guard, a year flip and a run-time lookup, and the probe's source assertion was tightened. No new spec written |

### Edits

Three shapes the route's atomics do not list.

**`write-the-specs` → `## Fails when`.** New row, for the refusal this run hit:

| seen | means | do |
|------|-------|----|
| `specced` refuses `<spec>:<n>: `## Verify and Proof` holds no fenced `sh` block` and the block is plainly there | a line inside the block begins `## ` — commonly a heredoc writing a markdown fixture. The section reader in `resources/board/specs.py` is line-based and fence-blind, the same way the acceptance-box matcher is | write the fixture's headings with a placeholder prefix and raise them at run time (`sed 's/^@@ /## /'`). Never a literal `## ` at line start inside a verify block, in a heredoc or out of one |

**`write-the-specs` → `#### Do` item 4.** The current sentence is "Give each
spec a `## Verify and Proof` block whose every command names a path from that
spec's own `footprint:`". `names` is the whole ambiguity: the block that warned
here **did** run only over footprint files, through a `$f` variable, and the
warning fired on the spelling — while a block that spells a footprint path once
and then gates on `index.py check` passes the warning and is exactly the
disease. Proposed replacement:

> 4. Give each spec a `## Verify and Proof` block in which every path is
>    spelled **literally**, not through a variable — the checker at
>    `resources/board/specs.py:523` matches the `footprint:` string, and a
>    `"references/personas/$f.md"` reads as no footprint path at all. Spelling
>    is not the point, though: **no command's exit may be decided by a file
>    outside the footprint.** A repo-wide command (`index.py check`, `doctor`, a
>    root `git status`) may be captured and printed, and the block may fail only
>    on the lines of its output that name a footprint path. A file the block
>    must read but does not own — a neighbour's fixture input, a sibling's
>    roster — is not copied, it is **stubbed**: the block writes a minimal valid
>    stand-in, so a rename or an empty read next door cannot decide the colour.
>    Guard every captured output with `[ -n "$out" ]` before greping it: a
>    producer that dies before printing looks exactly like a passing grep miss.

**`re-run-the-harnesses` → `## Fails when`.** New row:

| seen | means | do |
|------|-------|----|
| a count dropped and the failing line is a harness's own `index.py check`, `doctor.sh` or manifest assertion over the live checkout | the harness measures the workspace, not its PRD's footprint; a parallel worker's new file with no manifest row reddens it | quote the line and the file that explains it (`git status --short` names it untracked, its mtime post-dates your baseline), leave the harness alone, and cite `.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md` — the repair is owed to that harness's own PRD, not to you |

## Scores

complexity: 20
blast-radius: low
workflow: probe-then-spec
