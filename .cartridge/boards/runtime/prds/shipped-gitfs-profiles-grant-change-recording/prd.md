---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: "passed"
needs:
- '@gitfs/overlay-mutations-report-revisions'
- '@sessions/file-change-records-retain-reported-revisions'
---

# Grant change recording in the shipped GitFS profiles

The default, live and MCP profiles already declare Sessions and GitFS. Add the
exact Sessions injection to those GitFS entries so the optional producer can
record into the same session owner. A capability grant is the composition's
permission to call; file-change metadata cannot add or expand it.

## Acceptance

- [ ] Each existing GitFS profile entry receives exactly the Sessions grant while other entries and permissions remain unchanged.
- [ ] Real Host composition runs FS/GitFS against the declared Sessions instance and records distinct changes; a standalone GitFS profile remains usable without a Sessions dependency.
- [ ] Existing public runtime/profile gates and the composed provenance fixture pass with pinned native binaries and recorded source revisions.

No new runtime dependency language, wildcard grant, implicit activation, session
mapping or authentication is introduced. The profile's existing declared-provider
startup behavior still applies. Coordinate workspace lock edges for the shared
Sessions DTO dependency, retaining unrelated changes. Inherit the provenance
requirement's two used review rounds; coordinator owns this source and collection.
