---
complexity: small
footprint:
  - src/transport/settings.rs
  - src/transport/mod.rs
  - src/settings
  - docs/settings.txt
---

# spec01 — move the settings schema from transport into settings/spec.rs

Base: cartridge.ctg `445a87f` (proved there; `324f36e` too). No `needs`.
Behaviour does not change; a module path changes and the manual stops naming
the removed module.

## Users of the old path (all of them, at 445a87f)

`rg --hidden 'transport::settings|transport::\{[^}]*settings|transport/settings'`
over cartridge.ctg (target excluded) finds only:

- `src/settings/mod.rs:8` `pub use crate::transport::settings::{...}` and
  `:18` `crate::transport::settings::apply(...)`. Every other caller in the
  crate, the binary and `.cartridge/tests` already goes through
  `crate::settings::*` / `cartridge::settings::*`, which keeps working
  unchanged.
- `src/transport/mod.rs:3` `pub mod settings;`.
- `docs/settings.txt:89-90`, the manual `cartridge help` serves, shows
  `transport::settings::declared/merge` in an example of a cartridge's own
  `Config::parse`. The cartridges it describes (`fs.ctg/src/service.rs`,
  `proxy.ctg/src/service.rs`, `harness.ctg/src/lib.rs`) call
  `crate::settings::declared/merge`; after this change `transport::settings`
  names nothing, so the example is superseded and changes with it.

No sibling `.ctg` crate imports `cartridge::transport::settings`.

## Steps

1. `mv src/transport/settings.rs src/settings/spec.rs` (plain `mv`: collect refuses a staged index). Change nothing in
   the file (it holds no crate path).
2. `src/transport/mod.rs`: delete the line `pub mod settings;`. Add no
   re-export.
3. `src/settings/mod.rs`: add `mod spec;` after `mod host;`; replace
   `pub use crate::transport::settings::{` with `pub use spec::{`; replace
   `crate::transport::settings::apply(` with `spec::apply(`. Then
   `rustfmt --edition 2021 src/settings/mod.rs` (it moves the `pub use spec`
   line after `pub use host`). Never bare `cargo fmt`.
4. `docs/settings.txt:89-90`: `transport::settings::declared(DOCUMENT)` becomes
   `crate::settings::declared(DOCUMENT)` and `transport::settings::merge(` becomes
   `crate::settings::merge(`. Nothing else in the file changes.
5. Write `src/settings/README.md` in the parent's README shape (defined by the
   sibling `every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it`,
   "The shape": at most 25 lines, headings `# <module>`, `Does:`, `Why:`,
   `Owns:`, `Talks to:`, `Start at:`, in that order, no paragraphs). Draft,
   with `Talks to` taken from the real `use` edges at 445a87f:

   ```
   # settings
   Does:      Turns what a cartridge declares, plus the config files a person wrote, into one checked table of values.
   Why:       Without it every cartridge guesses its own defaults and a wrong-typed or out-of-range value reaches running code.
   Owns:      `Spec`, `Kind`, `Specs`, `Host`, `Sources`
   Talks to:  calls `error`, `trust`, `lua`; called by `host`, `loader`, `node`, `lua`, `trace`, `sandbox`, `trust`, `cli`
   Start at:  `apply` in `spec.rs`: defaults, then the layers merged on top, then each declared key checked
   ```

   If `ledger`/`loader`/`host::plan` have already moved into `composition/`
   when this lands, name `composition` in `Talks to` instead.

Reusable attempt: `scratchpad/analyst-settings/attempt.patch` (steps 1-5,
applies cleanly at 445a87f).

## Acceptance

