---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `source_id()` hashes the section and `forget_by_source` ignores it, and the ingest tool lets a caller set one — decide which identity is the identity, then make both removal paths use it

## Do

`two-identities-for-one-source` measured it and the correction of 2026-09-06
made it live rather than latent: `section` is an advertised parameter on the MCP
`ingest` tool, `src/rpc/src/server.rs:1651` writes it into a `Source::File`, and
from that moment the file's two removal paths key on different things.

- `tombstone` resolves `source.source_id()`, which hashes
  `scheme \0 object_id \0 section`, so a file-delete retires only rows whose
  section matches the one the watcher used — the empty string.
- `forget_by_source` compares scheme and object_id and never reads the section,
  which is the "takes all sections" contract `operations` states.

Deleting a file therefore stops retiring rows an agent ingested against that same
path with a section, while an explicit forget still reaches them. Nothing fails;
the counts simply disagree.

Decide first, because the two paths cannot both be right:

- **Section-blind everywhere.** The file is the unit of removal. Cheap, matches
  the stated contract, and loses the ability to retire one section of a document
  — which nothing currently does.
- **Section-exact everywhere.** The section is provenance and part of identity.
  Then `forget_by_source` must take a section, and the contract in `operations`
  is wrong rather than the code.
- **A file has no section.** Reject or ignore `section` when `source == "file"`
  at the operation boundary, leaving `Source::Session`'s per-turn sections as the
  only sectioned kind. Smallest change, and it makes the agreement structural
  instead of conventional.

Option three is cheaper than it looks, and this is measured rather than assumed:
**nothing in the ingest ever sets a section on a `Source::File`.** Chunk identity
does not use the field — `chunk_source_id` (`ingest_place.rs:403`) appends
`#chunk{index}` to the whole `source_id`, deliberately, because "section-only ids
collide across documents, so chunk 0 of every source superseded chunk 0 of the
previous one — silent data loss". So chunks are built *on top of* `source_id`,
not inside its section, and refusing a section on a file source would break
nothing that exists. The only writer of one is a caller of the operation.

Do not pick by taste: `Source::Session` already carries per-turn sections
(`ingest_intake.rs:192-203`), so whichever rule is chosen has to hold for both
kinds or say why they differ. And there is a fourth option the three above hide:
the section belongs in the *object id* for both kinds, which makes one identity
by construction and needs no rule about who may set what. It is the largest
change of the four and the only one that removes the question rather than
answering it.

## Acceptance
A test ingests a `file` row with a non-empty section, deletes the file, and
asserts the row is retired — or asserts the operation refused the section,
depending on the decision. `rg -n 'section' src/rpc/src/server.rs` and the
`ingest` tool schema agree with whichever was chosen, and `just all` is green.

Option three landed: `validate_ingest` (`src/rpc/src/server.rs`) refuses a
non-empty `section` when `source == "file"`, so the file's path is its whole
identity and `tombstone_source`'s exact `source_id` and `forget_by_source`'s
scheme+object selector name the same rows. `Source::File.section` and
`graph_ops`'s selector comment say so where they are read,
`tool_ingest_refuses_a_section_on_a_file_source`
(`src/rpc/src/tests/server_mutate_test.rs`) pins the refusal and pins that it
is scoped to files — `Source::Session` keeps its per-turn sections, and no
delete leg exists to disagree with them. `operations` states the refusal on
`ingest` and no longer reads the two paths as divergent.
