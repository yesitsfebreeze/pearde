# Report — apply-the-prds-rename-table

Verdict: **DONE**. Five of five acceptance boxes ticked in
`specs/spec01.md` with quoted output.

## Roots

| root | repo | what it holds |
|---|---|---|
| `/Users/feb/dev/infra/pearde` | outer | every footprint path — `references/`, `resources/`, `README.md`, `index.md`. Every edit landed here |
| `/Users/feb/dev/infra/pearde/.pearde` | board | the PRD tree. Only `specs/spec01.md` and this file were written |

## What this pass did

Pass one (the analyst's) had already written the rename. This pass verified
it, found six table-rule matches left unconverted, fixed them, and closed the
boxes.

| file | lines | was | now |
|---|---|---|---|
| `references/archive.md` | 65, 82 | `git rm -r prds/<name>` / `<parent>` | `.pearde/prds/…` |
| `references/archive.md` | 70, 96 | `git log --follow -- prds/<name>` | `.pearde/prds/<name>` |
| `references/obsidian.md` | 78 | `prds/memos`, `prds/workflows` | `.pearde/memos`, `.pearde/workflows` |

All six were table rules the pass-one script missed for want of a trailing
slash. The four in `archive.md` sat inside code blocks whose neighbouring
line already read `.pearde/prds/` — `git rm -r prds/<name>` would not have
resolved.

## Numbers

| measure | value |
|---|---|
| `prds/` lines, in-scope (the 80 files), at HEAD | 221 |
| `prds/` lines, in-scope, now | 76 |
| `prds/` lines, whole-tree grep as the spec writes it | 297 -> 152 |
| unconverted `prds/` tokens left in scope | 45 — 36 bare, 9 named exceptions |
| `git diff --stat` | 49 files, 211 insertions, 211 deletions — 1-for-1 |
| `python3 -m py_compile` | 9/9 OK |
| `bash -n` | 2/2 OK |
| `.pearde/.pearde` or `prds/prds` introduced | 0 |
| `python3 resources/index.py check` | one line, pre-existing (see Findings) |

The 45 remaining tokens: 36 bare `prds/` (the sibling PRD
`resolve-bare-board-path-mentions`), 3 `<prds/>` template tokens, 2
`prds/knowledge` in `doctor.sh`'s comment and message, 2 `prds/*` in
`guard.py`'s `WALKS` comment and `guard.md`'s mirroring row, 1
`prds/{local}` in `brief.py`, 1 `prds/<path>` in `commits.md`.

## Gate

`bash resources/doctor.sh` reports six broken rows: `skills`, `index`,
`guard`, `members`, `vision`, `questions`. Every one is pre-existing and
none is touched by this PRD — `resources/doctor.sh` and `resources/guard.py`
each carry exactly one changed line in this diff, neither of them a check.

## Findings — not fixed, out of scope

Each is behaviour, and the parent PRD's scope is prose.

- **`doctor.sh`'s `skills` row is broken by the `skills/` move.** Line 69
  globs `"$SKILL_ROOT"/skills/*.md`; the directory is now
  `references/skills/`. `doctor` prints `skills broken — skills/ holds no
  .md file — there is nothing to install`. The parent PRD says `install.sh`
  was already repointed for both moves; `doctor.sh` was not. This is the
  clearest live consequence of the move and wants its own PRD.
- **`resources/board/knowledge/**` and `resources/board/obsidian/**` still
  name `prds/knowledge/`** — 43 occurrences across `Dashboard.md`,
  `sources/_index.md`, `conclusions/_index.md`, `graph.json`, `app.json`.
  They are executed Dataview `FROM` clauses and Obsidian query/exclude
  paths, not prose, and the parent PRD scopes `resources/board/` to
  `{brief,collect,specs,view.js}` — so they are outside the 80 scoped files
  and account for the whole gap between the in-scope count (76) and the
  spec's whole-tree grep (152). The vault is now `.pearde/wiki/`; every one
  of these queries returns nothing. A real defect, and its own PRD.
- **Board paths still tested as literal `prds`.** `resources/guard.py`'s
  `board_of()`, `resources/index.py`'s `board()`, and `doctor.sh`'s board
  walk (`"$d/prds"`) all test the pre-move name, and `doctor.sh`'s knowledge
  check looks for `$BOARD/knowledge`, not `wiki`. Their describing prose was
  deliberately left unrenamed — `guard.py`'s `WALKS` comment,
  `references/parts/guard.md`'s mirroring row, `doctor.sh`'s knowledge-row
  lines — because renaming a comment while the code it describes still runs
  on the old path makes the document wrong, not right.
- **`resources/board/brief.py:310`** still emits `"<probe>":
  f"prds/{local}/probe/"` — executable code, excluded by the PRD's Python
  scope. A dispatched worker's `<probe>` line therefore still reads
  `prds/<prd>/probe/`.
- **`references/parts/commits.md:101`, `prd: prds/<path>`** — left as-is, and
  it is the one remaining token that is a judgement call rather than a rule.
  `collect.py:715` computes `relpath(prd["dir"], planlib.repo_root(prd["dir"]))`.
  On this checkout `.pearde` is its own git repo, so the trailer really does
  read `prds/<path>`; on a board that is not its own repo it reads
  `.pearde/prds/<path>`. The document cannot be right for both. That is a
  decision about `collect.py`, not a rename.
- **`<prds/>` (`brief.py:346`, `workers.md` 83 and 279)** is a literal
  template token name, not a path. Correct as written.
- **`references/archive.md` has no row in `references/files.md`** — the one
  line `index.py check` still prints. Pre-existing and unrelated: `git show
  HEAD:references/files.md | grep archive` exits 1.

## Scores

complexity: 12
blast-radius: low
workflow: none fit
