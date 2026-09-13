---
kind: work
level: 10
status: done
description: twenty-seven comments cite `RECALL_PLAN F*` and `rekey-existing-stores spec01/02/03` — design documents that exist nowhere in the tree or the record
read_when: "picking up work, or following a plan tag in a comment"
---

# the-plan-citations-name-no-document

## Do

Comments across thirteen files cite two design documents by name and section:
`RECALL_PLAN F2a`, `F2c`, `F4`, `F5`, `F5b` and `rekey-existing-stores spec01`,
`spec02`, `spec03`. Neither string appears anywhere in `memos/`, and `docs/`
was deleted by `the-registers-collapse`, so a reader following one lands
nowhere. They are not path citations, so `tests/cited_paths.rs` cannot see them
(`a-citation-rots-quietly`).

The sites, `rg -n 'RECALL_PLAN|spec0[123]' src tests`:
`src/graph/src/graph.rs` (4), `src/graph/src/diskann.rs` (2),
`src/graph/src/graph_ops.rs`, `src/graph/src/accept.rs`,
`src/graph/src/tests/graph_test.rs` (2), `src/config/src/config.rs` (2),
`src/config/src/tests/config_test.rs` (2), `src/store_core/src/lib.rs`,
`src/commands/src/commands_admin.rs`, `src/commands/src/commands_graph_ops.rs`,
`src/commands/src/tests/commands_doctor_test.rs`,
`src/commands/src/tests/commands_admin_test.rs`,
`src/ingest/src/tests/truthful_placement_probe.rs`.

Decide first, then edit: a tag naming a document nobody can read is either
replaced by the record part that carries the same decision — F4 is the DiskANN
spill, which `persistence` and `graph-store` describe — or the sentence
stands on its own reasoning and the tag is struck. Do not invent a part to
receive them.

Re-counted 04:20 on 2026-09-06: `rg -n 'RECALL_PLAN|spec0[123]' src tests`
answers **27 lines across 13 files**, not the nineteen across nine this part was
written with. The gap is one file the first sweep did not reach —
`src/ingest/src/tests/truthful_placement_probe.rs` carries 8 of the 27 on its
own, more than any other. Quote the re-count, and re-run the `rg` before
starting rather than sizing the job from this list
(`one-reading-is-not-a-measurement`).

Why the first sizing missed a third of it: the sweep was
`rg -n 'RECALL_PLAN|spec0[123]' src tests | head -20`, and the part was written
from that truncated listing rather than from the count. `head` cut the tail
alphabetically, and `truthful_placement_probe.rs` sorts last. Nothing about the
file or the path hid it — the reader stopped. Same family as
`clippy-stops-at-the-first-failing-crate`, self-inflicted, an hour after
writing that part.

Its eight are one cluster, not eight judgments: they are section banners
(`==== spec01: ... ====`) naming the probe's test sections after the spec
sections they discharge. One decision covers the file, and it is the cheapest
third of the job — start there.

Not done in one sitting on 2026-09-06 because six of those files were held by
other sessions.

**Done 2026-09-06, and 27 sites needed two decisions rather than 27.**

*Replace, 10 sites.* Every `RECALL_PLAN F4` is the DiskANN spill, which
`persistence` describes, so each now cites it. Checked first that a code
comment citing a part by wikilink was already idiomatic rather than establishing
a convention by being the first: ``who-writes-where`` (`commands_route.rs:9`),
``operations`` and ``wire``
(`commands_mcp.rs:19`, `:96`). Sites: graph.rs ×4, diskann.rs ×2, graph_test.rs
×2, config.rs, config_test.rs.

*Strike, 17 sites.* `F2a` ×2, `F2c`, `F5`, `F5b`, and every `spec01/02/03`. In
each the sentence already carried its whole reasoning and the tag did no
referential work — the probe's eight are section banners, where
`==== spec01: the second Outcome names itself ====` loses four characters and
nothing else.

One site was rewritten rather than cut: `accept.rs:909` read "spec03 still names
the variant `Rekeyed` for that reason", where the tag was explaining why a name
exists. It now reads "which is why the variant is still named `Rekeyed`" — the
same fact, and it keeps the name's historical origin that a bare strike would
have lost.

No part was invented to receive a tag, per the `Do` above. `F2a`, `F2c`, `F5`
and `F5b` have no record part carrying their decision, and manufacturing one to
hold a citation would be worse than the citation.

## Check

`rg -n 'RECALL_PLAN|spec0[123]' src tests` returns nothing, and `just all` is
green. Both hold: the sweep answers nothing, and `check`, `memos-check` and the
suite at 1,239 passed are green.