- [ ] `src/transport/settings.rs` does not exist, and `src/settings/spec.rs` is byte-identical to the last committed `src/transport/settings.rs`.
- [ ] No file under `src/`, `.cartridge/tests/` or `docs/` names `transport::settings`; `src/transport/mod.rs` neither declares nor re-exports `settings`; `src/settings/mod.rs` declares `mod spec;` and re-exports from `spec::`.
- [ ] `src/settings/README.md` exists, is 25 lines or fewer, has the headings `# settings`, `Does:`, `Why:`, `Owns:`, `Talks to:`, `Start at:` once each in that order, and its `Start at` names a function defined under `src/settings`.
- [ ] The footprint's Rust files are rustfmt-clean and `cargo clippy --workspace --all-targets` passes (the `just check runtime` gate).
- [ ] `cargo test --workspace --all-targets -- --list` names exactly the same tests as the same tree with this change's paths put back as they were before it.
- [ ] The nine settings tests pass under their unchanged names.

## Verify

```sh
old=src/transport/settings.rs
if [ -e "$old" ]; then echo "$old still exists" >&2; exit 1; fi
if [ ! -f src/settings/spec.rs ]; then echo "src/settings/spec.rs does not exist" >&2; exit 1; fi
# Before the change: HEAD while the move is uncommitted, else the parent of the commit that removed the file.
if git cat-file -e "HEAD:$old" 2>/dev/null; then before=HEAD; else
  last=$(git rev-list -1 HEAD -- "$old")
  if [ -z "$last" ]; then echo "no commit in HEAD's history holds $old" >&2; exit 1; fi
  before="$last^"
fi
scratch=$(mktemp -d "${TMPDIR:-/tmp}/ctg-settings-spec.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
git show "$before:$old" > "$scratch/moved.rs"
if ! cmp -s "$scratch/moved.rs" src/settings/spec.rs; then echo "src/settings/spec.rs is not the last committed $old unchanged" >&2; exit 1; fi
if grep -rnE 'transport::(settings|\{[^}]*settings)' src .cartridge/tests docs; then echo "the old transport settings path is still named" >&2; exit 1; fi
if grep -nwE 'settings' src/transport/mod.rs; then echo "transport still declares or re-exports settings" >&2; exit 1; fi
if ! grep -qnE '^mod spec;$' src/settings/mod.rs; then echo "settings does not declare its spec module" >&2; exit 1; fi
if ! grep -qnE '^pub use spec::' src/settings/mod.rs; then echo "settings does not re-export from its spec module" >&2; exit 1; fi
```

```sh
f=src/settings/README.md
if [ ! -f "$f" ]; then echo "$f does not exist" >&2; exit 1; fi
lines=$(wc -l < "$f")
if [ "$lines" -gt 25 ]; then echo "$f has $lines lines, more than 25" >&2; exit 1; fi
order=$(grep -oE '^(# settings$|Does:|Why:|Owns:|Talks to:|Start at:)' "$f" | tr '\n' '|')
if [ "$order" != '# settings|Does:|Why:|Owns:|Talks to:|Start at:|' ]; then echo "$f does not have the five headings once each, in order: $order" >&2; exit 1; fi
start=$(sed -n 's/^Start at: *`\([A-Za-z_][A-Za-z0-9_]*\)`.*/\1/p' "$f")
if [ -z "$start" ]; then echo "Start at does not name a function in backticks" >&2; exit 1; fi
if ! grep -rqE "fn $start\b" src/settings; then echo "Start at names $start, which is no function under src/settings" >&2; exit 1; fi
```

```sh
export CARGO_TARGET_DIR="${TMPDIR:-/tmp}/ctg-settings-spec-target"
rustfmt --edition 2021 --check src/settings/mod.rs src/settings/spec.rs src/settings/files.rs src/settings/host.rs src/transport/mod.rs
cargo clippy --workspace --all-targets --quiet
```

