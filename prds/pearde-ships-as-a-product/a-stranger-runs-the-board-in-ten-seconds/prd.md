---
state: open
origin: requested
priority: 85
complexity: 20
blast-radius:
needs: the-second-cleanup-pass
---

# a stranger runs the board in ten seconds

One script `resources/smoke.sh` that, in a temp dir with no machine path, runs `pearde init --example`, `doctor`, `add`, `claim`, `specced`, `collect` and exits 0 green. Runnable in CI.

## Done means

Green on a clean clone under 10 s; `pearde test` runs it first.

## Needs

`the-second-cleanup-pass` — the container's gate.
