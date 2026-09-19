---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
footprint:
  - "src/host/plan.rs"
  - ".cartridge/tests/unit/src/host/plan.rs"
---

# An optional need with no provider still loads

## Outcome

A cartridge that declares an optional need (`key?`) loads and runs when no cartridge in the composition
provides that key; only a hard need with no provider fails the cartridge. An optional glob need
(`key*?`) keeps its optionality instead of silently becoming a hard need.

## Evidence

Measured 2026-09-19 at cartridge.ctg 324f36e by the analyst of
`the-isolation-gate-reads-the-composition-profile/prd-declares-the-memory-call-it-makes`
(`.state/loop/prd-declares-the-memory-call-it-makes/analyst-1.md`, probe `analyst-1-probe.sh`, daemon-free):

- `src/host/plan.rs:146-157` strips `?` and records the key in both `needs` and `optional`; `optional`
  only affects start gating (`plan.rs:42-44`, `host/mod.rs:453-457`).
- `plan.rs:324-333` `unmatched` checks every need, optional ones included, so `needs: ["memory?"]` with
  no memory cartridge fails the consumer: "needs `memory`, which no cartridge declares"
  (`host/mod.rs:389-399` marks it Failed). Probe: exit 1, prd not loaded.
- `plan.rs:177` drops a glob need from `optional` after expansion, so `memory*?` behaves as a hard need;
  with memory present but failing, the consumer waited 62 s and never started. `loader/document.rs:157`
  says `?` is "never a glob", yet `memory*?` is accepted and its `?` lost.

prd must declare the `memory` call it makes (isolation rule) while still planning on a machine with no
memory cartridge; this defect makes that impossible.

## Acceptance

- [ ] A host test proves a cartridge with an optional need and no provider loads and is active, while the
      same need without `?` still fails it with the existing message.
- [ ] A glob need with `?` is either optional after expansion or refused at load with a clear message;
      it is never silently hard. A host test pins which.
- [ ] `just check cartridge` and `just test cartridge` pass (run as `env -u CARTRIDGE_YOLO`).
