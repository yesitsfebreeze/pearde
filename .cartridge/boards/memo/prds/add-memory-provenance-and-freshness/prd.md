---
repo: /Users/feb/dev/cartridge/memo.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
needs:
- "@memo/implement-memo-usage-resolution"
description: "Attach provenance and freshness metadata to resolved memory"
---

# Add memory provenance and freshness

## Outcome

Every resolved memory item tells the agent where it came from and what revision or digest it reflects, so retrieved context can be cited, checked for staleness, and safely re-read before mutation.

## Acceptance
- [x] Already met: every item carries `path` and a 64-character `revision`; an
      item that points outside the record also carries `target` and a separate
      `target_revision` for the file itself.
- [x] Already met: `open.kind` is `memo` for record-only knowledge and `file`
      for an external target, with `open.path` naming what to read in each case.
      The legacy `.kern` record no longer exists; it was migrated into
      `.cartridge/memos` as ordinary memos, so there is no third category left.
- [x] Proven: an exact read by reference reports the same `target_revision`
      while the file is untouched and a different one once it moves, and the
      memo's own `revision` stays put — the two digests answer different
      questions.
- [x] Already met: a write carrying an overtaken `expected_revision` is refused
      with `revision conflict: read the current memo before writing`, so a
      lesson drawn from a stale reading cannot land on top of a newer one. The
      resolver-assessment path additionally requires the revision it judged.
- [x] `every_result_says_where_it_came_from_and_how_fresh_it_is` covers the
      record-only memo, the external target, the moving file, and the refused
      stale write. `usage_validation_scope_cycles_and_revision_conflicts_are_actionable`
      already covered the conflict message itself.

## Approach

Probed first: every behaviour here was already delivered by
[implement-memo-usage-resolution](../implement-memo-usage-resolution/prd.md). What was missing was a test tying the pieces
together, and in particular one that shows the two digests are not the same
thing — a caller who conflates `revision` with `target_revision` will think a
memo went stale when only the file it points at moved.

One test in `builtin/memo/tests/resolver.rs`.

## Result

No behaviour changed. The distinction worth carrying forward: `revision` digests
the memo, `target_revision` digests the file it names, and only the second moves
when the code changes underneath a resource memo.
