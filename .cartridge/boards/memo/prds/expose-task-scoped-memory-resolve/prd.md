---
repo: /Users/feb/dev/cartridge/memo.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
needs:
- "@memo/implement-memo-usage-resolution"
description: "Expose task-scoped memory resolution for agent requests"
---

# Expose task-scoped memory resolve

## Outcome

Agents can ask for relevant memory using a declared `usage` and short `situation`, and receive ranked results that are small enough to inspect before choosing files or actions.

This extends [implement-memo-usage-resolution](../implement-memo-usage-resolution/prd.md) into the agent-facing workflow without requiring manual memo listing or broad search.

## Acceptance
- [x] Already met before this pass: `resolve` takes `usage` plus a free-text
      `query` and returns candidates ranked by score, bounded by `limit` (1..20)
      with a `cursor` for the rest.
- [x] Already met before this pass: each candidate carries `path`, `item_type`,
      `why`, and `matched` naming the fields that hit with their weights, plus
      `revision`, `when`, `caveats` and an `open` hint.
- [x] An empty result now carries `note`: "no memo declares this usage for this
      situation; the record is not known to be empty of relevant context.
      Continue with list, read or coverage." A non-empty result carries no note.
- [x] The tool description says to call resolve before acting, which usage names
      which action, and that empty means undeclared rather than absent.
- [x] `a_situation_ranks_relevant_over_ambiguous_and_says_so_when_nothing_matches`
      covers all three: a declared situation ranks above a body-only match and
      the reason names what hit; an ambiguous situation reaches both declarers
      in an order proven stable across two calls; an unmatched situation returns
      `total: 0` with the note.

## Approach

Probed first: most of this was already built by [implement-memo-usage-resolution](../implement-memo-usage-resolution/prd.md).
A live `resolve` against the workspace record returned ranked items with paths,
kinds, reasons and matched fields, so two boxes were already met. Three were not:
an unmatched situation returned a bare `{"items": [], "total": 0}`, the tool
description said what resolve does but never when to call it, and no test covered
an unrelated or ambiguous situation.

1. `builtin/memo/src/usage.rs`: add `note` to the payload when `total == 0`.
2. `builtin/memo/src/service.rs`: say in `describe()` when to resolve and what
   an empty result means.
3. `builtin/memo/tests/resolver.rs`: one test over relevant, ambiguous and
   unrelated situations, asserting stable ordering across repeated calls.

## Result

The resolver no longer lets an empty answer read as "there is nothing relevant".
Ranking itself was not changed: a situation that matches a declared `when`
outranks a body-term match already, and the top hit reports an exact situation
phrase match when there is one.
