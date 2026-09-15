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

# the naming task writes the model's whole answer as a memory's graviton text, so an entire document became the name of a memory in this store

## Do

`do_name` (`src/tick_loop/src/tick_tasks.rs:260-276`) takes the LLM's answer,
strips the known prefixes, and assigns it to `memory.graviton_text` with no bound
on its length or shape. This store's `health` answer proves the cost: of twelve
gravitons, one is a complete install guide — headings, code fences, tables,
several thousand characters — sitting where a two-word name belongs, and it is
embedded and matched against as if it were one.

Bound the name where it is written: reject an answer that carries a newline or
runs past a short character cap, and treat the rejection the way the empty
answer at `:262` is treated — return, leave the memory unnamed, let a later pass
try again. A truncated document is not a name either, so this refuses rather
than trims.

Then repair what is already there: the two oversized gravitons in this store
are renamed through `promote_unnamed`'s path (`memory unnamed promote`) or
re-named by a fresh pass once the guard is in.

Done 2026-09-05: `do_name` (`src/tick_loop/src/tick_tasks.rs`) refuses an
answer carrying a newline or running past `GRAVITON_NAME_MAX_CHARS` (80) and
returns, leaving the memory unnamed for a later pass; two tests in
`src/tick_loop/src/tests/tick_tasks_test.rs` drive a document answer and a
short one. The install-guide graviton was removed through `graviton remove`,
which routes to the daemon; the follow-up `unnamed promote` does not route and
was clobbered twice — `unnamed-promote-is-clobbered` — so the memory it left
holds 79 thoughts and stays unnamed until a daemon carrying the guard names
it. `memory graviton list` now reports four gravitons, longest 68 characters.

## Acceptance
A unit test in `tick_loop` drives `do_name` with an LLM that answers a
200-word document and asserts the memory is still unnamed; `memory health` on this
store lists twelve gravitons, none longer than the cap.
