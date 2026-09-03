# every documented command exists — implementer report

Verdict: DONE

22 of 22 acceptance boxes closed — spec01 9/9, spec02 6/6, spec03 7/7. Every
box was ticked against output quoted below; none was ticked from reading.

Work landed in the lane
`/Users/feb/dev/infra/pearde/.pearde/.lanes/the-doctor-refuses-drift-every-documented-command-exists`
on branch `lane/the-doctor-refuses-drift-every-documented-command-exists`.
Nine files: `resources/claims.py` (new, staged), `resources/board/init.py`,
`resources/doctor.sh`, `references/archive.md`, `references/settings.md`,
`references/parts/contract.md`, `references/parts/doctor.md`,
`references/files.md`, `index.md`.

The row works. Clean, it reads:

```
  claims      ok      45 commands · 45 keys · every name a document uses exists
```

Dirty — which is the tree's real state today, and what the PRD asked for — it
reads six drifted names, each `file:line`, with the two-repair fix line.


## What was already there, and what this run added

The tree carried the probe's uncommitted build: `resources/claims.py` whole,
`init.py`'s two registries, and `doctor.sh`'s row. That was pass one. This run
fixed one defect in it and finished the three specs' remaining work.

**The defect: `_registry` swallowed the rest of `init.py`.** It looked for the
tuple's closing paren with `^\)` and then with `\)\s*$`. Neither ends either
tuple — `DEFAULTS` ends on `("happiness", "0"))` and `SETTING_KEYS` on
`"machine-ceiling")` — so the non-greedy `.*?` ran on to the next line in the
file that happened to start with `)`, and every quoted lowercase word in
between was read as a settings key. `claims.py keys` printed 142 lines, 80 of
them "settings", including `rev-parse`, `pgrep`, `obsidian-local-rest-api` and
`git`. A registry that permissive is a check that passes anything.

Replaced with a paren count, which is what the shape actually needs:

```python
    m = re.search(r"^%s\s*=\s*\(" % name, src, re.M)
    if not m:
        return set()
    i, depth = m.end(), 1
    while i < len(src) and depth:
        depth += (src[i] == "(") - (src[i] == ")")
        i += 1
    return set(re.findall(r'["\']([a-z][a-z0-9-]*)["\']', src[m.end():i - 1]))
```

`keys` now prints 45 lines: 23 settings, 22 frontmatter. The reported misses
did not change — the over-match was luck, not cover.

Then: spec02's three `<!-- claims: ignore -->` markers, and spec03's three map
and prose edits.


## Spec01 — the checker

```
$ python3 resources/claims.py verbs | wc -l
45
$ python3 resources/claims.py keys | wc -l
45        # 23 settings + 22 frontmatter
$ python3 resources/claims.py check .pearde ; echo exit=$?
references/parts/view.md:51: `pearde report` — no such command
references/skills/pearde.md:3: `pearde once` — no such command
references/skills/pearde.md:3: `pearde master` — no such command
references/parts/commits.md:223: `commits:` — no settings key of that name
resources/board/mapfile.py:201: memo `done-counts-which-boxes` — no such memo on this board
resources/board/prdfile.py:347: memo `done-counts-which-boxes` — no such memo on this board
exit=1
```

Clean, it prints nothing and exits 0 — shown under spec03 below, where the six
were temporarily resolved to render the `ok` row.

**Plant, ignore, restore.** Each file was backed up and restored with `cp`, not
`git checkout` — `git stash` is refused in this lane by
`.pearde/memos/no-destructive-git-runs-in-a-tree-the-session-does-not-own.md`,
and a copy proves the same thing without the risk.

```
base=6
planted=7        references/parts/doctor.md:224: `pearde frobnicate` — no such command
ignored=7        (the marked line reports nothing; the earlier plant still does)
restored=6
```

**The two other claims, one line each.** Planting `` `frobnicate: off` ``
beside a mention of `settings.md`, and `.pearde/memos/no-such-memo-at-all.md`
in a `.py`, took the count 6 → 8 and added exactly:

```
references/settings.md:92: `frobnicate:` — no settings key of that name
resources/questions.py:603: memo `no-such-memo-at-all` — no such memo on this board
```

**Prose is not a claim.** A planted sentence carrying four unbackticked prose
forms — "the pearde board", "whether pearde is up to date", "pearde already
ships", "pearde frobnicate as prose" — left the count at 6 and reported nothing
in that file.

**A citation wraps.** `resources/board/refuse.py` cites the shared-checkout
memo twice, once wrapped in prose (lines 10-11) and once across a Python string
concatenation (lines 341-342). Neither is reported. A planted wrapped slug
naming no memo is:

```
resources/questions.py:604: memo `a-wrapped-slug-that-names-nothing-at-all` — no such memo on this board
```

reported at 604, the line the slug starts on, not the line it ends on.

`claims.py` imports `common` and `memos as memoslib` and defines no
`read_text`, `find_board` or `scan` of its own.


## Spec02 — the registry

```
$ python3 -c "... assert d<=set(init.SETTING_KEYS) ..."
23 settings 22 frontmatter; DEFAULTS subset ok
```

Every one of the 23 `SETTING_KEYS` is named in `references/settings.md`; the
only names in that file absent from the tuple are `claim` (frontmatter, and
`bad_keys` skips a frontmatter key in the settings branch) and `persona`, which
is the deliberate non-key. `FRONTMATTER_KEYS` covers contract.md's `prd.md` and
`specNN.md` tables plus `vision:`/`terminals:`/`edges:` as `board.md` and
`order.md` name them.

