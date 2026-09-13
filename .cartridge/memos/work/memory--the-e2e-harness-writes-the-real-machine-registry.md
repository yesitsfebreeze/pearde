---
kind: work
level: 10
status: done
description: the harness isolated `XDG_RUNTIME_DIR` and not `XDG_STATE_HOME`, so every test hub wrote its roots into the developer's own `~/.local/state/memory/hub-roots.json`; `XDG_STATE_HOME` now points at the per-test state dir and a full suite adds no root
read_when: "running the e2e suite, or reading the hub registry"
---

# the-e2e-harness-writes-the-real-machine-registry

## Do

`MemoryProject` gives each test a private cwd, runtime dir and config dir, and its
header says why: "`XDG_RUNTIME_DIR` isolates the hub"
(`tests/e2e/harness.rs:3`). The child gets `.env("XDG_RUNTIME_DIR", &self.runtime)`
(`:230`). It does not get `XDG_STATE_HOME`, and that is the variable
`default_registry_path` reads (`src/hub/src/hub_registry.rs:39-52`) before
falling back to `~/.local/state/memory/hub-roots.json`.

So the socket is isolated and the machine inventory is not. Read on
2026-09-06 09:20, the developer's own registry holds:

```
     0  /private/tmp
    12  /private/tmp/memory-recall-probe
    23  /private/tmp/claude-501/.../4995d3f0-.../scratchpad/fold
    12  /private/tmp/claude-501/.../85937a72-.../scratchpad/wproof
```

None of those is a project. Two are scratchpad directories belonging to other
sessions, one is a probe store ([[the-suite-measures-recall-not-precision]]),
and `/private/tmp` is the harness's own parent. They are permanent: nothing
prunes the registry — `Registry::prune_missing` has no production caller
([[the-hub-registry-is-the-machine-inventory]]) — so every run leaves its roots
behind and the count only grows, which is why eight of the roots now hold zero
entities.

The processes leak with it. Six or more `target/debug/memory hub
--idle-exit-secs 300` were alive at 09:20, all started within four seconds at
09:17 by one test run — the orphaning [[e2e-bounds-are-exec-latency]] records,
still happening, and each of those hubs is a writer of the file above.

Add `XDG_STATE_HOME` beside the runtime dir at `:230`, pointed at the same
per-test directory. One line, and it closes the last unisolated path the
harness leaves open.

## Check

A full `just test` run adds no root to `~/.local/state/memory/hub-roots.json` —
compare the file's root set before and after. `just test` green.

Planning recheck 2026-09-07: `tests/e2e/harness.rs` already passes
`XDG_STATE_HOME = self.config_home.join("state")` through `program`, alongside
runtime and config isolation. The implementation requested above is present;
this item remains open for its literal full-suite and registry comparison
Check, not another environment-variable edit. The historical assertion that
registry pruning has no caller is also obsolete: the hub reaper calls
`handler.registry.prune_missing()` on each pass. Do not remove other sessions'
registry entries or mistake their concurrent writes for this suite's roots.

Closed 2026-09-08 by measurement, not by an edit. Two suite runs from the
lane against `~/.local/state/memory/hub-roots.json`, 18 roots before: a
fail-fast `just test` (696 of 1429 tests) and a full
`cargo nextest run --workspace --no-fail-fast` (1429 tests, 1423 passed).
Neither added a harness root — a project's cwd is a `tempfile::tempdir()`
under `/var/folders`, and no `/var/folders` or `/tmp/memory-test-*` path
entered the file. The two roots that did appear, `.../scratchpad/health-root`
and `.../scratchpad/approot`, are other sessions' own probe roots, the
concurrent writes this memo's recheck warned not to count.

The six failures on the full run are none of them this one. Two are the gates
already red on `main` in their own lanes — `declared_dependencies` on the
`extension` catalogue row and `cited_paths` on a citation into an untracked
nested clone. The other four — three `hub::vanished_root_reaper_*` and
`rpc ...every_health_field_is_carried_by_the_payload` — pass on re-run in
isolation, as does `gnn_recall::recall_over_a_graph_the_gnn_has_propagated`,
which failed the first run with `handing over to new binary` in its daemon
log: eight lanes share one `target/` ([[lanes-not-a-shared-tree]]), so a
sibling's rebuild of `target/debug/memory` hot-reloads a running test daemon
out from under its own assertion.
