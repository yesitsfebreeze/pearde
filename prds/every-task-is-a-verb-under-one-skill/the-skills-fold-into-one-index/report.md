# the-skills-fold-into-one-index — implementer report

Verdict: DONE

worker `impl-skills-index2` · engineer · lane
`/Users/feb/dev/infra/pearde/.pearde/.lanes/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index`
branch `lane/every-task-is-a-verb-under-one-skill-the-skills-fold-into-one-index`,
uncommitted per @references/parts/commits.md — the lane's commit is `collect`'s
step 1b, not a worker's.

**30 of 30 boxes ticked, each against output quoted below.** 43 files changed,
675 insertions, 669 deletions. Pass one stood the fold up; this pass finished
the wording each spec named as outstanding, and fixed one real defect found
while proving spec03.

| spec | boxes | state |
|---|---|---|
| `spec01` — seventeen skills become eighteen tasks, one skill indexes them | 7/7 | green |
| `spec02` — a doctor row that fails when a trigger phrase falls out | 7/7 | green |
| `spec03` — installing is one symlink, updating clears what an older one left | 9/9 | green |
| `spec04` — the map names the tasks, and nothing names the skills | 7/7 | green |

`python3 resources/index.py skills` exits 0. `bash resources/doctor.sh` reports

```
skills  ok  1 skill · 18 tasks · doctor drill grammar graph health knowledge
            master memo persona-ask persona-create persona plan report run
            scout update view workflow
```

`python3 resources/index.py check` reports exactly one problem, pre-existing and
outside every footprint (below). `bash -n` passes on every `resources/*.sh`;
`py_compile` passes on `index.py`, `knowledge.py`, `pearde.py`. No untracked
file was left in the lane.

## What this pass changed

Pass one left four "what is left to finish" items, one per spec. All four are
closed, and one defect was found and fixed inside spec03's scope.

**spec01 — three sentences that only made sense while each task was a skill.**
`references/tasks/persona.md` said *"`pearde-persona-ask` changes nothing. This
skill is the switch itself"*; `persona-ask.md` said *"Run
`pearde-persona-create` first"*; `persona-create.md` said *"call it with
`pearde-persona-ask`, or wear it with `pearde-persona`"*. All three now name the
verb, not a skill: *"the `persona-ask` verb changes nothing. This one is the
switch itself"*, and so on. `grep -rn 'pearde-' references/tasks/` outside the
`## Fires on` lists is now empty — the lists keep the old names because those
are the phrases a person still types.

