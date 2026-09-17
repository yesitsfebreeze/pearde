---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
capability-owner: mcp
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "mcp.ctg"
- "mcp.ctg/src/service.rs"
- "mcp.ctg/src/lib.rs"
- "mcp.ctg/cartridge.json"
- "mcp.ctg/.cartridge/tests/unit/tests.rs"
- "mcp.ctg/.cartridge/tests/integration/instances.test.ts"
- "cartridge.ctg"
- "cartridge.ctg/src/cli/host.rs"
commit: "805efec546a02e78224c92e3de02ca8a8c40e6e6"
---

# MCP keys sessions and inflight calls by attached instance

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies mcp stdio clients and
in-flight calls as per-instance state keyed inside the shared cartridge: mcp
keeps one `session` and one `inflight` map per node today
(`mcp.ctg/src/service.rs:100-113`), so two attached stdio clients would share
one session and one call set.

## Outcome

The one mcp node keys its `session` and `inflight` maps by attached instance
(the connected stdio client), so two attached MCP clients keep separate
sessions and separate in-flight calls, while the node itself exists once.

## What changes

- `session`/`inflight` maps become keyed by instance id (the connection), not
  one entry per node.
- Session lifecycles: **not in this slice** (round 1, F3). The bridge sends no
  `closed` event today, so nothing can be dropped or cancelled on disconnect.
  What this slice delivers is isolation while attached: one instance's session
  and in-flight calls are neither visible to nor disturbed by another's. The
  cost is one small map entry per bridge that ever attaches — the same trade
  the done sibling `agent-runs-key-per-attached-instance-not-per-process` took.
  A `closed` event and real teardown are their own PRD.

## Acceptance

- [x] Two `cartridge mcp` stdio clients attached to one daemon keep separate
      sessions (each sees only its own initialization and history), and one
      closing does not affect the other's session or calls.
- [x] An in-flight call from one instance is not visible in or cancellable
      from the other.
- [x] Exactly one mcp node exists with the daemon running, proven at composed
      scope inside this PRD's own fixture: with two bridges attached to one
      daemon, `instances.test.ts` asserts that `status` lists exactly one `mcp`
      node in state `active`, and that the run directory holds exactly one pid
      directory containing exactly one `mcp.sock`. Structurally, mcp.ctg starts
      no host, node or child process of its own — a standing property, guarded
      against regression rather than introduced here. For the live project,
      the daemon-wide count is delivered by the done sibling
      `an-instance-attaches-to-the-daemon-and-never-composes-silently` and
      re-proven composed by
      `the-composed-acceptance-test-proves-one-daemon-one-node-per-cartridge-and-attached-instances`,
      which is still `open` — that re-proof has not landed yet.

## Landing blocker (observed 2026-09-17, coordinator cartridge-fa)

The work is written but unlanded, and three separate facts in the shared
checkout keep it that way.

1. The implementation exists only as two commits no branch points to:
   `mcp.ctg` `ad9a28e` "Key every client's session and in-flight calls by
   attached instance" (on `345871e`, touching `src/service.rs`, `src/lib.rs`,
   `cartridge.json`, `.cartridge/tests/unit/tests.rs` and a new
   `.cartridge/tests/integration/instances.test.ts`), and `cartridge.ctg`
   `f445f60` "Name the instance every mcp bridge speaks for" (on `04aae7f`,
   16 lines in `src/cli/host.rs`). A duplicate of the mcp commit exists as
   `7a72f42`; the two differ only in `instances.test.ts`. None of this is in
   either submodule's working tree: `mcp.ctg/src/service.rs` contains no
   occurrence of `instance`, and `mcp.ctg/.cartridge/tests/integration/instances.test.ts`
   does not exist.
2. Neither commit can be replayed onto its submodule's current head without
   overwriting another session's uncommitted work in the same files.
   `mcp.ctg/.cartridge/tests/unit/tests.rs` carries three foreign added lines
   (an `#[ignore]` on the stdio fixture) and `ad9a28e` rewrites that file.
   `cartridge.ctg/src/cli/host.rs` is foreign-dirty and `f445f60` edits it.
   `cartridge.ctg` has also moved on from `04aae7f` to `63ff234`, which is not
   an ancestor of `f445f60`, so that commit needs a rebase as well.
3. `prd collect` cannot run against this PRD's `repo` at all while the
   superproject index holds another session's staged rename of
   `.cartridge/tools/pi-voice` to `.cartridge/tools/live`. The engine answers
   `repository has staged changes; preserve them before collection`, which is
   repository-wide rather than footprint-scoped.

The ticked Acceptance boxes above record proof observed against the work in
those commits, not against the current tree. They are left as they are because
the evidence was real; what is missing is the landing, not the proof.

