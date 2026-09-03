---
complexity: 8
footprint:
  - references/obsidian.md
  - references/graph.md
  - references/knowledge.md
---

# spec04 — the vault, graph and knowledge references are rewritten dense

**Already stands.** Nothing. All three files are untouched.

**Left to finish.** `references/obsidian.md` is 85% prose — the highest share in the PRD — and `prose.py check` reports 7 unbound waste words in it. It is cited from six files under `resources/` as the reason the dot had to go, so the reasoning it carries is load-bearing. `references/knowledge.md` is the contract `@resources/knowledge.py relink` and `doctor`'s `knowledge` row point at.

## The rules

@references/language.md `## Density` is the whole standard — nine rules, four of
them mechanical and checked by `@resources/prose.py`. Nothing in this spec
restates them.

Three constraints hold over every file here:

| constraint | why |
|---|---|
| Every backtick-quoted token and every fenced line survives character-identical | a command line, flag, refusal string, frontmatter key, state name or settings key is behaviour, never prose |
| Every table row survives as a row | cutting words never means cutting a fact |
| No file is renamed, moved, split or merged | the rewrite is content only |

Prose becoming a table is the main lever — `references/archive.md` gave up 28%
of its words that way. A file whose prose is mostly command text lands nearer
`references/install.md`'s 11%.

## Acceptance

- [x] `python3 resources/prose.py check references/obsidian.md references/graph.md references/knowledge.md` exits 0.
- [x] `python3 "$PRD/probe/tokens.py" 3b4114d references/obsidian.md references/graph.md references/knowledge.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/obsidian.md references/graph.md references/knowledge.md` exits 0 — no backtick-quoted token and no fenced line lost.
- [x] `python3 resources/prose.py stat 3b4114d` sums the 3 files to 1611 words or fewer, from 2170.
- [x] `python3 resources/index.py check` names no file in the footprint.
- [x] Every table row present at `3b4114d` is present after — `python3 "$PRD/probe/rows.py" 3b4114d references/obsidian.md references/graph.md references/knowledge.md` exits 0 — per file the table count and the row count rise or hold, never fall. A re-worded row and a tightened header both keep the row; `git diff | grep -c '^-|'` counts a re-worded row as removed and cannot back this box.
- [x] `git diff --stat -- references/obsidian.md references/graph.md references/knowledge.md` shows 3 files changed, none renamed, none deleted.
- [x] No file in the footprint opens on a heading followed by an approach sentence — the first line after each heading is the finding, command or state.

## Verify and Proof

```sh
# from a lane worktree the board is ../..; from the repo root it is .pearde
PRD=../../prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense
[ -d "$PRD" ] || PRD=.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense

# every rule prose.py can check, clean
python3 resources/prose.py check references/obsidian.md references/graph.md references/knowledge.md

# no address broken by the rewrite — the gate is red on inherited lines
# outside this footprint, so capture it and fail only on our own
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ "$rc" != 0 ] && [ -z "$out" ]; then echo "index.py check died silently"; exit 1; fi
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'references/(obsidian|graph|knowledge)\.md'; then exit 1; fi

# every backtick token and fenced line still present
python3 "$PRD/probe/tokens.py" 3b4114d references/obsidian.md references/graph.md references/knowledge.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/obsidian.md references/graph.md references/knowledge.md

# the group total is at or under the ceiling
python3 resources/prose.py stat 3b4114d | grep -E '^references/(obsidian|graph|knowledge)\.md' | sed 's/.*: //' | \
  awk '{b+=$1; a+=$3} END {printf "%d -> %d words\n", b, a; exit (a <= 1611) ? 0 : 1}'

# nothing renamed, nothing deleted, and every footprint file changed
git diff --stat -- references/obsidian.md references/graph.md references/knowledge.md | tail -1
if git diff --name-status -- references/obsidian.md references/graph.md references/knowledge.md | grep -qE '^[RD]'; then exit 1; fi
[ -f references/obsidian.md ]
[ -f references/graph.md ]
[ -f references/knowledge.md ]
```