**spec02 — the docstring and the doctor page.** `index.py`'s usage block now
lists `skills` beside `check`, and a paragraph says what the second check
answers that the first cannot. `references/parts/doctor.md`'s `skills` row
described the old per-file check (*"a skill file with no `name:` … or a `name:`
that disagrees with its file name"*) and now names all three failures the row
actually has. Its section, *"`skills` is about frontmatter, not placement"*, is
rewritten as *"`skills` is about the one description, not placement"* and split
into **The frontmatter** and **The union**, with why the row is not
`--fix`-able. The *"No agent is named"* section said doctor checks *"the skill
files parse"*; it now says *"the skill parses and reaches every task"*.

**spec03 — the install wording, in three places pass one missed.**

- `resources/update.sh`'s own header still opened *"An install is five symlinks
  per skill … re-applies the links where an install is already present"* — the
  whole model the spec deletes, and invisible to `git grep 'five links'`
  because it says *five symlinks*. Rewritten around the one link and the
  removal. Its `SKILLS` variable pointed at `references/tasks`; renamed
  `TASKDIR`, since a variable that lies is the next reader's wrong turn.
- `README.md`'s *In sixty seconds* block still ran
  `python3 <repo>/resources/pearde.py install --apply <skills-dir>` — a command
  that no longer exists, two lines above a table row already giving the `ln -s`.
  The block now runs `ln -s <repo> <skills-dir>/pearde`, matching its own table.
- `references/tasks/update.md` promised *"every install found, checked and
  re-linked"* and *"why an install is never copied"*. Both now say what
  `update.sh` does: cleared of leftovers, and one symlink that cannot go stale.

`references/install.md`, `references/update.md` and the `## Uninstall` section
needed nothing — they were already correct, and `git grep -i uninstall` finds
that section and nothing pointing at it wrongly.

**spec04 — the manifest and the map.** `references/files.md` called `@SKILL.md`
*"the installer — invocable before the skills are, retired once they exist"*,
and carried a **second** `@SKILL.md` row inside the tasks table, so one file had
two rows saying different things. The Entry-points row now describes the one
skill; the duplicate is gone and its point moved into the section's prose, so
the table is one row per `references/tasks/*.md` and nothing else. The section
heading *"one file per skill"* is now *"one file per task"*, and its paragraph
*"Frontmatter, and a body …"* now says `## Fires on`. `@resources/update.sh`'s
row said *"re-link the set"*. In `index.md`, `@@install` read *"putting every
skill where this agent finds it"* and `@@update` *"the set of links, not the
content"* — both rewritten. `references/templates/grammar.md` still carried the
exact sentence the contract deletes from `handles.md` (*"Several are also skills
of their own"*) on its **handle** row, and an **install** row defining an
install as *"the set of links … Updating is re-linking"*. Both rewritten.
`resources/knowledge.py`'s `index_kind` docstring listed `skill` among the kinds
its own `KINDS` map no longer produces; it lists `task`.

## The defect found and fixed: a note printed under the wrong row

`update.sh --dry` on this machine printed

```
  local   off   …/.claude/skills does not exist · <lane>
                fix: mkdir -p … && ln -s …
                dry · would remove pearde pearde-all … from /Users/feb/.claude/priv/skills
```

The removal note names `/Users/feb/.claude/priv/skills` — the **global**
directory — while sitting under the `local` row. `note()` prints under an empty
label column, so a note emitted before its own row reads as belonging to the row
above it. `check_dir` acted on the leftovers before deciding the row, so every
directory's leftovers were reported against the previous directory's name. On
this machine that read as *"the lane's local skills directory holds 19 leftover
folders"*, which is false, and it is the exact shape of failure this PRD exists
to stop: an agent seeing one thing and being told another.

Fixed by holding the message in `leftmsg` and emitting it after whichever row is
printed. **The removal itself did not move** — it still runs before the row, so
the row describes what is left behind rather than what was found. Proved: each
note now sits under its own directory's row, and the fixture below still passes.

This is inside spec03's footprint and inside its box *"prints what it would
remove"* — a line printed under the wrong name has not reported it. Not a
refactor: one variable and two call sites.

## Proof

**spec01** — `references/skills` gone, `git grep -c 'references/skills'` 0 lines;
`references/tasks/` holds 18 (`doctor drill grammar graph health knowledge
master memo persona-ask persona-create persona plan report run scout update view
workflow`); every one opens `# <verb>` with a `## Fires on` list of backtick
phrases and no frontmatter; `SKILL.md` is `name: pearde` with one
`description:` line of 4824 characters matching `^description: [^|>"]` — a plain
scalar, not block, not quoted; 18 `@references/tasks/` rows in its index;
`grep -c 'Several of these are also skills' references/parts/handles.md` is 0
and `grep -c 'pearde-'` on that file is 0; `index.py check` names no task file.

**spec02** — clean tree: `index.py skills` silent, exit 0. Injected failures,
each restored after:

```
drop  , "what gained stars this week"  → references/tasks/scout.md fires on
        "what gained stars this week" — absent from SKILL.md's description   exit 1
empty references/tasks/memo.md's list  → references/tasks/memo.md has no
        `## Fires on` list — nothing of it reaches the skill description      exit 1
remove description:                    → SKILL.md has no description: in
        frontmatter — nothing decides when the skill fires                    exit 1
```

No traceback in any case. `doctor` on the first: `skills broken 1 skill · 18
tasks · 1 problem`, the phrase named, `fix:` the `index.py skills` command. On
`name: peardeboard`: `skills broken … SKILL.md says name: peardeboard — an
install links it in as pearde/`. Restored: `skills ok`, quoted above.
`index.py badcmd` prints the usage block with the `skills` line in it.

**spec03** — `resources/install.sh` absent; `git grep -c 'install\.sh'`,
`git grep -c 'five links'` both 0 lines; `pearde.py help` exits 0 and lists no
`install`; `bash -n resources/update.sh` passes; `--dry` names `tree ok`,
`local off`, `global off`, `global-alt off` and invokes no installer. On a
throwaway skills directory holding (a) `pearde-doctor/` whose five entries are
all symlinks, (b) a real `pearde-notes/` with a real `SKILL.md`, (c) an
unrelated symlink:

```
--dry     → dry · would remove pearde-doctor from <dir>   … removed nothing
real run  → cleared what an earlier install left: pearde-doctor
after     → pearde-notes and somethingelse both survive
ln -s <repo> <dir>/pearde then → local ok  <dir> · one link · 18 tasks
```

**spec04** — `index.py check` minus the pre-existing `commits.md` line is 0
lines; `index.py scope skills` prints 20 anchors and every one is on disk;
`grep -c '^| @references/tasks/' references/files.md` is 18 and
`grep -c '^| @SKILL.md'` is 1; `grep -c 'install\.sh'` on `references/files.md`
and `index.md` is 0 each; `grep -c 'references/skills' resources/knowledge.py`
is 0 and `index_kind('references/tasks/drill.md')` returns `task`; `@@install`
and `@@update` name no installer script.

## One box whose verify comment does not match its own acceptance

`spec04`'s verify block reads `grep -c '@references/tasks/' references/files.md
# 18`. It returns **19**. The nineteenth is not a row: `@resources/scout/README.md`'s
row says *"the scout manual — what @references/tasks/scout.md is a door to"*,
legitimate prose, and `grep -c` counts lines. The box itself says *"one row per
`references/tasks/*.md`"*, and `grep -c '^| @references/tasks/'` is exactly 18.
Proved against the box, and the comment is reported rather than made true by
distorting a row.

## Findings — defects outside scope, none fixed

- **`references/parts/commits.md` references
  `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`, not on disk.**
  The one problem `index.py check` still reports, and the reason `doctor`'s
  `index` row is `broken`. The path is missing its leading dot — the file is at
  `.pearde/memos/…` — so this looks like one anchor the `dot-pearde` sweep
  (`d0a8da0`) missed rather than a deleted memo. Not in any of the four
  footprints. **The whole of the gap between `index check` clean and `index
  check` exit 1 is this one line**, so it is worth a one-line fix on the next
  pass that owns that file.
- **`doctor`'s `skills` row carries one `fix:` line for two different
  problems.** When the failure is `name:` rather than a dropped phrase, the fix
  offered is still *"the union of every task's `## Fires on` lives in
  SKILL.md's description — python3 …/index.py skills"*, and that command does
  not report the name at all (`doctor.sh` prepends it). The row is correct and
  loud; only its repair line points at the wrong thing. Left alone deliberately:
  spec02's box names that fix line verbatim, and changing it is a judgement the
  spec did not ask for.
- **The board's other `broken` rows** — `vault` (the board is `.pearde`, a
  dot-segment Obsidian skips), `origin` (6 derived PRDs with no `from:`),
  `memos` (44 memos, 45 missing `tags:`, `memos.py retag` is the fix) — are the
  board's own pre-existing state, untouched by this PRD and unchanged by it.

## Health

The brief named no file in the footprint under the health floor, and none was
found. Two names were made honest inside the work already being done —
`update.sh`'s `SKILLS` → `TASKDIR`, and the duplicate `@SKILL.md` manifest row
collapsed to one. Neither is a split; nothing in the footprint wants one.

## Grammar and knowledge

Every term in the contract — *lane*, *footprint*, *scope*, *anchor*, *manifest*,
*handle*, *task*, *verb* — is on record and was used as defined. No word was
needed that the vocabulary does not carry, and none was invented. No fact was
learned outside this repo this pass: the two the build needed
([[260903-1458]], [[260903-5e08]]) were written to the record by the probe pass
and neither needed revisiting.
