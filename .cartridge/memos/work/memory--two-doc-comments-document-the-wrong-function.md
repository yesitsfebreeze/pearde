---
kind: work
level: 10
status: done
description: the contentless-reap change inserted each new function between an existing doc comment and the function it described, so `is_contentless` and `reap_contentless` carry someone else's docs and `score_noise` and `forget_by_source` carry none
read_when: "picking up work, or adding a function next to a documented one"
---

# two-doc-comments-document-the-wrong-function

## Do

Both files are in the working tree uncommitted, from the change that closed
[[@prd/work/memory--empty-entities-leave-the-graph.md]], and both have the same slip.

`src/hygiene/src/hygiene.rs:173-181`:

```
/// Score one thought's text for noise likelihood. `confidence` is the caller's
/// importance signal (memory: the Beta posterior mean) — below 0.2 is itself a
/// weak noise signal, mirroring mnemosyne's `low_importance` rule.
/// A thought carrying no word and no number. `""` is the obvious case; ...
pub fn is_contentless(content: &str) -> bool {
```

`score_noise` follows at `:185` with no doc comment of its own.

`src/graph/src/graph_ops.rs:137-148` is the same shape: the paragraph
explaining what `prefix` widens — "thousands of exact calls is not a cleanup",
the sentence [[the-cleanup-could-only-reach-one-scheme]] quotes — sits above
`reap_contentless`, and `forget_by_source` at `:167` has none.

Split each block: the first paragraph moves down to the function it describes,
the second stays. Fold it into the uncommitted change rather than making a
separate commit — the same hand wrote both.

Nothing would have caught it. Rustdoc has no way to know a comment describes a
different function, and nothing runs its lints anyway
([[@prd/work/memory--the-record-citation-breaks-rustdoc.md]]). It is the same failure as a stale
citation (`a-citation-rots-quietly`) with the pointer running the other way:
there the comment named code that moved, here the code moved under the
comment.

**Done 2026-09-06, by the hand that made it.** Both blocks split: the first
paragraph moved down to the function it describes, the second stayed with the
newcomer. `score_noise` (`hygiene.rs:203`) and `forget_by_source`
(`graph_ops.rs:163`) carry their own docs again; `is_contentless` and
`reap_contentless` carry only theirs.

The direction is what makes this worse than the citation rot it mirrors. A
stale citation names something that moved, and is wrong on its face once
followed. A displaced doc comment is a **true paragraph attached to the wrong
subject** — nothing in it is false, so it reads as correct to any reader who
does not already know what the function does, which is exactly the reader a doc
comment is for.

## Check

`forget_by_source` and `score_noise` each carry their own doc comment, and
`is_contentless` and `reap_contentless` carry only the paragraph that describes
them. `just check` green, suite 1,248 passed.
