---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
needs:
- "@memory/agent-turn-recall-is-bounded-and-fail-open"
estimate: "4h"
---

# Changing memory and Reflex context reaches ongoing turns without duplicating unchanged content or rewriting the stable prompt

## Do

Volatile recalled facts and learned tool guidance remain separate from the stable
system prompt. Unchanged context is not appended repeatedly; context that
reappears after an empty interval is available again. Session or project changes
cannot retain another context's suppression state. Source labels and the
distinction between retrieved facts and trusted guidance survive preparation.

Pi's change-gated context messages are the reference. The expected behavior
includes repeated identical content, changed content, and A then empty then A;
the stable prompt remains byte-identical across those cases. Existing host
message and attachment mechanisms remain authoritative, with no second agent or
parallel conversation representation.

[agent-turn-recall-is-bounded-and-fail-open](../agent-turn-recall-is-bounded-and-fail-open/prd.md) supplies bounded facts;
[[reflex-guides-deferred-tool-visibility]] supplies learned availability guidance.
This work serves [proxy-turns-carry-recall-and-reflex-tools](../../../proxy/prds/proxy-turns-carry-recall-and-reflex-tools/prd.md).
