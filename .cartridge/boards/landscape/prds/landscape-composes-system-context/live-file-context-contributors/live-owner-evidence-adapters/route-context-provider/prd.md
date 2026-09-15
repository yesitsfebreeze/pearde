---
repo: /Users/feb/dev/cartridge/router.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: router
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/route-context-provider
needs:
- "@router/improve-router-route-explanation"
footprint:
- /Users/feb/dev/cartridge/router.ctg/cartridge.json
- /Users/feb/dev/cartridge/router.ctg/init.lua
- /Users/feb/dev/cartridge/router.ctg/src/proxy.rs
- /Users/feb/dev/cartridge/router.ctg/.cartridge/tests/unit/proxy/capabilities.rs
---

# Router answers context with redacted route explanations

router already explains a routing decision (`src/proxy.rs` `explain_routes`: chosen model, candidates, rejection reasons, `catalog_revision` and `policy_revision`, with no tokens, headers or credential values). The explanation is per request, not per session, so it answers "why this model" for the configured routes. This leaf makes router define and listen to `context.route`, answering memo's `contribute` and `read` shapes (`memo.ctg/.cartridge/docs/context.md`) with those explanations.

## Acceptance

- [ ] A memo `context` prepare naming `route` returns rows with `reference.kind: route` for the configured routes, carrying the explanation fields and both revisions. No credential, header or connection state appears.
- [ ] Readback is `changed` after the catalog or policy revision moves. Contribute makes no provider calls and changes no health state.
- [ ] With router removed or its catalog unavailable, `route` is `absent` or `unavailable` and the other contributors keep their rows. A forwarded `scope` is ignored.

## Proof and recovery

Probe first: which routes count as "configured" (the profile default and named aliases), and the row size against the evidence row caps in `memo.ctg/evidence`. Extend `.cartridge/tests/unit/proxy/capabilities.rs` with a fixture catalog and no live provider. Gates, cwd `/Users/feb/dev/cartridge`: `just test router`, `just check router`, `just isolation`. Not run. Rollback: remove the event; `explain_routes` stays unchanged.

## Dependencies and review

Needs only the delivered route explanation; memo's scope facade is not required because routes are not session-scoped. Rounds 1–2 are inherited; this leaf was created by the round-3 split ([review](review.md)).
