---
complexity: 8
footprint:
  - resources/board/orphans.py
  - references/files.md
  - index.md
---

# spec01 — the orphan scan is a board command

`python3 resources/board/orphans.py` — the repo-bug audit this PRD ran as a
probe, landed in the tree so the next bug window is one command away. It
enumerates every done PRD on every board in `resources/board/state/serve.json`,
classifies each footprint path against the branch that should hold it (the
code branch of the store the board's worktree resolves to, or the branch the
PRD's `repo:` key names), and prints one ORPHAN block per done PRD whose
footprint has a `branch-only`, `nowhere` or `absent` path, then the count line
`done PRDs: N · with footprints: N · flagged: N · branch-only (bug residue): N`.
Exit 0 when the scan ran, 1 when a footprint path could not be classified.

What already stands: the whole classification as a probe at
`prds/collect-commits-the-code-repo-not-the-board-repo-twice/list-the-collects-the-repo-bug-orphaned/probe/scan.py`
— per-branch commit checks (`branch_local`), the worktree discovery
(`worktrees` in the board's `--git-dir`), the `repo:` key override, the
shared-store premise, and the decision tree hand-proven on a fixture. Left:
move it into the tree as a real module (name, argument handling, row output
only as `--json`, no fixtures under the board), and give the file its manifest
rows.

Compute cost: ~2 `git log` calls per footprinted done PRD — seconds on this
machine's 166; no `--all`, no index rebuild.

What it must NOT do: no `--fix`, no commit, no write outside stdout/stderr —
a person does the re-commits the list names.

## Acceptance

- [x] `python3 resources/board/orphans.py` from the code repo prints a count
      line carrying `done PRDs: N · with footprints: N · flagged: N ·
      branch-only (bug residue): N` and exits 0 when `branch-only` is 0
- [x] a fixture repo with a nested worktree board and a done PRD whose
      footprint path was committed on the board branch only classifies that
      path `branch-only` and exits 1 — misdirection is caught, not just absence
- [x] a `repo:` frontmatter key pointing at a second repo checks the
      footprint against that repo's branch, not the board's default
- [x] `python3 resources/index.py check` exits 0 with the new file landed —
      the manifest row in `@references/files.md` and a place in every scope
      it belongs to
- [x] the same fixture with the board NOT its own worktree (plain `.git` walk-up)
      reports no `branch-only` — the old default was harmless exactly there

## Verify and Proof

```sh
python3 /Users/feb/dev/infra/pearde/resources/board/orphans.py | tail -1
python3 resources/index.py check && echo "manifest ok"
bash /Users/feb/dev/infra/pearde/.pearde/prds/collect-commits-the-code-repo-not-the-board-repo-twice/list-the-collects-the-repo-bug-orphaned/probe/verify.sh | tail -2
```