---
complexity: small
footprint:
  - .cartridge/tests/integration/source-layout.test.ts
  - .cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md
  - .cartridge/memos/decision/the-terminal-grid-lives-in-pty.md
  - .cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md
  - .cartridge/memos/note/ui-design-aurora-gradient.md
  - .cartridge/memos/note/ui-design-art-deco.md
  - .cartridge/memos/note/ui-design-bauhaus.md
  - .cartridge/memos/note/ui-design-bento-grid.md
  - .cartridge/memos/note/ui-design-claymorphism.md
  - .cartridge/memos/note/ui-design-constructivism.md
  - .cartridge/memos/note/ui-design-dark-mode.md
  - .cartridge/memos/note/ui-design-flat-design.md
  - .cartridge/memos/note/ui-design-glassmorphism.md
  - .cartridge/memos/note/ui-design-material-design.md
  - .cartridge/memos/note/ui-design-memphis.md
  - .cartridge/memos/note/ui-design-minimalism.md
  - .cartridge/memos/note/ui-design-neo-brutalism.md
  - .cartridge/memos/note/ui-design-neumorphism.md
  - .cartridge/memos/note/ui-design-retro-pixel.md
  - .cartridge/memos/note/ui-design-skeuomorphism.md
  - .cartridge/memos/note/ui-design-swiss-international.md
  - .cartridge/memos/note/ui-design-tui-terminal.md
  - .cartridge/memos/note/ui-design-vaporwave-synthwave.md
  - .cartridge/memos/note/ui-design-y2k-frutiger-aero.md
---

# spec01 — the record's relative links resolve, and the layout test proves it

Base: superproject HEAD 801aa8e. All 24 footprint files are tracked and clean
(`git status --porcelain -- <each path>` is empty, re-checked in revision 1). The footprint lists files
one by one, not the `note/` directory. Other sessions write untracked memos into `note/`, and a
directory footprint would abort collect after the fast-forward.
The lane must seed submodules at their pinned shas (claims since 2026-09-19 do this). 40 memo links
point into `prd.ctg`, `pty.ctg` and other siblings, and all 40 resolve at the pinned shas.

## Current dead links (census at 801aa8e, fenced code skipped): 23

- `.cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md:22` → `../../../prd.ctg/.cartridge/boards/ui/prds/copy-mode-interacts-with-the-text/prd.md`
- `.cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md:45` → `../../../prd.ctg/.cartridge/boards/ui/prds/the-gutter-is-the-boundary/prd.md`
- `.cartridge/memos/decision/the-terminal-grid-lives-in-pty.md:54` → `../../../prd.ctg/.cartridge/boards/ui/prds/the-gutter-is-the-boundary/prd.md`
- 20 lines (not 19) of the form `Full reference: [README](./<style>/README.md)`, one in each
  `.cartridge/memos/note/ui-design-*.md`: aurora-gradient, art-deco, bauhaus, bento-grid, claymorphism,
  constructivism, dark-mode, flat-design, glassmorphism, material-design, memphis, minimalism,
  neo-brutalism, neumorphism, retro-pixel, skeuomorphism, swiss-international, tui-terminal,
  vaporwave-synthwave, y2k-frutiger-aero.

## Steps

1. Record edits. Use the memo tool: `read` each memo, then `write` it with `path`, the full `body` and
   `expected_revision` (see `.cartridge/memos/system/memos.md` and `memo.ctg/README.md`). Verify never
   calls the tool, because the tool needs a daemon.
   Coordinator decision (2026-09-19): every write targets the lane through the tool's `cwd` field,
   never the live checkout. Run the command from the live repo root `/Users/feb/dev/cartridge`,
   never from the lane. `cartridge` picks its project from the process cwd, and the lane has its own
   `.cartridge/init.lua`, so a run from the lane would start or attach a second host. The lane is
   `LANE=/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/.lanes/the-shared-record-describes-only-this-repository-every-link-in-the-record-resolves-and-a-test-says-so`
   (confirm it with `ls`). For each memo:
   ```
   cd /Users/feb/dev/cartridge
   cartridge run memo "$(jq -n --arg cwd "$LANE" --arg path "<kind>/<name>.md" '{op:"read",cwd:$cwd,path:$path}')"   # note .revision
   cartridge run memo "$(jq -n --arg cwd "$LANE" --arg path "<kind>/<name>.md" --arg rev "<revision>" --rawfile body <draft> \
     '{op:"write",cwd:$cwd,path:$path,body:$body,expected_revision:$rev}')"
   ```
   Read each result's warnings and saved status. Afterwards, `git -C "$LANE" status --porcelain` must
   list exactly the 23 edited memos. `git status --porcelain` on the footprint in the live repo must
   stay empty. The executed link test is the check.
   - In each of the 3 decision memos, replace the `[<slug>](…/boards/ui/…/prd.md)` link with the bare
     slug in backticks (`` `the-gutter-is-the-boundary` `` or `` `copy-mode-interacts-with-the-text` ``).
     Add the reason in the same sentence or directly after it: the `ui` board was deleted in
     prd.ctg `bed3eaaa`. Leave the links to root-board PRDs alone, because they resolve.
   - In each of the 20 `note/ui-design-*.md`, delete the `Full reference: [README](./<style>/README.md)`
     line and the blank line before it. Those directories never existed in this repo.
