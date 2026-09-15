---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
---

# the fold's de-link rewrites a citation of a folded part into a plain code span, indistinguishable from an ordinary backticked name — mark it, in the one function that does the rewrite

## Do
**Blocked 2026-09-08: this `Do` has no target left.** `72a1edfd` ("Port bounded
intake scheduling onto hub-owned mine completion") rewrote
`src/commands/src/commands_compact.rs` whole and deleted both `delink_bodies`
and `rewrite_index` — with them the de-link itself. Nothing in the workspace
matches `rg -n delink --type rust`. In their place `land` calls `has_links`,
and a memo any other memo cites is `relocate`d whole instead of being folded
and struck, so no fold can strand a citation and there is no rewrite left to
mark. `bf5c7ce5` had already added the `(folded)` mark this memo asks for, on
2026-09-07; `72a1edfd` removed it that evening along with the function. What is
left is the historical damage the paragraph below measures, which is
[[compact-breaks-the-links-no-gate-reads]]'s register, not a mark at a call
site that no longer exists. A person decides whether to void this memo or
re-aim it at that residue.

`delink_bodies` (`src/commands/src/commands_compact.rs:472-495`) walks every
`.md` under `memos/` after a fold and replaces `[[struck]]` with `` `struck` ``.
Give that one replacement a mark: `` `struck` (folded) ``. It is not a
wikilink, so the gate stays green exactly as it does today, and
`rg -n '\(folded\)' memos/` becomes the list of every citation whose target the
fold absorbed — the absorbing file is the one whose `sources:` names it, which
is the only pointer the record already keeps.

Delete the duplicate rewrite in `rewrite_index` (`:452-455`) in the same
change: `land` writes the index and then calls `delink_bodies` on `memos/`,
`SYSTEM.md` among the `.md` files it walks, so the row-dropping above it is all
`rewrite_index` still owes. Its unit test's `` assert!(out.contains("see `gone`")) ``
moves to a test of `delink_bodies` over a temp tree that asserts the mark.

The cost this closes, re-measured on 2026-09-07: 27 `sources:` entries across
ten condensed parts name a leaf `memos/` no longer holds, over ten distinct
lost claims — the standing figure at [[the-first-fold-named-thirteen-sources-and-kept-four-bodies]]
was 21 over nine, and a second fold has run since. Twelve backticked spans in
part bodies match one of those ten names, and four of the twelve are the
ordinary command name `nvim`: a third of the marks the fold left cannot be told
from prose by grep or by a reader. The one that matters is
`memos/knowledge/status-blocked-conflates-three-different-waits.md:18`, whose
last sentence still reads "It has since been made: `blocked-does-not-say-who-unblocks`
takes the line and refuses the fourth status" — a decision `b9cabee0` folded
and no file in `memos/` holds, asserted as settled because the de-link turned
the citation into a span. [[the-fold-de-links-the-past-not-the-future]] asks
for the same mark for the citations written after a fold, and
[[compact-breaks-the-links-no-gate-reads]] is the register the gate does not
read; this unit is the mark itself, at the one function that writes it.

## Acceptance
`cargo test -p commands delink` — a test over a temp tree holding a part whose
body cites `[[gone]]` leaves `` `gone` (folded) `` and no `[[gone]]`, and the
same run over `SYSTEM.md`'s shape leaves the struck rows dropped. Then
`just memos-check` green: the mark is not a link, so no body resolves worse
than it does now.

Run literally on 2026-09-08 from a lane cut at `864ed48c`:
`cargo test -p commands delink` compiles and reports
`0 passed; 0 failed; 126 filtered out` — the filter matches no test because no
`delink` symbol exists. The `Check` cannot be satisfied as written.

**Voided 2026-09-08, not achieved.** The coordinator's call on the lane's
blocked report: `72a1edfd` deleted `delink_bodies`, `rewrite_index` and the
de-link itself, and `land` now `relocate`s a cited memo whole instead of
folding it, so there is no rewrite a mark could sit on. The residue the lane
found — 27 orphaned `sources:` entries, twelve unmarked backticked spans —
is [[compact-breaks-the-links-no-gate-reads]]'s register and is not re-opened
here.

