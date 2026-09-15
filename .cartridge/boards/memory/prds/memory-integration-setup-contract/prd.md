---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
---

# Keep setup instructions and examples synchronized with actual health fields and verification behavior.

## Do

Replace stale setup references such as `health.thoughts` when the response exposes `entities`, and make verification examples derive from or test against the actual schema. Cover setup output in CLI and MCP surfaces. Keep setup fast; performance work already belongs to [setup-sorts-every-access-count-to-render-a-greeting](../setup-sorts-every-access-count-to-render-a-greeting/prd.md). Avoid duplicating field definitions in prose when generated or typed data can supply them.

**Done 2026-09-09.** `render_setup` (`src/rpc/src/server.rs`) names
`health.entities` where the Verify step said `thoughts`, and names
`health.embed_unreadable` beside `health.embed_mismatch` — the pair together,
because a false mismatch beside a stamp that did not decode is "nothing to
compare" and not "compatible" ([[@prd/routine/run-board.md]] siblings `30e70a67`/`5c81bdb5` took the
same stance one level down). Every field is written in one `health.<field>`
form so a gate can find it, and the module comment says so: a name written any
other way is one nothing checks, which is how `thoughts` outlived the response
that answered it. The CLI keeps its own vocabulary — its line is prose about a
count, not a field reference — so no second name was invented for one field.

## Acceptance
A contract test renders setup instructions, executes or parses every named verification field against a representative health response, and fails on unknown fields. Human-readable setup output still explains expected ingest, health, and query outcomes. Existing setup and schema tests pass.

Held by `tests/setup_contract.rs`: it renders `setup` off a real `Server`
through `invoke` — the one dispatch the CLI and the MCP surface both reach
`render_setup` through — parses every `health.<field>` out of the text, and
looks each one up in a live `health` response. `every_field_setup_names_is_one_health_answers`
fails on an unknown field and, separately, on a rendering that names none, since
a containment check over an empty list passes vacuously.
`an_unknown_field_is_what_this_gate_catches` holds the scanner to a known-good
and a known-bad name so the check has been seen to bite; red-proofed by putting
`health.thoughts` back, which named the field in the failure line.
`verify_still_explains_ingest_health_and_query` keeps the human sentences.
Suite read 1,472 of 1,473 passed — the one red is `memory::cited_paths`, which
fails in every lane because `src/rpc/src/plan.rs` cites a file only the trunk
has. The three `server_setup_tests` and the `wire_tolerant_decode` schema tests
pass.

