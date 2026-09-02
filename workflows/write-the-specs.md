---
atomic: write-the-specs
subject: turn what the build stands up into implementable units
date: 2026-08-28
updated: 2026-09-02
runs: 31
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
4. Give each spec a `## Verify and Proof` block in which every path is
   spelled **literally**, not through a variable — the checker at
   `resources/board/specs.py:523` matches the `footprint:` string, and a
   `"references/personas/$f.md"` reads as no footprint path at all. Spelling
   is not the point, though: **no command's exit may be decided by a file
   outside the footprint.** A repo-wide command (`index.py check`, `doctor`, a
   root `git status`) may be captured and printed, and the block may fail only
   on the lines of its output that name a footprint path. A file the block
   must read but does not own — a neighbour's fixture input, a sibling's
   roster — is not copied, it is **stubbed**: the block writes a minimal valid
   stand-in, so a rename or an empty read next door cannot decide the colour.
   Guard every captured output with `[ -n "$out" ]` before greping it: a
   producer that dies before printing looks exactly like a passing grep miss.
   There is no `verify:` frontmatter key — the template's keys are a closed
   set.

   Before the spec is done, run the block **the way `collect` runs it** and
   confirm the exit. The flags are `bash -e -o pipefail` — the pair at
   `resources/board/collect.py:1242` — and both matter, in opposite directions:
   `pipefail` makes a board-wide gate's exit inside a pipeline the block's, and
   `-e` aborts the block at the first bare command that fails. A block tested
   under `pipefail` alone is not tested. Awk the fence out and run it:

   ```
   bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"
   ```

   It must exit 0 on a green tree, and must exit **non-zero** with one
   footprint file mutated.

   Two shapes are safe under `pipefail` and abort under `-e`, so they are only
   ever caught by running with both. An assignment from a command substitution
   carries the substitution's status, so `out=$(<gate> 2>&1); rc=$?` kills the
   block on exactly the red output it was written to survive — write
   `out=$(<gate> 2>&1) && rc=0 || rc=$?`, or `|| true` where the code is not
   wanted. And a bare `<test> && <action>` aborts when the test is false, which
   is its passing case whenever the test is looking for something that should
   not be there — write it `if <test>; then <action>; fi`.

   A mutation proves one of two different things, and only the second is what
   the box claims. A mutation aimed at the string a `grep` reads — a renamed
   function, an altered heading, a changed wording — proves the **counter is
   wired**: the check runs and the failure reaches the exit. A mutation aimed
   at what the tool **computes** — a score, a weight, an axis, a fallback,
   a threshold — proves the block **detects a regression**. A block with only
   the first kind behind it should say so in the report rather than let the
   tick imply the second. The cheapest honest behavioural mutation is usually
   one constant in the unit's own footprint file, restored by `cp` from a
   scratch dir outside the repo and proved back with `cmp`.

   Run the block from the root `collect` will run it from — the orchestrator's
   checkout, not your lane — and where the block hard-codes that path, run it
   once with your own root substituted and leave the block as written. A block
   rewritten to name the lane passes for you and fails for `collect`.
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
| a block exits non-zero on the result that means it passed | a command whose **passing** result is "nothing matched" — `grep -c`, `grep -vc`, `ls <glob>`, `find … \| wc -l` — exits non-zero on exactly that result | guard the *producer*, not the pipeline: `{ <cmd> \|\| true; } \| wc -l` |
| a block exits **0** while a line in it printed a failure | the assertion is written `[ <test> ] && echo "<the good news>"`, or `<probe> && echo BAD \|\| echo OK`. Neither can fail a block: a false test prints nothing and the next command's status becomes the block's, and the `&&…\|\|` pair always exits 0 | put the assertion **last** and write it bare — `[ ! -s "$f" ]` — or accumulate a counter in the loop and end on `[ "$N" = 0 ]`. Then run the block the way collect does (`awk` it out, `set -o pipefail`) **against a tree where the check should fail**, and confirm it does |
| a box or block asserts a literal total of the PRD's **own** probe | the spec has locked its harness shut: a later pass cannot add the check a thin box needs without reddening the spec that names it | assert the tally *parses* and `failed == 0` — never a total, not even the probe's own. A floor (`>= N`) is honest; an equality is a wall |
| `specced` refuses `<spec>:<n>: `## Verify and Proof` holds no fenced `sh` block` and the block is plainly there | a line inside the block begins `## ` — commonly a heredoc writing a markdown fixture. The section reader in `resources/board/specs.py` is line-based and fence-blind, the same way the acceptance-box matcher is | write the fixture's headings with a placeholder prefix and raise them at run time (`sed 's/^@@ /## /'`). Never a literal `## ` at line start inside a verify block, in a heredoc or out of one |
| a spec contracts a file under `.pearde/memos/` and `memos.py check` goes red the moment it lands | the index by kind is generated, and adding a memo makes `memos/README.md` stale — a file no footprint names and that the spec cannot omit | run `python3 resources/memos.py index <board>` and check `git diff --stat` names one added row; the index is part of adding a memo, not a separate edit. Say so in the report, because the footprint is wrong and the next author of a memo spec should carry the index row in it |
| a `## Verify and Proof` block reads as instructions to a person — a `<placeholder>` argument, a `# note the dir` comment standing in for a value, a bare `$?` echoed after the command it describes | the block was written to be *read* and never run, and `collect` runs it: `<that dir>` is parsed as a redirect from a file named `that`, and the spec dies on a syntax error with every box already ticked | run every block, of every spec in the set, exactly as `collect` will — `bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"` — before `specced` is called. `specced --check` reads the block's *presence*, never its exit, so a block that cannot parse passes the gate |
