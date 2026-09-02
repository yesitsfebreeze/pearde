---
state: done
origin: derived
priority: 92
complexity: 26
blast-radius:
from: every-task-is-a-verb-under-one-skill/the-machine-is-the-run-verb  # derived only — the PRD whose work surfaced this one
actual: 0.35h
---

# a verify block must not destroy the checkout it runs in

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Failure

The worker reported DONE, 22/22, `probe/verify.sh` 24 passed 0 failed. The
orchestrator does not believe it. The **mechanism is sound** — the merge
holds, the ordering inside `guarded_run` is carefully reasoned, the section-A
re-pin is right and survived an attempt to break it, and the E2 witness
genuinely fails without the snapshot. The **parsing is not**, and the code
that lands with it destroys other sessions' work. That is not a `done`.

First, the size: the change is **+288/−2, not the +116 the report claims**.
`spec01`'s entire guard — `_dirty`, `_park`, `_heal`, `_head_of`,
`_restore_head`, `owned_by`, `guarded_run` — is *also* uncommitted in this
lane; none of it exists at `e5abc5b`. This lands ~290 lines of new machinery
into the path every future `collect` runs.

The merged tree is fine, and that was checked rather than assumed: main never
touched `collect.py` since the lane base (`git diff e5abc5b fc75bcf --
resources/board/collect.py` is empty). Rebuilt from `fc75bcf` anyway — 24/24
on the merged tree, and 24/24 again with the guard committed, i.e. post-land.
Unlike the previous PRD, this one is not standing on a stale base.

### Blocking · 1 · `_dirty` does not unquote, and silently restores HEAD over the work

`_dirty` does `rest = line[3:]` on `git status --porcelain`. Git quotes any
path with a space or a non-ASCII byte, and `core.quotePath` is unset here, so
quoting is on. On `src/a b.py` — plain ASCII, one space:

    _dirty rows : [(' M', '"src/a b.py"'), (' M', 'src/plain.py')]
    'src/a b.py'   -> kind='blob'          <- misclassified
    OUT: ... put back: src/a b.py, src/plain.py
    after _unerase: 'src/a b.py' -> HEAD   <- the uncommitted work is gone

The quoted path never enters `moved`, so `_snapshot` calls it clean, holds the
index blob, and `_unerase` writes HEAD's bytes over the PRD's uncommitted work
— **while printing `put back:` as if it succeeded.** That is the exact loss
this PRD exists to prevent, dressed as a success line. The same bug reaches
everywhere: `_park` feeds the quoted string in as a pathspec and fails
(`fatal: pathspec … did not match any files`), returns `False`, and **the
whole block then runs unguarded** — one spaced foreign path disables the fence
for every foreign path; `_heal`'s `git checkout HEAD -- '"…"'` fails with its
returncode never checked and names the file as put back anyway; and
`inside(p, feet)` cannot match a quoted owned path, so an owned dirty file
with a space is parked as foreign and the block measures a clean HEAD — which
`spec01` itself names as the fatal failure.

Not live today (no path in either tree needs quoting) but latent forever, on
every board. **The fix is one line:** `git status --porcelain -z`, which never
quotes, or `-c core.quotePath=false`. Add a spaced-path case to `probe_unit`.

### Blocking · 2 · a peer's new file is destroyed outright

Live, not theoretical: the shared checkout has 24 dirty files from other
sessions right now, all foreign to this footprint, and `verify.sh` runs ~8s
per block. A peer write arriving inside that window:

    after the guard finishes:
      other/peer.txt      -> PEER EDIT BEFORE THE BLOCK  (their edit reverted)
      other/peer-new.txt  -> DESTROYED   (git clean -f -d; never in the stash)
    HEAL: ... put back: other/peer.txt, other/peer-new.txt

`_heal`'s `git clean -f -d` deletes a foreign untracked file created during
the window, the stash pop cannot bring it back, and the output claims it was
put back. `_heal`'s `git reset -q HEAD --` also wipes any index state a peer
staged. Several sessions writing one board is the documented working practice
on this machine. **`_heal` must move a foreign untracked path aside rather
than `clean -f -d` it, and must check the returncodes it currently swallows
before printing "put back".** Destroying a peer's new file is strictly worse
than the incident this PRD was filed to fix.

### Record, not necessarily fix · the filed incident is still not caught

`git reset --hard HEAD` — the harness's own `DESTRUCTIVE` constant, and the
incident in this PRD's title — on the laneless path:

    state: done | disk: "# empty" | COMMITTED: "# empty" | put-back lines: 0

The footprint is reverted to HEAD, `_unerase` sees the file present and does
nothing, the reverted content is committed, `done` is written, nothing is
printed. Section E only ever tests `rm -f`. `spec02`'s box reads "a green
destructive verify block, and the PRD's uncommitted footprint change is what
gets committed — not the deletion", and it is closed against the one
destructive shape the mechanism happens to catch. The spec does state
"modified stays modified" as a deliberate decision, but a revert-to-HEAD-blob
is *distinguishable* — the guard already holds the pre-block bytes — and it is
the headline case. **Either narrow spec02's wording to "a block that
deletes", or add the revert-to-blob case.** As written the box overclaims.

### Cheap and worth taking

Drop the hardcoded `cd /Users/feb/dev/infra/pearde` from both verify blocks.
At collect time `cwd` for a spec block is already `repo`, so the `cd` is a
no-op that buys nothing, and it is both a machine pin and the one documented
way to step outside the fence — `guarded_run` fences `cwd`, and any block can
simply leave it. No fixture block in the harness ever `cd`s.

