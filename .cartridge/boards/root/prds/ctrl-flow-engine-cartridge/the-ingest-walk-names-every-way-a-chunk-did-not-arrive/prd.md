---
state: open
origin: requested
priority: 30
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: the-ingest-walk-names-every-way-a-chunk-did-not-arrive
footprint:
  - "flow.ctg"
---

# The ingest walk names every way a chunk did not arrive

Port the ingestion pipeline: one item from a source driver walked to the stores its authored paths reach, performing the graph's `Route` and `Transform` nodes. Everything that does not reach a store comes back as typed data beside the targets — an unrouted item, a dropped branch, a refused pattern, a target a route names that no link reaches, a model that failed — so a partial ingest is a readable record and never a silent absence.

The run is the durable half: seeded from a journal, planned against a graph snapshot, and suspended by re-deriving readiness over the nodes the source's paths reach. Suspension is a read of the readiness function from the first child, never a second implementation of it. The model that classifies a route and performs a prompt transform is a seam this cartridge declares and does not fill; the composition fills it from `agent.ctg` through `router.ctg`, and the offline suite fills it with an identity function.

## Acceptance

- [ ] One item walked through a graph with a route and two transforms reaches the expected stores, and the attempt record lists each target with the path that reached it.
- [ ] Each non-delivery is reported as its own typed variant with the node that caused it: unrouted item, dropped branch, refused pattern, unreachable target, model failure. An empty target list with an empty reason list is not producible.
- [ ] A run whose graph is missing a required fact is suspended with the requirement named, no source driver is reached, and re-deriving readiness after the fact is supplied resumes the same run.
- [ ] A source driver yielding more items than one checkpoint interval is checkpointed at the declared cadence, and a run interrupted mid-walk resumes from the last checkpoint without re-delivering a committed item.
- [ ] The whole walk runs offline in `just test flow` with the model seam filled by a test double and no store behind it.

## Proof and recovery

Port from upstream `ctrl` `src/pipeline.rs` (241 lines at survey), `src/run.rs` with its `distil`, `driver`, `journal`, `plan`, `record` and `step` modules, and `src/connect.rs` (the filesystem driver). Upstream keeps all of this IO-free with the journal, facts, driver, embedder, model and distiller as caller-filled seams; preserve that, so this child pulls in no client and no runtime.

Depends on the workflow graph child for readiness and the node model. The `Distiller` seam is declared here and filled by `@memory/ingestion-distiller-seam`.

Gates, cwd `/Users/feb/dev/cartridge`: `just test flow`, `just check flow`. Not run for this plan.
