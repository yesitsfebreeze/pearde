---
complexity: 6
footprint:
  - references/parts/workers.md
---

# spec01 — the brief names the `Verdict:` line, and the rewrap's leftover goes

Two edits to one file, both inside `references/parts/workers.md`.

**The gap.** `collect.route_report` refuses any report whose first 40 lines
carry no `Verdict:` line, and the brief handed to every worker never said so.
The sentence goes into `<!-- brief:every -->`, not into the analyst block:
`brief.py:340` appends `blocks["every"]` to the analyst's brief *and* the
implementer's, while the consultant (`:361`) never receives it — and the
consultant is the one role that writes no report. One edit, exactly the two
roles that need it.

**The wording has to name the safe shape, not just the word.** The probe
measured `verdict_of` across fifteen line shapes. It tolerates emphasis before
the colon (`**Verdict**: X`, `**Verdict: X**`) but *silently* refuses
`**Verdict:** X`, `*Verdict:* X`, `- Verdict: X` and `> Verdict: X` — the
bold-and-bullet shapes a worker writing markdown reaches for first. Since the
PRD forbids loosening the tool, the brief must steer to the shape that works:
the marker, then the one word, nothing else on the line, not in a list item
and not in a block quote.

**The folded-in repair.** Line 156 was a continuation `7809756` left behind
when it rewrapped the line above; it shipped as instructions in every analyst
brief. Deleting that one line is the whole repair.

**This already stands in the tree, uncommitted** — both edits are made and the
probe is green. What is left is to confirm it against the boxes below and
leave the file as the one source.

## Acceptance

- [ ] The `brief:every` block names the marker `Verdict:`, the 40-line window, and says a report carrying none is refused.
- [ ] The block names the shape that works: one word after the marker, nothing else on the line, and neither a list item nor a block quote.
- [ ] The rendered analyst brief carries exactly one `Verdict:` line, and so does the rendered implementer brief.
- [ ] The rendered consultant brief carries none — it writes no report, and `brief.py:361` must stay the one role that skips the `every` block.
- [ ] The half-sentence `as you would one the PRD already carries` appears exactly once in `workers.md`, and the analyst brief renders with no repeated continuation.
- [ ] `verdict_of` and its 40-line window are unchanged: the span from `VERDICT_RE` to `def scores_of` in `resources/board/collect.py` is byte-identical to `HEAD`. Scope the check to that span, not to the whole file — a sibling PRD is adding an `--also` guard to `collect.py`, so a whole-file diff measures that session's work, not this one's restraint.
- [ ] `references/templates/report.md` shows no diff against `HEAD` — the PRD names it explicitly as not the gap.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
# G1, G2 and G5 of the probe cover every box above
bash .pearde/prds/the-brief-names-the-verdict-line-collect-requires/probe/verify.sh
# the two things the PRD forbids touching. collect.py is scoped to the verdict
# mechanism: another session is adding an --also guard to the same file.
diff <(git show HEAD:resources/board/collect.py | sed -n '/^VERDICT_RE/,/^def scores_of/p') \
     <(sed -n '/^VERDICT_RE/,/^def scores_of/p' resources/board/collect.py) \
  && echo "verdict_of unchanged"
git diff --stat HEAD -- references/templates/report.md   # empty
# the one source, and the consultant that must not carry the line
grep -c 'as you would one the PRD already carries' references/parts/workers.md   # 1
python3 resources/board/brief.py --consult skeptic --question x --board .pearde \
  2>/dev/null | grep -c 'Verdict:'                                               # 0
```
