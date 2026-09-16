---
complexity: small
footprint:
  - src/proxy.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
---

# spec01 — Serve every listed model on the single-model surfaces

Base: `router.ctg` `effe3c5f57b634996a810c98bef756c90c630682`, with the existing implementation in `src/proxy.rs` and the existing regression test in `.cartridge/tests/unit/proxy/capabilities.rs`.

The listing route is not enough. Claude Code validates the configured model by retrieving one model id before using it, so `/v1/models/<id>` and `/models/<id>` must agree with `/v1/models` and `/models`.

## Acceptance

- [x] `GET /v1/models/<id>` returns 200 for every id the listing publishes, with the percent-encoded form of a `:` accepted.
- [x] An id the listing does not publish returns 404.
- [x] `/models/<id>` behaves as `/v1/models/<id>`, as the listing pair does.
- [x] A test covers both forms, both spellings of the separator, and the unknown-id case.

## Verify and Proof

<!--
How collect runs these blocks (engine facts, src/lifecycle.ts collect/verify):
- Each sh/bash/shell block runs as `sh -eu -c`, 120 s limit, empty stdin, the
  collector's environment.
- It runs twice: first with cwd = the lane, a worktree of the PRD's `repo` at
  `prd.ctg/.cartridge/boards/<board>/.lanes/<slug>`; then, after the
  fast-forward, with cwd = `repo` itself. With no lane it runs once, in `repo`.
- Paths are relative to the repo root. Never `cd` to an absolute checkout, or
  pass 1 tests the wrong tree. `../<sibling>.ctg` does not resolve from the
  lane either; name absolute tools (e.g. CARTRIDGE_BIN) with an env default.
- Pass 2 runs in the live checkout. The host hot-restarts a cartridge when its
  target/debug dylib changes, so every cargo block first sets
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/<slug>-verify}"`.
- A block must not write inside the footprint. In the lane pass, collect
  commits such writes; in pass 2 they abort collection with "source footprint
  changed during integrated verification". Write scratch output elsewhere.
-->

Block 1 — run the behavioral regression test and prove it is present.

```sh
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/listed-model-retrieve-verify}"
log="$(mktemp)"
trap 'rm -f "$log"' EXIT
cargo test a_listed_model_is_also_retrievable_by_id --lib > "$log" 2>&1 || { cat "$log"; exit 1; }
cat "$log"
if ! grep -q "a_listed_model_is_also_retrievable_by_id .* ok" "$log"; then
    echo "the suite no longer runs a_listed_model_is_also_retrievable_by_id"
    exit 1
fi
```

Block 2 — pin the surface cases in the test source so a renamed or weakened test does not satisfy this PRD.

```sh
test -f .cartridge/tests/unit/proxy/capabilities.rs
for needle in \
    '"/v1/models/auto:code"' \
    '"/v1/models/auto%3Acode"' \
    '"/v1/models/auto"' \
    '"/models/auto:code"' \
    '"/v1/models/auto:nonsense"' \
    'assert_eq!(get(path.to_owned()).await, 200, "{path}")' \
    'assert_eq!(get("/v1/models/auto:nonsense".to_owned()).await, 404)'
do
    if ! grep -Fq "$needle" .cartridge/tests/unit/proxy/capabilities.rs; then
        echo "missing regression proof: $needle"
        exit 1
    fi
done
```

## Denied worlds

Observed against the implementation while preparing this record: before the `src/proxy.rs` single-model branch, `/v1/models/auto:code`, `/v1/models/auto`, and `/v1/models/claude-opus-5` fell through to `unknown endpoint` and returned 404 even though the listing and routing path served the same selectors. Removing the branch, the percent-decoding, either `/models/` prefix, or the unknown-id check makes one of the source-pinned cases fail.
