---
complexity: 10
footprint:
  - references/skills/pearde-machine.md
  - references/parts/machine.md
  - references/files.md
  - index.md
  - SKILL.md
---

# spec03 — the door: one skill, one part doc, and every wiring point

The script is reachable only if an agent knows it exists. This unit is the
skill file that fires on "work every board", the part doc that says what the
command reads and what it deliberately does not do, and the four places this
repo makes a new file visible. No logic; the logic is spec01 and spec02.

## What already stands

Nothing of this is built. The build proved two things that shrink it:
`resources/install.sh` globs `references/skills/*.md`, so a new skill file is
installed with no edit to the installer; and `resources/pearde.py` discovers
`COMMANDS` from the module, so `pearde machine` needs no row in `FORWARD`.

## The name, and why it is not `all`

The parent PRD wrote this as a `pearde-all` skill. The build does not use that
name. `all` already means the read-only page over every watched board, and
`@references/parts/all.md` says of it *"nobody works it"* — a line the parent's
own fork 1 rules must stay true and must not be edited. A command named `all`
that ranks the machine's work for dispatch would make that sentence read false
on its face. `machine` is the word the child's own contract already uses — *the
machine frontier* — and `resources/board/all.py` already holds the page's
merger, so the script needed a second file whatever the command was called.
This divergence from the parent's wording is deliberate and is recorded here so
it is not read as a slip.

## Acceptance

- [x] `references/skills/pearde-machine.md` exists with `name:` and `description:` frontmatter in the shape of the other sixteen, and its description names the trigger phrases: "work every board", "all my projects at once", "what should the machine do next", "the machine frontier"
- [x] The skill body points at `@references/parts/machine.md` and shows the four invocations — `machine`, `machine boards`, `machine slots`, `machine progress` — as `python3 @resources/pearde.py machine …`
- [x] The skill says in its own words that this command moves nothing, and names the sibling PRD as where dispatch lands
- [x] `references/parts/machine.md` says what is merged, what the marks mean, how the slot count is derived, and the three things it does not do: no write door on `all`, no persisted registry of boards, no board's `settings.md` written
- [x] `references/parts/machine.md` states that an unwatched board is not discoverable, and links `@references/parts/all.md`'s *"a member nobody watches is not one of them"* rather than restating it
- [x] Neither `@references/parts/all.md`'s *"nobody works it"* nor `@references/parts/master.md`'s definition is edited by this unit — `git diff` touches neither file
- [x] `SKILL.md`'s `description:` lists `pearde-machine` among the skill folders it materialises
- [x] `index.md` carries a `@@machine` scope row naming the skill, the part doc, `@resources/board/machine.py`, `@resources/board/plan.py` and `@resources/board/serve.py`
- [x] `index.md`'s `@@skills` row lists `@references/skills/pearde-machine.md`
- [x] `references/files.md` has a row for `references/skills/pearde-machine.md` and one for `references/parts/machine.md`
- [x] `python3 resources/index.py check` reports no problem beyond the one already on record (`resources/board/edit.py references @questions.py`)
- [x] `bash resources/doctor.sh` reports `skills ok 18 well-formed` and names `pearde-machine`
- [x] `bash resources/install.sh --apply <skills-dir>` creates the `pearde-machine` folder with no edit to `install.sh`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 resources/index.py check
bash resources/doctor.sh | grep -E '^  (skills|index) '
grep -c 'pearde-machine' SKILL.md index.md references/files.md
test -z "$(git diff --name-only -- references/parts/all.md references/parts/master.md)" \
  && echo "ok neither line touched"
bash resources/install.sh --dry "$HOME/.claude/priv/skills" | grep pearde-machine
```
