---
state: open
origin: requested
priority: 0
complexity: 0
blast-radius:
needs:
  - the-capability-registry
  - suggested-at-the-moment-of-need
---
---

# The vault's verbs are capabilities

*Source: `docs/content/docs/improvements/integration-vault-verbs.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Layer:** suggest · **Tool:** obsidian · **Unblocked by:**
[the registry](/docs/improvements/integration-registry),
[the suggestion](/docs/improvements/integration-suggest)

## Why now

The vault is treated as a *read layer* — the board rendered natively, the
dashboard for a person. But Obsidian is a tool the agent can *drive*: REST
and MCP from the same port (@references/obsidian.md), search across the
wiki, canvas composition, Dataview queries the dashboard itself runs. None
of those verbs are capabilities in any registry — the vault's settings are
resources, its plugins are fetched bundles, and the *operations* an agent
could take mid-pass (find every conclusion touching a decision before
writing a memo; lay a plan's PRDs on a canvas) live nowhere the brief
reaches. The board's own verbs are counted, routed, suggested; the vault's
are folklore.

## The change

The vault's agent-facing verbs get registry rows like every tool's: search
(query across wiki + board notes through the REST port), canvas (compose a
canvas from a PRD set), dataview (run a dashboard source against the board)
— each with reads, writes and the same cost class as the python tools. The
suggestion rule needs no extension: rows whose reads meet the footprint are
carried in the brief, and a pass whose footprint touches `wiki/` or
`memos/` now carries the vault's verbs beside the knowledge verbs. The
health-style check rides along: the REST port unreachable means the rows
report `off`, the way doctor's `view` row reports the service — never
suggesting a capability whose backend is down.

## Done when

- `pearde capabilities` lists the vault verbs with their reads/writes, and
  the suggestion section for a wiki-footprint pass carries them beside the
  knowledge verbs — one diff, no second mechanism.
- With Obsidian (or its REST bridge) closed, the same brief shows the rows
  marked `off` — a suggested capability never dead-ends the worker.
- The verbs' contract lines name the port and the vault root they resolve
  through — `.pearde/`-relative, the one rule the vault already keeps.

## Fails when

- The vault verbs bypass the board's own tools — an agent searching the
  wiki through REST when `knowledge.py query` is the contract. Guard: the
  rows' contract lines name what *not* to use them for (the loop queries
  through the tools, never by reading `Dashboard.md` — the same line the
  knowledge reference already draws, now carried in the suggestion).

## What stays out

No new plugin, no MCP server of our own — the vault's port is already open
and the verbs already exist. This page only makes them *countable
capabilities*: indexed, suggested, and eventually ranked like the rest.
