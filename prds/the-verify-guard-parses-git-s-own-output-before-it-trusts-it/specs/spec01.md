---
complexity: 12
footprint:
  - resources/board/collect.py
---

# spec01 — the guard reads git's own output before it trusts it

`6ea9c20` landed the whole verify guard — `guarded_run` and its ten helpers —
and `8bbb4c1` took it back out because `_dirty` believed a format that lies.
`git status --porcelain` QUOTES any path holding a space or a non-ASCII byte
unless `core.quotePath` is turned off, so `line[3:]` handed every consumer
`"src/a b.py"`, quotes and all. Each one then got it wrong at once:
`inside()` matched no footprint, so an owned file read as foreign and the
block measured a clean HEAD — the failure `spec01` of the previous PRD names
as fatal; `_park` fed the quoted string in as a pathspec, git refused it, and
ONE such path ran the whole block unguarded; `_snapshot` found the real path
in neither `moved` nor `indexed`, held its index blob, and let `_unerase`
write HEAD's bytes over the PRD's uncommitted work while printing
`put back:`.

This unit re-lands `6ea9c20`'s code unchanged in its mechanism and reads git
in a format that cannot lie: `git status --porcelain -z --untracked-files=all`.
`-z` never quotes and spends a second NUL-terminated record on a rename's
source, which is consumed rather than split out of a ` -> ` that is not there.
`-uall` because the default collapses a wholly untracked directory into one
row spelled `other/` — a row `inside()` reads wrong against any footprint
deeper than it, and one that makes the healing take a whole tree where a
single file was written.

The same pass closes the other place the guard trusted a shape it had not
read: `_owned_files` skipped every symlink, so a footprint link a block
deleted was never put back — and this repo's own `.pearde` **is** a symlink.
A link is now snapshotted by its target string, never followed, and re-made
with `os.symlink`; `os.stat` is not asked, so a dangling link survives too.

## What already stands

Nothing in the checkout: `8bbb4c1` reverted all 288 lines. The lane's
uncommitted tree carries this unit built and green, and `probe/verify.sh` now ends on
`exit $(( FAIL > 0 ))` so the tally is the exit status. `6ea9c20` is where the
code comes from — recover it (`git diff 8bbb4c1 6ea9c20 -- resources/board/collect.py`
applies clean), do not rewrite it. The design was checked and is not reopened:
`_park` pathspec-limited so it cannot disturb the snapshot's subjects,
snapshot after park, `_restore_head` before `_heal`, `_unerase` after `_heal`
and before the stash pop.

## What is left to finish

Nothing but landing it: re-apply, re-run both harnesses on the merged tree,
tick the boxes.

## Acceptance

- [x] `_dirty` reads `git status --porcelain -z --untracked-files=all` and
      returns unquoted paths — `probe_unit.py`'s
      "a path with a space is classified, parked, healed and unerased" holds
      an owned and a foreign spaced path and both come through exactly as
      their unspaced twins do
- [x] a rename is one row naming its destination — `-z`'s separate source
      record is consumed, not read as the next row's status code
- [x] `_dirty` returns `[]` rather than garbage when the `git status` call
      itself fails
- [x] a footprint symlink a block deletes is put back with its target string,
      and a DANGLING one is snapshotted and restored too — `os.stat` follows
      a link and would drop it
- [x] `guarded_run`, `owned_by`, `_park`, `_heal`, `_head_of`,
      `_restore_head`, `_dirty`, `_owned_files`, `_blobs`, `_snapshot` and
      `_unerase` are all in `resources/board/collect.py`, and the verify loop
      calls `guarded_run` with `owned` computed once before it
- [x] `probe/verify.sh` section F5/F6: a foreign path with a space in the
      checkout, and a destructive block — the neighbour survives here and is
      destroyed on pass one's collect, which says `could not park foreign
      dirt` as it goes
- [x] `probe/verify.sh` exits non-zero when a check fails — the tally line
      alone was the whole ending, so both specs' verify blocks passed on a red
      run; `PEARDE_ROOT` at a tree with no guard in it must redden the command
- [x] this spec's own verify block contains no `cd` — `collect` already runs
      a spec block in `repo`, and the `cd` pass one carried pinned the
      machine and was the one documented way out of the fence

## Verify and Proof

```sh
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
grep -c '"--porcelain", "-z"' resources/board/collect.py
test -z "$(grep -n 'line\[3:\]' resources/board/collect.py)" && echo "no line[3:] left"
grep -n "code, output = guarded_run" resources/board/collect.py
bash .pearde/prds/the-verify-guard-parses-git-s-own-output-before-it-trusts-it/probe/verify.sh
```
