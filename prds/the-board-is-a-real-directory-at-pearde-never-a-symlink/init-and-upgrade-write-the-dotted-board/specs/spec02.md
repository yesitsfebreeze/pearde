---
complexity: 4
footprint:
  - .gitignore
---

# spec02 — this repo's own `.gitignore` is the block the tool would write

The code repo's `.gitignore` is the one real file the whole-block rewrite has to
land on, and it was three layouts behind: a header carrying a sentence about a
compatibility symlink that no longer exists, `/pearde` and `/.pearde` as bare
whole-directory rows, and a second block further down naming
`pearde/.state/`, `pearde/wiki/`, `.pearde/.state/` and `.pearde/wiki/` under a
comment saying `pearde/` is the board. Measured before the fix: running
`write_gitignore` against this file appended a **second** header block and left
every stale row of the first standing.

## What already stands

Applied in the lane, uncommitted:

- The machine-local block is the canonical one — `# machine-local per board —
  regenerable`, then `/.pearde` and the eight `.pearde/…` rows and `.obsidian/`.
  `/.pearde` is there because this repo's board is a git worktree of the code
  repo and carries its own `.git`; `ignored_names` writes that row for exactly
  that case, so the file is now stable under a rewrite rather than drifting
  from it.
- The second, stale block is gone with its comment.
- Every other block — the plugin bundles, the session measurements, `/board`,
  the playwright rows with their `@@share` note — is byte for byte where it was.

## What is left to finish

- Land it, and check nothing that used to be ignored is now noisy: `/pearde`
  and the two `pearde/…` rows were dropped, which is right only because this
  repo holds no directory called `pearde`.
- `.obsidian/` appears twice, once at the top of the file and once inside the
  block. Harmless to git and pre-existing; remove the top one or leave it, but
  do not remove it from the block — the block is regenerated.

## Acceptance

- [ ] `.gitignore` holds exactly one line equal to
      `# machine-local per board — regenerable`.
- [ ] No line in `.gitignore` starts with `pearde/`, and no line is `/pearde`.
- [ ] The block holds `/.pearde` and the eight `.pearde/…` rows.
- [ ] `git status --short` in the code repo prints nothing about `.pearde`, and
      `git add -A` stages no entry of mode 160000.
- [ ] Running `write_gitignore` against the landed file changes nothing — the
      file is already what the tool would write.

## Verify and Proof

```sh
test "$(grep -cx '# machine-local per board — regenerable' .gitignore)" = 1
test "$(grep -c '^pearde/' .gitignore)" = 0 && test "$(grep -cx '/pearde' .gitignore)" = 0
grep -qx '/\.pearde' .gitignore && test "$(grep -c '^\.pearde/' .gitignore)" = 8
git status --short | grep -c pearde | grep -qx 0
python3 - <<'PY'
import os, sys, shutil, tempfile
sys.path.insert(0, "resources"); sys.path.insert(0, "resources/board")
import init as I
d = tempfile.mkdtemp(); shutil.copy(".gitignore", os.path.join(d, ".gitignore"))
b = os.path.join(d, ".pearde"); os.makedirs(os.path.join(b, "prds"))
open(os.path.join(b, "settings.md"), "w").write("---\n---\n")
open(os.path.join(b, ".git"), "w").write("gitdir: /nowhere\n")
before = open(os.path.join(d, ".gitignore")).read()
I.write_gitignore(d, b)
assert open(os.path.join(d, ".gitignore")).read() == before, "the tool would rewrite it"
print("stable")
PY
```
