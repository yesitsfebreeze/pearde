---
complexity: 1
footprint:
  - "src/store/core/src/lib.rs"
  - "src/graph/src/persist.rs"
  - "src/bootstrap/src/lib.rs"
  - "src/health/src/lib.rs"
  - "src/commands/src/commands_check.rs"
  - "src/retrieval/piece/src/retrieval_query.rs"
---

# spec01 — lock the embedding stamp that made this PRD unnecessary

## Files and steps

No code changes. This PRD was investigated on 2026-09-16 and withdrawn: the
guard it proposed is already in the tree, and the 363 rows that motivated it
were superseded, not mis-embedded. The withdrawal is only durable if the guard
it points at cannot be quietly removed, so this spec is the regression lock and
nothing else.

Every assertion below was reproduced against `memory.ctg` at
`3432b13376017be921d745719e0626d6f0b5463c`. Each block is a grep lock: it
asserts that a named line of the guard is present, in the function that has to
hold it. A grep lock catches deletion, renaming, and a changed constant or
severity — the ways a guard actually rots under an unrelated edit. It does not
execute the code, so it cannot catch a line that is still present and no longer
reached. That ceiling is stated in **Risk** below rather than papered over.

The guard, as it stands:

1. `store_core::EmbedStamp { model, dim }` (`src/store/core/src/lib.rs:312`) is
   the per-store identity of the model that produced the vectors. `EmbedRead`
   keeps `Missing`, `Stamped` and `Unreadable` apart, so a corrupt stamp never
   reads as an unstamped store.
2. `Store::check_embed_stamp` (`src/store/core/src/lib.rs:587`) adopts on an
   unstamped store, clears the flag on a match, and on a change sets the durable
   `embed_mismatch` `AtomicBool` and logs that recall stays near zero until
   `memory reembed`. An unreadable stamp propagates its error and is left on
   disk.
3. `graph::persist` (`src/graph/src/persist.rs:73-101`) builds the stamp from the
   configured model plus the width the graph actually holds, and runs the check
   on every write path: `save_graph_into`, `flush_guarded`, `flush_snapshot`.
4. The open path is `bootstrap::bind_embed_model`
   (`src/bootstrap/src/lib.rs:81-84`), the sole caller of `check_graph_stamp`:
   it sets the configured model on the graph and then checks the stamp. The
   order is load-bearing — `stamp_of` returns `None` while the model is empty,
   so a check before the bind would be a silent no-op. Block 2 asserts the call,
   its position after the bind, and that all three functions that open or reopen
   a graph still route through the binder: `load_graph` (`:57`),
   `try_load_graph` (`:71`) and `reload_graph` (`:99`).
5. `memory health` reports the model, the width, the flag and the unreadable
   diagnostic (`src/health/src/lib.rs:185-201`); `memory check` raises both
   `embed_unreadable` and `embed_mismatch` as `error` findings
   (`src/commands/src/commands_check.rs:126-147`).
6. `cold_candidates` (`src/retrieval/piece/src/retrieval_query.rs:751`) skips
   superseded rows unless the query is `as_of` a past time. That, not any width
   check, is why the store in question answered nothing.

No test is added: this spec asserts code that exists and changes none of it. No
`cargo` command is run either — a Verify block has 120 s, and a cold
`CARGO_TARGET_DIR` for this workspace does not fit in it, while a hot one would
restart the live cartridge. The blocks are grep-only.

## Acceptance

- [x] `EmbedStamp` still carries both halves of the identity — a model name and
      a dimension — and `EmbedRead` still distinguishes an unreadable stamp from
      an absent one.
- [x] A changed model still raises the durable `embed_mismatch` flag on the
      store and still names `memory reembed`; an unstamped store still adopts;
      an unreadable stamp is still not adopted over.
- [x] The stamp is still checked on all three write paths (`save_graph_into`,
      `flush_guarded`, `flush_snapshot`) and at graph open, where
      `bind_embed_model` still calls `check_graph_stamp` after binding the
      configured model, and `load_graph`, `try_load_graph` and `reload_graph`
      all still route through `bind_embed_model` — from a stamp built out of
      that model and the graph's real vector width.
- [x] `memory health` still reports the model, the width, the mismatch flag and
      the unreadable diagnostic, and `memory check` still raises
      `embed_unreadable` and `embed_mismatch` as `error` findings, unreadable
      first.
