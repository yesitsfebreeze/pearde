---
complexity: 3
footprint:
  - references/parts/commits.md
---

# spec03 — the reference says which repo a footprint path commits in

`references/parts/commits.md` is where a session and a worker read what
`collect` adds and where. It says **One commit per repo the PRD wrote**, and
it says a footprint is the union of the specs' `footprint:` — but it never
says which repo a given footprint path lands in, so `pearde/.gitignore` reads
as a code-repo path to everyone who writes a spec. That silence is what
produced the footprint that took a lane's merge down.

This unit adds the rule to the "One commit per repo the PRD wrote" paragraph,
in that file's prose: a footprint path is spelled relative to the code repo,
and a path that resolves inside a board which is its own git repo is committed
in the board repo under its board-relative name — never staged in the code
repo, which ignores the board and holds no such path. The lane does not carry
it either: the lane is cut without the board, so the board's own file is the
checkout's to commit, and it lands in the board's commit beside the PRD's
record.

**What already stands**: nothing in this file. **What is left**: the
paragraph, and one line naming what a spec author should expect when a
footprint names a path under the board. Prose only — `python3
resources/prose.py check` is the standard this repo holds its documents to.

## Acceptance

- [x] `references/parts/commits.md` states, in prose, that a footprint path
      resolving inside a board that is its own git repo commits in the board
      repo under its board-relative name
- [x] the same paragraph says the lane never stages it, because the lane is
      cut without the board
- [x] `python3 resources/prose.py check references/parts/commits.md` exits 0
- [x] `python3 resources/index.py check` reports no new line against the
      count before this PRD — every handle the new prose names resolves

## Verify and Proof

```sh
grep -qi "board repo" references/parts/commits.md
grep -qi "board-relative" references/parts/commits.md
python3 resources/prose.py check references/parts/commits.md
test "$(python3 resources/index.py check | wc -l)" -le 3
```