2. Test. Add the following to `.cartridge/tests/integration/source-layout.test.ts` after the existing
   test, reusing its `source`, `fs`, `os` and `path`:
   - `function deadLinks(root: string, files: string[]): string[]`. For each root-relative path ending
     in `.md` that exists, it toggles a fence flag on lines matching `/^\s*(```|~~~)/`. Outside fences
     it matches `/\]\(([^)\s]+)\)/g`. It skips targets matching `/^[a-z][a-z0-9+.-]*:/i` or starting with
     `#`, strips `#…`, resolves the rest against `path.dirname(file)` and records
     `${rel}:${line}: ${target}` when `fs.existsSync` is false.
   - `test('every relative link in the record resolves', …)` takes the file list from
     `git ls-files -z -- .cartridge/memos` run in `source` (split on `\0`, drop empties, expect exit 0).
     It expects more than 100 files (387 today), so an empty list cannot pass, and expects
     `deadLinks(source, files)` to equal `[]`. Only the tracked record is judged, so both collect passes
     see the same set, and untracked memos from other sessions are out of scope.
   - `test('the record link check reports a planted dead link', …)` works in a
     `fs.mkdtempSync(os.tmpdir())` fixture, which it removes in `finally`. `note/target.md` exists.
     `note/memo.md` holds a good link `./target.md#part`, an `https://` link, a `#top` link, a dead
     `./missing.md` on line 2, and a dead link inside a ``` fence. The test calls
     `deadLinks(dir, ['note/memo.md', 'note/target.md'])` and expects exactly
     `['note/memo.md:2: ./missing.md']`.
   - Both test names must contain `link`. The existing test's name must not: it is "recorded memory
     source …", which contains `record`. Filtering with `-t 'record'` would therefore also run the heavy
     snapshot test, which clones every submodule.

A prototype of this design (`git ls-files` variant, revision 1) was probed in the analyst scratch dir. On today's record it reports all 23
links. The planted test passes. A no-op checker (`return []`) fails the planted test, and so does a
checker that ignores fences.

## Acceptance

- [ ] `every relative link in the record resolves` passes.
- [ ] `the record link check reports a planted dead link` passes. It asserts the exact list, so a no-op
      checker or one that ignores fences fails it.
- [ ] None of the three decision memos links into `boards/ui/`. Each still names the slug and cites
      `bed3eaaa` as the reason the link was removed.

## Verify

```test
run: bun test ./.cartridge/tests/integration/source-layout.test.ts -t 'link' --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: every relative link in the record resolves
pass: the record link check reports a planted dead link
```

```sh
for f in desktop-is-a-later-client-over-the-same-core the-terminal-grid-lives-in-pty the-agent-surface-preserves-the-visible-shell; do
  if grep -n 'boards/ui/' ".cartridge/memos/decision/$f.md"; then exit 1; fi
  grep -q 'bed3eaaa' ".cartridge/memos/decision/$f.md"
done
grep -q '`copy-mode-interacts-with-the-text`' .cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md
grep -q '`the-gutter-is-the-boundary`' .cartridge/memos/decision/the-terminal-grid-lives-in-pty.md
grep -q '`the-gutter-is-the-boundary`' .cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md
```

Notes for Verify:
- The `./` prefix is required. Without it, bun treats the argument as a name filter, never scans
  `.cartridge/`, and exits 1 with "filters did not match any test files". The draft's `run:` line had
  this bug.
- `-t 'link'` against today's file matches 0 tests and exits 1, so the block fails before the
  implementation lands. After it lands, the block runs in about 0.1 s.
- Both passes judge only `git ls-files` output, so the untracked memos in the live tree (`ranking/`,
  `note/asp-…`, `note/user-correction-…` and others) are not walked. In pass 2, a tracked memo that
  another session has edited but not committed is still read from the working tree.

## Review notes carried into implementation (round 2, clarification only)

- Draft memo bodies live outside the lane (e.g. the worker's scratch dir), never in the lane, or they
  become untracked files there.
- The planted-link fixture uses `fs.mkdtempSync(path.join(os.tmpdir(), 'record-links-'))`, so the
  folder lands inside `$TMPDIR`.
- Recovery: the repo pass resolves the prd.ctg link targets in the live prd.ctg checkout, not the
  pinned sha. If another session moves a board PRD between the two passes and collect fails after the
  fast-forward, rerun `prd collect` once the record is consistent; the landed commit is already on
  the repo and the failure names the dead link.

