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

One real directory at the project root, called `.pearde/` — every file the
board owns lives under it, and no board file is reachable only through a
symlink. `pearde/` is the legacy name, carried for the day between 2026-09-02
and 2026-09-03 and kept only so a board that has not run `pearde upgrade` still
resolves. The dot cost the board nothing and the undotted name cost two
outages: one board answering to two names fanned every dispatch out twice and
refused every collect. @.pearde/memos/the-board-directory-is-pearde-and-the-compat-symlink-is-gone.md
is the invariant, and where the Obsidian vault roots is @references/obsidian.md's
to say, not this page's.

`pearde` is an ordinary word, and one project cannot have it: this repo's own
checkout sits at `infra/pearde`, beside the `infra` board, and the name is
taken. So the board's directory name is **configurable**, and the board
configures it by naming its own directory:

1. `<project>/.pearde/` when it carries a board — `settings.md`, or a `prds/`.
2. `<project>/pearde/` when only that does — the legacy name, kept so a board
   still on it resolves without a move.
3. otherwise the one immediate child of the project holding `settings.md`.
   `/Users/feb/dev/infra` calls its board `board/` and is found this way.
4. and when none does, `<project>/.pearde/` — the path `pearde init` creates.

Either known name is read **through** a compatibility symlink where one still
stands, on a board upgraded by an older release: a link's name is not the
board's name, and handing the link's spelling back would write the board's own
wikilinks against a path nothing else spells. `pearde` writes no such link any
more — in a checkout the two names are one directory, in a lane they are two
real ones, and one board resolving twice is what the pair cost.

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
one stat each, no dot-directory — the board's own two names are asked by name
in steps 1 and 2, before the scan, and the scan is what skips a dot. The walk
runs on every command and on every ancestor up to the root.

The walk is written eight times on purpose — `plan.py`, `health.py`,
`questions.py`, `memos.py`, `grammar.py`, `guard.py` and the two shell ones,
in `doctor.sh` and `statusline.sh` — each with its own error prefix, so no
reader depends on the planner to find a board and every refusal says which
command refused.

`pearde upgrade` moves a board still at `pearde/` into `.pearde/` — a rename
inside the board's own repo, so its log survives, and it leaves no link behind.
`pearde upgrade --dir <name>` and `pearde vault --dir <name>` move it into a
name of your own instead. Either strands every lane and session worktree under
the old name, so both want `scan` clean and `session reap --apply` done first.
