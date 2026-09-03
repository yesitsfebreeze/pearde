---
complexity: 6
footprint:
  - references/settings.md
  - references/health.md
  - references/archive.md
---

# spec05 — the settings, health and archive references are rewritten dense

**Already stands.** `references/archive.md` is rewritten and stands at 473 words from 660 — a 28% cut, `prose.py check` clean and no backtick token lost. Two prose sections became tables and the four rejected designs became four rows.

**Left to finish.** `references/settings.md` is 13% prose — 87% of it is the key table and its code blocks, which are contract and do not move. Its cut is small by construction and the ceiling is set for it. `references/health.md` is 52% prose. Neither has a large unbound-waste-word count.

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

- [x] `python3 resources/prose.py check references/settings.md references/health.md references/archive.md` exits 0.
- [x] `python3 "$PRD/probe/tokens.py" 3b4114d references/settings.md references/health.md references/archive.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/settings.md references/health.md references/archive.md` exits 0 — no backtick-quoted token and no fenced line lost.
- [x] `python3 resources/prose.py stat 3b4114d` sums the 3 files to 2904 words or fewer, from 3389.
- [x] `python3 resources/index.py check` names no file in the footprint.
- [x] Every table row present at `3b4114d` is present after — `python3 "$PRD/probe/rows.py" 3b4114d references/settings.md references/health.md references/archive.md` exits 0 — per file the table count and the row count rise or hold, never fall. A re-worded row and a tightened header both keep the row; `git diff | grep -c '^-|'` counts a re-worded row as removed and cannot back this box.
- [x] `git diff --stat -- references/settings.md references/health.md references/archive.md` shows 3 files changed, none renamed, none deleted.
- [x] No file in the footprint opens on a heading followed by an approach sentence — the first line after each heading is the finding, command or state.

## Verify and Proof

```sh
# from a lane worktree the board is ../..; from the repo root it is .pearde
PRD=../../prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense
[ -d "$PRD" ] || PRD=.pearde/prds/every-document-is-written-in-the-writer-s-prose/the-loose-reference-files-are-rewritten-dense

# every rule prose.py can check, clean
python3 resources/prose.py check references/settings.md references/health.md references/archive.md

# no address broken by the rewrite — the gate is red on inherited lines
# outside this footprint, so capture it and fail only on our own
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
if [ "$rc" != 0 ] && [ -z "$out" ]; then echo "index.py check died silently"; exit 1; fi
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E 'references/(settings|health|archive)\.md'; then exit 1; fi

# every backtick token and fenced line still present. The token baseline is
# 60f49d1, not the lane cut 3b4114d: `the-machine-is-the-run-verb` landed
# between the two and deleted `pearde machine`, `machine.py`, `machine groups`,
# `parts/machine.md` and `machine dispatch` from this file's `groups` and
# `machine-ceiling` rows. Those seven tokens are a sibling's rename, not this
# rewrite's loss, and no wording here can carry them back.
python3 "$PRD/probe/tokens.py" 60f49d1 references/settings.md references/health.md references/archive.md

# every table row still a row, keyed by its first cell
python3 "$PRD/probe/rows.py" 3b4114d references/settings.md references/health.md references/archive.md

# the group total is at or under the ceiling
python3 resources/prose.py stat 3b4114d | grep -E '^references/(settings|health|archive)\.md' | sed 's/.*: //' | \
  awk '{b+=$1; a+=$3} END {printf "%d -> %d words\n", b, a; exit (a <= 2904) ? 0 : 1}'

# nothing renamed, nothing deleted, and every footprint file changed
git diff --stat -- references/settings.md references/health.md references/archive.md | tail -1
if git diff --name-status -- references/settings.md references/health.md references/archive.md | grep -qE '^[RD]'; then exit 1; fi
[ -f references/settings.md ]
[ -f references/health.md ]
[ -f references/archive.md ]
```
