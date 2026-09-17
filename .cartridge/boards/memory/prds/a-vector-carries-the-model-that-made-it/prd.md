---
state: "open"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/memory.ctg"
footprint:
  - "src/base/src/base_types.rs"
  - "src/graph/src/persist.rs"
  - "src/store/core/src/lib.rs"
  - "src/retrieval/piece/src/retrieval_query.rs"
  - "src/health/src/lib.rs"
  - "src/commands/src/commands_check.rs"
---

# A vector carries the model that made it

## Outcome

Withdrawn. The premise was investigated on 2026-09-16 and does not hold.

The guard this PRD proposed already exists, and the observation that motivated it
has a different cause.

What exists: `store_core::EmbedStamp` (`src/store/core/src/lib.rs:312`) records the
model name and dimension for a store. It is written and checked on load and on every
flush (`stamp_of` and `check_stamp`, `src/graph/src/persist.rs:73-99`); an unstamped
store adopts the configured model, a changed model sets a durable `embed_mismatch`
flag and logs that "recall stays near zero until `memory reembed`", and an unreadable
stamp is deliberately left intact rather than adopted over. `memory health` reports the
model, the dimension and the flag (`src/health/src/lib.rs:187-200`), and `memory check`
already raises both `embed_mismatch` and `embed_unreadable` as error findings
(`src/commands/src/commands_check.rs`).

What the 363 rows actually were: the `memory.ctg/.memory` store that prompted this PRD
holds zero live thoughts and 363 cold rows, every one of them `EntityStatus::Superseded`
with a correct 1024-dimension vector. Probed by instrumenting `store.cold_visit` and
printing each row's `veclen` and `status`: all 363 printed `veclen=1024 status=Superseded`.
`cold_candidates` excludes superseded rows by design
(`src/retrieval/piece/src/retrieval_query.rs`), so every query over that store correctly
returns nothing. The store is a development leftover, not a corrupted one, and the
dimension check was never the thing rejecting those rows.

A speculative `vector_dim_mismatch` finding was written against both tiers and then
removed: it fired on nothing, because no row in the store has a mismatched width. Adding
a check for a fault with no instance is the kind of code this repository deletes.

The one real gap the investigation found — that an empty result could not be told apart
from an excluded one — is fixed and collected under
[the floor names the weak hits it cut](../the-floor-names-the-weak-hits-it-cut/prd.md).
`memory query` on that same store now answers: `no results — nothing entered the ranking
pool (363 cold rows scanned; seeding found nothing, or rows were excluded by a filter or
an embed mismatch)`.

## Acceptance

- [x] Establish whether per-row model provenance is missing. It is not missing in the way
      this PRD assumed: the stamp is per store, and no evidence of a mixed-width corpus
      exists on this machine.
- [x] Record the investigation so the premise is not re-derived from the same observation.

## If this is wanted again

Per-row (rather than per-store) model identity remains a defensible design, but it needs a
real instance to justify a persisted-layout change to a bincode-positional `Entity`
(`src/base/src/base_types.rs:328`). The trigger to re-open: a store that carries rows of
two different widths, or a `check` run where `embed_mismatch` is false while recall is
nonetheless near zero. Neither is observed today.
