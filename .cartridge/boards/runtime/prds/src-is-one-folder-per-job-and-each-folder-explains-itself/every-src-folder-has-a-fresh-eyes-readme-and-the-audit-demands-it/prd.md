---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
blast-radius: low
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/node/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lua/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/sandbox/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trust/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/error/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/README.md
  - /Users/feb/dev/cartridge/cartridge.ctg/README.md
---

# every src folder has a fresh eyes readme and the audit demands it

## Outcome

Every folder under `cartridge.ctg/src` has a `README.md` a newcomer reads in under a minute, and a folder without one fails the audit. The sibling children write the READMEs for the folders they create; this child writes the rest (`asp`, `host`, `node`, `lua`, `sandbox`, `trust`, `error`, `cli`) and adds the check.

## The shape

At most 25 lines, the same five headings in every folder, no paragraphs:

```
# <module>
Does:      one sentence
Why:       what breaks without it
Owns:      the three to six types that matter
Talks to:  the modules it calls, and the modules that call it
Start at:  the one function to read first
```

## Acceptance

- [ ] Every directory directly under `src/` has a `README.md` with those five headings, in that order, in 25 lines or fewer.
- [ ] Each `Talks to` agrees with the crate's real `use` edges, and each `Start at` names a function that exists.
- [ ] `just audit` fails, naming the folder, when a directory under `src/` has no `README.md` or a README missing a heading. A test proves it by running the check against a copy of the tree with one README removed.
- [ ] The crate's top-level `README.md` lists the folders with their `Does` lines and no other description of the layout.

## Proof and recovery

Gates, cwd `/Users/feb/dev/cartridge`: `just audit`, `just check runtime`. Not run. The audit recipe lives in the parent repository's `.cartridge/justfile`; if the check belongs there rather than in `cartridge.ctg`, the analyst widens the footprint before speccing.
