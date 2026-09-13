---
kind: ideas
description: A task receives a bounded deterministic shortlist of relevant capabilities without losing access to other tools
read_when: preparing worker context or reducing irrelevant tool discovery
---

# task-briefs-suggest-relevant-capabilities

Deferred on 2026-09-09 during the proxy-first work review. This is a later possibility, not a requirement for the first usable core revision. The original proposal and constraints below are retained; no acceptance or implementation completion is claimed.

A worker brief names a small deterministic set of capabilities relevant to the
task's already-declared scope. Suggestions retain their canonical descriptions,
explain omissions when capped, and are empty when nothing matches. The complete
authorized surface remains callable: a suggestion is neither permission nor a
reason to hide an unrelated tool.

Pearde's executable brief preparation is the reference: declared task paths and
capability metadata select a bounded shortlist without a model chooser. Existing
registries remain authoritative. This work introduces neither another navigator
nor a worker-footprint system previously rejected by
[[@prd/decision/memory--the-pearde-workflow-is-the-work-record.md]].

[[@prd/ideas/memory--routine-briefs-carry-bounded-ingredients.md]] owns procedure expansion;
[[deferred-tools-remain-discoverable-and-callable]] owns optional schema deferral.
The benefit is fewer discovery calls on equivalent tasks, not more instructions.
