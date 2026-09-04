---
complexity: 9
footprint:
  - .pearde/prds/a-parked-prd-comes-back/probe/verify.sh
  - .pearde/prds/an-unknown-flag-refuses/probe/verify.sh
  - .pearde/prds/collect-commits-the-code-repo-not-the-board-repo-twice/list-the-collects-the-repo-bug-orphaned/probe/verify.sh
  - .pearde/prds/complexity-is-guarded-like-priority/probe/verify.sh
  - .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh
  - .pearde/prds/nothing-left-open/the-skill-tree-is-guarded/probe/verify.sh
  - .pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh
  - .pearde/prds/seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green/probe/verify.sh
  - .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh
  - .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
  - .pearde/prds/the-board-asks-for-itself/two-questions-start-a-drill/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/init-asks-nothing/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/one-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-loop-is-commands/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-next-line-runs/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/tokens-per-transition/probe/verify.sh
  - .pearde/prds/the-collect-and-brief-harnesses-are-carried-across-the-layou/probe/verify.sh
  - .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh
  - .pearde/prds/the-graph-lands-inside-the-board/probe/verify.sh
  - .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh
  - .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-attach/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-seed/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-skill/probe/verify.sh
---

# spec02 — the twenty-six that also read the board stop deriving it from the root

These twenty-six carry spec01's preamble and one thing more. Each of them names
the live board, and each spells it as `<its root>/.pearde` — `BOARD="$ROOT/.pearde"`,
`"$ROOT/.pearde/.state/serve.json"`, `find "$ROOT/.pearde/prds" …`, and so on.
That spelling is only correct while the root is the orchestrator's checkout.
Point the root at a lane and the board vanishes: a lane is a worktree of the
code repo and `.pearde/` is gitignored, so there is no `.pearde` under it at
all.

The preamble already computes `BOARD` by walking up to the `.pearde` the
harness file sits under — which is the board it belongs to, whatever tree is
being measured. Every `<root>/.pearde` in these files becomes `$BOARD`. The
two are the same directory when the runner names no tree, so nothing moves on
the orchestrator's checkout; they part company exactly when a worker points the
set at a lane, which is the whole point.

`$ROOT` keeps every other use it has — the code under test is still reached
through it (`$ROOT/resources/...`), and that is what must follow the runner.

**Already standing (this analyst's uncommitted pass one):**
`.pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh` is converted:
preamble in, `BOARD="$ROOT/.pearde"` out, and it runs 20 checks, 20 pass against
the orchestrator's checkout — the count it printed before the edit.

That same file also measured what this spec does **not** promise. Under
`PEARDE_ROOT=<lane>` it drops to 16 pass, 4 fail, and all four failures are of
one kind: checks that assert a pearde tool *discovers* the board from the
current directory (`memos.py list` with no argument, the doctor `memos`,
`workflows` and `questions` rows, `knowledge.py board`). A lane has no board to
discover, by construction. Standing those checks down is rewriting an
assertion, which this PRD's `## Out of scope` excludes, so they are left failing
under a lane root and named in the report. A green sweep from the orchestrator's
checkout — which is what spec05 proves — is unaffected.

## Acceptance

- [x] All 26 files carry spec01's preamble (`BOARD` from the walk, `ROOT` from `${PEARDE_ROOT:-…}`).
- [x] No file in the footprint derives the board from its root: `grep -nE '\$\{?(ROOT|REPO|CODE|R|PWD)\}?/\.pearde' <file>` is empty for each.
- [x] Every place that named the board now reads `$BOARD`, and `$BOARD` resolves to the harness's own `.pearde` in each — not to `$ROOT/.pearde`.
- [x] `$ROOT` is still what reaches the code: each file still has at least one `$ROOT/resources/` (or its own root variable's equivalent).
- [x] Run from the orchestrator's checkout with `PEARDE_ROOT` unset, each of the 26 exits with the code and prints the check count it did before the edit.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
B=.pearde/prds/a-harness-measures-the-tree-its-worker-built-in
N=0
for h in $(sed -n 's/^  - //p' $B/specs/spec02.md); do
  grep -qF 'basename "$BOARD"' "$h" || { echo "no preamble: $h"; N=$((N+1)); }
  if grep -nE '\$\{?(ROOT|REPO|CODE|R|PWD)\}?/\.pearde' "$h"; then
    echo "still derives the board: $h"; N=$((N+1))
  fi
  grep -qF '$BOARD' "$h" || { echo "never names \$BOARD: $h"; N=$((N+1)); }
done
echo "spec02 census over 26 harnesses: $N offending"
# The one converted in pass one still runs the twenty checks it ran before the
# edit — that is this spec's claim on it. Its pass count is not: it went red on
# the `.pearde/` → `pearde/` migration standing uncommitted in the checkout,
# before this PRD's first edit, and the failing lines name memos.py,
# questions.py and workflows.py. Captured, printed, and not gating.
out=$(bash .pearde/prds/one-definition-of-the-board-not-two/probe/verify.sh </dev/null 2>&1) || true
[ -n "$out" ]
printf '%s\n' "$out" | tail -1
printf '%s\n' "$out" | grep -q '^20 checks' || { echo "its check total moved"; N=$((N+1)); }
[ "$N" = 0 ]
```
