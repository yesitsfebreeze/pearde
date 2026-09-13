---
kind: ideas
description: A routine brief includes its explicitly declared ingredients within a hard output bound and preserves source pointers
read_when: routine invocation still requires repeated ingredient discovery
---

# routine-briefs-carry-bounded-ingredients

Deferred on 2026-09-09 during the proxy-first work review. This is a later possibility, not a requirement for the first usable core revision. The original proposal and constraints below are retained; no acceptance or implementation completion is claimed.

A routine invocation supplies the prepared context it explicitly declares, not
only instructions to rediscover it. Included ingredients carry source identity,
duplicate references appear once, missing ingredients are named, and content
beyond the budget remains reachable through exact pointers. Cycles and oversized
inputs cannot cause unbounded expansion. Unrelated links are not an instruction
to traverse the whole record, and ingredient text cannot grant additional powers.

[[routine-is-prepared-context]] states the existing principle. Pearde's executable
workflow expansion with a hard ceiling and pointer fallback is the reference;
its particular size limit is evidence, not an unmeasured Memory default. Canonical
memos remain the single source, with no copied procedure registry.

[[@prd/ideas/memory--task-briefs-suggest-relevant-capabilities.md]] owns capability suggestions. A
routine with its ingredients available should require fewer discovery calls than
the same task with only its body, without increasing context without bound.
