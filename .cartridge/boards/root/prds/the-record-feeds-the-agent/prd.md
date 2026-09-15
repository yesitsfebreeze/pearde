---
repo: /Users/feb/dev/cartridge
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: rollup
needs:
- "@landscape/a-usage-ranked-tool-graph-serves-the-best-way"
- "@root/the-memory-bank-is-wired-into-the-surface"
- "@root/context-is-living-not-per-session"
- "@root/context-corrections-carry-their-context"
- "@memo/integrate-memory-resolver-into-agent-harness"
- "@root/long-horizon-recall-benchmark"
- "@memo/a-shadowing-write-passes-the-leaf-check"
---

# The agent's context is the record: system memos, and memory resolved for the task at hand

## Outcome

What the agent knows comes from the record, not from a prompt pasted into the
code. The harness composes the enabled `kind: system` memos in order and renders
the session variables on each request, and the resolver returns the memos and
files that the task at hand actually calls for — with provenance, with freshness,
and with staleness and conflict surfaced rather than silently merged.

This is the half of the system that makes the inline agent worth reaching. The
resolver chain under `builtin/memo` carries it; its roof is
[integrate-memory-resolver-into-agent-harness](../../../memo/prds/integrate-memory-resolver-into-agent-harness/prd.md), and that memo's `needs:` names
the completed resolver units.

Current direction, 2026-09-12: keep working context small while retaining goals,
evidence, decisions and their effects. Detailed recipes and full history remain
retrievable. Program discovery/debug/extension is tracked under
[[the-agent-can-diagnose-and-extend-its-runtime]], not claimed complete here.
The composed-system list below is historical evidence; current profiles also
include environment-specific visible-shell guidance.

## Acceptance
- [x] [integrate-memory-resolver-into-agent-harness](../../../memo/prds/integrate-memory-resolver-into-agent-harness/prd.md) is done, and with it the
      seven units beneath it.
- [x] The composed list is `base`, `memos`, `resolver-guidance`, `workspace`,
      `summary`. `resolver-guidance` exists only in
      `builtin/memo/.zirkle/memos/system/`, so an enabled cartridge's record is
      merged and ordered among the workspace's own.
- [x] Every item carries `revision`, and `target_revision` for an external file,
      so a moved file is distinguishable from a changed memo. A replaced memo
      carries `superseded_by` and never outranks its replacement; an open
      question carries `unresolved`; and the response carries a `conflicts` list
      rather than merging the disagreement away.

## Result

The resolver chain under `builtin/memo` is complete. What the agent knows now
comes from the record with its provenance attached: where it came from, how
fresh it is, whether it still holds, and whose word says it was useful.

Two properties are worth keeping as the record grows. Retrieval grants no
authority — a system memo counts because the harness composed it, not because a
search found it. And nothing is merged quietly: supersession and open questions
are reported as conflicts for the reader to settle.
