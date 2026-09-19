---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/memos-are-asp-entities-and-memo-kinds-are-asp-types'
---

# context providers become ASP providers and the context path is deleted

## Outcome

Every `context.<kind>` provider answers as an `asp.<kind>` provider instead,
and memo's `context.*` injection and its `context` op are deleted in the same
change. Deferred landscape PRDs remain outside this run and unchanged. Live provider and consumer contracts are reconciled through the owner-addressed deletion plan.

## Start at

- `memo.ctg/src/context.rs`: the `context.` prefix, contributor toggles and
  the `read` state machine (`available`, `changed`, `unavailable`).
- `memo.ctg/cartridge.json:127`: `needs: ["tool.*", "context.*", "source.*"]`.
- `cartridge.ctg/src/host/plan.rs:62-76`: glob `expand`, which ASP reuses for
  `asp.*`.
- Providers today: `fs.ctg/src/source.rs` (`context.file`), memory
  (`context.memory`), and any other `listen` of the form `context.*`.
- Deferred records excluded: `@landscape/landscape-composes-system-context` and its descendants, and `@landscape/one-search-covers-the-record-and-memory`.

## Decision (2026-09-19, ASP coordinator)

A read-only analysis of every `context.*` provider and consumer (2026-09-19)
settles the plan:

- **Consumers.** Only two things call memo's `context` op: the prompt-recall
  hook (`.cartridge/hooks/prompt-recall`, written by
  `cartridge.ctg/src/cli/setup.rs` from `src/cli/prompt-recall.sh`, and `just
  recall`) and proxy (`proxy.ctg/src/service.rs:403-450`, `prepare`, memory
  rows only). Both move to ASP `search`.
- **The `read` action has no production caller** (only memo's integration
  tests). ASP's `stale` marking on expand replaces it; it is deleted, not
  ported.
- **`context.file`** nominates only `context_files`, which nothing in this
  project sets, so it answers `empty` here. ASP already gives the file node,
  its SHA-256 revision and a `read` action for the text. It is deleted, not
  ported.
- **`context.lsp`** returns the language-server catalog (id, installed). That
  is `tool.lsp status`, not a fact about the world. It is deleted, not ported.
- **`memory`** has no ASP provider yet: child `memory-contributes-its-entities-to-asp`.
- **`documents`** (memo-internal) has no scheme yet: child
  `memo-contributes-documents-to-asp`.
- **`kernel`** (memo-internal) is the host's `cartridge:` entity minus state
  and generation: child `the-host-s-cartridge-entities-carry-state-and-generation`.
- Then `the-prompt-recall-and-the-proxy-read-asp-search`, and last
  `the-context-path-is-deleted`, which removes `context.*`, memo's `context`
  op, every copy of the evidence contract and the `context.*` need.
- The landscape records are deferred. Current task instructions exclude them, so deletion does not change their files or states.

## Acceptance

- [ ] `rg -n '"context\.' --glob cartridge.json` finds nothing, and every
      former provider declares `asp.<kind>`.
- [ ] Each fact a former provider used to return through `context` is now
      returned through ASP `expand`, with the same owner and revision, and a
      named test shows it.
- [ ] Deferred records remain unchanged and `./task prd check --board root` is clean.
