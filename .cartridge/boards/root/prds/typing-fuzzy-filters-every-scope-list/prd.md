---
state: "open"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
---

# Typing fuzzy filters every scope list

## Outcome

Every Scope list filters locally as the user types. Waterfall, System, Activity and Plan share case-insensitive subsequence matching. Each view retains its own query. Visible rows and keyboard selection use the same filtered collection. Existing alphabetic shortcuts move to control keys or header focus so typing q, j, f and p searches normally.

## Acceptance

- [ ] Typing immediately filters each of the four lists, including no-match and clearing states.
- [ ] Backspace edits, Escape clears, arrows navigate, and Enter opens the selected filtered row. Ctrl-Q quits and Ctrl-H focuses the view header.
- [ ] Filtering preserves stable selection when possible and safely clamps it when rows disappear or live data arrives.
- [ ] Filtering makes no host requests and never modifies underlying state, occurrence counts or heat.

## Proof and recovery

Accountable component: scope.ctg. Start at src/navigation.py, dashboard.py, waterfall.py and plan.py. Add one local fuzzy matcher and tests in scope.ctg/src/test_filter.py. Run python3 -m unittest discover -s scope.ctg/src -p 'test_*.py' from the composition root, then just audit scope and just isolation. Update README.md and .cartridge/help.md with the new key map. Preserve active concurrent Scope changes. Rollback is limited to the filter and key handling diff; no persistent data changes.

## Dependencies and review

This work is independent of memory storage. It serves the user's speed and smoothness constraint by filtering the current snapshot with no network round trip. Review history is in review.md. Correctness tests use deterministic rows, including Unicode, hidden descendants, empty results and updates while a query is active.

## Current committed UI evidence, 2026-09-19

The source owner has now committed the replacement UI in cartridge.ctg at 58a59366c5fc3d6d27959ff0861dc56838394868. Coordinator codex extracted exactly that revision with git archive into /tmp/scope-current-proof-n0njbq56 and executed all 37 Python UI tests successfully in 22.177 seconds. Output is retained at /tmp/codex-scope-tick17-proof.txt. This proves the committed suite passes; it does not prove every historical criterion above.

The explicit user corrections in note/scope-three-coordinated-panes.md replace the old four-list architecture with shared context and then the centered input/preview/results layout and composable filters. note/scope-command-leader.md records the subsequent mnemonic leader replacing application shortcuts. Current tests include shared filter/selection, live reorder identity, fuzzy matching and captured filter chains. The old scope.ctg Python paths and original shortcut assertions therefore require a faithful current-plan reconciliation, preserving applicable local-filter and stable-selection outcomes while explicitly mapping superseded layout/key requirements to those user corrections. Round 1 PASS 92 remains historical, one round used and four remain. No acceptance box is ticked by this evidence. Runtime broad ASP claim currently reserves the host; coordinate an exact owner footprint before implementation.