Clearing this needs the owner of the uncommitted work in `mcp.ctg` and
`cartridge.ctg` to commit or set it aside, and the staged superproject rename
to be committed or unstaged. After that the two commits rebase onto the current
heads and the PRD collects.

Ownership established 2026-09-17 by asking the two live peer sessions directly.
Neither `cartridge-1c` nor `cartridge-8e` owns the staged
`.cartridge/tools/pi-voice` rename or the 44 uncommitted lines in
`cartridge.ctg/src/cli/host.rs`; both report the work as the user's own,
already staged before either session began, and `cartridge-8e` says the user
had said they would commit it themselves. `cartridge-1c` has put the rename to
the user and will report when it clears. So this is a user-owned external
blocker, not a coordination failure between sessions, and the PRD waits rather
than being worked around.

Update, later on 2026-09-17: blocker 3 is cleared. `cartridge-1c`'s user
authorised the rename and it is committed as superproject `89522e3`, so the
index is clean and `prd collect` no longer refuses repository-wide. Blockers 1
and 2 stand unchanged: the implementation is still only in `mcp.ctg` `ad9a28e`
and `cartridge.ctg` `f445f60`, and neither replays onto its submodule's head
while `mcp.ctg/.cartridge/tests/unit/tests.rs` and
`cartridge.ctg/src/cli/host.rs` carry the user's uncommitted work in the same
files. Landing the mcp half alone would not satisfy the PRD, because the
bridge must name its instance in `host.rs` for the node to key anything by it.

Update, 2026-09-17, coordinator cartridge-24: **the landing blocker above is
fully cleared and its account of where the code lives is now out of date.**
Blockers 1 and 2 are gone — both submodules were clean, and `attempt-2.patch`
applied to their current heads with `git apply -p1` from the superproject with
offsets only (`tests.rs` +3, `host.rs` +35), no fuzz and no rejects. The
implementation is committed as `mcp.ctg` `ec4de01` (parent `f302ca0`) and
`cartridge.ctg` `4b607ea` (parent `57abb99`). The dangling `ad9a28e` /
`f445f60` / `7a72f42` commits are superseded and no longer the only copy. What
remains is not a landing blocker but a missing assertion; see "Box 3 unticked"
at the end of this file.

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. Unlike the sibling
`agent-runs-key-per-attached-instance-not-per-process`, **the audit premise
holds here**: `mcp.ctg/src/service.rs:100-113` keeps one `session` OnceCell,
one `inflight` map keyed by the client's own JSON-RPC id (every client counts
from 1, so two clients collide on `"1"`) and one `restored` set per node. The
analyst reproduced it live — two `cartridge mcp` children on one daemon both
echoed `session-1`.

`repo` moved from `mcp.ctg` to the superproject and the footprint was widened
across both submodules, because no instance identity exists anywhere today:
`cartridge mcp` sends `{"op":"message","line"}` only
(`cartridge.ctg/src/cli/host.rs:283-317`), the socket handler passes `data`
through verbatim, and stdio MCP carries no session header. The key's only
possible producer is the bridge, in `cartridge.ctg`. This is not a SPLIT — the
bridge's id has no consumer without the node, and the node's keying is
unobservable without the bridge — so it lands the established superproject way:
commit inside each submodule, bump the pointers, collect against the
superproject. Both submodules were clean when the footprint was widened; check
again before collecting, because the `cartridge.ctg` and `mcp.ctg` directory
entries make collect sweep everything inside them.

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, after reviewer-4 (round 4, PASS 95) and
verifier-1.

Boxes 1 and 2 were proven by execution in verifier-1: two real `cartridge mcp`
children with distinct, stable sessions, and two genuinely concurrent held calls
under the same JSON-RPC id 1 where a cancel reaches only its own context.

Box 3 is ticked on an assertion that **fails in the world it denies**, which it
took two corrections to reach. Round 3 found my earlier narrowing rested on a
false premise (the daemon-wide count *is* observable from this PRD's own
fixture). Round 3 then recommended `filter(n => n.id === 'mcp').length === 1` —
and the implementer found that this too cannot fail for the reason it claims:
with `{id="mcp",path="mcp"}` removed from the composition, `cartridge status`
still prints `{"id":"mcp",…,"state":"disabled"}`, because the entry comes from
the profile directory. Round 4 reproduced that independently. The shipped
assertion adds `&& node.state === 'active'`, which returns 0 in that world, plus
a `mcp.sock` route that fails there too.

The dead `run.length <= 1` check is **deleted**, not disclaimed: run directories
live at `base()/tag(descriptor)/<pid>` (`cartridge.ctg/src/host/socket.rs:46-84`),
never the project's `.cartridge`, so it looked where numeric entries cannot
appear.

