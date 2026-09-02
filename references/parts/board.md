# The board

The layout the scan walks and the progress line counts.

```
prds/
  settings.md       # board settings — @references/settings.md
  vision.md         # where the board is going — @references/templates/vision.md
  memos/            # decision records — @references/memo.md
    <slug>.md
  workflows/        # how a kind of job is done — @references/workflow.md
    <slug>.md
  <prd-name>/
    prd.md          # frontmatter state + the request
    specs/          # analyst-written, one implementable unit per file
      spec-<name>.md
    <child-prd>/    # a sub-PRD from refine
      prd.md
```

- A directory holding `prd.md` is a PRD. A subdirectory holding its own is a
  child PRD.
- `specs/`, `memos/` and `workflows/` hold no `prd.md`, so scan walks past
  all three.
- `vision.md` is one file beside `settings.md`, not a PRD: `vision:` in one
  sentence, `terminals:` naming the PRDs whose completion is it, `edges:` for
  a dependency nobody wrote as `needs:`. How the plan reads it is
  @references/parts/order.md.
- A parent with children is **not dispatchable** until every child is `done`:
  work flows to the leaves. What that gate tests exactly — leaf, container,
  parked child, `needs:`, footprint, `workflow:` — is one function,
  `plan.dispatchable`, and it is written out once, under **The command is the
  gate** in @references/parts/states.md. `scan`'s ready band and `claim` both
  read that one function, so what the scan offers is what `claim` takes.

## Where the board is

The board is one directory at the project root, and it is called `pearde/`.
The name has no dot because Obsidian skips every path holding a dot-segment
before a setting is read, so a hidden board can never appear in a vault at
the project root — and the vault has to root at the project, or the project
is invisible from the board. `.pearde/` survives as the legacy name, and as
the relative compatibility symlink `pearde upgrade` leaves behind, so every
path spelled the old way keeps resolving. @references/obsidian.md is the
mechanism.

`pearde` is an ordinary word, though, and one project cannot have it: this
repo's own checkout sits at `infra/pearde`, beside the `infra` board, and the
name is taken. So the board's directory name is **configurable**, and the way
it is configured is that the board says which directory it is:

1. `<project>/pearde/` when it carries a board — `settings.md`, or a `prds/`.
2. `<project>/.pearde/` when only that does, read **through** the symlink: a
   compat link's name is not the board's name, and handing back `.pearde/…`
   would write the board's own wikilinks where the vault cannot see them.
3. otherwise the one immediate child of the project holding `settings.md`.
   `/Users/feb/dev/infra` calls its board `board/` and is found this way.
4. and when there is none, `<project>/pearde/` — the path `pearde init`
   creates.

Two children carrying `settings.md` is not a board to choose between. Every
resolver refuses and names both; doctor reports `board broken · two boards in
one project`; the status line drops its board segment rather than guess.

There is no setting for the name, and that is the point. A setting would have
to live in `settings.md`, inside the board a resolver has not found yet. A
marker file at the project root would be a second name for one directory and
a second thing to keep true. An environment variable is one value on a
machine watching nine boards. A key in the project's `.claude/settings.json`
binds this layout to another tool's file and makes seven resolvers — one of
them a shell script — parse JSON on every command. Renaming the directory is
the whole act of configuring it, and nothing can go stale because the name is
written in exactly one place: the directory.

Step 3 asks for `settings.md` and not the `prds/` half: under the two known
names the name itself is corroboration and either marker is enough, but a
directory nothing named must carry the file only a board carries. A repo with
`docs/prds/` in it is not a repo with two boards. It is immediate children
only, one stat each, no dot-directory — this walk runs on every command and
on every ancestor up to the root.

The walk is written seven times on purpose — `plan.py`, `health.py`,
`questions.py`, `memos.py`, `grammar.py`, `guard.py` and the shell one in
`doctor.sh` — each with its own error prefix, so no reader depends on the
planner to find a board and every refusal says which command refused.

`pearde upgrade --dir <name>` is what moves a board out of the hidden name
into one that is free, and `pearde vault --dir <name>` does the same before
seeding a vault. Both leave the `.pearde` symlink pointing at wherever the
board went.
