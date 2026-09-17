---
state: "done"
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/proxy.ctg"
commit: "94979b74307ad7c8cadc11cfea7f6843fc86d627"
---

# The proxy answers within its bound or reports the delay

## Outcome

The proxy either answers a model request inside its configured bound or reports
the delay in the error it returns; a caller never receives a silent timeout
with no diagnosis and no way to distinguish a wedged harness from a slow
provider.

## Evidence

Observed 2026-09-16/17 by coordinator cartridge-8e. Repeated `mcp did not
answer in time` / "harness did not answer in time" responses killed four
dispatched worker agents 3–4 minutes into their turns, all with exit 0 client
sides and no diagnosis of whether the daemon, the provider, or the proxy was
the stall. Workers could not distinguish transient outage from a hang, and the
same calls later succeeded unchanged after a plain retry — the failure was
unexplained each time. No daemon-log cause was surfaced to the caller.

## Acceptance

- [x] A proxy timeout response names the stage that overran (harness, provider
      route, or cartridge call) and the bound it exceeded.
- [x] A stalled request eventually yields either its result or a failure —
      the caller is not left with neither.
- [x] A plain retry after a transient timeout succeeds without restarting the
      daemon (already true today; the box pins it).

## Scope note (2026-09-17, coordinator cartridge-2e, from analyst-2)

The Evidence section above records both `mcp did not answer in time` and
`harness did not answer in time` stalls. spec01 closes the proxy's side only.
The analyst established the mechanism: `proxy.ctg/cartridge.json` declares the
`proxy` event with no `timeout_ms`, so the host applies its default
`event_timeout_ms` of 60000 ms (`host/plan.rs:322-324`) while the proxy's own
`timeout_secs` defaults to 1800 — an event-bus request is cut by the host at
60 s with a bare `proxy did not answer in time`, thirty times before the
proxy's own diagnosed 504 could ever exist. For the `proxy` event the proxy is
the provider, so the bound belongs in this repository's manifest.

The identical mechanism for `mcp did not answer in time` belongs to the `mcp`
cartridge's manifest and is the subject of the sibling PRD
`@mcp/a-cartridge-call-is-cancellable-and-bounded`. It is not folded in here:
a cartridge declares its own surface, and widening this footprint across
`mcp.ctg` would take that decision away from the sibling. This PRD's Acceptance
is therefore about proxy-routed requests, and the worker stalls the Evidence
records are only fully answered once both PRDs land.

Acceptance clauses 2 and 3 already hold at HEAD `0692c18`: `src/service.rs:302-317`
wraps `run()` in a timeout on `timeout_secs`, `usage.rs:248` classifies it 504
and `notice.rs:27` makes it an assistant turn, pinned by existing tests at
`.cartridge/tests/unit/tests.rs:832-836` and `:2113-2115`; and no failure latch
exists anywhere, so a retry after a transient timeout cannot be poisoned. They
are not ticked here — a box is ticked on a verifier's observed evidence against
the collected revision, not on an analyst's reading.

## Verification (2026-09-17, coordinator cartridge-2e, from verifier-1)

An independent verifier reran everything against lane `529d661`, whose parent is
`proxy.ctg` HEAD `132f458` and whose diff is exactly the four footprint paths,
+142 / −13, with no stray hunk. All five Verify blocks exit 0; the suite is
`58 passed; 0 failed` with all three new test names matched; `cargo clippy --lib`
exit 0; the scoped `rustfmt --check` exit 0 and silent. `cargo clippy --workspace
--all-targets` exits 101 on `.cartridge/tests/unit/wire/tests.rs:29`, which is
outside the footprint and byte-identical to `132f458`, so it is pre-existing and
not charged here.

The falsification reproduced exactly: with the `ends_with` guard deleted in a
copy, `57 passed; 1 failed`, the single failure being
`an_upstream_rejection_survives_the_stage_wrapper`, panicking with
`proxy provider route stage stalled after 0ms: model request (429 Too Many
Requests): {}`, and the other two new tests green. So the guard is proved by a
test that fails in the world it denies — which is what two review rounds were
spent on.

