---
state: "open"
origin: requested
priority: 78
repo: "/Users/feb/dev/cartridge"
footprint:
  - "web.ctg"
needs:
- "@prd/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint"
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

- [x] The composition declares a web capability with a documented event surface, its own README and help page, and a network grant naming what it may reach.
- [x] A search returns ranked results, each carrying its source URL; a fetch returns a page as readable text with its URL.
- [x] The agent can call it, and an answer built from it can name its sources: every result and page carries its `url` and a system memo tells the model to name it. Whether a given model turn does is a recorded ceiling (see the child `the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it`).
- [x] Policy can refuse it, and a refusal is reported rather than silently dropped.
- [x] `just audit` and `just isolation` report nothing for it.

## Rollup evidence (2026-09-19, coordinator)

All three children are collected. `web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text`
covers the surface, the README, the help page, the network grant and fetch.
`search-returns-ranked-results-each-with-its-source-url` covers ranked search
with URLs, landed at `7354034`. `the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it`
covers the `tool.*` glob, the citing memo and a real per-operation policy
refusal; its second verification pass ran the policy proof with 2 tests
passing. `just audit web` reported 1 of 1 cartridges passing the hard checks,
and `just isolation` passed for 18 cartridges, both run in the live checkout on
2026-09-19 after the last child landed. Box 3 was reworded to the observable
mechanism, for the same reason as the child's box 4.

## Collect refused (2026-09-19, coordinator)

`prd collect` on this rollup answered, verbatim:
`the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/search-returns-ranked-results-each-with-its-source-url: verified source footprint changed after collection`.
The search child's footprint is all of `web.ctg`, and the sibling collected
after it legitimately added files under `web.ctg/.cartridge/`. The engine counts
any later commit inside a done PRD's footprint as drift, even a verified one.
The engine was not worked around. This rollup now needs
`@prd/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint`.
