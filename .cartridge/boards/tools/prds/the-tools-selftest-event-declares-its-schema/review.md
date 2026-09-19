# @tools/the-tools-selftest-event-declares-its-schema review history

Plan: `@tools/the-tools-selftest-event-declares-its-schema`,
`prd.ctg/.cartridge/boards/tools/prds/the-tools-selftest-event-declares-its-schema/prd.md`.
Scope: one observable outcome — the `tools.selftest` event declares a schema that
matches what it accepts, and the host refuses a call against that declaration.
Executable leaf, one spec, one file in the footprint.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Presented revision: `tools.ctg` at `024f5dd37e7cff0f940a4e5e1858c362c8959867`,
working tree clean. Planning records under `prd.ctg` are dirty but neither the
PRD nor the spec is modified relative to what is digested below.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-tools-selftest-event-declares-its-schema/prd.md` — SHA-256 `7acf1741e45ed14558f012f0bb68dcee888f88c1fe1053c7ea678cc06a996aec` |
| Specs | `specs/spec01.md` — SHA-256 `7781d11144bbb6544c8a60dfe670c8ecf24635b561da814c3969ffae0730618e` |
| Material contracts/dependencies | `tools.ctg/cartridge.json` SHA-256 `84e3eb5080bbf92aa7006ac574f71b98b27aa6a01b921e9d08a59e19bd457169`; `cartridge.ctg` at `ab2383a8223a096509b24bf429f3023bfd80024d` (`Ctx::validate`, `run_contracts`, `cli/args.rs`); `.cartridge/memos/routine/audit-cartridges.md` (the `!event.schema` rule) |

### Independent verification of the four load-bearing claims

All four hold. Each was read in the source, not taken from the analyst report.

1. **Stale PRD evidence — confirmed.** `git show 8d0dbe6 -- cartridge.json` in
   `tools.ctg` adds `"schema": {}` to the `tools.selftest` event; the line is
   `tools.ctg/cartridge.json:49` today. The PRD's quoted audit finding
   (`prd.md:26`) predates that commit and no longer reproduces.
2. **The audit rule is vacuous against `{}` — confirmed.**
   `.cartridge/memos/routine/audit-cartridges.md:118` reads
   `if (!event.schema) hard.push(\`event ${name} declares no schema\`);`. `{}` is
   truthy in JS, so PRD acceptance (c) is already satisfied by a schema that
   satisfies neither (a) nor (b). The spec is right to reframe the work as
   (a) and (b).
3. **The host validates before the handler runs — confirmed.**
   `cartridge.ctg/src/transport/cartridge.rs:239-278` is `Ctx::validate`; it
   returns `` `<name>` payload rejected by its schema: … ``, and returns `Ok(())`
   early when the declaration carries no schema. `src/host/mod.rs:811`
   (`self.ctx.validate(name, data).map_err(Error::Argument)?` inside `sender`)
   runs on the sending side before a listener is chosen;
   `src/transport/cartridge.rs:973` runs it again on the receiving node ahead of
   the Lua listener. Acceptance (b) is therefore reachable with no host change.
4. **`null` is forced, and the handler reads nothing — confirmed.**
   `cartridge.ctg/src/host/run.rs:173` sends every `contracts` key as
   `serde_json::Value::Null` through `send_to`, which routes through the
   validation above, so a declaration refusing `null` would break
   `cartridge verify tools`. The handler ignores its payload at all three
   levels: `tools.ctg/init.lua:3` (`function() return tools.selftest() end`),
   `tools.ctg/src/lib.rs:15` (`fn selftest(lua: &Lua, _: LuaValue)`),
   `tools.ctg/src/service.rs:335` (`pub fn selftest() -> Result<…>`, no argument).

Two further checks the reviewer added. `cartridge.ctg/src/host/socket.rs`
derives the socket from `base()/tag(descriptor)[..12]/host.sock`, so a probe
host under `$TMPDIR` cannot collide with the shared project daemon — the block
is safe to run on this machine. And `grep -rn "tools\.selftest"` across the
superproject finds no second declarer and no sender other than `run_contracts`,
so the narrowing the spec proposes breaks no existing caller.

### The Verify block, measured

Extracted verbatim from `spec01.md:120-165` and executed under `sh -eu -c` with
no injected environment (`CARTRIDGE_BIN` unset, `cartridge` taken from PATH).

| Run | cwd | Observed |
| --- | --- | --- |
| current tree (`schema: {}`) | `/Users/feb/dev/cartridge/tools.ctg` | **exit 1** in 2 s — `the declaration let {"unread":1} reach the listener; …` |
| fixed: `anyOf` of `null` and a closed object | scratch copy of the same manifest | **exit 0** — `tools.selftest: the declaration accepts an empty payload and turns back one that carries anything` |
| defeat attempt: same `anyOf` plus `{"type":"number"}` and `{"type":"boolean"}` | scratch copy | **exit 0** — the gate passes a declaration that admits `42` and `true` |

The block is clean on the static hazards: no `${VAR:?}`, no `!` negation, no
`a && b` guard, `${TMPDIR:-/tmp}` and `${CARTRIDGE_BIN:-cartridge}` both
defaulted, no cargo and so no `CARGO_TARGET_DIR` needed, nothing written inside
the footprint, and 2 s against a 120 s limit. It fails closed: the accepting
loop runs first, so a missing binary or a dead host fails the block rather than
letting the refusing loop pass on silence. Its failure messages name the
property and never the JSON to paste.

The stub entry is a faithful stand-in, not a substitute for the thing under
test: the block copies the **real** manifest (`cp "$manifest" …`) and replaces
only `init.lua`, and validation happens at `mod.rs:811` before any listener is
chosen, so the listener's identity cannot affect the property. Discrimination
by cwd was confirmed empirically — run from `tools.ctg` it read that manifest,
run from a scratch copy it read that one — so pass 1 will read the lane's file
and pass 2 the live one.

Probe hosts were all stopped: `ps` showed no surviving `cartridge` process for
the probe after the failing run. The scratch **directory** was not.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Correctly detects that the PRD's evidence is a day stale and that acceptance (c) is already met vacuously, then reframes the work as (a)+(b) — one file, one edit. Correctly refuses to widen to the four sibling contract events with the same empty schema. −2 for F3: the stated value rests partly on a `{}`-sending caller that does not exist in this repo. |
| Ownership and reuse | 20 | Footprint is exactly `tools.ctg/cartridge.json`. Establishes that no host change is needed by citing the existing validation path rather than proposing one. Reuses the dialect of the sibling `tools` event (`cartridge.json:12-38`). Verified that `README.md:17` and `.cartridge/help.md:9` already say "no arguments", so leaving them is correct under the README-currency memo, not an omission. |
| Dependencies and implementable slices | 18 | No prerequisites, no cross-cartridge edit, one coherent slice. Correctly identifies the one binding constraint (`null` from `run_contracts`) that a naive strict schema would break. −2 for F5: step 2 is conditional, unobservable and ungated. |
| Observable acceptance and baseline evidence | 15 | The gate is behavioural, executes real refused calls, discriminates between the unfixed and fixed trees as measured above, and names properties rather than tokens. −5 for F2: it was defeated on the first attempt — a schema admitting numbers and booleans passes it while violating the spec's own step 1 ("no number") and its own acceptance (b) ("a call carrying anything … is refused"). This is not the gate-design ceiling the method describes; the fix is one line. |
| Failure, recovery and compatibility | 14 | Every probe host is stopped on every path, verified. −4 for F1: neither `exit 1` path removes the scratch directory, observed left behind after the measured failing run. −2 for F4: the change narrows a surface that today tolerates every payload, and the spec never says so or records the caller survey that makes the narrowing safe. |
| Reviewer total | 85 / 100 | Below the 90 threshold. |

Findings and concrete revisions:

- **F1 (blocking) — the block leaks its scratch directory on failure.**
  `specs/spec01.md:145` and `:156` call `finish` and `exit 1`; the only
  `rm -rf "$probe"` is at `:163`, on the success path. Observed: after the
  measured exit-1 run, `$TMPDIR/tools-selftest-schema-probe` was still present
  with both subdirectories. The path is a fixed shared name and this machine
  runs five live sessions, so two concurrent collections would also race —
  one's `rm -rf` at `:123` against the other's mid-loop host. Recommendation:
  make the probe path unique (append `$$`) and clean up from a single place,
  e.g. `trap 'finish; rm -rf "$probe"' EXIT INT TERM` set immediately after
  `probe=` is assigned, then drop the scattered `finish` calls. Resolution:
  open.
- **F2 (blocking) — the refusal set does not cover the spec's own step 1.**
  `specs/spec01.md:150` probes only `{"unread":1}`, `"a string"` and `[1]`,
  while step 1 at `:73-77` requires "no object with a property, no string, no
  array, no number". Demonstrated: a declaration of
  `anyOf[null, closed object, number, boolean]` passes the block with exit 0,
  yet it admits `42` and `true` — payloads that carry data, which spec
  acceptance (b) at `:94-98` says must be turned back. Recommendation: add
  `'1'` and `'true'` to the loop at `:150`. Resolution: open.
- **F3 (non-blocking) — the `{}` rationale overstates the evidence.**
  `specs/spec01.md:51-54` presents `null` and `{}` as "the two empty payloads
  the system sends", and the failure message at `:144` repeats the conflation
  for both values. Verified: nothing in this repo sends `{}` to
  `tools.selftest`; `cartridge call/run/send` default their payload to `null`
  (`cartridge.ctg/src/cli/args.rs:79`, confirmed), and the `{}` convention at
  `cartridge.ctg/docs/creating-cartridges.txt:181` belongs to the `doctor`
  event in another cartridge's docs. Accepting `{}` is a defensible leniency
  and the analyst report flags it honestly as their own choice; the spec should
  say the same in its own voice rather than attribute it to the system.
  Recommendation: restate `:51-54` as a recorded decision with its reason, and
  reword the `:144` message so it does not claim the host sends `{}`.
  Resolution: open.
- **F4 (non-blocking) — the narrowing is undiscussed.** The handler ignores
  every payload today, so this change turns calls that are currently harmless
  into hard refusals. The reviewer's survey found the only sender is
  `run_contracts` with `null`, so nothing in the composition breaks — but that
  survey is the compatibility argument and it appears nowhere in the spec.
  Recommendation: add one sentence stating the survey and its result.
  Resolution: open.
- **F5 (non-blocking) — step 2 is conditional and ungated.**
  `specs/spec01.md:81-83` says to bring the `description` into agreement "if it
  now understates the surface". Nothing observes it and an implementer may do
  nothing. `README.md:17` and `.cartridge/help.md:9` already state "no
  arguments"; the manifest description is the only place that does not.
  Recommendation: either require the description change outright or drop step 2.
  Resolution: open.
- **F6 (accepted, no deduction) — acceptance (c) is guarded transitively only.**
  `just audit` lives in the superproject and can run in neither pass, since
  pass 2's cwd is `tools.ctg`, not the root. The spec says so at `:99-102` and
  the transitive argument is sound: a schema that refuses `{"unread":1}` cannot
  be absent or empty, which is exactly what `!event.schema` tests.
- **Noted, not a finding.** The probe project holds a single cartridge, so it
  cannot detect a future sibling that declares the same event name and shadows
  this schema in the merged directory. No such declarer exists today (verified).
  One sentence in the spec would record the limit.

Disposition: revise. The spec's reading of the code is correct and independently
confirmed on every load-bearing point, and its chosen shape for the Verify block
— real manifest, stubbed entry, cwd-captured path — is sound. The deductions are
about the gate's coverage and the block's cleanup, both small edits.

Validation: extracted `spec01.md:120-165` to `/tmp/reviewer-78-selftest-schema/block.sh`;
ran `sh -eu -c "$(cat block.sh)"` with cwd `/Users/feb/dev/cartridge/tools.ctg`
→ **exit 1**, 2 s, scratch directory left behind; with cwd a scratch copy
carrying `anyOf[null, closed object]` → **exit 0**; with cwd a scratch copy
carrying `anyOf[null, closed object, number, boolean]` → **exit 0** (the defeat).
Source reads: `tools.ctg` `git show 8d0dbe6 -- cartridge.json`;
`.cartridge/memos/routine/audit-cartridges.md:118`;
`cartridge.ctg/src/transport/cartridge.rs:239-278,973`, `src/host/mod.rs:811`,
`src/host/run.rs:173`, `src/cli/args.rs:76-79`, `src/host/socket.rs`;
`tools.ctg/init.lua:3`, `src/lib.rs:15`, `src/service.rs:335`,
`cartridge.json:7,47-50`. No source file was changed, no `prd` operation run,
nothing committed.

Reviewer identity: reviewer agent, coordinator-78 session (independent of the
analyst who wrote the spec).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** — 85/100, below the 90 threshold, with two blocking findings.
Unresolved blocking findings: F1 (scratch directory leaked on both failure
paths, `specs/spec01.md:145` and `:156`); F2 (refusal set omits number and
boolean, `specs/spec01.md:150`; demonstrated defeat).
Rounds used / remaining: 1 / 4.
Next action: bounded revision of `specs/spec01.md` addressing F1 and F2, and
preferably F3–F5, then re-review in round 2. No change to `prd.md` is required
beyond the reviewer's note that its Evidence section is stale; the spec already
carries that correction.

## Round 2 — 2026-09-19

Presented revision: `tools.ctg` at `024f5dd37e7cff0f940a4e5e1858c362c8959867`,
working tree clean. `prd.md` is unchanged since round 1; `specs/spec01.md` was
revised in place. Every command below was run as `env -u CARTRIDGE_YOLO …`,
because this machine's sessions export `CARTRIDGE_YOLO=1` and that variable
changes real host behaviour.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-tools-selftest-event-declares-its-schema/prd.md` — SHA-256 `7acf1741e45ed14558f012f0bb68dcee888f88c1fe1053c7ea678cc06a996aec` (unchanged from round 1) |
| Specs | `specs/spec01.md` — SHA-256 `95ff4a41cecf0790db4dbe5bf6e333da820a504ba0b298fdb4142b9052df3880` (round 1 reviewed `7781d11144bbb6544c8a60dfe670c8ecf24635b561da814c3969ffae0730618e`) |
| Material contracts/dependencies | `tools.ctg/cartridge.json` SHA-256 `84e3eb5080bbf92aa7006ac574f71b98b27aa6a01b921e9d08a59e19bd457169`; `cartridge.ctg` (`Ctx::validate`, `run_contracts`, `cli/mod.rs` project location); `.cartridge/memos/routine/audit-cartridges.md` (the `!event.schema` rule) |

Round 1's confirmed analysis was re-read, not re-litigated. The audit rule at
`.cartridge/memos/routine/audit-cartridges.md:118` is `if (!event.schema)`; the
host validates on the sender side at `cartridge.ctg/src/host/mod.rs:811` and
again at `src/transport/cartridge.rs:973`; `null` is forced by
`src/host/run.rs:173`. Nothing found in this round contradicts any of that.

### The three round 1 findings, judged

**F2 (was blocking) — cleared.** The refusal loop at `specs/spec01.md:175` now
walks `{"unread":1}`, `"a string"`, `[1]`, `42` and `true`, which is one
representative of every JSON type a caller can send. Round 1's counter-example
was re-run rather than taken on report: a manifest carrying
`anyOf[null, closed object, number, boolean]` now gives **exit 1** with `the
declaration let 42 reach the listener; …`. The census is complete over types,
so the fix is a property, not a patch fitted to last round's example.

**F1 (was blocking) — the directory leak is cleared, but the same trap has a
new and worse defect.** `probe=$(mktemp -d)` at `:149` is unique per run, the
`trap … EXIT INT TERM` at `:150` is armed before the first `mkdir` at `:151`,
and it covers the probe host and the directory together. Measured: after five
runs of the block, including two that exited 1 and one forced to abort
mid-setup, `find "$TMPDIR" -maxdepth 2 -name tools.ctg` returned nothing. The
new defect is where the trap's `stop` lands. `cd "$probe"` happens at `:161`,
eleven lines after the trap is armed, so an abort under `set -e` anywhere in
`:151-160` — a failed `mkdir`, `cp` or heredoc write — fires the trap with the
cwd still at the repo root. `cartridge` locates its project by walking up from
the cwd (`cartridge.ctg/src/cli/mod.rs:90`, `Command::Stop =>
client::ask(project, "stop", Value::Null)` at `:142`), and from
`/Users/feb/dev/cartridge/tools.ctg` that walk reaches the superproject:
`cartridge socket` prints `/tmp/cartridge-501/69a3b8e0c7a1/host.sock` from
`tools.ctg` and the identical path from `/Users/feb/dev/cartridge`. Demonstrated
without harming the live host by running the block from `tools.ctg` with a
forced failure after the `cp`, and `CARTRIDGE_BIN` pointed at a stub that
records its target: `stub invoked: argv=stop
cwd=/Users/feb/dev/cartridge/tools.ctg
targets=/tmp/cartridge-501/69a3b8e0c7a1/host.sock`. In a real collect that is
pass 2 stopping the machine's shared daemon.

**F3 (was non-blocking) — cleared, and the choice is right.**
`specs/spec01.md:54-66` now says in the spec's own voice that accepting `{}` is
"this spec's decision, not the code's", gives the reason, and writes down the
two-line change that produces the null-only alternative. The supporting
citation was checked rather than accepted: `cartridge.ctg/docs/creating-cartridges.txt`
reads "`cartridge doctor` sends the `doctor` event {} to every enabled cartridge
that declares one", so `{}` is the host's own spelling of an empty payload and
not a convention borrowed from elsewhere. Refusing it would make this one
declaration stricter than the host's own idiom for the same thing. The spec is
now honest about which constraint is forced (`null`, `src/host/run.rs:173`) and
which is chosen (`{}`).

F4 is substantially answered at `:55-57` ("nothing sends it anything but null"),
which is the caller survey round 1 asked for. F5 is not: step 2 at `:94-96` is
still conditional and still unobserved.

### The Verify block, measured

Extracted verbatim from `spec01.md:147-187` and run under
`env -u CARTRIDGE_YOLO sh -eu -c` with no other injected environment.

| Run | cwd | Observed |
| --- | --- | --- |
| current tree (`schema: {}`) | `/Users/feb/dev/cartridge/tools.ctg` | **exit 1** in 1.7 s — `the declaration let {"unread":1} reach the listener; …` |
| step 1's schema, `anyOf[null, closed object]` | scratch copy of the manifest | **exit 0** |
| round 1's counter-example, `anyOf[null, closed object, number, boolean]` | scratch copy of the manifest | **exit 1** — `the declaration let 42 reach the listener; …` |
| this reviewer's defeating schema (below) | scratch copy of the manifest | **exit 0** — the gate passes a declaration that admits a data-carrying object |

The defeating schema constructed for this round is
`{"anyOf":[{"type":"null"},{"type":"object","properties":{"verbose":{"type":"boolean"}},"additionalProperties":false}]}`.
It accepts `null` and `{}`, refuses all five probed payloads, and therefore
exits 0 — while admitting `{"verbose":true}`, which spec step 1 ("no object with
a property") and spec acceptance (b) both forbid. Confirmed against a live probe
host rather than inferred: with that manifest, `cartridge --yolo run
tools.selftest '{"verbose":true}'` answered `"the listener ran"` while
`{"unread":1}` and `42` were both answered with `` `tools.selftest` payload
rejected by its schema ``.

This is not a coverage gap of the kind round 1 found. The gate's payload census
is complete over JSON types; the hole is value-level inside a probed type, and
no finite set of constructed payloads can close it, because the property "and
nothing else" is universally quantified over an infinite payload space and a
schema can always admit exactly one property name the block did not guess.
Catching it needs a reading of the declared schema itself, which is a text gate
on the manifest and would name its own cure. This is the gate-design ceiling the
method describes, round 1 was the round spent on gate design, and it is
therefore recorded rather than treated as blocking: the diff reading is the
backstop for "the accepted set is exactly `null` and `{}`". The spec should say
so in one sentence; today it says only that every type is named, which is true
but reads as a completeness claim the gate does not support.

Static hazards are clean: no `${VAR:?}`, no `!` negation, no `a && b` guard,
`${CARTRIDGE_BIN:-cartridge}` defaulted, no cargo and so no `CARGO_TARGET_DIR`
needed, no `cd` to an absolute checkout, nothing written inside the footprint,
1.7 s against a 120 s limit, and the accepting loop runs first so a dead host
fails the block rather than letting the refusing loop pass on silence.

One residue the spec's comment does not account for. `:133-134` claims "no run
can leave a scratch project or a probe host behind". The project and the host
are indeed gone, but each run leaves two run directories under the shared socket
base: `ls /tmp/cartridge-501 | wc -l` went from 1381 to 1383 across a single
successful run. A collect runs the block twice, so it deposits four. They are
empty and `cartridge sweep` exists for exactly this, so it is not blocking, but
the comment overstates what was verified.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Round 1's −2 is restored. The `{}` rationale is now owned as a decision, its reason is sound, and its supporting citation was independently checked in `cartridge.ctg/docs/creating-cartridges.txt` — `cartridge doctor` really does send `{}`, so the chosen leniency matches the host's own idiom instead of inventing one. The narrower alternative and its exact edit are written down for the coordinator. |
| Ownership and reuse | 20 | Unchanged and unbroken by the revision. Footprint is exactly `tools.ctg/cartridge.json`; no host change proposed; the dialect of the sibling `tools` event is reused; `README.md` and `.cartridge/help.md` already say "no arguments". |
| Dependencies and implementable slices | 18 | Unchanged. −2 for F5, still open: step 2 at `:94-96` is conditional ("if it now understates the surface"), unobserved by the block, and an implementer may satisfy the spec by doing nothing to a description that today names no payload. |
| Observable acceptance and baseline evidence | 18 | F2 cleared and re-measured, including the round 1 counter-example now failing. The gate executes real refused calls against the real manifest and discriminates unfixed from fixed. −2 because the residual value-level hole is neither recorded nor backstopped: the spec's comment at `:136-139` reads as a completeness claim, and no sentence names the diff reading as what covers "and nothing else". |
| Failure, recovery and compatibility | 14 | The leak is genuinely fixed and F4 is substantially answered. −5 for B1: the trap at `:150` issues `cartridge stop` against whatever project the cwd resolves to, and for the eleven lines before `cd "$probe"` at `:161` that is the superproject's shared daemon, demonstrated above. −1 because the comment at `:133-134` claims a cleanliness the run directories under `/tmp/cartridge-501` contradict. |
| Reviewer total | 90 / 100 | At the threshold on score, but a pass needs at least 90 **and** no blocking finding, and B1 is blocking. |

Findings and concrete revisions:

- **B1 (blocking) — the cleanup trap can stop the shared daemon.**
  `specs/spec01.md:150` runs `"${CARTRIDGE_BIN:-cartridge}" stop` from whatever
  the current directory is, and the `cd "$probe"` that makes that directory the
  probe is at `:161`. Any `set -e` abort in `:151-160` therefore stops the host
  of the repo root instead, which on this machine is the one daemon six live
  sessions share (`cartridge socket` resolves identically from `tools.ctg` and
  from the superproject). Recommendation: target the probe explicitly, for
  example `trap '(cd "$probe" && "${CARTRIDGE_BIN:-cartridge}" stop) >/dev/null 2>&1 || true; rm -rf "$probe"' EXIT INT TERM`.
  The directory always exists once the trap is armed, so the subshell always
  lands on the probe. Resolution: open.
- **N1 (non-blocking, recorded ceiling) — the gate cannot prove "and nothing
  else".** Defeated with
  `anyOf[null, {"type":"object","properties":{"verbose":{"type":"boolean"}},"additionalProperties":false}]`
  at exit 0 while admitting `{"verbose":true}`. No payload enumeration can close
  this, and the alternative is a text gate on the manifest that would name its
  own cure. Recommendation: one sentence in the Verify comment recording that
  the census is over types rather than values, and naming the diff reading as
  the backstop. Not a reason to withhold a pass on its own.
- **N2 (non-blocking) — the comment overstates the cleanup.** `:133-134` says no
  run leaves anything behind; each run leaves two directories under
  `/tmp/cartridge-501` (measured 1381 → 1383). Recommendation: say that the
  scratch project and the probe host are removed and that the run directories
  are `cartridge sweep`'s business.
- **F5 (non-blocking, carried from round 1, still open) — step 2 is conditional
  and ungated**, `specs/spec01.md:94-96`. Recommendation unchanged: require the
  description change or drop the step.

Disposition: revise. The analysis is right, the `{}` decision is right, the gate
is as strong as a payload gate can be, and the one blocking defect is a
one-line correction to a trap.

Validation: extracted `spec01.md:147-187` to `/tmp/rev78r2/block.sh`; ran
`env -u CARTRIDGE_YOLO sh -eu -c "$(cat /tmp/rev78r2/block.sh)"` with cwd
`/Users/feb/dev/cartridge/tools.ctg` → exit 1 in 1.7 s; with cwd a scratch copy
carrying `anyOf[null, closed object]` → exit 0; with cwd a scratch copy carrying
`anyOf[null, closed object, number, boolean]` → exit 1; with cwd a scratch copy
carrying the reviewer's `verbose` schema → exit 0. Trap target demonstrated with
a stub `CARTRIDGE_BIN` and a forced mid-setup failure; no real `stop` was sent to
any host other than the probes. Source reads: `cartridge.ctg/src/cli/mod.rs:90,142`,
`src/cli/args.rs:12-22`, `docs/creating-cartridges.txt` (the `doctor` `{}`
convention); `tools.ctg/cartridge.json:47-50`. After every run,
`find "$TMPDIR" -maxdepth 2 -name tools.ctg` returned nothing and no probe host
survived. No source file was changed, no `prd` operation was run, nothing was
staged or committed.

Reviewer identity: reviewer agent, coordinator-78 session (independent of the
analyst and of the round 1 reviewer).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** — 90/100 on score, but the pass needs no blocking finding and
B1 is blocking.
Unresolved blocking findings: B1 (`specs/spec01.md:150`, the trap's
`cartridge stop` resolves to the shared daemon when the block aborts before
`:161`).
Rounds used / remaining: 2 / 3.
Next action: one-line correction of the trap at `specs/spec01.md:150`, and
preferably N1, N2 and F5 in the same edit, then re-review in round 3.

## Round 3 — 2026-09-19

Presented revision: `tools.ctg` at `024f5dd37e7cff0f940a4e5e1858c362c8959867`,
working tree clean. `prd.md` is unchanged since round 1; `specs/spec01.md` was
revised in place again. Every command in this round was run as
`env -u CARTRIDGE_YOLO …`, because `just launch claude --yolo` exports
`CARTRIDGE_YOLO=1` and that variable changes real host behaviour. Measurements
were taken against the daemon replaced at 13:02Z, the host built at
`cartridge.ctg` `324f36e`, with all 18 cartridges active.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-tools-selftest-event-declares-its-schema/prd.md` — SHA-256 `7acf1741e45ed14558f012f0bb68dcee888f88c1fe1053c7ea678cc06a996aec` (unchanged since round 1) |
| Specs | `specs/spec01.md` — SHA-256 `f74dff586e74cd8431b23ac0b1ae4a6770b0d03d25d2522224b82937be08c35f` (round 2 reviewed `95ff4a41cecf0790db4dbe5bf6e333da820a504ba0b298fdb4142b9052df3880`) |
| Material contracts/dependencies | `tools.ctg/cartridge.json` SHA-256 `84e3eb5080bbf92aa7006ac574f71b98b27aa6a01b921e9d08a59e19bd457169`; `cartridge.ctg` at `324f36e` (`Ctx::validate`, `run_contracts`, `cli/project.rs`, `loader::root`, `transport::typed::path_tag`); `.cartridge/memos/routine/audit-cartridges.md` (the `!event.schema` rule) |

The verified findings of rounds 1 and 2 were re-read, not re-litigated. Nothing
in this round contradicts them.

### B1, the round 2 blocker: fixed for the shared daemon, with one narrow residue

The trap at `specs/spec01.md:185` is now
`trap '(cd "$probe" && "${CARTRIDGE_BIN:-cartridge}" stop) >/dev/null 2>&1 || true; rm -rf "$probe"' EXIT INT TERM`.
It was tested with this reviewer's own stub on `CARTRIDGE_BIN`, which records
the cwd and the socket a real `stop` would have addressed and issues none. The
shared socket is `/tmp/cartridge-501/69a3b8e0c7a1/host.sock`, printed identically
by `cartridge socket` in `tools.ctg` and at the composition root.

| Abort path tested | Trap behaviour | Socket the stop addressed |
| --- | --- | --- |
| `mktemp -d` itself fails (abort before `:184` returns) | trap never armed; no invocation logged | none |
| abort between `mktemp -d` and the first write (`false` after `:185`) | subshell `cd` succeeds into an empty directory | `/tmp/cartridge-501/ee9824bf5d0a/host.sock` — the no-project fallback, **not** the shared daemon |
| abort after `mkdir -p` and before `.cartridge/init.lua` exists | stop from the probe | `/tmp/cartridge-501/69bbb4cf8de0/host.sock` — the probe's own |
| `cd "$probe"` itself fails (probe removed first) | subshell `cd` fails, `&&` short-circuits | none |
| `$probe` empty in the trap | `rm -rf ""` is a no-op; exit status preserved | none |

No path reaches `69a3b8e0c7a1`. The blocker is cleared. Two corrections to the
record it leaves behind. First, the fallback tag is not "the probe's own", as
the analyst report at `.state/loop/selftest-schema/analyst-1.md` states:
`cartridge.ctg/src/loader/mod.rs:97-102` falls back to the cwd when no ancestor
holds `.cartridge/init.lua`, and `src/transport/typed.rs:324-345` then hashes the
*relative* `.cartridge`, which fails to canonicalize and hashes the literal
string, so **every** directory on this machine without a `.cartridge` maps to
`ee9824bf5d0a` — measured identical from two different `mktemp -d` directories,
and different (`67195c56d702`) as soon as `.cartridge` exists. Second, the
directory `/tmp/cartridge-501/ee9824bf5d0a` exists and is empty, so nothing is
listening there today; the residue is narrow, not harmless in principle.

Exit-status preservation was checked separately, since the trap's last command
is `rm -rf`: a block exiting 1 still exits 1 through this `EXIT` trap under
`sh -eu`. A failing gate cannot report success.

### The gate, measured, and this reviewer's own defeating schema

The block was extracted verbatim from `spec01.md:182-220` (SHA-256
`569b49b9b820df51f629d55d6ff383f147009fbed091f7c4319ea2df7690b610`) and run
under `env -u CARTRIDGE_YOLO sh -eu -c` with no other injected environment.

| Run | cwd | Observed |
| --- | --- | --- |
| base tree, `schema: {}` | `/Users/feb/dev/cartridge/tools.ctg` | **exit 1** in 2 s — `the declaration let {"unread":1} reach the listener; …` |
| step 1's schema, `anyOf[null, closed object]` | scratch copy of the manifest | **exit 0** in 3 s |
| this reviewer's defeating schema (below) | scratch copy of the manifest | **exit 0** in 3 s — defeated |

The defeating schema is a blacklist rather than round 2's declared property:

```json
{"not":{"anyOf":[{"type":"string"},{"type":"number"},{"type":"boolean"},
                 {"type":"array"},{"type":"object","required":["unread"]}]}}
```

It refuses all five probed payloads and accepts `null` and `{}`, so it exits 0,
while admitting every object that does not carry an `unread` key. Confirmed
against a live probe host rather than inferred: `{"verbose":true}` and
`{"leak":"everything","nested":{"a":[1,2]}}` both answered `"the listener ran"`,
while `{"unread":1}` and `42` were both answered with
`` `tools.selftest` payload rejected by its schema ``.

This is the ceiling the method describes, and recording it was the right call.
It is not only that no payload enumeration closes the hole; the strongest
non-text strengthening available — deriving the probe payloads from the property
names the declaration itself mentions, which would catch round 2's `verbose`
schema — does not touch this one, because it declares no `properties` at all and
its single named key is the one it refuses. Any gate that catches it must read
the declared schema as text, which is the paste-in bypass the method forbids.
The spec is therefore right to record the ceiling and name the diff reading as
the backstop.

The backstop as *worded* is the problem. `specs/spec01.md:172-173` says the
reviewer "checks that the declared schema names no property". The schema above
names no property and still admits arbitrary data-carrying objects, so the
sentence as written passes it. The backstop has to be the acceptance condition
itself — the declaration admits nothing but the empty payloads — not a proxy for
it. That is one clause, and it does not name a cure.

### Step 2, and the cleanup comment

Step 2 at `specs/spec01.md:98-102` is now unconditional: rewrite the description
so it says the event takes no payload, read in the diff and deliberately
ungated. That is acceptable here and not a hole. The conditional form round 1
faulted let an implementer comply by doing nothing; the unconditional form
cannot be satisfied by an unchanged file, and the method's own rule is that a
gate pins a name and the diff reviewer is the backstop for a body. A gate on
particular words in a description would be exactly the text gate naming its own
cure. `README.md:17` and `.cartridge/help.md:9` were re-read and both already
say "no arguments", so leaving them is correct under the README-currency memo.

The cleanup comment at `:152-157` now matches what happens. Measured: one run
of the block deposits exactly **two** directories under `/tmp/cartridge-501`;
after three runs no scratch project remained under `$TMPDIR`
(`find "${TMPDIR:-/tmp}" -maxdepth 2 -name tools.ctg` empty), no `host.sock`
newer than the runs survived anywhere under the socket base, and the shared host
answered `cartridge status` with all 18 cartridges active. N2 is cleared.

### Citation drift

Two host citations have drifted since the daemon was rebuilt at `324f36e`. The
sender-side validation the spec cites as `src/host/mod.rs:811` is now
`src/host/mod.rs:820`, and the load-time schema check cited as
`src/loader/document.rs:184-186` is now `:191-193`. Both facts hold —
`self.ctx.validate(name, data).map_err(Error::Argument)?` and
`jsonschema::validator_for(schema)` — only the line numbers are stale.
`src/transport/cartridge.rs:973`, `src/host/run.rs:173`, `src/cli/mod.rs:142`
and `src/cli/args.rs:79` were each read at the cited line and are exact.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | Unchanged by the revision and re-checked, not carried. The `{}` decision is still owned in the spec's own voice with its reason; `README.md:17` and `.cartridge/help.md:9` were re-read and agree; the narrower null-only alternative and its exact edit remain written down for the coordinator. |
| Ownership and reuse | 20 | Footprint is exactly `tools.ctg/cartridge.json`; no host change proposed, and the host path that makes acceptance (b) reachable was re-read at the current `324f36e`. The sibling `tools` event's `anyOf` dialect (`cartridge.json:12-38`) is reused. |
| Dependencies and implementable slices | 19 | F5 is resolved: step 2 is unconditional and its ungated status is stated with a reason the method supports. −1 for the two stale host line numbers above, in a spec whose argument is anchored on cited lines. |
| Observable acceptance and baseline evidence | 18 | The gate discriminates, measured again in both directions on the current daemon, and the ceiling is now recorded rather than claimed away. −2 because the recorded ceiling understates the hole and the named backstop does not close it: a `not`-blacklist passes at exit 0 while admitting every object without an `unread` key, and it "names no property", which is the exact check `:172-173` asks the diff reviewer to perform. |
| Failure, recovery and compatibility | 18 | B1 is fixed: four abort paths tested with a stub, none addresses the shared daemon, and the exit status survives the trap. N2 is cleared and re-measured. −2 for R1: in the one-line window between `mktemp -d` and `mkdir -p` the stop lands on `ee9824bf5d0a`, the bucket every non-project directory shares, and the comment at `:140-150` claims the subshell pins the stop to the throwaway project and that an abort before the `cd` sends no stop at all. Both are more than holds. |
| Reviewer total | 95 / 100 | At or above the 90 threshold, with no blocking finding. |

Findings and concrete revisions:

- **R1 (non-blocking) — the trap's narrow window reaches a shared fallback
  socket, and the comment overstates the fix.** `specs/spec01.md:185` arms the
  trap one line before `mkdir -p` at `:186`; an abort in between finds a probe
  directory with no `.cartridge`, so `loader::root` falls back to the cwd and
  `path_tag` hashes the unresolvable relative `.cartridge`, giving
  `/tmp/cartridge-501/ee9824bf5d0a/host.sock` for every such directory on the
  machine. Demonstrated with a stub; nothing listens there today. Recommendation:
  arm the trap after `mkdir -p "$probe/.cartridge"`, or guard the subshell with
  `[ -d .cartridge ]`, and correct `:148-150` so it claims only what holds.
- **R2 (non-blocking) — the named backstop does not close the recorded
  ceiling.** `specs/spec01.md:172-173` asks the diff reviewer to check that the
  declared schema "names no property". This reviewer's defeating schema names
  none and admits arbitrary objects. Recommendation: state the backstop as the
  acceptance condition — the declaration admits nothing but `null` and `{}` —
  and record that a blacklist form, not only a declared property, is what gets
  past the payload census.
- **R3 (non-blocking) — stale host line numbers.** `src/host/mod.rs:811` →
  `:820`; `src/loader/document.rs:184-186` → `:191-193`, at `cartridge.ctg`
  `324f36e`. The facts are unchanged.
- **N1 (carried, recorded ceiling, not blocking)** — confirmed independently
  this round with a different and stronger defeat, and confirmed unclosable by
  any payload-derived gate. The method's rule applies: record, name the diff
  reading as backstop, score the remaining dimensions.

Disposition: keep, and implement. The reading of the code is correct at the
current host revision, the footprint is one file, the gate is as strong as a
payload gate can be and fails closed, and the round 2 blocker is genuinely
fixed. R1, R2 and R3 are one-line corrections that do not need another review
round; R2 is the one worth making before the diff is read, because it tells the
reader what to look for.

Validation: extracted `spec01.md:182-220` to `/tmp/rev78r3/block.sh`
(SHA-256 `569b49b9b820df51f629d55d6ff383f147009fbed091f7c4319ea2df7690b610`);
ran it as `env -u CARTRIDGE_YOLO sh -eu -c "$(cat block.sh)"` with cwd
`/Users/feb/dev/cartridge/tools.ctg` → exit 1 in 2 s; with cwd a scratch copy
carrying `anyOf[null, closed object]` → exit 0; with cwd a scratch copy carrying
the `not`-blacklist above → exit 0 (the defeat), then confirmed against a live
probe host that `{"verbose":true}` and `{"leak":"everything",…}` reach the
listener under it. Four abort paths run with `CARTRIDGE_BIN` pointed at a
recording stub; no real `cartridge stop` was issued against any project other
than probe hosts this review created, and no daemon was killed by process name.
Source reads at `cartridge.ctg` `324f36e`: `src/cli/project.rs:12-31`,
`src/loader/mod.rs:93-102`, `src/transport/typed.rs:324-345`,
`src/host/socket.rs:47-84`, `src/host/mod.rs:820`,
`src/transport/cartridge.rs:239-250,973`, `src/host/run.rs:173`,
`src/cli/mod.rs:90,142`, `src/cli/args.rs:79`, `src/loader/document.rs:191-193`;
`tools.ctg/cartridge.json:5-14,47-50`, `README.md:3,9,10,17`,
`.cartridge/help.md:3,9`. No source file was changed, no `prd` operation was
run, nothing was staged or committed.

Reviewer identity: reviewer agent, coordinator-78 session (independent of the
analyst and of the round 1 and round 2 reviewers).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** — 95/100, at or above the 90 threshold, with no unresolved
blocking finding.
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation of `specs/spec01.md`. Fold R1, R2 and R3
into the spec as part of that work; none of them requires a further review round.
