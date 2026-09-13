---

kind: work
level: 10
status: done
description: "`GCounter::slots` is the one exported function in 559 with no caller anywhere in `src/` or `tests/` — and the sweep that found it produced three false positives for every true one"
read_when: "picking up work, or sweeping for uncalled code"
---

# the-gcounter-accessor-has-no-caller

## Do

`GCounter::slots` (`src/base/src/crdt.rs:47-49`) returns a reference to the
counter's private replica map. Nothing calls it: no `.slots()` and no
`::slots` appears in `src/` or `tests/`. Delete it — the frontier law in
[[SYSTEM]] is that an exported function nothing calls is deleted, and the field
it exposes is reachable inside the module without it.

The sweep behind that: 221 constants and 559 distinct `pub fn` names across
`src/`, each counted for references outside its own definition. Every constant
is live — the residue [[one-deletion-commit-left-four-residues]] describes was a
method and a struct field, not a `const`, so a constant sweep would not have
found either. Of the four functions the sweep flagged, three are false
positives and one is real:

```
from_i32         called as and_then(ReasonKind::from_i32)   — no parentheses
service          the service! proc-macro entry point         — invoked by expansion
spawn_successor  passed as map(identity::spawn_successor)    — no parentheses
slots            no caller                                   — real
```

Three of four, all the same mistake: a search for `name(` cannot see a function
passed as a value or expanded by a macro.

It has a second blind spot, found the same night: the sweep counts callers in
`src/` and `tests/`, and a `#[cfg(test)] mod tests` inside a source file counts
as `src/`. So a function called only by its own in-file tests reads as live —
`Registry::prune_missing` (`src/hub/src/hub_registry.rs:100`) is exactly that
and the sweep passed it ([[the-hub-registry-is-the-machine-inventory]]).
`slots` stood out only because it had no caller at all. That is the reason not to promote
this sweep to a gate as written — it is the failure
[[a-gate-that-walks-cannot-fail-short]] describes, and a gate at a 75% false
positive rate is a gate nobody will keep green. The narrower checks that do run
— `tests/orphan_modules.rs` for an undeclared file, `cargo machete` for an
unused dependency — stay the ones with a runner.

**Done 2026-09-06.** `GCounter::slots` is deleted; `rg` for `.slots()` and
`::slots` over `src` and `tests` answers nothing, and the `BTreeMap` import it
used is still carried by the field itself.

The sweep's accounting is the part worth keeping, and it argues against its own
promotion: three false positives to one true finding, all three from one cause —
a function used as a *value* rather than called. Put harder than the part does,
a gate at that rate is worse than no gate, because the first person to run it
green resolves the noise by deleting the exceptions.

## Check

`GCounter::slots` is gone, `just check` and `just test` are green, and a
re-run of the same sweep over `pub fn` names reports only the three
value-passed false positives above. `just check` green, suite 1,248 passed.
