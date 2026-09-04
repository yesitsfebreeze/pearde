---
complexity: 6
footprint:
  - references/parts/handles.md
  - references/files.md
  - index.md
  - resources/doctor.sh
---

# spec02 — the verb named in the map, the handles table and a doctor row

`purge` is dispatch-discoverable with no edit to `pearde.py` — `pearde help`
and `pearde purge` already work off `COMMANDS = {"purge": cmd_purge}`
(spec01) alone. What is left is what discovery does not cover: the verb
named where a person reads the board's command set, and one doctor row
that runs the scan read-only on every check, so the refuse rule failing
silently would show up as `broken` rather than being found by hand.

What already stands, built and checked in this lane:

- `references/parts/handles.md` — one row, `reclaim the lifecycle leaks`,
  next to `sweep the stale claims` in the same table.
- `references/files.md` — one row for `@resources/board/purge.py`, next to
  `@resources/board/orphans.py`.
- `index.md` — `@@handles`'s file list gains `@resources/board/purge.py`;
  a new `@@purge` keyword row after `@@guard`, scoped to the files this PRD
  actually touches (`purge.py`, `session.py`, `lanes.py`, `handles.md`) —
  see `## Findings` in the report for the one path this row does **not**
  name and why.
- `resources/doctor.sh` — one block after the `plan` row and before
  `harnesses`: runs `purge.py purge $BOARD` with no `--apply`, reports
  `broken` on a nonzero exit, else `ok <n> candidates · every claim and
  registered board held`. Read-only — the row costs one scan, never a
  write.

## Acceptance

- [x] `references/parts/handles.md` names `purge` in the same table as
  every other verb, with its flags and what each does
  - proof: `grep -n 'reclaim the lifecycle leaks' references/parts/handles.md` on the lane, one match
- [x] `references/files.md` carries a row for `purge.py` and `index.py
  check` raises no new problem against the baseline this pass took before
  its first edit
  - proof: `python3 resources/index.py check` on the lane prints the same
    3 lines before and after this spec's edits (`resources/common.py …`,
    `references/files.md lists @…/hotreload-test.js …`, `@@view names
    @…/hotreload-test.js …`) — none of the three names anything this PRD
    touched, and none is new
- [x] `index.md`'s `@@handles` row lists `purge.py`, and a `@@purge` row
  exists naming the verb's own files
  - proof: `grep -n '@@purge\|purge.py' index.md` on the lane
- [x] `bash resources/doctor.sh <board>` prints a `purge` row, `ok` on the
  live board with the candidate count `purge.py`'s own scan reports, and
  the row is read-only — a second run's candidate count only moves if the
  board itself moved
  - proof: run against `/Users/feb/dev/infra/pearde/.pearde` from the lane:
    `purge       ok      7 candidates · every claim and registered board held`;
    `git status --short` in the real board directory shows no new writes
    from this run

## Verify and Proof

```sh
LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
grep -qF 'reclaim the lifecycle leaks' "$LANE/references/parts/handles.md"
grep -qF '@resources/board/purge.py' "$LANE/references/files.md"
grep -qF '@@purge' "$LANE/index.md"
bash -n "$LANE/resources/doctor.sh"
python3 "$LANE/resources/index.py" check 2>&1 | wc -l   # 3, unchanged from baseline
bash "$LANE/resources/doctor.sh" /Users/feb/dev/infra/pearde/.pearde 2>&1 | grep '^  purge'
```
