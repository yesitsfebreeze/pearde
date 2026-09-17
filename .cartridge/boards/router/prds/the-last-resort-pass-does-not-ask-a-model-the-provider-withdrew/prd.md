---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
  - "src/proxy.rs"
  - "src/health.rs"
---

# The last-resort pass does not ask a model the provider withdrew

## Outcome

A model the provider has withdrawn is never asked again, including on a turn
where every other candidate is already shelved. Today the routing loop's
last-resort pass drains the deferred queue and still sends the request to a
route whose incident says the model no longer exists, spending a call that
cannot succeed on a turn that was already going to fail.

## Evidence

Measured 2026-09-17 by the analyst of the sibling PRD
`a-deprecated-model-leaves-the-catalog-instead-of-being-retried`, in a scratch
copy of `router.ctg` at `7b2917a` with that sibling's `retry_due` guard already
applied: three turns in which both healthy siblings answered 503 asked the
withdrawn route five times. The path is the last-resort pass at
`src/proxy.rs:449-450,497`.

The sibling PRD closes the ordinary path — while a turn has any other
candidate, a withdrawn route is not asked. It cannot close this one, because
its footprint is `src/health.rs` and its own unit test file, and this fix needs
`src/proxy.rs`. After the sibling lands, this is the only path left that can
reach a withdrawn route.

## Acceptance

- [ ] On a turn where every candidate is shelved, a route whose open incident
      is `Kind::Withdrawn` is not asked by the last-resort pass, while a route
      shelved for any other reason still is.
- [ ] The turn still ends in a reported failure rather than silence when the
      withdrawn route was the only remaining name.
- [ ] A test drives a real turn in which every sibling is shelved and asserts
      the withdrawn route received zero calls, failing in the world it denies.

## Needs

Blocked on the sibling `a-deprecated-model-leaves-the-catalog-instead-of-being-retried`
only in the ordering sense: this PRD's test is written against the behaviour
that sibling establishes, and its measurement above already assumes that
guard. Specify it after the sibling lands, or specify it independently and
state the assumption.

## Direct evidence, contributed 2026-09-17 by session cartridge-ae

While fixing a separate panic this PRD's title made it re-read, the author of
`router.ctg` `9b5897b` observed the behaviour this PRD asserts, in a running
test rather than by reading the code: **with routes marked withdrawn and the
providers healthy, a request received a 200 from a withdrawn model.** The
last-resort pass does ask a model the provider withdrew; sorting the deferred
queue by `retry_at` only pushed those routes to the back rather than removing
them.

That is stronger than the measurement this PRD was filed on (5 calls over 3
turns with the sibling's `retry_due` guard applied), because it shows the
withdrawn route not merely being asked but being *served* — so the defect is
reachable on a turn that then succeeds, not only on one that was already
failing.

Related, and deliberately not folded in: `9b5897b` fixes a panic on the same
path. A withdrawn incident carries `retry_at = u64::MAX` so nothing waits for
it, and the wait added in `7b2917a` took the soonest deferred retry time without
asking whether it was a real reopening; with every deferred route withdrawn that
is `u64::MAX`, giving a wait of roughly 584 billion years and
`overflow when adding duration to instant` at `library/std/src/time.rs:429`. It
needs every candidate withdrawn and every attempt failing at once. The fix stops
the router **waiting** on a withdrawn route. It does not stop it **attempting**
one, which is this PRD's subject and remains open.
