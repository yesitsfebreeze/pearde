---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: "done"
origin: requested
priority: 50
blast-radius: small
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 1
review-status: passed
canonical-scope: startup-eof-retains-exit-status
footprint:
  - src/sdk.rs
  - src/cartridge.rs
  - .cartridge/tests/unit/src/tests/wire.rs
commit: "1a5e9867acec1d07cd732c3af2ccf331a0979a61"
---

# Startup EOF retains exit status

A process can close stdout before its exit status becomes available. Both runtime host startup and SDK nested spawn currently poll try_wait once, report closed stdout and drop the child, losing a legitimate exit status. Wait for that owned process within the existing startup deadline. This is a separate measured lifecycle defect; tool observation behavior is unchanged.

## Acceptance

- [x] Direct and nested children that close stdout, then exit 7 after a short delay, retain exit status 7; the existing strict immediate-exit and malformed-line assertions continue to pass.
- [x] Closing stdout without exiting never hangs startup: the existing five-second deadline reports timeout and the owned child is killed and reaped.
- [x] Disposing/cancelling startup remains bounded; startup byte limits and ready handling pass unchanged.

## Baseline and proof

[Measured baseline](baseline.json): real nested SDK child closes stdout then waits 50ms before exit7; the host reports nested exited before ready: closed stdout. The startup read observes EOF before try_wait sees termination. Existing full test intermittently fails the strict exit7 assertion. No stderr is involved.

No existing canonical leaf matches this narrow EOF/exit-status race. The broader a-key-starts-its-provider-on-demand owns activation policy, and document-sidecar-lifecycle owns sidecars; neither is reclaimed or re-scored. This new defect starts round1, not a renamed failed proposal. Use public runtime test/check and exact native fixtures; preserve failure evidence. No user data, transport API or diagnostic privacy contract changes.

## Review

[Independent root review](review.md), pending round1; threshold90, maximum5.