- [x] `cold_candidates` still skips — `continue`s past — a superseded row unless
      the query is `as_of`, and no speculative `vector_dim_mismatch` finding has
      returned.

## Risk

A grep lock has one ceiling, and it is worth naming so nobody reads a green
collect as more than it is: a line that is present but unreachable still passes.
Four semantic no-ops were constructed and confirmed to survive every block — an
early `return` inserted in `check_stamp`, `check_graph_stamp`'s body wrapped in
`if false`, `check_embed_stamp` short-circuited to `Ok(EmbedCheck::Match)`, and
`embed_mismatch()` hardcoded to `false`. Closing that gap needs an executing
test, which is code, and this PRD is withdrawn precisely because it should not
add any. The lock is aimed at the realistic failure — a future refactor drops a
call site or downgrades a finding without noticing — and it catches every such
mutation tried.

## Verify and Proof

<!--
Engine facts (prd.ctg/.cartridge/templates/spec.md): each block runs as
`sh -eu -c`, 120 s, twice — first with cwd = the lane, then with cwd = `repo`.
Paths are relative to the repo root; no `cd`, no absolute checkout. These
blocks read six source files and write nothing, inside the footprint or out.
No cargo command, so no CARGO_TARGET_DIR is needed.
-->

The stamp type, the unreadable/absent distinction, and the durable flag:

```sh
f=src/store/core/src/lib.rs
# The stamp type carries the model identity and the vector width.
grep -q '^pub struct EmbedStamp {' "$f"
awk '/^pub struct EmbedStamp/,/^}/' "$f" | grep -q '^	pub model: String,$'
awk '/^pub struct EmbedStamp/,/^}/' "$f" | grep -q '^	pub dim: usize,$'

# A stamp that did not decode is its own answer, never "unstamped".
awk '/^pub enum EmbedRead/,/^}/' "$f" | grep -q 'Missing,'
awk '/^pub enum EmbedRead/,/^}/' "$f" | grep -q 'Stamped(EmbedStamp),'
awk '/^pub enum EmbedRead/,/^}/' "$f" | grep -q 'Unreadable(String),'

# The durable mismatch flag: a store field, not a log line.
grep -q 'embed_mismatch: std::sync::atomic::AtomicBool,' "$f"
grep -q 'pub fn embed_mismatch(&self) -> bool {' "$f"

# Writing a stamp clears the flag.
awk '/pub fn set_embed_stamp/,/^	}/' "$f" | grep -q 'self.put(self.meta, EMBED_KEY, stamp)'
awk '/pub fn set_embed_stamp/,/^	}/' "$f" | grep -q '.store(false, std::sync::atomic::Ordering::Relaxed)'

# The check: unstamped adopts, unchanged clears, changed raises the durable flag
# and names reembed. An unreadable stamp propagates its error and is left on disk.
c=$(awk '/pub fn check_embed_stamp/,/^	}/' "$f")
printf '%s\n' "$c" | grep -q 'self.set_embed_stamp(current)?;'
printf '%s\n' "$c" | grep -q '.store(true, std::sync::atomic::Ordering::Relaxed);'
printf '%s\n' "$c" | grep -q '.store(false, std::sync::atomic::Ordering::Relaxed);'
printf '%s\n' "$c" | grep -q 'memory reembed'
printf '%s\n' "$c" | grep -q 'EmbedCheck::Mismatch'
# No adoption over an unreadable stamp: the read error must escape, not default.
printf '%s\n' "$c" | grep -q 'self.get::<EmbedStamp>(self.meta, EMBED_KEY).map_err'
```

Where the check runs: on every path that writes vectors, and at graph open:

