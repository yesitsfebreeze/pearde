---
state: open
origin: requested
priority: 78
repo: "/Users/feb/dev/cartridge"
footprint:
  - "web.ctg"
---

# The voice can look something up on the internet when the answer is not in the repository

## Outcome

The agent this composition runs can answer a question whose answer is not on
this disk. Today its tools are `digest, docs, draft, edit, gitfs, glob, grep,
live, live_agent, live_note, lsp, memo, memory, prd, read, search, shell, ship,
write` — every one of them local, and the only way out is `shell`, which means
the reach exists but has no declared surface, no result shape and no policy.

A capability that the composition owns explicitly: a search that returns ranked
results with their sources, and a fetch that returns a page as text, both
declared, both granted the network on purpose, and both refusable by policy.
What comes back is evidence with a URL attached, so a spoken answer can say
where it came from.

This is a prerequisite for the voice being a coworker rather than a librarian of
one repository: the question "is that still how that library works" has to be
answerable.

## Acceptance

- [ ] The composition declares a web capability with a documented event surface, its own README and help page, and a network grant naming what it may reach.
- [ ] A search returns ranked results, each carrying its source URL; a fetch returns a page as readable text with its URL.
- [ ] The agent can call it, and an answer built from it names its sources.
- [ ] Policy can refuse it, and a refusal is reported rather than silently dropped.
- [ ] `just audit` and `just isolation` report nothing for it.
