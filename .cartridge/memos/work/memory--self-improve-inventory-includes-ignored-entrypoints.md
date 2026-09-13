---
kind: work
level: 10
status: done
description: Correct the self-improve inventory recipe so ignored entry points and linked skills remain visible.
read_when: approving or implementing the bounded self-improve inventory correction
---

# self-improve-inventory-includes-ignored-entrypoints

## Do

Approved and implemented on 2026-09-08; see [[approve-self-improve-inventory-scope]] for the reply that authorized it.

Observed defect, measured on 2026-09-07 in /Users/feb/dev/memory on macOS, code revision c9763ac77c80de34a3ff789110c73871625c8361 and record revision 4194216fae5352e9f1fe63f58729c1a2a096be1c: [[@prd/routine/plan-cartridge-work.md]] lines 24–27 require a harness inventory, but its prescribed `rg --files --hidden .claude scripts -g '!worktrees/**' -g '!.claude/worktrees/**'` returned only three scripts. `git check-ignore -v .claude/commands/self-improve.md .claude/settings.json` identified `.gitignore:47:/.claude/*`. Following links alone exposed the terminal skill but still omitted ignored entry points.

After approval and after the existing untracked routine is released by its author, change only the inventory instruction in `memos/routine/self-improve.md`. Enumerate existing optional command, skill, agent, and script directories with `rg --files --hidden --no-ignore --follow .claude/commands .claude/skills .claude/agents scripts`, omitting absent roots, and check `CLAUDE.md`, `.claude/settings.json`, and `justfile` explicitly. Preserve the rule that absent optional paths are not defects and that only scoped file contents are opened. Do not change ignore rules, settings, tools, or runtime code.

The benefit is a complete local entry-point inventory without scanning worktrees. The tradeoff is following links inside the explicitly selected roots; this must not become an audit of user-global configuration or transcripts. Keep [[terminal]] discovery and its unsupported-LSP fallback unchanged. The existing routine file and pre-existing generated-index changes are not owned by this assessment.

## Check

Run on 2026-09-08 against `routine/self-improve.md` as landed. The corrected
command
`rg --files --hidden --no-ignore .agents .claude scripts -g '!worktrees/**' -g '!.claude/worktrees/**'`
returned 23 paths and no `worktrees/` path. The three entry points the
prescribed command had missed are all present: `.claude/agents/rust.md`,
`.claude/settings.json`, and the terminal skill, now at
`.agents/skills/terminal/SKILL.md`. Require those entry points, not a fixed
count. `.claude/commands/self-improve.md` is not among them because
`.claude/commands/` was deleted as a duplicate of the skills
([[one-skill-file-per-routine-under-two-harness-names]]).

`--follow` is deliberately absent: it would descend the `.claude/skills`
symlink and return every skill twice.

`ls -ld CLAUDE.md .claude/settings.json justfile` listed all three; CLAUDE.md
is a symlink to `memos/SYSTEM.md`.

The revised instruction omits absent optional roots, and user-global files,
transcripts and worktrees stay outside its scope.

`just memos-check` passes.
