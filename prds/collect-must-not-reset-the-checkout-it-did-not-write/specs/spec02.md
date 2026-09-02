---
complexity: 3
footprint:
  - references/parts/commits.md
---

# spec02 — the commits contract says what the rollback actually does

`references/parts/commits.md` is the one document describing what a red
verify does to the checkout, and its sentence is the one the code was
written from: *"A red verify resets the checkout to the commit it was on
and leaves the lane branch untouched, so a retry merges the same commits
again."* Read literally that sentence permits `reset --hard` — it names the
checkout, not the branch pointer, and says nothing about the uncommitted
work standing beside the merge. The next reader of that paragraph must not
be able to write `--hard` back.

**Standing after pass one**: nothing. The paragraph is untouched; only the
code changed.

**Left to finish**: replace that sentence in the "Where the commit is made:
the lane" paragraph so it says three things the code now does — the branch
pointer moves back and the working tree is kept, nothing is rolled back
when the merge merged nothing, and a rollback that cannot keep the
uncommitted work refuses rather than discarding it. One paragraph edit; no
new heading, no new row anywhere.

## Acceptance

- [x] the sentence in `references/parts/commits.md` that describes a red
      verify names the branch pointer, not "resets the checkout"
- [x] it says the checkout's uncommitted work is kept
- [x] it says a merge that merged nothing is not rolled back
- [x] it says a rollback that cannot keep the work refuses and leaves the
      merge standing
- [x] `python3 resources/index.py check` prints no line naming
      `references/parts/commits.md`
- [x] `bash resources/doctor.sh` prints no new red row against the run
      recorded in this PRD's report

## Verify and Proof

```sh
p=references/parts/commits.md
grep -n 'branch pointer' "$p"
n=0
for s in 'branch pointer' 'is kept, because a gate' 'rolled back at all' \
         'rather than discarding it'; do
  if ! grep -qF "$s" "$p"; then echo "missing from $p: $s"; n=$((n+1)); fi
done
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ -z "$out" ] && [ "$rc" != 0 ]; then echo "index.py check printed nothing on exit $rc"; n=$((n+1)); fi
c=$(printf '%s\n' "$out" | { grep -cF "$p" || true; })
if [ "$c" != 0 ]; then echo "index.py check names $p $c time(s)"; n=$((n+1)); fi
echo "spec02: $n problem(s)"
[ "$n" = 0 ]
```
