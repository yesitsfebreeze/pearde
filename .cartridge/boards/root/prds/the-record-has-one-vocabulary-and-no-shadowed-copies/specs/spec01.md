---
complexity: small
footprint:
  - /Users/feb/dev/cartridge/.cartridge/memos/type/prd.md
  - /Users/feb/dev/cartridge/.cartridge/memos/type/note.md
  - /Users/feb/dev/cartridge/.cartridge/memos/type/type.md
  - /Users/feb/dev/cartridge/.cartridge/memos/prd/the-binary-target-passes-on-a-runner.md
  - /Users/feb/dev/cartridge/.cartridge/memos/prd/the-windows-runner-gates-again.md
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/terminal.md
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/terminal-control.md
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/neovim-control.md
  - /Users/feb/dev/cartridge/.cartridge/memos/note/release-baseline.md
  - /Users/feb/dev/cartridge/.cartridge/memos/note/release-status.md
  - /Users/feb/dev/cartridge/.cartridge/memos/note/release-state.md
  - /Users/feb/dev/cartridge/.cartridge/memos/note/release-checkpoint.md
  - /Users/feb/dev/cartridge/.cartridge/memos/routine/self-improve.md
  - /Users/feb/dev/cartridge/.cartridge/memos/grammar/record-grammar.md
  - /Users/feb/dev/cartridge/.cartridge/memos/grammar/memo-grammar.md
  - /Users/feb/dev/cartridge/.cartridge/memos/decision/the-work-checkpoint-journals-are-not-this-passs-candidate.md
  - /Users/feb/dev/cartridge/.cartridge/memos/principle/encode-lessons-in-structure.md
  - /Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/decision/memory--the-pearde-workflow-is-the-work-record.md
  - /Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/decision/memory--new-work-is-on-the-plan-by-default.md
  - /Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/grammar/memory--drill-grammar.md
---

# spec01 — one vocabulary in the workspace record, no shadowed shipped memo

Three deletions and four repairs, all inside the two memo records.

1. Delete the memos that name a kind the board already owns (`type/prd.md`,
   `prd/*`), a runtime that is not here (`routine/terminal.md`,
   `routine/terminal-control.md`, `routine/neovim-control.md`) or a release
   journal the board replaced (`note/release-{baseline,status,state,checkpoint}.md`).
2. Delete the two workspace `type/` leaves that shadow memo.ctg's shipped
   declarations — `type/note.md` and `type/type.md`. Every composed cartridge
   ships byte-identical copies of both, so the kinds stay declared.
3. Repoint every unqualified wikilink whose leaf those deletions remove
   (`[[terminal]]`, `[[terminal-control]]`, `[[neovim-control]]`, `[[type]]`,
   `[[note]]`), and the pre-existing dangling `[[drill]]`, at
   `[[@prd/routine/root--drill.md]]` or at the shipped qualified path.
4. Strike from `@prd/decision/memory--the-pearde-workflow-is-the-work-record.md`
   and `@prd/decision/memory--new-work-is-on-the-plan-by-default.md` every
   sentence that makes a work memo the PRD. Both are already `status:
   superseded`; the port table and the present-tense claims go, the history
   line stays.

`cartridge call memo '{"op":"index"}'` cannot be the gate here: the host
serving this project was started from an older build and answers `unknown
token`, and this work may neither start nor stop a host. The shadow check
below is the same question asked of the composed record on disk.

## Acceptance

- [ ] No memo named in the PRD's first box is left under `.cartridge/memos/`, and `.cartridge/memos/prd/` is gone.
- [ ] No leaf under `.cartridge/memos/` has the same `<kind>/<name>.md` path as a memo shipped by a cartridge that `.cartridge/init.lua` composes.
- [ ] Neither named decision memo contains the phrase `work memo`, and `@prd/routine/root--drill.md` is the only `routine/*drill*` memo in the workspace record or any composed cartridge record.
- [ ] No unqualified wikilink in either record names a leaf the deletions removed (`terminal`, `terminal-control`, `neovim-control`, `type`, `note`, `drill`).

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge
set -e

W=/Users/feb/dev/cartridge/.cartridge/memos
COMPOSED="auth memo sessions docs router policy gitfs fs pty prd tools harness agent live mcp proxy"

# 1. named memos deleted
for f in type/prd.md routine/terminal.md routine/terminal-control.md \
         routine/neovim-control.md note/release-baseline.md note/release-status.md \
         note/release-state.md note/release-checkpoint.md; do
  if [ -e "$W/$f" ]; then echo "FAIL still present: $f"; exit 1; fi
done
if [ -e "$W/prd" ]; then echo "FAIL .cartridge/memos/prd still present"; exit 1; fi

# 2. no workspace leaf shadows a shipped memo of a composed cartridge
shadows=""
for c in $COMPOSED; do
  d="/Users/feb/dev/cartridge/$c.ctg/.cartridge/memos"
  [ -d "$d" ] || continue
  for r in $(cd "$d" && find . -name '*.md' -type f | sed 's|^\./||'); do
    [ -e "$W/$r" ] && shadows="$shadows$r <- $c
"
  done
done
if [ -n "$shadows" ]; then echo "FAIL shadowed shipped memos:"; echo "$shadows"; exit 1; fi

# 3a. neither decision memo still calls a work memo the PRD
P=/Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/decision
if grep -n 'work memo' \
   "$P/memory--the-pearde-workflow-is-the-work-record.md" \
   "$P/memory--new-work-is-on-the-plan-by-default.md"; then
  echo "FAIL a decision memo still says a work memo is the PRD"; exit 1
fi

# 3b. exactly one drill routine in the composed record
drills=$(find /Users/feb/dev/cartridge/.cartridge/memos/routine \
              $(for c in $COMPOSED; do echo "/Users/feb/dev/cartridge/$c.ctg/.cartridge/memos"; done) \
              -path '*/routine/*drill*' -type f 2>/dev/null | sort)
if [ "$drills" != "/Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/routine/root--drill.md" ]; then
  echo "FAIL drill routines: $drills"; exit 1
fi

# 4. no unqualified link to a leaf the deletions removed
if grep -rnE '\[\[(terminal|terminal-control|neovim-control|type|note|drill)\]\]' \
     --include='*.md' "$W" /Users/feb/dev/cartridge/prd.ctg/.cartridge/memos; then
  echo "FAIL dangling unqualified wikilink"; exit 1
fi

echo "spec01 OK"
```
