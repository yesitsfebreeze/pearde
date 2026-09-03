# the-prose-and-the-invariants-say-dot-pearde — analyst report

Verdict: SPECCED

Three specs, complexity 3 + 6 + 8 = 17, over six files of prose and invariants
plus eight modules. The build went through: the whole sweep stands in the lane,
uncommitted, and one invariant that was red in every lane is now green.

Workflow followed: `probe-then-spec`. `correct-a-documented-claim` is the route
the build inside step 3 took, and its `## Use when` fits this contract exactly —
but this pass is an analyst on an `analyzing` PRD, which is what
`probe-then-spec` is for. Both files already exist; neither is a finding.

The record had the answer before the build: `knowledge.py query` returned 90
hits, 90 strong, the top one `[[260901-ee0f]] Every pearde board on this machine
is on the .pearde layout`. No gap enqueued into `.pearde/wiki/pending/`.

## What the build found first

The parent PRD describes a repo that no longer exists. Its **Today** section
says the board is `<project>/pearde/` with `.pearde` a symlink beside it; the
move back landed in `c88a64a` before this pass started, and
`.pearde/memos/the-board-directory-is-pearde-and-the-compat-symlink-is-gone.md`
records it as an invariant with `verify: test -d .pearde -a ! -L .pearde -a ! -e
pearde`. Measured on this checkout: `.pearde` is a real directory and no
`pearde/` exists. So this PRD is not prose written ahead of a move — the move
happened, and the prose is what is behind.

`references/` was already almost entirely dotted. The undotted spellings left
sit in three places: `references/parts/board.md`'s *Where the board is*, the
invariant scripts, and module comments.

## Specs

| spec | goal | complexity |
|---|---|---|
| `specs/spec01.md` | *Where the board is* reads the dotted order, and the pages that copy it agree | 3 |
| `specs/spec02.md` | every invariant finds the dotted board, and exercises it | 6 |
| `specs/spec03.md` | the comments and printed paths outside the resolvers say `.pearde` | 8 |

Union of the footprints, 14 files:

```
references/parts/board.md
references/parts/commits.md
references/parts/guard.md
resources/board/collect.py
resources/board/refuse.py
resources/board/serve.py
resources/board/session.py
resources/board/shared.py
resources/guard.py
resources/knowledge.py
resources/graph/graph.sh
resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
resources/invariants/every-artifact-lands-inside-the-board.sh
resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
```

All three verify blocks were run in the lane and each printed `ok`. `spec01`'s
and `spec02`'s greps were each proved to fail against an injected line asserting
`pearde/` as the board's name.

## The red invariant nobody was seeing

`resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh`
exited **1** in this lane at baseline —

```
BROKEN: no board at pearde/ — the second check has nothing to read
```

It resolves the board beside itself (`dirname $0/../..`). From the checkout that
is the repo root and the board is there; from a lane — a worktree of this repo,
holding an empty `.pearde/` — nothing is. Green from the checkout, red from
every one of the 50 trees a worker actually builds in. It now resolves the
checkout from `git rev-parse --git-common-dir`, asks `.pearde/` before
`pearde/`, and names the path it looked at when it finds none. Green from the
lane and from a fresh worktree.

This is the memo's own last consequence arriving in a script instead of a spec:
*"A verify block that names a board path cannot spell it relative to the cwd: a
worktree of the code repo holds an empty `.pearde/`."*

## The invariant that was testing the wrong layout

`a-board-s-own-file-commits-in-the-board-repo.sh` built its `nested` fixture —
"a code repo that ignores its board, and a board that is its own git repo",
which is this repo's layout — at `<code>/pearde`. It was green, because the
fixture is self-consistent, and it was green about the name the board no longer
uses. The fixture is now `.pearde` throughout: the board directory, the code
repo's `/.pearde` ignore line, the lane probe path, both log needles and the
board-spelled section. Still 20 PASS 0 FAIL, now against the real layout.

## Findings

**1. Three siblings and this PRD overlap on eleven files.** The parent set all
four children `needs: —`, so they run at once, but the comments this contract
owns sit inside the readers the other three rewrite. Measured:

- `the-board-name-is-one-dotted-constant` owns `boards.py`, `common.py`,
  `plan.py`, `health.py`, `questions.py`, `memos.py`, `grammar.py`, `doctor.sh`,
  `statusline.sh`.
- `init-and-upgrade-write-the-dotted-board` owns `init.py`.
- `the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind` owns
  `doctor.sh`'s vault row, `obsidian/app.json`, `knowledge/Dashboard.md`,
  `knowledge/{sources,conclusions}/_index.md`, `references/obsidian.md` and
  `references/parts/statusline.md`'s vault section.

The specs stop at that line, so none of those files is in this PRD's footprint.
The stale comments inside them are listed below, so the sibling that rewrites
each reader rewrites its comment in the same hunk. That is why `spec03` says so
in its body rather than reaching for the file.

**2. Two resolvers still ask the legacy name first.** Not this PRD's to fix —
`the-board-name-is-one-dotted-constant`'s — but both are wrong against
`boards.py BOARD_DIRS`, which is `(".pearde", "pearde")`:

- `resources/doctor.sh:264` — `for n in pearde .pearde`
- `resources/statusline.sh:96` — `if [ -f "$d/pearde/settings.md" ]` before the
  dotted test

