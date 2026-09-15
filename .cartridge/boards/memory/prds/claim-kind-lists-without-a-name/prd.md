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

# `ClaimKindArgs` makes `action` and `name` required, so `claim_kind {action: "list"}` is refused with `missing field name` — listing the registered kinds is unreachable from the tool surface

## Do

`ClaimKindArgs` (`src/rpc/src/server.rs:1988`) carries `#[serde(default)]` on
`description` and `parent` and on neither `action` nor `name`. Every call must
name a claim kind, including the one that asks which claim kinds exist:

```
claim_kind {"action":"list"}  ->  invalid arguments: missing field `name`
```

The tool description (`src/commands/src/commands_mcp.rs:37`) advertises
`{action?: list|add|rm, name?, description?, parent?, strength?}` — both fields
optional, plus a `strength` the struct does not have. Measured 2026-09-06: the
only listed action of the tool is the only one that cannot be called.

Put `#[serde(default)]` on `action` and `name`, default the empty action to
`list` as the description promises, keep the existing "description required for
add" refusal shape for a missing `name` on `add` and `rm`, and delete
`strength?` from the description. Reading the kinds matters more now that a
part's `kind:` reaches `claim_kind` unvalidated
(`claim-kind-filter-rejects-part-kinds`) — the list is how a caller learns
which words the filter will accept.

**Done 2026-09-06, and a passing test was holding the defect in place.**
`unknown_action_returns_error` (`src/rpc/src/tests/server_admin_test.rs`) used
`"list"` as its example of an *unknown* action and asserted
`action must be add or rm` — so the one action the tool description advertised
was pinned as an error by a green suite. Adding the arm turned that test red,
which is the only reason anyone read it. The same shape as
`the-worktree-check-passes-without-its-fix` from the other side: there a Check
passed without its fix, here a test failed because of one.

`action` and `name` both carry `#[serde(default)]`, an empty action means
`list`, and `list` answers `{claim_kinds: [{name, description, parent}]}` sorted
by name — the description rides along because a caller picking a kind needs the
sentence, not just the word. The refusal moved from serde to the arm that needs
it, so `{action: "add"}` answers `name required for add` rather than
`invalid arguments: missing field name`, and an unknown action answers
`action must be list, add or rm`. The tool description and its schema moved with
it ([mcp-tools-declare-their-schema](../mcp-tools-declare-their-schema/prd.md) makes the second a gate: a description
naming a field the schema lacks fails).

**The CLI still cannot read it.** `ClaimKindAction` (`src/commands/src/lib.rs:571`)
is `Add` and `Rm` only, so an agent can list the registry and a person at a
prompt cannot. Outside this item's `Do`, left open on purpose rather than
widened into it.

## Acceptance
`cargo test -p rpc claim_kind` — a test calls `tool_claim_kind` with `{}` and
with `{"action":"list"}` over a server holding two registered kinds and expects
both to answer the same list; `{"action":"add"}` with no name still refuses.
Held by `a_bare_call_and_an_explicit_list_answer_the_same_registry` — which also
asserts the save counter is unchanged, so a read persists nothing — and
`add_without_a_name_names_the_field_it_wants`. The suite read 1,236 passed.
