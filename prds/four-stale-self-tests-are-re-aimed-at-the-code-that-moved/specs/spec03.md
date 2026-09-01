---
complexity: 6
footprint:
  - .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
---

# spec03 — the vanished registry: four checks in two harnesses, not two

Both harnesses read `resources/board/state/serve.json`. That path has not
existed since the `every-artifact-lands-inside-the-board` invariant moved the
daemon's registration into the board that owns it — `resources/board/serve.py`
`entry_path()` returns `<board>/.state/serve.json`, and no machine-wide list
survives.

Each harness carries **two** checks on that path, and this is the trap the PRD
names: the loud one ("the copy's registry never learned the fixture", wanting
`[]`) fails, and the silent sibling ("the real registry is untouched") compares
an empty string to an empty string and **passes measuring nothing**. Re-aiming
only the loud one leaves the harness green and blind. All four move.

**Already standing (this analyst's uncommitted pass one), the same shape in
each file:**

- `REG` points at `$ROOT/.pearde/.state/serve.json` — this board's own
  registration, the file the invariant actually created.
- `REG_BEFORE` and the comparison both end `|| echo absent`. That is the part
  that removes the vacuity: the real board is not registered on a machine where
  the view daemon is not watching it, so a bare `[ -f ] && cksum` would still be
  empty-versus-empty. With the sentinel, a run that *creates* the real board's
  registration flips `absent` to a checksum and the check fails — which is the
  failure the check exists to catch.
- The sibling is re-aimed to the invariant it now expresses rather than to a
  deleted file's contents: `find "$TOP/srv" -name serve.json | wc -l` is `0` —
  the copied install is code only, and nothing the fixture run did wrote state
  beside it. `find` does not follow the symlinks `$TOP/srv` holds into the real
  tree, so this reads only the copy.
- Both are retitled ("the real board's registration is untouched", "the copied
  install holds no registration at all") and carry a comment naming the
  invariant that moved the file.

**Left to finish:** re-run both harnesses whole. `collect-is-a-command` is slow
and binds a port; run it on its own, never through a sweep.

**Downstream, already confirmed and not to be edited:**
`the-collect-and-brief-harnesses-are-carried-across-the-layou` sums sibling
totals and picked up `133 · 133 pass · 0 fail` with no edit of its own. Re-run
it as proof, change nothing in it.

## Acceptance

- [ ] `collect-is-a-command` reports 133 checks, 133 pass, 0 fail, exits 0, and its two R rows both read ok
- [ ] `init-asks-nothing` reports 88 checks, 88 pass, 0 fail, exits 0, and its two J rows both read ok
- [ ] Neither harness names `resources/board/state/serve.json` any more — `grep -c` over both files is 0
- [ ] The re-aimed sibling is shown non-vacuous: in a scratch directory, the `absent` sentinel changes value when the file is created, and the `find` count goes 0 → 1 when a `serve.json` is planted. Neither probe touches the real board
- [ ] `the-collect-and-brief-harnesses-are-carried-across-the-layou` exits 0 with no edit — `git -C .pearde diff --name-only` does not name it

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh; echo "exit=$?"
bash .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh; echo "exit=$?"
bash .pearde/prds/the-collect-and-brief-harnesses-are-carried-across-the-layou/probe/verify.sh; echo "exit=$?"
grep -c 'resources/board/state/serve.json' \
  .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh \
  .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
git -C .pearde diff --name-only
# non-vacuity, in a scratch dir only
M=$(mktemp -d); mkdir -p "$M/srv/board"
echo "empty: $(find "$M/srv" -name serve.json | wc -l)"
echo '{}' > "$M/srv/board/serve.json"; echo "planted: $(find "$M/srv" -name serve.json | wc -l)"
R="$M/x.json"; B="$( [ -f "$R" ] && cksum < "$R" || echo absent )"
echo x > "$R"; A="$( [ -f "$R" ] && cksum < "$R" || echo absent )"
[ "$A" = "$B" ] && echo VACUOUS || echo "sentinel catches creation"
rm -rf "$M"
```
