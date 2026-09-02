# The ramp

Before a pass touches a PRD, one question: **is this machine tooled for this
repo at all.** A board driving a Rust tree with no Rust skill installed works,
and works worse than it had to, for as long as nobody looks. The ramp is the
looking, and it happens once — not once a pass.

`python3 @resources/pearde.py ramp` is loop step 0. It reads one key.

## happiness

```yaml
happiness: 0
```

`.pearde/settings.md`, `0` when the file does not carry it —
@references/settings.md. Non-zero is **a person saying the toolbox is good
enough**, and the gate prints one line and gets out of the way:

```
ramp: happy 1 — skipped (`pearde ramp happy 0` reopens it)
```

Zero means it was never settled, or a person reopened it. Then the gate owes
the user a proposal before step 1, and it repeats — every pass, until the
answer comes back **yes** and `pearde ramp happy 1` is written. That is the
whole loop the value exists for: *zero, propose, install, ask, until happy.*

Nobody but a person writes a non-zero value. A pass that decides on its own
that the toolbox is fine has answered the one question it was not asked.

## The three lists

| list | what |
|---|---|
| **need** | a job the tree or the board asks for. A `Cargo.toml` asks for rust; a hundred markdown files ask for writing; a board of Vue PRDs asks for Vue before a dependency does |
| **have** | every skill this machine offers *this* repo — the project's `.claude/skills/`, `CLAUDE_CONFIG_DIR`'s, the user's, and the skills inside installed plugins. A flat set of `skill-*.md` files counts the same as a folder holding a `SKILL.md` |
| **gap** | a need whose words no installed skill's name or description mentions |

`ramp need`, `ramp have`, `ramp gap` print them; each answers on its own and
changes nothing. The signal count is how loudly the tree asks — file markers,
manifest dependencies, and PRD titles, the last weighted double because a
board says what is *coming* and the tree only says what is already there.

**The `JOBS` table in @resources/board/ramp.py is the knob**, the way
`buckets.txt` is scout's. A job nothing marks never reaches a gap, and a job
whose keyword is somebody else's word — `workflow` on this board — raises a
gap that is not one. Keywords stay specific; the floors under the common
markers (`*.md`, `*.sh`) keep one stray file from asking for anything.

## Where the candidates come from

Discovery is scout's, always — @resources/scout/README.md. The ramp holds the
*fit*, and calls two routes for the rest:

- `skills` — the skills.sh directory, **ranked by installs**. One skill per
  row, installable by name. The leaderboard carries no description, so the
  route matches the name first and then reads the description off each
  skill's own page, bounded to the top rows by installs — a job word finds
  `tdd` under *test-driven development* rather than only what is named for
  the job. The gate holds that pass at `SCOUT_DEPTH=20` because it calls the
  route once per word.
- `skillrepo` / `gh` — a whole repository, **ranked by stars**. A source to
  enumerate, not a skill to install, so its line is `-l`, which lists and
  writes nothing.

Two axes, because one is an opinion — scout's own rule, and it holds here for
the same reason. Installs say a skill is used; stars say a repo is liked; a
repo with stars and no installs is a reading list, not a dependency.

## It proposes; the user picks

The gate writes `.pearde/.state/ask.md` — one fork per gap job, each carrying
its candidates with the exact `npx skills add …` line, plus **none**, plus a
last fork asking whether the toolbox is now good enough. The pass hands back
`ASK`, the dispatcher puts it, the user's picks are theirs to run.

**The ramp installs nothing.** A gate that wrote to the machine would be a
sweep with a shell, and the machine is not the board's to write — the board's
own writes stop at `.pearde/`, per
@resources/invariants/every-artifact-lands-inside-the-board.sh. What comes
back from the user is the decision; a person runs it, or says to.

A gap with no candidates is said plainly and closes nothing:

```
ramp: 2 gaps, no candidates — the routes answered nothing;
      `pearde ramp happy 1` closes the gate anyway
```

That is not a failure. A field with no published skill is a field where the
board works without one, and the person is the only one who can say so.
