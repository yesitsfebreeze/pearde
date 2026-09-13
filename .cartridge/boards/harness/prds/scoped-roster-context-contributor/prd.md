---
repo: /Users/feb/dev/cartridge/harness.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: harness
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: scoped-roster-context-contributor
needs: ["@sessions/an-agent-is-one-lookup-from-the-roster/scoped-roster-projection", "@landscape/landscape-composes-system-context/context-contributor-contract"]
---

# Render the authenticated roster through Landscape context

Add an optional host-configured roster contributor to harness composition using the existing Landscape evidence collector. Render bounded untrusted roster data once per composed request. Default configuration performs no roster lookup and leaves the swarm block blank.

## Acceptance

- [x] Actual sessions+harness SDK composition renders an authenticated20-session roster below the configured cap; disabled configuration produces no roster call or block.
- [x] Host actor/credential configuration cannot be overridden by JSON arguments; mismatched session identity, unavailable source and deadline expiry yield explicit unavailable context without exposing other scopes.
- [x] The source revision and unavailable state appear in inspection; closing-frame/prompt-like data remain escaped conversation evidence, and original compaction/transcript gates pass.

## Baseline and review

The parent roster baseline records actual absent SDK operations at423ecd3 and existing harness/Landscape boundaries. This child inherits original roster review rounds1–2; independent round3 review by /root passed 95/100 before implementation. Tests use disposable data. The roster and independently reviewed existing fallback edits are integrated in the actual owner at 698a4dc9555a6b3ad8d46dcc5dd3a14463048e70, with an entirely clean tree equal to tested candidate d3a4187. Detailed proof/recovery is in specs/spec01.md.
