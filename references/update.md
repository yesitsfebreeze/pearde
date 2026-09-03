# Update

`pearde update` re-applies every install's links and reports each `ok`, `off`
or `broken`. @references/install.md is what an install is.

## The set goes stale, never the content

An install is five symlinks per skill, made by @resources/install.sh:

```
<skills-dir>/<name>/  SKILL.md · README.md · index.md · references · resources
```

Every link points into this repo's working tree, so the content is current the
moment the tree is. Only the set goes stale, and silently.

| what changed | what the agent gets |
|---|---|
| a skill added since the install | no folder, no skill |
| a skill renamed | a folder whose `SKILL.md` points nowhere |
| the repo moved on disk | every link dead at once |

`update.sh` re-runs `install.sh --apply` on each directory already holding a
pearde, then counts dead links.

## The rows

| row | is |
|---|---|
| `tree` | this checkout — branch, uncommitted count, ahead/behind upstream. Never pulled: a pull with local work in the way strands every install half-current. `off` means behind; the fix is the pull |
| `local` | `<repo>/.claude/skills` for the repo the shell is in — skills wanted here only |
| `global` | `$CLAUDE_CONFIG_DIR/skills`, or `~/.claude/skills` when unset — the one in force, labelled as such |
| `global-alt` | `~/.claude/skills` when `CLAUDE_CONFIG_DIR` points elsewhere — a complete install never read |

| verdict | is |
|---|---|
| `ok` | present, every link resolving |
| `off` | no install there — not a fault; the `fix:` line would make one |
| `broken` | present, links resolving to nothing; exits 1 |

## `off` is printed, never run

`update` creates no install the user did not ask for. `CLAUDE_CONFIG_DIR`
moves an agent's whole configuration directory, so a machine can hold two
complete installs — the `global` / `global-alt` split — one of them correct,
complete and inert. A skill that does not fire looks the same whether never
installed or installed in the wrong place.

## Installs, not boards

`update` touches skills directories only. A board's own `.pearde/` — the
`wiki/` content, the Obsidian vault, the generated PRD notes under
`wiki/board/` — comes up to this repo's layout by `pearde upgrade [<dir>]`, in
@resources/board/init.py.
