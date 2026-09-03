# Install

Make five links per skill where your agent looks for skills. Nothing here is
specific to one agent; work out what your setup calls each thing.

## What the system is

Three folders, and the split between them is the whole design.

| folder | holds | who touches it |
|---|---|---|
| `references/skills/` | one `.md` per skill — frontmatter and a short body | an agent, as an entry point |
| `references/` | everything **read**: the workflow, personas, templates, rules | an agent, mid-task |
| `resources/` | everything **run**: the board service, scout, the status line, doctor | a shell, never read for meaning |

A skill file is thin on purpose. Its frontmatter — `name` and `description` —
makes the skill findable and decides when it fires; its body points into
`references/` and stops. The skill is the door, never the knowledge.

**The file name is the command.** `name:` equals the file name, and an install
builds the folder from it, so `references/skills/pearde-view.md` is invoked as
`pearde-view` wherever it lands. Namespace and grouping are spelled into that
one name, `-` separated: `pearde-persona-ask` is namespace `pearde`, group
`persona`, verb `ask`.

**`-` and not `:`.** A skill name is kebab-case — lowercase letters, digits,
hyphens, nothing else. Some agents render a *plugin's* skills as
`plugin:skill`, but a plugin loader puts that colon there, carries exactly one
level with it, and a skill installed as a folder never gets one. A colon in a
name makes the skill fail to load. The prefix is the whole portable namespace.

`@index.md` is the map both `@<path>` and `@@<keyword>` resolve against.

## What installing means

Each file in `references/skills/` reaches your agent's skills directory, copied nowhere.

**The catch:** a skill file says `Read @README.md`, a path relative to the
skill's own folder, which resolves to nothing for a bare `.md` dropped into a
skills directory. So a skill is installed as a *folder* of links:

```
<skills-dir>/<name>/            # <name> is the file name, minus .md
    SKILL.md    -> <repo>/references/skills/<name>.md
    README.md   -> <repo>/README.md
    index.md    -> <repo>/index.md
    references  -> <repo>/references
    resources   -> <repo>/resources
```

Five links, one skill, nothing copied — read through them, every `@<path>` in
the repo resolves as it does here. `@resources/install.sh` builds all of
`references/skills/` in one command:

```bash
bash @resources/install.sh <skills-dir>          # say what it would make
bash @resources/install.sh --apply <skills-dir>  # make it
bash @resources/install.sh --remove <skills-dir> # take it back out
```

- **Two lines.** `--apply` prints `alias pearde='python3 <repo>/resources/pearde.py'` and `export PEARDE_AS=engineer` — add both to your shell yourself. Nothing here writes a shell file. The alias is the one word; every skill file names the same `python3 @resources/pearde.py <cmd>` line, so the alias and the skills are one surface. The export is who is working: every command that moves a PRD records `· as <id>` on its line from that variable and refuses without it, per @references/parts/personas.md — `add` alone files a new PRD `· as engineer (default)`, so the first minute runs before the export is in place. `persona <id>` re-exports it.
- **Links, not copies.** One source of truth — editing this repo updates every
  install at once, where a copy drifts silently. The links run both ways: a
  session on any other board reaches this repo's working tree through them, so
  `@resources/guard.py`, where wired, refuses an `Edit` or `Write` through a
  link from a pass whose board is not this repo's, naming the real path and
  `.pearde/memos/the-install-is-live-symlinks.md`. @references/parts/guard.md
  is the row.
- **Windows** needs Developer Mode or Administrator for a symlink. Without
  one, `ln -s` in Git Bash silently *copies*. Turn it on
  (`MSYS=winsymlinks:nativestrict`), or clone this repo straight into the
  skills directory and let `git pull` be the update path.
- **Something real already sitting where a link goes** is never replaced — it
  may hold someone's edits. Reconcile by hand.

## Finding where the links go

Work down the four in order and stop at the first that holds.

1. **This repo is already inside a skills directory**, under the name of one of
   its own skills. The slot is taken and no folder is built over it — the repo
   *is* that skill. Build the others as siblings.
   - **Then retire the installer.** `@SKILL.md` made this repo invocable before
     any of its skills were, and answers to the same name as
     `references/skills/pearde.md`. Two things called `pearde` is one too many:

     ```bash
     ln -sfn references/skills/pearde.md SKILL.md
     ```

     Relative, so the repo survives a move. The board skill is live under the
     name it shadowed, and `git checkout SKILL.md` brings the installer back. git reports `SKILL.md` as changed from then on — the install, not
     damage.
2. **Your agent has a skills directory.** Make the folders there — the
   machine-wide one for the skills everywhere, the project-local one for here
   only.
   - **Check which configuration is in force first.** An environment variable
     can move an agent's whole configuration directory, a machine can hold
     several profiles, and links written into the wrong one are correct and
     inert. An install present and broken looks exactly like an absent one —
     worth one extra command to avoid.
