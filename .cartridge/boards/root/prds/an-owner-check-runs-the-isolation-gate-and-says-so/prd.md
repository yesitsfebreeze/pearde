---
state: "open"
origin: derived
priority: 60
repo: "/Users/feb/dev/cartridge"
footprint:
  - ".cartridge/justfile"
  - ".cartridge/tests/integration/owner-check-isolation.test.ts"
---

# An owner check runs the isolation gate, and says so

## Outcome

`just check <owner>` runs the composition's isolation check as part of its
verdict, and the repository's own documentation says it does. A fixture that
reaches into a sibling cartridge fails an owner's check, instead of passing
every owner gate and breaking the build at composition time.

## Acceptance

- [ ] `just check <owner>` reports an `isolation composition` verdict alongside
      the owner's own targets, for any named target.
- [ ] A fixture reaching `../<sibling>.ctg` makes `just check <owner>` exit
      non-zero. One test proves it by constructing that fixture, running the
      gate and observing the exit code — not by grepping the justfile.
- [ ] The failure summary counts every verdict it printed, so "N of M targets
      failed" cannot report a smaller M than the number of lines above it.
- [ ] `just test <owner>` is unchanged, or the change is stated: this PRD is
      about `check`, and the two gates should not quietly diverge without a
      reason in the record.
- [ ] README.md and the development routine say what an owner check now covers.
      An instrument that silently does more than its name is the defect this
      PRD exists to remove, so leaving the documentation behind would reproduce
      it in a new place.

## Evidence

An uncommitted hunk implementing most of this behaviour has been sitting in
`.cartridge/justfile` in the shared checkout for at least a day. Inside `_fan`
it runs `just _one isolation composition` whenever `gate` is `check`, appends
that verdict, and changes the failure denominator from `${#targets[@]}` to
`${#verdicts[@]}`. Its comment states the reason: an owner's check never saw the
composition, so a fixture reaching a sibling passes every owner gate and still
breaks the build.

Nobody owns it, and the question is now closed. On 2026-09-19 the user said it
is not theirs; cartridge-5c, cartridge-eb and cartridge-1f each disclaimed it in
writing; cartridge-4b and cartridge-1f both found `.cartridge/justfile` already
listed as modified in their session-start snapshots, 1f's taken at 12:10Z before
it had touched anything. It appears in no commit touching `.cartridge/justfile`
and in no PRD body.

cartridge-eb, which read the recipe closely, confirms the substance
independently: an owner's `check` genuinely never sees the composition, and this
board carries a recorded case of a fixture reaching `../sibling.ctg` that passes
every owner gate and still breaks the build. It also makes the point that
belongs in the acceptance above rather than in an implementation note — the
denominator change is not cosmetic, because it changes what a partial failure
reports.

The hole it addresses is real and was recorded independently: `just check
<owner>` and `just test <owner>` never call `just isolation`, so a fixture
reaching `../sibling.ctg` collects green and breaks the composition.

So the behaviour should land deliberately, with a test and a reason, rather than
persist as an unattributed edit. Two properties of the current situation are
what make this urgent rather than tidy: `just check <owner>` today means
something different from what the repository says it means, and every session on
this machine is reading its verdicts as evidence.

## Coordination

`.cartridge/justfile` is also the footprint of
`@root/the-composition-s-gates-do-not-inherit-cartridge-yolo`, held by
cartridge-4b, which is holding its collect precisely because this hunk is in the
file and `collect` commits every dirty path inside a footprint.

The two rows are the same kind of defect — a gate that does not mean what its
name says, one because the answer depends on the shell that invoked it, one
because the gate silently does more than it claims. They should land in a
deliberate order, not whichever finishes first. Whoever takes this row agrees
that order with cartridge-4b before collecting.

The implementer must not sweep the existing hunk into an unrelated commit. It
either becomes this PRD's own change, attributed here, or it is removed and
rewritten with a test.
