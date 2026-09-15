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

# extend the parts gate from SYSTEM.md to part bodies, once the convention decides how a part quotes the syntax without citing it

## Do

`tests/memos_index.rs` resolves the links in `SYSTEM.md` and nothing else, so a
body link naming no file passes and the fold turns it into an edge to nothing
([[the-parts-gate-checks-links-in-one-file]]).

The code half of the decision is settled — [[a-code-citation-is-backticked]]
wrapped every citation in `src/**/*.rs`, and the body half is unchanged by it. A body checker must tell a
citation from the four other shapes a doubled bracket takes in this record — a
part quoting the syntax to explain it, a placeholder standing for any name, an
ellipsis used as punctuation, and a bracketed `file.rs:line`. The parts that
quote the syntax are exactly the parts about linking, so the collision is not
incidental and cannot be scanned away. One convention settles both gates; guess
it here and the two will disagree.

Then: resolve body links with `ingest_wikilinks::wikilink_names` rather than a
pattern of the gate's own, so what the gate checks is by construction what the
fold folds. Two extraction rules for one syntax is how the counts came out 20,
23 and 16 for the same record.

Sixteen edges to nothing were listed in
[[the-parts-gate-checks-links-in-one-file]] under a looser pattern; the gate
landing red on whatever the extractor actually finds is correct and they are
repaired as part of this, not before it.

Landed: the convention is [[a-body-citation-is-backticked]] — the backtick
marks the quote in a body as it marks the citation in code, and the gate defers
to `wikilink_names` rather than restating it. `check` resolves the body links of
every indexed part and of `SYSTEM.md` against every leaf the walk finds, and
`the_gate_can_go_red` proves both directions: a bare `[[nowhere]]` fails, a
backticked one beside it does not. Re-derived under that rule the record carried
two, not sixteen — a bracketed `ingest_file_watcher.rs:218` and a bracketed
`[[name]]` placeholder — both repaired by backticking. The rest of the earlier
count was code spans two scanners read as prose.

## Acceptance
`cargo test --test memos_index` fails on a body link that names no file and on
the sixteen currently present, passes once they are repaired under the chosen
convention, and the gate calls `wikilink_names` rather than matching its own
pattern.