```sh
f=src/graph/src/persist.rs
# The stamp about to be written is the configured model plus the width the graph holds.
s=$(awk '/^fn stamp_of\(/,/^}/' "$f")
printf '%s\n' "$s" | grep -q 'store_core::EmbedStamp {'
printf '%s\n' "$s" | grep -q 'model: model.to_string(),'
printf '%s\n' "$s" | grep -q 'dim: g.entity_vector_dim()?,'

# The shared check, and its one call into the store.
awk '/^fn check_stamp\(/,/^}/' "$f" | grep -q 'store.check_embed_stamp(stamp)'

# On load, and on every path that writes vectors to disk.
for fn in check_graph_stamp save_graph_into flush_guarded flush_snapshot; do
	if ! awk "/^pub fn $fn\(/,/^}/" "$f" | grep -q 'check_stamp('; then
		echo "$fn does not check the embedding stamp" >&2
		exit 1
	fi
done
# The snapshot flush carries the stamp taken under the read guard.
awk '/^pub fn snapshot_for_flush\(/,/^}/' "$f" | grep -q 'stamp: stamp_of(g),'

b=src/bootstrap/src/lib.rs
# The open path. bind_embed_model is the SOLE caller of check_graph_stamp, so
# without this the definition above is reachable from nothing and the open-time
# check is gone with every other block still green.
o=$(awk '/^pub fn bind_embed_model\(/,/^}/' "$b")
printf '%s\n' "$o" | grep -q 'graph::persist::check_graph_stamp(g);'
# ...and every path that opens or reopens a graph must go through it. A binder
# nothing calls is the same missing check one indirection further out.
for fn in load_graph try_load_graph reload_graph; do
	if ! awk "/^pub fn $fn\(/,/^}/" "$b" | grep -q 'bind_embed_model(&mut g, cfg);'; then
		echo "$fn does not bind the embedding model" >&2
		exit 1
	fi
done
# Order is load-bearing: stamp_of answers None while the model is empty, so a
# check before the bind would be a no-op that still greps clean.
set_at=$(printf '%s\n' "$o" | grep -n 'g.set_embed_model(&cfg.embed.model);' | head -1 | cut -d: -f1)
chk_at=$(printf '%s\n' "$o" | grep -n 'graph::persist::check_graph_stamp(g);' | head -1 | cut -d: -f1)
[ "$set_at" -lt "$chk_at" ]
```

What the operator is told — `memory health` and `memory check`:

```sh
f=src/health/src/lib.rs
# health reports the model, the width, the durable flag, and the unreadable case.
grep -q 'pub embed_model: String,' "$f"
grep -q 'pub embed_dim: usize,' "$f"
grep -q 'pub embed_mismatch: bool,' "$f"
grep -q 'pub embed_unreadable: String,' "$f"
grep -q 'embed_mismatch: store.map(|s| s.embed_mismatch()).unwrap_or(false),' "$f"
grep -q 'store::EmbedRead::Stamped(s) => s.model.clone(),' "$f"
grep -q 'store::EmbedRead::Unreadable(diag) => diag,' "$f"

g=src/commands/src/commands_check.rs
# Both are error findings, and unreadable is raised before mismatch: it is the
# stronger claim, and embed_mismatch is false there for want of a comparison.
grep -q 'if !h.embed_unreadable.is_empty() {' "$g"
grep -q 'if h.embed_mismatch {' "$g"
grep -A1 '"embed_unreadable",' "$g" | grep -q '"error",'
grep -A1 '"embed_mismatch",' "$g" | grep -q '"error",'
u=$(grep -n '"embed_unreadable",' "$g" | head -1 | cut -d: -f1)
m=$(grep -n '"embed_mismatch",' "$g" | head -1 | cut -d: -f1)
[ "$u" -lt "$m" ]
```

Why the 363 rows returned nothing, and the check that was deleted for firing on
nothing:

```sh
f=src/retrieval/piece/src/retrieval_query.rs
# The cold scan skips superseded rows unless the query asks as-of a past time.
# This, not any width check, is why a store of superseded rows returns nothing.
c=$(awk '/^fn cold_candidates\(/,/^}/' "$f")
# Anchored to the disjunct's own indentation, so the expression cannot be
# demoted to a standalone `let` while the skip branch is quietly dropped, and
# the branch must still reach `continue` three lines on. cold_candidates has two
# `continue;` statements, so a bare grep for one of them proves nothing.
printf '%s\n' "$c" | grep -q '^			|| (entity.is_superseded() && opts.is_none_or(|o| o.as_of.is_none()))$'
printf '%s\n' "$c" \
	| grep -A3 '^			|| (entity.is_superseded() && opts.is_none_or(|o| o.as_of.is_none()))$' \
	| tail -1 | grep -q '^			continue;$'

# No width-mismatch finding was reintroduced: it fired on nothing, and this PRD
# was withdrawn rather than adding a check for a fault with no instance.
for p in src/retrieval/piece/src/retrieval_query.rs src/commands/src/commands_check.rs src/health/src/lib.rs; do
	if grep -qn 'vector_dim_mismatch' "$p"; then
		echo "vector_dim_mismatch returned in $p" >&2
		exit 1
	fi
done
```
