---
state: done
origin: requested
priority: 40
complexity: 18
blast-radius: mid
workflow: probe-then-spec
actual: 0.54h
commit: 740713b 551a422
---

# The master ramp measures its own tree, not its members

The ramp gate is loop step 0, and on a master board it reads the wrong tree.
`ramp need` measures the board's **own** repo and only that repo, so the one
signal that opens or closes the gate has nothing to do with the code the board
plans over.

## Measured 2026-09-02 on `/Users/feb/dev/infra/.pearde` (master of 4)

```
$ pearde ramp need
writing        104  *.md×104
docker           2  1 PRD
rust             1  *.rs×1
```

That `rust 1` is one file:

```
.pearde/prds/a-shared-name-is-not-a-shared-function/probe/main.rs
```

A probe, inside the board's own directory. The four member trees this board
plans over hold **14,562 tracked `.rs` files** — mitosys 14,113, model 344,
realm 86, shared 19. Every member is a Rust workspace; `infra` is not a Rust
repo at all.

That single probe file raised a `GAP rust` that reached the user as a question
and cost two passes. The gap was real by accident: the board does need Rust
skills, but not for the reason the gate gave, and the same arithmetic would
have missed it entirely had that probe not existed.

## Cause

`needs(board)` in `resources/board/ramp.py`:

- `repo = repo_of(board)` — the board's parent directory, one repo.
- `paths = tracked(repo)` — `git ls-files` in that one repo.
- `titles = board_words(board)` — walks `board/prds` only.

`members:` is never read. Neither the file markers, nor the manifest
dependencies, nor the PRD titles cross a member boundary, so a master board
measures the one tree that by construction holds the least code — its own.
`docker 2 · 1 PRD` has the same fault on the title axis: it counts the
master's own PRD titles and none of its members'.

## What it should be

A master board's `need` is the **union over its members**, each member
measured in its own repo the way its own board would measure it, then summed
per job. The master's own tree is one more member of that union, not the whole
of it. `repo_of` stays right for a plain board; the master case needs the
member list `plan.py` already resolves.

## Boxes

- [x] `needs()` reads `members:` and unions each member's `tracked(repo_of(m))`
      and `manifest_text`, the master's own repo included
- [x] `board_words()` unions each member's `prds/` titles
- [x] `need` / `gap` / `ramp` print per-job counts that add up to the union,
      and a master's row says which members contributed
- [x] a plain board's numbers are unchanged — the same three jobs, the same
      counts, on a member board scanned directly
- [x] the master board's `ramp need` reports rust in the thousands, not 1

## Verify and Proof

```
python3 resources/pearde.py ramp need --board /Users/feb/dev/infra/.pearde
```

Green when the `rust` row counts the members' trees rather than the board's
own probe file, and a member board scanned on its own is unchanged.

## Notes

Found while answering the ramp's own question. The user's ruling was: fix the
signal first, leave `happiness:` at 0, and file this — the gate should not be
closed by hand while the number it prints is measured against the wrong tree.

Two neighbouring findings from the same pass, neither this PRD's to fix:

- `installed()` is **not** at fault for symlinks — `os.path.isdir` follows
  them. The 38 skills installed this pass were invisible to `ramp have`
  because `npx skills add` wrote *relative* links (`../../../.agents/skills/X`)
  into `~/.claude/skills`, while computing the depth for
  `$CLAUDE_CONFIG_DIR/skills` — which on this machine is a symlink to it. All
  38 were dangling. Repaired by hand to absolute links; the gap then closed.
  An installer bug this machine's layout triggers, not a ramp bug — but a
  ramp that said "0 of 3 unanswered" one command after 38 skills landed would
  have been believed.
- `ramp have` cannot tell a live skill from a dangling link, and the same
  `isdir`-follows-symlinks that makes it correct also makes it silent. A row
  that names a broken install would have caught the above in one line.

## Report

spec01: exit 0
PASS  a alone counts its own 30 .rs (got 30)
PASS  b alone counts its own 12 .rs (got 12)
PASS  the master sums 30+12+1 = 43 (got 43)
PASS  the master's rust row credits member a
PASS  the master's rust row credits its own tree
PASS  c's .md alone stays under writing's floor
PASS  d's .md alone stays under writing's floor
PASS  the floor is applied to the sum, never per member: 35 over two members that each fall short
PASS  a master under a master reaches the grandchildren: 43 (got 43)
PASS  a members cycle terminates and counts each repo once: 8 (got 8)
5 plain boards identical to the committed ramp.py
rust         15245  mitosys 14769, model 353, realm 99, shared 23, infra 1
writing       1790  mitosys 1235, model 283, infra 104, shared 99, realm 69
shell           42  mitosys 26, shared 6, model 4, infra 3, realm 3
testing         20  mitosys 10, model 8, realm 2
node            16  model 16
python          10  mitosys 9, model 1
ci               9  realm 3, mitosys 2, model 2, shared 2
docker           8  infra 2, mitosys 2, realm 2, shared 2
go               3  mitosys 3
need: 9 jobs

spec02: exit 0
PASS  a plain board counts its own tree: 30 (got 30)
PASS  a plain board's why is the marker list, not a member credit (got  *.rs×30)
PASS  the second member counts its own 12 (got 12)
PASS  the master sums 30+12+its own 1 = 43 (got 43)
PASS  the master's row credits member a (got  a 30, b 12, top 1)
PASS  the master's row credits its own tree as one more member
PASS  the master's row is a member credit, not a marker list
PASS  the master's credits are loudest member first
PASS  one member's 15 .md stays under writing's floor on its own
PASS  the floor lands on the sum: 35 over two members that each fall short
PASS  a master under a master reaches the grandchildren: 43 (got 43)
PASS  a members cycle terminates and counts each repo once: 8 (got 8)
PASS  board_words unions a member's PRD titles (got MEMBER OWN)
PASS  board_words keeps the master's own PRD titles in that union
PASS  a master's fork names the member that asked (got: a 30, b 12, top 1 ask for rust)
PASS  a master's fork does not say "The tree"
PASS  a plain board's fork still says "The tree" (got: The tree asks for rust (*.rs×30))
the invariant exits 1 against the committed ramp.py
memos.py check exit 0:
(silent)
index.py check exit 1:
resources/board/lanes.py is on disk with no row in references/files.md
index.py check names no path in this spec's footprint