3. **Your agent reads one instructions file instead** — a single file it loads
   every session, whatever its name. Append `@references/system.md` to it,
   creating the file if absent. The block carries `pearde:begin` /
   `pearde:end` markers, so nothing outside them is read back out. A marker already present
   means installed — leave the block, or replace what lies between the markers
   when the block has changed.
   - **Substitute `<PEARDE>` for this repo's absolute path** as you write it.
     The block goes into a file belonging to some other repo, where a relative
     `@references/...` resolves against *that* tree — silently, into a foreign
     file or into nothing. The placeholder stops exactly that.
4. **Neither.** Nothing is broken. Every skill reads where it lies — point
   yourself at `references/skills/<name>.md` and its `references/` for the whole system.
   A complete install, done by hand each time.

Say which of the four you did, and where. That sentence is the install's only
record.

## The status line

Optional, and separate from any skills directory.

`@resources/statusline.sh` renders `<dir> <branch> · <model>`, plus
`▸pearde <d>/<n> <p>% · open <o> <q>%` when a board is in scope. It walks up
from the working directory to the nearest board and stays silent where none
is, so wiring it globally is safe.

- Input: the status JSON on stdin, or `$PRD_STATUS_JSON`. Output: one line.
- Wire `bash @resources/statusline.sh` wherever your setup runs a command for
  its status line. With no such hook, the same numbers on demand are
  `bash @resources/statusline.sh <<< '{}'`.
- `pearde guard on`, in the repo the board lives in, writes into that repo's
  `.claude/settings.json`: `python3 @resources/guard.py` as a `PreToolUse`
  hook on `Bash|Read` and on `Edit|Write` and a `PostToolUse` hook on
  `Edit|Write`, `python3 @resources/board/serve.py ensure` as a
  `SessionStart` hook so opening a session brings this board's view up, and
  `MAX_THINKING_TOKENS` beside them — every other key kept. `pearde guard
  off` takes exactly those out again. @references/parts/guard.md is the block
  and the reasoning. Optional: the loop runs without the guard, which is the loop's own rules
  made unignorable where a pass is long enough to forget them.
  `doctor` reports it `ok`, `off` or `broken`, its `off` fix line is the
  command, and `pearde guard status` is that row alone.
- **Compose, never overwrite.** An existing status line keeps working — export
  `$PRD_STATUS_JSON` once, call both, join the output. Only the board segment
  is this repo's; drop the dir/branch/model part where the other line has it.
- A settings file is the user's. Print the line to add. Never write it.

## The view

Optional, one command, and the board reads and plans without it. The view is
how a person looks at the board and edits it. Needs Python 3 — no Docker, no
account, one loopback port.

```bash
python3 @resources/board/serve.py ensure   # start the service, register this board
```

It prints the URL: `http://127.0.0.1:8443/board/<name>`. Every registered
board is listed at `/`.

- **One daemon per machine**, singleton by port bind — `ensure` on another
  board registers it with the same service. `PEARDE_PORT` moves the port.
- **Nothing leaves the machine.** It binds `127.0.0.1`, reads the board's
  files, writes the same files back on an edit.
- `@resources/board/serve.py status` says what it watches;
  `@resources/board/serve.py stop` ends it. `@resources/doctor.sh` reports a
  board the service is not watching, and `--fix` registers it.
- Nothing lands outside a board. Each board records its own registration in
  `<board>/.state/serve.json`, the daemon holds the union in memory and logs
  to the `.state/serve.log` of the board that started it, and no machine-wide
  list exists. A daemon stopped and started watches nothing until each board
  is `ensure`d again — which every session start does, from the
  `SessionStart` hook `pearde guard on` writes.
- No service at all: `python3 @resources/board/plan.py gantt --open` writes
  the same render to `.pearde/.state/view.html` as one self-contained file.

## A master board

Optional, nothing to install — a board becomes the parent of several others by
naming them.

```yaml
# <parent-repo>/.pearde/settings.md
members:
  - ../mitosys/prds
  - ../model/prds
```

- The members stay where they are, boards in their own right. The parent gets
  the merged scan, the merged plan, one timeline.
- Run the pass in the parent from then on. `@resources/doctor.sh` grows a
  `members` row, and the status line marks the group `⊞N`.
- `@references/parts/master.md` is the contract.

## The first run

`pearde init` — one command, and a board exists: `.pearde/settings.md` with
every knob named, `language: English` on its first line, `.pearde/vision.md`
from the template, the daemon watching it, `doctor` once, and the three lines
to run next, each running as printed with the two lines above in the shell. It
asks nothing; `pearde settings <key>=<value>` changes a knob, per
@references/settings.md. Nothing about installing does that, and nothing about
installing touches `.pearde/`.

## Uninstall

Remove the skill folders you made, or `bash @resources/install.sh --remove
<skills-dir>`. `git checkout SKILL.md` restores the installer `--apply`
retired. Delete the `pearde:begin`/`:end` block from the instructions file and
leave the rest alone. Unwire the status line yourself — that file is yours.
Drop the alias from your shell file — yours to add, yours to remove.

`.pearde/` is your data: untouched by installing, and it survives
uninstalling. The view stops with `python3 @resources/board/serve.py stop`.
Nothing else of this system lives outside this folder except
`.pearde/.state/plan.json`, `.pearde/.state/history.jsonl` and
`.pearde/.state/view.html` on each board — machine-local and regenerable.