```sh
export CARGO_TARGET_DIR="${TMPDIR:-/tmp}/ctg-settings-spec-target"
old=src/transport/settings.rs
# Before the change: HEAD while the move is uncommitted, else the parent of the commit that removed the file.
if git cat-file -e "HEAD:$old" 2>/dev/null; then before=HEAD; else
  last=$(git rev-list -1 HEAD -- "$old")
  if [ -z "$last" ]; then echo "no commit in HEAD's history holds $old" >&2; exit 1; fi
  before="$last^"
fi
scratch=$(mktemp -d "${TMPDIR:-/tmp}/ctg-settings-spec.XXXXXX")
trap 'rm -rf "$scratch"' EXIT
# The tree as it is, with only this change's paths put back as they were.
git ls-files -co --exclude-standard | while IFS= read -r f; do if [ -e "$f" ]; then printf '%s\n' "$f"; fi; done > "$scratch/files"
mkdir "$scratch/before"
tar -cf - -T "$scratch/files" | tar -xf - -C "$scratch/before"
rm -rf "$scratch/before/src/settings"
git archive "$before" src/settings src/transport/mod.rs "$old" docs/settings.txt | tar -xf - -C "$scratch/before"
cargo test --workspace --all-targets --quiet --manifest-path "$scratch/before/Cargo.toml" -- --list > "$scratch/before.raw"
cargo test --workspace --all-targets --quiet -- --list > "$scratch/after.raw"
grep -E ': (test|bench)$' "$scratch/before.raw" | sort > "$scratch/before.txt"
grep -E ': (test|bench)$' "$scratch/after.raw" | sort > "$scratch/after.txt"
if [ ! -s "$scratch/after.txt" ]; then echo "cargo listed no tests" >&2; exit 1; fi
if ! diff "$scratch/before.txt" "$scratch/after.txt" >&2; then echo "the test names differ from before the move" >&2; exit 1; fi
echo "same $(wc -l < "$scratch/after.txt") test names before and after"
```

```test
run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR="${TMPDIR:-/tmp}/ctg-settings-spec-target" cargo test --lib settings -- --test-threads=1
pass: tests::settings::keys_inside_an_absent_optional_table_stay_absent
pass: tests::settings::naming_the_table_fills_the_keys_inside_it
pass: tests::settings::yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it
pass: tests::settings::an_untrusted_project_config_is_refused_at_its_read
pass: tests::settings::a_configuration_file_that_never_returns_is_refused
pass: tests::settings::refused_settings_do_not_wedge_the_process_when_diagnostics_are_on
pass: settings::files::tests::the_listing_reads_each_configuration_file_once
pass: settings::host::tests::an_undeclared_host_key_leaves_the_declared_defaults_standing
pass: tests::host::grant_paths_name_the_project_and_settings
```

Notes on the blocks:

- "Before" is found, not pinned: in the lane pass the move is uncommitted, so
  HEAD still holds `src/transport/settings.rs` and is the before-tree; in pass 2
  the move is committed and the before-tree is the parent of the commit that
  removed the file. An upstream edit to the file before this lands therefore
  moves with it.
- Block 4 lists test names in a copy of the working tree with only this
  change's paths restored from the before-tree, so a peer's uncommitted edit
  elsewhere in the live checkout (pass 2) sits on both sides and does not
  trip it (measured: a dirty extra `#[test]` in `src/cli/args.rs` gives 197 =
  197, green).
- Scratch is `mktemp -d` per run and removed on exit. The cargo target is one
  shared dir in `$TMPDIR` on purpose: it keeps pass 2 and the test block warm,
  cargo's own lock makes concurrent runs safe, and it never touches
  `target/debug`.
- `env -u CARTRIDGE_YOLO`: an inherited `CARTRIDGE_YOLO=1` fails
  `an_untrusted_project_config_is_refused_at_its_read` at base too.
  `--test-threads=1`: the settings tests share process-global
  `CARTRIDGE_HOME` (the reason `just test` uses nextest); run in parallel
  under a cold build's load the same test flaked once. The filter `settings`
  selects exactly these nine of 174 in `--lib`.
- Block 4 does not re-prove the names of tests inside the moved file: it has
  none, and block 1 proves it byte-identical.
