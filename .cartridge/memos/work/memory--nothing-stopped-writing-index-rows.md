---
kind: work
level: 10
status: done
description: the-index-is-derived's write-back is gone — `memory compact` folds intake without touching `memos/SYSTEM.md`, and every routine's index-row instruction is deleted; the table never grows back
read_when: "touching compaction, the index, or a routine's close step"
---

# nothing-stopped-writing-index-rows

[[the-index-is-derived]] emptied the table and closed with one consequence
nobody executed: "Whatever else writes rows must stop." Nothing did.
`memos/SYSTEM.md` is 290 lines and 14,635 bytes today and already carries 11
condensed rows at lines 272-282, inserted before `### The membrane record` at
line 284 — precisely the anchor `rewrite_index`
(`src/commands/src/commands_compact.rs:443-470`) writes at
([[the-rows-grew-back-into-the-protocol]] dates the regrowth and measures it).
Each compaction writes one more pipe-delimited row per condensed file into the
middle of the protocol's prose, under no header row and no separator line, and
the daemon runs one a day. The gate does not
catch it: `tests/memos_index.rs` generates `<kind>/_index_.md` and only checks
that `SYSTEM.md` exists, so the table grows back silently in the file every
session loads through the `CLAUDE.md` symlink. `claims_parse_and_index_rewrites`
(`:524-546`) asserts the insertion, so a test holds the retired behaviour in
place.

The routines say it too, in eight places that tell a pass to write a row into a
table that is gone: `drill.md:20`, `improve.md:53`, `new-routine.md:57`,
`quality.md:162` and `:168`, `legible.md:128` and `:134`, `scout.md:65`, and
`herd.md` three times — a `rows` field in its agent schema (`:41`), the prompt
line that asks each agent for one (`:56`), and a whole step 3, "Write the rows"
(`:73-79`), that edits `memos/SYSTEM.md`'s repo table.

## Do

- `src/commands/src/commands_compact.rs`: delete `INDEX`, `INDEX_TAIL`,
  `rewrite_index` and the read/write pair at `:256-258`, and the module doc's
  "`memos/SYSTEM.md` loses their rows and gains the condensed ones" clause.
  `delink_bodies` stays — a wikilink to a folded file still fails the gate
  ([[compact-breaks-the-links-no-gate-reads]]) — and takes `memos/` directly
  instead of `Path::new(INDEX).parent()`.
- `claims_parse_and_index_rewrites` keeps its `parse_claims` and `body_of`
  assertions and loses the `rewrite_index` half with the function.
- The eight routine sites lose the row instruction. `herd.md` loses the `rows`
  schema field, the prompt line and step 3; its step numbering closes up.
  A close step that named only the row now names `just memos-check` alone.

## Check

`rg -n 'INDEX|rewrite_index' src/commands/src/commands_compact.rs` returns
nothing, `rg -n 'index row|row to the index' memos/routine/` returns nothing,
and `just test` is green. Then `memory compact` on a store with intake parts
folds them and leaves `memos/SYSTEM.md` byte-identical.
