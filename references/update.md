# Update

What `pearde update` checks, and why each row reads the way it does.
@references/install.md is what an install *is* — this is keeping one current.

## Why an update is not a download

An install is five symlinks per skill, made by @resources/install.sh:

```
<skills-dir>/<name>/  SKILL.md · README.md · index.md · references · resources
```

Every one of them points into this repo's working tree, so the *content* of an
install is current the moment the tree is. Nothing is ever copied, and there is
nothing to re-copy.

What does go stale is the **set**. A skill file added since the install has no
folder and therefore does not exist for the agent; a skill renamed leaves a
folder whose `SKILL.md` points at a path that is gone; a repo moved on disk
leaves every link dead at once. All three are silent — the agent does not
report a skill it never saw. So updating is re-applying the links and then
looking at what resolves.

`update.sh` re-runs `install.sh --apply` on each directory that already holds a
pearde, then walks the folders itself and counts the links that resolve to
nothing.

## The rows

| row | is |
|---|---|
| `tree` | this checkout — branch, uncommitted count, ahead/behind its upstream. Reported, never pulled: a pull with local work in the way stops halfway and leaves every install half-current. `off` means behind, and the fix is the pull |
| `local` | `<repo>/.claude/skills` for the repo the shell is in — the per-project directory, for skills wanted here and nowhere else |
| `global` | `$CLAUDE_CONFIG_DIR/skills`, or `~/.claude/skills` when that variable is unset. The one actually in force, and labelled as such |
| `global-alt` | `~/.claude/skills` when `CLAUDE_CONFIG_DIR` points somewhere else. A complete install that is never read |

`ok` is an install present and every link resolving. `off` is no install in
that place — not a fault, and the `fix:` line is what would make one. `broken`
is an install present with links that resolve to nothing, and exits 1.

## Why `off` is never repaired on its own

`update` will not create an install that is not there. A skills directory the
user did not ask for is how a machine ends up holding two complete installs
with only one of them read — which is exactly the `global` / `global-alt` split
this repo has to report, and the failure that looks identical to no install at
all. So the command is printed and not run.

## Two global directories

`CLAUDE_CONFIG_DIR` moves an agent's whole configuration directory. Links
written into the other one are correct, complete, and inert. Both are checked
and both are named, because the difference is invisible from inside the agent —
a skill that does not fire looks the same whether it was never installed or
installed twice in the wrong place.

## Installs, not boards

`update` touches skills directories only. Bringing a *board* up to the layout
this repo is on — the `wiki/` content, the Obsidian vault, the generated PRD
notes under `wiki/board/` — is `pearde upgrade [<dir>]`, in
@resources/board/init.py. The two are separate on purpose: one is where the
code is read from, the other is what a project's own `.pearde/` holds.
