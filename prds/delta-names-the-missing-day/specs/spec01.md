---
complexity: 15
footprint:
  - resources/scout/scout.sh
---

# spec01 — `delta` names the window it actually used, and refuses a stretched one

`cmd_delta` in `resources/scout/scout.sh` picks a base snapshot the same way
as before (nearest to the requested `N` days back, preferring not to go past
it), but now says which day it landed on and how far back that really is,
and refuses to print a table over a window stretched past tolerance instead
of silently mislabeling it.

Already built and proven against fixtures in
`.pearde/prds/delta-names-the-missing-day/probe/cmd_delta_probe.sh` (pass one
— the standalone function this spec's edit mirrors into the real script) and
directly against a scratch copy of `resources/scout/scout.sh` itself:

- A clean, unbroken daily history: `delta 7` prints `delta 7 · diffed
  against <exact-date> (7 days back, nearest to 7)` before the table.
- Three snapshots, newest 20 days old: `delta` (default 7) prints `gap: no
  snapshot within 2× of 7 days — run sweep first` and no table — the
  requested window is more than double the actual gap between "today" and
  the nearest usable base.
- A young tree (one week of daily snapshots): `delta 60` still diffs
  against the oldest snapshot (6 days back) and says so — the tolerance
  never narrows a legitimately short history into a refusal.
- `delta 0` (the path `cmd_sweep` calls automatically after every sweep) is
  unchanged: no window search, no gap check, straight diff against the
  previous snapshot — sweep's own "honest delta" after a machine's week off
  is this path, unaffected.

Two things changed in the window-search loop itself, both needed for the
tolerance check to be honest:

1. The cutoff and the "how many days back" arithmetic are anchored on the
   real calendar date (`date -u +%Y-%m-%d`), not on the newest snapshot's own
   date — a stale newest snapshot (machine off) must not hide behind its own
   staleness.
2. The window-search loop's candidates now exclude the newest snapshot
   itself (`sed '$d'` before the loop). Without this, a sparse history can
   let the loop pick `$newest` as its own base — printing an exact-looking
   "0 days back" with an empty table instead of naming the gap.

A new `epoch_of` helper does portable day-math (GNU `date -d`, falling back
to BSD `date -j -f`), both forced to UTC midnight — an unforced BSD parse
fills the missing time-of-day from *now*, which would skew every day-count
by however far into the day the caller runs.

## Acceptance

- [x] A directory of 90 unbroken daily snapshots ending today: `scout.sh delta 7` prints a line matching `^delta 7 · diffed against [0-9-]+ \(7 days back, nearest to 7\)$`, followed by the ranked table.
- [x] A directory holding only three daily snapshots, the newest dated 20 days before the real calendar date: `scout.sh delta` (no argument) prints exactly `gap: no snapshot within 2× of 7 days — run sweep first` and prints no `BUCKET` table header.
- [x] A directory of 7 unbroken daily snapshots ending today (a young tree): `scout.sh delta 60` prints a line naming the oldest snapshot's date and `(6 days back, nearest to 60)`, and still prints the ranked table — the tolerance never refuses a short-but-honest history.
- [x] `scout.sh delta 0` on any of the above directories prints no `delta ·` line and no `gap:` line — the window-naming and gap-tolerance logic runs only when a window is actually requested.
- [x] `NEW` still marks a repo absent from the base snapshot, unaffected by which base the window search chose — present in the 90-snapshot table's `GAIN` column whenever a repo/bucket pair in the newest snapshot has no row in the chosen base.
- [x] `bash -n resources/scout/scout.sh` exits 0 — the edit is syntactically valid.
- [x] `python3 resources/index.py check` and `bash resources/doctor.sh` name no new line on `resources/scout/scout.sh` beyond what stood before this PRD's edit.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
SCOUT=resources/scout/scout.sh
bash -n "$SCOUT" || { echo "syntax error"; exit 1; }

work=$(mktemp -d)
mkdir -p "$work/resources"
cp -R resources/scout "$work/resources/scout"
snaps="$work/resources/scout/snapshots"
rm -f "$snaps"/*.tsv
today=$(date -u +%Y-%m-%d)

row() { printf 'agents\tfoo/bar\t%s\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\tsome repo\n' "$1"; }

# clean 90-day history ending today
python3 - "$snaps" "$today" <<'PY'
import sys, datetime
snaps, today = sys.argv[1], sys.argv[2]
today = datetime.date.fromisoformat(today)
for i in range(90):
    d = today - datetime.timedelta(days=89 - i)
    with open(f"{snaps}/{d.isoformat()}.tsv", "w") as f:
        f.write(f"agents\tfoo/bar\t{1000+i*10}\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\tsome repo\n")
PY
out=$(bash "$work/resources/scout/scout.sh" delta 7)
echo "$out" | grep -qE '^delta 7 · diffed against [0-9-]+ \(7 days back, nearest to 7\)$' || { echo "FAIL clean90 line"; exit 1; }
echo "$out" | grep -q '^BUCKET' || { echo "FAIL clean90 table"; exit 1; }

# three snapshots, newest 20 days old
rm -f "$snaps"/*.tsv
python3 - "$snaps" "$today" <<'PY'
import sys, datetime
snaps, today = sys.argv[1], sys.argv[2]
today = datetime.date.fromisoformat(today)
for age in (22, 21, 20):
    d = today - datetime.timedelta(days=age)
    with open(f"{snaps}/{d.isoformat()}.tsv", "w") as f:
        f.write("agents\tfoo/bar\t1000\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\tsome repo\n")
PY
out=$(bash "$work/resources/scout/scout.sh" delta)
[ "$out" = "gap: no snapshot within 2× of 7 days — run sweep first" ] || { echo "FAIL gap line: $out"; exit 1; }

# young tree: one week of history, delta 60
rm -f "$snaps"/*.tsv
python3 - "$snaps" "$today" <<'PY'
import sys, datetime
snaps, today = sys.argv[1], sys.argv[2]
today = datetime.date.fromisoformat(today)
for i in range(7):
    d = today - datetime.timedelta(days=6 - i)
    with open(f"{snaps}/{d.isoformat()}.tsv", "w") as f:
        f.write(f"agents\tfoo/bar\t{1000+i*20}\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\tsome repo\n")
PY
out=$(bash "$work/resources/scout/scout.sh" delta 60)
echo "$out" | grep -qE '\(6 days back, nearest to 60\)$' || { echo "FAIL young tree: $out"; exit 1; }
echo "$out" | grep -q '^BUCKET' || { echo "FAIL young tree table"; exit 1; }

# delta 0 unaffected
out=$(bash "$work/resources/scout/scout.sh" delta 0)
if printf '%s\n' "$out" | grep -qE '^delta [0-9]+ · diffed against|^gap:'; then echo "FAIL delta 0 leaked window logic"; exit 1; fi
echo "$out" | grep -q '^BUCKET' || { echo "FAIL delta 0 table"; exit 1; }

rm -rf "$work"
echo "spec01: all checks passed"
```
