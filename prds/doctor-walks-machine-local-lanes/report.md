Verdict: SPECCED

# doctor-walks-machine-local-lanes

Doctor gains a `lanes` row: it walks every worktree under `<board>/.lanes/`
on this machine and names the ones that cannot reach the board — the same
class of silent break the deferred `a-session-worktree-lacks-the-pearde-
symlink-a-lane-gets` documents for session trees, but hitting lanes too.
Measured live: **7 of the 45 real lanes on this board have no working link
to `.pearde`**, including this PRD's own lane (fixed by hand during the
probe, since a working lane was needed to build in).

## What the build found (root cause, out of this footprint)

Two distinct, still-live causes, both silent today:

1. **A session-nested repo defeats `board_rel`.** `collect.repo_of` swaps
   the claiming repo for the running session's own worktree once one is
   held (`session.instead_of`) — and a session's worktree lives INSIDE the
   board, at `<board>/.sessions/<id>`. `lanes.py`'s `board_rel(board, repo)`
   answers `None` whenever `os.path.relpath(board, repo)` starts with
   `..`, true for a genuinely unrelated repo and also true here, where
   `board` is `repo`'s ancestor rather than the reverse. `link_board`
   returns `None` on that and never symlinks. Reproduced directly against
   today's `resources/board/lanes.py`:
   `board_rel('/…/.pearde', '/…/.pearde/.sessions/s85810')` → `None`.
2. **A stale lane never gets retrofitted.** `create()`'s idempotent path
   (an existing worktree dir) returns early without ever calling
   `link_board` again, so a lane cut before that function existed in the
   checkout's own history — or one whose link was lost some other way —
   stays broken across every future re-claim.

Filed as a knowledge note (`260904-4a41`) rather than a spec or a new PRD —
fixing `board_rel`'s direction, or making reuse re-link, widens this
contract past what "doctor walks machine local lanes" asks for. `doctor`'s
new row reports and repairs the symptom regardless of which cause produced
it; the causes are a fix for whoever picks up that knowledge note next.

## Built and proven

- `resources/board/lanes.py`: `check(board)` (one `"<slug>: no link to the
  board"` line per lane whose top level holds nothing that resolves to the
  live board) and `relink(board, slug)` (places a symlink named after the
  board at the lane's root, refuses rather than overwrite when something
  else is already there).
- `resources/doctor.sh`: a `lanes` row, board-scoped like `health` — `ok`
  with the lane count, `broken` with one line per name `check` returns.
  `--fix` calls `relink` per broken name and reports `relinked` or
  `refused — something else is already there`; a plain run without
  `--fix` only ever prints the advisory `fix:` line, matching every other
  row's convention.
- Probe at `.pearde/prds/doctor-walks-machine-local-lanes/probe/verify.sh`
  — a throwaway-board fixture (three lanes: no link, real content in the
  way, already linked) exercising `check`/`relink` directly, then the same
  fixture through `doctor.sh` and `doctor.sh --fix`, then a re-run
  confirming the refused lane is still (correctly) named. `ALL OK` from
  this lane's checkout.
- Run against the real board too (not part of the probe, since the real
  lane count moves under concurrent sessions): `bash resources/doctor.sh
  .pearde` reported `7 of 45 lane(s) cannot find the board`; `--fix`
  relinked the ones nothing occupied and refused on the ones that already
  held real content (one lane held a stray `graphify` cache at the
  board's name — left untouched).

Workflow followed: `probe-then-spec` (used 77 times, most recent in the
library; `implement-a-spec` and `write-the-specs` are its steps, both
already in the library — no new atomic).

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
