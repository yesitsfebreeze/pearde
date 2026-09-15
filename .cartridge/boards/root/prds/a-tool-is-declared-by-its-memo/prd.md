---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
---

# A tool is declared by its memo — event-typed in frontmatter, executed from inline just-syntax blocks, one memo for every reader

## Outcome

A tool can be born as a memo and serve with no separate implementation: the
frontmatter declares its type by the event shape it serves (one-shot command,
watcher over an event type, and so on), and the body carries fenced code
blocks in justfile syntax that the runner extracts and executes, so the
cross-platform commands live inline in the memo. The same memo is the
documentation, the retrieval contract and the executable — the justdown
lenses: humans read the prose, the index reads the frontmatter, agents
retrieve the body, the runner executes the blocks. What a memo cannot
express stays a cartridge; what it can, is no longer written twice.

## Acceptance
- [ ] A memo whose frontmatter declares a one-shot tool type and whose body
      carries a fenced just-syntax block is discovered, described and called
      through the same `tool.*` surface a cartridge tool is — no Rust change
      to add it.
- [ ] A memo whose frontmatter declares a watcher type subscribes to the
      named event type, and its block runs per event like an event listener
      does; a one-shot never subscribes.
- [ ] The same memo serves all four readers with one source: the prose
      renders, the index reads the frontmatter, retrieval returns the body,
      and the runner executes the block — verified by changing the block and
      seeing the change in all four lenses with no sync step.
- [ ] `just check` and `just test` pass.

## Context

Decided in [[the-tool-contract-is-a-memo]] (Stefan, 2026-09-12); the shape is
justdown's — github.com/yesitsfebreeze/justdown, spec v0.1, where the fenced
`just` block *is* the tool and the frontmatter is the retrieval contract.
Sharpens [every-tool-is-one-command](../every-tool-is-one-command/prd.md) and the typed-event chain
([an-event-declares-its-type](../../../agent/prds/an-event-declares-its-type/prd.md)): the tool type in the frontmatter names the
event shape. Existing routine memos already dispatch; this memo extends the
same courtesy to tools. An analyst probing this should check what
[tool-dispatch-and-routines-are-graph-nodes](../tool-dispatch-and-routines-are-graph-nodes/prd.md) already provides for free.