On a board carrying both names the two shell readers pick the legacy directory
and every Python reader picks the dotted one, so `doctor` and the status line
report a different board from the one every command works.

**3. `doctor`'s `board broken` fix line moves a board to the undotted name.**
`resources/doctor.sh:379` prints `mkdir -p $OFFROOT/pearde && git mv …` as the
repair for a board found on the old layout, and `:381` says `no board — pearde
init creates pearde/`. Both contradict the invariant memo and the init sibling.
Same owner as finding 2, plus the vault row at `:457`, whose fix line runs
`pearde upgrade` to move the board *back* — which the vault PRD already names in
its own body.

**4. The graphify cache store is keyed on a path no tree holds.**
`shared.py CACHE_KEY` is `"pearde/graphify/cache"`, and the store carries 29 MB
under it (`/Users/feb/dev/infra/pearde/.git/pearde-shared/pearde/graphify/cache`,
measured 2026-09-03). The dotted row is `RETIRED` onto it, so nothing is broken
and `one-copy-per-machine` is 4 PASS 0 FAIL. The cost is the row: applying the
table materialises an undotted `pearde/graphify/` in every tree it reaches, and
**25 of this repo's 50 lanes carry one**. None is board-shaped — no
`settings.md`, no `prds/` — so `is_board_dir` is false and no tree resolves
twice; if one ever gained either marker, that is the double-resolution outage
the memo describes, arriving through the share table. `spec03` reorders the two
rows so the dotted one is listed first and states in the comment why the key
keeps the legacy spelling. Flipping the key itself is a store migration and a
wider contract than this PRD's.

**5. `references/parts/board.md` cannot state where the vault roots.** The page
argued the board's name from Obsidian's behaviour, and the vault contract is
being reversed underneath it right now:
`the-vault-roots-at-the-board-not-the-project` is `superseded` by
`the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`, which roots the
vault at the project and adds `obsidian-unhide` to index the dot. Whichever way
it lands, a vault claim on this page goes stale the day it does. The rewrite
therefore cites `@references/obsidian.md` as the page that settles it and
asserts nothing itself, and `spec01`'s first box holds that line.

**6. Pre-existing, not cleared, not this PRD's.** `python3 resources/index.py
check` printed the same three lines before and after — `resources/common.py`
with no row in `references/files.md`, and `references/files.md` plus `@@view`
naming `resources/board/hotreload-test.js`, deleted in `b1d3f5d`. `doctor` shows
the same six broken rows as at baseline (`index`, `vault`, `origin`, `health`,
`knowledge`, `questions`) and no new one. `prose.py check
references/parts/commits.md` reports 3 unbound waste words at `HEAD` as well as
in the lane.

## Stale comments inside sibling-owned files

Handed over, not fixed. Each says the board is `pearde/`, or that `.pearde` is a
symlink onto it:

| file | lines |
|---|---|
| `resources/doctor.sh` | 256-258, 317, 355-356, 375, 377, 379, 381, 451, 453 |
| `resources/statusline.sh` | 80-82, 290-291 |
| `resources/board/boards.py` | 113 — `board_link` argues from the superseded premise; 184 — `board_named`'s docstring gives the two names in the order the code no longer uses |
| `resources/common.py` | 87 — same docstring, same wrong order |
| `resources/guard.py` | 50, 178, 216 — same |
| `resources/board/init.py` | 7, 23, 69-76, 129, 134, 179, 297-311, 407-420, 589, 822, 994, 1027, 1074, 1082, 1161 |
| `resources/board/knowledge/*.md`, `resources/board/obsidian/app.json` | every Dataview `FROM "pearde/…"` and every ignored-path row — vault-relative, so their spelling follows the vault sibling's answer |

## Harnesses

Baseline and after, both from the lane:

| harness | before | after |
|---|---|---|
| `a-board-s-own-file-commits-in-the-board-repo.sh` | rc 0 · 20 PASS 0 FAIL | rc 0 · 20 PASS 0 FAIL |
| `a-master-need-is-the-union-of-its-members.sh` | rc 0 · 17 PASS 0 FAIL | rc 0 · 17 PASS 0 FAIL |
| `every-artifact-lands-inside-the-board.sh` | rc 0 · 7 PASS 0 FAIL | rc 0 · 7 PASS 0 FAIL |
| `no-colour-group-in-the-vault-preset-is-a-path-query.sh` | **rc 1 · BROKEN** | rc 0 · 8 groups carried |
| `no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` | rc 0 · 6 PASS 0 FAIL | rc 0 · 6 PASS 0 FAIL |
| `one-copy-per-machine-of-what-every-lane-regenerates.sh` | rc 0 · 4 PASS 0 FAIL | rc 0 · 4 PASS 0 FAIL |

`python3 resources/index.py check`: three lines before, the same three after.
`bash resources/doctor.sh`: no row broken that was not broken at baseline.

## Probe

The build is uncommitted in
`/Users/feb/dev/infra/pearde/.pearde/.lanes/the-board-is-a-real-directory-at-pearde-never-a-symlink-the-prose-and-the-invariants-say-dot-pearde`
— 14 files, +128 -100. The implementer continues it; nothing here needs
rebuilding.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
