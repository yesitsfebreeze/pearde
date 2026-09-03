# Archive

A `done` PRD moves to `.pearde/prds/archive/` as one flat file, so `scan` stops
walking it. `state: done` keeps its meaning; only the file moves.

```
.pearde/prds/archive/
    <name>.md             a former top-level PRD, flattened
    <parent>--<child>.md  a former child PRD, flattened, parent-prefixed
```

Flat, no nesting — the shape of `.pearde/memos/` (@references/memo.md). The file
is `prd.md`'s frontmatter, title and body unchanged. No `archived_at:`, no new
key — nothing reads the directory back.

## Why `scan` already ignores it

`_scan_one` (@resources/board/registry.py) finds a PRD by one test: `"prd.md" in
files`. `.pearde/memos/` and `.pearde/workflows/` are invisible for the same
reason (@references/parts/board.md) — they hold no file named `prd.md`. Every
file in the archive is `<name>.md`, never `prd.md`. So no name joins
`dirs[:] = [d for d in dirs if d not in ("specs",)]`.

The shape has to be a flat file. `.pearde/prds/archive/<name>/prd.md` matches the
same test, and the walk and the count go on including it.

An archived PRD is not counted in the progress line, not offered to `claim`,
not walked by `doctor`'s census. Twenty archived PRDs are twenty fewer
directories `scan` opens per pass.

## What is eligible

| PRD | rule |
|---|---|
| `state: done` | eligible once its commit has landed and nothing live needs it |
| `superseded` | kept at top level for its evidence — `probe-code-lives-in-the-prd-folder`, `snapshots-fold-to-one-row`; archive only when whoever wrote it judges the evidence no longer needs the visibility |
| parked — `deferred`, or any spelling @references/parts/states.md calls "the user's own" | never; `release <prd> open` reads the very file a move would take (`a-parked-prd-comes-back`) |

Check for a live `needs:` or `footprint:` first:

```
grep -rl '<name>' .pearde/prds/*/prd.md .pearde/prds/*/*/prd.md
```

Rarely fires — `dispatchable` already requires every `needs:` to be `done`
(@references/parts/states.md) — but a stale mention dangles silently.

## Moving one

A leaf:

```
git mv .pearde/prds/<name>/prd.md .pearde/prds/archive/<name>.md
git rm -r .pearde/prds/<name>
```

`specs/` goes with it. A done PRD's specs are history `scan` never reads back
(`resources/board/plan.py`, "boxes for live PRDs only"), and the whole tree
survives at `git log --follow -- .pearde/prds/<name>` up to the `git rm` — the
same tool `plan.py` reaches for when a done PRD's `done_at` is wanted and not
worth a stat-cheap read on every rebuild.

A container whose children are all `done` and `collect`ed — bottom-up, so
`.pearde/prds/archive/` never collides on a bare child name:

```
git mv .pearde/prds/<parent>/<child>/prd.md .pearde/prds/archive/<parent>--<child>.md
git rm -r .pearde/prds/<parent>/<child>
# … repeat per child, then the parent itself:
git mv .pearde/prds/<parent>/prd.md .pearde/prds/archive/<parent>.md
git rm -r .pearde/prds/<parent>
```

## When

By hand, alongside a `doctor` pass, never on every `collect`. A PRD that just
landed is what a fresh commit message points at — leave it at top level for a
few days. Two `git` calls are the whole mechanism; no command wraps them.

## Finding one again

```
grep -l <name> .pearde/prds/archive/*.md
git log --follow -- .pearde/prds/<name>
```

## Rejected

| rejected | why |
|---|---|
| A `pearde archive` command | the board's idiom for a directory `scan` ignores is a naming trick, not an entry in `plan.py`'s prune list — `memos/` and `workflows/` prove the shape. Script the two `git` calls once running them by hand gets old |
| Moving the whole directory, `prd.md` and all | still matches `"prd.md" in files` — `scan` keeps walking, `doctor`'s count holds, and the walk cost is unfixed |
| A tenth `state:` meaning, `state: archived` | still a live directory under `.pearde/prds/` — the walk cost is the size of `.pearde/prds/`, not the spelling of `state:` |
| Deleting done PRDs | out of scope by instruction, and against practice — `superseded` PRDs are kept for their evidence |
