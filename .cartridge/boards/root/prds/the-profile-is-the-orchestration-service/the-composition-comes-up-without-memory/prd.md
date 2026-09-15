---
state: "specced"
origin: discovered
priority: 95
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- "/Users/feb/dev/cartridge/prd.ctg/cartridge.json"
---

# The composition comes up without memory

## Outcome

Taking `memory` out of the profile leaves every composed cartridge able to
start. Today it does not: `prd.ctg/cartridge.json` still declares
`needs: ["memory"]`, so `prd` fails at load and the whole graph behind it stalls.

## Acceptance

- [x] `cartridge status` on a freshly started host reports no cartridge in state `failed`, and none `waiting` on `tool.prd` or `source.board`.
- [x] `cartridge call live '{"op":"status"}'` answers `running`, and `cartridge call memo '{"op":"index"}'` answers instead of `service unavailable`.
- [x] `just verify` reaches the harness contracts rather than `service harness.selftest unavailable: harness is not active`.
- [x] Whatever `prd` used `memory` for is either declared optional or removed with its call sites, not simply deleted from the manifest while the code still calls it.

## Result

2026-09-15. Found, fixed and observed by the coordinator on a host it started
itself, after clearing a stale socket left behind by a runtime that had died.

### What was red

The profile stopped composing `memory`, but `prd.ctg/cartridge.json` still
declared `needs: ["memory"]`, so the host refused to start `prd` and every
cartridge behind it stalled.

```
$ cartridge daemon
ERROR needs `memory`, which no cartridge declares cartridge=prd

$ cartridge status
prd     state: failed   error: needs `memory`, which no cartridge declares
memo    state: waiting  waiting: tool.prd, source.board
harness state: waiting  waiting: memo
agent   state: waiting  waiting: harness, memo, tool.memo, tool.prd
live    state: waiting  waiting: agent, memo
mcp     state: waiting  waiting: tool.memo, tool.prd
proxy   state: waiting  waiting: harness, memo, tool.memo, tool.prd

$ cartridge call live '{"op":"status"}'
service `live` unavailable: no active listener

$ cartridge call memo '{"op":"index"}'
service `memo` unavailable: no active listener

$ just verify
harness contract `harness.selftest`: service `harness.selftest` unavailable: `harness` is not active
verify    composition FAIL
```

`memory.ctg` itself was correctly `disabled`, and no memory daemon ran on the
machine. The single unsatisfied declaration was `prd.ctg/cartridge.json`.

### The change

One deletion. `needs: ["memory"]` is gone, and the manifest description no
longer claims an integration the composition does not have. No call site
moved, because `prd` already treated memory as optional everywhere it used it:
`memory()` bounds every call to three seconds and rejects with no provider,
`recall()` catches that and answers `{ status: 'unavailable', authority:
'context only; PRD record is authoritative' }`, and `rememberVerified()` queues
to an outbox and records the delivery error for `replayMemory()` to retry.
Isolation stays green because `memory` is provided by a cartridge the profile
does not compose, so it is not in the checker's owner map.

Editing the manifest invalidated its recorded hash, which the host reported
plainly and which `cartridge trust` cleared:

```
ERROR /Users/feb/dev/cartridge/prd.ctg/cartridge.json: has changed since it was trusted; review it, then run `cartridge trust /Users/feb/dev/cartridge`
$ cartridge trust
trusted /Users/feb/dev/cartridge: 48 files
```

### What is green

```
$ cartridge daemon   # started by this session, and stopped by it afterwards
$ cartridge status   # 19 cartridges: 0 not active or disabled
$ cartridge call live '{"op":"status"}'
{"cwd":"/Users/feb/dev/cartridge","running":true,"url":"http://localhost:50348","voice":[]}

$ cartridge call harness '{"op":"ring"}'
{"disabled":"no memory key configured"}

$ cartridge call memo '{"op":"index","cwd":"/Users/feb/dev/cartridge"}'
kinds: 13, no kind declared by both a workspace leaf and a shipped memo

$ just check prd
check     prd        pass
$ just isolation
isolation composition pass
```

`just test prd` is red and was red before this edit: 69 pass, 6 fail both
times, the same six cases. They are the board's own `deferred` state missing
from an allowed-state list, a migration manifest count, and four statusline
cases. None is in this footprint, so none was widened into.

The named call in the parent's and the record item's acceptance,
`cartridge call memo '{"op":"index"}'`, cannot succeed as literally written:
`memo.ctg/src/service.rs:455` requires the request to carry `cwd`, answering
`trusted memo cwd required` without it. The working call adds
`"cwd":"/Users/feb/dev/cartridge"`. Those two boxes should be reworded.
