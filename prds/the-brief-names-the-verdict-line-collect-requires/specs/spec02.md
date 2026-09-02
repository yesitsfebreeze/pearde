---
complexity: 10
footprint:
  - resources/board/brief.py
  - resources/doctor.sh
---

# spec02 — a `briefs` check that fails on the defect it just found

The PRD leaves this to the analyst and gives the reason: `doctor`'s `briefs`
row read `ok — 5 blocks · every placeholder named` the whole time both defects
shipped, so the existing checker cannot see either. Counting markers and
placeholders is a check about the brief's *frame*; nothing read its *content*.

Two rules go into `brief.check()` in `resources/board/brief.py`, and the
`doctor` row's summary stops overstating what it proved.

**Rule one — the brief names the line.** `brief:every` must contain the marker
`Verdict:` and the number `40`. This is the exact defect spec01 repairs: had it
existed, the missing sentence would have been a `broken` row rather than an
orchestrator's habit of adding the word by hand.

**Rule two — no rewrap leftover.** Two adjacent lines in one block whose
trailing 30 characters coincide is the shape a rewrap leaves when the old
continuation is not deleted — `workers.md:155-156` exactly. Thirty is chosen so
that ordinary repeated cadence in a block does not trip it; the whole current
file passes at that length, and the restored defect fails.

The value is in the second half of each rule: **both must actually fail on
their defect.** The probe builds each defect into a temp copy of `workers.md`
and asserts `check()` returns at least one problem for it, so neither box is a
check that cannot fail.

**This already stands in the tree, uncommitted** — both rules and the row
wording are in place, `--check` is silent on the real file and `doctor` reads
`ok`. What is left is confirmation against the boxes.

## Acceptance

- [x] `python3 resources/board/brief.py --check` prints nothing and exits 0 on the repository as it stands.
- [x] With the `Verdict:` marker removed from `brief:every` in a temp copy, `check()` returns at least one problem naming that block.
- [x] With the duplicated continuation restored in a temp copy, `check()` returns at least one problem naming `brief:analyst` and quoting the repeated tail.
- [x] Neither new rule fires on any of the five blocks as they stand — no false positive, so the row can stay `ok`.
- [x] `doctor`'s `briefs` row renders `ok` and its summary names the verdict line, not only the placeholders.
- [x] `bash resources/doctor.sh` exits 0 and every other row reads exactly as it did before this PRD.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
# G3 of the probe builds both defects and asserts each is caught
bash .pearde/prds/the-brief-names-the-verdict-line-collect-requires/probe/verify.sh
# the checker on the real file: silent, exit 0
python3 resources/board/brief.py --check; echo "check exit=$?"
# the row, and the gate
bash resources/doctor.sh | grep briefs
bash resources/doctor.sh >/dev/null; echo "doctor exit=$?"
python3 resources/index.py check >/dev/null; echo "index exit=$?"
```
