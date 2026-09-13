---
repo: /Users/feb/dev/cartridge/prd.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: prd
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: declared-source-edges
needs: []
commit: "c344629f00bd9afc4b5f993538600fc52e612ab2"
---

# Existing board declarations expose bounded source edges

One PRD-owned prerequisite extracted from @landscape/recursive-development-graph/recursive-source-census. Preserve its two inherited rounds. The maintained settings.md member grammar already drives strict board scanning; source discovery needs the same declarations before descendant existence checks, so an unavailable child does not erase usable siblings.

## Acceptance

- [x] Existing members()/scan behavior and current member grammar remain compatible, including strict cycle/missing-board errors and hierarchical aliases.
- [x] A read-only exported/native declaration operation returns bounded normalized member edges and the exact settings-byte revision from a real three-level fixture; deleted children remain named edges.
- [x] Native input stays under configured board-root authority; malformed/oversized declarations and escapes fail with static status, no absolute caller-root override, lifecycle change, journal, provider call or subprocess.

## Proof and recovery

Measured census baseline preserves existing successful three-level scan and failing cycle/deleted-child results. Root owns implementation in records.ts, service.ts, declaration tests/docs. The operation remains native-only; model tool grammar and existing mutations are unchanged. Public PRD tests/check, scanner compatibility and native SDK proof must pass before dependent Landscape traversal implementation. A failed declaration read preserves records and returns an explicit unavailable/malformed/capacity state.

## Review

Inherits rounds1–2 from the source census; maximum five. This draft does not claim a passed implementation review. Coordinator installs the new owner board and canonical dependency after independent round3 review.
