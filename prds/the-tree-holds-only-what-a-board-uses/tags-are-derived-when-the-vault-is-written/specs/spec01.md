---
complexity: 14
footprint:
  - resources/knowledge.py
  - resources/board/obsidian/graph.json
---

# spec01 — the vault writer derives a tagged note for every memo and every workflow

`knowledge.py board` already writes one generated, tagged note per PRD and
derives its tags from the fields it just wrote (`prd_tags`). This spec gives
memos and workflows the same treatment: `board` writes `wiki/memos/<slug>.md`
and `wiki/workflows/<slug>.md`, each carrying the tags its kind and status
imply, and the graph preset stops drawing the authored folders — exactly as
it already stops drawing `prd.md`. After this spec the tags exist in the
vault without any authored record storing one, so spec02 can delete the
stored copies.

**What already stands** — the whole of it, built in the lane and uncommitted
there: `Store.memos` / `Store.workflows` and their `ensure()` rows,
`memo_tags(kind, status)` and `workflow_tags(kind)` beside `prd_tags`,
`write_kind_notes()`, the `cmd_board` wiring that scans the library through
`workflows.py scan` and re-aims the `## Decisions` links at the generated
notes, and the new `search` string in `graph.json`. Verified in a clean-room
copy of this board: 189 PRD notes, 67 memo/workflow notes, invariant green.

**What is left** — carry the lane's two files into the checkout, and confirm
the counts on the live board rather than the clean room.

The one trap the build hit: Obsidian's `path:` operator matches a **substring**
of the path ([[260903-b678]]), so `-path:"memos"` would hide the generated
`wiki/memos/` folder along with the authored one. The filter is spelled
`-path:"pearde/memos"` and `-path:"pearde/workflows"`, which separates the two
and is still a substring of `.pearde/memos` — so it holds for a board under
either name.

## Acceptance

- [ ] `python3 resources/knowledge.py board` writes one note under
      `.pearde/wiki/memos/` per authored memo and one under
      `.pearde/wiki/workflows/` per authored workflow or atomic, and its
      printed line names both counts.
- [ ] Every generated memo note carries `tags: [memo, kind/<kind>, status/<status>]`
      with the kind and status read from the authored memo; every generated
      library note carries `tags: [workflow]` or `tags: [atomic]`.
- [ ] No generated note is written by hand: deleting an authored memo and
      re-running `board` removes its generated note, and adding one adds it.
- [ ] A generated note links the authored record it derives from, and relays
      every wikilink that record's body draws, re-aimed at the generated note
      of any authored record it names.
- [ ] A PRD note's `## Decisions` list links `<board>/wiki/memos/<slug>`, not
      the bare slug.
- [ ] `graph.json`'s `search` excludes `pearde/memos` and `pearde/workflows`
      and excludes neither `pearde/wiki/memos` nor `pearde/wiki/workflows`.
- [ ] `resources/knowledge.py` byte-compiles and `python3 resources/index.py check`
      names no file in this footprint.

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
python3 -m py_compile resources/knowledge.py
python3 resources/knowledge.py board
ls .pearde/wiki/memos/*.md | wc -l        # = memos on disk, README excluded
ls .pearde/wiki/workflows/*.md | wc -l    # = workflows + atomics on disk
grep -h '^tags:' .pearde/wiki/memos/*.md | sort -u
grep -h '^tags:' .pearde/wiki/workflows/*.md | sort -u
python3 -c "import json;s=json.load(open('resources/board/obsidian/graph.json'))['search'];assert 'pearde/memos' in s and 'pearde/workflows' in s and 'wiki/memos' not in s;print(s)"
python3 resources/index.py check
```
