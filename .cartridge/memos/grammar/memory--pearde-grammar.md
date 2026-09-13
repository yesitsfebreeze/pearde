---
kind: grammar
first: "2026-09-02 05690dfd"
description: the sibling board that runs PRDs and specs through agents
read_when: "meeting `pearde` in the code or the record, or naming something near it"
---

# pearde

The board this record cites for the frontmatter contract and the analyst /
implementer split, and the source of the `pearde-*` agents ([[PRINCIPLE]]). It
is the one sibling tree that types a file by its filename and folder rather
than a `kind:` field, which is why it needs its own parser — cited here as the
exception that argued for [[kind-grammar]]. Sits next to
[[membrane-grammar]], [[kind-grammar]].
