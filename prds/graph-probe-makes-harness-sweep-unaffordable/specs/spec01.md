---
complexity: 8
footprint:
  - .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
---

# spec01 — the graph probe extracts on a fixture, not on the repo's docs

The graph probe (`the-graph-lands-inside-the-board/probe/verify.sh`) proved the
graph's location contract with a full `extract <repo> --force`: a semantic pass
that dispatches an LLM chunk per document and ran past ten minutes, every time
doctor's `--harnesses` sweep ran — the sweep whose wall-clock design is "the
slowest harness, not the sum of all of them". The location contract extract
must prove does not need the LLM: output placement is identical for a
code-only corpus, which dispatches zero chunks.

**What already stands (analyst pass one, uncommitted in the tree):** the probe
is rewritten. Steps [1] update and [2] query keep their shape; step [3] now
runs `extract` on a run-time `mktemp` fixture holding one small Python file
(0 docs, 0 papers, 0 images — extract prints the census, so a 0-doc corpus is
checkable), asserts graph.json + obsidian vault + resolved marker + no
`graphify-out` leak inside the fixture, pins its denominator, and ends on a
check that carries the exit code. 10 checks, 10 pass, ~2 s wall-clock.

**What is left:** re-verify the rewritten probe on a tree that also carries
the other workers' edits (it was written against one), and the sweep-level
checks in spec02.

## Acceptance

- [x] `bash .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh` exits 0 and prints a line ending `0 fail`
- [x] the run's wall-clock is under 60 seconds (the sweep's own envelope)
- [x] the harness contains no `extract` invocation whose target is the repo root without `--code-only`
- [x] the harness ends on a check that carries the exit code — `tail -3 | grep -qE 'exit 1|exit "\$fail"|\[ "\$FAIL" = 0 \]'` matches, so the gate's census J counts it
      (end-state property, not a delta: the predicate already held at board
      HEAD — the pre-build file ended `exit "$fail"`, which this regex
      whitelists, so `git show HEAD:` matches. It can still fail: replacing
      the ending with a bare `exit 0` makes it go red, and drops the harness
      from census J. Verified, not newly earned by this build.)
- [x] after the run, `.pearde/graphify/` still holds the real graph and the repo root holds no `graphify-out/`

## Verify and Proof

```sh
time bash .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
grep -n "extract" .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
test -e graphify-out && echo LEAK || echo no-leak
```