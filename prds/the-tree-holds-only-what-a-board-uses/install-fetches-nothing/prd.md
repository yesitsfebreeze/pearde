---
state: specced
origin: requested
priority: 50
complexity: 12
blast-radius: mid
workflow: probe-then-spec
---

# install fetches nothing

The Obsidian plugin download leaves `install.sh --apply` — an installer whose thesis is links, never copies — and lives in `pearde vault`. Install runs offline; `--remove` stops deleting bundles.

## Done means

`install.sh` makes no network call; `pearde vault` fetches when bundles are missing.

## Needs

No gate.
