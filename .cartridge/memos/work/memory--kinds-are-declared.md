---
kind: work
level: 10
status: done
description: a claim kind exists because a part declares it — `DEFAULT_KINDS` retires into the record, the `claim_kind` operation stops being the only way in
read_when: "executing the declared-surface plan"
---

# kinds-are-declared

## Do

A claim kind is declared by a part: `kind: claim-kind`, `name:` the word, and
`description:` the sentence the distill prompt shows. The live registry
(`g.root.claim_kinds`, with its subClassOf closure) is populated from those
entities at load, and `DEFAULT_KINDS` (`src/ingest/src/ingest_distill.rs:33`)
is deleted with its readers moved to the registry —
`apply_claim_kind_filter` and the `report` group check
(`src/rpc/src/server.rs:439`, `:1449`), the distill prompt's `kind_list`, and
the `fact` fallback in `parse_claims` (`:172`). The `claim_kind` operation
keeps working for a caller with no record; it is no longer the only door.

The eight built-ins become the first eight declaring parts, and the record's
own vocabulary joins them — `claim-kind-filter-rejects-part-kinds` measured
620 entities in this store carrying `knowledge`, `documentation`, `research`,
`work`, `insight`, `routine` and `question` as their `claim_kind`, every one
of which the filter refuses today while `report` groups them happily. Those
words become declarations in the same change, so the record reads back by the
kind it was written with.

## Check

`just test` green, plus: `query {claim_kind: "knowledge"}` against this
repo's store answers rows instead of `unknown claim kind`, a store whose
record declares a kind accepts a filter naming it with no `claim_kind`
operation ever called, and a kind nothing declares still answers
`unknown claim kind`.

Landed. `DEFAULT_KINDS` is gone from `src/ingest/src/ingest_distill.rs` and
every reader is on `root.claim_kinds`: `apply_claim_kind_filter` and
`resolve_claim_kind` (`src/rpc/src/server.rs`) ask the registry alone, the
`claim_kind {action: add}` arm and its no-daemon twin in
`src/commands/src/commands_admin.rs` pass an empty builtin set, `kind_list`
sorts the whole vocabulary instead of appending a declared order to a built-in
one, and `parse_claims` keeps `fact` as the fallback for a word the registry
does not hold — which now includes the seven words this const used to admit for
free.

`claim-kind` joined `DECLARING_KINDS` in `src/ingest/src/ingest_worker.rs`, so
a declaring part lands in `behaviour` with no TTL and no vector, and
`register_declared_kind` runs at the head of the per-job `distill` — above the
unchanged-bytes gate, so a boot scan carries the whole vocabulary into a store
that predates it even when nothing on disk moved.

The deviation this record should carry: **the word is the part's `# ` heading,
not its leaf**. `a-declaration-carries-its-payload-in-a-toml-block` expected the
leaf to be the handle, and for a routine it is. It cannot be here —
a leaf is unique across `memos/` and eight of the fifteen words are already held
by a `system/` type part (`decision`, `knowledge`, `documentation`, `research`,
`work`, `insight`, `routine`, `question`), the same squeeze that made the part
declaring the kind `work` the file `system/work-memo.md`. So the files are
`memos/claim-kind/<word>-claim-kind.md` and the heading is the word;
`system/claim-kind.md` states the rule.

Fifteen declarations landed: the eight retired built-ins plus the seven words
`claim-kind-filter-rejects-part-kinds` measured 620 entities already carrying.

The Check, clause by clause: `cargo nextest run --workspace` is 1323 passed;
`a_declaring_part_registers_its_claim_kind_and_nothing_else_does` drives a
`kind: claim-kind` job through `process_batch` and reads the word and its
sentence back out of `root.claim_kinds` with no `claim_kind` operation called,
while `an_ordinary_part_registers_no_claim_kind` holds the other side;
`claim_kind_filter_rejects_an_unknown_label_instead_of_matching_nothing` keeps
an undeclared word answering `unknown claim kind`. The store clause —
`query {claim_kind: "knowledge"}` answering rows — runs the moment the daemon
reads the landed `memos/claim-kind/`, by that same path.

Retired since. [[one-vocabulary-not-two]] (`9ad73aaa`) folded this vocabulary
into the `kind: type` declaration, so every sentence above naming
`kind: claim-kind` is what landed then and not the rule now: `DECLARING_KINDS`
(`src/ingest/src/ingest_worker.rs:67`) no longer carries the word,
`register_declared_kind` fires on `TYPE_KIND`, and `memos/claim-kind/` and
`system/claim-kind.md` are gone with the fifteen declarations folded into the
type memos that already held each word. The deviation this record carries
survived the fold — the word is still the memo's `# ` heading and not its leaf
— and so did both tests of the Check, renamed to
`a_declaring_memo_registers_its_claim_kind_and_nothing_else_does` and
`an_ordinary_memo_registers_no_claim_kind`, each now driving a `kind: type`
job. [[type]] states the rule; [[claim-kind-lives-on-in-three-work-memos]]
measured the drift.
