---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: cartridges-compose-recursively
needs:
- '@runtime/the-profile-is-the-root-composer'
- '@runtime/a-key-starts-its-provider-on-demand'
- '@runtime/a-cartridge-installs-from-its-source'
---

# cartridges-compose-recursively

This parent coordinates the remaining composition leaves and records their combined evidence. To implement, claim a leaf. Nesting itself is already in the base: [ledger.rs](../../../../../../cartridge.ctg/src/ledger.rs) installs a `cartridge.json` folder at any depth under its path identity. Profile entries such as `live/record` compose nested cartridges, and planning reads declarations without running an entry.

## Acceptance

- [ ] Each linked leaf that is still wanted passes its own review and observable acceptance.
- [ ] At the integrated revisions, `just test runtime` (cwd `/Users/feb/dev/cartridge`) passes, with a recorded list of tested mitigations and remaining limitations.

## Work items

- [the-profile-is-the-root-composer](../the-profile-is-the-root-composer/prd.md): done.
- [a-key-starts-its-provider-on-demand](../a-key-starts-its-provider-on-demand/prd.md): needs a user decision, because on-demand start conflicts with the base's eager wave start.
- [a-cartridge-installs-from-its-source](../a-cartridge-installs-from-its-source/prd.md): rebased onto `cartridge setup`.

## Review

[Review](review.md). Inherits rounds from `cartridges-compose-recursively`, `build-the-composition-pillar` and `the-extension-crate`; at most five.
