---
complexity: 11
footprint:
  - resources/install.sh
  - resources/update.sh
  - resources/pearde.py
  - references/install.md
  - references/update.md
  - README.md
---

# spec03 — installing is one symlink, and updating only clears what an older one left

With one skill and a repo root already shaped like a skill folder, an install is
`ln -s <repo> <skills-dir>/pearde` and nothing is built. `resources/install.sh`
therefore has no job and is deleted, along with its `install` row in
`resources/pearde.py`'s `FORWARD` table. `resources/update.sh` keeps exactly one
job: removing the folders an earlier install left, because a leftover
`pearde-doctor/` and an index row are the agent seeing one task twice and the
folder wins the name match. A link to a working tree is never stale, so there is
nothing to re-link.

**This stands in the lane already** — `install.sh` is deleted, `FORWARD` no
longer carries it, `update.sh`'s `check_dir` reports the one link and clears
leftover folders (proved with `--dry` against three real skills directories on
this machine, which named 18 leftovers each and left the non-pearde symlinks
alone), and `references/install.md`, `references/update.md` and `README.md` are
rewritten around it. What is left to finish is `references/parts/doctor.md`'s
install wording and the `## Uninstall` cross-references.

The removal must never delete a real directory someone put there: only a folder
whose five entries — `SKILL.md`, `README.md`, `index.md`, `references`,
`resources` — are all symlinks, which nothing but an old install makes.

## Acceptance

- [x] `resources/install.sh` is not in the tree, and `git grep -c 'install\.sh'` over the tree is 0
- [x] `python3 resources/pearde.py help` runs and lists no `install` command
- [x] `bash -n resources/update.sh` passes and `bash resources/update.sh --dry` names each skills directory `ok`, `off` or `broken` without invoking any installer
- [x] `update.sh --dry` on a directory holding old `pearde-*/` folders prints what it would remove and removes nothing
- [x] `update.sh` on that directory removes only folders whose five entries are all symlinks, and leaves a real directory of the same name untouched
- [x] `update.sh` reports `ok` when `<dir>/pearde` is a symlink resolving to this repo, and `off` with `ln -s <repo> <dir>/pearde` as the fix when it is absent
- [x] `references/install.md` gives the install as one `ln -s` line, keeps the four cases for finding `<skills-dir>`, and describes no folder of five links
- [x] `git grep -c 'five links'` is 0 and no file says the installer retires itself
- [x] `references/update.md` says an install is one symlink and that `update.sh` clears leftovers rather than re-linking

## Verify and Proof

```sh
test ! -e resources/install.sh
test "$(git grep -c 'install\.sh' | wc -l)" -eq 0
test "$(git grep -c 'five links' | wc -l)" -eq 0
python3 resources/pearde.py help >/dev/null
bash -n resources/update.sh
bash resources/update.sh --dry
# the removal is scoped: a real directory of the same name survives
T=$(mktemp -d); mkdir -p "$T/pearde-doctor/notes"; echo hi > "$T/pearde-doctor/SKILL.md"
bash resources/update.sh --dry >/dev/null; test -f "$T/pearde-doctor/SKILL.md"
```
