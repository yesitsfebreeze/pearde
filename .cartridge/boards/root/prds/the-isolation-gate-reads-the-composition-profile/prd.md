---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
footprint:
  - ".cartridge/memos/routine/check-cartridge-isolation.md"
---

# The isolation gate reads the composition profile

## Outcome

`just isolation` measures the profile the composition actually runs. Today it
reads the wrong file and passes for the wrong reason.

## Evidence

`check-cartridge-isolation.md:52` reads the profile from
`cartridge.ctg/.cartridge/init.lua`. That file is the host's own
project-marker profile and its entire body is `return {}` — by its own comment,
"An empty profile still makes this directory a project". The composition's real
profile is `.cartridge/init.lua` at the repository root, which declares
nineteen entries: auth, memo, sessions, docs, router, policy, lsp, fs, pty,
prd, memory, tools, harness, environment, agent, live, mcp, proxy.

The gate therefore credits no profile-injected key to any cartridge. That makes
it stricter than the rule rather than looser, so `just isolation` reporting
"Isolation passed for 17 cartridges" today is not a false pass — but it is not
a measurement of the stated rule either, and the moment a cartridge legitimately
relies on a profile-injected key the gate will reject a change the rule allows.

Recorded as a known defect in `.cartridge/memos/system/vision.md` under "Where
the composition actually stands", with no PRD behind it until now.

## Acceptance

- [ ] The routine reads the composition profile at the repository root, not
      `cartridge.ctg/.cartridge/init.lua`.
- [ ] A cartridge that reaches for a key the root profile injects passes the
      gate; one that reaches for a key no profile injects still fails it, and
      the failure names the key and the consumer.
- [ ] `just isolation` still reports nothing for all seventeen cartridges at
      the recorded SHA set, and the run is in Result.
- [ ] The vision memo's "Where the composition actually stands" no longer
      carries this finding.
