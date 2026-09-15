---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
---

# One daemon serves the project and every run, launch and mcp is an instance attached to it

## Why

The intended shape is one daemon per project with many instances over it.
What runs today is one full composition per command. Observed on 2026-09-15
for project socket directory `/tmp/cartridge-501/69a3b8e0c7a1/`:

- `cartridge daemon` 74584, `cartridge launch claude` 58681 and
  `cartridge run memory …` 78693 each had their own socket directory. Each
  started its own node for every cartridge in `.cartridge/init.lua`.
- Earlier that day, three `cartridge daemon` processes (68790, 92754, 93456)
  ran on this project at once.
- Every host starts its own memory node. Memory holds a single-writer lock on
  its store (`store::lock::acquire`), so the first host to open it wins. The
  others fail with `another memory writer holds this data dir`. Attached
  memory is read-only, so their writes fail, the exchange ledger's `append`
  included.
- Each `cartridge run` pays a full composition start of about 15 seconds.

## Outcome

One project has at most one daemon. `run`, `call`, `launch` and `mcp` find it
through the project's `host.sock`, start it when none answers, and send their
events to it. They never start nodes of their own. Stateful cartridges such as
memory, sessions and router exist once per project, so every instance shares
one store and one writer.

## Open questions

- Do per-instance pieces stay in the instance and only services move to the
  daemon? Examples: `launch`'s agent process and tmux window, `mcp`'s stdio,
  and the proxy listener that `launch` points an agent at.
- What happens to instances when the daemon restarts or reloads the profile?
  Do they reconnect, or end?
- How does a second daemon started on the same project behave? It could refuse
  or hand over. Starting a second full composition is not an option.
- `call` already asks the running host (`client::ask`). Should `run` become
  `call` with auto-start, or keep its own meaning for a solo host
  (`verify_one`)?

## Acceptance

- [ ] With a daemon running, `cartridge run memory '{"op":"status"}'` answers
      without starting any node process (count `cartridge node` children before
      and after).
- [ ] Two `cartridge launch` instances and one `cartridge mcp` on the project
      leave exactly one `cartridge daemon` and one node per composed
      cartridge.
- [ ] A memory `ingest` from one instance is returned by `query` from another,
      with no writer-lock error.
- [ ] With no daemon running, the first instance starts one, and a second
      instance started concurrently attaches to it instead of starting another.
