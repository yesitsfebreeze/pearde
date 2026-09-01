# report — seven-closed-probes-drifted-red · analyst · as engineer

Verdict: **REFINE** — the build diagnosed every red probe to its root by
reproduction, and the fixes decompose into four contracts no one sitting can
close honestly as one: the seven probes did not drift for one reason.

Workflow followed: `probe-then-spec` (its `## Use when` fits: an open PRD from
contract to specs written from a build). `read-the-contract`,
`capture-the-harness-baseline`, `attempt-the-build` and `write-the-specs`
were the steps the run took. Knowledge queried first — gap auto-enqueued at
`.pearde/wiki/pending/260901-a2ed.md` (priority med); noted, not mine to ask.

## The contract as found

The PRD body is the template only; the title is the contract. Doctor's
`--harnesses` sweep at 10:23 read `5 of 43 green · 7 failed`. I ran all 45
harnesses sequentially twice (runner left uncommitted at `probe/run-all.sh`)
and re-ran every red one alone. Nine are red on the current working tree; one
of doctor's seven was transient; three new reds appeared or flipped as the
tree moved under me (other sessions landed work mid-run). Every root cause
was reproduced in a `mktemp` fixture, not inferred.

## The seven, root causes

1. **`an-unknown-flag-refuses` · 3 fails** — reproduced: any command that
   calls `scan` persists `.pearde/.state/parse-cache.json` even when it then
   refuses or runs `--dry` (plan.py:374 saves whenever a parse was a miss).
   Fixture boards are hand-rolled git repos with no `.gitignore` naming
   `.pearde/.state/`, so the "a refusal writes nothing" checks see
   `?? .pearde/.state/`. The cache PRD calls the cache machine-local
   "exactly like `.pearde/.state/plan.json`", and the real board's
   `.gitignore` does ignore it — the product kept its contract; the fixtures
   predate the cache. Re-aim `clean()`, not a product change. (Alternative —
   save only on a successful non-dry command — is the upgrade path if a
   person's board ever tracks `.state/`.)
2. **`the-tool-keeps-its-word/one-predicate-for-dispatchable` · 2 fails** —
   same root cause, same re-aim.
3. **`the-board-runs-itself/transitions-are-commands` · 10 fails** — one fail
   is the cache (see 1); eight are the drill gate
   (`two-questions-start-a-drill`, committed 07f0e0f, ~22 h after the probe's
   last re-aim): the fixture board holds four unanswered questions, so
   `claim next impl-1` refuses with `asking 4 — drill first`. The designed
   escape exists — the gate reads `.pearde/.state/round.md`'s `## Asked` by
   title — the fixture predates it. Reproduced: a round file listing the four
   titles turns `claim` green. The tenth fail (the stray check) follows.
4. **`the-gate-runs-the-harnesses` · 1 fail** — census J counts 44 of 45
   harnesses ending on an exit-code-carrying check: the graph-probe analyst's
   new harness (pass one, uncommitted) ends on `[ "$FAIL" = 0 ]`, which the
   census regex does not read; the library's own shape
   (`[ "$FAIL" = 0 ] || exit 1`, as workflow-skill ends) closes it. One line.
5. **`the-view-row-names-a-variable-that-exists` · 4 fails** — root cause in
   `resources/doctor.sh`, not the probe: `the-vault-link-opens-the-board`
   (c02546f, 08:23) added the vault row reading `$HOME` bare (doctor.sh:334),
   42 minutes *after* the view-row probe (44e9a11, 07:41). The probe runs
   doctor under `env -i` to prove no unset variable kills a row; under
   `set -u` the vault row now aborts the whole report (`HOME: unbound
   variable`) before the view row prints. Reproduced: `env -i
   PEARDE_PORT=9999 bash doctor.sh <board>` dies at line 334. The probe's
   fixture is right; doctor gained an unprotected read. A two-line guard
   (`${HOME:-}` with an empty-register fallback) closes it — and is what
   quickstart's green needs too (see 7).
6. **`one-page-that-says-whats-up` · 4 fails** — two distinct drifts.
   (a) The probe asserts the report carries `## In work` and `## Planned`.
   references/report.md and templates/report.md still mandate the four parts,
   and the committed what's-up section of view.js (`reportParts()`) renders
   exactly those headings — but the live `.pearde/report.md` was rewritten as
   pure prose by the 53/53 round (4771654) and holds no headings. The file
   drifted from three standing contracts, not the reverse. (b) The two
   stage-height checks pin `height:min(74vh,720px)`; uncommitted view work in
   the tree replaces it with `calc(100vh - 260px)` plus a comment retiring the
   one-screen constraint deliberately. That work is claimed by no PRD I can
   find (finding 1 below).
7. **`the-board-runs-itself/readme-in-three-rings` · 4 fails, cascading into
   `workflow-skill` · 1** — (a) the D section greps `| step | command`; the
   pearde-next commit (9a7ce2c, 11:15) re-aimed loop.md to the two-column
   `| step | the orchestrator decides |`, and the README's mirror edit sits in
   the tree uncommitted — the awk anchor matches nothing, 0 rows. Re-aim two
   awk anchors. (b) `H quickstart.sh exits 0` — a fresh `init --example`
   board fails doctor three ways: `memos broken` (init strips the example's
   memos/README.md at init.py:148 and never regenerates the generated kind
   index), `knowledge broken` (init never runs knowledge board/relink — the
   loop that does lives in cmd_upgrade only, init.py:683), and `vault broken`
   (the new register row on a machine where Obsidian runs). This is the
   defect the graph-probe analyst already flagged as its own contract; it is
   what keeps quickstart from ever closing green, and it is too big to fold
   into a re-aim sitting.
8. **`workflows-on-the-board/workflow-improve` · 1 fail** — the collect-reads
   implementer (claimed 11:15, in flight) is deliberately replacing the
   workers.md verdict table with `collect --report` prose; the probe pins the
   table row. Their spec01 footprint claims workers.md and its verify block
   already gates brief-is-printed. Their landing closes this; a re-aim now
   would race them. Not mine.
9. Greened during the run by other workers' landings (verified):
   `workflows-on-the-board/workflow-attach` (was 4 fails on loop.md literals;
   47/47 after pearde-next committed the rewrite),
   `the-graph-lands-inside-the-board` (10/10 on the graph-probe analyst's
   uncommitted re-aim; their PRD carries it),
   `nothing-left-open/the-line-tells-the-truth` (85/85 alone; its doctor
   failure was E14 — a sibling harness's `collect` held its
   `/tmp/pearde-index-*` scratch index concurrently in the parallel sweep.
   Transient, but a real flake of doctor's unbounded-parallel design).

## Split

| child | contract | needs |
|---|---|---|
| the-fixtures-meet-the-tool | every harness red only because its fixture predates the tool runs green: the machine-local parse-cache write and the drill gate are paid in the fixtures (`clean()` filters `.pearde/.state/`, the transitions fixture writes the round file's `## Asked`), and the graph-probe harness ends on a check that carries its exit code — no file under resources/ changes | — |
| the-doctor-completes-without-a-home | doctor.sh finishes every row when the shell holds no HOME — the vault row's register read is guarded and nothing aborts — and the view-row probe reads green end to end | the-fixtures-meet-the-tool |
| the-page-and-the-report-agree | the live report is rewritten into the four-part shape the reference, the template and the committed what's-up renderer all name, and one-page's two stage-height checks pin the retired-constraint rule the tree now carries | — |
| init-seeds-a-board-doctor-calls-green | a fresh `init --example` board passes doctor: the memo kind-index is regenerated after the copy, the knowledge graph is planted the way upgrade does it, and quickstart proves it running doctor under a HOME that holds no Obsidian config | the-doctor-completes-without-a-home |

Not split off: `workflow-improve`'s one literal — owned, in flight, by the
collect-reads implementer whose own spec verify block gates it.

## Findings (defects outside this contract — not fixed here)

1. **Unowned uncommitted view work.** `resources/board/view.css` (+40: the
   stage-height change and a full K-search overlay) and `view.js` (+138) sit
   in the tree named by no PRD, no report, no round-file line; they rode the
   10:48 stash cycle. Whoever lands them owns the stage re-aim in child
   three. The orchestrator should claim or revert them explicitly.
2. **A collect can commit a sibling's pass-one code inside a shared file**:
   the pearde-next commit (9a7ce2c) carried the whole parse-cache
   implementation (scan-parse PRD, only claimed 11:15:40) inside its +271
   plan.py — the footprint gate read `resources/board/plan.py`, so nothing
   caught it. A rule that a collect commits only what its specs name, even
   inside a shared file, is the fix.
3. **Parallel-sweep flake**: harnesses that run `collect` share the
   `/tmp/pearde-index-*` prefix (collect.py:382); two running concurrently in
   doctor's sweep can fail each other's "no scratch left behind" checks. A
   per-run suffix is the fix; no harness owns it today.
4. **doctor.sh:743** now reads `bash <board>/<path above>` — a one-line edit
   by the graph-probe analyst, uncommitted, outside their footprint. Collect
   it with whoever owns doctor.sh next (child two).
5. **My incident, disclosed**: at 10:35 my harness-runner — written with a
   relative `cd` — executed `git add -A && git commit -qm w` in the real repo
   after the shell's cwd reset. Caught within one command; reverted with
   `git reset bbd707d` (mixed — working tree untouched) and verified against
   this session's opening `git status`, byte-identical. Commit e71bfc5
   existed for under a minute, was never pushed, and the reflog records it.
   Rule for any successor: fixture scripts take absolute paths and assert
   `$PWD` before any git write.

## Numbers for the orchestrator

Nine harnesses red on the working tree at 12:00 (seven at doctor's 10:23
sweep); four children above; workflow `probe-then-spec`, library file, no
route owed. Probe code left uncommitted in the tree:
`probe/run-all.sh`. Complexity and blast-radius are per child, at each
child's spec time.

## Scores

Verdict REFINE — the `## Split` table above is what `pearde refine` reads. A
single-sitting spec set would need six specs summing ~48 to leave all nine
green — over both limits — and the four contracts have different owners,
footprints and risk, so the split is the honest shape.
