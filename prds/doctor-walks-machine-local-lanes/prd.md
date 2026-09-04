---
state: done
origin: requested
priority: 0
complexity: 12
blast-radius: low
workflow: probe-then-spec
actual: 0.18h
---

# doctor-walks-machine-local-lanes

<The request, for an analyst who knows the codebase but not this conversation:
what exists at the end and why, what must not change, pointers to files and
prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

doctor-walks-machine-local-lanes: session/s85810 moved under the lane — resources/board/lanes.py

spec01: exit 0
1 lanes.check / lanes.relink, on a throwaway board
  ok: check flags x and y, leaves z alone
  ok: relink(x) makes a working link
  ok: relink(y) refuses rather than overwrite real content
  ok: check(board) now names only y
2 doctor.sh's lanes row, same fixture, --fix relinks x and stops at y
  ok: doctor reports 2 of 2 lanes broken
  ok: --fix relinks x, refuses on y
  ok: doctor now reports 1 of 2 — x fixed, y still named
  ok: with nothing in the way, the row goes ok with the lane count
3 a .lanes/ that cannot be read is broken, never a silent ok
  ok: an unreadable .lanes reports broken, not ok
0 failure(s)
