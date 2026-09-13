---
kind: work
level: 1
status: open
description: memory is proxy plus memory engine plus extensions — bounded memory and reflex preparation on agent turns, graph and multimodal ingest, a dated track record across stores, and optional capabilities mounted through the core extension mechanism
read_when: "asking what memory is working towards, or picking what to do next"
---

# the-vision

The goal the plan feeds. [[vision]] is the authoritative destination; this memo
projects the first usable core revision onto a finite set of executable
terminals. Later core work remains recorded, but does not have to finish
before the proxy, memo tools, memory, and extensions are usable together.

## Do

Carry the terminals to done:

`subwork:` [[@prd/work/memory--the-graph-converges.md]], [[@prd/work/memory--declare-the-surface-in-the-record.md]],
[[@prd/work/memory--the-agent-surface-is-usable.md]], [[@prd/work/memory--build-the-composition-pillar.md]],
[[@prd/work/memory--proxy-turns-carry-recall-and-reflex-tools.md]]

Later committed core work remains [[@prd/work/memory--multimodal-content-reaches-the-graph.md]] and
[[@prd/work/memory--the-track-record-is-reachable-across-stores.md]]. They are not dismissed as ideas,
but are not prerequisites for the first usable revision. Ongoing maintenance
[[@prd/work/memory--keep-the-tree-and-record-true.md]] is not a never-ending release gate; a concrete
release-blocking defect belongs under the terminal it prevents.

Memory bundles no client: it is consumed through its proxy, memory, memo tools
and extension interfaces ([[memory-is-consumed-not-a-ui-host]]), so no client
work hangs under this vision. [[@prd/work/memory--every-compute-crate-is-a-piece.md]] retains its
existing claim, but development hot-reload expansion is not a release
prerequisite. Do not automatically reattach the deferred items merely because
they are outside this milestone's axis.

## Check

The retained terminals pass their current behavioural checks. An external agent
using the proxy receives bounded source-labelled memory without a nested agent;
memo read/write and ingest/recall work; failures, cancellation, and daemon
replacement preserve the stated ownership and integrity contracts. Required
services shut down without leaked listeners or tasks. No bundled client or
native coding-agent loop is required. The plan's zero-hours header is not
substitute evidence.
