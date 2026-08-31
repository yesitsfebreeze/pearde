---
complexity: 5
footprint:
  - references/parts/loop.md
  - references/parts/round.md
  - references/parts/guard.md
  - references/drill.md
---

# spec03 — the manual says where the drill starts

Already stands: the four manual edits the PRD's where-it-lands table names.
`references/parts/loop.md`: step 1's paragraph names the count and the drill
section standing first; step 2 carries the trigger table (0 questions →
nothing, 1 → that question put as today, ≥2 → one drill round over all of
them, `out` carried, the rest put) and the sentence that nothing is dispatched
while the round is unput; step 8 says it is the same drill the scan count
starts, reached because nothing else was left rather than because two
questions were. `references/drill.md` § The board's own frontier gained its
second entry point — the count on the scan. `references/parts/round.md`:
`## Asked` is what the gate reads, by title, `answered` and `out` alike.
`references/parts/guard.md` § What it counts: a claim over an unput frontier
is a refusal the loop names here, and it lands in the transition window's
`refused` count like every refused call. The loop's step-2 table is the PRD's
own wording; the PRD's "step 7 says it is the same drill" row lands on step 8,
where the drill lives since the knowledge step became loop step 7.

## Acceptance

- [x] loop.md step 1's paragraph names the count and the drill-first cut;
      step 2 carries the three-row trigger table verbatim in meaning
      (0 / 1 / ≥ 2); step 8's paragraph says it is the same drill
- [x] drill.md § The board's own frontier names both entry points — the
      blocked-board round and the scan count — and `asking N — drill first`
- [x] round.md's `## Asked` bullet says the gate reads it, and names the
      title as the word the gate matches
- [x] guard.md says where the guard is wired, the drill refusal lands in the
      transition window's `refused` count
- [x] the drill word survives the checker: `questions.py check` on this board
      is silent after the edits

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
grep -q "asking N over M" references/parts/loop.md \
  && grep -q "same drill the scan count starts" references/parts/loop.md \
  && grep -q "drill.*section stands first" references/parts/loop.md \
  && echo "loop.md says the count"
grep -q "second entry point" references/drill.md && echo "drill.md: two entry points"
grep -q "the drill gate" references/parts/round.md && echo "round.md: Asked is what the gate reads"
grep -q "asking N — drill first" references/parts/guard.md && echo "guard.md names the refusal"
python3 resources/questions.py check "$(pwd)/.pearde" && echo "questions check silent"
echo "spec03 verify done"
```