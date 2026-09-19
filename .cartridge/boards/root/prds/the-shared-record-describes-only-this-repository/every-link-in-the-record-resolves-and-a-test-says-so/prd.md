---
state: "analyzing"
origin: requested
priority: 55
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
footprint:
  - ".cartridge/tests/integration/source-layout.test.ts"
  - ".cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md"
  - ".cartridge/memos/decision/the-terminal-grid-lives-in-pty.md"
  - ".cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md"
  - ".cartridge/memos/note"
claim: "coordinator-5c-6 2026-09-19T12:28:53.239Z"
---

# Every link in the record resolves and a test says so

## Outcome

Every relative markdown link in `.cartridge/memos/**/*.md` outside fenced code resolves from the
memo's own directory, and an executed test in the `layout` target of `just test` fails on any link
that does not.

## Acceptance

- [ ] `every relative link in the record resolves` passes.
- [ ] `the record link check reports a planted dead link` passes (the checker is not a no-op).
- [ ] The three decision memos state why their `ui` board links were removed.

## Analysis

Split from `@root/the-shared-record-describes-only-this-repository` on 2026-09-19 by analyst-1 (coordinator-5c-3). No review rounds used before the split. Full analysis: `.state/loop/the-shared-record-describes-only-this-repository/analyst-1.md`.

Outcome: every relative markdown link in `.cartridge/memos/**/*.md` outside fenced code resolves
from the memo's own directory. An executed test in the existing `layout` target of `just test`
fails on any link that does not.
Decision on box 4: do not touch `.cartridge/justfile`. It is dirty with another session's edits,
and collect would commit them. Add the test to `.cartridge/tests/integration/source-layout.test.ts`,
which is clean. `just test`/`just test layout` already runs it (`_one test layout` → `bun test …source-layout.test.ts`).
No new justfile target is needed.
Record edits: in the 3 decision links, replace the link with the bare slug in backticks and add the reason
("the `ui` board was deleted in prd.ctg bed3eaaa"). In each of the 19 `note/ui-design-*.md`, delete the
`Full reference: [README](./<style>/README.md)` line. The directories never existed in this repo.
Footprint: `.cartridge/tests/integration/source-layout.test.ts`,
`.cartridge/memos/decision/desktop-is-a-later-client-over-the-same-core.md`,
`.cartridge/memos/decision/the-terminal-grid-lives-in-pty.md`,
`.cartridge/memos/decision/the-agent-surface-preserves-the-visible-shell.md`,
`.cartridge/memos/note` (only the 19 `ui-design-*.md` change; the whole dir is clean).
Test design: one function `deadLinks(recordDir)`. It walks `*.md`, skips ``` fences, matches `](target)`,
ignores `scheme://` and `#anchor`, strips `#…`, resolves the target against `path.dirname(file)` and
collects the ones that do not exist. Two tests call it:
`every relative link in the record resolves` (runs on `.cartridge/memos` and expects `[]`) and
`the record link check reports a planted dead link` (writes a tmpdir fixture with one good link, one
dead link and one dead link inside a fence, and expects exactly the one outside the fence). The second
test is the mutant, so the checker cannot be a no-op.
Acceptance:
- [ ] `every relative link in the record resolves` passes.
- [ ] `the record link check reports a planted dead link` passes.
- [ ] The three decision memos state why their `ui` links were removed.
Verify:
```test
run: bun test .cartridge/tests/integration/source-layout.test.ts -t 'record' --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: every relative link in the record resolves
pass: the record link check reports a planted dead link
```
```sh
for f in desktop-is-a-later-client-over-the-same-core the-terminal-grid-lives-in-pty the-agent-surface-preserves-the-visible-shell; do
  if grep -n 'boards/ui/' ".cartridge/memos/decision/$f.md"; then exit 1; fi
done
```
(`-t 'record'` skips the heavy snapshot test, which clones every submodule, so the block stays under 120 s.)
