---
title: rust-idioms-converge-on-name-the-reason-before-paying-the-co
date: 2026-09-04
type: conclusion
tags: [conclusion, error-handling, ownership, performance, rust]
sources:
  - "[[260904-e5a5]]"
  - "[[260904-a575]]"
  - "[[260904-ac72]]"
derived_from: []
---

# rust-idioms-converge-on-name-the-reason-before-paying-the-cost

Ownership, error handling, and performance rules all encode the same instinct: the compiler's default is already the cheapest correct choice, so any deviation needs a named reason before it's written. Borrow by default and clone only when a specific cause forces an owned copy — sharing, caching, an API contract. Propagate errors by default with Result and `?`, and panic only where the cause is named — a test, a provably impossible state. Leave code as the compiler produces it by default, and spend optimization effort only where a flamegraph named the cost — never on a hunch. Each rule replaces a defensive habit (a clone "to be safe," an unwrap() "it won't happen," a rewrite "this feels slow") with a requirement to name the forcing reason first.

Consequence: a reviewer challenging a .clone(), an unwrap(), or a hand-rolled optimization needs exactly one question for all three — "what forced this?" — and a line that can't answer it is the line to delete.
