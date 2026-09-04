---
complexity: 8
footprint:
  - resources/board/ramp.py
---

# spec01 — a master's need is the union of every tree it reaches

`needs()` measures the union over `members:` rather than the board's own repo,
each member measured in its own repo the way its own board would measure it,
and the master's own tree counted as one more member. The floor lands on the
sum, never per member, and a master's `why` credits the members that
contributed instead of restating markers summed over five trees.

## What already stands

The probe left this working in the tree, uncommitted:

- `scan_roots(board)` — `[(name, board)]`, every board a need is measured
  over, each exactly once. A plain board returns `[("", board)]` and nothing
  downstream changes. A master returns itself plus every board reachable
  through `members:` **to any depth**, keyed by realpath so a cycle
  terminates and a board reached by two routes is counted once. Names come
  from `members:` and are suffixed `-2`, `-3` on a collision.
- `_measure(board)` — `{job: (hits, why)}` for one board, floors not applied:
  the old `needs` body, with `board_words` swapped for `_words_of`.
- `_words_of(board)` — one board's PRD titles; `board_words` unions these.
- `needs(board)` — sums `_measure` across `scan_roots`, floors the sum, and
  builds `why` from the per-member parts, loudest member first.

Proven by `probe/compare.sh` (five plain boards byte-identical against the
committed `ramp.py`, only the master moves) and `probe/fixture.sh` (ten
assertions on a tree built at run time).

## What is left

Two edges the probe reached and did not close.

`write_ask()` phrases every fork as "The tree asks for {job} ({why})". On a
master `why` is now `mitosys 3` — a member credit, not a marker list — so the
sentence a person reads is "The tree asks for go (mitosys 3)", which names one
tree for a signal that came from another. The fork must say which member asked.

`board_words()` unions the members' titles and has no caller: `_measure` needs
the per-board split, so `_words_of` is what `needs` reaches for. It stays as
the public accessor the contract names, and its docstring must say why nothing
inside `needs` calls it — an unexplained uncalled function reads as a leftover
and the next pass deletes it.

## Acceptance

- [x] `scan_roots` on a board with no `members:` returns exactly one row whose
      name is empty, and `needs` on that board is byte-identical to the
      committed `ramp.py`'s output — checked on all four member boards and on
      pearde's own
- [x] `scan_roots` on a master returns the master and every board reachable
      through `members:`, at any depth, each realpath once
- [x] a `members:` cycle terminates and counts each repo once
- [x] `needs` on a master returns per-job counts that equal the sum of the
      members' own counts, the master's own repo included
- [x] a floor is applied to the summed count, so two members that each fall
      short of `writing`'s 25 raise `writing` together
- [x] each master row's `why` names the members that contributed, loudest
      first, and no marker pattern
- [x] `write_ask` on a master phrases the fork so it names the member the
      signal came from, not "the tree"
- [x] `board_words`'s docstring says it is the public union accessor and why
      `needs` calls `_words_of` instead

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# The union arithmetic, on repos built at run time — decided by
# `resources/board/ramp.py` and nothing else in the checkout.
bash .pearde/prds/the-master-ramp-measures-its-own-tree-not-its-members/probe/fixture.sh

# A plain board is one unnamed root and its own marker list. This is asserted
# against the module, not against a `git archive HEAD` export: once this unit
# is committed HEAD *is* the union, so a diff against it proves nothing, and
# in the meantime it is decided by whichever sibling has `plan.py` in flight.
for b in /Users/feb/dev/infra/mitosys/.pearde /Users/feb/dev/infra/model/.pearde \
         /Users/feb/dev/infra/realm/.pearde /Users/feb/dev/infra/shared/.pearde \
         /Users/feb/dev/infra/pearde/.pearde; do
  if [ -d "$b" ]; then python3 - "$b" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    "ramp_ut", "resources/board/ramp.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
b = sys.argv[1]
roots = m.scan_roots(b)
if roots != [("", b)]:
    print("FAIL a plain board is not one unnamed root:", b, roots); sys.exit(1)
rows = [r for r in m.needs(b) if r[0] == "rust"]
if rows and "×" not in rows[0][2]:
    print("FAIL a plain board's why is not a marker list:", b, rows[0]); sys.exit(1)
print("plain:", b)
PY
  fi
done

# The master on this machine, printed. Its numbers are the member repos', not
# this footprint's, so they are gated only where the board is actually here.
if [ -d /Users/feb/dev/infra/.pearde ]; then
  need=$(python3 resources/pearde.py ramp need --board /Users/feb/dev/infra/.pearde 2>&1) && nrc=0 || nrc=$?
  printf '%s\n' "$need"
  if [ "$nrc" != 0 ]; then echo "FAIL ramp need exit $nrc"; exit 1; fi
  rust=$(printf '%s\n' "$need" | awk '$1=="rust"{print $2}')
  if [ -z "$rust" ]; then echo "FAIL the master prints no rust row"; exit 1; fi
  if [ "$rust" -lt 1000 ]; then echo "FAIL rust $rust — the master is measuring its own tree"; exit 1; fi
  credit=$(printf '%s\n' "$need" | awk '$1=="rust"{$1="";$2="";print}')
  case "$credit" in *mitosys*) ;; *) echo "FAIL the rust row credits no member:$credit"; exit 1;; esac
else
  echo "skip: /Users/feb/dev/infra/.pearde is not on this machine"
fi
```
