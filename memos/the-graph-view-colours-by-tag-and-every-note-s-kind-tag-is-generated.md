---
memo: the-graph-view-colours-by-tag-and-every-note-s-kind-tag-is-generated
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: the vault's graph colours by tag and never by folder, and every note carries a generated kind tag
date: 2026-09-02
updated: 2026-09-03
---

# the-graph-view-colours-by-tag-and-every-note-s-kind-tag-is-generated — a path group dies on the move that renames a folder

## Decision

The Obsidian graph's colour groups are `tag:` queries — `#prd`, `#memo`,
`#workflow`, `#atomic`, `#conclusion`, `#source`, `#pending`, `#graph` — and
every note carries the tag of its kind. No group queries a path.

The kind tag is never typed and never stored. `knowledge.py board` is the one
writer: it derives each tag onto the generated note it writes — a PRD note
under `wiki/board/`, a memo's under `wiki/memos/`, a library file's under
`wiki/workflows/` — from the `kind`, `status` and slug key the authored record
already carries, on every regeneration. The authored file itself carries no
`tags:` key; a stray one fails the check, which names deleting it.

A PRD note carries three axes beside its kind — `state/`, `origin/`, `blast/`
— and not `workflow/`: `workflow:` is a wikilink, so the graph already draws
that edge, and a tag beside it would be a second, weaker copy of it.

## Why

The groups were `path:` queries until today, and every one of them died in
silence when the board moved to `pearde/wiki/` — `path:"prds/knowledge/board"`
matches nothing now. Obsidian does not report a group that matches nothing: it
draws grey. So the view degraded to the wiki's own wikilinks, which is the
folder tree and not the board, and it looked like a deliberate layout rather
than a break. The user read it as the old Vicky/wiki layout and asked why we
had gone back to it.

A tag is carried by the note. A path is carried by the tree, and the tree
moves — twice this month. Keying colour on the thing that travels with the
note means the next layout change costs nothing.

Tags earn a second thing paths never could: with `showTags` on, `#state/open`
is a node every open PRD hangs off, and `#kind/invariant` gathers the memos
that bind. The connections a person opens the graph to see are drawn, not
inferred from colour.

## Alternatives considered

**Repair the path queries in place** — one edit, and correct until the next
rename. It also cannot express an axis: a folder says a note's kind and
nothing else, so `state/open` has no spelling as a path.

**Obsidian's property search (`[type:prd]`)** — the properties already exist,
so no file would have changed. The graph's colour groups do accept a search
query, but a property is not a node: nothing is drawn for `type: prd`, so the
graph gains colour and no connections. It also leaves the kind of an
authored memo unqueryable by anything but its folder.

**Tags typed by hand** — rejected on this repo's own rule that two fields
which must agree are one field that can disagree. See
[[a-duplicate-a-second-reader-forces-is-generated-and-checked-never-typed]].

## Consequences

- No memo and no library file stores a `tags:` key. The authored
  `memos/` and `workflows/` folders are excluded from the graph preset's
  `search`, so each record draws once — through its generated note, coloured.
- A vault seeded before today keeps its own scale and forces;
  `init.repair_graph_view` overwrites only `colorGroups`, `search` and
  `showTags`, on `init` and on `upgrade`.
- It does not fix what the search filter hides: specs, raw `prd.md` and the
  file index stay out of the graph, so their groups would be dead weight and
  are not written.
