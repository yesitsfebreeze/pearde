# Round — board↔wiki↔obsidian integration + pearde-update

## Established
- Vault root is `.pearde/`; KB store root is `.pearde/wiki/` (not `knowledge/`).
- Board→wiki is `knowledge.py board` (74 notes here). wiki→board is only loop step 7 `knowledge.py query`.
- Global installs are live symlinks: `~/.claude/priv/skills` (in force, CLAUDE_CONFIG_DIR=/Users/feb/.claude/priv) and `~/.claude/skills` (not in force). No repo-local `.claude/skills` anywhere.

## Fixed this round
1. `resources/board/obsidian/community-plugins.json`: `local-rest-api` -> `obsidian-local-rest-api` (wrong id = REST port never opened). Live vault repaired too.
2. `resources/doctor.sh`: knowledge row guarded/rooted at `$BOARD/knowledge` -> `$BOARD/wiki`. Row now prints.
3. `knowledge.py cmd_board`: `## Knowledge` harvested every memo wikilink; now filtered against a once-built sources+conclusions index (`kb_names`).
4. `resources/board/knowledge/_index.md` deleted (duplicate of conclusions/_index.md, stale `knowledge/` path). `conclusions/_index.md` dataviewjs `"conclusions"` -> `"wiki/conclusions"`.
5. NEW `init.py`: `KNOWLEDGE_PRESET`, `write_knowledge()`, `repair_plugin_ids()`, `BOARD_IGNORED`, `write_board_gitignore()`, `cmd_upgrade` + COMMANDS["upgrade"]. `cmd_init` now calls write_knowledge.
6. Ran `pearde upgrade` on all 8 boards — all now have wiki content + board notes.

## SECURITY (reported to user, done)
- `.obsidian-api-key` was committed+pushed in TWO repos: `infra/pearde/.pearde` (c624a16, github/pearde) and `dotfiles` (bca38f0, github/.files). Both `git rm --cached`'d and rotated. History NOT rewritten — user's call, still pending their word.

## Owed / next
- **/pearde-update DONE** — `resources/update.sh` + FORWARD["update"] in pearde.py + `references/skills/pearde-update.md` + `references/update.md` + `@@update` in index.md + files.md rows. 15 skills, both global installs re-linked. `local` reads off (no `<repo>/.claude/skills` here) by design — update never creates an install unasked.
- Also fixed: dotfiles board repo leaked its key too (bca38f0, github/.files) — untracked + rotated.
- Nothing committed yet. 13+ uncommitted files in the pearde repo.
- Nothing auto-runs `knowledge.py board`/`relink` on a state change (graph goes stale). PRD-shaped, not done.
- Obsidian is RUNNING: repaired plugin id + vault registrations need an Obsidian restart / `pearde vault --wait --open`.
