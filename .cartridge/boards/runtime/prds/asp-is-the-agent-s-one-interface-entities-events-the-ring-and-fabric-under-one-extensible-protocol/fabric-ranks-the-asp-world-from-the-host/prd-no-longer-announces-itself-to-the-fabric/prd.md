---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/prd.ctg"
work-kind: leaf
capability-owner: prd
footprint:
  - /Users/feb/dev/cartridge/prd.ctg/cartridge.json
  - /Users/feb/dev/cartridge/prd.ctg/init.lua
  - /Users/feb/dev/cartridge/prd.ctg/src/service.ts
  - /Users/feb/dev/cartridge/prd.ctg/README.md
commit: "e1b6b97ce5df325c01a474fef2f0a6381f599f16"
---

# prd no longer announces itself to the fabric

## Outcome

prd no longer listens to `graph.announce`. It answered it only to announce `tool.prd` to memo's fabric, and the host now contributes every `tool:` entity to ASP itself, so the listener, its `listen` entry and its README line are deleted together with memo's declaration of the event.

## Acceptance

- [x] `rg -n graph.announce prd.ctg` outside the boards finds nothing.
- [x] prd is active after the reconcile and `cartridge run prd` answers.
