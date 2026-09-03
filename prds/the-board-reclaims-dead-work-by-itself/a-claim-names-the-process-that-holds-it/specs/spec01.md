---
complexity: 20
footprint:
  - resources/board/prdfile.py
  - resources/board/silence.py
  - resources/board/transitions.py
  - resources/board/plan.py
---

# spec01 — a claim names the session, and `silent_of` asks it before the clock

`resources/board/session.py` already knows whether a process is alive, dead
or unknown — the pid-reuse guard included — but nothing before this wrote a
claim that named a process at all: `claim: <worker> <since>` said only who
and when. This spec threads a session id through the whole path: `pearde
claim` writes it, `prdfile.claim_of` parses it back, and `silence.silent_of`
— the one rule the scan line, the page's row and `sweep` all read — asks the
session ledger for that id's liveness before it ever looks at a file's
mtime.

**This already stands**, built in this session's own tree and measured by
the probe at
`prds/the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it/probe/probe.sh`
(run through the committable wrapper at
`prds/the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it/verify.sh`)
— 17 assertions, green, `PROBE probe: 17 pass, 0 fail`. What is left for an
implementer is landing the four files on the branch a person reads; nothing
in this spec is unbuilt design.

**The claim's shape.** `transitions.claim_value(worker)` writes
`<worker>@<session> <since>` when this process runs inside a session —
`session.my_id()`'s own spelling, `s<pid>` — and `<worker> <since>` with no
session when it does not, exactly the shape every claim wrote before this
existed. `prdfile.claim_of` parses either back: the timestamp is pulled out
first by the existing `CLAIM_TS_RE`, then a trailing `@s<digits>` on what is
left is the session, anchored to the very end so a worker name that happens
to hold an `@` of its own — an email address — is left whole. Measured
against six shapes, including one two `@`s deep (`a@b@s9`) and one that is
an address and carries no session at all (`mail@example.com`): every one
parses to the `{who, since, session}` the table names.

**`silent_of` asks the session first.** `silence.session_liveness_of` builds
`{"pid": <the claim's pid>, "started": <the ledger row's, if one exists>}`
and calls `session.liveness` on it — the same three-valued rule `session.py`
already uses to decide whether `reap` may touch a worktree. `dead` — the pid
is gone, or a different process now holds it — is silent at once, whatever
the mtime says: measured, a claim taken seconds ago against a killed pid
reads `silent 0m`, never waiting out `claim-ttl`. `alive` — the pid is
running under the start time the ledger recorded — is never silent, however
long the tree has sat: nothing here reaps a worker that is merely reading
before its next edit. `unknown` — no session on the claim, or `ps` refusing
to answer, or a live-looking pid with no recorded start time to check it
against — is the ttl rule exactly as it stood before this spec: measured, a
running pid with no ledger row is not swept while its claim is fresh.

**A stale pass file no longer shields a dead session.** `sweep_rows` already
lets `prds/.pass.md` keep a live worker's claim off `--apply`'s table; that
shield now stands down when the session ledger already says the holder is
dead, because a name in a file a dead process wrote is not a second vote —
measured: a claim named in a fresh `.pass.md` is still swept the moment its
session reads dead.

**`## Failure` says which happened.** A `claimed` PRD `--apply` fails now
carries "the session holding this claim is gone" when the sweep fired on a
dead session, and the previous "no file of this PRD's moved past
`claim-ttl`" only when it fired on the plain clock — measured on both paths.

**Constraint already met.** The lane is committed before its worktree is
dropped: `sweep`'s own `drop_lane` already ran `commit_all` before `remove`
before this spec touched anything, so the faster reclaim this spec adds
never widens the window in which uncommitted work could be lost — measured:
a file written into a dead claim's lane and never committed by the worker is
on `lane/<prd>` after `--apply`, and the worktree is gone.

**Found, not fixed** (this PRD's footprint does not reach it):
`prds/an-unknown-flag-refuses/probe/verify.sh:140` reads a claim's raw
frontmatter and cuts the first whitespace-separated field, asserting it
equals the bare worker name. Run this probe inside a live session — the
ordinary way a person or an agent runs it — and that assertion now sees
`w1@s<pid>` instead of `w1`, because the claim it wrote really does carry a
session id, by design. The fix is `prdfile.claim_of(...)["who"]`, not a raw
cut, and it belongs to whoever owns that PRD.

## Acceptance

- [ ] `prdfile.claim_of({"claim": "w 2026-09-03 12:00"})` returns
  `{"who": "w", "since": "2026-09-03 12:00", "session": ""}`
- [ ] `prdfile.claim_of({"claim": "w@s123 2026-09-03 12:00"})` returns
  `{"who": "w", "since": "2026-09-03 12:00", "session": "s123"}`
- [ ] `prdfile.claim_of({"claim": "mail@example.com 2026-09-03"})` returns
  `{"who": "mail@example.com", "since": "2026-09-03", "session": ""}`
- [ ] a claim taken with `PEARDE_SESSION_PID` set writes `claim: <worker>@s<pid> <since>` to `prd.md`
- [ ] `sweep` reports a claim `silent 0m` — not after `claim-ttl` — when its session's pid is dead
- [ ] `sweep` does not report a claim silent when its session's pid is alive, however old the claim's mtime
- [ ] a `.pass.md` naming a claim does not shield it from `sweep --apply` once its session reads dead
- [ ] `sweep --apply` on a `claimed` PRD with a dead session appends a `## Failure` line containing `the session holding this claim is gone`
- [ ] `sweep --apply` commits every uncommitted lane path to `lane/<prd>` before the worktree is removed, for a claim released by a dead session

## Verify and Proof

```sh
set -e -o pipefail
ROOT="$(git rev-parse --show-toplevel)"
python3 -m py_compile resources/board/prdfile.py resources/board/silence.py \
  resources/board/transitions.py resources/board/plan.py
out=$(PEARDE_ROOT="$ROOT" bash "$ROOT/.pearde/prds/the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it/verify.sh" 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out" | tail -5
[ "$rc" = 0 ]
printf '%s\n' "$out" | grep -E '^probe: [0-9]+ pass, 0 fail$'
```
