---
state: open
origin: requested
priority: 40
complexity: 0
blast-radius:
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

- [ ] `needs()` reads `members:` and unions each member's `tracked(repo_of(m))`
      and `manifest_text`, the master's own repo included
- [ ] `board_words()` unions each member's `prds/` titles
- [ ] `need` / `gap` / `ramp` print per-job counts that add up to the union,
      and a master's row says which members contributed
- [ ] a plain board's numbers are unchanged — the same three jobs, the same
      counts, on a member board scanned directly
- [ ] the master board's `ramp need` reports rust in the thousands, not 1

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
