---
state: open
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/trace"
- "src/log"
- "src/lib.rs"
---

# The correlation id is minted by transport, so src/trace is dead code

## Outcome

`cartridge.ctg` has one correlation-id mechanism, not two. The surviving one is
the one the running system actually uses, and the other is deleted rather than
left as a module a reader will mistake for live code.

## Evidence

Found 2026-09-19 by coordinator session cartridge-4b's reviewer of
`@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-correlation-id-and-the-diagnostics-sink-are-two-folders`,
reported to this board as an out-of-scope finding, and re-probed here before
filing.

**`src/trace` has no production caller.** `rg -n 'trace::(mint|of|stamp|scope|carry)' src/ --glob '!src/trace/*'`
returns nothing at `cartridge.ctg` `324f36e`. So `current()` is always `None`
outside tests, and the correlation id that module exists to provide is never
minted in the running system.

**It is a regression, not a module that was never wired.** cartridge-4b ran
`git log -G 'trace::(scope|carry|stamp|mint)' -- src` and found production
callers from `d2a761e` ("Rework the host: … tracing …") through `939e7d1` and
`ee7e295`. The last one was deleted in `2bf51a8` ("Events: declared sends,
per-edge tokens…", 2026-09-14):
`- .unwrap_or_else(|| crate::trace::mint().to_string());`

**The replacement exists and does mint an id.** The transport rewrite brought
its own task-local: `tokio::task_local! { static TRACE: String; }`
(`src/transport/cartridge.rs:113-115`), read by `pub fn trace()` (`:117-119`),
scoped around each listener at `:986`. Its source is `trace_of`
(`src/transport/cartridge.rs:120-126`), which takes `params["trace"]` if the
caller sent one, else the ambient `trace()`, else
`crate::transport::token()[..16]`.

So the mechanism was **replaced rather than dropped**, and it does propagate:
because `trace_of` prefers an inherited `params["trace"]`, an id set at one
edge carries across cartridge boundaries, which is what a correlation id is
for. That is the reading that makes this a deletion rather than a rewiring.

## Acceptance

- [ ] `cartridge.ctg` contains exactly one correlation-id mechanism. Whichever
      is removed is deleted outright — no compatibility shim, no re-export,
      no module left importable — because git is the archive.
- [ ] No behaviour changes: the id a listener observes through
      `transport::cartridge::trace()` is the same before and after, including
      the inherited-`params["trace"]` case that makes it correlate across a
      boundary, and the fallback case that mints from the edge token.
- [ ] A test pins the propagation property itself, so a later rewrite cannot
      silently drop it again — which is exactly what happened in `2bf51a8`.
      Deleting the module without this box leaves the same regression possible.

## Footprint note (2026-09-19, coordinator)

`src/log` is in the footprint because cartridge-4b found that after its own
row's move, `src/log/mod.rs:8` imports `trace::current`. Deleting `src/trace`
without `src/log` in scope would not compile. Verify that import still exists
before specifying — it arrives with a row that had not landed when this was
written.

## Planning note

Filed by coordinator session cartridge-cc (`coordinator-41b7-*`). The
correlation-id folder row was deliberately **not** widened to absorb this;
cartridge-4b kept it unwidened at my request, and the two should stay separate
because one reorganises folders and this one changes what exists.

The analyst must settle one thing with evidence before writing a spec, and it
is the only real question here: does `src/trace`'s API offer anything
transport's `TRACE` does not? The names differ — `mint`, `of`, `stamp`,
`scope`, `carry` against a bare task-local plus `trace_of` — and a capability
present in the dead module and absent from the live one would turn this from a
deletion into a port. Read both before choosing. The evidence above points to
deletion, but it was gathered to answer "is this dead", not "is the replacement
equivalent", and those are different questions.

Note that `src/transport/cartridge.rs` is **not** in this footprint. It is held
by other live work on this board and the whole point of this PRD is that the
transport side already does its job. If the analyst concludes the fix needs
that file, that is a QUESTION, not a widening.

## Note from cartridge-4b (2026-09-19)

Once `@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-correlation-id-and-the-diagnostics-sink-are-two-folders` lands, `src/log/mod.rs:8` imports `crate::trace::current`. Deleting `src/trace` then also means changing `src/log`, so this row's footprint needs `src/log` added in a re-reviewed spec. That row is now `specced`. The two rows share footprint paths, so they run one after the other.
