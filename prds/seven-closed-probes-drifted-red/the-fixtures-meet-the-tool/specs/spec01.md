---
complexity: 6
footprint:
  - .pearde/prds/an-unknown-flag-refuses/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh
---

# spec01 — the "wrote nothing" harnesses stop counting the machine-local parse cache

`scan` persists `<board>/.state/parse-cache.json` on a parse miss, and every
command that reads the board scans. A fixture board is a hand-rolled `git init`
repo whose `.gitignore` names nothing, so from the moment the cache landed
every "the refused command wrote nothing" check in these harnesses saw an
untracked file the tool was entitled to write. The product kept its word — the
real board's parent `.gitignore` carries `.pearde/.state/` — so the fix belongs
in the fixtures: `clean()` filters `.pearde/.state/`, and the one harness that
checksums the whole board excludes `./.state/*` from the sum.

## What the probe already established

Reproduced on a fresh `plan.py example` board committed clean: one
`pearde scan --board` leaves `?? .pearde/.state/` in `git status --porcelain`
and nothing else. The filter is narrow — a file touched under
`.pearde/prds/` still shows through it — and the harnesses keep their separate
`rows()` assertions on `transitions.jsonl`, so filtering the directory does not
blind them to a transition row a refusal should never have written.

Three edits stand in the tree, all from pass one:
`an-unknown-flag-refuses` line 32 and `one-predicate-for-dispatchable` lines 91
and 112 pipe `git status` through `grep -v`; `specced-is-a-command`'s
`tree_sum()` adds `-not -path './.state/*'`. The first two closed a red (3 and 2
failures); the third is the same family, taken as hardening — that harness was
green before and after, and its checksum would have gone false-red the first
time a scan landed between two `tree_sum` calls.

The root defect is left standing on purpose, and this contract forbids the fix:
`.state/parse-cache.json` is named in neither `.pearde/.gitignore` nor
`init.py`'s `BOARD_IGNORED`, while `.state/plan.json` — which the cache PRD said
it was "exactly like" — is in both. Every board this machine writes will show
the cache as untracked. See the report's findings.

## Acceptance

- [x] `bash .pearde/prds/an-unknown-flag-refuses/probe/verify.sh` exits 0 — 196 checks, no failure; before the filter it reported 3
- [x] `bash .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh` exits 0 — 53 checks, no failure; before the filter it reported 2
- [x] `bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh` exits 0 and `grep -c "not -path './.state/\*'" .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh` reports 1
- [x] section A of this PRD's own harness passes: a scan on a clean fixture board leaves exactly `.pearde/.state/`, the filtered status is empty, the unfiltered one is not, and a file under `.pearde/prds/` still shows through the filter
- [x] this spec's footprint holds three paths, all under `.pearde/prds/`, and `grep -rc 'parse-cache' resources/board/init.py .pearde/.gitignore` reports 0 for both — the product side is deliberately unchanged

## Verify and Proof

```sh
bash .pearde/prds/an-unknown-flag-refuses/probe/verify.sh | tail -1
bash .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh | tail -1
bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh | tail -1
grep -c 'parse-cache' resources/board/init.py .pearde/.gitignore
bash .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
```
