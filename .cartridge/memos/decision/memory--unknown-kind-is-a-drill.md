---
kind: decision
status: decided
description: the first time the fold meets a kind with no kind file, it creates one and drills the user for what the kind means; states, transitions and their gates are answers in that drill
read_when: "touching the fold, kinds or state machines"
date: 2026-09-05
subject: an unknown kind is not an error but a drill; the fold writes a kind file skeleton and asks the user, one question at a time, what a node of that kind is, which keys it requires, which states it has, which verb moves it between states and under which gate, and how it renders; transitions live in the kind file the drill produces
---

# unknown-kind-is-a-drill

## Decision

When pass one of the fold finds a node whose `kind` has no kind file in any
store, it does not fail. It writes a kind file skeleton into the repo store
and starts a drill: one question per turn until the kind is described.

The drill asks, in order:

1. What is a node of this kind, in one sentence.
2. Which keys must every node carry; which may it carry.
3. Which of those keys are edges, and to which kinds they point.
4. Does it have a `state`; if so, which states.
5. For each state, which verb moves it where, and what must be true first.
   Each answer becomes one row of a `transitions` table: `from -> to : verb,
   gate`. The gate is a predicate the guard can run.
6. How a node of this kind renders in a brief: whole, snippet, tool
   definition, guard row, or not at all.

`mem task claim <id>` and every other state verb is generic: it reads the
kind's `transitions` table, evaluates the gate as a rule, and writes the new
state. Any kind with states gets its verbs from the table, and the state key
is written by that verb alone.

Until the drill is complete the kind file carries `status: draft`, its nodes
index but do not render, and every fold reports the open questions.

## Why

Mitosys made an undeclared type an error. That is right for a plugin host
where a type without an owner has no reader. Here the reader is the fold and
the author is a person: the moment a new kind appears is the moment they know
best what it means, and a drill captures that while it is fresh. Pearde's
nine states and their gates were prose in `references/memos/states.md` that
the tool enforced separately; here the table and the enforcement are one file.

## Consequences

- A kind file is the only place a state machine lives. There is no
  transitions code per kind.
- A gate is a rule predicate, so the same guard that runs on tool calls runs
  on state changes.
- A drill is itself recorded: each answer appends to the record, so the
  navigator later knows why a kind is shaped as it is.
