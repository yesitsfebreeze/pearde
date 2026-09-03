---
state: done
origin: requested
priority: 85
complexity: 18
blast-radius: mid
workflow: probe-then-spec
actual: 1.52h
---

# common-py-gains-a-git-runner-and-a-section-extractor — resources/common.py` holds one git runner and one section extractor, each shaped (via `check=`/`default=`/`raise_as=`-style parameters) to cover every existing caller's return-or-raise contract, so every module below has one version to point at.

resources/common.py` holds one git runner and one section extractor, each shaped (via `check=`/`default=`/`raise_as=`-style parameters) to cover every existing caller's return-or-raise contract, so every module below has one version to point at.

## Report

spec01: exit 0
PASS: every checked caller contract reproduced
common.py parses
