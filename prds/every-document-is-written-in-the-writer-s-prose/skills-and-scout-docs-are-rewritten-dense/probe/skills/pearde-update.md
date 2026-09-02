---
name: pearde-update
description: Check every install of pearde on this machine and bring it current — the project-local skills directory for this repo first, then the machine-wide one, each reported ok, off or broken with the exact command that fixes it. An install is symlinks, so updating is re-linking the set, never a copy. Use for "/pearde-update", "update pearde", "pearde update", "is pearde up to date", "am I on the latest pearde", "re-install pearde", "a skill is missing", "the new skill does not fire", "update the skills", "did the install pick up the new skill", "check my pearde install".
---

Read @references/update.md — what each row means, why an install is never
copied, and why two global skills directories can both look installed while
only one is read. The scope is `@@update`.

```bash
python3 @resources/pearde.py update              # every install found, checked and re-linked
python3 @resources/pearde.py update --dry        # say what it would do, write nothing
python3 @resources/pearde.py update --local      # this repo's .claude/skills only
python3 @resources/pearde.py update --global     # the machine-wide one only
```

Print every row returned, the `off` ones included. `off` is not a fault: a
skills directory could sit there and does not, and the `fix:` line under the
row names the one command for putting one there. Never run that command
unasked — an install nobody wanted is how a machine ends up with two, one of
them inert.

**Installs are updated, never boards.** A board made before part of the layout
existed is brought current by `pearde upgrade [<dir>]` — the wiki content, the
vault, the generated PRD notes. Say so when a board looks behind, and run it
when asked.

Exit 1 means a `broken` row: a link resolving to nothing, which is what a
moved or renamed repo leaves behind. The fix line is the whole repair.
