# root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text review history

Plan: board `root`, `prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/web-ctg-exists-as-a-cartridge-and-fetches-a-page-as-readable-text/prd.md`.
Scope: one observable outcome — a new `web.ctg` TypeScript cartridge that fetches a page as readable text and refuses anything off its own host allowlist. Executable leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-17

Presented revision: repo HEAD `e8fc2ba`, dirty at review start and end:
`M .cartridge/config.lua`, `M cartridge.ctg`, `M prd.ctg`, `M proxy.ctg`, `M router.ctg`
(submodule pointers moved by other sessions; unchanged by this review).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `ab441fac9c332169bb076aa97dbcabc80d70ccdce655fc786d8d305bd575a96f` |
| Specs | `specs/spec01.md` SHA-256 `9d4034059ff7fd8101d6c61caf738e391f61d6f05a7fb2c25f0ec4c14f599b70` |
| Material contracts/dependencies | `.cartridge/init.lua` SHA-256 `d9ff29579cd1718ef096fe7a1447e2f25f989cd91e9e437d034fdc0260ac0367`; `.cartridge/justfile:100-101`; `auth.ctg` at HEAD; `bun 1.3.14`; `cartridge` at `/Users/feb/.local/bin/cartridge` |

### Independently reproduced gate table

An independent reference implementation of `spec01.md` and four wrong versions
were built from scratch in `<scratch>/reviewer-web-fetch/` (none of the
analyst's artifacts were reused) and each of the three Verify blocks, extracted
verbatim from the spec, was run as `sh -eu` in a detached superproject worktree
of `e8fc2ba` with the submodule directories empty. Observed exit codes:

| Tree | Block 1 | Block 2 | Block 3 | Spec claims block 3 |
| --- | --- | --- | --- | --- |
| the change absent (clean worktree) | 1 | 1 | 1 | 1 ✓ |
| (a) declares `allow_hosts`, never checks it | 0 | 1 | 1 | 1 ✓ |
| (b) fetches, refusal path removed | 0 | 1 | 1 | 1 ✓ |
| (c) all declared, `Web.fetch` a stub, six empty tests | 0 | 1 | **0** | 1 ✗ |
| (d) reference `src/`, hollow suite (6 empty tests, 0 assertions) | **0** | **0** | **0** | — |
| the reference implementation | 0 | 0 | **1** | 0 ✗ |

Two of the spec's own measured rows do not reproduce. The clean tree correctly
fails all three. The behaviour gate (block 2) holds: it caught every cheat that
touched `src/web.ts`, including a real implementation defect of my own
(`HTMLRewriter` `text(t){t.remove()}` on `script`/`style` leaves the text in the
`*` handler's output — block 2 failed on `script contents reached the caller`
until I switched to an element-scoped drop counter). Block 2 could not be beaten.
Block 3 can be beaten completely, and block 3 also fails the correct answer.

### Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, one cartridge, an exact 14-row file table (`spec01.md:20-35`) and an explicit "nothing else". The credential question is correctly deferred to the sibling; only `grant.net` changes later (`prd.md:22-24`). −1: `spec01.md:37-41` decides the submodule question inside a spec rather than leaving it in the PRD's open-decision section where it already lives. |
| Ownership and reuse | 19 | Mirrors `auth.ctg` down to byte copies of `src/wire.ts`, `tsconfig.json`, both `.gitignore`s and `.cartridge/tests/integration/node.ts`; reuses the `auth.ctg/src/main.ts:5` injected-client seam, which is what keeps the suite off the live network. The Rust-is-unavailable reasoning (`prd.md:26-30`) is correct — every Rust cartridge is a workspace member and would need edits outside the footprint. `needs` absent, no `../<sibling>.ctg`, no symlink; `just isolation` verified passing. −1: `commands.build` correctly dropped but the reason (no `bun.lock`) is only in prose, not gated. |
| Dependencies and implementable slices | 18 | No `bun install`, no lockfile, no new submodule, no `.gitmodules`. `HTMLRewriter.transform(string)` returning a string synchronously reproduced (bun 1.3.14). Claims 4b, 4c, 4d all verified true (below). −2 for finding N1: the `bun test` engine fact at `spec01.md:130-133` is wrong in both halves. |
| Observable acceptance and baseline evidence | 9 | Block 1 and block 2 are honest and strong; block 2 is the best gate in any spec reviewed this session — it drives the module with a recording client and counts requests, so it cannot be satisfied by a grep. Block 3 is not a gate at all (B1), rejects the spec's own required test case (B2), and the spec's evidence table for it is false (B3). Acceptance box 5 — "at least six tests and twenty-five assertions" — is completely unenforced as written. |
| Failure, recovery and compatibility | 17 | Exact error-string contract (`spec01.md:55-56, 67-76`), refusal before the first statement of `fetch`, refusal returned to the model as `{error: true}` rather than thrown away, `max_bytes` and empty-allowlist defaults all pinned and all proven by block 2. −3 for N2/N3: the "every sibling" half of box 6 and the PRD's `cartridge help web` box are ungated and one of them is not even reworded to say so. |
| Reviewer total | **82 / 100** | FAIL — below 90 and three blocking findings. |

### Findings

**B1 (blocking) — `spec01.md:249` and `spec01.md:251`: both census guards are inert under `sh -eu`.**
`test -n "$pass" && test "$pass" -ge 6` and `test -n "$checks" && test "$checks" -ge 25`
are AND-OR lists; `set -e` is ignored for every command of such a list but the
last, and when the left side fails the list short-circuits so the last command
never runs. Measured directly:
`sh -eu -c 'checks=""; test -n "$checks" && test "$checks" -ge 25; echo after=$?'`
prints `after=1` and the shell exits **0**. Consequence: a tree carrying the
reference `src/` and a `fetch.test.ts` of six empty `test(...)` bodies with zero
`expect()` calls — bun then prints no `expect() calls` line at all, so `checks`
is empty — passes block 3 with exit **0**, and passes blocks 1 and 2 as well
(row (d) above). The assertion census the spec says it added specifically to
catch this is doing nothing. This is the same class as the recorded
`negated-grep-guards-are-inert-under-set-e` trap.
*Remedy (validated):* split each into two statements —
```sh
test -n "$pass"
test "$pass" -ge 6
...
test -n "$checks"
test "$checks" -ge 25
```
With that change the hollow suite scores block 3 = **1** and the reference
implementation still scores **0**.

**B2 (blocking) — `spec01.md:265`: the host filter rejects the spec's own required test case.**
The allowlist alternative `[a-z0-9-]+\.(example|test|invalid)$` admits exactly
one label before the reserved suffix, so `https://sub.allowed.example` is not
matched and block 3 exits 1 with *"a test names a host that is neither loopback
nor a reserved documentation name"*. But `sub.allowed.example` is the sub-domain
case the spec's own Acceptance box 4 (`spec01.md:99`) demands, the case block 2
itself drives (`spec01.md:203`), and the case `src/web.ts`'s "Match the host
exactly" rule (`spec01.md:72`) exists for. A correct implementation therefore
cannot pass block 3. Measured: reference implementation → block 3 = **1**; only
flagged token is `https://sub.allowed.example`.
*Remedy (validated):* `([a-z0-9-]+\.)+(example|test|invalid)$`. Reference
implementation then scores block 3 = **0**.

**B3 (blocking) — `spec01.md:299-305`: the measured evidence table is wrong in two rows.**
Row (c) ("everything declared, `Web.fetch` a stub, six empty tests") is recorded
as block 3 = **1**; reproduced independently it is **0**. The reference row is
recorded as `0 0 0`; reproduced it is `0 0 1`. The table is the only evidence the
spec offers that its gates hold, and the one row it was written to defend is the
false one. An implementer reading `spec01.md:238-240` ("the assertion census …
because six empty bodies would otherwise pass") will believe a guard that does
not exist.
*Remedy:* re-measure and rewrite the table after B1 and B2 land; row (c) then
genuinely reads `0 1 1` and the reference row `0 0 0`.

**N1 (non-blocking) — `spec01.md:130-133`: the `bun test` engine fact is wrong in both halves.**
Measured in the live repo with bun 1.3.14:
`bun test auth.ctg/.cartridge/tests/` (no `./`) matches nothing and exits **1**,
not 0 — bun prints *"Tests need \".test\"… in the filename"*. And
`bun test ./auth.ctg/.cartridge/tests/` — a directory, with `./` and without
naming a file — **does** descend the dotdir: `15 pass, 0 fail, 74 expect() calls,
Ran 15 tests across 3 files`, exit 0. So neither "finds nothing and still exits
0" nor "unless it is given with a leading `./` AND names the file" is true. The
form block 3 actually uses is fine, so nothing fails today, but the comment will
mislead the next editor.
*Remedy:* replace the paragraph with the two measured facts above.

**N2 (non-blocking) — `spec01.md:101` / `prd.md` Acceptance box 6: "both still pass for every sibling" is not gated.**
Block 1 runs `just audit web` (one cartridge: verified output `audit: 1 of 1
cartridges pass the hard checks`) and `just isolation` (composition-wide, so the
sibling half is covered there), but never `just audit` across all targets — and
it cannot, because in a superproject lane every sibling directory is empty.
*Remedy:* narrow the box to `just audit web` plus `just isolation`, and record
the all-cartridge `just audit` as a pass-2/post-merge manual check in the block
comment where the other two deliberate omissions are already explained.

**N3 (non-blocking) — `prd.md` Acceptance box 2: "`cartridge help web` prints the page and exits zero" is unprovable as written.**
Claim 4b verified true: in the scratch superproject worktree with `web.ctg` and
the profile entry present, `cartridge help web </dev/null` exits **1** with
`<tree>/.cartridge/init.lua: is in no trusted project; review it, then run
`cartridge trust <dir>``, and the prompt does not wait on a non-tty. `spec01.md:97`
already reworded its own box honestly to the three facts that make the page
exist; the PRD's box still asserts the exit code.
*Remedy:* reword the PRD box to match `spec01.md:97`, or mark it a manual
post-merge check in a trusted checkout.

**N4 (non-blocking) — `spec01.md:223`: block 2 bypasses the `make` seam it is testing.**
`serve({on: …}, () => web)` discards the config argument, so
`handlers.get("apply")({allow_hosts: […]})` proves only that `apply` is
registered, never that it builds a `Web` from the host's config. The
"settings must be read from the config the host passes" requirement
(`spec01.md:90-92`) is proven earlier by direct construction, so this is a gap in
coverage, not a hole a cheat walks through.
*Remedy:* pass `config => new Web(config, {fetch: client})` and assert the
allowlist from `apply` takes effect.

### Verified analyst claims

| Claim | Verdict | Evidence |
| --- | --- | --- |
| 4a `bun test web.ctg/.cartridge/tests/` matches nothing and exits 0 | **FALSE**, both halves | exits 1; and the `./dir/` form does descend the dotdir (N1) |
| 4b `cartridge help web` cannot be a Verify block | **TRUE** | exit 1, "is in no trusted project", non-tty prompt does not wait |
| 4c `just check web` / `just test web` can never work | **TRUE** | `.cartridge/justfile:100-101` hardcode the target lists; `web` absent; that file is outside the footprint |
| 4d `just audit web` and `just isolation` exit 0 in a superproject worktree with empty submodules | **TRUE** | both ran inside block 1 in exactly that tree: `audit: 1 of 1 cartridges pass the hard checks`, `isolation composition pass`, superproject dirt appearing only as soft `find:` lines |

### Acceptance boxes against the gates

| Box | Gated by | Verdict |
| --- | --- | --- |
| `spec01.md:96` manifest, listen, settings, `grant` | block 1's `bun -e` manifest probe | gated |
| `spec01.md:97` profile entry, README ≥ 10 lines, non-empty help.md | block 1 `grep -qn`, `awk NF`, `test -s` | gated (see N3 for the PRD's wording) |
| `spec01.md:98` readable text, title, bytes, truncated, `max_bytes` | block 2 lines 184-197 | gated, strongly |
| `spec01.md:99` every refusal, no request made, `{error:true}` to the caller | block 2 lines 199-231 | gated, strongly |
| `spec01.md:100` six tests, twenty-five assertions, loopback-only hosts | block 3 | **NOT gated** (B1); and the host clause rejects a required case (B2) |
| `spec01.md:101` `just audit web`, `just isolation`, "every sibling" | block 1 | first two gated; "every sibling" not (N2) |

### Cost of the specified work

The reference implementation took ~25 minutes: thirteen files, of which five are
byte copies (`wire.ts`, `node.ts`, `tsconfig.json`, both `.gitignore`s) and three
are near-copies (`init.lua`, `package.json`, the manifest shape). The only real
engineering is `readable()` — roughly fifteen lines, and the obvious
`HTMLRewriter` spelling is wrong in a way block 2 catches. `complexity: 3` is
right; the spec's step list is sufficient to build from without further
questions.

Disposition: revise. The spec is one 3-line edit away from being the strongest
in this session; the defect is confined to block 3.
Validation: `sh -eu` on each extracted block, cwd `<scratch>/reviewer-web-fetch/tree`
(detached worktree of `e8fc2ba`, submodules empty), 18 block runs plus 3 runs of a
patched block 3; `bun 1.3.14`; no block exceeded 25 s. No repository file was
written; `git status --porcelain` identical at start and end; the scratch worktree
is removed.
Reviewer identity: independent reviewer agent `reviewer-web-fetch`, round 1.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (82/100, three blocking findings).
Unresolved blocking findings: B1, B2, B3.
Rounds used / remaining: 1 / 4.
Next action: bounded revision of Verify block 3 (split the two census guards into
single statements; widen the reserved-host alternative to `([a-z0-9-]+\.)+`),
re-measure the evidence table, correct the `bun test` comment, then re-review.

## Round 2 — 2026-09-17

Presented revision: repo HEAD `67a773b` (the spec was measured by the analyst at
`e8fc2ba`; I re-measured at `e8fc2ba` in a detached worktree so the tables are
comparable). Working tree dirty at review start and end, identically:
`M .cartridge/config.lua`, `M prd.ctg`, `M proxy.ctg`, `M router.ctg`
(submodule pointers moved by other sessions; unchanged by this review).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `606d1df14c2937b520a950392d73383b4ef5d189cba95414d24225fb436661f8` |
| Specs | `specs/spec01.md` (published spec02 text, second revision) SHA-256 `366275a1cde3e941fa9bd919a39cdfb60b0136134f0e07119fb9d8a5299c15da` |
| Material contracts/dependencies | `.cartridge/init.lua` SHA-256 `d9ff29579cd1718ef096fe7a1447e2f25f989cd91e9e437d034fdc0260ac0367`; `.cartridge/justfile:100-101`; `auth.ctg` at HEAD; `bun 1.3.14`; `cartridge` at `/Users/feb/.local/bin/cartridge` |

### Independently reproduced gate table

The three ```` ```sh ```` fences were extracted from the **published** spec by
`awk` (3 fences, 31/65/31 lines) and run verbatim as `sh -eu <file>` — no script
of the analyst's was used and none of its artifacts were read as input. A fresh
reference implementation (13 files, five byte copies of `auth.ctg`) and eight
wrong versions were built in `<scratch>/reviewer-web-fetch-r2/`, each installed
into a detached superproject worktree of `e8fc2ba` with the submodule
directories empty. 27 block runs. Observed exit codes:

| Tree | Block 1 | Block 2 | Block 3 | Spec claims |
| --- | --- | --- | --- | --- |
| the change absent (clean worktree) | 1 | 1 | 1 | 1 1 1 ✓ |
| (a) declares `allow_hosts`, never checks it | 0 | 1 | 1 | 0 1 1 ✓ |
| (b) fetches, refusal path removed | 0 | 1 | 1 | 0 1 1 ✓ |
| (c) `Web.fetch` a stub, six empty test bodies | 0 | 1 | 1 | 0 1 1 ✓ |
| (d) reference `src/`, hollow suite (6 empty tests, 0 assertions) | 0 | 0 | 1 | 0 0 1 ✓ |
| (e) `serve`'s `apply` ignores the host's config | 0 | 1 | 0 | 0 1 0 ✓ |
| (f) `commands.build --frozen-lockfile`, no `bun.lock` | 1 | 0 | 0 | 1 0 0 ✓ |
| the reference implementation | 0 | 0 | 0 | 0 0 0 ✓ |
| **(g) reference `src/`, suite padded to 6 tests / 30 trivial assertions** | **0** | **0** | **0** | — (my cheat, N5) |
| (h) allowlist enforced only when a client is injected | 0 | 0 | 1 | — (my cheat, caught) |

**Every one of the spec's eight rows reproduces exactly.** The reference passes
all three blocks; every wrong version the spec lists is caught by at least one.
Row (d) — the tree that beat all three gates in round 1 — is now caught by block
3 (`test -n "$checks"` fires on the missing `expect() calls` line). Rows (e) and
(f), the two gates added for round 1's prose-only arguments, both bite with the
messages the spec predicts (`a re-applied allow_hosts did not take effect: the
old host is still reachable`; `commands.build installs --frozen-lockfile but the
cartridge ships no bun.lock`).

Attempts to beat it: block 2 again could not be beaten by any implementation
that is actually wrong — (h), a deliberately seam-aware sabotage that enforces
the allowlist only when `deps.fetch` is injected, walks past block 2 but is
caught by block 3 because the spec's required test 6 drives the real `serve`
seam through `node.ts` with the default (non-injected) client. Block 3 was
beaten once, by (g) — see N5.

### Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome, one cartridge, an exact 14-row file table and an explicit "nothing else". Round 1's −1 is closed: the submodule question is no longer decided in the spec, which now points at the PRD's open-decision section and only constrains the footprint (no `.gitmodules`, no Cargo path dep, no symlink, no `../<sibling>.ctg`). −1: the spec is still titled `spec02` in a file named `spec01.md`; the supersession note inside it makes this navigable but the filename and the heading disagree. |
| Ownership and reuse | 19 | `auth.ctg`'s shape down to byte copies; the `main.ts:5` injected-client seam is what keeps the suite off the live network, and I rebuilt against it without friction. Round 1's −1 closed: the dropped `commands.build` is now *gated*, not argued — tree (f) reproduces block 1 = 1. −1: the manifest contract is only in prose plus a `bun -e` probe; `grant.net` and `allow_hosts` both defaulting to the placeholder `example.com` is recorded in the analyst report but nowhere in the spec. |
| Dependencies and implementable slices | 19 | No `bun install`, no lockfile, no submodule. N1 closed: I re-measured both halves myself — `bun test auth.ctg/.cartridge/tests/` exits **1**, `bun test ./auth.ctg/.cartridge/tests/` exits **0** with `15 pass, 74 expect() calls`; the spec comment now carries exactly these two facts. The `HTMLRewriter` drop-counter trap the round-1 reviewer hit by accident is written into the spec, and I did not re-hit it. −1: `complexity: 3` is right but the suite (six tests, ≥25 assertions, one of them a real `Wire` over a `PassThrough` pair) is over half the build cost and is not called out as such. |
| Observable acceptance and baseline evidence | 18 | B1, B2 and B3 all close, verified independently (below). Block 2 remains the strongest gate in this session: it drives the module with a recording client, counts requests, and now re-applies a different `allow_hosts` through the real `serve` seam. The evidence table is now true in every cell. −2 for N5: block 3's censuses are counts, and a suite of six correctly-titled tests padded with `expect(noise.length).toBe(2)` scores `6 pass, 0 fail, 30 expect() calls` and passes all three blocks (tree (g)). Acceptance box 5's "proves fetch and every refusal" is therefore gated in shape, not in substance. |
| Failure, recovery and compatibility | 19 | Exact error-string contract, refusal as `fetch`'s first statement, refusal returned to the model as `{error: true}`, `max_bytes` and the empty-allowlist default all pinned and all proven by block 2 in my own tree. N2 and N4 closed (below). −1: the one standing inference — that the cartridge loads under a running daemon — is honest and unavoidable in a lane, but the spec's own block comment does not name it; only the analyst report does. |
| Reviewer total | **94 / 100** | PASS — ≥90 with no unresolved blocking finding. |

### Verdict on every round-1 finding

**B1 — inert AND-OR census guards. CLOSED.** I confirmed the inertness
independently: `sh -eu -c 'n=""; test -n "$n" && test "$n" -ge 6; echo after=$?'`
prints `after=1` with `SHELL_EXIT=0`. Block 3 now carries six single-statement
guards, one per line. **I swept all three blocks myself** for the shape: the only
shell-level `&&`/`||` in any block is block 3 line 2,
`bun test … || { cat "$log"; rm -f "$log"; exit 1; }`, whose last command is an
explicit `exit 1` — correct, not inert. Every other `&&`/`||` hit is inside the
`bun -e` JavaScript of blocks 1 and 2, where it is an ordinary boolean. No
statement-level `! grep` anywhere (`grep -n '! *grep'` → none), and no BRE `\|`
alternation — the one alternation, the reserved-host filter, is `grep -vE`.
Reproduced: (d) block 3 = **1**, reference block 3 = **0**.

**B2 — the reserved-host regex rejected a required case. CLOSED.** With
`([a-z0-9-]+\.)+(example|test|invalid)$` my reference suite, which names
`sub.allowed.example` exactly as Acceptance box 4 and block 2 require, passes:
reference block 3 = **0**. The pattern still rejects what it should — it is
`grep -vE … | grep -q .` on `grep -rhoE 'https?://[a-zA-Z0-9.-]+'`, anchored at
`$`, so a real host (`https://en.wikipedia.org`) is still flagged; loopback,
`localhost`, any depth of `*.example|test|invalid`, and `example.com|org|net` pass.

**B3 — the evidence table was false in two rows. CLOSED.** I extracted the three
fences from the published spec myself and ran them against my own eight trees:
all eight rows reproduce, including the two that were wrong last round — row (c)
is genuinely `0 1 1` and the reference row is genuinely `0 0 0`. The analyst's
claim that the fences are byte-identical to the scripts it measured is consistent
with what I observe: the published fences produce exactly the published numbers.

**N1 — the `bun test` engine fact. CLOSED**, both halves re-measured by me (above).

**N2 — "every sibling" ungated. CLOSED.** Acceptance box 6 is narrowed to
`just audit web` plus `just isolation`, with the composition-wide property of
`just isolation` stated and the all-cartridge `just audit` recorded as a
post-merge check against the 17-of-17 baseline, in the block comment beside the
other two deliberate omissions. Verified in my worktree: block 1's
`just audit web` → `audit: 1 of 1 cartridges pass the hard checks`, `just
isolation` → `isolation composition pass`, both exit 0 with the submodules empty.

**N3 — the PRD's `cartridge help web` box. CLOSED, and the rewording is
correctly bounded.** The new box asserts only the three artefacts that make the
page exist, each of which block 1 gates directly (`grep -qn 'id = "web", path =
"web.ctg"'`, `awk 'NF' … -ge 10`, `test -s …/help.md`) — all three verified
firing in my trees. It keeps the original intent visible ("print a page and exit
zero **in a trusted checkout**") and names the post-merge manual check plus the
measured reason (exit 1, `is in no trusted project`, prompt does not wait on a
non-tty). **It does not narrow the PRD's intent too far**: the only thing dropped
is an assertion no Verify pass in either lane or repo can make, and it is
re-homed as a named manual check rather than deleted. The parenthetical
explaining the rewording is long for a checkbox, but that is style, not scope.

**N4 — block 2 bypassed the `make` seam. CLOSED, and it now bites.** Block 2
passes `config => new Web(config, {fetch: client})`, asserts `make` ran exactly
once, then re-applies a different `allow_hosts` and requires both directions.
Tree (e) reproduces block 2 = **1** with the predicted message.

**Both round-1 score deductions outside the findings — CLOSED.** The submodule
decision now lives only in the PRD (dimension 1); the dropped `commands.build` is
gated by block 1 rather than justified in prose, reproduced as tree (f)
(dimension 2).

### New finding

**N5 (non-blocking) — block 3's censuses are counts, and a padded suite meets
them.** Tree (g): the reference `src/` plus a `fetch.test.ts` of the six exact
required titles, each body five copies of `expect(noise.length).toBe(2)`, with
`Bun.serve`, `127.0.0.1`, `OFF_ALLOWLIST` and `NOT_HTTP` present only as an
import and a comment. Measured `6 pass, 0 fail, 30 expect() calls` and
**block 1 = 0, block 2 = 0, block 3 = 0** — all three gates passed by a suite
that proves nothing. This is strictly weaker than round 1's (d): the *code* is
still fully gated by block 2, so no defective implementation can ship through
it; what escapes is only the suite's value as a regression net. Not blocking.
*Remedy, if it is worth the lines:* have block 3 mutate one thing and require the
suite to fail — e.g. run `bun test` a second time with an env var that the
`Web` constructor honours by skipping the allowlist, and require a non-zero exit.
Cheaper alternative: require the per-test assertion floor by naming a minimum for
`Ran N tests across 1 file` together with a higher `expect()` floor; it raises
the cost of padding without closing it.

### Note, not a finding

The spec requires (suite item 6) a real `Wire` driving a **refused** `call`
through the default, non-injected client. That is what catches tree (h), so it
earns its place — but on a *broken* implementation that same test makes a real
DNS lookup for `denied.example` before failing. `denied.example` is a reserved
documentation name that resolves nowhere, so the cost is a timeout, not traffic
to a stranger; worth knowing, not worth changing.

### Acceptance boxes against the gates

| Box | Gated by | Verdict |
| --- | --- | --- |
| spec box 1 — manifest, listen, settings, `grant`, `commands` | block 1's `bun -e` probe | gated; tree (f) proves the `build`/lockfile clause bites |
| spec box 2 — profile entry, README ≥ 10 lines, non-empty help.md | block 1 `grep -qn`, `awk NF`, `test -s` | gated (PRD box 2 now matches) |
| spec box 3 — readable text, title, bytes, truncated, `max_bytes` | block 2 | gated, strongly; trees (a)(b)(c) caught |
| spec box 4 — every refusal, no request made, `{error:true}`, re-apply | block 2 | gated, strongly; trees (a)(b)(e) caught |
| spec box 5 — six tests, 25 assertions, loopback-only hosts | block 3 | gated in shape (hollow caught, tree (d)); **not gated in substance** (N5, tree (g)) |
| spec box 6 — `just audit web`, `just isolation` | block 1 | gated; both exit 0 in a superproject worktree with empty submodules |

### Ruling on the analyst's disclosure

Accepted, and the correction is real, not rhetorical. The root cause it names —
reading piped output and asserting an exit code it never looked at — is exactly
what produced the false 4a claim, and I re-measured both halves myself and got
the analyst's new numbers. Of the claims it now marks *measured*, I independently
re-measured: the AND-OR inertness, both `bun test` path forms, `just audit web`
and `just isolation` in an empty-submodule worktree, all 21 of its table cells,
and the `cartridge help web` reasoning (through N3's artefacts). They hold.
**The one remaining inference — that the cartridge loads under a running daemon
and answers a live `tool.web` dispatch — is acceptable to leave standing.** It
cannot be measured inside this footprint (a lane is untrusted, and editing a
manifest untrusts the live project), the layer below it is measured three ways
(the manifest by `just audit web`, the handlers and the `apply` seam by block 2,
the wire by `node.ts` in test 6), and the unmeasured part is a fifteen-line copy
of a file that works. It is labelled as an inference, which is the whole of what
round 1 asked for. My only note is that the label lives in the analyst report and
not in the spec's block comment, where the other three deliberate omissions are;
that costs one point in dimension 5, nothing more.

Disposition: keep. Proceed to implementation.
Validation: `awk` fence extraction from the published spec (3 fences); `sh -eu`
on each extracted block, cwd `<scratch>/reviewer-web-fetch-r2/tree` (detached
worktree of `e8fc2ba`, submodules empty); 27 block runs across nine trees
(reference, clean, a–f, plus my (g) and (h)); `bun 1.3.14`; no block exceeded
25 s. No repository file was written outside this review record;
`git status --porcelain` identical at start and end
(`M .cartridge/config.lua`, `M prd.ctg`, `M proxy.ctg`, `M router.ctg`);
the scratch worktree is removed and `git worktree list` shows only the repo.
Reviewer identity: independent reviewer agent `reviewer-web-fetch-r2`, round 2
(a different agent from round 1; round 1's artifacts were not reused).
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** (94/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: implement the spec as written. N5 is optional and may be taken as a
one-line strengthening of block 3 at implementation time or left alone.
