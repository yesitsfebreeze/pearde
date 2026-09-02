---
complexity: 8
footprint:
  - resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
  - references/files.md
---

# spec05 — a check that fails when the sharing stops holding

Nothing on this repo verifies the store. There is no invariant script, no doctor
line and no harness naming `share`; the mechanism is proved only by a person
reading `pearde share` output. The board keeps its standing claims in
`resources/invariants/`, each a script that exits non-zero when the claim stops
being true, and this claim has none.

What already stands: `share --json` reports every tree, path and state, which is
all the evidence a check needs. What is left is the script and its row.

The claim to check is the one the memo makes: every worktree of this repo points
at one store, no shared path is a real copy in two trees at once, and no linked
path is visible to `git status`. The script reports what fails and where, and
says nothing when the claim holds.

## Acceptance

- [x] The script exits zero on this repo as it stands and prints one line per claim it checked.
- [x] It exits non-zero when a linked path is replaced by a real directory in two trees at once.
- [x] It exits non-zero when a linked path becomes visible to `git status` in the tree that holds it.
- [x] It names the tree and the path in every failure, never just a count.
- [x] The script has its row in `references/files.md` and `python3 resources/index.py check` stays clean.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
sh resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh

D=$(mktemp -d)
mkdir -p "$D/a/x" "$D/b/x"
printf '{"store":"%s/store","rows":[{"tree":"a","path":"%s/a","rel":"x","state":"local"},{"tree":"b","path":"%s/b","rel":"x","state":"local"}]}' "$D" "$D" "$D" > "$D/two.json"
if SHARE_JSON="$D/two.json" sh resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh > "$D/two.out" 2>&1; then
  rm -rf "$D"; echo "the script passed a survey with one path real in two trees"; exit 1
fi
grep -q "real copy in 2 trees at once" "$D/two.out" || { rm -rf "$D"; echo "it failed without naming the doubled path"; exit 1; }

git init -q "$D/r"
mkdir -p "$D/r/store/y"
ln -s store/y "$D/r/y"
printf '{"store":"%s/r/store","rows":[{"tree":"r","path":"%s/r","rel":"y","state":"linked"}]}' "$D" "$D" > "$D/vis.json"
if SHARE_JSON="$D/vis.json" sh resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh > "$D/vis.out" 2>&1; then
  rm -rf "$D"; echo "the script passed a survey whose link git shows"; exit 1
fi
grep -q "git shows the link at y" "$D/vis.out" || { rm -rf "$D"; echo "it failed without naming the visible link"; exit 1; }
rm -rf "$D"
echo "ok: the script reports both failures and names tree and path"

out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
case "$rc" in 0|1) ;; *) echo "index.py check crashed, rc=$rc"; exit 1;; esac
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'one-copy-per-machine-of-what-every-lane-regenerates|^references/files\.md '; then
  echo "the new script or its row is not answered by the manifest"; exit 1
fi
echo "ok: index.py check names neither the script nor its row"
```

The two fixture surveys are what proves the check can fail: `SHARE_JSON`
replaces `share --json` with a file, so claim 2 and claim 3 are put a tree
that breaks them and the block refuses a script that stays green. `index.py
check` reads the whole manifest and its exit is decided by rows in every other
file on the board, so it is captured and printed, and only the lines naming
this spec's own two paths decide the block.
