---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `parse_claims` takes the first `[` to the last `]`, so one bracket in a preamble makes a good reply unparseable — and the caller's retry policy is built for a failure a resample would fix, which this one is not

## Do

`parse_claims` (`src/ingest/src/ingest_distill.rs:157-167`) takes the span
between the first `[` and the last `]` and parses that:

```rust
let (start, end) = match (raw.find('['), raw.rfind(']')) {
    (Some(s), Some(e)) if e > s => (s, e),
    _ => return None,
};
```

So a reply reading `Here are the claims [1]: [{"text": …}]` yields the span
`[1]: [{"text": …}]`, which is not JSON, and a good answer is discarded. The
same holds for a bracket after the array.

The caller's policy is the other half, and it is right about the case it was
written for. The doc comment above the function says `None` is "a format
failure the caller must retry, not archive", and `drain_entry` obeys it —
`record_stuck` leaves the job queued with no attempt count
([[the-intake-refuses-one-thing-permanently-and-retries-the-rest-forever]]).
For a genuine prose reply that is correct: nothing seeds the reason model on
the shipped config ([[nothing-seeds-the-completion-client]]), so the next drain
resamples and may well parse.

A preamble bracket is not that. The model writes the same shape of preamble
each time, so the span is wrong each time, and a retry policy built for
resampling spends a completion per drain forever
(`a-bracket-in-a-preamble-retries-the-delta-forever` is where this was first
seen). Fixing the span is therefore the better repair than bounding the retry:
it converts the failure back into the transient one the policy already handles,
rather than teaching the policy to give up on failures that would have passed.

Take the first `[` whose value parses rather than the first `[` at all — walk
each `[` index and try `serde_json::Deserializer::from_str(&raw[i..])
.into_iter::<Vec<Value>>().next()`, which stops at the end of the first
complete array and ignores whatever follows. That also drops the need for
`rfind(']')`, and with it the trailing-bracket case.

## Acceptance
A reply whose array is preceded by `[1]` and followed by prose parses to its
claims; a reply with no array still answers `None`; the existing
`[[…]]`-unwrap case is unchanged; `cargo test -p ingest distill` and
`just all` green.

Planning recheck 2026-09-07: the first/last-bracket implementation remains.
The proposed first parseable array is not sufficient: `[1]` itself parses,
and ignoring a later sibling array contradicts an existing retry test.
[[which-claims-array-does-distill-accept]] holds the two unanswered acceptance
questions. Do not execute this algorithm until the answers reconcile its Do
with the empty-array, nested-array, and sibling-array contracts.

Execution attempt 2026-09-09: blocked, unchanged. `parse_claims` is still the
first-`[`/last-`]` span at `src/ingest/src/ingest_distill.rs:157-167`, both
`A:` in [[which-claims-array-does-distill-accept]] are still `?`, and that
memo was not on this one's `needs:` line, which is why the scan read it as
ready — the link is now written, so the next pass puts the two questions
before it is dispatched again. What the attempt established for the answering
round: the two recommended answers do reconcile against
`src/ingest/src/tests/ingest_distill_test.rs` as it stands, under one rule —
walk the reply for non-overlapping top-level arrays (parse at each `[`, jump
past the one that parses, so a nested `[` is never a second candidate), then
take the sole candidate holding JSON objects, answer `None` when two hold
them, and fall back to the first candidate when none does. That keeps `[]`
empty, `[[a]]` unwrapped, `[[a],[b]]` an archived no-claims result and
`[a] [b]` a retry, while `[1]: [{…}]` parses. It is the shape to confirm or
reject, not a decision this session may take.

Unblocked 2026-09-09: [[which-claims-array-does-distill-accept]] is a decision
now, and the selection rule it names is what this memo executes — walk the
non-overlapping top-level arrays, take the sole candidate holding JSON objects,
`None` when two hold them, the first when none does. The retry contract stands
and `multiple_sibling_arrays_signal_retry` is not touched.

Done 2026-09-09 (`ac0459c1`, landed): `parse_claims` walks the reply's
non-overlapping top-level arrays through a `serde_json` stream deserializer —
`top_level_arrays` parses at each `[` and jumps past whatever parses — and takes
the sole candidate holding JSON objects, `None` when two hold them, the first
when none does. `citation_markers_around_the_claims_array_are_not_the_span`
covers the defect row; the other four rows of
[[which-claims-array-does-distill-accept]] were already asserted by
`genuine_empty_array_is_some_empty`, `single_nested_array_is_unwrapped`,
`len2_array_of_arrays_parses_to_empty` and `multiple_sibling_arrays_signal_retry`,
all untouched and all green. Three inverse edits proved each half: accepting the
first of two payloads reddens the sibling test, dropping the object-bearing
filter reddens the citation test, and advancing one byte instead of past the
parsed array reddens the array-of-arrays test.

`cargo test -p ingest distill` 31/31. `just all` is green apart from two reds
that predate this lane and belong to no part of it: `every_cited_path_is_there`
fails in every lane because `src/rpc/src/plan.rs:2` cites a file in a nested
repo git does not track, so no worktree but the trunk has it; and `lifecycle::a_handover_generation_stops_on_a_signal`
fails only under sibling-lane build load and passes when run alone.
