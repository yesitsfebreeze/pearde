---
state: open
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
- [ ] `cartridge call memo '{"op":"index"}'` lists no shipped memo shadowed by a workspace leaf; one `routine/hygiene.md` pass runs clean and its evidence line is in Result.

## Result

2026-09-15, worked by a dispatched analyst/implementer and checked by an
independent verifier. Two boxes are observed green; the third is open on a
blocker no session here may clear. Not collected.

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

### Box 3 — `memo index` and a hygiene pass: open, blocked

The named command cannot be run here. Two attempts, from
`/Users/feb/dev/cartridge`:

```
$ ./cartridge.ctg/target/debug/cartridge call memo '{"op":"index"}'
unknown token
EXIT=1

$ ./cartridge.ctg/target/debug/cartridge run memo '{"op":"index"}'
/tmp/cartridge-501/69a3b8e0c7a1/host.sock is already served
EXIT=1
```

The verifier, asking a few minutes later, got a third shape from the same
socket: `adapter i/o: Connection refused (os error 61)`, the socket file still
present and nothing listening. The cause is settled and is not a defect in this
record. The host on that socket is pid 92897, started 09:49 from a build older
than the working tree: its socket no longer writes the token file the command
line reads, and its authentication path predates the current one, so a client
built from this tree speaks a protocol it does not implement. `cartridge run`
then finds the address taken. Whoever owns pid 92897 must restart it against a
current build. No session here will stop a host it did not start, so this box
stays open and this PRD is not collected.

The substance of the first clause was checked on disk instead, over every
cartridge `.cartridge/init.lua` composes, including the two nested `live.ctg`
entries: zero workspace leaves share a `<kind>/<name>.md` path with a shipped
memo. That is check 2 of the spec block above, and it passes.

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
