---
state: open
origin: requested
priority: 70
complexity: 15
blast-radius:
needs: the-doctor-refuses-drift
---

# the guard costs one walk of prds

`stamp()` walks `prds/` under each board only; the guard state file is saved once per call and stamp keys older than the session's `since` are pruned. The walk and re-read rules apply only while a pass is active (`.state/pass.md` present or `PEARDE_AS` set); the `state:`-by-hand rule applies always.

## Done means

`guard.py pre` on `ls prds` under 30 ms above interpreter start on this board; the state file stops growing across 100 calls; a plain session's `ls` of prds is allowed.

## Needs

`one-primitive-one-definition` and `every-documented-command-exists` — both children of `the-doctor-refuses-drift`; the frontmatter `needs:` names that container, which is done exactly when both are.
