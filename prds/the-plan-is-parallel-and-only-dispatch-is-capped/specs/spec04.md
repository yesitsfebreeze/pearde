---
complexity: 6
footprint:
  - .pearde/prds/the-plan-is-parallel-and-only-dispatch-is-capped/probe/verify.sh
---

# spec04 — proof that dispatch, not the plan, still owns the clash guarantee

`spec01` moves the footprint clash out of the plan's schedule entirely.
The one thing that must not move is the runtime guarantee — never two
writers on one real path — which `resources/board/dispatch.py` already
enforces on the in-flight set, untouched by this PRD. Acceptance asks for
this "proved by a test that tries"; this spec is that test, landed where
the PRD's own probe code already lives.

**What stands** — `probe/probe_dispatch_clash.py` (already in the tree,
uncommitted, from this PRD's own build) builds two rows that clash on a
real file and a third that clashes with neither, launches all three
through `dispatch.dispatch` with a stand-in `/bin/sh` adapter (no model
call, no network), and asserts from the write timestamps each produces:
the clashing pair's live windows never overlap, and the non-clashing row's
window overlaps at least one of them — proving dispatch still serialises a
real clash and still runs unrelated work alongside it. Run against this
lane: `windows: {'a': ..., 'c': ...(overlaps a)..., 'b': (starts after a
ends)}`, `done=3 refused=0 dead=0`.

**What is left** — `probe/verify.sh` wrapping the existing probe script so
`collect` and a future harness sweep can run it the same way every other
PRD's proof runs, with `PROBE_LANE` defaulted to the checkout it is run
from (the probe already reads it as an override, falling back to a
relative walk-up when absent — @resources/board/dispatch.py sits four
directories above `prds/<this-prd>/probe/`).

## Acceptance

- [x] `probe/verify.sh` runs `probe_dispatch_clash.py` and exits 0 on a
      clean tree
- [x] the probe's own two assertions both hold: the clashing pair's windows
      never overlap, and the solo row's window overlaps at least one of
      them
- [x] the probe launches through `dispatch.dispatch` itself — not a
      hand-rolled stand-in for it — so a regression in the real clash
      check is what turns it red

## Verify and Proof

```sh
cat > .pearde/prds/the-plan-is-parallel-and-only-dispatch-is-capped/probe/verify.sh <<'SH'
#!/bin/sh
# Proves resources/board/dispatch.py still refuses a second writer on one
# real path, independent of the plan's own schedule (this PRD's subject).
# PROBE_LANE points at the checkout under test; unset, the probe walks up
# from its own path (this file's directory) instead.
HERE="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$HERE/probe_dispatch_clash.py"
SH
chmod +x .pearde/prds/the-plan-is-parallel-and-only-dispatch-is-capped/probe/verify.sh
PROBE_LANE="$(pwd)" .pearde/prds/the-plan-is-parallel-and-only-dispatch-is-capped/probe/verify.sh
```
