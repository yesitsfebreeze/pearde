---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "4h"
---

# Reject unresolved templates and placeholder scaffolds before they become confident facts or graph edges.

## Do

Add a narrow ingestion-hygiene rule for unresolved template material such as placeholder tokens, empty ledger rows, and instruction scaffolds. Apply it at the shared ingestion boundary so direct ingest and watched sources agree. Do not reject legitimate prose merely because it contains angle brackets or examples; define the accepted and rejected shapes from fixtures. Report rejection in existing hygiene counters. Do not automatically delete existing facts; [empty-entities-leave-the-graph](../empty-entities-leave-the-graph/prd.md) governs only empty entities and does not cover this case.

## Acceptance
Focused fixtures reject the observed prevention-ledger template, accept a completed ledger entry and ordinary technical text containing comparison operators or generic type syntax, and produce no entity or edge for rejected input. Direct and watched ingestion paths return the same classification. Existing ingestion and memo indexing tests pass.

A refusal that fires on real content is worse than the scaffold it was
written to catch, and a refusal that misses one leg teaches a reader that
the other leg's silence is a verdict. So the legs were read off the code
rather than recalled.

`fn job` in `src/ingest/src/ingest_worker.rs:191` says so itself — "the ONLY
place a Job is built" — and exactly four public methods on `Worker` reach it:
`enqueue` (284), `submit` (333), `start` (381) and `run` (410), which is
`start` plus a wait. `grep -n "Task::Ingest" src/ingest/src/ingest_worker.rs`
answers four lines: three sends (297, 350, 403 — one per method, `run`
borrowing `start`'s) and the one receive at 459, in `run_loop`, which pushes
every job into `distill`. `distill` opens with `hygiene_refusal`. There is no
fifth door and no way around that one.

`grep -rn "\.enqueue(\|\.submit(\|\.start(\|\.run(" src --include='*.rs'`,
minus the unrelated `enqueue`s on `tick::tick_queue` and `tick_trainer` and
minus `/tests/`, names six production call sites of those four — every place
text can enter the graph as an ingest:

| leg | call site | producer |
|---|---|---|
| MCP/RPC `ingest`, `sync: true` | `src/rpc/src/server.rs:1887` | `worker.run` |
| MCP/RPC `ingest`, queued | `src/rpc/src/server.rs:1953` | `worker.enqueue` |
| durable direct-intake drain | `src/ingest/src/ingest_direct.rs:136` | `worker.start` |
| intake queue, claim leg | `src/ingest/src/ingest_intake.rs:232` | `worker.run` |
| intake queue, document leg | `src/ingest/src/ingest_intake.rs:274` | `worker.run` |
| watched file roots | `src/ingest/src/ingest_file_watcher.rs:184` | `worker.submit` |

The watcher's other leg and `tool_ingest`'s durable leg are not a seventh
door: both write a `DirectJob` to disk (`intake_durably`) and it comes back
through row three. The tree already asserts the shape —
`every_public_entry_point_walks_through_the_clamp` in
`src/ingest/src/tests/ingest_worker_test.rs` was written for the confidence
clamp and holds the same funnel.

Landed at that one point. `hygiene::is_unresolved_template` in
`src/hygiene/piece/src/lib.rs` is the classifier and `hygiene_refusal` in
`src/ingest/src/ingest_worker.rs` the caller, beside `is_contentless` and
above the gate rather than inside it: `HygieneConfig::default().gate` is
`"off"`, so a rule that only ran when an operator turned the gate on would
refuse nothing on any store nobody configured. A refusal is `Rejected`, not
`Failed`, so the durable legs archive it instead of retrying bytes that
cannot become content on a second read, and it is counted on
`ingest_hygiene_rejected` — the counter the gate's own refusals already use,
read by `health` and by the RPC health payload.

The rule is two conditions, both load-bearing: at least two unfilled slots,
AND slots are at least a fifth of the whitespace tokens. A slot is one of
three shapes — an angle group standing alone with a lowercase body, a
`{{mustache}}`, or the literal `YYYY-MM-DD`. "Standing alone" is what keeps
prose out: the `(?m)(?:^|[^\w>])` before the `<` means a generic is glued to
the identifier it parameterises, so `Vec<String>`, `HashMap<String, Vec<u8>>`
and `Option<u8>` are not slots, and a `<` followed by a space or a digit is
never one, so `attempts < 5` and `x<30s` are prose. The density is what keeps
mentions out: a memo that says `<stem>` twice in three hundred words is 0.7%
slots and passes.

The observed artifact is `docs/LEDGER.md` as it stood at `5b7db7c3^`, before
the fold that made `open-work.md` the board deleted it:

```text
# Prevention ledger

- YYYY-MM-DD — <problem> — guard: <path/recipe/commit>
```

Three slots in ten tokens. Fill the row in and every slot is gone, so the
completed entry is ordinary content — that contrast, not the header, is the
fixture pair.

Known ceiling: prose that teaches bare HTML tags (`use <div> and <span>`) is
short enough to clear the density bar. Every such line in this corpus puts
the tag in backticks; the upgrade, if that stops being true, is to skip code
spans before counting — never to loosen the density.

Tests: `src/hygiene/piece/src/tests/hygiene_test.rs` carries the fixtures —
the ledger refused, the filled row accepted, and seven shapes this repo
actually writes (spaced and glued comparisons, nested and multi-argument
generics, one slot inside a real sentence, a URL and an address in angle
brackets, and `YYYY-MM-DD` named as a format in a sentence about it) all
accepted. `an_unresolved_template_is_refused_on_the_direct_and_the_watched_leg_alike`
in `src/ingest/src/tests/ingest_worker_test.rs` runs the same bytes through
`run` (the direct leg's producer) and `submit` (the watcher's), asserts the
counter reaches two and the graph holds zero entities — so nothing for an
edge to point at — and then proves the refusal was the rule and not the dead
embedder: the filled-in row on the same worker reaches the embed leg and
fails there instead.

`just check` green. `cargo nextest run --workspace --no-fail-fast`
1474/1475, the one red `memory::cited_paths`, owned by
[the-plan-crate-cites-an-untracked-file](../the-plan-crate-cites-an-untracked-file/prd.md). `just memos-check` green.