Minor, undocumented and untested: `_owned_files` skips symlinks, so a
footprint symlink a block deletes is never restored — and this repo's
`.pearde` **is** a symlink.

### What is NOT the reason

The ordering inside `guarded_run` is correct and was checked: `_park` is
pathspec-limited so it cannot disturb the snapshot's subjects; snapshot-after-
park is right; `_restore_head` before `_heal` means `checkout HEAD` uses the
restored ref; `_unerase` after `_heal` means healing cannot re-delete a
restored path; `_unerase` before the pop means the pop sees the restored
files. The missing-blob path is handled with an explicit message. The verify
blocks' `cd` did **not** close the boxes against the wrong tree — all 24 were
re-run on the post-land merged tree and pass. The board has no `gate:` key in
its settings frontmatter, so the `index.py check` redness the report mentions
cannot block collection. Do not redo any of this.

One method note for the retry: the implementer's own runs used `PEARDE_ROOT`
at the lane, whose tree is 12 commits stale across `plan.py`, `guard.py`,
`index.py`, `doctor.sh` plus a new `prose.py`. It happened not to bite. That
is luck, not method.

## Report

spec01: exit 0
collect.py parses
1622:            code, output = guarded_run(["bash", "-e", "-o", "pipefail"],
7
no _foot_in left
A. reproduced at e5abc5b8729525f282364ea8e08f00fce98689c1: a GREEN verify block destroys the checkout
  ok   A1 the old collect exits 0 — the block never failed
  ok   A1 ...and the PRD is done
  ok   A1 the neighbour's uncommitted work is GONE
B. the same block, guarded: the checkout it did not own is untouched
  ok   B1 collect exits 0
  ok   B1 the PRD reaches done
  ok   B1 the neighbour's uncommitted work survives
  ok   B1 no stash is left behind
C. the board is its own repo: the block still sees the change under test
  ok   C1 collect exits 0 — the footprint was NOT parked
  ok   C1 the PRD reaches done
  ok   C1 the neighbour's uncommitted work survives
C. this repo's own roots: the footprint groups under the code repo
  ok   C2 this board's repo and board root really are two paths
  ok   C2 ...and the footprint groups under the code repo, unrebased
E. laneless: a green block deletes the PRD's own uncommitted footprint
  ok   E1 collect exits 0
  ok   E1 the PRD reaches done
  ok   E1 collect names the path it put back, on its own line
  ok   E1 the uncommitted footprint is back on disk, not deleted
  ok   E1 ...and it is the helper that got COMMITTED, not the deletion
  ok   E1 the neighbour's uncommitted work survives
E. the same fixture on spec01's collect: the deletion is what lands
  ok   E2 spec01's collect exits 0 — the block never failed
  ok   E2 ...and the PRD is done
  ok   E2 the work under test is GONE from the checkout
  ok   E2 ...and the deletion is what got committed
D. the unit probes
  ok   D probe_unit
  ok   D probe_roots

24 passed, 0 failed

spec02: exit 0
collect.py parses
A. reproduced at e5abc5b8729525f282364ea8e08f00fce98689c1: a GREEN verify block destroys the checkout
  ok   A1 the old collect exits 0 — the block never failed
  ok   A1 ...and the PRD is done
  ok   A1 the neighbour's uncommitted work is GONE
B. the same block, guarded: the checkout it did not own is untouched
  ok   B1 collect exits 0
  ok   B1 the PRD reaches done
  ok   B1 the neighbour's uncommitted work survives
  ok   B1 no stash is left behind
C. the board is its own repo: the block still sees the change under test
  ok   C1 collect exits 0 — the footprint was NOT parked
  ok   C1 the PRD reaches done
  ok   C1 the neighbour's uncommitted work survives
C. this repo's own roots: the footprint groups under the code repo
  ok   C2 this board's repo and board root really are two paths
  ok   C2 ...and the footprint groups under the code repo, unrebased
E. laneless: a green block deletes the PRD's own uncommitted footprint
  ok   E1 collect exits 0
  ok   E1 the PRD reaches done
  ok   E1 collect names the path it put back, on its own line
  ok   E1 the uncommitted footprint is back on disk, not deleted
  ok   E1 ...and it is the helper that got COMMITTED, not the deletion
  ok   E1 the neighbour's uncommitted work survives
E. the same fixture on spec01's collect: the deletion is what lands
  ok   E2 spec01's collect exits 0 — the block never failed
  ok   E2 ...and the PRD is done
  ok   E2 the work under test is GONE from the checkout
  ok   E2 ...and the deletion is what got committed
D. the unit probes
  ok   D probe_unit
  ok   D probe_roots

24 passed, 0 failed
PASS: unguarded, the block really does empty the checkout
PASS: foreign dirt survives a block that empties the checkout
PASS: own footprint left exactly as the block leaves it
PASS: `git reset --hard` + `git clean -fdx` undone, foreign dirt intact
PASS: nothing foreign — no stash left behind
PASS: git reads inside the block see the real tree
PASS: without the snapshot the block loses the work under test
PASS: a deleted owned file comes back, bytes and mode, both branches
PASS: an owned file the block MODIFIES stays modified
PASS: an owned file the block CREATES stays created
PASS: a deletion the worker made before the block stays deleted
PASS: a directory footprint: a file deleted from inside comes back
PASS: every restored path is named on collect's own output line
ALL PASS
