---
state: "specced"
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
wave: 1
date: "2026-09-15"
footprint:
- ".cartridge/memos/**"
- "prd.ctg/.cartridge/memos/**"
---

# The record has one vocabulary and no shadowed copies

## Outcome

The workspace record declares every kind once (memo.ctg `type/`), carries no memo describing a runtime that is not here, and shadows no shipped memo.

## Acceptance

- [x] Deleted: `type/prd.md` and `prd/*` (their two items live on this board as host-tests-hold-under-suite-contention and ci-runs-the-gates-on-macos-and-linux), `routine/terminal.md`, `routine/terminal-control.md`, `routine/neovim-control.md`, `note/release-{baseline,status,state,checkpoint}.md`.
- [x] `@prd/decision/memory--the-pearde-workflow-is-the-work-record.md` and `@prd/decision/memory--new-work-is-on-the-plan-by-default.md` no longer say a work memo is the PRD; `@prd/routine/root--drill.md` is the only drill routine in any composed record.
- [x] `cartridge call memo '{"op":"index"}'` lists no shipped memo shadowed by a workspace leaf; one `routine/hygiene.md` pass runs clean and its evidence line is in Result.

## Result

2026-09-15, worked by a dispatched analyst/implementer and checked by an
independent verifier. All three boxes are observed green. Not collected:
`prd collect` refuses while the composed root's working tree carries other
sessions' uncommitted submodule work, which is recorded on the board as its own
blocker.

### Box 1 — deletions: green

Twelve memos gone from `.cartridge/memos/`: `type/prd.md`, `prd/` (both of its
items, `the-binary-target-passes-on-a-runner.md` and
`the-windows-runner-gates-again.md`, and the directory), `routine/terminal.md`,
`routine/terminal-control.md`, `routine/neovim-control.md`,
`note/release-{baseline,status,state,checkpoint}.md`, and the two shadowing
leaves `type/note.md` and `type/type.md`. `type/prd.md` and `prd/*` were
untracked, written 09:17 the same morning, so git holds no record of them; their
two items are on this board as `host-tests-hold-under-suite-contention` and
`ci-runs-the-gates-on-macos-and-linux`. Verified from the filesystem:

```
$ cd /Users/feb/dev/cartridge && bash <the spec01 Verify and Proof block>
spec01 OK
EXIT=0
```

### Box 2 — one vocabulary, one drill: green

Both named decision memos were read in full by the verifier. Every sentence
that made a work memo the PRD is gone: the port row `a PRD, prd.md … | a work
memo — ## Do is the contract` became `not ported: the PRD is still prd.md, and
## Outcome is its contract`, the spec row lost `the work-memo note`, `A work
memo waiting on a question…` became `A PRD waiting on a question…`, and both
`description:` lines now open with `superseded —`. The port table is rewritten
rather than removed: the rows that do not equate the two are the record of what
was not ported.

```
$ grep -n 'work memo' prd.ctg/.cartridge/memos/decision/memory--the-pearde-workflow-is-the-work-record.md \
                      prd.ctg/.cartridge/memos/decision/memory--new-work-is-on-the-plan-by-default.md
(no output, exit 1)

$ find <the workspace record and every composed cartridge's record> -path '*/routine/*drill*' -type f
/Users/feb/dev/cartridge/prd.ctg/.cartridge/memos/routine/root--drill.md
```

The only other `*drill*` memos anywhere are `memory.ctg/.cartridge/memos/system/drill.md`,
which `.cartridge/init.lua` does not compose, and a `decision` and a `grammar`
in prd.ctg, neither of which is a routine.

### Box 3 — `memo index` and a hygiene pass: green, later the same day

Cleared once the composition could start. The blocker was never this record:
`prd.ctg/cartridge.json` still declared `needs: ["memory"]` after the profile
stopped composing memory, so `prd` failed at load and `memo` stalled behind it.
That is its own item, `the-composition-comes-up-without-memory`. With it fixed
and the host started by this session:

