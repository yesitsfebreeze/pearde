---
memo: the-board-keeps-two-journals
kind: decision
status: decided
subject: .history.jsonl and .transitions.jsonl are two different records, not one duplicated
date: 2026-08-31
prds:
  - the-sweep-leaves-nothing-unregistered
---

# the-board-keeps-two-journals — why `.history.jsonl` and `.transitions.jsonl` both exist

## Decision

The board keeps two journals under `.pearde/.state/`, and both stay.
`.history.jsonl` is one row **a day** — `{d, states, hdone, hleft, done,
left}`, a daily aggregate snapshot of board counts, written once by
`plan.write_history()` (called by `serve.py`'s daemon), deduped same-day,
capped at 400 rows, and read by `plan.read_history()` to draw the burn-down.
`.transitions.jsonl` is one row **a transition** — `{t, prd, from, to}` plus
guard telemetry (`calls, reads, refused, tokens`), written by
`transitions.record()` on every `transitions.py` command and by `collect.py`
on `done`/`failed`, and read for cost-per-transition analytics. Neither
writer ever appends to the other's file; `transitions.py`'s own docstring
says so explicitly ("never `.history.jsonl`"), and `references/parts/guard.md`
and `references/parts/view.md` already document the split correctly.

## Why

A fourteen-agent sweep produced a finding that the two files "looked like
the same record." They are not: different shape, different writer, different
reader, different question answered — one is a calendar-day gauge for the
burn-down, the other is a per-event ledger for guard cost analytics. The
confusion traced to naming, not to a real duplication: `collect.py` had
aliased its own transitions-writing helper as `HISTORY_FILE` /
`history_row()` — names that said "history" while the code wrote
`.transitions.jsonl` — and `specs.py`'s module docstring stated that
`transitions.py` "records the row in `.history.jsonl`," which is backwards.
Both were fixed already: `collect.py` now names them `TRANSITION_FILE` /
`transition_row()`, and `specs.py`'s docstring names the right file.
Verified against the current tree (2026-08-31): the rename holds, the
docstring is correct, and `.pearde/.state/` is ignored as a whole directory
in `init.py`'s `IGNORED` tuple, so a fresh board's `.gitignore` already
covers both files without naming either one — the missing
`prds/.transitions.jsonl` gitignore line the sweep also flagged no longer
applies under the current `.pearde/.state/` layout. No code defect remains;
this memo is the record that the split itself was never the bug.

## Alternatives considered

**Merge into one file, one row per event, with a daily-aggregate view
computed on read.** Would remove the naming confusion at the source, but
trades a cheap append-and-cap write (`.history.jsonl`, 400-row ceiling) for a
read-time scan of a file that grows without bound as long as the board runs
— the burn-down chart would recompute the same daily aggregate on every
render instead of reading one pre-summarized row.

**Keep the misleading `HISTORY_FILE`/`history_row()` names in `collect.py`
and document the alias instead of renaming.** Cheaper in the moment, but
leaves the exact string that produced this finding in place for the next
reader to trip on again.

## Consequences

- Two files stay on disk under `.pearde/.state/`; `doctor` and `view` read
  both by their real names now — no further change needed there.
- The next agent reading `collect.py`, `specs.py`, or `init.py`'s journal
  handling can trust the names as written; the drift that caused this
  finding is closed, not just relocated.
- Not addressed here: any future change to either journal's *format* — this
  memo covers why the split exists, not the shape of either row.
