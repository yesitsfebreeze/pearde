---
state: deferred
origin: derived
from: every-document-is-written-in-the-writer-s-prose
priority: 60
complexity: 0
blast-radius:
---

# the writer persona is cited everywhere and has no file

The user did not ask for this. `python3 resources/index.py check` is red on
2026-09-03 with one line:

    references/language.md references @references/personas/writer.md — not on disk

Earlier pass files carried this as an index-exit-code complaint. It is not one.
**The file is genuinely absent and the roster is four:** `references/personas/`
holds `designer.md`, `engineer.md`, `mentor.md`, `skeptic.md` and `INDEX.md`.
There is no `writer.md`.

**What cites it.** `references/language.md:34` reads *"From
@references/personas/writer.md, Vera Lindqvist. Checked by …"* — it names an
author and a checking regime that live in a file nobody wrote. `language.md` is
the rule set `resources/prose.py` enforces, and the board's largest PRD tree,
`every-document-is-written-in-the-writer-s-prose`, is named after that persona.
Six of its children have been specced and several are in flight, every one of
them against a voice whose definition is a dangling handle.

**Why the shape matters.** A persona is a field, a bias and a way of reading —
`references/parts/personas.md`. `prose.py` can only check the mechanical part
of a voice: sentence length, clause shape, the em-dash rule. The judgment the
checker cannot make is exactly what the missing file was meant to hold, and its
absence is the likeliest reason `prose.py` has three measured defects
(it flags grammatically bound relative clauses, 71–73% of its hits) that nobody
can adjudicate — there is no written standard to adjudicate against.

## Done means

- `references/personas/writer.md` exists, in the same format the other four
  use, and `references/personas/INDEX.md` carries its row.
- It is built the way the roster requires — from research into the field and
  its named practitioners, per the `pearde-persona-create` route — not invented
  to satisfy a link. Vera Lindqvist is the name `language.md` already fixed;
  the file must earn it or `language.md` must stop using it.
- It says what `prose.py` cannot check: what this voice does with a fact it
  cannot compress, and what it refuses.
- `python3 resources/index.py check` exits zero on this repo.
- `python3 resources/pearde.py persona` lists five, and `writer` is selectable.

## Related, and deliberately not folded in

`prose.py`'s three measured defects are owned by a PRD that is already `done`
and need a reopen or a PRD of their own. Writing this persona does not fix the
checker. It gives the checker's disputed hits somebody to appeal to, which is
the smaller and the answerable half.

Whether `index.py check` should exit non-zero on a broken handle outside any
PRD's footprint is a separate question and is not settled here.
