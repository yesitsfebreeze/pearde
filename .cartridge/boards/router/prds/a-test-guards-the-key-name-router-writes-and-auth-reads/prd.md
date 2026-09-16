---
state: open
origin: requested
priority: 60
repo: "/Users/feb/dev/cartridge/router.ctg"
footprint:
- "src/catalog.rs"
- ".cartridge/tests"
---

# a test guards the key name router writes and auth reads

## Outcome

The name router writes a provider key under is pinned by a test on the router
side, so renaming it fails router's own suite instead of silently breaking
discovery in another cartridge.

## Evidence

Found 2026-09-16 by the round-1 reviewer of
`@auth/gpt-live-connects-over-websocket-on-the-discovered-credential`, and
re-derived by its round-2 reviewer (recorded there as F5 and F9).

That PRD's acceptance box 3 — "discovery finds an OpenAI key stored through the
router's `login` op" — holds **by inspection only**. The chain is:
`router.ctg/src/service.rs` `login` takes the name from `catalog.rs` `push_api`
(`format!("{key}_API_KEY")`, with `openai` in `API_PROVIDERS`), `settings.rs`
`Paths::from` binds the store to `config_dir`, the superproject's
`.cartridge/config.lua` points router's `config_dir` and auth's store at the same
directory, and `auth.ctg/src/openai.ts` reads `OPENAI_API_KEY` from there.

The auth half is tested (`auth.test.ts`). **The router half is guarded by
nothing**, and cannot be guarded from inside auth's footprint. The contract also
assumes both processes resolve the same *relative* path.

## Acceptance

- [ ] A router test pins the exact key name `login` writes for `openai`, so
      changing `push_api`'s format or the provider list fails router's suite.
- [ ] The test fails when the name is changed, demonstrated by observing that
      failure rather than by assertion alone.
- [ ] The relative-path assumption is either pinned too, or recorded in the test
      as a stated limit.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed on the reviewer's recommendation
(F9) rather than left as a prose residual in the auth spec: a residual nobody
tracks is indistinguishable from one nobody noticed. Scoped to the router board
because the unguarded leg is router's to guard; the auth PRD is not blocked by
this and does not `need` it.
