---
complexity: 2
footprint:
  - .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
---

# spec02 — the spent non-goal becomes a guard on the fix that landed

`the-fixtures-meet-the-tool` line 174 asserted `grep -c parse-cache
.pearde/.gitignore` is **0**. That was never a claim about correct behaviour: it
froze the *absence* of a fix, recorded at the time as "a finding, not a fix" and
pinned so the PRD could prove it had stayed inside its contract. The ignore line
has since been added, so the non-goal is spent and the check is asserting the
world is still broken.

Re-aim, do not delete: the fix it was pinned against is worth a guard of its own
— `.state/parse-cache.json` is rebuilt by `pearde scan` and must stay out of the
board's history — so the check now asserts the line is present, anchored, exactly
once.

**Already standing (this analyst's uncommitted pass one):** the check reads
`grep -c '^\.state/parse-cache\.json$'` against `.pearde/.gitignore` and wants
`1`, retitled "`.state/parse-cache.json` is git-ignored on the board", with a
comment saying what the old check pinned and why that is over. The harness's
pinned denominator of 35 is unchanged because the check was re-aimed in place
rather than added beside. Its neighbour, "init.py does not seed it either", was
green before and after and is untouched.

**Left to finish:** re-run the harness, and account for its one remaining
failure, which is not this PRD's — see the box below.

## Acceptance

- [x] The parse-cache row reads ok, and the re-aim was made in place rather than added beside — the row stands exactly once in the harness and the spent `grep -c parse-cache` non-goal is gone (the harness's own total, 35 at this run, is a board-wide census three live sessions move, so it is printed, never gated)
- [x] The check fails when the ignore line is removed — shown against a scratch copy of `.pearde/.gitignore`, never against the real file
- [x] The harness's row "F no file under resources/ carries any of this" is accounted for: it reads the whole working tree's `git diff` of `resources/board/plan.py` and `resources/board/init.py`, so it goes red on any concurrent session's uncommitted edit to either. Show `git diff -- resources/board/init.py resources/board/plan.py` and state whether the hunks are this PRD's. If they are not, the row is contention and this spec's boxes still close; if the tree is clean of other sessions' work, the harness exits 0

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
H=.pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
rc=0; bash "$H" > "$W/out" 2>&1 || rc=$?
# Printed, never gated: this harness's own tally and its FAIL rows. Its C rows
# census every harness on the board, its E rows re-run two neighbouring
# harnesses, and its F row reads the whole working tree's `git diff` of two
# files a live session holds — all three are board-wide and go red on work that
# is not this PRD's. What this block asserts is only this PRD's own row.
{ grep -E 'FAIL|^[0-9]+ checks' "$W/out" || true; }
echo "exit=$rc"
row="$( { grep -c 'ok   F .state/parse-cache.json is git-ignored on the board' "$W/out" || true; } )"
red="$( { grep -c 'FAIL.*parse-cache' "$W/out" || true; } )"
# the re-aim was made in place, not added beside — one row, in this PRD's own file
inplace="$( { grep -c 'F .state/parse-cache.json is git-ignored on the board' "$H" || true; } )"
spent="$( { grep -c 'grep -c parse-cache' "$H" || true; } )"
# the F row's inputs, for the record — hunks in either file are another session's
git diff --name-only -- resources/board/plan.py resources/board/init.py
# non-vacuity, on scratch text only — .pearde/.gitignore is never written
live="$( { grep -c '^\.state/parse-cache\.json$' .pearde/.gitignore || true; } )"
gone="$(grep -v '^\.state/parse-cache\.json$' .pearde/.gitignore \
  | { grep -c '^\.state/parse-cache\.json$' || true; } )"
echo "row-ok=$row row-red=$red in-place=$inplace spent-non-goal=$spent ignore-live=$live ignore-without-the-line=$gone"
[ "$row" = 1 ] && [ "$red" = 0 ] && [ "$inplace" = 1 ] && [ "$spent" = 0 ] \
  && [ "$live" = 1 ] && [ "$gone" = 0 ]
```
