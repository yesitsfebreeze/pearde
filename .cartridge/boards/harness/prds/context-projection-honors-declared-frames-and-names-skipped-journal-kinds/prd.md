---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/harness.ctg"
needs:
  - "@agent/an-event-declares-its-type"
footprint:
  - src
  - .cartridge/tests
  - cartridge.json
  - README.md
  - .cartridge/help.md
---

# Context projection honors declared frames and names skipped journal kinds

## Outcome

Harness projects journal records using the writer's host-declared frames. Message records retain their conversation roles, data records enter a labelled data frame, and none records stay out of model input. Unknown historical kinds remain stored and appear as skipped in context inspection. Adding a declared kind requires no per-kind projector branch or copied agent catalog.

## Acceptance

- [ ] Fixed v1 conversation fixtures produce byte-identical message projections, retaining the existing user/assistant/tool role ceiling.
- [ ] A fixture adds data and none declarations; the data appears in its labelled frame and the none record is absent without editing projector branches.
- [ ] Unknown historical kinds preserve the remaining conversation and context inspection names each skipped kind. Inspection attributes every journal record to its declared or unknown kind and makes projected, non-projecting and skipped disposition observable without parsing message payloads.
- [ ] Invalid or unavailable declarations cannot promote journal payloads to system/developer authority; failure and recovery are observable and leave stored transcripts intact.

## Proof and recovery

Current source still filters only message in src/lib.rs project_messages and src/working.rs; src/inspection.rs owns inspection. First reproduce the missing data/unknown-kind behavior through the real harness projection and inspection APIs, then establish the host declaration-access contract without reading sibling source at runtime. Run ./task check harness and ./task test harness from the composition root; specs must include named executable fixture tests. No proposed checks have run. Preserve v1 bytes and source attribution on failure.

## Dependencies and review

This is the downstream half required by @agent/an-event-declares-its-type review round 3. Its implementation depends on that leaf. It inherits three used review rounds from the split scope; two remain. Narrow the initial owner footprint during specification. The agent's write-time declaration enforcement remains independently deliverable, with non-message kinds initially framed none.
