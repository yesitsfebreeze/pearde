---
kind: work
description: Keep memory writes validated, atomic, and revision-aware
status: done
needs:
  - "[[@prd/work/memo--implement-memo-usage-resolution.md]]"
---

# Validate safe memory writes

## Outcome

Agents update durable memory through validated, atomic writes that respect declared types and expected revisions, preventing casual or stale mutation of project knowledge.

## Check

- [x] Already met: `nope/x.md: undeclared kind nope` and `note/x.md: description
      required`, each naming the path and the missing thing.
- [x] Already met: a stale `expected_revision` gives `revision conflict: read the
      current memo before writing`; covered by
      `usage_validation_scope_cycles_and_revision_conflicts_are_actionable`.
- [x] Already met: `../outside.md: expected <kind>/<name>.md with lowercase
      names`, `work/the-vision.md: duplicate memo leaf`, and the undeclared kind
      above.
- [x] Already met: a `kind: resolver` assessment requires a nonempty `evidence`
      list and the digest of the revision it judges;
      `observations_need_context_and_assessments_need_evidence` proves an empty
      list is refused.
- [x] `a_refused_write_leaves_the_memo_on_disk_untouched` closes the one gap:
      refusal by record validation, by the revision guard, and by cancellation
      each leave the file byte-identical, and an accepted write replaces it
      whole with nothing of the original left.

## Approach

Probed first: four of the five boxes were already delivered. Live writes against
the workspace record gave clear, actionable refusals for an undeclared kind, a
missing description, a path outside `<kind>/<name>.md`, a duplicate leaf and a
stale revision, and the resolver-assessment path already demands evidence.

The gap was proof of atomicity. `record.rs` validates the whole record and then
calls `atomic_write`, so a refusal cannot leave a partial file — but nothing
asserted it, and that is exactly the property a reader of this memo needs to
trust. One test in `builtin/memo/tests/tests.rs` exercises each refusal stage,
including cancellation, which is checked at the last moment before the write.

## Result

No behaviour changed; the guarantee is now proven rather than asserted. The
cancellation case matters most: it is the only refusal that happens after
validation has passed, and so the only one where a half-written file was ever
conceivable.
