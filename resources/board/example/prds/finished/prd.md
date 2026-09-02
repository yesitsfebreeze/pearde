---
state: claimed
origin: requested
priority: 55
complexity: 10
blast-radius: low
claim: worker-finished 2026-08-28 12:00
footprint:
  - src/util.py
---

# finished — every box closed, a worker still holding it

The band to collect. Every acceptance box in `specs/spec01.md` is closed and
`prd.md` carries none, so the scan lists `finished` first — one commit closes
it `done`.
