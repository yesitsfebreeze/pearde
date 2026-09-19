---
state: "done"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/tests/integration/source-layout.test.ts"
  - ".cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md"
  - ".cartridge/memos/decision/the-terminal-grid-lives-in-pty.md"
  - ".cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md"
  - ".cartridge/memos/note/ui-design-aurora-gradient.md"
  - ".cartridge/memos/note/ui-design-art-deco.md"
  - ".cartridge/memos/note/ui-design-bauhaus.md"
  - ".cartridge/memos/note/ui-design-bento-grid.md"
  - ".cartridge/memos/note/ui-design-claymorphism.md"
  - ".cartridge/memos/note/ui-design-constructivism.md"
  - ".cartridge/memos/note/ui-design-dark-mode.md"
  - ".cartridge/memos/note/ui-design-flat-design.md"
  - ".cartridge/memos/note/ui-design-glassmorphism.md"
  - ".cartridge/memos/note/ui-design-material-design.md"
  - ".cartridge/memos/note/ui-design-memphis.md"
  - ".cartridge/memos/note/ui-design-minimalism.md"
  - ".cartridge/memos/note/ui-design-neo-brutalism.md"
  - ".cartridge/memos/note/ui-design-neumorphism.md"
  - ".cartridge/memos/note/ui-design-retro-pixel.md"
  - ".cartridge/memos/note/ui-design-skeuomorphism.md"
  - ".cartridge/memos/note/ui-design-swiss-international.md"
  - ".cartridge/memos/note/ui-design-tui-terminal.md"
  - ".cartridge/memos/note/ui-design-vaporwave-synthwave.md"
  - ".cartridge/memos/note/ui-design-y2k-frutiger-aero.md"
commit: "db88de4c4f6a6ebd2ff93ad592486fb8eae0af8e"
---

# Every link in the record resolves and a test says so

## Outcome

Every relative markdown link in the tracked `.cartridge/memos/**/*.md` (`git ls-files`) outside fenced code resolves from the
memo's own directory, and an executed test in the `layout` target of `just test` fails on any link
that does not.

## Acceptance

- [x] `every relative link in the record resolves` passes.
- [x] `the record link check reports a planted dead link` passes (the checker is not a no-op).
- [x] None of the three decision memos links into `boards/ui/`. Each still names the slug and cites `bed3eaaa` as the reason the link was removed.

## Analysis

Split from `@root/the-shared-record-describes-only-this-repository` on 2026-09-19 (analyst-1, coordinator-5c-3).
The census at 801aa8e finds 23 dead links: 3 decision-memo `boards/ui/` links (the board was deleted in
prd.ctg `bed3eaaa`) and 20 (not 19) `note/ui-design-*.md` `Full reference` lines. The design, steps and
Verify live in `specs/spec01.md`. Evidence: `.state/loop/every-link-in-the-record-resolves-and-a-test-says-so/analyst-1.md`
and `revision-1.md`. The justfile is untouched: `just test layout` already runs `source-layout.test.ts`.
