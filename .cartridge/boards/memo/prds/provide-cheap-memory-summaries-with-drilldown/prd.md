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
description: "Return concise resolved-memory summaries with explicit drill-down paths"
---

# Provide cheap memory summaries with drill-down

## Outcome

Resolver responses are concise by default but include enough path and revision information for an agent to read the full memo or file only when needed.

## Acceptance
- [x] Already met: `description` and `excerpt` are each clipped to 512 bytes, so
      a long memo costs the same as a short one.
- [x] Already met: every item carries `path`, plus an `open` hint naming whether
      to read the memo or the file it points at.
- [x] Already met: `limit` bounds the page at 1..20 with a `cursor` for the rest,
      and `max_output_bytes` bounds the whole response at the service boundary.
- [x] Already met: `read` on the item's own `path` returns the full body; no
      second resolve is needed.
- [x] `summaries_stay_small_pages_stay_bounded_and_the_cap_is_actionable` closes
      the gap: a 3200-byte memo comes back as a 512-byte excerpt whose path
      reads the whole thing; nine matches page at three with an honest `total`,
      `more` and `cursor`; and a 1024-byte cap refuses with "reduce list limit or
      read individual memos".

A measured page: one item is about 1.7 KB, five about 7 KB, twenty about 25 KB.

## Approach

Probed first: all four behavioural boxes were already delivered. What was missing
was proof — nothing exercised the 512-byte clip, the paging of a large match set,
or the output cap, so all three could have regressed silently.

One test in `builtin/memo/tests/resolver.rs` covers the three together, going
through `Service` for the cap because that bound lives at the service boundary
rather than in the record.

## Result

No behaviour changed. The cap's message is worth keeping as it is: it refuses and
says what to do instead, rather than truncating a response into something that
still looks complete.
