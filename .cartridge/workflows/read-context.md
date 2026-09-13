---
atomic: read-context
subject: read context
date: 2026-09-13
tags:
  - atomic
---

## Do

Read owner instructions, root and owner PRDs, accepted decisions, assessment and source code. Resolve dependencies from the root board.

Apply the [artifact placement rule](../boards/root/README.md#keep-cartridge-roots-small): all
Cartridge-authored Markdown, including memos, tool documents and reports, belongs
inside the owning `.cartridge/`. Choose that path before creating any artifact.

Resolve historical IDs through [the work map](../boards/root/work-map.json). Select the
canonical leaf, preserve an existing source claim, and read its inherited review
history. A parent coordinates children; it is not another implementation ticket.

## Done when

The owner, intended behavior, dependency status and relevant source revisions are recorded.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Missing source or unresolved dependency | Context cannot establish the contract | Stop this step; record the evidence and resolve the named cause before continuing. |
