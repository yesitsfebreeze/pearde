---
complexity: 8
footprint:          # none — the probe was the whole unit, and probe
                    # code is never a footprint. It is retired in
                    # board commit c15b234.
---

# spec01 — migrate.py, the throwaway one-shot

The migration script itself, proven on fixtures: a whole `prds/` board moves
to `.pearde/` in one pass (git mv where tracked, plain move where not), then
sorts itself out — `prds/` and `.state/` created inside, every PRD directory
into `prds/`, `knowledge/` to `wiki/`, `memos/`/`workflows/` left as siblings
of `prds/`, `settings.md` and `vision.md` at the board root, the five state
dotfiles into `.state/<name>` (leading dot dropped), the board's `.gitignore`
rewritten, the master's members rows and the serve.json registry rows
repointed. A state file both a loose dotfile and `prds/.state/` supplied
keeps the loose copy (the fuller record); the loser is kept aside as
`<name>.from-state-dir` and warned about, never deleted. Already-migrated
boards are skipped, so a re-run is a no-op.

What already stands: the script is written and lives at the probe path below,
fixture-proven — `bash probe/verify.sh` prints `verify: 31 checks · 31 pass ·
0 fail`. It covers a tracked board (git mv staged as renames, untracked PRDs
riding along), a master whose members row names a member by its old `prds/`
spot (row rewritten `../board-a/prds` → `- ../board-a/.pearde`, member PRDs
reported under the `@board-a/` sigil), a fully untracked board (index
untouched), state collisions, and registry rewrite.

What is left: nothing on the script itself. It stays where it is until
spec02 has run it for real and spec03 deletes it.

## Acceptance

- [x] `migrate.py` on a fixture copy of an old-layout board produces
      `.pearde/prds/<name>/prd.md` for every PRD dir that `prds/` held, with
      the PRD's name unchanged, and no `prds/` left at the board root
- [x] after migration the moved code's own scan of the fixture exits 0 and
      lists every PRD under the name it had before the move
- [x] the five state dotfiles sit at `.pearde/.state/<name>` with the leading
      dot dropped, and a collision keeps the loose copy with the loser at
      `.state/<name>.from-state-dir`
- [x] on a git-tracked board the move lands as staged `R` renames; on a fully
      untracked board the index is untouched
- [x] a re-run on a migrated board exits 0 and prints "already"

## Verify and Proof

```sh
D=$(mktemp -d) && cd "$D" || exit 1
mkdir -p b/prds/alpha b/prds/memos b/prds/.state
git -C b init -q
printf -- '---\nstate: open\n---\n\n# a\n' > b/prds/alpha/prd.md
echo m > b/prds/memos/m.md && echo h > b/prds/.history.jsonl
echo s > b/prds/.state/history.jsonl
git -C b add prds && git -C b -c user.email=p@p -c user.name=p commit -qm i
python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan "$D/b" >/dev/null 2>&1 \
  && echo "BAD: unmigrated board scanned" || echo "pre-gate ok"
python3 "$OLDPWD/probe/migrate.py" "$D/b" || echo "MIGRATE FAILED"
python3 /Users/feb/dev/infra/pearde/resources/board/plan.py scan "$D/b" >/dev/null 2>&1 &&
  echo "GATE: scans clean" || echo "GATE: FAILED"
[ -f "$D/b/.pearde/prds/alpha/prd.md" ] && [ ! -e "$D/b/prds" ] &&
  echo "LAYOUT: ok" || echo "LAYOUT: FAILED"
[ "$(cat "$D/b/.pearde/.state/history.jsonl")" = h ] &&
  echo "STATE: loose record kept" || echo "STATE: WRONG COPY"
echo "spec01 probe: 4/4 gate lines above must read ok"
rm -rf "$D"
echo "spec01 fixture gate done"
```