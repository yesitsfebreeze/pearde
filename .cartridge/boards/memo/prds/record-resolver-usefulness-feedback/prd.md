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
description: "Record whether resolved memory was used and whether it helped"
---

# Record resolver usefulness feedback

## Outcome

Agents can record explicit evidence about surfaced memory: whether it was used, whether the outcome succeeded, and what evidence supports that result. The resolver can later learn from usefulness rather than access frequency alone.

## Acceptance
- [x] Already met: `observe` takes a `stage` of `surfaced`, `used` or `outcome`,
      each counted separately in the `resolver` report, with `parent` chaining
      one to the next and duplicates reported rather than double-counted.
- [x] Already met: every event carries `path`, `revision`, and `target_revision`
      where the item has an external target, plus the `origin` session, run and
      call it came from.
- [x] Already met and now proven: a `surfaced` event on its own produces no
      outcome, and the report states "explicit caller reports; access counts are
      not usefulness scores".
- [x] Already met and now proven: running the report twice leaves the judged
      memo byte-identical on disk.
- [x] `every_outcome_is_recorded_and_none_is_inferred_from_access` adds the two
      outcomes nothing covered, `failure` and `cancelled`, alongside `unknown`.
      `success` and stale target revisions were already covered by
      `resolver_attributes_reports_deduplicates_and_recovers_partial_tail`.

## Approach

Probed first: the whole mechanism was already delivered — stages, parent chains,
duplicate detection, origin attribution, the stale-target refusal, and the
attribution string that refuses to read access as usefulness.

Two of the four outcomes the schema accepts, `failure` and `cancelled`, had no
test. One test in `builtin/memo/tests/resolver.rs` records a chain for each,
checks the counts and the recorded outcomes, and pins the two properties this
memo exists to protect: a surfaced event alone yields no outcome, and reporting
never edits the memo it judged.

## Result

No behaviour changed. Worth knowing for the next reader: report events nest the
recorded fields under `observation`, with `origin` beside it — not flat on the
event.
