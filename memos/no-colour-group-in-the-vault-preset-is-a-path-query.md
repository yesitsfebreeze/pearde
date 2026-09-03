---
memo: no-colour-group-in-the-vault-preset-is-a-path-query
kind: invariant
status: decided
tags:
  - memo
  - kind/invariant
  - status/decided
subject: every colour group in the vault preset is a tag query, and every tag it names is carried by a note
date: 2026-09-02
updated: 2026-09-03
verify: bash resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh
---

# no-colour-group-in-the-vault-preset-is-a-path-query — a group matching nothing draws grey, and grey is not an error

## Decision

Every `colorGroups` query in `resources/board/obsidian/graph.json` is a
`tag:#…` query, and every tag it names is carried by at least one note on the
board. The check is the verify command; a group keyed on a path, or a group
naming a tag no writer emits any more, is a break.

## Why

Obsidian reports nothing for a colour group that matches nothing — the graph
draws grey and reads as a design choice. The path-keyed groups died the day
the board moved to `pearde/wiki/`, and nobody saw it until a person said the
graph looked like the old wiki layout. A silent failure needs a check or it
recurs.

The second half is the same failure in the shape it will take next. Keying on
tags removes the folder-move break, not the possibility of a dead group: a
writer that stops emitting a kind's tag leaves the group behind it matching
nothing, and greys out exactly as before. So the check regenerates the vault
first — `knowledge.py board` — and then asks whether the tag is actually
carried by a generated note, rather than trusting the writers or reading a
vault some earlier run happened to leave behind. The tags it checks live only
in generated notes: `wiki/` is gitignored, so a checkout without one is not a
break, it is an ungenerated vault, and the regeneration is what makes the
check honest on one.

See [[the-graph-view-colours-by-tag-and-every-note-s-kind-tag-is-generated]]
for the call this proves.

## Alternatives considered

**Nothing — trust the preset** — how the last break survived a month of
passes. The config is edited by one tool and rewritten by another (Obsidian
owns the file after the seed), so nothing about it is stable by inspection.

**A checker inside `doctor.sh`** — the `vault` row already reads the register
and would have carried this. Rejected: an invariant that binds is the memo
format's own answer for a rule that must keep holding, and it comes with its
own command a person can run alone.

**Assert the live vault too** — `.obsidian/graph.json` is a person's file
after the seed, and their scale and forces are theirs. `repair_graph_view`
brings the three keys forward on `init` and `upgrade`; asserting them
continuously would fight a machine the user is allowed to configure.

## Consequences

- `memo verify` gains a check that regenerates the vault and then reads every
  `.md` under the board — tens of milliseconds, run on demand and never in the
  loop's hot path.
- A new note kind needs its writer to emit a tag before a group for it lands
  in the preset, or the invariant breaks on the commit that adds the group.
- It does not check the live vault, so a person who deletes their colour
  groups by hand gets no complaint — `pearde init` puts them back.
