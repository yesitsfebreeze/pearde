---
state: "specced"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/policy.ctg"
footprint:
- "README.md"
---

# The policy cartridge ships the README its audit demands

## Outcome

`policy.ctg` ships a `README.md`, so `just audit` stops reporting `hard: no README.md`
for it and a reader arriving at the cartridge can tell what capability it owns
without reading its source.

## Evidence

`just audit` from the superproject root, run 2026-09-17 by coordinator
cartridge-2e: **0 of 17 cartridges pass the hard checks**, and 17 of the 17 fail
on `hard: no README.md`. `policy.ctg` is one of them; its line reads:

```
policy.ctg  FAIL  123 source lines in 1 file(s), largest init.lua at 123, 6% comment, 10 tracked
```

Every one of the 17 does have its `.cartridge/help.md` — the missing artefact is
the README specifically. The host `cartridge.ctg` has one, so the standard is
not aspirational; it is met exactly once, by the thing that is not a cartridge.

This work had no representation on any board — live, done or deferred — while
eleven live rows propose brand-new cartridges. The standing memo is explicit:
a cartridge "owns one capability, declares its whole surface in cartridge.json,
ships its own README and help page, and is not done until `just audit` and
`just isolation` report nothing for it", and the vision's own "How we get there"
step 2 says every hard `just audit` finding becomes a PRD on the owning board.
Filed 2026-09-17 to close that gap.

## Acceptance

- [x] `policy.ctg/README.md` exists and states, in its own words, the one capability
      this cartridge owns and the surface it declares — not a copy of another
      cartridge's README with the name changed.
- [x] It agrees with `policy.ctg/cartridge.json` and `policy.ctg/.cartridge/help.md`:
      every event or op it names is really declared, and it names no surface the
      manifest does not carry.
- [x] `just audit` no longer reports `hard: no README.md` for `policy.ctg`.

## Note on scope

This PRD is one cartridge's README and nothing else. The other sixteen are
filed separately on their own boards, because each lands in its own repository
and a single footprint across seventeen submodules would sweep every one of
them. The two additional hard findings the same audit reports —
`event docs.discover declares no schema` and `event tools.selftest declares no
schema` — are their own PRDs, not part of this one.

## Verification (2026-09-17, coordinator cartridge-2e)

Landed outside the engine by session `cartridge-ae`, whose user asked it to make
`just audit` pass, at `policy.ctg` — see the adoption record for the sha. Checked
here rather than taken on report:

- `just audit` from the superproject root reports **17 of 17 cartridges pass the
  hard checks** and zero `hard:` findings, where this morning it reported 0 of 17
  with 17 missing READMEs plus two schema findings.
- `policy.ctg/README.md` exists and is over the gate's ten-line minimum.
- A mechanical check across all seventeen READMEs compared each one's
  **Defines** and **Listens to** lists against its own `cartridge.json`: every
  event named in a README is declared in that manifest, every declared event
  appears in the README, and no README names a surface its manifest does not
  carry. All seventeen consistent.
- Each README's opening paragraph is byte-identical to the lead of its own
  `.cartridge/help.md`, and the most similar pair of openings across the
  seventeen scores 0.26 similarity. They are not one template with the name
  swapped; each states its own cartridge's capability, taken from that
  cartridge's own help page.

Recorded honestly: the opening is copied from this cartridge's own help page
rather than written fresh. That satisfies "its own words" in the sense the box
means — one capability, one source of truth, agreeing with the manifest — and it
is worth knowing that help.md is the origin if either is ever edited alone.
