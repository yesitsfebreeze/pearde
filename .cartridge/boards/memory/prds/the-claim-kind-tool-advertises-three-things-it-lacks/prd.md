---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# the `claim_kind` tool description offers an optional action, an optional name, a `list` action and a `strength` field — the handler requires the first two, has no `list` arm and has no such field

## Do

The description is
`{action?: list|add|rm, name?, description?, parent?, strength?}`
(`src/commands/src/commands_mcp.rs:38`). Four of its five claims are false
against `ClaimKindArgs` (`src/rpc/src/server.rs:1991-1999`) and
`tool_claim_kind` (`:2095-2130`):

- `action` carries no `#[serde(default)]`, so an omitted action fails
  deserialization with `invalid arguments`, not with a default of `list`.
- `name` likewise — a `list` call has no name to give and cannot be made.
- `list` has no arm. The match is `add`, `rm` and `_ => Err("action must be add
  or rm")`, so the one action the description names first is unreachable, and
  the CLI has no `List` either (`ClaimKindAction`, `src/commands/src/lib.rs:572-589`).
- `strength` is not a field on `ClaimKindArgs` at all.

Fix the description to `{action: add|rm, name, description?, parent?}`, or add
the `list` arm and default `action` to it — the tool is the only surface that
would answer "what claim kinds are registered", and
[[claim-kind-filter-rejects-part-kinds]] is the reason a caller asks. Either way
the description and the handler must say the same thing: a caller reads the
description, sends what it advertises, and gets `invalid arguments` back with no
hint which field was wrong.

This is what the ledger's `dead` verdict on `claim_kind` recorded, and recording
it changed nothing ([[a-dead-verdict-changes-nothing]]).

## Acceptance
Every field and value the `claim_kind` description names is accepted by
`tool_claim_kind`, and every one it omits is rejected; a test in
`src/rpc/src/tests/` sends the description's own shape and asserts a non-error.

**Done 2026-09-06.** `ClaimKindArgs` defaults all four fields
(`src/rpc/src/server.rs:2022-2032`), an empty action reads as `list`
(`:2162-2165`), and `list` answers `{claim_kinds: [{name, description, parent}]}`
sorted by name. The refusal moved from serde to the arm that needs it, so
`{action: "add"}` names the missing field instead of failing to deserialize, and
an unknown action answers `action must be list, add or rm`. Held by
`a_bare_call_and_an_explicit_list_answer_the_same_registry` and
`add_without_a_name_names_the_field_it_wants`. The description and schema moved
with it. One asymmetry stays open and outside this `Do`: `ClaimKindAction` is
still `Add` and `Rm` only, so the tool surface can read the registry and a
person at a prompt cannot.
