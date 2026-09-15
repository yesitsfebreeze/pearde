---
complexity: small
footprint:
  - /Users/feb/dev/cartridge/prd.ctg/cartridge.json
---

# spec01 — the planning cartridge stops hard-needing memory

`prd` already treats memory as optional everywhere it actually uses it. Only
the manifest disagrees, and the manifest is what the host enforces.

- `src/service.ts` `memory()` rejects when no provider is reachable and bounds
  every call to three seconds, with the comment "memory is context and never
  holds up planning".
- `recall()` catches that rejection and returns
  `{ status: 'unavailable', authority: 'context only; PRD record is authoritative' }`.
- `rememberVerified()` writes to an outbox and records the delivery error;
  `replayMemory()` retries later.

So the change is the declaration, not the behaviour: drop `"memory"` from
`needs` in `prd.ctg/cartridge.json`, and stop the manifest description claiming
an integration the composition no longer has. No call site moves, because every
one of them already has its unavailable path. Nothing is added: this is one
deletion plus a sentence.

Isolation stays green because `memory` is provided by a cartridge the profile
does not compose, so it is not in the isolation checker's owner map.

## Acceptance

- [x] `prd.ctg/cartridge.json` has no `memory` entry in `needs`, and its description no longer claims integration with memory.
- [x] A freshly started host reports `prd` active, and no cartridge failed or waiting on `tool.prd` or `source.board`.
- [x] `cartridge call live '{"op":"status"}'` and `cartridge call memo '{"op":"index"}'` both answer instead of `service unavailable`.
- [x] `just check prd` and `just isolation` pass, and `just test prd` is unchanged by this edit: the same 69 pass and 6 fail as before it, all six failing for reasons outside this footprint.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge

# The declaration is gone and the description no longer claims it.
bun -e '
  const m = await Bun.file("prd.ctg/cartridge.json").json();
  const needs = m.needs ?? [];
  if (needs.includes("memory")) { console.error("FAIL: needs still declares memory"); process.exit(1); }
  if (/integrated with memory/i.test(m.description ?? "")) {
    console.error("FAIL: description still claims memory integration"); process.exit(1); }
'

# Every memory call site still has its unavailable path, so the deletion
# removed a declaration and not a behaviour.
grep -q "memory is context and never holds up planning" prd.ctg/src/service.ts
grep -q "status: 'unavailable'" prd.ctg/src/service.ts

just isolation | grep -Eq '^isolation +composition +pass$'
just check prd | grep -Eq '^check +prd +pass$'

# The manifest edit changes no test outcome. The six failures are the board's
# own deferred state, a migration manifest count and four statusline cases,
# none of them in this footprint.
( cd prd.ctg && bun run test 2>&1 ) | grep -Eq '^ 69 pass$'
( cd prd.ctg && bun run test 2>&1 ) | grep -Eq '^ 6 fail$'

echo 'prd no longer hard-needs memory'
```
