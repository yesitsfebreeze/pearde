---
complexity: 8
footprint:
  - resources/board/collect.py
  - .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe
---

# spec01 — `--also` resolves against the board, and refuses what the board does not hold

`collect --also <path>` gets the existence guard the footprint loop eight
lines above it has always had, and the board-relative resolution `--widen`
two lines below it has always had. A path the board does not hold refuses
the **whole call** — nothing written, nothing committed, for any PRD named —
and the refusal names the path as it was given, the absolute path it
resolved to, and the directory it was resolved against.

**What already stands.** The build is in the tree, uncommitted, and its
harness reads 41/41 green:

- `also_path(board_root, a)` and `check_also(board_root, opts)` in
  `resources/board/collect.py`, added after `parse_args`. `also_path` is the
  one place an `--also` entry becomes a path, so the path a refusal names and
  the path a commit carries cannot drift.
- `cmd_collect` calls `check_also(planlib.repo_root(board) or board, opts)`
  immediately after `find_board`, **before** the `for rel in rels` loop.
  That loop catches `Stop` per PRD and carries on to the next one, so a guard
  inside `collect_one` would refuse one PRD and still commit the rest — the
  contract is refusal of the call.
- `sort_paths`' `--also` loop now reads `also_path(board_root, a)` in place of
  `os.path.abspath(a)`.
- The harness at
  `.pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh` —
  eight sections, a throwaway `git init` board per scenario, never the real
  board. `COLLECT` is overridable, so pointing it at `git show
  HEAD:resources/board/collect.py` shows it go red (20 pass · 21 fail).

**What is left to finish.** Run the boxes below and quote the counts. The
guard's predicate is `os.path.exists` — the same one the footprint loop uses,
so a directory that is on the board still goes through; do not narrow it to
`os.path.isfile`, and do not touch `--widen` or the footprint loop.

## Acceptance

- [ ] The probe harness reads `41 checks · 41 pass · 0 fail` and exits 0
- [ ] Pointed at `HEAD`'s `collect.py` via the `COLLECT` env var, the same
      harness exits non-zero — the checks can fail
- [ ] `collect --also <path the board does not hold>` exits 1, commits
      nothing, and the message names the path, the resolved absolute path and
      the board root
- [ ] Two collectable PRDs named on one call with a bad `--also` leave both at
      `state: claimed` with no commit — the refusal is the call's, not one PRD's
- [ ] A relative `--also` that exists under the board resolves and rides the
      commit even when the caller's cwd is somewhere else entirely
- [ ] A relative `--also` that exists only under the caller's cwd is refused,
      and the refusal names the board root rather than the caller's file
- [ ] `collect-is-a-command` reads `133 checks · 133 pass · 0 fail` — its
      section K, which passes an absolute `--also`, is unchanged
- [ ] `collect-keeps-its-word` reads `101 checks · 101 pass · 0 fail`
- [ ] `python3 resources/index.py check` exits 0 and `bash resources/doctor.sh`
      exits 0 with no row that was not there before

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh
mkdir -p /tmp/pearde-head/board
git show HEAD:resources/board/collect.py > /tmp/pearde-head/board/collect.py
COLLECT=/tmp/pearde-head/board/collect.py \
  bash .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh; \
  test $? -ne 0 && echo "can-fail: proven"
rm -rf /tmp/pearde-head
bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh
python3 resources/index.py check
bash resources/doctor.sh
```
