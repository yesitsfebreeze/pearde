---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/proxy.rs"
- ".cartridge/tests/unit/proxy/capabilities.rs"
commit: "9f995d9d82982b2c9282eba1174652f7848ec963"
---

# every listed model is retrievable by id

## Outcome

A client that validates its configured model against the router gets the same
answer from every surface. Retrieving one model by id succeeds for every id the
listing publishes, so a launched agent starts on the model it was launched
with.

## Evidence

Reported 2026-09-16 by the user: `/live` failed twice in a launched session
with

```
There's an issue with the selected model (auto:code). It may not exist or you
may not have access to it.
```

and again after `/model auto`. The router was healthy throughout — the listing
carried all 474 selectors including `auto:code`, and `POST /v1/messages` with
`auto:code` returned 200.

The string is emitted by Claude Code 2.1.273 only on an HTTP 404 from the
configured base URL. Probed against the live router:

```
GET /v1/models/auto:code     -> 404
GET /v1/models/auto          -> 404
GET /v1/models/claude-opus-5 -> 404
```

`proxy.rs` `forward` matched `/v1/models` exactly; any path below it fell
through to `Wire::from_path` and returned `unknown endpoint`. Every model in
the catalog was unretrievable, and the client read that as the model not
existing.

An earlier round of this same report was answered on the listing surface — the
test `every_auto_task_selector_is_listed_as_well_as_routed` was added and has
always passed. The listing was never the broken surface.

## Acceptance

- [x] `GET /v1/models/<id>` returns 200 for every id the listing publishes,
      with the percent-encoded form of a `:` accepted.
- [x] An id the listing does not publish returns 404.
- [x] `/models/<id>` behaves as `/v1/models/<id>`, as the listing pair does.
- [x] A test covers both forms, both spellings of the separator, and the
      unknown-id case.

## Planning note

2026-09-16. Implemented in the same session it was reported, before the rest of
the set was planned. Filed afterwards so the board records the defect and its
proof rather than only the commit. It belongs to the vision's second rule —
never offer what it will not serve — and it is the reason that rule is written
in [[@router/system/vision.md]] as being about *every* publishing surface.
