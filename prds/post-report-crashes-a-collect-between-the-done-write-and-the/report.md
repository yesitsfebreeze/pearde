# post_report crashes a collect between the done write and the commit — implementer report

Verdict: DONE

Second pass on `probe-then-spec`. The specs and the build were already in the
lane from the analyst's pass; nothing was built and nothing was written to
`resources/` this run. All six acceptance boxes on `spec01` are ticked against
output quoted below, the spec's `## Verify and Proof` block exits 0 on the
tree that holds the build and exits 1 on the tree that does not, and every
count the analyst published re-measures identically.

The one edit this run made to any file is the six `[ ]` to `[x]` ticks in
`prds/post-report-crashes-a-collect-between-the-done-write-and-the/specs/spec01.md`.
`resources/board/collect.py` in the lane is byte-for-byte what the analyst
left: `git -C <lane> status --short` is ` M resources/board/collect.py` and
nothing else, before the first command and after the last.

## Roots

- checkout (orchestrator's, `main`): `/Users/feb/dev/infra/pearde` at
  `148e0095e8dec56e4b8efea68ed43d0161a9f628`, recorded before the first run and
  unmoved at the last.
- board (`pearde` branch): `/Users/feb/dev/infra/pearde/pearde`, reached as
  `.pearde` through the symlink `.pearde -> pearde`, at `d51ed16`.
- lane: `/Users/feb/dev/infra/pearde/pearde/.lanes/post-report-crashes-a-collect-between-the-done-write-and-the`
  at `58c92e6`, one modified file.

The lane was cut at `58c92e6` and the checkout has moved since, so every
harness was run twice — `PEARDE_ROOT=<lane>` for the tree that holds the build,
and unset (the checkout) for the tree that does not. Both are quoted.

## The boxes

All six ticked. The evidence, per box:

**1 — `post_report` returns a phrase and raises nothing for the four
live-but-wrong daemons.** `probe/verify.sh` stands up each shape on a socket
and runs a real collect against it. On the lane:

```
ok T/garbage  ...no traceback   ok T/garbage  ...the line says not posted
ok T/truncate ...no traceback   ok T/truncate ...the line says not posted
ok T/list     ...no traceback   ok T/list     ...the line says not posted
ok T/entry    ...no traceback   ok T/entry    ...the line says not posted
```

**2 — a collect against each of the four exits 0 and lands.** Same four
groups, six checks each: `exit 0`, `...no traceback`, `...the line says not
posted`, `the record says done`, `...with a commit: on it`, `...two commits on
top`. 24 checks, all `ok`.

**3 — a correct daemon is still posted to.**
`ok T/ok exit 0`, `ok T/ok the line says report posted`, `ok T/ok ...two
commits on top`.

**4 — a raise from anywhere in the window is a refusal, not a tear.**
`probe/inject.py` replaces `post_report` with a bare `RuntimeError`:

```
ok T/inject exit 1 — a refusal, not a traceback
ok T/inject ...nothing escaped
ok T/inject ...it says the record was put back
ok T/inject ...and names what raised
ok T/inject the record was put back whole
ok T/inject ...and nothing was committed
```

**5 — `close_container` is guarded the same way.**
`ok T/container exit 0`, `...no traceback`, `...the line says not posted`,
`the record says done`, `...one commit on top`; and
`ok T/container-inject exit 1`, `...nothing escaped`, `the record was put back
whole`, `...and nothing was committed`.

**6 — the committed collect harnesses.** Run with `PEARDE_ROOT=<lane>`:

| harness | published by pass one | this run |
|---|---|---|
| `collect-stages-a-shared-file-whole` | 32 passed, 0 failed | `---- 32 passed, 0 failed` |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101 · 0 | `101 checks · 101 pass · 0 fail` |
| `the-board-runs-itself/collect-is-a-command` | 133 · 0 | `133 checks · 133 pass · 0 fail` |
| `collect-must-not-reset-the-checkout-it-did-not-write` | 31 · 0 | `31 checks · 31 pass · 0 fail` |

The baseline is **inherited from pass one and confirmed**, not re-taken: the
build is uncommitted but in a lane whose only modified file is the footprint,
and every published count re-measures equal on the built tree, which confirms
the inherited numbers without a window in which the tree is half-reverted.

## The flip, shown against the tree that does not hold the build

`collect-stages-a-shared-file-whole` is the box's own claim, and it is the
honest red side. Run from the checkout, whose `collect.py` lacks the fix:

```
---- 25 passed, 7 failed
verify.sh exit 1
FAIL 2c-real-exit: got [1], want [0]
FAIL 2d-a-line-committed: expected [one-A] in: eight
FAIL 3c-real-ok: got [1], want [0]
FAIL 3d-committed: expected [one-A] in: eight
FAIL 4a-widen-ok: got [1], want [0]
FAIL 4b-widen-named: expected [widened shared.py] in:        ~~~~~~~~~~~~~~~^^^^^^^^^^^
FAIL 4c-whole-file: expected [ten-B] in: eight
```

25 pass / 7 fail on the unfixed tree, 32 pass / 0 fail on the fixed one, with
no line of that harness changed. That harness sets no `PEARDE_PORT`, so it
reaches the live daemon and walks the `boards` list to the virtual `all` board
whose `path` is `null` — the crash this unit fixes, counted against another
PRD until now.

The spec's whole `## Verify and Proof` block, awked out and run the way
`collect` runs it (`bash -e -o pipefail -c`), both ways:

```
verbatim, from the checkout (no build):  exit 1  ·  verify: 75 checks · 44 pass · 31 fail
PEARDE_ROOT=<lane> (the build):          exit 0  ·  75 · 75 · 0  |  32 passed, 0 failed  |  101 · 101 · 0
```

That is the red-to-green flip against the tree that does not hold the build —
the whole gate ran on the old file — and it is why no `git show HEAD:`
predicate check was needed. The block is left exactly as written: it names no
root, so `collect` running it from the checkout after the merge will read the
merged `collect.py` and exit 0.

## What the merge must not do

`resources/board/collect.py` moved in the checkout after the lane was cut:
`344d09d a-verify-block-that-pipes-a-probe-exits-zero-on-a-broken-tre` rewrote
`run()` to pass the block as an argument with stdin closed. The lane, at
`58c92e6`, still carries the old `input=script` form. The lane's own diff
against `58c92e6` is 63 insertions / 25 deletions confined to `post_report`
(about line 1395) and the `collect_one` / `close_container` windows (about
line 1976), disjoint from `run()` at about line 401, so a rebase of the lane
onto `main` keeps `344d09d`. A whole-file copy of the lane's `collect.py` over
the checkout's would silently revert it. Merge the hunks, not the file.

`probe/verify.sh` pins `58c92e6`, and `58c92e6` is an ancestor of the
checkout's `main` HEAD, so the pin stays reachable from the checkout after the
merge and the harness keeps working where `collect` will run it.

## The repo's own gate

Run in both roots, after the ticks — no baseline of my own was needed, because
this run wrote nothing outside `specs/spec01.md`.

| gate | checkout | lane |
|---|---|---|
| `python3 resources/index.py check` | exit 1 · 1 line | exit 1 · 3 lines |
| `bash resources/doctor.sh` | exit 1 · `index broken`, `origin broken` | not run — the board harness set is nailed to the checkout |

The checkout's one index line is
`references/language.md references @references/personas/writer.md — not on disk`.
The lane prints that one and two more —
`@@share names @pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md`
and the same handle from `index.md` — which the checkout does not print. That
is the lane being behind the checkout, not a regression: a sibling closed those
two handles in a commit the lane does not carry, and they close on the merge.
Nothing was added in the lane to silence them.

Doctor's two broken rows are `index` (the same `writer.md` handle) and
`origin` (`33 derived · 1 with no from:`). Neither names `collect.py` and
neither is this unit's. Doctor's `view` row is `ok · watching ·
http://127.0.0.1:8443/board/pearde-2` after the run — nothing in the set
stopped the live daemon.

No fixture board reached the live registry: the freshest temp board in
`serve.py status` synced 1239 s before this report was written, older than the
first command of this run. The probe points every fixture at a stub port or at
`PEARDE_PORT=1`.

## Findings

Carried forward from pass one, each still open, plus one new:

- **The virtual `all` board's null `path`** — `resources/board/serve.py` puts
  `"path": null` on the virtual `all` board in `/status`. Confirmed still live
  this run: `all synced never · None · master of 25`. Every other reader of
  that list has the same trap; this unit only stops `collect` dying of it. A
  separate contract.
- **`index.py check` is red on three handles**, none touched by this build:
  `@pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md` (from
  `@@share` and from `index.md`, lane only — closes on the merge) and
  `@references/personas/writer.md` (from `references/language.md`, red in both
  roots). Pre-existing.
- **`doctor`'s `origin` row is broken** — `33 derived · 1 with no from:`. Not
  this unit's; not fixed.
- **A candidate invariant, not written** — "a collect never leaves a PRD `done`
  on disk with nothing committed" is now enforced by two guards and by
  `inject.py`, and would carry a verify command. Writing it would widen this
  contract, so it is named here rather than done.
- **Knowledge gap enqueued** by pass one: `.pearde/wiki/pending/260902-9152.md`.
- **A job that recurs and already has its file** — reproducing a defect against
  a pinned pre-fix copy of one module in scratch is `attempt-the-build`, as
  four harnesses on this board now do it. It wants no second workflow file.
- **New this run: the lane's `collect.py` is one commit behind the checkout's**
  on an unrelated hunk. See *What the merge must not do*. This is not a defect
  in anything; it is the shape every lane cut before a sibling lands has, and
  it is worth the orchestrator reading before `collect` writes.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ok — `prd.md`'s body is the unedited template, so the contract was taken from `specs/spec01.md` and pass one's `report.md`, per the atomic's own row for that shape. `git status --short` recorded in the checkout, the board and the lane before the first command. Footprint `resources/board/collect.py` exists in all three roots. |
| 2 | `capture-the-harness-baseline` | ok — baseline **inherited from pass one and confirmed** by re-running its whole published set on the built tree and showing every count equal. Nothing was reverted; nothing was written before the measurement. |
| 3 | `attempt-the-build` | **not entered** — the specs exist and the build is in the tree, which is the route's second pass. The atomic's `Fails when` row for exactly this says run 1, 2 and 4 only and claim no flip earned by the pass that built it. No flip is claimed as this pass's. |
| 4 | `re-run-the-harnesses` | ok — every recorded harness re-run with the same command line and the same `PEARDE_ROOT`, plus the checkout root for the red side. No count dropped; none rose. |
| 5 | `write-the-specs` | applied as the implementer's pass, no spec authored — the `Fails when` table run over the standing block. The block parses, exits 0 with the build and non-zero without it, spells its footprint path literally, and gates on no board-wide command. Boxes ticked against quoted output. |

### Edits

One, on the `write-the-specs` atomic. Step 5 item 4 says:

> Where the block invokes the tool by a path relative to the root — `python3
> resources/<mod>.py` — running it from the checkout runs the checkout's copy,
> not your lane's, and the exit says nothing about your build. Substitute the
> module path, not the root: run from the checkout with
> `s#resources/<mod>.py#<lane>/resources/<mod>.py#`, and run the block verbatim
> as well.

"Substitute the module path, not the root" is wrong for the commonest shape on
this board. A block whose lines are `bash "$B/prds/<prd>/probe/verify.sh"`
invokes no module: the harness resolves the tree itself, from `PEARDE_ROOT`,
and there is no module path in the block to substitute. Rewriting the harness
path would point at a different harness, not at a different tree. The root
substitution the atomic warns against is the only one that works here, and it
is not a rewrite of the block at all — it is an environment variable on the
run, so the block is still verbatim.

Replacement text for that paragraph:

> Where the block invokes the tool by a path relative to the root — `python3
> resources/<mod>.py` — running it from the checkout runs the checkout's copy,
> not your lane's, and the exit says nothing about your build. Substitute the
> module path, not the root: run from the checkout with
> `s#resources/<mod>.py#<lane>/resources/<mod>.py#`, and run the block verbatim
> as well. Where instead the block runs a **harness** that resolves the tree
> itself from `PEARDE_ROOT`, there is no module path in the block to
> substitute and rewriting the harness path would name a different harness, not
> a different tree: run the block verbatim under `PEARDE_ROOT=<lane>`, which
> leaves the block untouched, and verbatim with `PEARDE_ROOT` unset as well.
> Verbatim it must FAIL before the merge — that failure is the red-to-green
> flip shown against the tree that does not hold the build, and it is stronger
> evidence than `git show HEAD:`, because the whole gate ran on the old file.

No other atomic misfired. Step 1's template-body row, step 3's second-pass row
and step 4's lane-behind-the-checkout row each named this run's shape exactly
and needed nothing.

## Scores

complexity: 9
blast-radius: mid
workflow: probe-then-spec
