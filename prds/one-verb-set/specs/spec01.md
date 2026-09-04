---
complexity: 12
footprint:
  - resources/scout/scout.sh
  - resources/scout/toolscout.sh
  - resources/scout/check.sh
  - resources/scout/README.md
  - references/files.md
---

# spec01 — one door onto scout's four layers

`scout.sh` gains four verbs — `tool`, `find`, `reading`, `quality` — beside
the existing `sweep`, `delta`, `trending`, so `scout.sh <verb>` is the one
entry point the PRD asks for instead of four files with four `--help` texts.
`toolscout.sh` becomes a one-line compat entry that execs `scout.sh tool
"$@"`; `route.sh` is unchanged and is what `find` reads through. A `registry`
function inside `scout.sh` is the single source both the no-argument verb
table and README.md's Commands table print from, and `check.sh` is the
doctor-style guard the PRD's `Fails when` box asks for: it runs `scout.sh`
with no argument, reads README.md's Commands table the same way, and fails
loudly the moment the two disagree.

What already stands, built and run against this repo's own snapshots and
routes: every verb dispatches, `toolscout.sh` and `scout.sh tool` produce
identical output for the same arguments (including the same exit code with
no query), `scout.sh find list | wc -l` still reports the 45 routes
`route.sh list` always has, and every verb's last line names the file its
record lives in or says plainly that none is kept. One real defect surfaced
while proving the last point: `delta`'s pipeline piped into `head -40` dies
of `SIGPIPE` on any diff over 40 rows, and `pipefail` turned that ordinary
truncation into a `set -e` exit that skipped the line after it — fixed by
turning `pipefail` off around that one pipeline, verified on this repo's own
`2026-08-25 -> 2026-08-28` snapshots, which hold more than 40 changed rows.
What is left is only running the block below on the merged tree.

## Acceptance

- [x] `scout.sh` with no argument prints one row per verb (`sweep`, `delta
  [days]`, `trending`, `tool <query>`, `find`, `reading`, `quality`), and
  exits 0.
- [x] `resources/scout/check.sh` exits 0 — the no-argument table and
  README.md's Commands table agree, row for row.
- [x] `toolscout.sh` and `scout.sh tool` produce byte-identical stdout,
  stderr and exit code for the same arguments.
- [x] `scout.sh delta` on a window wide enough to produce more than 40
  changed rows still exits 0 and its last line names the snapshots it
  diffed.
- [x] `scout.sh reading`'s last line names `reading-list.md`; `scout.sh
  quality`'s last line names `templates/`.

## Verify and Proof

```sh
set -e -o pipefail
cd "$(git rev-parse --show-toplevel)"

out=$(bash resources/scout/scout.sh 2>&1) && rc=0 || rc=$?
[ "$rc" = 0 ] || { echo "no-arg exit $rc"; exit 1; }
for v in sweep 'delta \[days\]' trending 'tool <query>' find reading quality; do
  echo "$out" | grep -qE "^${v}[[:space:]]" || { echo "no-arg table missing verb: $v"; exit 1; }
done

bash resources/scout/check.sh || { echo "check.sh: scout.sh and README.md's Commands table disagree"; exit 1; }

ta_out=$(bash resources/scout/toolscout.sh 2>&1) && ta=0 || ta=$?
tb_out=$(bash resources/scout/scout.sh tool 2>&1) && tb=0 || tb=$?
[ "$ta" = "$tb" ] && [ "$ta_out" = "$tb_out" ] || { echo "toolscout.sh and scout.sh tool disagree with no args"; exit 1; }

# `delta`'s SIGPIPE/pipefail fix needs a diff over 40 rows to exercise —
# stubbed rather than read off this repo's own snapshots/, which this spec
# does not own and which the daily sweep keeps changing underneath it.
snap_bak=$(mktemp -d)
cp -R resources/scout/snapshots/. "$snap_bak"/ 2>/dev/null || true
restore_snaps() { rm -rf resources/scout/snapshots; mkdir -p resources/scout/snapshots; cp -R "$snap_bak"/. resources/scout/snapshots/ 2>/dev/null || true; rm -rf "$snap_bak"; }
trap restore_snaps EXIT
rm -f resources/scout/snapshots/*.tsv
for i in $(seq 1 50); do printf 'b%d\trepo/x%d\t100\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\td\n' "$i" "$i"; done > resources/scout/snapshots/2020-01-01.tsv
for i in $(seq 1 50); do printf 'b%d\trepo/x%d\t200\t2026-01-01T00:00:00Z\tfalse\tMIT\tRust\td\n' "$i" "$i"; done > resources/scout/snapshots/2020-01-02.tsv
d_out=$(bash resources/scout/scout.sh delta 9999 2>&1) && drc=0 || drc=$?
[ "$drc" = 0 ] || { echo "delta 9999 exit $drc"; exit 1; }
echo "$d_out" | tail -1 | grep -q '^record:' || { echo "delta's last line does not name a record"; exit 1; }
restore_snaps
trap - EXIT

r_out=$(bash resources/scout/scout.sh reading 2>&1)
echo "$r_out" | tail -1 | grep -q 'reading-list.md$' || { echo "reading's last line does not name reading-list.md"; exit 1; }

q_out=$(bash resources/scout/scout.sh quality 2>&1)
echo "$q_out" | tail -1 | grep -q 'templates' || { echo "quality's last line does not name templates/"; exit 1; }

echo ok
```
