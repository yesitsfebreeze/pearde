---
complexity: 3
footprint:
  - src/slice.ts
  - src/jev.ts
  - src/main.ts
  - cartridge.json
  - README.md
  - .cartridge/help.md
  - .cartridge/memos/type/judgement.md
  - .cartridge/memos/judgement/example-which-entities-bear-on-a-change.md
  - .cartridge/tests/integration/slice.test.ts
---

# JEV retrieves ASP context and judges a bounded selection

The implementation builds on jev bd7b7e0. It adapts the saved slice draft to
the current ASP host contract and the combined trace-provider surface.

## Contract

A decide request accepts state, about, search, or state plus either selector.
A selector requires judgement slice {subject, k, threshold}. About permits
one to sixteen ids; search asks for at most 256 candidates. The host's ASP
method is authenticated for cartridge tokens and forbids act; ASP is not an
event dependency. No fictitious asp need is added.

Explicit absent or stale entities remain excluded if search also returns them.
One first-pass noul per candidate selects valid probabilities at or above the
threshold, sorted descending and capped by k. The final auth request uses the
original judgement questions and caller state with the selected entities.

The allow_schemes default is symbol, event, agent and memo, following the
existing PRD. Disallowed schemes send IDs ONLY. This intentionally supersedes
the old attributes exemption: trace attributes can contain complete private
records. Allowed entity descriptions are truncated to 200 characters in pass
one and 2000 in pass two; the complete outgoing request is budget checked.
The estimated limits are 24000 tokens for state plus longest question and
48000 tokens for the serialized request, at three characters per token.

The single existing deadline covers memo, ASP and both auth calls. Checks
before and after await boundaries prevent late replies from starting later
requests. Any retrieval, shape, selection or timeout failure escalates. The
plain-state path remains one call. Successful sliced replies report selected
entities, withheld reasons and both pass latencies/usages. Scheme filtering
reports every candidate whose text was withheld, including ranking rejects.
The existing event excludes retrieved entity content and sums both usages.

## Acceptance

- [x] A fixture search with 200 candidates sends the exact best k in pass two.
- [x] Full serialized requests and state/question pairs stay below their budgets.
- [x] Disallowed file text and nested trace attributes cannot reach either pass.
- [x] Stale and absent ids cannot re-enter through search.
- [x] Invalid ranking types or probabilities never survive.
- [x] Late ASP or first-pass replies start no subsequent calls.
- [x] Both docs and the judgement type describe selectors, filtering and limits.
- [x] The real host admits about/search and serves authenticated helper host:asp.
- [x] The combined live system probe records both actual TypeSafe passes.

## Verify and Proof

From the candidate JEV worktree:

```sh
bun install --frozen-lockfile
bun run check
env -u CARTRIDGE_YOLO bun test ./.cartridge/tests/integration/
git diff --check
```

The independent verifier owns the real-host probe and the coordinator owns
live credentials, runtime reload, owner audit/isolation and PRD collection.
