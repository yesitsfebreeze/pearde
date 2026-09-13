---
kind: work
level: 10
status: open
claim: b424ceba 2026-09-09 15:55
estimate: 4h
description: Changing memory and Reflex context reaches ongoing turns without duplicating unchanged content or rewriting the stable prompt
needs: '[[@prd/work/memory--agent-turn-recall-is-bounded-and-fail-open.md]]'
read_when: preparing repeated memory attachments or refreshing learned triggers during a session
---

# changed-context-preserves-the-stable-prompt

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

[[@prd/work/memory--agent-turn-recall-is-bounded-and-fail-open.md]] supplies bounded facts;
[[reflex-guides-deferred-tool-visibility]] supplies learned availability guidance.
This work serves [[@prd/work/memory--proxy-turns-carry-recall-and-reflex-tools.md]].
