---
complexity: small
footprint:
  - proxy.ctg/src/service.rs
  - proxy.ctg/.cartridge/docs/README.md
  - proxy.ctg/.cartridge/tests/unit/tests.rs
---

# spec01 — rerun the proof that a namespaced caller copy replaces the injection

The behaviour is already landed in `proxy.ctg` at `0692c18`; this spec is the
executable record of it. Every block below reruns the proof rather than
restating it.

What the landed code does, at `0692c18`:

- `src/service.rs:589-600` collects the caller's tool names per wire
  (`t["function"]["name"]` for Chat, `t["name"]` otherwise) before descriptor
  assembly.
- `src/service.rs:629-639` skips the descriptor whose public name
  `cartridge__{name}` is a **strict** suffix of a caller tool name
  (`caller.len() > public.len() && caller.ends_with(&public)`). A skipped
  descriptor never reaches `registry.insert` at line 647.
- Because the exact name is not a strict suffix of itself, an exact
  `cartridge__{name}` caller tool still reaches `wire::inject`, which fails
  with `caller tool collides with injected tool` (`src/wire.rs:86-93`) before
  the request is forwarded.
- A model call is dispatched internally only when `registry.contains_key` holds
  (`src/service.rs:759`), and `Service::execute` (line 809) is the only site
  that consults the `policy` service (line 823) and the only caller of
  `observe` (lines 864, 899). A skipped tool is not in the registry, so its
  namespaced calls are handed back to the caller untouched.

## Base and dependencies

- `repo` is the superproject `/Users/feb/dev/cartridge`; the footprint lives in
  the `proxy.ctg` submodule, whose HEAD is `0692c18`.
- **Collect this PRD without a lane.** A lane is `git worktree add` on the
  superproject (`prd.ctg/src/lifecycle.ts:225`), which leaves every submodule
  directory empty — `proxy.ctg/` in a lane contains nothing. Each block below
  therefore refuses outright when `proxy.ctg/src/service.rs` is missing instead
  of reporting a vacuous pass. With no lane, `collect` runs the blocks once in
  `repo` itself (`lifecycle.ts:126`), where the submodule is checked out.
- The blocks are not hermetic: they compile the `proxy.ctg` working tree as it
  stands, and block 2 resolves `../memo.ctg` from the live checkout for the
  `evidence` path dependency that `0692c18`'s `Cargo.toml` declares (the
  working tree currently carries `evidence` as a crate module instead, so the
  symlink is harmless either way).
- `proxy.ctg` carries about ten dirty paths belonging to other work (including
  an untracked `src/evidence.rs`). None is in this footprint; the superproject
  cannot see inside the submodule, so `collect`'s footprint scan sees no change
  here and the receipt commit is the superproject HEAD.
- Every cargo command runs under an isolated `CARGO_TARGET_DIR` so no live
  cartridge dylib is rewritten and no host restarts mid-verification.

## Acceptance

- [x] The proxy unit suite passes in this tree with no failure and at least 55
  tests, and `namespaced_copies_of_injected_tools_are_skipped_not_duplicated`
  is one of the tests that ran (block 1).
- [x] That test's first half observes a Chat request whose caller tools carry
  `mcp__cartridge__memo`: the forwarded tool list keeps the namespaced name,
  carries no `cartridge__memo`, and no internal `tool.memo` call is dispatched
  (block 1).
- [x] Its second half observes an exact `cartridge__memo` caller tool failing
  with `collides` and no router request at all — the collision check in
  `wire::inject` still fires before any side effect (block 1).
- [x] A caller-owned namespaced call asks no policy round and journals no
  observation: block 2 reruns the same test with both absences asserted, on an
  out-of-tree copy of the crate, and the run passes.
- [x] `proxy.ctg/.cartridge/docs/README.md` documents both halves — the exact
  collision that fails before forwarding, and the namespaced duplicate that is
  skipped (block 1).

## Verify and Proof

Block 1 — the suite, the named test and the documented distinction.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/teaches-once-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER=
test -f proxy.ctg/src/service.rs || { echo "proxy.ctg is not checked out here (a superproject lane has empty submodules); collect this PRD without a lane" >&2; exit 1; }

grep -q 'Exact name collisions with caller tools fail before forwarding' proxy.ctg/.cartridge/docs/README.md
grep -q 'skips the duplicate instead of teaching the model the same' proxy.ctg/.cartridge/docs/README.md
grep -q 'mcp__cartridge__memo' proxy.ctg/.cartridge/docs/README.md

out="$CARGO_TARGET_DIR/suite.txt"
mkdir -p "$CARGO_TARGET_DIR"
cargo test --manifest-path proxy.ctg/Cargo.toml --lib > "$out" 2>&1 || { cat "$out"; exit 1; }
grep -q 'test tests::namespaced_copies_of_injected_tools_are_skipped_not_duplicated ... ok' "$out"
grep -Eq 'test result: ok\. (5[5-9]|[6-9][0-9]|[1-9][0-9]{2,}) passed; 0 failed;' "$out"
grep -E 'test result:' "$out"
```

Block 2 — the caller-owned call asks no policy and journals nothing. The same
test is re-run out of tree with the two absences asserted, because the shipped
test only asserts the third (no internal dispatch). Nothing in the footprint is
written: the crate is copied to a temporary directory first.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/teaches-once-verify}"
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER=
test -f proxy.ctg/src/service.rs || { echo "proxy.ctg is not checked out here (a superproject lane has empty submodules); collect this PRD without a lane" >&2; exit 1; }

probe=$(mktemp -d)
mkdir -p "$probe/proxy.ctg/.cartridge"
cp proxy.ctg/Cargo.toml proxy.ctg/Cargo.lock proxy.ctg/build.rs proxy.ctg/cartridge.json "$probe/proxy.ctg/"
cp -R proxy.ctg/src "$probe/proxy.ctg/src"
cp -R proxy.ctg/.cartridge/tests "$probe/proxy.ctg/.cartridge/tests"
ln -s "$PWD/memo.ctg" "$probe/memo.ctg"

t="$probe/proxy.ctg/.cartridge/tests/unit/tests.rs"
awk '/no internal tool dispatch happened/ {
    print "\t\tassert!(!calls.iter().any(|(k, _)| k == \"policy\"), \"{calls:?}\");";
    print "\t\tassert!(!calls.iter().any(|(k, a)| k == \"memo\" && a[\"op\"] == \"observe\"), \"{calls:?}\");";
  } { print }' "$t" > "$t.probe"
mv "$t.probe" "$t"
# The anchor must have matched: a silent no-op would prove nothing.
test "$(grep -c 'k == "policy"), "{calls:?}"' "$t")" -eq 1
test "$(grep -c 'a\["op"\] == "observe"), "{calls:?}"' "$t")" -eq 1

out="$CARGO_TARGET_DIR/probe.txt"
mkdir -p "$CARGO_TARGET_DIR"
cargo test --manifest-path "$probe/proxy.ctg/Cargo.toml" --lib \
  tests::namespaced_copies_of_injected_tools_are_skipped_not_duplicated > "$out" 2>&1 || { cat "$out"; exit 1; }
grep -Eq 'test result: ok\. 1 passed; 0 failed;' "$out"
grep -E 'test result:' "$out"
rm -rf "$probe"
```
