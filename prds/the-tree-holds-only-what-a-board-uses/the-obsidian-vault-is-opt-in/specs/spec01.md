---
complexity: 12
footprint:
  - resources/board/init.py
  - resources/board/obsidian/community-plugins.json
---

# spec01 — `init` writes no vault, mints no key, and `pearde vault` is the only door

`init` wrote `<project>/.obsidian/` on every new board: an app configuration
for a viewer its owner may not have, may keep somewhere else, or may never
open. It also minted a fresh `obsidian-local-rest-api` API key into every
board and mirrored it at `wiki/.obsidian-api-key` — a live credential written
for a caller that does not exist, since no module in this repo reads that key,
makes a request to the port, or speaks the protocol. Both leave. `vault` seeds
and registers; `upgrade` brings a vault that IS there current and conjures
none; `init` says in one line that the board is plain Markdown and where the
door is.

**What stands** (built in this lane, uncommitted): `OBSIDIAN_PLUGINS` is
`("dataview",)`; `write_obsidian` returns `(installed, missing, stranded)` —
the key is gone from the tuple and from the body, and its docstring says it is
called by `vault` and `upgrade`, never by `init`; `BOARD_IGNORED` no longer
names `wiki/.obsidian-api-key` and `BOARD_HEADER` no longer claims two entries
hold a credential; `cmd_init` drops the `write_obsidian`, `register_vault` and
missing-bundle blocks and the `.obsidian/plugins/dataview` line from its `--dry`
paths, and prints the one no-vault line instead; `cmd_upgrade` guards the
vault, repair and register block on `os.path.isdir(<project>/.obsidian)` and
prints `no vault to register` otherwise, its `--dry` line saying `no vault
here, and upgrade writes none`; `repair_plugin_ids` says it takes no plugin
away from a vault that has one; `community-plugins.json` lists `dataview`
alone.

**What is left**: nothing in this file — the unit is built and needs its boxes
run. Do not remove `obsidian-local-rest-api` from a vault that already has it:
`repair_plugin_ids` has never taken a plugin away and must not start.

## Acceptance

- [ ] `pearde init <fresh-dir>` creates no `<fresh-dir>/.obsidian` and no file named `.obsidian-api-key` anywhere under the project.
- [ ] `pearde init` prints one line naming `pearde vault` as the way to get the vault and `knowledge.py dashboard` as the text fallback.
- [ ] `init` makes no entry in Obsidian's machine-wide vault register — a throwaway board no longer registers itself.
- [ ] `write_obsidian` returns a three-tuple and every caller unpacks three names; `grep -c "apiKey" resources/board/init.py` is 0.
- [ ] `OBSIDIAN_PLUGINS` and `resources/board/obsidian/community-plugins.json` each name `dataview` and nothing else.
- [ ] `pearde upgrade` on a board whose project has no `.obsidian/` creates none, prints `no vault to register`, and its `--dry` says none is written.
- [ ] `pearde upgrade` on a project that HAS `.obsidian/` still repairs the plugin ids, the ignore filters and the graph groups.
- [ ] `BOARD_IGNORED` does not name `wiki/.obsidian-api-key`, and no line of `resources/` writes that path.

## Verify and Proof

```sh
cd "$(mktemp -d)" && git init -q .
python3 <repo>/resources/pearde.py init "$PWD" | tee /tmp/init.log
test ! -e "$PWD/.obsidian" && echo "PASS no vault"
! find "$PWD" -name '*obsidian-api-key*' | grep . && echo "PASS no key"
grep -q 'pearde vault' /tmp/init.log && echo "PASS door named"
python3 <repo>/resources/pearde.py upgrade --dry "$PWD" | grep -q 'no vault here' && echo "PASS upgrade dry"
grep -c apiKey <repo>/resources/board/init.py
python3 -c "import ast;ast.parse(open('<repo>/resources/board/init.py').read())"
```
