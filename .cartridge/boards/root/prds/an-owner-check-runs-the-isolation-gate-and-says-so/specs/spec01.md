---
complexity: small
footprint:
  - ".cartridge/justfile"
  - ".cartridge/tests/integration/owner-check-isolation.test.ts"
---

# spec01 — the composition verdict joins every check, with a test that can fail

An owner's `check` fans out over one target list and never asks the composition
anything, so a fixture reaching `../<sibling>.ctg` passes every owner gate and
breaks the build later. The fix is one verdict appended to the `check` fan and
a denominator that counts the verdicts rather than the targets. The work of
this spec is not the verdict — it is the test that makes the verdict a
behaviour rather than a line in a recipe.

## The hunk is no longer uncommitted

The PRD describes the hunk as uncommitted. It is not, as of 16:17:57 today:
`5831e2a` — "Name the program ackin, advance submodules and record idle
superproject work", a twenty-six file commit by the user's own hand — swept it
into HEAD along with the ranking memos, `ASP.md`, `.claude/` settings and four
submodule bumps. That is precisely what the PRD's Coordination section asked
nobody to do, and the sweep happened between this analysis starting (`d701bac`)
and finishing. `.cartridge/justfile` is now clean in the working tree, and
`git diff d701bac HEAD -- .cartridge/justfile` is exactly the hunk.

Two consequences. The code half of this outcome is already in HEAD — attributed
to an unrelated commit message, with no test and no documentation — so this
spec's diff is the test, the comment, the wiring and the header sentence, not
the eleven lines themselves. And `@root/the-composition-s-gates-do-not-inherit-cartridge-yolo`
is no longer blocked: the dirty path it was waiting on is gone.

## What the hunk is worth

The hunk now in `.cartridge/justfile` was measured, not read. Built as a
synthetic three-cartridge composition in a temporary directory, with the real
`.cartridge/justfile`, the real `.cartridge/tools/memo-run` and the real
`check-cartridge-isolation.md`, and a stub owner gate in place of the
development routine:

| justfile | fixture | `check alpha` | summary |
|---|---|---|---|
| `d701bac`, before the hunk | `alpha.ctg/Cargo.toml` names `../beta.ctg/crate` | exit **0** | none printed |
| hunk (now HEAD) | same fixture | exit **1**, `isolation composition FAIL` | `check: 1 of 2 targets failed` |
| hunk, `${#verdicts[@]}` reverted to `${#targets[@]}` | same fixture | exit 1 | `check: 1 of 1 targets failed` beneath two verdict lines |
| hunk | no fixture | exit 0, `isolation composition pass` | none |
| hunk | same fixture, `test alpha` | exit **0**, no isolation line | none |

So the hunk does exactly what the outcome asks, the denominator change is
load-bearing in a way a single run exposes, and `test` is untouched. **The plan
keeps the hunk as written**, and adds to it only what the measurement showed
was missing. Rewriting it would cost a diff and buy nothing: the block is
eleven lines, it reuses the verdict shape of the loop above it, and for every
gate other than `check` the number of verdicts equals the number of targets, so
the denominator is unchanged everywhere else. It is also already in HEAD, so a
rewrite would now be a second unexplained change to the same recipe.

Two amendments, both to the comment rather than the code:

1. The comment claims isolation "costs about a second". Measured 4.3 s over the
   live eighteen-cartridge composition. The plan drops the number — a figure
   that depends on how many cartridges the composition holds does not belong in
   a comment — and says what makes it cheap instead: it reads sources and
   builds nothing.
2. The comment does not say why `test` is left alone, and the record needs that
   said rather than inferred. Add the reason: one gate carrying the composition
   verdict is enough, and `check` is the short one.

## The change

### `.cartridge/justfile`

- The `if [[ "$gate" == check ]]` block and the `${#verdicts[@]}` denominator
  are already in HEAD at `5831e2a` and stay exactly as they are.
- Rewrite the block's comment to remove the unmeasured cost claim and to state
  why the `test` gate does not do the same.
- Extend the file's own header comment (lines 1–4) so the sentence describing
  what every gate does also says that a `check` reports the composition's
  isolation verdict beside the owner's own.
