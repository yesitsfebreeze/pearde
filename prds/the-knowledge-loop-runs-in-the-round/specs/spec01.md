---
goal: The round's own loop reaches for the record before it drills a fork to the user
complexity: 6
footprint: references/parts/loop.md
---

# spec01 — the loop gains its knowledge step

## What already stands

Applied directly in pass one (probe), in the tree, uncommitted:
- `references/parts/loop.md` header now reads "Eight steps, in order."
- A new row `7 knowledge` sits in the step table, before `8 drill, then
  stop` (renumbered from `7`) — no other row moved or renumbered.
- A new prose paragraph **7 · Knowledge.** sits before **8 · Drill, then
  stop.**, describing: query `python3 resources/knowledge.py query` for a
  fork about to be drilled; a strong hit answers it under `## Answers`
  directly (step 2's own mechanism) and the fork is not put to the user; a
  gap or thin hit changes nothing — `query` already auto-enqueued the gap
  into `.pearde/wiki/pending/`, per `knowledge.py`'s own `auto_enqueue`
  default — and the fork still reaches step 8 as before.

## What is left to finish

Nothing — closed by the probe edit itself; verified below.

## Acceptance

- [x] `references/parts/loop.md` reads "Eight steps, in order."
- [x] the step table has a `7 knowledge` row before `8 drill, then stop`
- [x] no existing step (1 scan … 6 collect) changed its number or its
      command column
- [x] a **7 · Knowledge.** paragraph precedes **8 · Drill, then stop.**

## Verify and Proof

```sh
set -e
grep -q "Eight steps" references/parts/loop.md
grep -q "^| 7 knowledge " references/parts/loop.md
grep -q "^| 8 drill, then stop " references/parts/loop.md
grep -q "^\*\*7 · Knowledge\.\*\*" references/parts/loop.md
grep -q "^\*\*8 · Drill, then stop\.\*\*" references/parts/loop.md
echo "spec01: loop.md carries eight steps, 7 knowledge before 8 drill — ok"
```
Run 2026-08-31 (analyst pass): all five greps hit, echo printed. Re-run
2026-08-31, implementer, against the files now on disk (the probe's edits are
committed — another PRD's collect carried them, so the file is clean in
`git status`): all five greps hit again, echo printed, exit 0. Box 3 held
against the pre-change blob (`96231df`, the image `eef2dba`'s own diff was
cut from): rows 1–3, 5, 6 identical; row 4's command column changed in the
same commit by the other PRD's `--worker` spec, not by the knowledge step —
see report.md.
