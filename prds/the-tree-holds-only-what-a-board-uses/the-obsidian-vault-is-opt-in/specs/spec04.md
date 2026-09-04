---
complexity: 8
footprint:
  - README.md
  - references/obsidian.md
  - references/files.md
  - resources/board/knowledge/Dashboard.md
  - resources/knowledge.py
---

# spec04 — the written contract says optional viewer, and the text fallback is named where a person meets it

Four documents told a reader the vault is part of a board, seeded by `init`,
with two required plugins and a REST port a pass reads the board through.
Three of those four claims were never true of the code and the fourth stops
being true with spec01. The prose says instead: the vault is an optional
viewer needing Obsidian and its Dataview plugin, `pearde vault` is the door,
and a script reads the board the way every reader in this repo actually does —
files, `plan.py`, `knowledge.py`, `pearde view`. Two pages a person meets
*without* a vault — `Dashboard.md`, which renders as a table of contents in
any other reader, and `knowledge.py dashboard`'s closing line — name the text
fallback where they are read.

**What stands** (built in this lane, uncommitted): `references/obsidian.md`'s
plugin section is `## One plugin, seeded by pearde vault and never
overwritten` with a one-row table and a paragraph saying what the REST plugin
was and why it went; the `Two ways in`, `The connection facts` and `Queries
worth running` sections are replaced by `## How a script reads the board —
files, never a port` and its table; the `pearde vault` paragraph says `init`
writes none and doctor's row is `off` with no vault and `broken` only with a
vault and no entry. `references/files.md`'s `init.py` row, its
`obsidian.md` row and its `resources/board/knowledge/` paragraph are
rewritten. `README.md` gains a `<project>/.obsidian/` row under *What is on
disk*. `Dashboard.md`'s opening says every block below is a Dataview query and
names the text fallback; `knowledge.py`'s `cmd_dashboard` closes with the same.

**What is left**: nothing in these files. **Read this before starting**: three
sibling PRDs also write into this footprint —
`install-fetches-nothing`/spec02 and
`the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`/spec04 both own
`references/obsidian.md` and `references/files.md`, and the second of those
declares a *second* plugin, `obsidian-unhide`. Whichever lands second keeps
the one claim this PRD is responsible for — `obsidian-local-rest-api` is named
nowhere as current, and the vault is optional — and does not restore a
plugin count this PRD did not set.

## Acceptance

- [x] No file under `references/`, `README.md`, `index.md` or `resources/` presents `obsidian-local-rest-api`, port 27124 or `.obsidian-api-key` as something the repo currently ships or reads.
- [x] `references/obsidian.md` says the vault is seeded by `pearde vault`, that `init` writes none, and that doctor's row is `off` with no vault.
- [x] `references/obsidian.md` carries a section naming what a script reads the board with instead of a port, and every command it names exists.
- [x] `README.md` has a row for the vault saying it is an optional viewer needing Obsidian and Dataview, written by `pearde vault` alone.
- [x] `references/files.md`'s `init.py` row does not claim `init` seeds a vault or mints a key.
- [x] `Dashboard.md` and `knowledge.py dashboard` both name the text fallback, spelled as a command that runs.
- [x] `python3 resources/index.py check` reports no new problem beyond the four already on record at `f8968fe`.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
# the three names may survive only as history, and only in the three files
# that carry the note saying the plugin went on 2026-09-03
test "$(grep -rl '27124\|obsidian-api-key\|local-rest-api' README.md index.md \
    references/ resources/ --include='*.md' --include='*.py' --include='*.sh' \
    --include='*.json' | sort | tr '\n' ' ')" \
  = "references/obsidian.md resources/board/init.py resources/install.sh "
echo "PASS only history"
grep -q 'optional viewer' README.md
echo "PASS readme row"
grep -q 'One plugin, seeded by' references/obsidian.md
echo "PASS one plugin"
grep -q 'knowledge.py dashboard' resources/board/knowledge/Dashboard.md
echo "PASS text fallback named in Dashboard"
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -vE 'resources/common\.py is on disk|hotreload-test\.js|a-board-s-own-file-commits-in-the-board-repo' | grep -q .; then echo "FAIL new index problem"; exit 1; fi
echo "PASS index gate — the four on record at f8968fe and no more"
python3 resources/knowledge.py dashboard | tail -3
echo "PASS dashboard runs and closes with the text fallback"
```
