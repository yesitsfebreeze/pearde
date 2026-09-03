---
state: done
origin: requested
priority: 85
complexity: 16
blast-radius: mid
needs:
  - common-py-gains-a-git-runner-and-a-section-extractor
workflow: probe-then-spec
actual: 2.17h
---

# the-lane-and-repo-modules-delegate-to-common — resources/board/lanes.py`, `orphans.py`, `ramp.py`, `refuse.py`, `repos.py`, `shared.py` and `transitions.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`.

resources/board/lanes.py`, `orphans.py`, `ramp.py`, `refuse.py`, `repos.py`, `shared.py` and `transitions.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`.

## Blocked

**2026-09-03 17:28 — the lane will not rebase**

`lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` does not land on `session/s98669`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-doctor-refuses-drift/one-primitive-one-definition/the-lane-and-repo-modules-delegate-to-common`.

**2026-09-03 17:28 — the lane will not rebase**

`lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` does not land on `session/s98669`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-doctor-refuses-drift/one-primitive-one-definition/the-lane-and-repo-modules-delegate-to-common`.

**2026-09-03 17:29 — the lane will not rebase**

`lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` does not land on `session/s98669`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-doctor-refuses-drift-one-primitive-one-definition-the-lane-and-repo-modules-delegate-to-common` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-doctor-refuses-drift/one-primitive-one-definition/the-lane-and-repo-modules-delegate-to-common`.

## Report

spec01: exit 0
PASS: every checked caller contract reproduced
all seven parse
