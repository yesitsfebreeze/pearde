---
atomic: attempt-the-build
subject: build the contract until it works or hits something undefined
date: 2026-08-28
updated: 2026-09-02
runs: 38
---

# attempt-the-build — the attempt is the analysis

## Do

1. Build the thing the contract asks for. Whatever the build passes through
   needs no question; whatever it hits is the finding.
2. Keep NEW code under `prds/<prd>/probe/` — never at the repo root, where it
   would redden the map check for every later PRD — so a file the PRD's
   footprint places under `resources/` is built under `probe/` and moved by
   its spec. A change that is an **edit to an existing footprint file** cannot
   be staged this way: a guard, a rename or a branch has no meaning outside
   the function it lives in, so it is built in place, in the footprint file
   itself, and the spec records what already stands rather than what to move.
   Say which it was in the report.
3. Build every fixture in a directory made at run time — `D=$(mktemp -d)`,
   removed at exit. A fixture `prd.md` left anywhere under `prds/` becomes a
   real PRD the scan picks up.
4. Write `prds/<prd>/probe/verify.sh` as you go: one line per assertion, a
   count at the end. The count is printed, never asserted by a spec.
5. Stop at the first fork the build cannot pick and cannot build around, and
   record what the build was doing when it hit it. Which verdict that becomes
   is @references/parts/workers.md.

## Done when

- `bash prds/<prd>/probe/verify.sh` prints a count, and the count is
  quoted — **unless the contract's verification is the repo's own gate**
  (a `justfile` recipe, a `scripts/` tripwire, `cargo test`), in which case
  that gate's command line and exit code are quoted instead and the probe
  directory carries only what the build needed to reproduce a finding.
  A probe `verify.sh` that merely re-calls the repo gate is a second copy
  of it that can drift.
- `ls <board>/prds` against the pre-run listing shows no `prds/<slug>/` you did not make — a hand-walked sweep over the board is refused by the guard in a wired repo, and the listing answers the same question. `git status --short` is silent here where the board is gitignored.
- the probe is under `<board>/prds/<prd>/probe/` and nothing this run wrote
  is at the repo root — check with `ls`, not `git status`, where the board
  is gitignored.

## Fails when

