---
state: open
origin: requested
priority: 85
repo: "/Users/feb/dev/cartridge/live.ctg"
needs: ["a-claude-session-is-the-voice-delegate"]
footprint: ["/Users/feb/dev/cartridge/.claude/skills/live/**"]
---

# The live skill drives voice through live

## Outcome

`/live` in a Claude Code session started in this repository enables voice on a
Live conversation, arms a Monitor on `live watch`, answers with `live reply`,
turns requests into PRDs and drives the board by `PROMPT.md`. The skill's
standalone client (`voice.ts`, `whisper`, `listen`, `speak`) is replaced by
the live cartridge; `/live stop` turns voice off.

## Acceptance

- [x] `.claude/skills/live/` holds only `SKILL.md` plus at most thin wrappers around `cartridge call live`.
- [x] The skill states that irreversible or outward actions need a typed confirmation.
- [ ] A manual run with a real key: speak a request, see a `task` line, reply, hear the answer.