- Wire the new suite in as a target of the `test` gate, the way `layout` and
  `lifecycle` already are: add `gates` to the `test` target list in `_fan`, and
  one dispatch line in `_one`'s `test` arm running
  `bun test "{{root}}/.cartridge/tests/integration/owner-check-isolation.test.ts"`.
  This adds a target to `just test all`; it changes no owner's `just test
  <owner>`, and nothing else in the repository asserts that target list.

### `.cartridge/tests/integration/owner-check-isolation.test.ts`

A new Bun suite in the house style of `source-layout.test.ts`: `const source =
path.resolve(import.meta.dir, '../../..')`, `Bun.spawnSync`, `mkdtempSync` with
an `rmSync` in `finally`.

It builds a synthetic composition under `os.tmpdir()` and runs the repository's
own recipe against it. The composition must be a copy, because `_fan` derives
`root` from `parent_directory(source_directory())` — pointing `just` at the
live justfile with a foreign working directory would run the live composition
instead. The copy is taken from `source` at run time, so the suite always
exercises the justfile as it stands:

    <tmp>/.cartridge/justfile                                   copy of source
    <tmp>/.cartridge/tools/memo-run                             copy, mode 0755
    <tmp>/.cartridge/memos/routine/check-cartridge-isolation.md copy
    <tmp>/.cartridge/memos/routine/cartridge-development.md     written stub
    <tmp>/cartridge.ctg/cartridge.json                          {"name":"cartridge"}
    <tmp>/cartridge.ctg/.cartridge/init.lua                     one comment line
    <tmp>/alpha.ctg/cartridge.json                              {"name":"alpha"}
    <tmp>/beta.ctg/cartridge.json                               {"name":"beta"}

The stub development memo carries a single `just` block whose `check` and
`test` recipes echo and exit 0. Only the owner's own gate is stubbed, and it is
the one thing under no test here; the fan-out, the composition check and the
fixture are all real. The fixture is one file,
`<tmp>/alpha.ctg/Cargo.toml`, containing `beta = { path = "../beta.ctg/crate" }`
— the exact shape the isolation rule forbids.

Every gate runs through a helper that spawns
`just --justfile <tmp>/.cartridge/justfile --working-directory <tmp> …` with
`CARTRIDGE_YOLO` removed from the inherited environment, so the suite means one
thing in any terminal on this machine.

Three gate runs, memoised so the failing run serves two tests:

1. **`an owner check reports the composition isolation verdict`** — clean
   composition, `check alpha`: exit 0, stdout matches
   `/^check\s+alpha\s+pass$/m` and `/^isolation\s+composition\s+pass$/m`.
2. **`a fixture reaching a sibling makes an owner check exit non-zero`** —
   fixture present, `check alpha`: exit code is not 0, and stdout matches
   `/^isolation\s+composition\s+FAIL$/m`. This is the box the PRD says cannot be
   proved by reading the recipe, and it is not: the fixture is written, the
   gate is run, the exit code is read.
3. **`the failure summary counts every verdict it printed`** — same run. Count
   the stdout lines matching `/^\S+\s+\S+\s+(pass|FAIL)$/`; parse `M` out of the
   stderr line `check: N of M targets failed`. Assert `M` equals that count,
   and assert the count is 2 while exactly one target was named. Under
   `${#targets[@]}` the same run prints `1 of 1` beneath two verdict lines, so
   this assertion is what holds the denominator in place.
4. **`the test gate does not run the composition isolation check`** — fixture
   present, `test alpha`: exit 0, and no stdout line begins with `isolation`.
   This is the PRD's fourth box turned into an assertion: the divergence
   between `check` and `test` is deliberate, and it is now recorded by
   something that fails if it drifts.

A single synthetic `check alpha` was measured at 1–5 s on a quiet machine, so
three runs leave the whole suite well under ten seconds. Give each test a 90 s
timeout anyway and keep the run count at three: the same gate was observed at
16.6 s while another session was rebuilding the composition, and the Verify
block's ceiling is 120 s.

## What this spec does not deliver

The PRD's fifth box asks that `README.md` and the development routine say what
an owner check now covers. Neither path is in the footprint, and **this
repository has no `README.md` at its root** — the gates are described in the
root `justfile` header, in `.cartridge/memos/routine/cartridge-development.md`,
in `ASP.md:176-178` and in `PROMPT.md:70`. The in-footprint part of that box is
delivered here: the `.cartridge/justfile` header sentence and the comment
inside `_fan`. The rest needs a footprint decision by the coordinator, and
`cartridge-development.md` is already the footprint of
`@root/the-composition-s-gates-do-not-inherit-cartridge-yolo`, so it cannot be
taken without ordering the two rows first.

## Order against the sibling row

`@root/the-composition-s-gates-do-not-inherit-cartridge-yolo` (priority 85)
holds `.cartridge/justfile` and `.cartridge/memos/routine/cartridge-development.md`;
this row (priority 60) holds `.cartridge/justfile`. The ordering question the
PRD raised has resolved itself: that row was holding its collect because this
hunk was dirty in the shared file, and `5831e2a` has committed it, so the file
is clean and either row can now collect. They still share the file, so they
should not be in flight at the same moment; nothing here depends on that row's
outcome, because the composition check is a Bun script that builds nothing and
`CARTRIDGE_YOLO` cannot change its verdict either way.

## Acceptance

- [ ] `just check <target>` prints an `isolation composition` verdict line
      beside the owner's own verdict, for a named target and for `all`, and
      still exits 0 on a clean composition.
- [ ] A fixture reaching `../<sibling>.ctg` makes `just check <target>` exit
      non-zero, proved by a test that writes the fixture, runs the gate and
      reads the exit code.
- [ ] The failure summary's `M` equals the number of verdict lines printed
      above it, asserted on a run where one target was named and two verdicts
      were printed.
- [ ] `just test <owner>` runs no composition check and exits 0 with that same
      fixture in place; the divergence is stated in the recipe's comment.
- [ ] The suite is reachable as `just test gates`, and the file's header
      comment says a check now reports the composition's isolation verdict.

## Verify and Proof

<!--
Engine facts honoured here: every block is `sh -eu -c`, 120 s, run first in the
lane and again in `repo`, with paths relative to the repository root and no
`cd`. No environment is injected, so nothing uses `${VAR:?}`. No block writes
inside the footprint. No cargo runs, so no `CARGO_TARGET_DIR` is needed. The
negated checks use `if …; then exit 1; fi`, never `!` and never `&&`, both of
which are inert under `set -e`.
-->

```sh
# The live composition is clean, so appending its verdict to every check does
# not turn every owner gate red.
just isolation

# The suite is reachable from the composition's own test gate.
just test gates
```

```test
run: bun test .cartridge/tests/integration/owner-check-isolation.test.ts --reporter=junit --reporter-outfile="$PRD_TEST_REPORT"
pass: an owner check reports the composition isolation verdict
pass: a fixture reaching a sibling makes an owner check exit non-zero
pass: the failure summary counts every verdict it printed
pass: the test gate does not run the composition isolation check
```

```sh
# The suite must be observing the composition check, not merely the machinery
# around it. Rebuild the smallest tree the suite reads from, give it a
# composition check that can never report anything, and require the suite to
# fail there. A suite that still passes is not measuring what it claims.
work="${TMPDIR:-/tmp}/owner-check-isolation-mutant"
rm -rf "$work"
mkdir -p "$work/.cartridge/tests/integration" "$work/.cartridge/tools" "$work/.cartridge/memos/routine"
cp .cartridge/justfile "$work/.cartridge/justfile"
cp .cartridge/tests/integration/owner-check-isolation.test.ts "$work/.cartridge/tests/integration/"
cp .cartridge/tools/memo-run "$work/.cartridge/tools/memo-run"
chmod +x "$work/.cartridge/tools/memo-run"

fence=$(printf '\140\140\140')
printf '%s\n' '---' 'kind: routine' \
    'description: a composition check that can never report a reference' '---' \
    "${fence}just" 'check:' '    @echo "composition check disabled"' "$fence" \
    > "$work/.cartridge/memos/routine/check-cartridge-isolation.md"

if bun test "$work/.cartridge/tests/integration/owner-check-isolation.test.ts" > "$work/mutant.log" 2>&1; then
    echo 'the suite passes against a composition check that reports nothing, so its verdict does not come from the composition' >&2
    exit 1
fi
echo 'mutant killed'
```
