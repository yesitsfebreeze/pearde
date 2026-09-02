---
complexity: 9
footprint:
  - resources/board/collect.py
---

# spec01 — nothing raised between the done write and the commit tears the board

`collect_one` writes the record — `actual:`, the claim deleted, `state: done`
— then calls `post_report`, then commits. `post_report` guarded only
`urllib.error.URLError, OSError, ValueError`, which is not the set a live
socket can raise: a port held by something that is not this daemon answers
with `http.client.BadStatusLine`, a daemon killed mid-write with
`IncompleteRead` — both `HTTPException`, neither an `OSError` — and a
`/status` of another shape raises `AttributeError` or `KeyError` off the
parse of `boards`. Each of those raised straight through `collect_one` and
left `prd.md` saying `done`, with no claim, no `commit:`, and no commit in
any repo: the PRD finished on the board and unfinished in git, which the next
scan reads as landed work. `close_container` had the identical window.

This unit makes `post_report` total — every failure a returned phrase the
progress line carries, none of them an exception — and wraps the window in
both call sites so that whatever is put there later, a raise puts `prd.md`
back byte-for-byte and refuses with `Stop` rather than escaping as a
traceback.

**What already stands.** All of it: `resources/board/collect.py` in the lane
carries the widened `post_report` and both `try/except BaseException` guards,
and `probe/verify.sh` is 75 checks · 75 pass · 0 fail, with every check first
reproduced red against the pinned pre-fix `collect.py` at `58c92e6`.

**What is left to finish.** Nothing but landing the hunk. An implementer
picking this up re-runs the verify below and the collect harnesses named in
it, and accounts for any count that moved.

## Acceptance

- [x] `post_report` returns a phrase and raises nothing for all four live-but-wrong daemons the probe stands up — non-HTTP bytes on the wire, a truncated `/report` body, a `/status` that is a JSON list, and a `boards` row with no `path` key
- [x] a collect against each of those four exits 0, prints no traceback, says `not posted` on its progress line, and leaves the record `done` with a `commit:` and two commits on the branch
- [x] a daemon that answers correctly is still posted to — the line says `report posted`
- [x] an exception raised inside the window from anywhere — `probe/inject.py` replaces `post_report` with a bare raise — exits 1 as a refusal, prints no traceback, names what raised, and leaves `prd.md` byte-identical to what it was with nothing committed
- [x] `close_container` is guarded the same way: the wrong-daemon collect of a container exits 0 and lands one commit, and the injected raise puts the parent's `prd.md` back whole
- [x] the three committed collect harnesses that were green before — `the-tool-keeps-its-word/collect-keeps-its-word`, `the-board-runs-itself/collect-is-a-command`, `collect-must-not-reset-the-checkout-it-did-not-write` — stay green, and `collect-stages-a-shared-file-whole` goes from 25 pass / 7 fail to 32 pass / 0 fail, because its 7 failures were this crash against the live daemon

## Verify and Proof

```sh
B="$(git rev-parse --show-toplevel)/.pearde"   # every fixture below is mktemp
bash "$B/prds/post-report-crashes-a-collect-between-the-done-write-and-the/probe/verify.sh"
bash "$B/prds/collect-stages-a-shared-file-whole/probe/verify.sh"
bash "$B/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh"
```
