---
complexity: small
footprint:
  - /Users/feb/dev/cartridge/justfile
  - /Users/feb/dev/cartridge/.cartridge/justfile
---

# spec01 — One gate runner in `.cartridge/justfile`

`check`, `test`, `smoke`, `verify` and `isolation` stop being five unrelated
delegations and become one shape: name the toolchain, fan a target list, report
every target, fail if any target failed.

- `.cartridge/justfile` derives `root` from `source_directory()` rather than
  `justfile_directory()`, so the same paths resolve whether the file is imported
  by the root justfile or named directly with `--justfile`.
- `tools` reports any missing member of `cargo cargo-nextest bun tmux` by name
  and exits 2. Every gate runs it before its first target.
- `_fan` expands `all` into the gate's target list, runs `_one` per target
  without stopping at a failure, prints `<gate> <target> pass|FAIL` per target,
  and exits 1 when any target failed.
- `_one` dispatches one target to the owner that implements it: the development
  memo for `check` and `test`, the smoke memo for `smoke`, the isolation memo
  for `isolation`, the built host for `verify`. The composed repository's own
  `source-layout` test is a `test` target named `layout`, because the gate owns
  the target list and the development memo only ever sees one owner at a time.
  `verify` resolves the host through `CARGO_TARGET_DIR` exactly as the runtime
  memo does.
- The root justfile keeps only `prd` and the import; `isolation` moves into
  `.cartridge/justfile` with the other gates.

## Acceptance

- [ ] `just tools` from the composed root names the four tools and exits 0, and with those tools off `PATH` it reports them as missing and exits 2.
- [ ] `just isolation` prints one `isolation composition pass` line and exits 0, and `just --justfile .cartridge/justfile isolation` behaves identically.
- [ ] A target that cannot run prints a `FAIL` verdict line for that target and makes the gate exit non-zero.
- [ ] The composed repository's `source-layout` test is a target of the `test` gate and gets its own verdict line.

## Verify and Proof

```sh
cd /Users/feb/dev/cartridge
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# The toolchain is named before any target runs.
just tools | grep -qx 'toolchain: cargo cargo-nextest bun tmux'

# With none of them on PATH, each missing tool is named and the gate refuses.
ln -s "$(command -v just)" "$work/just"
PATH="$work:/usr/bin:/bin" just tools > "$work/tools.out" 2>&1 && {
  echo 'a missing toolchain must fail before any target runs' >&2; exit 1; }
grep -q 'toolchain: missing cargo cargo-nextest bun tmux' "$work/tools.out"

# One verdict line per target, from the composed root and from the file itself.
just isolation | grep -Eq '^isolation +composition +pass$'
just --justfile .cartridge/justfile isolation | grep -Eq '^isolation +composition +pass$'

# A target that cannot run is reported as FAIL and fails the gate.
just check nosuch > "$work/check.out" 2>&1 && {
  echo 'a failing target must fail the gate' >&2; exit 1; }
grep -Eq '^check +nosuch +FAIL$' "$work/check.out"

# The composed repository's own layout test is a target, not a tail of one
# owner's run. Its verdict line must appear whichever way the test goes.
just test layout > "$work/layout.out" 2>&1 || true
grep -Eq '^test +layout +(pass|FAIL)$' "$work/layout.out"

echo 'gate contract holds'
```
