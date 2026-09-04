---
complexity: 12
footprint:
  - resources/scout
  - references/files.md
  - references/knowledge.md
  - references/plugins.md
  - references/skills/pearde-scout.md
  - index.md
---

# spec01 — resources/scout holds only tool files

The author's research leaves the shipped tree: `findings.md`, `reading-list.md`,
the two dated `snapshots/*.tsv` and all five `templates/` configs — 1,847 lines
measured at HEAD. `scout.sh`, `toolscout.sh`, `route.sh`, `routes.md`,
`buckets.txt` and `snapshots/` stay, `snapshots/` shipping a README and nothing
else. Every document that named a departing file names its new home instead, so
no prose in the tree points at a path that is gone.

**Already standing in the lane.** The nine files are staged as deletions,
`snapshots/README.md` is added, and `index.md`, `references/files.md`,
`references/knowledge.md` and `references/plugins.md` carry their rewritten
rows. `resources/scout/README.md` is rewritten to two layers — discover and ask
— with the layout table, the sweep paragraph and the research loop no longer
naming a departing file; the loop's index two is now `knowledge.py`.
`resources/scout/routes.md` and `resources/scout/buckets.txt` no longer cite
`findings.md`, and `references/skills/pearde-scout.md` no longer advertises the
reading list or the quality gates.

**Left to finish.** Nothing but the checks below, run against the lane as it
stands. The move's destination is spec02; this unit only takes the files out.

## Acceptance

- [x] `resources/scout` holds exactly `README.md`, `buckets.txt`, `route.sh`, `routes.md`, `scout.sh`, `toolscout.sh` and `snapshots/README.md` — no other tracked file
- [x] No file under `resources/`, `references/` or `index.md` contains the strings `findings.md`, `reading-list` or `scout/templates`
- [x] `references/files.md` carries no row for a departing file, and its `snapshots/` directory row survives
- [x] `references/skills/pearde-scout.md` names neither `/scout reading` nor `/scout quality` nor `wire the quality gates`
- [x] `python3 resources/index.py check` prints the same four lines it printed at HEAD and no line naming `resources/scout`
- [x] `python3 resources/prose.py check` is silent on `resources/scout/README.md` and `resources/scout/routes.md`
- [x] `bash resources/doctor.sh` reports `skills ok` with 19 well-formed

## Verify and Proof

```sh
set -e
test "$(git ls-files resources/scout | tr '\n' ' ')" = "resources/scout/README.md resources/scout/buckets.txt resources/scout/route.sh resources/scout/routes.md resources/scout/scout.sh resources/scout/snapshots/README.md resources/scout/toolscout.sh "
if grep -rn -e 'findings\.md' -e 'reading-list' -e 'scout/templates' resources references index.md; then exit 1; fi
if grep -n -e '/scout reading' -e '/scout quality' -e 'wire the quality gates' references/skills/pearde-scout.md; then exit 1; fi
grep -q '@resources/scout/snapshots/' references/files.md
if grep -nE '@resources/scout/(findings|reading-list)\.md|@resources/scout/templates' references/files.md; then exit 1; fi
python3 resources/prose.py check resources/scout/README.md resources/scout/routes.md
idx=$(python3 resources/index.py check 2>&1) && irc=0 || irc=$?
[ "$irc" -lt 2 ]
printf 'index.py check — %s line(s):\n%s\n' "$(printf '%s\n' "$idx" | grep -c . || true)" "$idx"
if printf '%s\n' "$idx" | grep -q 'resources/scout'; then exit 1; fi
doc=$(bash resources/doctor.sh 2>&1) && drc=0 || drc=$?
[ -n "$doc" ]
printf '%s\n' "$doc" | grep -E '^  skills ' 
printf '%s\n' "$doc" | grep -qE '^  skills +ok +19 well-formed'
echo spec01 green
```

`index.py check` and `doctor.sh` read the whole checkout, so their exit is
captured and printed rather than gated on: both carry inherited problems no
path in this footprint owns. What decides this block is the footprint —
no line of either naming `resources/scout`, and the `skills` row reading 19
well-formed. The four inherited `index.py check` lines are quoted in the
report against the same four at HEAD.
