---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `wire_tolerant_decode` covers the three `memory_rpc` responses and none of the six on the hub wire, which follow the discipline today with nothing holding them to it — the position `HealthRes` was in when `persist_failed` slipped

## Do

`tests/wire_tolerant_decode.rs` exists because the law was enforced by accident.
Its header records it: `persist_failed` landed on 2026-09-06 without
`#[serde(default)]` and was caught only by a reflex-line test "whose fixture
happens to be a minimal payload and therefore happens to look like an old
daemon… that enforcement is an accident of one fixture's style, and it
disappears the moment someone writes the next fixture with
`..Default::default()`."

Its test is named `every_response_decodes_a_payload_with_none_of_its_later_fields`
and covers three: `HealthRes`, `ShutdownRes`, `InvokeRes` — every response in
`src/transport/src/memory_rpc.rs`. The other wire has six more
(`src/transport/src/hub_rpc.rs`): `ResolveRes`, `HubStatusRes`, `SearchRes`,
`StopRes`, `UnloadRes`, and `ResolveReq`/`UnloadReq` on the request side.

They are correct today — every field after `ok` carries `#[serde(default)]`,
and `ok` deliberately does not, the same split the gate's header defends. So
this is not a live defect; it is six structs held to a rule by convention on a
boundary where the skew is at least as likely as the daemon's. A hub is a
per-machine supervisor that outlives the daemons it tracks ([[wire]]), and
those daemons hand themselves over to new binaries while it keeps running
([[hot-reload-fingerprints-mtime-not-content]]).

Extend the existing test to the hub types with the same `FROM_AN_OLD_DAEMON`
shape — a payload carrying `ok` and nothing else.

**Done 2026-09-06.** The gate names all nine: the three `memory_rpc` responses it
already covered, plus `ResolveRes`, `HubStatusRes`, `SearchRes`, `StopRes` and
`UnloadRes` through a local macro, each decoding the same `FROM_AN_OLD_DAEMON`
payload — `{"ok": true}` and nothing else. The macro is there so adding the
tenth response is one identifier rather than a sixth copy of the same six lines,
which is how a list of this kind stops being extended.

**The red half was run, not assumed.** Removing `#[serde(default)]` from
`ResolveRes::endpoint` fails the test with `missing field endpoint`; restoring
it passes. A gate that has never been observed failing is a gate whose subject
is unproven, and this one had two candidate subjects — the rule, or a payload
that happens to decode.

**The subject list is now asserted against the source, not trusted.** The macro
invocation is written by hand, so a response added to either DTO file would not
be exercised and nothing would say so — the failure this gate's own family keeps
producing, built into the gate meant to close one. `the_gate_exercises_every_response_type_on_both_wires`
counts `pub struct …Res` declarations in `memory_rpc.rs` and `hub_rpc.rs` and
asserts 3 and 5, naming the test to extend when it fails. Verified red by adding
a sixth response type to `hub_rpc.rs`: "hub_rpc.rs declares 6 response types and
the test above names 5". Removed again.

`ResolveReq` and `UnloadReq` are deliberately not in it. They are *requests*,
where a missing field is silence rather than compatibility — the same
distinction the gate's header already defends with `InvokeReq::name`, and
`the_gate_can_go_red` pins it.

## Acceptance
The test names all nine response types, and removing `#[serde(default)]` from
any hub response field fails it. `just test` green — observed, at 1,250 passed
with the attribute restored and 1 failed with it removed. The coverage
assertion was proved the same way, and the count in the prose — "six responses"
where `hub_rpc.rs` declares five — was corrected before it could become a number
nobody rechecks.
