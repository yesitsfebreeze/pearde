---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
---

# resources are organised by responsibility

The user's ask, 2026-09-02: *"then also add a prd to organize the resources
better right now they are jumbled up we need a clean simple responsability and
if possible no node_modules required"*

## The mess, as it stands

`resources/` holds three unlike things at one level:

- the dispatcher, `pearde.py`;
- eight loose feature scripts beside it — `memos.py`, `workflows.py`,
  `grammar.py`, `health.py`, `questions.py`, `guard.py`, `index.py`, and the
  three shell scripts `doctor.sh`, `install.sh`, `update.sh`;
- three tool folders — `board/`, `scout/`, `graph/`.

`board/` is the worst of it: roughly nineteen Python modules, the view's
`view.css` and `view.js`, a vendored `lit-core.min.js`, `viewtest.js`,
`hotreload-test.js`, `package.json`, `package-lock.json`, `node_modules/`, and
four data and child folders — `adapters/`, `example/`, `knowledge/`,
`obsidian/` — all in one directory.

@index.md already states the rule this PRD is asking to be made true: markdown
someone reads lives under `references/`, anything executed lives under
`resources/`, whole, and a tool's own README ships inside the tool. It says
nothing about how `resources/` divides internally. That silence is the gap.

## What exists when this is done

Every file under `resources/` sits in a directory whose name says what the
files in it are responsible for, and a person opening `resources/` can say
what each entry is for without opening it. Node is required for nothing a
person runs by hand, or the one thing that still needs it says so where they
will read it.

## What must not change

- `pearde <cmd>` stays the whole shell surface — @references/install.md.
- `COMMANDS` discovery keeps working from wherever the modules land. It walks
  `resources/board/*.py` today, so moving a file changes discovery.
- Every moved file gets its row rewritten in @references/files.md, and every
  `@@` scope it changed in @index.md. The `index` doctor row is the gate that
  proves it.
- `resources/doctor.sh`, `resources/memos.py check` and `resources/index.py
  check` stay green throughout.

## Sequencing

This touches nearly every file under `resources/` — the widest footprint any
PRD on this board can have. It runs when nothing else is in flight, and its
children are cut so that siblings own disjoint directories.

## Open forks

Four, all of them the user's, none answerable by building. They are in
`## Questions` below once the drill is put.

## Questions

### Q1: How the code is divided up

You are choosing how the files that run this tool get grouped: by which of the
three tools each one belongs to, by what each one is responsible for, or by
which typed command it answers. Whichever you pick is what someone sees when
they open the folder, and it is expensive to change twice?

1. **By responsibility** — grouped by what they do: reading the plan, changing it, drawing it, launching things. (recommended)
2. **By tool** — the three tools each keep a folder of their own, and the loose scripts move inside whichever one owns them.
3. **By command** — one file per command you can type, so the folder reads like the list of things the tool does.

<!-- for the board: resources/ top level; pearde.py COMMANDS discovery walks resources/board/*.py, so any move touches it -->

### Q2: How deep the tidy goes

The largest file in the project does several unrelated jobs at once, so moving
folders around it would leave the real tangle exactly where it is. Breaking it
apart is most of the work here and most of the risk?

1. **Break it apart too** — the tidy is real rather than cosmetic. Slower, and more can break on the way. (recommended)
2. **Leave it whole for now** — folders get tidy quickly and safely, and the biggest file stays a job for later.
3. **Only where it is already two things** — the parts that clearly stand alone come out, the rest is left.

<!-- for the board: resources/board/plan.py — scan, parse cache, schedule, lanes and several commands in one module -->

### Q3: The downloaded dependency

You asked for no downloaded dependencies if it can be avoided. One downloaded
piece is used to draw the page you look at, and two more exist only to test
that the page still looks right; dropping all of it means rewriting those
tests?

1. **Keep a copy of the one drawing piece, drop the rest** — nothing is downloaded to use it, and the page tests become optional. (recommended)
2. **Drop all of it** — the page tests are rewritten in the same language as everything else. More work now, nothing downloaded ever.
3. **Keep it and say so** — nothing is rewritten, and the health check states plainly that the page tests need an extra install.

<!-- for the board: resources/board/lit-core.min.js vendored, viewtest.js and hotreload-test.js, package.json/package-lock.json/node_modules; doctor's jstests row -->

## Answers

**Q1** *(answered 2026-09-02 17:58)* — By responsibility — grouped by what they do: reading the plan, changing it, drawing it, launching things.

**Q2** *(answered 2026-09-02 17:58)* — Break it apart too — the tidy is real rather than cosmetic, accepting it is slower and more can break on the way. plan.py is to be split, not just moved.

**Q3** *(answered 2026-09-02 17:58)* — Keep a copy of the one drawing piece, drop the rest — vendor lit-core, nothing downloaded to use it, and the page tests become optional.

## Children

| child | contract | needs |
|---|---|---|
| `every-module-finds-its-siblings-by-one-rule` | One file puts every directory under `resources/` on the import path, one probe finds the repo root by `resources/pearde.py`, discovery walks every directory under `resources/`, and every tool that launches a sibling script finds it rather than spelling `board/` — so a file can move with no second edit anywhere; nothing has moved yet | — |
| `the-largest-module-is-cut-by-responsibility` | resources/board/plan.py` is several modules beside each other, each named for one thing it is responsible for and none over 700 lines, with every command, caller and harness unchanged from the outside | — |
| `every-file-sits-under-what-it-is-responsible-for` | Every file under `resources/` sits in a directory named for what the files in it are responsible for, the manifest and the map and the prose and the board's 51 harnesses all name the new paths, nothing is downloaded to run or draw the board, and `index.py check` and `doctor.sh` are green | every-module-finds-its-siblings-by-one-rule, the-largest-module-is-cut-by-responsibility |
