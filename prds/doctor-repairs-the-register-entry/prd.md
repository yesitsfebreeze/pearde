---
state: done
origin: requested
priority: 55
complexity: 16
blast-radius: low
workflow: probe-then-spec
actual: 0.8h
---

# Doctor repairs the register entry

*Source: `docs/content/docs/improvements/obsidian-register-repair.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** obsidian · **Axis:** integration (3 → 6) · **Pulls the score up by
~8 points**

## Why now

Doctor's `vault` row reads Obsidian's register
(`~/Library/Application Support/obsidian/obsidian.json`, passwd-resolved) and
reports `broken` with no entry. It stops there. The repair is a shell dance
away — quit Obsidian, run `pearde vault --wait --open`, reopen — and nobody
runs it, because the row says *broken*, not *how it gets whole*. The one file
the tool writes behind the app's back is the one file no verb can fix.

## The change

`pearde doctor --fix` gains a `vault` repair: when the board resolves and the
register lacks the entry, write it — through the same writer
`pearde vault --wait` uses, refusing while Obsidian runs, printing the quit
→ write → reopen line instead of doing it behind the app's back. The row
then reads `repaired` (or stays `broken` with the same refusal it has today),
and doctor's own report carries the command that finishes the job.

## Done when

- `env -i bash doctor.sh --fix` on a board whose register entry was removed
  prints `vault repaired`, and the register holds the entry afterwards.
- The same run with Obsidian up prints the refusal line and exits without
  writing — the register is never rewritten under the app.
- The `vault` row's pass/fail logic is untouched — only the fix path is new.

## Fails when

- A second board on the machine resolves to the same project root: two
  entries, one vault. The repair refuses both and names both, the way the
  board resolver refuses two children with `settings.md`.

## What stays out

No register migration, no multi-vault handling beyond the refusal. The
writer already carries the precedence rules; repair only reaches it.

## Report

spec01: exit 0

── A. plain --fix, Obsidian not running, real doctor.sh, no writer ─────
  ok   A the row starts broken — not registered
  ok   A the real cmd_vault bug is surfaced, not swallowed (see ## Finding)

── B. --fix, Obsidian not running, stubbed writer succeeds ─────────────
  ok   B prints the literal repaired line

── C. --fix, Obsidian running: refuses, writes nothing ─────────────────
  ok   C names the refusal, not a write
  ok   C never claims it repaired anything
  ok   C the register is untouched

── D. --fix, two entries already resolve to this project ───────────────
  ok   D names both ids
  ok   D names both ids
  ok   D refuses rather than picking one
  ok   D the register is untouched — still both ids
  ok   D the register is untouched — still both ids

── E. no --fix: unchanged behaviour, no repair attempted ────────────────
  ok   E row still just reports broken
  ok   E no repair line without --fix
  ok   E no refusal note without --fix

14 ok · 0 fail
index.py check:
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
memos.py check: 43 lines
