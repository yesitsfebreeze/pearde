---
state: open
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge/memory.ctg"
footprint:
  - "src/rpc/src/server.rs"
---

# A frozen query reads the bank without touching it

## Outcome

Every query commits access heat, so measuring the bank changes the bank. The benches
avoid this by excluding access persistence, which means they measure a store that
production never has. Read-only owner attachments and any future evaluation need a
query that leaves no trace. The test-model-thing issue tracker asked its author for
the same thing, a frozen mode, after a benchmark run through chat rewrote the
weights on disk.

Add `touch:false` to the query RPC and `--no-touch` to the CLI. A frozen query runs
the full pipeline, skips `commit_access` and the `task_commit_access` enqueue in
`src/rpc/src/server.rs`, and reports `touched:false` in its explain output. Attached
read-only instances always query frozen.

## Acceptance

- [ ] `memory query --no-touch` returns the same ranking as a touching query on a fresh store and leaves every heat value and `heat_updated_at` unchanged.
- [ ] An owner attachment's query never enqueues a commit-access task.
- [ ] The replay and mature benches run with the frozen flag and record that in their protocol files.
