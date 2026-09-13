---
kind: work
level: 10
status: open
estimate: 4h
description: Retrieval degradation weakens the evidence path identified by its documented query handle rather than an unrelated entity neighborhood
read_when: correcting bad recall with degrade or reconciling its schema with behavior
---

# degrade-corrects-the-retrieval-path-it-names

## Do

A documented retrieval-feedback handle identifies the actual bad retrieval path
whose reasons are to be weakened. Feedback cannot silently reinterpret a query
identifier as a thought identifier or weaken unrelated incident edges. Invalid,
expired, or cross-store handles fail explicitly without mutation; unrelated
retrieval evidence remains unchanged.

The 2026-09-09 inspection found a mismatch between the advertised query_id
contract and an implementation resolving that value as an entity. The completed
[[@prd/work/memory--mcp-tools-declare-their-schema.md]] work does not by itself settle the semantic
contract. The analyst must establish what provenance retrieval actually retains
before selecting the repair, rather than inventing a path from an arbitrary ID.

The result is one coherent public feedback contract across tools and documented
callers, not another parallel degradation operation.
