---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# Failures carry a type

## Outcome

Errors crossing a module boundary are enum values a caller can match on, not `String`. Today 58 signatures across ten files return `Result<_, String>`, `thiserror` is a dependency used in one file, and the single real error type is `runtime::Error`. The wire, the loader, the settings layer, and the socket all format failures into text at the point of origin, so nothing downstream can distinguish "cartridge not found" from "cartridge crashed" without parsing prose.

## Acceptance

- [ ] `grep -c 'Result<[^,]*, String>' src/*.rs` sums to zero outside `main.rs` presentation code.
- [ ] One `Error` enum per module that fails in more than one way (`loader`, `settings`, `cartridge`, `socket`, `stream`, `sdk`), each derived with `thiserror`, each variant carrying the path, key, or id it failed on.
- [ ] Wire and socket replies keep their current JSON shape; the string the client sees is rendered once, at the boundary, from the typed error.
- [ ] Every existing test that asserted on an error string now asserts on the variant, and the string rendering has its own test.
- [ ] `runtime::Error` remains the top type; module errors convert into it with `From`.

## Proof and recovery

Do this after `no-panic-answers-a-recoverable-failure` so the new `?` sites land on typed errors. Keep the change mechanical per module; do not redesign the wire.
