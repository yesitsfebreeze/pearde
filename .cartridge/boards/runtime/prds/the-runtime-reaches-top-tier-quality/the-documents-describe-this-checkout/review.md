# The documents describe this checkout — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-documents-describe-this-checkout` (`prd.md`).
Scope: one leaf. Every path and command the docs name exists in this checkout.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **DELIVERED** (pending verification).

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `e80a533cbfd71d80b7fb38b10156f64854e8c838e541aeb5583dfe059773ae51` (frontmatter only; prior text `592be7750c130f21cfc375d3f79c5cfd37a7145cf89b8ed0da9bb81ee7c16fe6`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

Evidence: the docs were rewritten for the transport host (`c80f63f`, `d2a761e`). `b1494bb` removed the composition (profiles, `builtin/`, the INSTALLED CARTRIDGES list), and `53ed88e` added a system memo that keeps the README current.

On both lines, `rg -i` over `llms.txt`, `docs/*.txt`, `README.md` and `.cartridge/README.md` finds none of the seven findings:
- `python`, `scripts/`, `workspace.py`;
- `builtin/`, profiles, the `ui` cartridge, "13 Rust";
- `just isolation/layout/describe`, `src/settings.rs`.

Every `src/`, `docs/` or `.cartridge/` path the docs name exists, except three that are correct in context:
- `~/.cartridge/trust` and `~/.cartridge/catalog.json` live in the home directory;
- `src/main.ts` appears inside an example `cartridge.spawn` snippet in `docs/creating-cartridges.txt:100`.

The docs name no `just` recipe.

Residual gap, not blocking: the automated doc-path test from acceptance 2 was not built; the README system memo is the chosen keep-current mechanism. Acceptance 3 is moot now that the list is gone.

Result: no score (verdict round). Status: `delivered-pending-verification`.
Unresolved blocking findings: none.
Validation (read-only):
- the `rg -i` stale-term scan on both lines;
- a shell loop that extracts `(src|docs|.cartridge)/…` paths from the docs and tests `-e`, on both lines;
- `grep 'just '`;
- `shasum -a 256`.

Rounds used / remaining: 2 / 3.
Next action: collect; recheck after the landing leaf merges the 5 doc files (`llms.txt`, `docs/{architecture,creating-cartridges,transport,writing-good-cartridges}.txt`) changed on both lines.
