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
  a dependency nobody wrote as `needs:`. The plan reads it per
  @references/parts/order.md.
- A parent with children is **not dispatchable** until every child is `done`:
  work flows to the leaves. One function, `plan.dispatchable`, tests leaf,
  container, parked child, `needs:`, footprint and `workflow:`, written out
  once under **The command is the gate** in @references/parts/states.md.
  `scan`'s ready band and `claim` both read that function, so what the scan
  offers is what `claim` takes.

## Where the board is

One directory at the project root, called `pearde/`. The name carries no dot:
Obsidian skips every path holding a dot-segment before a setting is read, so a
hidden board never appears in a vault at the project root — and the vault has
to root at the project, or the project is invisible from the board. `.pearde/`
survives as the legacy name, and as the relative compatibility symlink
`pearde upgrade` leaves behind, so every path spelled the old way keeps
resolving.
@references/obsidian.md is the mechanism.

`pearde` is an ordinary word, and one project cannot have it: this repo's own
checkout sits at `infra/pearde`, beside the `infra` board, and the name is
taken. So the board's directory name is **configurable**, and the board
configures it by naming its own directory:

1. `<project>/pearde/` when it carries a board — `settings.md`, or a `prds/`.
2. `<project>/.pearde/` when only that does, read **through** the symlink: a
   compat link's name is not the board's name, and handing back `.pearde/…`
   would write the board's own wikilinks where the vault cannot see them.
3. otherwise the one immediate child of the project holding `settings.md`.
   `/Users/feb/dev/infra` calls its board `board/` and is found this way.
4. and when none does, `<project>/pearde/` — the path `pearde init` creates.

Two children carrying `settings.md` is not a board to choose between. Every
resolver refuses and names both; doctor reports `board broken · two boards in
one project`; the status line drops its board segment rather than guess.

Renaming the directory is the whole act of configuring it: the name lives in
exactly one place, the directory, so nothing goes stale. What each alternative
would cost —

| instead | costs |
|---|---|
| a setting in `settings.md` | lives inside the board a resolver has not found yet |
| a marker file at the project root | a second name for one directory, and a second thing to keep true |
| an environment variable | one value on a machine watching nine boards |
| a key in the project's `.claude/settings.json` | binds this layout to another tool's file, and makes seven resolvers — one of them a shell script — parse JSON on every command |

Step 3 asks for `settings.md` and not the `prds/` half: under the two known
names the name itself corroborates and either marker is enough, but a
directory nothing named must carry the file only a board carries — a repo
holding `docs/prds/` is not a repo with two boards. Immediate children only,
one stat each, no dot-directory: the walk runs on every command and on every
ancestor up to the root.

The walk is written seven times on purpose — `plan.py`, `health.py`,
`questions.py`, `memos.py`, `grammar.py`, `guard.py` and the shell one in
`doctor.sh` — each with its own error prefix, so no reader depends on the
planner to find a board and every refusal says which command refused.

`pearde upgrade --dir <name>` moves a board out of the hidden name into a free
one; `pearde vault --dir <name>` does the same before seeding a
vault. Both leave the `.pearde` symlink pointing at wherever the board went.
