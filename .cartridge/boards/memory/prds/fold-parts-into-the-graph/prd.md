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

# item 6 of working-with-memory — parts become entities plus edges through a Node source, the interim script retires

From [[working-with-memory]] item 6, shaped by `the-parts-fold`. Level 9: it
is four focused changes, not one, and each child is level 10.

## Do
Nothing directly. `subwork:` — in this order, each child's `Check` standing
on its own:

- [node-source-reads-frontmatter](../node-source-reads-frontmatter/prd.md) — the reader and the `Source` kind.
- [kind-is-a-field](../kind-is-a-field/prd.md) — `kind` off the source title, onto the entity, format
  version byte moved.
- [wikilinks-become-edges](../wikilinks-become-edges/prd.md) — one `link` edge per `[[name]]` in a body.
- [retire-the-parts-ingest-script](../retire-the-parts-ingest-script/prd.md) — `scripts/parts_ingest.sh` and the
  `just memos-ingest` recipe deleted once the watcher carries the record.

## Acceptance
Every child `status: done`.

Done 2026-09-05: all four children `status: done`. The last one found the
carrier the fold assumed was missing; `the-watcher-watches-parts` is the
decision that closed it.
