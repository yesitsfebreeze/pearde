---
kind: work
level: 10
status: done
description: "every `kind: routine` part in the graph is served as an MCP tool `routine:<name>` answering with its body, counted and drawn by the reflex ledger under the same key"
read_when: "executing the declared-surface plan"
---

# routines-are-tools

**Needs [[@prd/work/memory--behaviour-is-a-space-field.md]]** and nothing else: the payload shape
is settled — the tool is keyed by the part's leaf name, `name:` having retired
([[a-declaration-carries-its-payload-in-a-toml-block]]).

That need is closed: [[@prd/work/memory--behaviour-is-a-space-field.md]] is `status: done` and the
surface landed as `211c3019`, so `blocked` was a word this part carried past
the thing that blocked it. Nothing waits now: the count landed too, and every
clause of the Check below runs.

## Do

`memory mcp`'s `tools/list` (`src/commands/src/commands_mcp.rs`) appends one
tool per `kind: routine` entity read from the graph — name `routine:<name>`,
description the part's `description`, one optional free-text argument.
`tools/call` on such a name answers with the part's body. The names go into
the `reflex {action: draw}` list alongside `TOOLS`, and because the call runs
through `Server::invoke` the count lands under `routine:<name>` with no
change to `src/rpc/src/reflex.rs`.

## Check

A new `tests/dynamic_surface.rs`: a temp store with two `kind: routine` parts
answers `tools/list` with both `routine:` names, `tools/call` returns the
body of one, and `reflex.json` then holds `routine:<name>` at 1.

Landed: `tools/list` and `initialize` ask the daemon for `part {op: list}` and
append one `routine:<leaf>` tool per `kind: routine` part — the leaf name is the
handle, the front matter's `description` is the line an agent picks it by, and
one optional free-text `input` opens the answer. `tools/call` on such a name
reads that part back through `part {op: read}` and answers with its body, the
front matter stripped by the same `split_front_matter` the watcher ingests with.
The names join the `reflex {action: draw}` list beside `TOOLS`. `respond_static`
went with the change: `tools/list` needs the daemon now, and `ping` was the only
reply left that did not, so it is one arm of the one match.

The read is the `part` operation and not a kind-filtered `query`, which is the
deviation this record should carry. A declaration's `description` is the half a
tool list cannot do without, and the graph does not hand it back: the watcher
sink puts it in `Source::title` and `entity_detail`
(`src/retrieval/src/id_detail.rs`) does not serialize it, so a graph read would
have offered every routine under a blank line. `part` answers the kind, the
description and the path in one call, over the roots the watcher feeds the graph
from — the same record either way.

The third clause runs now: `Server::invoke` (`src/rpc/src/server.rs`) dispatches
`routine:<leaf>` — it strips the prefix, finds the `kind: routine` part whose
leaf matches over the watched roots, and answers its body with the front matter
taken off by the same `split_front_matter` the watcher ingests with. `invoke`
records before it matches, so the count came free with the arm. `routine_answer`
collapsed to that one call: it was serving the read client-side out of two `part`
calls, which measured a routine as the reads it is made of and let
`reflex {action: draw}` list a name it would never count. A leaf the record does
not declare is refused by the same arm, so the ghost case answers where the real
one does.

The whole Check runs as `cargo test --test dynamic_surface`: two declared
routines are two tools carrying their own descriptions, a decision part beside
them is not a tool, the body answers with the argument at its head, a name the
record does not declare is refused, and the ledger the harness opens holds
`routine:polish` at 2 — one per call.