```
$ cartridge call memo '{"op":"index","cwd":"/Users/feb/dev/cartridge"}'
```

Thirteen kinds. Eleven are declared by exactly one workspace leaf and no
shipped copy. Two, `note` and `type`, are declared only by shipped memos, 12
each, which is what deleting the two workspace leaves was for. No kind is
declared by both a workspace leaf and a shipped memo, so nothing is shadowed:

```
decision   workspace=1 shipped=0     note       workspace=0 shipped=12
grammar    workspace=1 shipped=0     type       workspace=0 shipped=12
persona    workspace=1 shipped=0     principle  workspace=1 shipped=0
question   workspace=1 shipped=0     resolver   workspace=1 shipped=0
resource   workspace=1 shipped=0     routine    workspace=1 shipped=0
scope      workspace=1 shipped=0     system     workspace=1 shipped=0
usage      workspace=1 shipped=0
SHADOWED KINDS: none
```

The box's command does not work as literally written. `memo.ctg/src/service.rs:455`
requires a native memo request to carry `cwd` and answers `trusted memo cwd
required` without it, so `cartridge call memo '{"op":"index"}'` fails on any
host. The working form adds `"cwd":"/Users/feb/dev/cartridge"`. The box should
be reworded to the call that exists.

### What was tried while the composition was down

Before the composition could start, the named command failed three different
ways from `/Users/feb/dev/cartridge`, none of them about this record:

```
$ ./cartridge.ctg/target/debug/cartridge call memo '{"op":"index"}'
unknown token
EXIT=1

$ ./cartridge.ctg/target/debug/cartridge run memo '{"op":"index"}'
/tmp/cartridge-501/69a3b8e0c7a1/host.sock is already served
EXIT=1
```

and then `adapter i/o: Connection refused (os error 61)`, the socket file still
present with nothing listening. Pid 92897 had died and left its socket behind.
Removing that stale file and starting a fresh host showed the real cause, which
was the unsatisfied `memory` declaration above, not authentication.

The substance of the first clause was also checked on disk, over every
cartridge `.cartridge/init.lua` composes, including the two nested `live.ctg`
entries: zero workspace leaves share a `<kind>/<name>.md` path with a shipped
memo. That is check 2 of the spec block, and it agrees with the index.

The `routine/hygiene.md` pass: probe (d), the duplicate-claim probe, found
`type/note.md` and `type/type.md` carrying the same claim as `@memo/type/*` and
is clear after the deletion — `grep -h '^description: ' .cartridge/memos/*/*.md
| sort | uniq -d` returns nothing. Probes (a), (b), (c) and (f) have no surface
in this record: `memos/intake/`, the `code-fact`, `knowledge` and
`documentation` kinds and `.kern/data/reflex.json` are all absent. Probe (e) is
uncalibrated here and answers 200-plus of 377 memos unreachable, which the
routine's own note calls the probe failing rather than finding.

### A defect the verifier caught, and the repair

The implementer deleted `type/note.md` and `type/type.md` on the stated premise
that the shipped copies are byte-identical. They are not. The twelve shipped
copies are identical to each other and different from what was deleted: the
workspace `type/type.md` carried the memo file contract and the whole
qualified-versus-bare wikilink resolution rule, and memo.ctg's declaration is
one sentence. Two grammars cited that file as the authority for the file
contract, so the deletion left them pointing at a stub that no longer holds the
text. The contract now lives in `grammar/memo-grammar.md`, which is what a
grammar is for, and `grammar/record-grammar.md` cites the grammar instead of
the stub. Check 5 of the spec block fails if either regresses.

### Scope

Every changed path is inside the footprint and named in the spec. The five
edited workspace memos outside the deletions are wikilink repoints plus this
contract repair. No file outside the spec footprint was touched, and no link in
either record now names a leaf the deletions removed.
