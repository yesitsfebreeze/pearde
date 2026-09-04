---
title: cargo-vendor-is-order-independent-of-the-source-replacement-
date: 2026-09-02
type: conclusion
tags: [cargo, conclusion, source-replacement, vendor]
sources:
  - "[[260902-14d9]]"
  - "[[260902-4b7c]]"
derived_from: []
---

# cargo vendor is order-independent of the source replacement stanza

When re-vendoring a git dependency after a rev bump, the order of edits between `Cargo.toml` and the `[source]` replacement stanza in `.cargo/config.toml` does not matter: `cargo vendor` ignores `[source]` replacement unless passed `--respect-source-config`, so it fetches the rev `Cargo.toml` names even while the stanza still points a directory source at the old bytes. What DOES read the replacement is `cargo check`/`build`, and when the package was renamed as well as re-revved, stale bytes under the new directory name are a hard error (`no matching package named …`), not a false green — the vendor-check script's content match stays the only guard for a same-name rev bump.

Consequence: the regeneration recipe `cargo vendor --versioned-dirs /tmp/v && rm -rf vendor/<pkg>-<ver> && cp -R /tmp/v/<pkg>-<ver> vendor/` is order-independent, and a consumer PRD need not sequence the config edit around it.
