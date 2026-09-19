---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge"
commit: "0ba925860f88089792bb03dce1cba756b73d9a7e"
---

# Every agent request receives a JEV decision from the shared ASP world

## Outcome

Every new request entering a connected workspace agent consults JEV against the shared ASP tree and registered peer work. The agent receives an actionable, evidence-linked decision before continuing. Missing context or service failures remain explicit. JEV remains advisory and cannot grant permissions.

Native agents and model proxy requests use harness context. Claude Code uses the project prompt hook. Other repository agents use the composed instruction or the JEV tool. Live voice must expose an assessment path for direct replies as well as delegated native workers. This does not intercept unrelated applications outside the composition.

The ASP tree exposes bounded explicit agent work and retained decision metadata. Registration records observed activity; it does not fabricate unregistered agents or claim that the tree contains information no provider has published. The existing JEV closed-set model and two-pass selection are used; model training or gate tuning is outside this integration.

This outcome serves the JEV integration gap in ranking/cartridges.md and the shared agent, harness, sessions and live workflow.

## Acceptance

- [x] JEV returns an action with ASP evidence and other registered agents, excludes the caller from peers, and reports incomplete context.
- [x] Native and proxy requests receive the decision automatically and repeated tool rounds reuse one assessment.
- [x] The Claude hook registers work before assessment and marks the session inactive when it stops; other repository agents receive the composed instruction and tool.
- [x] Direct voice replies have an assessment path with transport enforcement limits stated accurately.
- [x] Retained decisions are inspectable through ASP and survive reload without storing prompt text.
- [x] Independent review, owner gates and actual running-host model calls verify the combined workflow.
