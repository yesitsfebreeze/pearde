---

kind: work
level: 10
status: done
actual: 15m
description: "`Channel::new` still takes a `codec` argument after the trait that made it a choice was deleted — a zero-sized type with one value, passed identically by all eight callers, while the body builds a second one itself"
read_when: "touching the RPC substrate, or sweeping for what a deletion left"
---

# the-codec-parameter-outlived-the-trait

Landed with this part's own commit: `Channel::new<A: Adapter>(adapter: A)`,
both framers building their own `JsonEnvelopeCodec::new()` inside, the second
argument struck from all eight callers, and the import struck from the four
files that carried `JsonEnvelopeCodec` only to pass it. `just check` is clean,
which is the whole proof — nothing could read a zero-sized argument.

## Do

`31ed282a` closed [[@prd/work/memory--the-codec-parameter-has-one-type.md]] by deleting the `Codec`
trait, and its `Check` — `rg -n 'JsonEnvelopeCodec|trait Codec' src` returning
only the definition and the `Channel::new` sites — passes today, re-run
2026-09-06. What it does not look at is the signature those sites call:

```rust
pub fn new<A: Adapter>(adapter: A, codec: JsonEnvelopeCodec) -> Self {
    let (read_half, write_half) = Box::new(adapter).split();
    let reader = FramedRead::new(read_half, codec);
    let writer = FramedWrite::new(write_half, JsonEnvelopeCodec::new());
```

(`src/transport/src/typed.rs:280-284`.) `JsonEnvelopeCodec` is a unit struct
(`:218`) — zero-sized, exactly one value — so the parameter can carry no
information, and the body already constructs its own for the writer rather
than cloning the one it was handed. All eight callers pass the same
expression: `memory_rpc.rs:38`, `hub_rpc.rs:18`, `rpc/src/lib.rs:228`,
`hub/src/lib.rs:765` and four in `src/transport/src/tests/typed_test.rs`.

It was a real parameter while `Channel` was generic over the trait. With the
trait gone it is the residue that shape leaves — the fifth of its kind after
the four [[one-deletion-commit-left-four-residues]] audits, and the reason
that part's lesson is about what a deletion's own gate cannot see.

Drop it: `pub fn new<A: Adapter>(adapter: A) -> Self`, both framers
constructing `JsonEnvelopeCodec::new()` inside, and the second argument struck
from the eight call sites.

## Check

`rg -n 'Channel::new' src` shows eight one-argument calls, `Channel::new`
takes no codec, and `just all` is green.
