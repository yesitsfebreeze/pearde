---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
needs:
- "@memory/read-when-is-frontmatter"
estimate: "4h"
actual: "2h"
---

# the gate walks `memos/` and generates the index rather than checking a typed copy of it — the table leaves SYSTEM.md, `index.json` is emitted, and the fold's own wikilink parser replaces the gate's second copy

Second half of [[the-index-is-derived]], and it lands only after
[read-when-is-frontmatter](../read-when-is-frontmatter/prd.md) — until every part carries its own
`read_when`, generating the table would lose that column.

## Do

- `src/ingest/src/ingest_wikilinks.rs`: `wikilink_names` becomes `pub`.
  It is `pub(crate)` in a `pub mod`, so nothing outside the crate can
  call it today.
- `tests/memos_index.rs`: delete `index_links` and call `wikilink_names`.
  The gate's copy takes any `[[...]]` of plain ASCII and does not strip
  code, so a part quoting the syntax links to its own examples; the
  fold's strips fenced blocks and inline spans first, which is the
  convention [[how-does-a-part-quote-a-wikilink]] settled and the ingest
  side already implements.
- The gate stops requiring `[[stem]] |` per part. It walks `memos/`,
  reads each front matter, and builds the rows. The remaining claims
  stand unchanged: a kind is declared by a `kind: type` part in `system/`,
  a part's folder is its kind, a part carries one claim, and a link
  resolves to exactly one file — the last now checked over part bodies,
  not SYSTEM.md alone, which is what [the-gate-reads-body-links](../the-gate-reads-body-links/prd.md) asks
  for and what its own note says was blocked on the quoting convention.
- The generated index is written to `memos/index.json` — one object per
  part, `leaf`, `kind`, `description`, `read_when`, and the leaf names it
  links to. This is the machine surface; a consumer reads it instead of
  parsing Markdown.
- `memos/SYSTEM.md` loses the table and keeps its 231 lines of protocol.
  Its closing line names `memos/index.json`.
- Whatever else writes rows stops: `compact`'s table rewrite has no
  target, and [part-write-indexes-a-new-part](../part-write-indexes-a-new-part/prd.md)'s append is retired by
  [[the-index-is-derived]] rather than built.

## Acceptance
`cargo test --test memos_index` is green with the table absent, and the
gate's own red fixture still fails for an undeclared kind, a wrong
folder, a non-atomic part and a link resolving to two files — proved by
driving each case, since a gate that walks its subjects cannot report
failing short ([[a-gate-that-walks-cannot-fail-short]]).
`memos/index.json` parses and holds one entry per part the gate checks,
the count printed beside it. `wc -c memos/SYSTEM.md` is under 40,000, so
the `CLAUDE.md` symlink loads within the harness limit that refused it.