Carried, non-blocking (F17): both boxes say "with two bridges attached" while the
assertion runs after `a.close()`. Step 6 and the code comment are accurate; the
box wording gets the one-line fix when the fixture is next touched.

## Box 3: unticked, then earned (2026-09-17, coordinator cartridge-24)

Box 3 is unticked, and so is the same box in `specs/spec01.md`. It was ticked on
an assertion that is not in the code.

`attempt-2.patch` had never been applied to this checkout. An implementer applied
it cleanly on 2026-09-17 (mcp.ctg `ec4de01`, cartridge.ctg `4b607ea`) and a fresh
verifier re-ran everything: all four Verify blocks exit 0, `just check mcp`,
`just test mcp` (22 passed, 0 failed, 1 ignored) and `just check cartridge` all
exit 0, and both commits touch exactly the six footprint paths. Boxes 1 and 2 are
proven by execution, as recorded above.

Box 3 is not. The committed `instances.test.ts` contains no `cartridge status`
call, no `cartridge socket` call, no `mcp.sock` check and no node-state filter —
`grep -n 'status\|socket\|mcp\.sock\|active\|dirname'` finds one hit, a comment
on line 85. Its entire one-node evidence is the
`readdirSync(composition).filter(/^\d+$/)` plus `toBeLessThanOrEqual(1)` pair at
lines 109-110, which is exactly the dead `run.length <= 1` check that the
"Evidence note for the ticked boxes" section above says is **deleted**. It is
vacuous for precisely the reason recorded there: run directories live at
`base()/tag(descriptor)/<pid>` under `$XDG_RUNTIME_DIR` or `/tmp/cartridge-<uid>`
(`cartridge.ctg/src/host/socket.rs:47-84`), never in the project's `.cartridge`,
so it evaluates `0 <= 1` whatever the node count is.

The implementer applied the patch faithfully; the patch is what is stale.
Round 3 and round 4 agreed on the corrected assertion, the spec's step 6 and box
3 describe it, and the "Evidence note" above records it as shipped — but it was
never written into `attempt-2.patch`, and no `attempt-3.patch` exists. The
record ran ahead of the code.

What is owed, and it is small: `instances.test.ts` must actually assert
`status.filter(n => n.id === 'mcp' && n.state === 'active').length === 1` and
that `path.dirname(<cartridge socket>)` holds exactly one pid directory
containing exactly one `mcp.sock`, and must delete the dead
`readdirSync(composition)` pair. That is already what spec step 6 and box 3
prescribe, so it needs no re-review.

Box 3's structural half — mcp.ctg starts no host, node or child process of its
own — was observed, by Verify block 4.

### Resolved, and re-ticked on observed evidence

The implementer wrote the assertion (mcp.ctg `9db553e`, parent `ec4de01`, one
footprint path) and a second verifier pass confirmed it independently.

The dead pair is gone: `grep -n 'readdirSync(path.join(composition))\|toHaveLength'`
finds no trace of the old bound, and the file now carries a `cartridge status`
call, a `cartridge socket` call, an `n.state === 'active'` filter and an
`mcp.sock` check — three `toHaveLength(1)` assertions, exact counts rather than
a `<=` bound. Verify block 3 exits 0 with 13 `expect()` calls, up from 9. Blocks
1, 2 and 4 exit 0, and `just check mcp`, `just test mcp` (22 passed, 0 failed,
1 ignored) and `just check cartridge` all exit 0.

The verifier reproduced three mutants itself rather than taking the
implementer's word, each in a scratch copy, with the restored copy returning to
green:

- `mcp` removed from the composition — exit 1. The failure message shows
  `{"id":"mcp",…,"state":"disabled"}` still present in the status array
  alongside three `active` nodes, `Expected length: 1 / Received length: 0`.
  This settles the question rounds 3 and 4 argued: a filter on `id` alone would
  have passed at 1, and `&& n.state === 'active'` is what fails it.
- the run directory pointed at the dead `.cartridge` location — exit 1, and the
  message proves that directory holds only `init.lua`, `config.lua` and
  `daemon.log`, which is why the old check passed at zero.
- `mcp.sock` deleted — exit 1, with the real pid directory left holding
  `policy.sock`, `sessions.sock` and `echo.sock`.

One caveat, recorded rather than smoothed over: the first mutant needed the
earlier initialize assertions short-circuited, because with no mcp node the
bridges never initialize and the fixture fails ~11.8 s earlier for a different
reason. The verifier hit the same wall independently, ruled the disclosure
honest, and noted that the other two mutants needed no scaffold at all. So
mutant 1 does not show that the unmodified test would fail *at the status
assertion* on a dropped node — it shows the assertion is load-bearing when the
bridges do work, which is the world box 3 describes.
