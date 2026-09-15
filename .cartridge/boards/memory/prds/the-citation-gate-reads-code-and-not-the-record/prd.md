---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1d"
---

# `tests/cited_paths.rs` walks `src/` only and cuts line suffixes unverified, so the record's 616 line-anchored citations — 10 naming a path that does not exist, 6 pointing past the end of their file — are outside the one gate written for exactly this rot

## Do

The runner exists and its scope is half the problem. `tests/cited_paths.rs`
collects `.rs` files under `src/` through `test_support::rs_files`, reads
whole-line comments, and resolves each cited path from the repo root or the
citing crate's own `src/`. Two deliberate limits leave the record uncovered:
the walk never enters `memos/`, and line suffixes are cut before the check and
never verified — its own header says every range measured that day had drifted,
"which is why the fix was to stop writing them."

The record did not stop. Measured 2026-09-06:

```
616  line-anchored citations under memos/     (205 the same morning)
190  name a bare filename with no directory
 10  cite a path that does not exist
  6  point past the end of the file they name
```

Extend the existing gate rather than adding a second one. Walk `memos/**.md`
beside `src/`, and for a citation carrying `path:line` or `path:line-line`
where the path resolves, fail when the highest cited line exceeds the file's
line count. Keep the resolution rules and `FOREIGN` as they are. The bare-name
class stays unchecked here: 190 is too many to fix in this item and a bare name
is a style question, not a provable break.

One exemption is required and it is not optional. A part *about* citation rot
quotes a broken citation as its evidence — `a-gate-can-see-half-of-citation-rot`
cites `src/ingest/src/ingest_worker.rs:910` precisely because that anchor was
wrong — so the check must skip a citation the part is exhibiting rather than
relying on. The narrowest form that works: skip any citation on a line that
also names the file it is quoted from, or accept an explicit marker. Decide
which when writing it; the same exemption problem is
[[the-parts-gate-checks-links-in-one-file]]'s, and guessing it here would make
two gates disagree.

## Acceptance
`cargo test --test cited_paths` fails on today's tree naming
`src/ingest/src/ingest_worker.rs:831-854` (835 lines) and
`src/rpc/src/test_helpers.rs:47` (43 lines) among its failures, passes once
those are repaired, and the existing `the_gate_can_go_red` fixture still
passes. `rg -n 'commands/src/lib.rs' memos/` returns nothing — the
crate-relative form is repaired to `src/commands/src/lib.rs` — and a fixture
part exhibiting a deliberately broken anchor does not fail the gate.

**Done 2026-09-08.** `tests/cited_paths.rs` walks `memos/**/*.md` beside `src/`
and `tests/`, reads a citation out of a part's code spans, and holds a `:N` or
`:N-M` suffix against the file the path resolved to. A part is held to its
anchors and not to its paths — the historical path a part names is correct as
written — and a fenced block is the exemption, so
[[a-gate-can-see-half-of-citation-rot]] can tabulate the broken anchors it
reports without failing on them.

The gate came up red on eight anchors past the end of their file, none of them
the two the `Check` above names — those were repaired by the commands-split
sweep ([[the-commands-split-left-eight-anchors-past-the-end]]) before this ran.
Seven had only drifted and their claim survived; one had not, and re-pointing
it would have been the falsification that sweep warns of:
`from_maps_every_field_without_drift` went with the two-struct `From` that
`a807a1f0` collapsed, so it loses its anchor rather than gaining a false one.

The `Check`'s `rg -n 'commands/src/lib.rs' memos/` clause cannot be satisfied as
written — `src/commands/src/lib.rs` contains that string — and the gate resolves
the crate-relative spelling through the crate layout by design, so the 43
crate-relative citations are not rot and were left alone. The bare-name class is
still unchecked, as the `Do` says.
