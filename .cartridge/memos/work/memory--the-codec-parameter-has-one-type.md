---
kind: work
level: 10
status: done
description: the `Codec` trait has one implementation and a type parameter threaded through every generated client and ~30 call sites — pin it to `JsonEnvelopeCodec` and delete the parameter
read_when: "picking up work, or touching the RPC substrate"
---

# the-codec-parameter-has-one-type

## Do

`src/transport/src/typed.rs:206` declares `pub trait Codec` and
`src/transport/src/typed.rs:239` is its only implementation, in the whole
workspace and in every test. The trait already pins `Frame = Value` at the one
place that bounds it — the `codec_bound` in `src/transport/macros/src/lib.rs:95`
— so the only thing a second implementation could vary is the framing, and
`wire` says newline framing is the wire. The parameter cannot vary.

What it costs: a 12-line `where` clause repeated through `service!`, a `<C>` on
every generated client and its `Channel`, and a turbofish at each call site —
`MemoryRpcClient::<JsonEnvelopeCodec>::connect_endpoint_with_retry` in
`src/hub/src/lib.rs` (5), `src/commands/src/commands_admin.rs` (10),
`src/commands/src/lib.rs`, `src/commands/src/commands_route.rs`,
`src/rpc/src/server.rs`, and the two `impl …Client<JsonEnvelopeCodec>` blocks in
`src/transport/src/memory_rpc.rs` and `src/transport/src/hub_rpc.rs`.

Delete the trait, make `Channel` and the generated clients concrete over
`JsonEnvelopeCodec`, drop `codec_bound` from the macro, and drop the turbofish
everywhere. `Encoder`/`Decoder` stay: those are `tokio_util`'s and carry the
framing.

Nothing reaches into the concrete codec any more: `set_max_frame_len`, the
pre-auth cap's last handle, went in `494508bf`
(`the-pre-auth-frame-cap-has-no-caller`), so the type parameter carries no
accessor the macro's callers depend on.

## Check

`rg -n 'JsonEnvelopeCodec|trait Codec' src` returns only the type's own
definition and `Channel::new` construction sites — no turbofish, no trait — and
`just all` is green.

Landed 2026-09-06 on branch `worktree-agent-a1428197a9059983d` (commit
`d5319c10`, on top of `825925fb`): the trait is gone from
`src/transport/src/typed.rs`, `Channel` and the `service!` clients in
`src/transport/macros/src/lib.rs` are concrete over `JsonEnvelopeCodec`, the
seven call-site files carry no turbofish, and the `rg` above returns the
definition, its `use` lines and the `Channel::new` sites; 1,230 tests green.
Blocked on the merge into `main`: six of its ten files sit uncommitted in the
shared tree under a session that is no longer live, so `git merge` refuses
until that work is committed or dropped. `main` itself is red at `825925fb`
— `tests/wire_tolerant_decode.rs:92` reads `persist_failed`, a field only that
uncommitted diff adds.

Merged into `main` 2026-09-06 as `31ed282a`, after the six dirty files it
touched were committed by their own sessions. Two conflicts, both real: the
impl block takes the branch's untyped form with main's body, `connect_local`
having been deleted after the branch was cut; and the shutdown helper keeps
main's `.ok()?` with the turbofish removed. 1,286 tests pass, fmt and clippy
clean.
