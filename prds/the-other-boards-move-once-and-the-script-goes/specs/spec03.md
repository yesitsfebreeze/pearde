---
complexity: 3
footprint:          # none — the probe was the whole unit, and probe
                    # code is never a footprint. It is retired in
                    # board commit c15b234.
---

# spec03 — the script goes

The decision on record: no dual-path support, no permanent migration command.
Once spec02's gate is green over all eight boards, `migrate.py` leaves the
tree — the board's own record keeps what it did. This unit is one deletion
and one re-run of the gate to prove nothing else depended on the script.

What already stands: everything in spec01 and spec02. What is left: the
removal and the final re-verification. (The probe copy left in the tree by
pass one is this unit's deletion target; the PRD's own history in the board
repo holds the file after that.)

## Acceptance

- [x] `migrate.py` exists nowhere under the code repo or any board outside
      this PRD's own folder
- [x] the eight-board gate re-run after the deletion still passes

## Verify and Proof

```sh
R=/Users/feb/dev/infra/pearde
P="$R/resources/board/plan.py"
find "$R" -name migrate.py -not -path "*/.pearde/prds/the-other-boards-move-once-and-the-script-goes/*" |
  grep . && echo "LEFTOVER migrate.py FOUND" || echo "TREE CLEAN: no migrate.py outside this PRD folder"
for b in /Users/feb/dev/dotfiles /Users/feb/dev/infra/mitosys \
         /Users/feb/dev/infra/model /Users/feb/dev/infra \
         /Users/feb/dev/infra/realm /Users/feb/dev/infra/shared \
         /Users/feb/dev/manola /Users/feb/dev/racer/.mi; do
  python3 "$P" scan "$b" >/dev/null 2>&1 &&
    echo "GATE ok: $b" || echo "GATE FAILED: $b"
done
echo "spec03 gate: TREE CLEAN plus 8 GATE ok lines"
```