---
complexity: 14
footprint:
  - resources/board/collect.py
---

# spec02 — the healing preserves what it cannot prove is the block's

`_heal` ran `git clean -f -d` on every foreign untracked path and
`git reset -q HEAD --` on every foreign tracked one, checked not one
returncode, and printed `put back: <every row>` regardless. All three are
wrong for the same reason: this board is written by several sessions at once
— the shared checkout held 24 foreign dirty files and nine live workers when
this was found, and a block runs for about eight seconds — so a foreign path
dirty AFTER the block is a peer's live work as readily as it is the block's
litter, and nothing at that point can tell them apart. `clean` deleted a
peer's brand-new file outright, the stash pop had never held it, and the
output line said it had been put back. That is strictly worse than the
incident the guard was filed to prevent.

So `_heal` deletes nothing. What the block left is moved out of the checkout
into `<git dir>/collect-aside/<stamp>/`, bytes intact, and `collect` prints
where; a path HEAD knows is then written back from HEAD's blob, READ and
written here rather than `git checkout`ed, because checkout writes the index
and a peer's staged entry is not this block's to discard. A path whose index
column is neither a space nor a `?` — someone ran `git add` on it inside the
window — is left exactly as it is, worktree and index both, and named:
`collect` builds its commits in a private index, so what stays staged there
reaches no commit of ours. Every git call is checked, and the `put back:`
line names only the paths actually restored; what could not be restored gets
its own line.

The same pass makes the previous PRD's `spec02` box honest. It claimed "a
green destructive verify block, and the PRD's uncommitted footprint change is
what gets committed", and closed against `rm -f` — the one destructive shape
the mechanism happened to catch. `git reset --hard HEAD`, the harness's own
`DESTRUCTIVE` constant and the incident in this PRD's title, left the file
PRESENT holding HEAD's bytes, so `_unerase` saw nothing missing, `collect`
committed the revert, wrote `done` and printed nothing. `spec02` decided that
a path the block MODIFIES stays modified, and that stands — a formatter
editing the file under test is legitimate and indistinguishable from the
change itself. A revert to HEAD is distinguishable: the file is byte-for-byte
HEAD again and the snapshot holds something else. `_unerase` now also puts
back a `copy`-kind snapshot whose path has been reset to HEAD's own bytes,
and only that.

## What already stands

Nothing in the checkout — `8bbb4c1` reverted it. The lane's uncommitted tree
carries this unit built and green on top of `spec01`. It needs `spec01`'s
`_dirty` under it: the old parser hid a spaced path from `_heal` entirely.

## What is left to finish

Nothing but landing it, on top of `spec01`, and re-running both harnesses on
the merged tree.

## Acceptance

- [x] a foreign UNTRACKED file created inside the verify window is on disk
      afterwards with its bytes intact, in the directory `collect` names on
      its `moved aside to` line — nothing calls `git clean` on it
- [x] `probe/verify.sh` section F3/F4: driven through `pearde collect`, the
      peer's file survives here and is destroyed on pass one's collect, whose
      output claims `put back: other/peer-new.txt` while the file is gone
- [x] the `put back:` line names only paths actually restored — an untracked
      path, which HEAD cannot restore, is not on it
- [x] a restore that fails is reported on its own `NOT put back` line rather
      than counted
- [x] a foreign path a peer STAGED inside the window keeps its index entry
      and its worktree bytes, and `collect` says it left it staged
- [x] a green block running `git reset --hard HEAD` on the LANELESS path
      leaves the PRD's uncommitted work on disk, gets it committed, and names
      it on a put-back line — and the same fixture on pass one's collect
      commits the revert silently
- [x] a block that edits an owned file to something that is NOT HEAD leaves
      it edited — the witness that keeps the box above from meaning "restore
      everything"
- [x] this spec's own verify block contains no `cd`

## Verify and Proof

```sh
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
test -z "$(grep -n 'clean., .-f., .-d' resources/board/collect.py)" && echo "no git clean left in the healing"
test -z "$(grep -n 'reset., .-q., .HEAD' resources/board/collect.py)" && echo "no blanket index reset left"
python3 .pearde/prds/the-verify-guard-parses-git-s-own-output-before-it-trusts-it/probe/probe_unit.py
bash .pearde/prds/the-verify-guard-parses-git-s-own-output-before-it-trusts-it/probe/verify.sh
```
