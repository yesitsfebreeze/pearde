---
kind: work
level: 10
status: done
description: entities whose whole text is `---` or the empty string rank in the top three of a real recall, and `audit` scores them 1.0 for deletion while nothing deletes them
read_when: "reading audit, or asking why recall returns nothing"
---

# empty-entities-leave-the-graph

## Do

Two reads on 2026-09-06 over this repo's store. `query {text: "why is the
delivery floor default 0.0"}` returned as its third hit, score 1.104, an entity
whose entire text is `---` — a part's frontmatter delimiter ingested as a
thought — and `log` shows `added document ''` rows arriving the same minute.
`audit {limit: 3}` names them exactly: three `document` candidates,
`"action": "delete"`, `"reasons": ["empty_content"]`, `"score": 1.0`, empty
preview.

So the classifier already finds them and the recall path still ranks them. The
audit is a read; nothing acts on what it returns. The LLM then writes edges
between them — `"There is no specific connection between these two pieces of
knowledge as both are currently undefined."` is a real reason text from this
store — so each empty row also costs reasoning calls and edge weight.

Give the reap a caller: `gc` already runs a live reap of empty and orphan memories
and is the verb that should take the `empty_content` candidates with it, at the
score the audit already assigns. The write-time half belongs to
`what-should-the-hygiene-gate-default-to` and is not settled here; this item
removes what is already in.

Distinct from [[@prd/work/memory--finish-the-store-the-doctor-found.md]], which repairs unkeyed
thoughts and dangling edges — these rows are keyed, live and empty.

**Done 2026-09-06, in two halves, and the caller alone would not have been
enough.** `score_noise` and `classify_write` both tested
`content.trim().is_empty()`, and `---` is not empty by that test — so the row
that ranked third was never an `empty_content` candidate and a caller on the
candidates would have left it exactly where it was
(`the-audit-cannot-see-what-ranks-first` measured that from the other side).
`hygiene::is_contentless` is the test now — no alphanumeric character anywhere,
so `""`, `---`, `''` and `#` all qualify — and both classifiers call it, which
also means the write-time gate would refuse those rows once anyone turns it on.

The caller is `graph_ops::reap_contentless`, run by `gc` **before** the memory
pass in both the routed and the no-daemon path. The order is load-bearing:
reaping the thoughts is what empties the memories, so a memory pass running first
leaves behind the memories the same `gc` just emptied. `tool_gc` answers
`reaped_entities` beside `reaped`.

**Facts are immune, deliberately.** The reap passes
`Removal::Explicit { force: false }`, so an empty Fact survives and stays
visible to `audit`. That is one case the Check below does not reach: an empty
Fact is a curator's problem, and a sweep should not be the thing that decides
it.

## Check

`audit` answers no candidate whose reason is `empty_content` after one `gc`
over this store — except a Fact, which the reap spares — and a `query` for a
common term returns no entity whose text is empty or `---`. Held by
`the_reap_takes_a_thought_with_no_word_or_number_and_spares_a_fact`
(`src/commands/src/tests/commands_graph_ops_test.rs`): a blank and a `---` go, a
real claim stays, a whitespace-only Fact stays. The suite read 1,235 passed.
Not yet run against this repo's own store — that is a real deletion on a store
under measurement, and it waits for the curator.
