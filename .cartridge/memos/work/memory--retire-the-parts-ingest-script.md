---
kind: work
level: 10
status: done
description: delete scripts/parts_ingest.sh and the just memos-ingest recipe once the watcher carries the record
read_when: "executing the fold"
---

# retire-the-parts-ingest-script

From [[@prd/work/memory--fold-parts-into-the-graph.md]]. Last child.
[[@prd/work/memory--interim-parts-ingest.md]] said this script retires with the fold; this is
that.

## Do
Delete `scripts/parts_ingest.sh` and the `parts-ingest` recipe in
`justfile`. Strike [[@prd/work/memory--interim-parts-ingest.md]]'s row nowhere — the part stays,
its `status` already `done`, and its body gains one line naming what
replaced it.

## Check
`just memos-ingest` no longer exists, `just memos-check` green, and
`memory report --group claim_kind` still returns a label per part kind with the
script gone — proving the watcher, not the script, is what carries the
record.

Landed 2026-09-05. The `Check` failed as written: the watcher carried
nothing — off by default, and blind to `memos/` behind the repo's
`.gitignore`. `the-watcher-watches-parts` records the config that makes
it true (`.memory/memory.toml`, `[watcher] roots = ["parts"]`), proven first in
an isolated tree, then on this store after one daemon restart:
`report --group scheme` gained `file`. `scripts/parts_ingest.sh` and the
`parts-ingest` recipe are gone; `just memos-ingest` errors with
"Justfile does not contain recipe". `the-watcher-walks-its-roots-at-start` holds what
the watcher does at boot, which is what makes the retirement safe.
