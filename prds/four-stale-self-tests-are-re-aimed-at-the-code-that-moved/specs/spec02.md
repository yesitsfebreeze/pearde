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

- [ ] The parse-cache row reads ok, and the harness's own total still reads 35 checks
- [ ] The check fails when the ignore line is removed — shown against a scratch copy of `.pearde/.gitignore`, never against the real file
- [ ] The harness's row "F no file under resources/ carries any of this" is accounted for: it reads the whole working tree's `git diff` of `resources/board/plan.py` and `resources/board/init.py`, so it goes red on any concurrent session's uncommitted edit to either. Show `git diff -- resources/board/init.py resources/board/plan.py` and state whether the hunks are this PRD's. If they are not, the row is contention and this spec's boxes still close; if the tree is clean of other sessions' work, the harness exits 0

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh; echo "exit=$?"
git diff --name-only -- resources/board/plan.py resources/board/init.py
# non-vacuity, on scratch text only
grep -v '^\.state/parse-cache\.json$' .pearde/.gitignore \
  | grep -c '^\.state/parse-cache\.json$'   # 0 — the check wants 1
```
