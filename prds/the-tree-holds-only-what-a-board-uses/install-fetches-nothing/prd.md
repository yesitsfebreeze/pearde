---
state: done
origin: requested
priority: 50
complexity: 12
blast-radius: mid
workflow: probe-then-spec
actual: 0.99h
commit: f68b88f cb399bc
---

# install fetches nothing

The Obsidian plugin download leaves `install.sh --apply` — an installer whose thesis is links, never copies — and lives in `pearde vault`. Install runs offline; `--remove` stops deleting bundles.

## Done means

`install.sh` makes no network call; `pearde vault` fetches when bundles are missing.

## Needs

No gate.

## Report

spec01: exit 0
0 problem(s)
spec01 green

spec02: exit 0

7 passed, 0 failed, 0 skipped
spec02 green