**Clause 3 is deliberately left unticked.** No test in this suite retries after
a timeout. The change adds no failure state, and the analyst's reading that a
plain retry cannot be poisoned is almost certainly right, but the verifier would
not certify it on observed evidence and neither will this record. It needs
either a test that retries after a timeout, or a rewording that says what is
actually proven.

Clause 1 is ticked for proxy-routed requests only. The `mcp did not answer in
time` half belongs to `@mcp/a-cartridge-call-is-cancellable-and-bounded/the-mcp-event-declares-its-own-bound`,
and the deadline message reports the configured bound rather than measured
elapsed milliseconds. Both limits are declared in spec01 rather than hidden.

## Landing blocker (2026-09-17)

`collect` is refused by the working tree, not by the engine. The lane
fast-forwards on paper — `merge-base --is-ancestor` exit 0 and `merge-tree
--write-tree` returns the lane's own tree — but `git -C proxy.ctg status
--porcelain` limited to the footprint shows **three** dirty paths, not the two
previously recorded: `src/service.rs`, `src/notice.rs` and
`.cartridge/tests/unit/tests.rs`. All three are modified by `529d661`, so
`--ff-only` aborts, and a collect would sweep another session's work. The dirt
is demonstrably not this change's: the live `src/service.rs` has no
`proxy.timeout_secs = {}s`, and the live `cartridge.json` declares no
`timeout_ms`. Verify pass 2 also runs in `repo`, where blocks 1 and 3 would fail
against today's tree regardless.

Collect when `proxy.ctg` is clean in those three paths. Nothing else is owed.

## Clause 3 earned (2026-09-17, coordinator cartridge-24)

Clause 3 was held unticked through two coordinator sessions for a good reason:
"a plain retry succeeds" rested on reading the code, not on evidence, because no
test retried after a timeout. It is now ticked on a test, not on a reading.

`a_plain_retry_after_a_timeout_succeeds_on_the_same_service` drives a real
`timeout_secs = 1` deadline and asserts the 504, then reissues against the same
`Service` binding — no restart, no re-composition — and asserts a real answer.
The property held on the first try with no production code changed, which is
what the box itself predicted.

It was falsified twice, independently. The implementer wedged the retry path
with a per-instance poison latch and saw `59 passed; 2 failed`, disclosing the
second failure as collateral from a deliberately blunt latch. The verifier
reproduced that with four anchored edits, each asserted to match exactly once,
and then traced the collateral rather than accepting the label: the second
failure is `trace_http_isolation_…`, which panics in a common tail where
`for _ in 0..2` reissues on the same service that just took the deadline — a
second incidental witness of the same property, exactly as disclosed.

The lane was rebased from `529d661` onto `04b64eb` (`3a2b1eb`, then `94979b7`),
with a safety tag `lane-backup-529d661` left on the pre-rebase commit. The
rebase reported no conflicts and the verifier checked why rather than trusting
it: `04b64eb`'s `src/notice.rs` hunk is byte-identical to the lane's
(`index d61982d..e74b565`, same hunk header), so the lane's copy became a no-op
and the rebased commit no longer touches `notice.rs`, while blob `e74b565` is
the `notice.rs` at every relevant revision and block 3's two greps each still
match once.

Verify blocks in the lane: 0, 0, 0, 0, 0, suite 61 passed. `just check proxy` 0,
`just test proxy` 0. Pass 2 against `proxy.ctg` reads 1, 1, 1, 1, 0 before the
merge, which is the spec's predicted HEAD baseline; the verifier did not leave
that as reasoning but built the post-fast-forward tree in scratch
(`git archive 94979b7` plus the untouched dirty `src/streaming.rs`) and ran all
five blocks there: 0, 0, 0, 0, 0.

One spec edit rides along, made by me and not by a worker: block 2 pinned only
the three original test names, so the new test could have vanished unnoticed.
Its name is now in that list. The edit is strictly additive and the verifier ran
the edited block.
