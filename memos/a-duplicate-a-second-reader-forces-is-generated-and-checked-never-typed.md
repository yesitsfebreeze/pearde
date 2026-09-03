---
memo: a-duplicate-a-second-reader-forces-is-generated-and-checked-never-typed
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: a field a second reader forces us to duplicate is generated from its source and checked, never hand-written
date: 2026-09-02
---

# a-duplicate-a-second-reader-forces-is-generated-and-checked-never-typed — the rule that survives a reader we do not control

## Decision

Where an outside reader cannot see the field we already carry, the value is
duplicated into the shape that reader understands — and that duplicate is
generated from its source, rewritten by a `retag`-shaped command, and checked
for drift. It is never a key a person fills in.

`tags:` on a memo is derived from its `kind` and `status`; on a workflow file,
from its slug key. `memo retag` and `workflow retag` write them; `memo check`
and `workflow check` fail on a tag that disagrees with the fields it came
from.

## Why

This repo's own rule is that two fields which must agree are one field that
can disagree — @resources/workflows.py says it where it refuses a `kind:`
beside a slug key. Obsidian's graph view forced the exception: it colours by
tag and cannot query a frontmatter property, so a memo's `kind` reaches it
only as a tag or not at all.

The rule survives the exception by moving the duplicate out of a person's
hands. A generated field cannot disagree with its source, because it is
rewritten from it; a checked field cannot silently drift, because the drift
is a named problem with the repair command in the message. What the original
rule actually forbids is a *second opinion*, and a derivation is not one.

The cost that made this worth writing down: `tags` had to join two closed
frontmatter sets, which is the one contract inversion the memo format allows,
and 59 files were rewritten to carry it. Both are acceptable for a field
nobody types.

## Alternatives considered

**Leave the duplicate to the author** — a `tags:` line written by hand beside
the `kind:` it repeats. One edit, no code. It is exactly the disagreement the
existing rule exists to forbid, and a stale tag is invisible: the graph still
draws, in the wrong colour.

**Refuse the duplicate and lose the feature** — keep `kind:` alone and let the
graph colour by nothing. Rejected: the graph is the read layer a person opens
to see how the board connects, and half of it would stay grey.

**Generate a mirror note per memo** — a `wiki/memos/` note carrying the tags,
the way PRDs get `wiki/board/` notes. Rejected: memos already live in the
vault, so the mirror would double every memo in the graph and break the
wikilinks that name the real file.

## Consequences

- Two closed key sets gained a key nobody writes, documented as `generated` in
  their contract tables.
- A new axis worth colouring is one line in `memo_tags` or `file_tags` plus a
  `retag` run — never a sweep over files by hand.
- It does not extend to values a reader could compute itself: a Dataview
  query reads `kind:` directly, and nothing is duplicated for it.
