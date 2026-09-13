# Implementation findings

Actual native gate fixture initially published on a required hold because the old
main read config["gitfs"], although runtime hands it the per-entry configuration.
The implementation now consumes that actual configuration directly. The native
fixture explicitly asserts required model and configured author in preview, then
proves required hold/error/malformed/body timeout and cancellation refuse.

The installed Git2.50.1 rejects symref-verify HEAD plus an update to its referent as
multiple HEAD updates. Publication now prepares an update of HEAD and verification
of the exact overlay, checks symbolic branch while Git holds its locks, checks
cancellation, then commits. Actual unit probe verifies symbolic-ref and overlay
updates refuse during prepare and the symbolic branch can change after abort.

Frozen stale-preview failure is retained in the parent. Regression proves a new
unowned trunk file survives refusal and a newly reviewed publication. Concurrent
attempts produce one winner; index/worktree are byte-preserved. Force never skips a
required gate. Missing gate config produces zero model calls. Remote helper sentinel
shows zero network publication, including with legacy push:true configuration.
