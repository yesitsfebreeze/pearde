---
state: done
origin: requested
priority: 0
complexity: 34
blast-radius: high
workflow: probe-then-spec
actual: 15.8h
commit: e55a0e7 d4626c9
---

# every-module-finds-its-siblings-by-one-rule — One file puts every directory under `resources/` on the import path, one probe finds the repo root by `resources/pearde.py`, discovery walks every directory under `resources/`, and every tool that launches a sibling script finds it rather than spelling `board/` — so a file can move with no second edit anywhere; nothing has moved yet

One file puts every directory under `resources/` on the import path, one probe finds the repo root by `resources/pearde.py`, discovery walks every directory under `resources/`, and every tool that launches a sibling script finds it rather than spelling `board/` — so a file can move with no second edit anywhere; nothing has moved yet

## Answers

**The four files outside the footprint — settled 2026-09-03 by the orchestrator.**
Two implementer passes stopped on the same fork: `resources/board/session.py`,
`resources/board/shared.py`, `resources/knowledge.py` and
`resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh`
carry a hand-rolled preamble of their own and hold spec03 boxes 2 and 5 and
spec04 box 6 red, and none of them was in any spec's `footprint:` because all
four landed *after* the specs were written.

The contract is *every* module, so the four are in scope and the footprint was
the thing that was wrong. They have been added — the three Python modules to
`spec03`, the invariant harness to `spec04`. **Fix them the way their siblings
were fixed and tick the boxes.** No frontmatter edit is owed to the implementer
any more; the footprint now holds what the contract always meant.

## Report

spec01: exit 0
spec01 ok

spec02: exit 0
spec02 ok

spec03: exit 0
spec03 ok

spec04: exit 0
probe: every module finds its siblings by one rule — tree /Users/feb/dev/infra/pearde/.pearde/.sessions/s88291
  ok   resources/pearde_path.py is the one file the rule lives in
  ok   it names resources/ and every directory under it: resources board graph invariants scout
  ok   no file on that path shadows a stdlib module
  ok   no entry point still probes for resources/board/plan.py
  ok   the probe is written out once, in pearde_path.py
  ok   renaming resources/board/ to core/ leaves 'pearde help' byte-identical
  ok   15 modules moved to four new directories — 'pearde help' byte-identical
  ok   specs.py imports its siblings from its new directory
  ok   transitions.py imports its siblings from its new directory
  ok   run.py imports its siblings from its new directory
  ok   brief.py imports its siblings from its new directory
  ok   memos.py imports its siblings from its new directory
  ok   guard.py imports its siblings from its new directory
  ok   pearde_path.script finds every launched sibling after the move
  ok   no python file addresses a sibling script as a path it builds itself
  ok   no launcher spells board/ any more
  ok   doctor.sh carries res() — the shell half of the same rule
  ok   doctor.sh spells $DIR/board/ nowhere
  ok   res() finds plan.py, serve.py and brief.py in the cut tree
  ok   plan.py is untouched — the sibling PRD owns it, so it is out of this footprint
  ok   plan.py's own two-line preamble, alone, still cannot find a moved render — the handoff
  ok   31 modules open with the one rule
  ok   no module imports a sibling without the rule (plan.py excepted)

probe: 23 passed, 0 failed
spec04 ok