`pearde init` is unchanged — `DEFAULTS` is still read at exactly one place
(`init.py:199`), and a fresh board still opens with the same six pairs:

```
language: English / workers: 0 / pipeline: 0 / weight-default: 50 / gantt-day: 8h / happiness: 0
```

The three deliberate mentions each carry exactly one marker
(`grep -c` → `archive.md:1  contract.md:1  settings.md:1`):

- `references/archive.md` — the rejected `pearde archive`, marked on the table row
- `references/settings.md` — the paragraph saying there is deliberately no `persona:` key
- `references/parts/contract.md` — the `time:` nesting example, with the bullet reflowed so the marker sits at a sentence end rather than mid-wrap

With those marked, `check` reports exactly the six real drifts spec02 names.


## Spec03 — the row and the map

Placed between `index` and `statusline`:

```
  index       broken  4 problems
  claims      ok      45 commands · 45 keys · every name a document uses exists
  statusline  ok      ~/dev/infra/pearde main *2 ↑7
```

That `ok` was rendered by temporarily resolving the six drifts (rename in
`view.md` and `pearde.md`, a marker on `commits.md:223`, an existing slug in
`mapfile.py`/`prdfile.py`), then restoring every file by copy. `check` exited 0
during that window. The dirty row is quoted at the top of this report.

Without python3 on `PATH` (a `PATH` holding symlinks to the other tools and no
python3), the row degrades the same way `index` does:

```
  index       broken  index.md present, no python3 to read it
                      fix: install python3 — index.py is the only reader of the format
  claims      broken  references/ present, no python3 to read it
                      fix: install python3 — claims.py is the only reader of these three claims
```

The row goes through `row`, which is what sets `BROKEN=1` and so doctor's exit.
The `doctor.sh` diff removes no line (`git diff HEAD | grep -c '^-[^-]'` → 0)
and its four new variables — `CPROBLEMS`, `NCV`, `NCK`, `NC` — occur only
inside the new block, so no other row's text can move.

`resources/claims.py` has its row in `references/files.md` and sits in
`index.md`'s `@@doctor` scope; `index.py check` says nothing about it.
`references/parts/doctor.md` gains a table row and a section naming the three
claims, the one direction, and the `<!-- claims: ignore -->` escape.

The sibling PRD `one-primitive-one-definition` had not landed its rows in these
three files, so there was nothing to rebase onto.


## The gate

The board's gate is `index.py check`, `memos.py check` and `doctor.sh` green.
It is red, and it was red before this PRD — every failure below predates this
work and lies outside this footprint, so each is reported rather than fixed.

- `index.py check` — 4 problems, unchanged by this run and none of them
  `claims.py`. `resources/common.py` is on disk with no row in
  `references/files.md`; `references/files.md` and `@@view` both still name
  `@resources/board/hotreload-test.js`, which is not on disk;
  `references/parts/commits.md` references a memo path that does not resolve.
  Confirmed pre-existing: `git show HEAD:references/files.md` has no
  `common.py` row and does list `hotreload-test.js`.
- `memos.py check` — 43 problems, every one a missing generated `tags:` plus a
  stale kind index. `memos.py retag` and `memo index` are the named repairs.
  Untouched by this run.
- `doctor.sh` — broken on `origin` (6 derived PRDs with no `from:`), `vault`,
  `memos`, `workflows`, `index`, and now `claims`. The `claims` row being
  broken is this PRD's stated intent: its **Done means** says today's known
  misses are reported until fixed.


## Defects outside scope

1. **`verbs()` degrades silently when any module under `resources/` fails to
   import.** Found by accident: a plant that left `resources/questions.py`
   syntactically invalid made `cli.discover()` return almost nothing, and the
   `claims` row went from 6 misses to about 120 — every real command in the
   tree reported as no such command. The row then names a hundred wrong causes
   instead of the one right one, which is the shape
   `.pearde/memos/a-crashing-checker-reads-as-a-failing-check.md` warns about.
   No acceptance box covers it and it is not in this PRD's contract, so it is
   reported. The fix is small: have `verbs()` raise, or have the row read
   `broken` naming the module that would not import, rather than trusting a
   short `discover()`.

2. **`bad_memos` has no `<!-- claims: ignore -->` escape.** `exempt()` is
   applied in `bad_verbs` and `bad_keys` only. A `.py` file citing a memo on
   purpose that does not exist — an example of drift in a docstring — cannot be
   marked, only renamed. No spec asked for it; noted because the fix line
   promises the escape without qualifying which of the three claims it reaches.

3. **The PRD's *Done means* names files that have moved.** It cites `plan.py`
   for the `done-counts-which-boxes` citation and `handles.md` for
   `master <path>`; the tree today has those in `mapfile.py`/`prdfile.py` and
   `references/skills/pearde.md`. Spec02 names the current files and is what
   was implemented. Nothing was edited in `prd.md`.


## Health

The brief listed no file in this footprint under the health floor, and none was
added. `resources/claims.py` is 260 lines with no function over 25.


## Grammar and knowledge

No word in the contract was unknown, and none needed coining. Nothing was
learned outside this repo, so `knowledge.py remember` had nothing to write.
