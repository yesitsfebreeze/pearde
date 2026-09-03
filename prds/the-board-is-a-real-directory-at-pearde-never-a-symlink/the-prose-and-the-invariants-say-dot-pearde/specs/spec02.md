---
complexity: 6
footprint:
  - resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
  - resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
  - resources/invariants/every-artifact-lands-inside-the-board.sh
---

# spec02 — every invariant finds the dotted board, and exercises it

Three invariant scripts spelled the board undotted. One of them was red:
`no-colour-group-in-the-vault-preset-is-a-path-query.sh` looks for the board
beside itself, so run from a lane — a worktree of this repo, holding an empty
`.pearde/` — it found no board and exited 1. Another,
`a-board-s-own-file-commits-in-the-board-repo.sh`, built its nested fixture at
`<code>/pearde`, so the invariant guarding the layout this repo has was
exercising only the name the repo no longer uses.

**Stands.** All three are rewritten in the lane and all three are green from
the lane. The colour-group script resolves the checkout from `git rev-parse
--git-common-dir` and asks `.pearde/` before `pearde/`; its BROKEN line names
the path it looked at. The board-file script's `nested` fixture is `.pearde/`
throughout — the fixture board, the code repo's ignore line, the lane probe
path, the two log needles and the board-spelled section — and still reports 20
PASS 0 FAIL, now against the dotted nested layout. `every-artifact` says
`.pearde/` in its prose and prunes both names with the dotted one first.

**Left.** Nothing but the checks below.

## Acceptance

- [x] `no-colour-group-in-the-vault-preset-is-a-path-query.sh` exits 0 run from
      a lane as well as from the checkout, and reports the same 8 colour groups
      from both.
- [x] Its board resolution reaches the checkout, not the tree the script sits
      in: pointing it at a worktree with an empty `.pearde/` still finds the
      board.
- [x] `a-board-s-own-file-commits-in-the-board-repo.sh` exits 0 with 20 PASS
      and 0 FAIL, and its nested fixture directory is `.pearde`.
- [x] `every-artifact-lands-inside-the-board.sh` exits 0 with 7 PASS and 0
      FAIL.
- [x] None of the three names `pearde/` as the board's own name; each bare one
      left says legacy.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
I=resources/invariants
for f in no-colour-group-in-the-vault-preset-is-a-path-query \
         a-board-s-own-file-commits-in-the-board-repo \
         every-artifact-lands-inside-the-board; do
  out=$(bash "$I/$f.sh" 2>&1); rc=$?
  printf '%-58s rc=%s PASS=%s FAIL=%s\n' "$f" "$rc" \
    "$(printf '%s' "$out" | grep -c '^PASS')" "$(printf '%s' "$out" | grep -c '^FAIL')"
  [ "$rc" = 0 ] || exit 1
  printf '%s' "$out" | grep -q '^FAIL' && exit 1
done
# the colour-group script is green from a WORKTREE too — the case that was red.
# The script under test is copied in, not the committed one: this has to fail
# before the fix lands and pass after it, in one tree, uncommitted.
W=$(mktemp -d)/w
git worktree add -q --detach "$W" HEAD
mkdir -p "$W/$I"
cp "$I/no-colour-group-in-the-vault-preset-is-a-path-query.sh" "$W/$I/"
mkdir -p "$W/.pearde"        # what a real lane holds: the empty dot-directory
( cd "$W" && bash "$I/no-colour-group-in-the-vault-preset-is-a-path-query.sh" ); rc=$?
git worktree remove --force "$W"
[ "$rc" = 0 ] || { echo "FAIL: red from a worktree"; exit 1; }
# the nested fixture is the dotted layout
grep -q 'board=$code/\.pearde' "$I/a-board-s-own-file-commits-in-the-board-repo.sh" || exit 1
# No invariant calls the undotted name the board's own. Every bare `pearde/`
# left says legacy, says upgrade, or is half of a `\.?pearde` pattern matching
# both names; a line asserting `pearde/` as the board fails here.
grep -nE '(^|[^./a-zA-Z_-])pearde/' $I/*.sh | grep -vE 'legacy|upgrade|\\\.\?pearde' && exit 1
echo "spec02 ok"
```
