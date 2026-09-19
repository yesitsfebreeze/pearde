---
state: open
origin: requested
priority: 45
repo: "/Users/feb/dev/cartridge/fs.ctg"
work-kind: leaf
footprint:
  - "README.md"
  - ".cartridge/help.md"
  - ".cartridge/tests/unit/readme_help.rs"
---

# fs README and help.md share one source for their opening paragraphs

## Outcome

`@fs/the-fs-cartridge-ships-the-readme-its-audit-demands` (done) made
`README.md`'s opening paragraph a byte-identical copy of `.cartridge/help.md`'s
own opening paragraph, verified by hand at review time ("the most similar
pair of openings across the seventeen scores 0.26 similarity... the opening
is copied from this cartridge's own help page rather than written fresh").
That hand verification is not repeated on every later edit, so an edit to
either file alone silently drifts and nothing catches it — which is the gap
the ranking still names in row 2 ("README and help.md duplicated",
`.cartridge/memos/ranking/cartridges.md`, 2026-09-19) even though the
one-time copy already landed. This PRD turns that one-time manual check into
a standing one: a test that fails the moment the two openings diverge, so the
duplication either stays exact or stops being silent.

## Evidence

`diff fs.ctg/README.md fs.ctg/.cartridge/help.md` (2026-09-19) shows the two
files share only their opening capability paragraph and the `mode` setting
paragraph (`README.md:1-3` / `.cartridge/help.md:1-3`) verbatim; everything
after that point is legitimately different (README carries a manifest-facing
"Events" table and composition boilerplate that help.md does not, help.md
carries the full "Use" walkthrough and "Read next" links that README does
not point readers past its own repo). So the fix is not "merge the files" —
they serve different readers — it is: stop trusting a copy-paste to hold and
assert it does.

## Acceptance

- [ ] A new test (`fs.ctg/.cartridge/tests/unit/readme_help.rs`, wired into
      the existing unit test tree the way `store/tests.rs` and
      `search/tests.rs` already are) reads both `README.md` and
      `.cartridge/help.md` at their repo-relative paths and asserts the
      shared opening paragraph(s) are byte-identical between the two.
- [ ] The test fails when either file's opening paragraph is edited alone
      (verified by a throwaway local edit during implementation, reverted
      before landing).
- [ ] `just test fs` runs and reports this test passing.
- [ ] `just audit fs` and `just isolation` still report nothing for fs; this
      PRD does not touch `cartridge.json`, so the README/help agreement with
      the manifest that the prior PRD established is undisturbed.

## Proof and recovery

Starting files: `fs.ctg/README.md`, `fs.ctg/.cartridge/help.md`, both
present and already agreeing on the opening paragraph today — no repair is
needed to the prose itself, only the new test. Gates, cwd
`/Users/feb/dev/cartridge`: `just check fs`, `just test fs`, `just audit fs`,
`just isolation`. Compatible fallback: neither file's content changes; a
reader following either README or help.md sees exactly what they see today.

## Dependencies and review

Independent footprint from `@fs/fs-src-store-rs-is-one-file-per-responsibility`
(that PRD's footprint is `src/**` plus its own test file; this one is
`README.md`, `.cartridge/help.md` and a new test file, no overlap). No
`needs`: `@fs/the-fs-cartridge-ships-the-readme-its-audit-demands` is done
and this PRD only adds a check on top of what it landed, it does not revise
that PRD's record.
