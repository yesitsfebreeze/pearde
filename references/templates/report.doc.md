# report.md — how to fill it, and why each line is there

The template is @references/templates/report.md. `.pearde/report.md` is
rewritten whole every time — one state, never a log, and git holds the earlier
ones. No frontmatter: only a person reads it. @references/report.md is the
format.

## The opening

A title in the reader's words, the date, then two or three sentences: what
works today and did not before, what is happening now, and the one thing pacing
the rest. One fraction where it helps — "eight of fourteen pieces done". No PRD
names, no states, no weights.

## Sections

**`## Planned`** — not started, in the order of happening; the first entry is
next. Each bullet names the thing in the reader's words, then what they get
when it lands. A tail past six entries is counted, not listed: "and four
smaller cleanups behind these".

**`## In work`** — under way now. Say which of the two — still being worked
out, or being built — and what is left.

**`## Undecided or failing`** — each entry names the one thing that moves it,
written as the choice itself so the reader can answer here: an open question as
a fork with its options; a wait with the event awaited; a failure with what was
tried and what it needs. Close with the parked work, a clause each: "Set aside
for now: …".
