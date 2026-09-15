---
repo: /Users/feb/dev/cartridge
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
---

# Move memo's memory, fs and prd context sources to their owners as providers of one memo-declared shape, so memo carries no sibling's protocol

## Outcome

memo composes context and searches sources without knowing memory, fs or prd.
It declares two contracts and injects every provider of each by glob, the way
`tool.*` already works for the agent:

- `context.<kind>`: an evidence contributor. `<kind>` is the contributor's name
  and the `reference.kind` of every row it emits, so a readback knows which
  provider to ask. `{"op":"contribute","query","limits"}` answers a
  `Contribution` (now `Serialize`/`Deserialize` in core, with
  `deny_unknown_fields`); `{"op":"read","reference","deadline_ms"}` answers one
  exact row or `changed`/`invalid_reference`/`timeout`/`unavailable`. fs
  provides `context.file` (with its own `context_files` setting), memory
  provides `context.memory`.
- `source.<kind>`: the owner of census roots of that kind, answering
  `source_declarations` and `source_records`. prd provides `source.board`.

The profile reads `{ id = "memo", inject = { "tool.*", "context.*", "source.*" } }`.
memo's `src/sources/memory.rs` and the file half of `src/sources/file_kernel.rs`
(now `kernel.rs`) are deleted, `src/context.rs` names no provider, and
`src/source_search.rs` names `source.board` (its config key `prd_scope` is
`board_scope`). Removing memory, fs or prd from the profile removes its
contribution and changes nothing in memo.

## Acceptance
- [x] `grep -rn '"memory"\|"fs.context"\|"prd"' memo.ctg/src` reports nothing:
      the only names left are the two contributors memo serves itself.
- [x] `just isolation` reports nothing for any of 18 cartridges.
- [x] A contributor toggle naming a kind nobody provides answers `absent`, and
      a readback for such a kind `unavailable`; memo loads either way.
      Evidence: memo's `context.test.ts` and `kernel-context.test.ts`, which
      fake `context.memory` and `context.file` as their owners ship them.
- [x] Each provider proves its own adapter: fs `.cartridge/tests/unit/source.rs`
      and `context-file.test.ts`; memory `.cartridge/tests/unit/src/cartridge/source.rs`;
      prd `service.test.ts` and the two source-op suites.
- [ ] proxy still asks memo for the contributor named `memory` and checks that
      name in the snapshot it gets back (`proxy.ctg/src/context.rs`). That is
      proxy's own request through a declared need, not memory's protocol, and
      it was left as is. Making it a setting is the one open follow-up.
- [x] `cartridge help` and `cartridge settings` exit zero on the composed profile.

## Approach

1. Lift the contribution shape memo already accepts (`Contribution`,
   `Candidate`, `Availability`, the read-back request) into memo's contract
   memo and its `describe`, so a provider can be written from the memo alone.
2. In memory.ctg, provide `source.memory`: the body of memo's
   `sources/memory.rs` moved across, calling memory's own service in process.
3. In fs.ctg, provide `source.files` over `fs.context`; in prd.ctg,
   `source.board` over `source_declarations` and `source_records`.
4. memo iterates `host.injections()` for keys starting with `source.` and
   calls each with the same request; delete the three sibling-shaped modules.
5. Profile: `{ id = "memo", path = "memo", inject = { "tool.*", "context.*", "source.*" } }`.

## Result

Delivered on 2026-09-14. Two names moved from the plan: evidence contributors
are `context.*` and root owners `source.*`, because they are different
contracts and one glob would have asked prd to contribute evidence. The
contributor `files` is now `file`, since the name is the kind. Memo's three
evidence budgets (`sources.id_bytes`, `source_bytes`, `text_bytes`) went with
the memory adapter: the contract's caps in `cartridge::fabric::evidence::valid`
are what a provider checks against, and a knob above them was dead.

Unresolved prerequisites at migration: `[[a-cartridge-brings-its-own-surface]]`.
