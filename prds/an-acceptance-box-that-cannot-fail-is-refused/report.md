# report — an-acceptance-box-that-cannot-fail-is-refused

**VERDICT: SPECCED**

## What the build did

`specced` now refuses a spec whose `## Verify and Proof` block cannot exit
non-zero, at the site `pearde specced` already read: `check_spec` in
`resources/board/specs.py` walks every fenced `sh` block and, when the block
cannot redden under the exact runner `collect` uses (`bash -e -o pipefail`,
cwd = the code repo, last command's exit read), appends
`verify block <N> cannot fail — <why>` to the refusals — the same path every
other specced refusal rides, exit 1, nothing written.

The contract is an edit to an existing footprint file (`resources/board/
specs.py`), built in place per the `attempt-the-build` atomic's rule for
footprint edits; the walker itself is new code and lives in the same file as
one section, `# ── can a verify block fail? ─` — the runner semantics it
models live in `collect.py verify_blocks()` and its `run(["bash","-e","-o",
"pipefail"], cwd, script)` call, left untouched.

## What already stands (in the tree, uncommitted)

- `_cannot_fail_why(script)` in `resources/board/specs.py`: a walker that
  models `bash -e -o pipefail` — and-or lists (only the last element can
  abort; earlier failures merely carry status), `||` fallbacks resetting the
  status, `!` inversions exempt from `set -e`, `exit`/`exec` killing the
  shell through any operator when their status can be non-zero, always-0
  builtins, bare assignments (`x=1` is 0, `x=$(cmd)` inherits), `pipefail`
  counting every pipeline member, heredoc bodies, function bodies, comments,
  continuations, quotes and `$( )` nesting. Loop/branch constructs
  (`if`/`while`/`do`) and `set +e` blocks read as able to fail — the
  unanalysable shapes are accepted, never refused.
- The refusal call in `check_spec`'s verify branch, one message per
  offending block, naming the shape.
- The sibling session's workflow-carry-down hunks in the same file survived
  intact and untouched; my hunks kept disjoint from theirs (docstring,
  `read_specs` tuple, `specced` body — none of it is mine).

## What is left (for the specs)

- spec01 — the refusal exists and fires at specced time: the walker plus the
  check_spec call site, refusing the four mechanical shapes the collect
  runner surfaced (everything guarded behind a closing always-0 command,
  `!` inversions, bodies in conditions, bare `true`), accepting a live block.
  `bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/
  verify.sh` pins both ends: 2 passed, 0 failed.
- spec02 — the refusal message names the block and shape a worker can act on
  (block number, the guard pattern, the always-0 last statement) and the
  gate survives a `specced --check` run with nothing written.

## Findings (in the report, not in any spec)

- `workflows.py list` refused the PRD name as a board argument; the bare
  form from the repo root lists fine. Cosmetic, not mine.
- `bash -e` exempts a failed left-of-`&&` operand but the list's carried
  non-zero result still becomes the whole script's exit when it is the last
  statement — `false && true` alone exits 1. The walker models this;
  collect keeps failing such blocks, correctly.
- `local` is not always-0 in bash 3.2 (`local` outside a function exits 1) —
  a fixture proved it red, so it stays out of the walker's ALWAYS0 set.
- Mid-pipeline `!` (`x | ! test`) is a syntax error in bash — the walker
  treats the block as able to fail rather than guessing the parse.
- Pre-existing, before my first edit: `doctor` exit 1 on `origin broken`
  (derived in flight vs requested — 7 then, 6 now, moving under other
  sessions), `view off`, `plan off`, `harnesses off`, `jstests off`.
  Not this PRD's.
- The knowledge query "A Verify block that cannot fail is refused" gap was
  auto-enqueued to `.pearde/wiki/pending/260831-17e4.md` (priority med) —
  a gap of the record, not a question of mine.

## Baseline and after

- before the first edit: `specced-is-a-command` harness 90/90, index.py
  check exit 0, doctor exit 1 (`origin broken` pre-existing),
  `git status --short` clean, 0 diff hunks.
- after: `specced-is-a-command` 90/90 (unchanged), index.py check exit 0,
  doctor exit 1 — same pre-existing `origin broken` row only — and my own
  `probe/verify.sh`: 2 passed, 0 failed.
- Randomized differential vs real `bash -e -o pipefail` across ~25k
  generated scripts (heredocs, function defs, subshells, redirects,
  inversions, env-prefixes, loop bodies): 0 wrong refusals across the
  recorded runs; every refusal the analyzer makes was one bash could not
  contradict.

## Footprint

- `resources/board/specs.py` (edit in place: the walker section, the
  refusal call in `check_spec`)
- probe artifacts: `.pearde/prds/an-acceptance-box-that-cannot-fail-is-
  refused/probe/` — `verify.sh` (2/2), `analyzer.py` (the walker's
  development copy, kept for the differential), `baseline/`.

## Scores

complexity: 24
blast-radius: mid
workflow: probe-then-spec

## This pass — specs written for a build already through

This pass wrote the specs for a build that was already through: the code
(`_cannot_fail_why` and the `check_spec` refusal call in
`resources/board/specs.py`) stood untouched from the earlier session, and
`bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/
verify.sh` was re-run against it now, unchanged: **2 passed, 0 failed**,
same as the earlier pass recorded. No code was touched this pass — only
`specs/spec01.md` and `specs/spec02.md` were written, each an implementable
unit the prior report's "What is left" section already named, each carrying
its own `## Verify and Proof` pointing at the standing probe harness.
Sum of spec complexity: 14 + 10 = 24, at or under the cap of 40, 2 specs, at
or under the cap of 6.

Re-running `python3 resources/knowledge.py query "a verify block that
cannot fail"` this pass returned 8 hits, 0 strong, and auto-enqueued a
*second*, separate gap: `.pearde/wiki/pending/260901-8a64.md` (priority
med) — distinct from `260831-17e4.md` named in the brief as already pending
from an earlier pass. Neither gap is a question of this pass's own; both
are noted here for the record, not acted on.

git diff --stat on the footprint file, confirmed still holding only this
PRD's hunks disjoint from the sibling session's carry-down hunks in the
same file:

```
resources/board/specs.py | 393 +++++++++++++++++++++++++++++++++--------------
1 file changed, 277 insertions(+), 116 deletions(-)
```


---

## Implementer pass — DONE (impl-33, as engineer)

**VERDICT: DONE** · spec01 5/5 · spec02 4/4 · 9 of 9 boxes ticked, each
against output quoted below.

### What this pass changed

The mechanism the two specs record was already in the tree. This pass ran
every box against the shipped file rather than the probe's development copy,
and closed the three gaps that reading exposed.

1. **Dead code removed from the walker's own section.** The body of
   `_statement_outcomes` stood a second time inside `_pipe_member_can_fail`,
   after its `return` — unreachable, referencing an `elements` name that does
   not exist there, and a straight copy of the live function below it. Also
   gone: a doubled two-line comment above `ALWAYS0`, a second `import re` at
   the head of the section (line 43 already has it), and an unused
   `stripped = line.strip()` in `_logical_lines`. No behaviour moved: the
   classification is byte-identical, proven below.

2. **The refusal message now names the shape, which is spec02's second box.**
   It read `every fallible command is guarded and its last statement only
   ends 0` — true, and useless to the worker who has to change something. The
   element tuple carries the command text now (a fifth field; `_snip` cuts it
   to 60 characters), and two new helpers, `_snip` and `_guard_shapes`, build
   the sentence. Before and after, on the same block:

   ```
   before: verify block 1 cannot fail — every fallible command is guarded and
           its last statement only ends 0 — nothing in it can make the block red
   after:  verify block 1 cannot fail — its last statement `echo done` only
           ends 0, and what could have gone red sits behind the always-0
           fallback `|| true` — nothing in it can make the block red
   ```

   Three shapes are named and quoted, at most three per message: the `!`
   inversion, the always-0 fallback `|| <cmd>`, the always-0 tail `&& <cmd>`.
   A block with no guard at all says so instead — `its last statement `true`
   only ends 0 and no command in it can exit non-zero at all`.

3. **Both `## Verify and Proof` blocks rewritten** — see the warnings section
   below.

`_statement_outcomes`'s tuple unpack moved from four fields to five in the
same edit; nothing outside this file reads it (`grep` over the repo: the only
references to `_cannot_fail_why` are its own definition and the `check_spec`
call site at line 529 — `block_cannot_fail`, the first-generation name still
at HEAD, is referenced nowhere and is gone).

### The two `specced` warnings — both were real, both fixed

```
warn: spec01.md:41: the verify block names no path under the footprint
warn: spec02.md:36: the verify block names no path under the footprint
```

Real. Each block held one line — `bash .pearde/prds/<slug>/probe/verify.sh` —
and the footprint is `resources/board/specs.py`. The smell the warning names
was under it, not just in the text: the probe harness runs its *case suite*
against `probe/analyzer.py`, the development copy, and only its differential
and its gate fixture against the shipped file. So spec01's box 2 ("the four
mechanical shapes are all refused") was, as written, a claim about a file
that is not the footprint.

Both blocks now run the harness **and then** load
`resources/board/specs.py` by path and check it directly:

- spec01's block asserts six dead shapes refused and five live shapes
  accepted, by the shipped `_cannot_fail_why`.
- spec02's block builds a two-block spec in a `tempfile.mkdtemp()` directory,
  calls the shipped `check_spec`, and asserts five things: exactly one
  `cannot fail` message, it starts `verify block 2` (the guarded block, not
  the live one), it quotes `|| true`, the fixture directory is unchanged
  after the call, and the same spec is accepted once the guarded block's last
  statement is replaced by a live one.

Both blocks end on a fallible `python3` heredoc, so both can still exit
non-zero — checked by the very code they test: `_cannot_fail_why` returns
`None` for each of them.

### Boxes, with the output each was ticked on

spec01 (5/5), run as `collect` runs a block — `bash -e -o pipefail`, cwd the
code repo, block on stdin:

```
verify: 2 passed, 0 failed
spec01: 6 dead shapes refused, 5 live shapes accepted, 0 wrong
block 1 exit 0
```

- box 1 — refused with the block number: `verify block 1 cannot fail — its
  last statement `echo done` only ends 0, and what could have gone red sits
  behind the always-0 fallback `|| true` …`, and `dir after check_spec:
  ['spec01.md']`.
- box 2 — the shapes, all refused: everything guarded behind a closing
  always-0 command, a `!` inversion, a `||` fallback resetting status, a body
  in a condition, a bare `true`, a bare `:`.
- box 3 — a live block accepted: `python3 -c 'import sys; sys.exit(1)'\necho
  done` returns `None`.
- box 4 — differential against real bash, run on the **shipped** file, seed
  4242: `differential: 4000 scripts, 1081 refused, 0 false refusals`.
- box 5 — unanalysable shapes accepted: `set +e`, an `if` body, a `while`
  body, a bare fallible command. None refused.

spec02 (4/4):

```
verify: 2 passed, 0 failed
  verify block 2 cannot fail — its last statement `echo done` only ends 0,
  and what could have gone red sits behind the always-0 fallback `|| true` —
  nothing in it can make the block red
spec02: 5 checks over resources/board/specs.py, 0 wrong
block 1 exit 0
```

- box 1 — the message points at block 2, the guarded one, with block 1 live.
- box 2 — it quotes `|| true`, the guard a worker has to change.
- box 3 — end to end in a run-time fixture directory: refused, nothing
  written (`sorted(os.listdir(d))` unchanged), then accepted once the last
  statement is live. Never against a real PRD under `.pearde/prds/`.
- box 4 — the probe's gate fixture against the code as it stands now:
  `gate: cannot-fail refused, live accepted`.

### The gate

- `bash .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/
  verify.sh` — **2 passed, 0 failed** (before the edits and after).
- `bash .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/
  verify.sh` — **90/90 checks pass**, before and after, unchanged.
- `python3 resources/index.py check` — exit 0.
- `bash resources/doctor.sh` — exit 0, one `broken` row: `origin broken · 5
  derived in flight vs 4 requested`, the pre-existing one the analyst's
  passes already recorded (the counts move under the other sessions). Every
  other row `ok`; `view`, `plan`, `harnesses`, `jstests` `off` as at
  baseline.
- `python3 resources/board/specs.py specced <prd> --check --as engineer` —
  `ok · complexity 24 · footprint resources/board/specs.py`, exit 0. The two
  footprint warnings are gone; the only warnings left are `5 of 5` and `4 of
  4 boxes already ticked`, which is what a finished implementer run looks
  like.

### Findings — not fixed, not mine

- `probe/analyzer.py` is a frozen development copy of the walker and now
  diverges from the shipped file in message text. Its **classification** does
  not diverge: 4000 generated scripts, seed 99, `0 divergences` between
  `resources/board/specs.py::_cannot_fail_why` and the probe's. Left as it
  is — it is the differential's second opinion, and a second opinion that is
  edited to match stops being one.
- The probe harness's case suite runs against `analyzer.py`, not the shipped
  file. Not repaired inside the harness (three other sessions hold harness
  `verify.sh` files this round); the shipped-file coverage now lives in this
  PRD's own two verify blocks instead.
- `doctor`'s `origin broken` row is pre-existing and belongs to the board's
  own shape, not to this footprint.
- Nothing was learned outside this repository on this pass: every bash fact
  the walker leans on (the `set -e` exemption for a non-final and-or element,
  the `!`-pipeline exemption, `local` failing outside a function) was already
  established and recorded by the analyst's passes above.

### Footprint touched

- `resources/board/specs.py` — four hunks, all inside `# ── can a verify
  block fail? ─` and the verify branch of `check_spec`. The sibling session's
  workflow-carry-down work is committed at HEAD (`7531010`), so no hunk of
  this pass overlaps it: `git diff` hunk heads are `@@ -75,36 +75,34 @@`,
  `@@ -126,27 +124,82 @@`, `@@ -168,99 +221,201 @@`, `@@ -368,6 +523,10 @@` —
  none reaches the docstring, `read_specs` or `specced`.
- `specs/spec01.md`, `specs/spec02.md` — boxes ticked, verify blocks
  rewritten.
- Nothing committed, nothing stashed, nothing reverted.

```
resources/board/specs.py | 397 +++++++++++++++++++++++++++++++++--------------
1 file changed, 278 insertions(+), 119 deletions(-)
```
