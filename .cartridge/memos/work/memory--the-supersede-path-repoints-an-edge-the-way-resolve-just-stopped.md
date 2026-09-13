---

kind: work
level: 10
status: done
description: "`supersede` re-points a deferred Rephrase candidate by writing `r.from` in place, leaving `by_from` under the old id and the content-addressed id stale — the identical move `6f52f2a8` replaced in `do_resolve` one commit earlier, with the cure already in the tree"
read_when: "touching reason edges, supersede, or writing a Check"
---

# the-supersede-path-repoints-an-edge-the-way-resolve-just-stopped

## Do

`src/graph/src/accept.rs:853-860`:

```rust
for r in memory.reasons.values_mut() {
    if r.kind == ReasonKind::Rephrase && r.from == old_id && r.to.is_empty() {
        r.from = entity_id.to_string();
        reclass.push(r.id.clone());
    }
}
```

The reason for the re-point is sound and the comment above it gives it: a
deferred contradiction candidate is orphaned when its old entity is superseded
by a different update, so it is moved onto the new active entity and queued for
re-classification. What the write does not do is everything around it.

`by_from` still lists the edge under `old_id` — the map is a
`HashMap<String, Vec<String>>` maintained only by `add_reason`/`remove_reason`
(`src/graph/src/reason.rs:59,70`), and a direct field write reaches neither.
And `reason_id` is content-addressed over `from`, `to`, `kind` and `text`
(`accept.rs:445` mints one that way), so changing `from` leaves the id no
longer matching its content — the second half of exactly what
[[resolving-a-question-edge-skips-by-to-and-its-own-id]] recorded for
`do_resolve`.

That one was closed by `6f52f2a8` the same day, and the cure is now sitting in
the tree: clone the reason, set the field, recompute `id`, `drop_reason` the
old, `add_reason` the new, `index_reason` the ownership
(`tick_loop/src/tick_tasks.rs:450-461`). `drop_reason` itself arrived one
commit before that in `0291199f`
([[removing-a-reason-leaves-it-in-the-reason-indexes]]). This site is the same
shape with neither applied.

Apply the same move here. The `reclass` list must carry the **new** id, since
`push_reclass` is what the tick loop later looks up.

## Check

A superseded entity's re-pointed Rephrase candidate is found under the new
entity in `by_from`, sits in the memory hosting its new `from`, has an id equal
to `reason_id(from, to, kind, text)`, both entities' BM25 documents are
re-derived, and the re-classification it was queued for still runs; `just all`
green.

**Done 2026-09-06 in `73258981`, and the Check above is a correction of the one
this part shipped with.** That one demanded `rg -n 'r\.from = ' src` return
nothing — a spelling, not a property — and the correct fix fails it: the
assignment survives at `accept.rs:874` on a *clone* taken out of the reasons
map, which is exactly how it should be written. A Check that forbids an
expression rather than naming the state it wants is the same error as
[[a-test-can-pin-the-defect-as-the-expectation]], pointed the other way.

The fix also carries a rule this part did not know. A memory hosts a reason if
and only if it hosts its `from` — stated in `reason.rs` — so the edge had to
move memories as well, and it is `add_reason`ed into `placed_memory_id` rather than
back where it sat. That is why `by_from` mattered twice over: it is the index
`entity_document` builds the BM25 document from, so the alternate wording had
stayed on the superseded entity and never reached the new one
([[repointing-a-rephrase-leaves-by-from-and-the-lexical-doc-stale]] is closed
by the same commit, `accept.rs:884-890` re-deriving both documents).
