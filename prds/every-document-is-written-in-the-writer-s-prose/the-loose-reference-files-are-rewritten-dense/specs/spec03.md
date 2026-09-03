---
complexity: 9
footprint:
  - references/memo.md
  - references/workflow.md
  - references/grammar.md
---

# spec03 — the memo, workflow and grammar formats are rewritten dense

**Already stands.** Nothing. All three files are untouched.

**Left to finish.** Three format definitions, each with a closed frontmatter key set that a checker reads: `@resources/memos.py`, `@resources/workflows.py` and `@resources/grammar.py`, and `@resources/doctor.sh` names all three in its fix lines. Every key name, every refusal string and every table row is contract. `prose.py check` reports 2, 7 and 8 unbound waste words.

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

- [x] `python3 resources/prose.py check references/memo.md references/workflow.md references/grammar.md` exits 0.
- [x] `python3 "$PRD/probe/tokens.py" 3b4114d references/memo.md references/workflow.md references/grammar.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/memo.md references/workflow.md references/grammar.md` exits 0 — no backtick-quoted token and no fenced line lost.
- [x] `python3 resources/prose.py stat 3b4114d` sums the 3 files to 2531 words or fewer, from 3171.
- [x] `python3 resources/index.py check` names no file in the footprint.
- [x] Every table row present at `3b4114d` is present after — `python3 "$PRD/probe/rows.py" 3b4114d references/memo.md references/workflow.md references/grammar.md` exits 0 — per file the table count and the row count rise or hold, never fall. A re-worded row and a tightened header both keep the row; `git diff | grep -c '^-|'` counts a re-worded row as removed and cannot back this box.
- [x] `git diff --stat -- references/memo.md references/workflow.md references/grammar.md` shows 3 files changed, none renamed, none deleted.
- [x] No file in the footprint opens on a heading followed by an approach sentence — the first line after each heading is the finding, command or state.

## Verify and Proof

```sh
# from a lane worktree the board is ../..; from the repo root it is .pearde
PRD=../../prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense
[ -d "$PRD" ] || PRD=.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense

# every rule prose.py can check, clean
python3 resources/prose.py check references/memo.md references/workflow.md references/grammar.md

# no address broken by the rewrite — the gate is red on inherited lines
# outside this footprint, so capture it and fail only on our own
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ "$rc" != 0 ] && [ -z "$out" ]; then echo "index.py check died silently"; exit 1; fi
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'references/(memo|workflow|grammar)\.md'; then exit 1; fi

# every backtick token and fenced line still present
python3 "$PRD/probe/tokens.py" 3b4114d references/memo.md references/workflow.md references/grammar.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/memo.md references/workflow.md references/grammar.md

# the group total is at or under the ceiling
python3 resources/prose.py stat 3b4114d | grep -E '^references/(memo|workflow|grammar)\.md' | sed 's/.*: //' | \
  awk '{b+=$1; a+=$3} END {printf "%d -> %d words\n", b, a; exit (a <= 2531) ? 0 : 1}'

# nothing renamed, nothing deleted, and every footprint file changed
git diff --stat -- references/memo.md references/workflow.md references/grammar.md | tail -1
if git diff --name-status -- references/memo.md references/workflow.md references/grammar.md | grep -qE '^[RD]'; then exit 1; fi
[ -f references/memo.md ]
[ -f references/workflow.md ]
[ -f references/grammar.md ]
```
