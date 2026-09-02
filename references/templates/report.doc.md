# report.md — how to fill it, and why each line is there

The template is @references/templates/report.md. `.pearde/report.md` is the
whole file, rewritten every time — one state, never a log; git holds every
earlier one. No frontmatter: nothing reads this but a person.
@references/report.md is the format.

## The opening

A title in the reader's words, the date, then two or three sentences: what
works today that did not before, what is happening now, and the one thing that
decides how fast the rest goes. One fraction — "eight of fourteen pieces
done" — where it helps, none where it does not. No PRD names, no states, no
weights anywhere in the file.

## Sections

**`## Planned`** — not started, in the order it will happen. The first entry
is what happens next. Each bullet is the thing in the reader's words, then
what they get when it lands. A tail past six entries is counted, not listed:
"and four smaller cleanups behind these".

**`## In work`** — being worked on right now. Say which of the two it is —
still being worked out, or being built — and what is left on it.

**`## Undecided or failing`** — each entry names the one thing that would
move it. A decision is written as the choice itself, so the reader can answer
it here: the open question as a fork with its options; the thing that is
waiting with the named event it waits on; the thing that did not work with
what was tried and what it needs now. Close with the parked work, one clause
each: "Set aside for now: …".
