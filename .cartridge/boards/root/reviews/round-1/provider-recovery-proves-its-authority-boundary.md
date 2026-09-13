---
kind: work
level: 10
status: open
estimate: 1d
description: route recovery proves finite incident budgets and review boundaries without falsely completing interrupted work
read_when: verifying the native provider healer beyond happy-path repairs
---

# provider-recovery-proves-its-authority-boundary

## Do

The existing route healer has a finite incident recovery budget and observable
exhaustion, coalesces concurrent failures, handles missing credentials and a
failed diagnosis route, and declares recovery only after an affected-route
stream succeeds. Unknown code/config repairs remain reviewable proposals,
never automatic deployment. Interrupted tasks remain interrupted.

This completes [[memory-provider-recovery]] using the native model service,
not a second recovery daemon. External failure sources need an explicit
incident input; absence of such input is reported rather than invented.
