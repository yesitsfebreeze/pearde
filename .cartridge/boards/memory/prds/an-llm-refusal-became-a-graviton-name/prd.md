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

# two memories in this store are named "The given thoughts are empty, so no theme exists." — the naming pass stores whatever the model answers, and the length bound is the only filter

## Do

`memory health` on 2026-09-06 lists two memories named
`The given thoughts are empty, so no theme exists.` and one named
```` ```json ````. These are not names; the first is the model declining the
naming prompt and the second is the opening fence of a code block it wrapped its
answer in. Both were stored as the memory's graviton text and both now appear in
the graviton list `health` prints and in every place a memory is identified by
name.

[a-graviton-name-is-bounded](../a-graviton-name-is-bounded/prd.md) closed the neighbouring hole — a name is one line
under 80 characters or the memory stays unnamed — and both of these pass that
bound comfortably. Length was never the problem: the naming pass treats any
short single line as a name, so a refusal sentence and a markdown fence are
indistinguishable from a title. Add the two filters the observed failures name,
in the same place the length bound lives (`src/tick_loop/src/tick_tasks.rs:260`):
strip a fenced wrapper before reading the answer, and refuse an answer that is a
sentence about the prompt rather than a title — the observed one ends in a full
stop and contains "thoughts", the prompt's own word. An unnamed memory is the
correct outcome for both; [unnamed-promote-routes-to-the-daemon](../unnamed-promote-routes-to-the-daemon/prd.md) is how a
person names it afterwards.

## Acceptance
`memory health` lists no memory whose name begins with a code fence or ends in a
full stop, and a unit test feeds the naming pass both observed strings and
asserts the memory stays unnamed.

**Done 2026-09-06, on the writing half only, and the Check is narrowed to say
so.** `is_name_shaped` (`src/tick_loop/src/tick_tasks.rs:39-41`) refuses a name
ending in `.` beside the newline and length bounds, and `strip_name_prefixes`
(`:43-52`) unwraps a fenced answer before the `Theme:`/`Name:` pass, so a bare
```` ```json ```` reduces to the empty string and the memory stays unnamed. Held
by `a_refusal_and_a_code_fence_leave_the_memory_unnamed`, which feeds both
observed strings verbatim.

The `Do`'s other suggestion was refused with a better argument than it was made
with: matching "contains the prompt's own word `thoughts`" breaks the moment the
prompt is reworded, while a trailing full stop is a property of the answer's
shape.

**That filter is narrower than the class it is aimed at, and knowing so is worth
more than widening it blind.** A refusal without terminal punctuation — "The
thoughts are empty" — passes every check here, because the rule keys on the one
property the two observed strings happened to share. Refusing the prompt-word
rule for overfitting and then keying on sentence-final punctuation is the same
error one step further out: both are properties of the samples, not of refusals.
What a refusal actually is — an answer *about* the prompt rather than *from* it
— has no cheap syntactic test, and the honest position is a filter that catches
what was seen, a note that it is not the class, and an unnamed memory as the
correct outcome either way. The store half — the two refusals and the fence already named here — is
[rename-the-memories-named-before-the-bound](../rename-the-memories-named-before-the-bound/prd.md), and leaving it there keeps one
store pass under one part.
