---
complexity: 12
footprint:
  - references/
  - resources/
  - README.md
  - index.md
---

# spec01 — apply the specific-rule table and fix agents/skills registration

Already done, in the outer repo `/Users/feb/dev/infra/pearde` (prose only, no
behaviour changed): the mechanical rename table from the parent PRD, plus the
extras it names (`.claims/`, `report.md`, `view.user.css`/`.js`, bare
`prds/knowledge`) and the `prds/<name>/` pattern (identifiers, `<placeholder>`
and `{placeholder}` tokens, `*`/`**` globs), across the 80 scoped files
(`references/**/*.md`, `README.md`, `index.md`, `resources/*.sh`,
`resources/*.py`, `resources/board/{brief,collect,specs}.py` + `view.js`).
Also fixed: `agents/`→`references/agents/` and `references/skills/`
registration in `references/files.md` (both the `agents/` section and the
`skills/` section), `index.md` (the `@@workers` row **and** every other
`@skills/…` anchor across its Keywords table, needed for `pearde index check`
to go silent), and `references/parts/workers.md`'s prose. `references/knowledge.md`
also carried one stale `@skills/` anchor, fixed the same way.

Two classes of `prds/` occurrence were deliberately left untouched because
mechanically renaming them would misdescribe code that has NOT itself been
migrated (see the report's Findings — out of scope, behaviour): the `ls
prds/*/prd.md` example in `resources/guard.py`'s `WALKS` comment and in
`references/parts/guard.md`'s mirroring table row (both describe
`guard.py`'s own still-literal `prds/` regex), and the `prds/knowledge/`
mentions in `resources/doctor.sh` around its `$BOARD/knowledge` check (which
still tests the pre-move directory name off a `$BOARD` that is itself found
by a still-literal `prds` walk). `resources/board/brief.py`'s `"<probe>":
f"prds/{local}/probe/"` was also left alone — it is executable code, not a
docstring, and the PRD excludes `resources/board/` Python from scope except
its docstrings/help text.

## Acceptance

- [x] `grep -rn "prds/" references resources *.md | wc -l` is far below the
      measured-before count, and every line it still prints is one of: a
      bare `prds/` (no trailing `/<name>/`), a `<name>`/`<parent>`-style
      placeholder with no trailing slash, or one of the named
      behaviour-coupled exceptions above — never a table-rule or
      `prds/<name>/`-pattern match left unconverted
      — in-scope (the 80 files): **221 lines at HEAD -> 76 now**. Whole-tree
      grep as written: **297 -> 152** (the extra 76 are `resources/board/
      knowledge/**` and `resources/board/obsidian/**`, outside the PRD's
      scoped set — see the report's Findings). The 76 in-scope lines carry
      45 unconverted tokens, and nothing else:

      ```
        36 prds/          bare — the sibling PRD's job
         3 prds/>         the `<prds/>` template token (workers.md x2, brief.py:346)
         2 prds/knowledge doctor.sh:477,483 — named exception
         2 prds/*         guard.py:72 WALKS, guard.md:15 — named exception
         1 prds/{local}   brief.py:310 — named exception, executable code
         1 prds/<path>    commits.md:101 — `prd:` trailer, matches collect.py
      ```

      Pass one had left six table-rule matches unconverted; this pass fixed
      them (`references/archive.md` 65, 70, 82, 96 — `git rm -r prds/<name>`
      / `git log --follow -- prds/<name>` / `git rm -r prds/<parent>`, each
      sitting in a block whose sibling line already read `.pearde/prds/`;
      `references/obsidian.md` 78 — `prds/memos`, `prds/workflows`, both
      table rules missed for want of a trailing slash)
- [x] `python3 resources/index.py check` prints only the pre-existing,
      unrelated `references/archive.md is on disk with no row in
      references/files.md` line — nothing naming `agents/` or `skills/`

      ```
      references/archive.md is on disk with no row in references/files.md
      exit 1
      ```

      Pre-existing confirmed: `git show HEAD:references/files.md | grep
      archive` exits 1 — the row was absent before this PRD too
- [x] every edited `.py` file still compiles: `python3 -m py_compile <file>`

      ```
      OK resources/board/brief.py    OK resources/memos.py
      OK resources/board/collect.py  OK resources/pearde.py
      OK resources/index.py          OK resources/workflows.py
      OK resources/knowledge.py      OK resources/guard.py
                                     OK resources/questions.py
      ```
- [x] every edited `.sh` file still parses: `bash -n <file>`

      ```
      OK doctor.sh
      OK install.sh
      ```
- [x] no occurrence of `.pearde/.pearde` or `prds/prds` was introduced
      (`grep -rn '\.pearde/\.pearde\|prds/prds' references resources *.md`)

      ```
      (no output, exit 1)
      ```

      `git diff --stat` closes at `49 files changed, 211 insertions(+), 211
      deletions(-)` — 1-for-1 throughout, no behaviour touched

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
echo "in-scope prds/ hits: $(grep -rn "prds/" references resources *.md | wc -l)"
python3 resources/index.py check 2>&1 | grep -E 'agents/|skills/' && { echo "FAIL: index check names agents/ or skills/"; exit 1; }
for f in resources/board/brief.py resources/board/collect.py resources/index.py \
         resources/knowledge.py resources/memos.py resources/pearde.py \
         resources/workflows.py resources/guard.py resources/questions.py; do
  python3 -m py_compile "$f" || exit 1
done
bash -n resources/doctor.sh || exit 1
bash -n resources/install.sh || exit 1
grep -rn '\.pearde/\.pearde\|prds/prds' references resources *.md && { echo "FAIL: forbidden token"; exit 1; }
echo "verify: clean"
```
