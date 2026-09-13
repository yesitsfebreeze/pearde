# TypeScript native PRD: bounded independent review

Snapshot: 2026-09-13 09:26 UTC. Reviewed six copied TypeScript modules using
Bun 1.3.14. The owning session is actively changing the implementation; these are
findings about the identified snapshot, **not a final release verdict**.

Owner: `Analyze plan rating`, thread `01a097e6-4d34-7390-b55f-23792b974627`, as
identified by the coordinator. No TypeScript source or live board was changed by
this reviewer. The probe created only temporary fixture records and processes;
its surviving fixture child was killed after observation.

See [coordination and ownership](native-rewrite-coordination.md) and
[the parity acceptance handoff](native-rewrite-review-handoff.md).

## Five reproduced issues

### 1. Completed process result can leave an owned descendant running

`src/process.ts`, `runProcess`: a Python fixture leader starts a same-group child
that ignores TERM, then exits zero. Its child redirects all streams away from the
leader's pipes. The function returns `state: completed`, `exit_code: 0`, while
`process.kill(childPid, 0)` confirms the child remains alive. The normal-close path
sends TERM once and never waits for group termination or escalates. Cancellation
also clears its scheduled KILL if the leader closes first.

Drain the entire owned group with a finite TERM/KILL budget before returning a
confirmed outcome. Preserve an explicit uncertain-cleanup outcome when that
cannot be established. Test both normal leader exit and cancellation with a
TERM-ignoring descendant.

### 2. A board of unverified done records is reported completed

`src/coordinator.ts`, final result: a fixture board containing one `state: done`
PRD with no commit or collection receipt returns:

```json
{"status":"completed","completed":[],"failed":[],"remaining":[]}
```

`plan` filters done records out, and the coordinator treats an empty remaining
plan as proof that the scope is complete. Validate every in-scope done record,
including records that predate this run, before reporting completion. Persist and
report each invalid receipt. The shared completion validator must also validate
child contracts recursively and bind all current specs to the receipt; filtering
the plan cannot substitute for this proof.

### 3. Finished claimed leaves cannot reach coordinator collection

`src/planner.ts` and `src/coordinator.ts`: a claimed leaf with all acceptance boxes
closed and an executable verification block produces:

```json
{"state":"claimed","collect":true,"dispatchable":false,
 "held":"unclaimed: held by worker","role":"implementer"}
```

The dispatch loop skips every non-dispatchable row. A returning implementation
worker that leaves its legitimate claim also becomes a failure rather than a
verified collection candidate. Thus the normal claim → implement → coordinator
collect path stalls unless workers bypass the intended ownership protocol.

Give collection its own eligibility and role, distinct from claiming new work.
After the owned worker finishes, require independent verification and permit the
coordinator to collect its authorized result. Preserve foreign claims and do not
make all claimed records generally dispatchable.

### 4. Plan addresses do not round-trip through read

`src/planner.ts` emits `addr: @root/root-task` for a root-owned PRD. Passing that
address to `execute('read', rootBoard, ['@root/root-task'])` returns exit 2:

```text
PRD missing, ambiguous, or outside this graph: @root/root-task
```

`records.resolve` expects the bare root-local key; the prefix is added only by the
plan renderer. Emit an accepted canonical address, or resolve the selected board's
own alias consistently. Test every address returned by a root/member plan against
read and dry claim.

### 5. Creating a sub-PRD under a member parent fails containment

`src/lifecycle.ts`, add: root board has member `member` and PRD
`@member/parent`. `execute('add', rootBoard, ['New child', '--parent',
'@member/parent'])` returns exit 2:

```text
path escapes its board or repository
```

The parent resolves into the member board, then `contained(board, ...)` checks it
against the root board directory. Resolve the parent once and use its owning
board for containment, its code repository for inheritance, and its full local
parent/child identity for the journal and result. The current add path also reads
the root board's default repository rather than inheriting the resolved parent's.

## Reproduction and snapshot identity

The self-contained probe and six copied source modules are retained at:

```text
/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-ts-review-qjbii7he/
```

`probe.ts` demonstrates all five cases and creates a fresh temporary fixture
directory per run. To evaluate the owner's current implementation without
overwriting the frozen evidence, run from `prd.ctg`:

```sh
prd_review_dir=$(mktemp -d)
cp src/{records,planner,process,lifecycle,coordinator,engine}.ts "$prd_review_dir/"
cp /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-ts-review-qjbii7he/probe.ts "$prd_review_dir/"
bun "$prd_review_dir/probe.ts"
```

The probe prints observations, not assertions. After fixes, expect the descendant
to be confirmed stopped, the unverified done board to be refused, an authorized
collection path to exist, the plan address to read successfully and the sub-PRD
to be created under its owning member with the inherited code repository.

SHA-256 of the reviewed copies:

```text
records.ts     25f61981c59e04517a87f83655fa1ec5b861ff3401aa69ab71505ed63c5dd9bb
planner.ts     f4a4447efa66c886744332a80809636bc46d0c2730b1ad58a3d3af736acb0c0f
process.ts     db3734521b41edef84ac2184f5447d48467989400d9bc8d10e61be19d6d163db
lifecycle.ts   e8bc88fc852b0edbd739183208511e9c9c7a8e4eabeffc414dff42d78a94276d
coordinator.ts 3414b817509ad37fe70005f8435f3726d3542427f00f7ea91a8d915376cc28c4
engine.ts      f0a884ce3a3a3d9b0bb47a3808e9805c3268735551c28faca1e0c986c719ff29
```

This bounded pass does not replace the parity suite or final runtime, memory,
event and MCP integration verification. The TypeScript owner should resolve these
cases in its current branch and return the final revision and test evidence.
