---
name: pearde-drill
description: Interview a vague request into a contract ready to spec — one pass of questions covering the whole frontier at once, each carrying a recommended answer, until no answer left changes the work. Ends in a settled contract and a PRD tree, each branch a child. Use for "/drill", "drill this", "drill <prd>", "help me work out what I want", "this request is too vague", "ask me what you need to know", "turn this into a spec", "interview me about this feature", "what questions do you have before building". Run it before dispatching anything — a one-line title is too thin to spec.
---

Read @references/drill.md — one pass over the whole frontier, the shape a
question must have, what one may never say, the exact pass and answer formats,
that nothing is dispatched while a drill runs, and the tree a drill ends in.
The scope is `@@drill`. @references/templates/prd.md is the shape of each
branch written, @references/parts/contract.md the keys.

A drill works with no board in scope — an interview, whose answer is the tree
the drill would write. Say so rather than creating `prds/` uninvited.
