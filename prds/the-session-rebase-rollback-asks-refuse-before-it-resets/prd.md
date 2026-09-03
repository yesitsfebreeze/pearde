---
state: open
origin: requested
priority: 70
complexity: 0
blast-radius:
---

# the session rebase rollback asks refuse before it resets

`resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh`
is **RED on main**: one FAIL against six PASS.

```
FAIL  resources/board/session.py:586 — git reset is not gated:
      reset --hard throws the working tree away.
      Ask @resources/board/refuse.py before it runs
```

The call is the rollback arm of a failed rebase: when `rebase` returns non-zero
and `rebase --abort` succeeds, the branch is reset hard to the `was` SHA read
before the attempt. The intent is a restore, not a discard — which is why it
reads as safe and was written ungated — but it is a `reset --hard` in a tree
the running session may not own, and the invariant (memo `ba69efa`) admits no
exception without a recorded reason. `lanes.py:257` does the same job gated and
is the shape to copy; `collect.py:750` and `:1142` show the recorded-reason
form.

## Acceptance

- [ ] `bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` exits 0, its FAIL line gone and the six PASS lines unchanged.
- [ ] The rollback still restores the branch on a conflicting rebase: a fixture whose rebase conflicts leaves the branch at the pre-rebase SHA and reports the conflicting files.
- [ ] The gate is `refuse.py`, matching `lanes.py:257`, or the exemption carries a recorded reason the invariant reads, as `collect.py:750` does.
