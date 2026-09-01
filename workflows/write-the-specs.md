---
atomic: write-the-specs
subject: turn what the build stands up into implementable units
date: 2026-08-28
updated: 2026-09-01
runs: 27
---

# write-the-specs — units another worker can finish

## Do

1. One `prds/<prd>/specs/specNN.md` per implementable unit, from
   @references/templates/spec.md.
2. Frontmatter carries `complexity:` and `footprint:`. The footprints across
   the specs are what the overlap check reads, so a path in two specs is a
   decision, not an accident.
3. Every acceptance box names an output a check can read. Write the box
   spelling inside backticks in any prose about it — the matcher is
   line-based and fence-blind, so a pasted open box becomes a real one.
4. Give each spec a `## Verify and Proof` block whose every command names a
   path from that spec's own `footprint:` — a check that reads a footprint file through a script outside it (`index.py check` on `index.md`) counts as naming it. Never the whole workspace. There is
   no `verify:` frontmatter key — the template's keys are a closed set.
5. Say in each spec what already stands from the build and what is left.
6. `grep -c '^- \[ \]' prds/<prd>/specs/*.md` — every spec has at least one
   box, and none is ticked before an implementer runs it. Then
   `awk '/^```/{f=!f;next} f' prds/<prd>/specs/*.md` and read every command
   back: each must name a path from its own spec's `footprint:`.
7. `pearde specced <prd> --check --as <id>` — the gate that reads the set, writing nothing. It refuses without `--as <id>` or `PEARDE_AS` — the persona is on the line even in check mode — and refuses a file naming line and reason, and a set over `split-above` or `specs-above`.

## Done when

- Every spec has `complexity:`, `footprint:`, acceptance boxes and a
  `## Verify and Proof` block.
- No box asks for a commit message — committing is not the implementer's act.
- No command in any block runs the whole workspace.
- Each spec states what the probe already left in the tree.

## Fails when

| seen | means | do |
|------|-------|----|
| `over split-above: N > 40 — REFINE it` | the set is heavier than the board allows | weigh each spec against the siblings' spec files first; if the weight is honest at that scale the verdict is REFINE with a `## Split` table, never a lower number |
| an implementer reports a box whose command prints a different number than the box asserts | the number was written from the build's memory rather than from running the command **as the box spells it** — a `grep -c` counts every matching line, and a word quoted in a comment beside the code counts too | run each box's own command line verbatim, from the repo root, and paste what it prints into the box. A count in a box is quoted output, never a recollection; when a literal appears in both prose and code, aim the box at the content instead of at the count |
| `collect` refuses with `spec<NN> exit <n> — nothing written`, and every command in the block passes when you run it by hand | a line in the block is a **board-wide gate** — `doctor`, a full harness sweep, a repo-root `git status`/`git diff` — and `collect` runs the block under `pipefail`, so that command's exit becomes the block's. The unit's pass is now conditional on every other PRD on the board. `141` instead of `1` means the same shape sigpiped into a `grep -q` | capture, then grep: `out=$(<board-wide command> 2>&1 \|\| true)` then `printf '%s\n' "$out" \| grep -E "<rows>"`. The rows stay visible and stop deciding the exit. Gate **only** on commands reading a path from this spec's own `footprint:`. Check it the way collect will, not by hand: `bash -c "set -o pipefail; $(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"` must exit 0 |
| the report path already holds a previous pass's report | this route is run twice on one PRD — the analyst's pass and an implementer's — and both write `prds/<prd>/report.md` whole | read it before writing and carry its `## Findings` forward into yours by name. A finding reported and not fixed is the route's only record of a defect nobody owns; an overwrite that drops it loses the board's sole copy |
| `collect` refuses with `spec<NN> exit <n> — nothing written`, and the block's last line is a `grep -c` printing `0` | `grep` exits 1 when it matches nothing, and a count of zero is the *expected* answer for a line that proves a red is not yours — so the block's happiest number is also its failing exit | append `\|\| true` to any `grep -c`/`grep -vc` whose passing value is `0`; the count still prints. Then check it the way collect will — extract the block with `awk` and run it under `set -o pipefail`; it must exit 0. Running the lines by hand will never show this |
