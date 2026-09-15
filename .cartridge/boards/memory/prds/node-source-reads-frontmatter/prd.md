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

# a Markdown file's front matter is split from its body, and the body is what a document entity carries

From [fold-parts-into-the-graph](../fold-parts-into-the-graph/prd.md). First child; nothing else starts before
it.

## Do
`ingest_worker::split_front_matter` returns `(kind, description, body)` for a
Markdown file, empty keys and the whole text when there is no fence. Both
file-origin paths call it — the watcher sink (`ingest_file_watcher.rs`) and
`drain_document` (`ingest_intake.rs`) — so the document entity's text is the
body and a part's `description` becomes the source title in place of the bare
file name.

No new `Source` variant. The drill's `Do` named `Source::Node { path, kind,
description }`; the code refuted it. `Source::File` already carries path,
title, commit and url, `origin_id()` already answers the path so two parts
never merge and two revisions of one part do, and a new enum variant would
have moved the format version byte to buy nothing. `kind` has no home on the
entity until [kind-is-a-field](../kind-is-a-field/prd.md), which is why the reader returns it and
nothing stores it yet.

## Acceptance
`just build && just check && just test` green.
`tests/e2e/part_front_matter.rs`: a part queued into the intake and
drained is recallable by its body, and `kind: decision`, `description:` and
the fence appear in no hit; a Markdown file with no fence keeps its whole
text.

Landed 2026-09-05 in `f7fcc53`. `split_front_matter` sits beside
`is_front_matter` in `ingest_worker.rs`; the watcher sink and
`drain_document` are its two callers. `tests/e2e/part_front_matter.rs`
holds both legs — a drained part is recallable by its body with no front
matter in any hit, and a fenceless Markdown file keeps its whole text.
Measured at the close: 1095 Rust tests pass, e2e 71 passed / 1 failed, that
one being `test_hub` and the unbuilt `memory mcp`.
