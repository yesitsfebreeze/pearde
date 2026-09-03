# Plugins

Four to install, four marketplaces to add, one corner to refuse.

| plugin | stars | job | why it fits |
|---|---|---|---|
| [ponytail](https://github.com/DietrichGebert/ponytail) | 117.9k | the laziest senior dev — best code is code never written | output discipline; composes with caveman; MIT, active |
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | 27.7k | context usage, active tools, running agents | the pass, visible while it runs |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 26.5k | markdown plans surviving session death | the board's plain-markdown conviction |
| [cc-safety-net](https://github.com/kenryu42/cc-safety-net) | 1.5k | blocks destructive git/fs commands | one board, many sessions, one writer per file |

`caveman` (102k, MIT) is already active here.

## Marketplaces, browsed on demand

- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — 35.7k — official directory
- [wshobson/agents](https://github.com/wshobson/agents) — 39.3k — multi-harness, MIT
- [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) — 1.2k — curated
- [davepoon/buildwithclaude](https://github.com/davepoon/buildwithclaude) — 3.4k — hub of hubs

## Rejected — pearde already is this

| plugin | stars | why |
|---|---|---|
| claude-mem | 92.7k | persistent memory — the knowledge layer is that |
| claude-obsidian | 14.4k | second brain — same overlap |
| engram, recall, claude-db | 1.4k–0.2k | memory engines, same overlap |
| cavekit, cavemem | 1.1k/0.7k | frozen by their own README |

The memory corner is the ecosystem's biggest star pool and the one to refuse —
installing one rebuilds outside the board, worse, what
`resources/knowledge.py` does natively.

## The list is Claude-adapter data

Plugins are Claude-Code-only: `resources/board/adapters/claude.json` carries
`plugins`, one `{"name","marketplace","repo"}` per entry, and `doctor.sh`
compares it against `$CLAUDE_CONFIG_DIR/plugins/installed_plugins.json`,
falling back to `~/.claude/plugins/`. `bash resources/doctor.sh` prints the
two install commands per missing plugin. `off`, never `broken` — cheaper,
never required. Another runtime's adapter carries no list, so the row stays
silent and the check names no agent.

## Measured 2026-08-31, re-measure 2027-03-01

GitHub search API (`topic:claude-code-plugin`, `topic:claude-plugin`,
`topic:claude-skills`, marketplace queries, each sorted by stars), then
state-checked for push date, license and archived flag. Stars discover, never
decide — [`../resources/scout/findings.md`](../resources/scout/findings.md)
holds the row. A pick falls on going archived or frozen, or on pearde shipping
the job natively.
