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

# the watcher computes a language hint per file and carries it through the durable intake into the worker, where its only reader is an LLM split branch no production call site ever takes

## Do

`split` (`src/ingest/src/ingest_worker.rs:750`) takes three arguments and has
one production caller, which passes `None` for the third:

```
// Heuristic split ONLY — an LLM split would add a per-document LLM call on the commit path.
let chunks = crate::ingest_worker::split(&job.text, &job.hint, None);
```

With `llm` `None`, `split` falls straight through to `paragraph_split` and
`hint` is never read. `llm_split` (`:760`) is the only code that reads it, and
its only callers are two tests that invoke it directly
(`ingest_worker_test.rs:817` and `:822`).

The hint is not cheap to carry. `language_hint`
(`src/util/src/watcher.rs:349`) maps an extension to a word per watched file,
`IngestRecord` carries it (`:217`), `MemoryFileWatcherSink::ingest` unwraps it
(`ingest_file_watcher.rs:110`) into `DirectJob.hint` — a required serde field
written into every payload in the durable intake — and the worker threads
it through four call layers (`:88`, `:160`, `:210`, `:258`) to the argument
position that discards it.

Delete `llm_split` and its two tests, delete `split` and call
`paragraph_split(&job.text)` at the one site, then unthread `hint`:
`DirectJob.hint`, the four worker layers, `IngestRecord.language_hint` and
`language_hint` itself. Removing the field is safe for the intake that already
holds it — `DirectJob` is `serde_json`, which ignores unknown keys, so the
pending payloads still deserialize
([[the-direct-intake-has-already-replayed-most-of-itself]]).

One thing goes with it that is worth naming rather than losing quietly: the
three refusals documented on `paragraph_split` — a one-line label glued to the
paragraph below, a front-matter fence skipped, a chunk with no letter or digit
skipped ([[session-names-no-origin]]) — apply to the heuristic path only.
`llm_split` returns every non-empty line of the model's answer as a statement,
so a refusal sentence or a "Here are the statements:" preamble would have
become thoughts. Deleting the branch removes that exposure instead of leaving
it one argument away.

**Done 2026-09-06, and the `Do` missed one surface.** Everything it names is
gone: `llm_split` and its two tests, `split` and its three, `DirectJob.hint`,
the four worker layers, `IngestRecord.language_hint` and `language_hint`
itself. `IngestRecord` is down to three fields.

**The hint was also an MCP argument.** `IngestArgs.hint` (`src/rpc/src/server.rs`)
reached `tool_ingest`'s three call sites, and the `ingest` tool advertised
`hint?` in its description and its schema. Unthreading the plumbing and leaving
that would have left the tool naming an argument that reaches nothing — the
defect [mcp-tools-declare-their-schema](../mcp-tools-declare-their-schema/prd.md) removed from `forget`, `degrade` and
`audit` earlier the same night, recreated by a deletion instead of by drift. So
the field, the description and the schema property go too, and `reflex`'s rate
path stops passing `"hint": "decision"` into its own `tool_ingest` call.

Two things the unthreading surfaced, both now gone. `ingest_intake.rs:212`
passed `c.kind.clone()` as the hint and `c.kind` as the claim kind — the drain
fed the claim kind in as the language hint, which `llm_split` would have
rendered as "This text describes decision." had it ever run. And eleven call
sites in `ingest_worker_test.rs` passed two adjacent `String::new()` for
hint-then-claim-kind: positional arguments of one type with nothing between
them, where removing the right one is safe only because the compiler counts.

The refusal note is kept where it is load-bearing rather than in the record
alone — the comment at the one remaining call site now says the paragraph
splitter's three refusals applied to that path only, so nobody re-adds an LLM
branch believing they were general.

## Acceptance
`rg -n 'llm_split|language_hint' src/ tests/` finds nothing, and `split` is
gone with its one caller reading `paragraph_split` directly. `just check` and
`just test` green. A parked payload written before the change still drains: the
`hint` key is present in the JSON and ignored.

All hold. `rg -n 'language_hint|llm_split' src tests` answers nothing, the one
caller reads `paragraph_split` directly, `just check` and `just memos-check` are
green, and the suite reads 1,239 passed with 17 skipped.