| seen | means | do |
|------|-------|----|
| the route's steps 3 and 5 have nothing to do because the specs already exist and the build is already in the tree | this is the route's **second** pass on the PRD — the analyst probed and specced, and an implementer has now been dispatched on the same route | run steps 1, 2 and 4 only, say in the report which steps were not entered and why, and claim no flip: every red-to-green on this tree was earned by the pass that built it. Ticking boxes against a green tree is the implementer's whole job here, and a route that forces a rebuild to have something to do would discard a working build |
| a fixture board built under `mktemp -d` shows up in `serve.py status` after the run, on a path that no longer exists | the probe ran a command whose repair registers whatever board it is handed — `doctor --fix` is one — and the live daemon's registry outlives the temp dir | never run a `--fix`-shaped command against a fixture while a real service is up; point it at a dead port (`PEARDE_PORT=1`) so the repair cannot connect, and check `serve.py status` at the end. `serve.py forget <name>` removes one already landed |
| a check stands a machine-wide guard down (`PEARDE_REAP_GRACE_S=0`, a disabled cap, a bypassed lock) to reach the behaviour it is measuring | the guard is the only thing keeping the action off a neighbouring session's processes, and the check has just removed it machine-wide | scope the action to what the check itself started — a `--pid`, a port, a path filter — and make the narrowing flag **refuse** an unreadable value rather than falling back to "everything". Assert the guard both ways: kept inside it, and expiring outside it, or a widened default keeps every box green while the guard never fires |
| the probe passes standalone and fails only when the runner that is its own subject runs it | the probe is itself an instance of the population it measures, and inherits the environment that runner sets — a guard variable, a cwd, a port — so it measures the guard instead of the behaviour | clear it explicitly for every fixture invocation (`env -u <VAR>`), keep one assertion that sets it deliberately, and run the harness both ways before quoting a count |
| every fixture lands on one board, and assertions pass or fail in the wrong sections | the fixture-maker is called as `B=$(mktemp_helper)`, and command substitution runs it in a **subshell** — a counter or path it keeps never reaches the caller, so every call returns the same board | make each fixture with its own `mktemp -d` inside the helper and echo that; never keep state in a helper you call through `$(…)` |
| a patch's anchor text no longer matches a file you read in step 1 | another session moved the file since | re-read it, merge into its current shape, keep your hunk disjoint from theirs, and name the collision in the report |
| the fixture's own git repo shows `?? err` or another scratch file after a refusal | the harness wrote its scratch inside the fixture, so "the diff is empty" cannot pass | keep scratch in a second `mktemp -d` outside the fixture repo |
| `verify.sh` prints a heading and hangs | a line in the harness reads stdin — a bare `cat` or `read` with no file | run it with `</dev/null`, then fix the line |
| a rule reading mtimes fires on a fresh copy of the example | `plan.py example` copies stat too, so the copy carries the example's own timestamps | `find <copy> -type f -exec touch {} +` before the byte-identity check; set them back only in the fixture that tests age |
| a page driver reads a Lit element right after `pearde.apply` and sees the old render | Lit renders on a microtask | `await el.updateComplete` before reading the DOM; and run any `pearde.replace` test last, since it removes the page's own element |
| `touch: out of range or illegal time specification` on **darwin** | `touch -d '<n> minutes ago'` is GNU coreutils; darwin's `touch` takes `-t <YYYYMMDDhhmm.SS>` and `date -v` for arithmetic — a GNU box never sees this row | portable on both: `python3 -c 'import os,time,sys; t=time.time()-120; os.utime(sys.argv[1],(t,t))' <file>`; darwin-only: `touch -t "$(date -v-2M +%Y%m%d%H%M.%S)" <file>` |
| a fixture meant to hold a foreign hunk and a kept one shows a single hunk, and the file goes whole | the two edits touch adjacent lines, and `-U0` merges adjacent changes into one hunk whose body is in neither baseline | leave one untouched line between the foreign edit and the kept one; the merge itself is a finding for the PRD that classifies hunks |
| `?? prds/<slug>/` appears mid-run and its `prd.md` is the untouched template | a harness in another PRD's probe calls a transition with no `--board` from a cwd inside the repo, and your edit turned its refusal into a write on the real board | before the first edit, grep every harness for the command with no `--board`; run those from a cwd with no `prds/` above; remove the untracked template PRD, name the row it left in `.transitions.jsonl`, and hand the harness's owner the `--board` line |
| a `sed -n 's/^\(a\|b\)$/\1/p'` extractor captures nothing, or captures `0`, on **darwin** | BSD sed has no `\|` alternation in a basic regex; GNU sed does | `grep -E '^(a|b)'` then `sed 's/^  //'` — portable on both |
| a fixture board made by `cp -R resources/board/example <d>/prds` shows `prds/prds`, and doctor resolves to a board one level too deep | `example` is a repo root, not a board — it holds `prds/` and a README | copy `resources/board/example/prds` to `<d>/prds`; doctor from `<d>` hides the nesting, a command run from inside the board does not |
| an assertion on a path printed by a Python command fails on **darwin** with `/private/var/…` against `/var/…` | `os.getcwd()` returns the real path; `mktemp -d` and bash's `$PWD` keep the symlink | compare against `$(cd "$D" && pwd -P)` — portable on both. **This is an equality hazard only. A `grep -F` needle is unaffected: `/private/var/X` contains `/var/X` as a substring, so a `mktemp`-spelled needle matches a realpath-spelled hit and "repairing" it adds a false claim to the file. Measure before you widen a needle on this ground.** |
| `ModuleNotFoundError: No module named 'memos'` from a copied `collect.py` or `plan.py` | the board scripts import from `resources/` beside `board/`, and the copy took `resources/board/*.py` alone | copy `resources/*.py` into `<scratch>/resources/` and `resources/board/*.py` into `<scratch>/resources/board/` — the layout, not just the files |
| a `lacks` needle for a PRD name fails on a `scan` band that does not list it | another row's `after <name>` or `needs <name>` bit carries the name | match the row token `· <name> ·`, never the bare name |
| a `--dry` run refuses on a gate the real run passes | the dry branch re-ran a gate that reads the file the real run writes first — `answer`'s gate saw the question still open because the answer is never on disk in a dry run | compute the gate's input on the scan dict in memory (the answer appended to `prd["body"]`, the state moved on `prd["fm"]`) and print the line off that dict; never re-enter `transition()` for a dry run of a two-step write |
| every assertion in a harness passes, or every one fails, regardless of the command's output | the helper is `ok "<label>" "<expr>"` with the expr evaluated inside `ok`, so `$2`/`$3` in the expr name `ok`'s own arguments, not the caller's values | evaluate the test in the caller (`eq() { [ "$2" = "$3" ]; ok "$1" $? "…"; }`) and hand `ok` only a label and an exit code |
| the brief says the probe's code is uncommitted, and `git status --short` is clean | a sibling session committed the whole tree, your hunks with it | `git log -1 -- <footprint path>` and read the file itself before concluding anything is missing; if the behaviour is present, the work stands — record the commit that took it, and read every spec's "what already stands" against the **file**, never against a diff |
| a box asks you to prove a check *can* fail, and the file to mutate is an uncommitted footprint file | the restore cannot be `git checkout` — the committed text is not the text you must return to, and a checkout would silently discard the build | `cp <file> <scratch>/<name>.bak` into a scratch dir **outside** the repo, mutate, run, `cp` back, and prove the restore with `cmp <scratch>/<name>.bak <file>`. Quote the failing count, the restored count, and the `cmp`. Make the mutation unreachable at run time (`if false; then … fi`) when the check reads text rather than behaviour — a reachable one measures the mutation instead of the check |
| a line appended with `>>` to a harness lands concatenated onto its last line | the harness ends on its exit-carrying check with no trailing newline — the shape every harness on this board ends in | `printf '\n%s\n' '<line>' >> <file>`, or check with `[ -n "$(tail -c1 <file>)" ]` first. An anchored matcher (`^…`) will not see a concatenated offender, so a can-it-fail box run this way reads green on a check that did not fire |
| your probe invokes another PRD's harness and its result is decided by that harness's own defect — a hard-coded port, a leaked process, a shared fixture | you are measuring the neighbour's file, and the box it backs is green or red by scheduling | do not edit that file. Make your own probe stand down when the condition holds (`PEARDE_HARNESSES` set, the port already bound) and say in the check's own text why, then report the neighbour's defect as a finding for the orchestrator to route. Demonstrate the box under the racing condition; never assert it |
| the brief names `probe/run.sh` and only `probe/verify.sh` is on disk | a spec in this PRD's own set contracted the rename, and an earlier pass did it | take the file that exists as the same probe, name both spellings in the report, and check the spec's box against the file rather than against the brief |
