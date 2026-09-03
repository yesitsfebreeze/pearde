---
state: specced
origin: requested
priority: 50
complexity: 15
blast-radius:
---

# ramp is a doctor row not a gate

A fresh board no longer opens with an ASK from ramp on pass 1 (`init` writes `happiness: 0`, ramp calls scout's `route.sh` over the network). `happiness` absent means closed; ramp runs by hand or as a doctor row.

## Done means

`pearde init --example` then `pearde next` reaches the scan without an ask; `pearde ramp` still measures on demand.

## Needs

No gate.
