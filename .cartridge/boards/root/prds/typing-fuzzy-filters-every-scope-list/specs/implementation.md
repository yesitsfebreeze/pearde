---
footprint:
  - scope.ctg/src
  - scope.ctg/README.md
  - scope.ctg/.cartridge/help.md
---

# Local filtering across Scope views

Printable Unicode input updates the current view's local subsequence query. Each view retains its own query. Backspace edits, Escape clears, Ctrl-H focuses the view header and Ctrl-Q exits. Arrow keys and Enter keep selection and expansion behavior. Filtering exposes collapsed System descendants without changing stored expansion state. Plan detail requests start when the detail is opened.

## Acceptance

- [ ] All four views accept Unicode and keep independent queries.
- [ ] Printable shortcut characters filter instead of changing views or quitting.
- [ ] Empty results and stable Plan selection preserve the underlying model.
- [ ] Terminal input handles Unicode, Backspace and Ctrl-Q in a real PTY without host calls.

## Verify

```sh
python3 -m unittest discover -s scope.ctg/src -p 'test_*.py'
```

## Evidence

The complete Python suite passed 43 tests. An isolated PTY drove the actual curses loop with Japanese input, Backspace and Ctrl-Q, and verified the resulting query and clean exit using fake local sources.

## Current verification status — 2026-09-19

The prior evidence paragraph above is historical and has not been reproduced
from an attributable committed revision. The current Verify command exits 1
because scope.ctg/src has been removed by the concurrent UI migration. Its
acceptance checks are therefore reopened, not treated as completed work. See
the coordinator analyst report under root/.state/loop/typing-fuzzy-filters-every-scope-list/analyst-codex-1.md.

Recorded user corrections replace separate views with a unified list, usage
waterfall and detail layout. The current foreign replacement is in
cartridge.ctg/ui, outside this historical footprint. A replacement executable
plan must reconcile the current owner and base, retain local Unicode subsequence
filtering and observational behavior unless specifically superseded, and receive
independent review. Do not restore obsolete views or collect this historical spec.
