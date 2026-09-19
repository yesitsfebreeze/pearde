---
complexity: small
footprint:
  - .gitmodules
  - .cartridge/init.lua
  - .cartridge/justfile
  - .cartridge/memos/routine/cartridge-development.md
---

# spec01 — land checks.ctg in the composition

Sequenced after the sibling child `the-checks-cartridge-exists-and-runs-a-repository-s-declared-checks`, whose spec builds the cartridge entirely inside
`checks.ctg`; nothing in the composition knows about it yet. This spec is the
landing step, and it is the reason the PRD's Acceptance 6 (`just test checks`)
cannot be satisfied by spec01 alone.

## The footprint this spec needs, and why it is not the PRD's

The PRD declares `footprint: ["checks.ctg"]`. Four facts about this composition,
each read from the file that carries it, make that footprint insufficient for the
PRD's own acceptance:

1. **Owner target lists.** `/Users/feb/dev/cartridge/.cartridge/justfile`, recipe
   `_fan`, hard-codes the target list per gate:
   `check) all=(runtime agent docs fs harness lsp mcp memo proxy pty router sessions tools memory policy live auth prd)`
   and the `test)` line beside it, which adds `layout` and `lifecycle`.
   `just check checks` and `just test checks` do not resolve until `checks` is in
   both.
2. **Owner dispatch.** `/Users/feb/dev/cartridge/.cartridge/memos/routine/cartridge-development.md`
   is the command implementation behind those gates. Its `_cargo` recipe ends in
   `*) echo "Unknown owner: $module" >&2; exit 2;;`, so an owner not named in the
   `agent|docs|fs|harness|live|lsp|mcp|memo|proxy|pty|router|sessions|tools`
   case arm is rejected by name. The same list is repeated in the `all` loop.
3. **The composition profile.** `/Users/feb/dev/cartridge/.cartridge/init.lua` is
   the one list of cartridges the host loads.
   `.cartridge/memos/routine/audit-cartridges.md` makes "the composition profile
   has an entry for it, and that entry's path resolves to a manifest" a **hard**
   encapsulation failure, so `just audit checks` fails until the entry exists.
   Without it the host never loads the cartridge and `cartridge call checks` has
   nothing to answer.
4. **The submodule.** Every `*.ctg` in this superproject except `web.ctg` is a git
   submodule registered in `/Users/feb/dev/cartridge/.gitmodules`. A collection
   against the superproject records `checks.ctg` as a gitlink only once the
   submodule is registered; otherwise the directory is either untracked — and
   `just audit`'s cleanliness axis reports it — or committed as ordinary files,
   which contradicts "each cartridge is its own repository with its own remote".

None of those four paths is under `checks.ctg`, and the coordinator took the
second of the two options rather than the first: `@root/repo-checks-cartridge`
was refined into two children, and this spec belongs to the registration child,
whose own `footprint:` is exactly the four paths above. The cartridge itself
lands first under the sibling child with `footprint: [checks.ctg]`, and the
parent's Acceptance 6 rides here rather than there.

Widening was refused for a reason worth keeping: `.cartridge/justfile` carries an
uncommitted edit belonging to another live session, and `collect` commits every
dirty path inside the footprint. A widened parent footprint would have swept that
edit into this PRD's receipt. The same four paths are shared with every other
port in the `@root/port-the-flow-engine-and-companion-tool-cartridges` tree and
with cartridge-b0's `jev.ctg`, so these registrations are serial by construction;
b0 registers first by agreement.

`web.ctg` is the precedent that the profile entry, not the submodule, is the part
that cannot be skipped: it is in the profile and in no `.gitmodules` entry, and
the composition loads it.

## Steps

1. **Create the cartridge's own repository and register it.** From the
   superproject root, with `checks.ctg` already populated by spec01:
   `git init` inside `checks.ctg`, commit its contents, then
   `git submodule add https://github.com/yesitsfebreeze/checks.ctg checks.ctg`
   so `/Users/feb/dev/cartridge/.gitmodules` gains the `[submodule "checks.ctg"]`
   block in the shape every sibling uses. **That remote does not exist yet.** This
   is the one product decision in the landing step and it belongs to the
   coordinator, not the implementer: either the remote is created first, or
   `checks.ctg` lands as tracked files of the superproject — as `web.ctg` does
   today — and the submodule conversion becomes a follow-up. Do not invent a
   remote, and do not push to one that was not named.

2. **`/Users/feb/dev/cartridge/.cartridge/init.lua`** — add
   `{ id = "checks", path = "checks.ctg" },` to the profile's service list.
   `checks` needs `memo`, so the entry is ordered after the `memo` entry; placing
   it beside `{ id = "tools", path = "tools.ctg" },` satisfies that.

3. **`/Users/feb/dev/cartridge/.cartridge/justfile`** — in `_fan`, add `checks`
   to the `check)` target list and to the `test)` target list. Nowhere else: the
   cartridge has no smoke fixture, and `verify` and `isolation` already run over
   the whole composition rather than over a named owner.

4. **`/Users/feb/dev/cartridge/.cartridge/memos/routine/cartridge-development.md`**
   — in the embedded `just` block: add `checks` to the `_cargo` `all` owner loop,
   and to the
   `agent|docs|fs|harness|live|lsp|mcp|memo|proxy|pty|router|sessions|tools`
   case arm, whose body already resolves `manifest="$repos/$module.ctg/Cargo.toml"`
   and `package=$module` correctly for a crate named `checks`. No new arm is
   needed. The memo's prose sentence naming what `all` covers is updated in the
   same change, because the memo body is the documentation of the recipe it
   carries.

## Acceptance

- [ ] PRD 6 — `just test checks` runs the cartridge's suite from
      `/Users/feb/dev/cartridge` and reports `test      checks     pass`, and
      `just check checks` runs `cargo fmt --check` plus
      `cargo clippy --all-targets -- -D warnings` for it and reports
      `check     checks     pass`.
- [ ] `just audit checks` reports no hard failure: the manifest parses and carries
      a description, every event has a description and a schema, every setting has
      a type and a doc line, the profile has an entry whose path resolves to a
      manifest, `README.md` has at least ten non-blank lines, and
      `.cartridge/help.md` is non-empty.
- [ ] `just isolation` reports nothing for `checks`: no reached-for key it did not
      declare, and no path into a sibling checkout.
- [ ] `/Users/feb/dev/cartridge/.gitmodules` carries a `checks.ctg` entry, or the
      coordinator has recorded the decision to land it as tracked files first.

## Verify and Proof

<!--
Same engine facts as spec01: `sh -eu -c`, 120 s, empty stdin, no injected
environment, run once in the lane worktree and once in /Users/feb/dev/cartridge,
paths relative to the repo root, no `cd` to an absolute checkout, isolated
CARGO_TARGET_DIR for anything that compiles.

What each block costs. `just audit` and `just isolation` are bun scripts over the
whole composition and take about a second each. `just check checks` and
`just test checks` compile the crate; spec01's retaken measurement was 13.65 s
compile / 17 s wall from an empty CARGO_TARGET_DIR with tokio in the dep set, so
both fit the 120 s ceiling with a large margin. Every gate here first runs the
`tools` recipe, which requires cargo, cargo-nextest, bun and tmux on PATH and
names any that are missing.

Why these blocks and not a grep of the four files. The finding this spec exists
to fix is registration, and registration is only real if the dispatcher resolves
it. A grep for the string `checks` in `.cartridge/justfile` passes on a comment.
Running the gate does not.
-->

The composition's own gates accept the cartridge as one of its own:

```sh
just audit checks
just isolation
```

Registration is reachable through the owner dispatcher, not merely present as
text. A target the `_fan` list does not carry never reaches `_one`; a target the
`_cargo` case arm does not name prints `Unknown owner` and exits 2. Both are
caught here, and `_fan` prints `FAIL` rather than exiting non-zero for some
per-target failures, so the verdict line is inspected as well as the exit status:

```sh
out=$(just check checks 2>&1) || {
  printf '%s\n' "$out"
  echo "the composition does not gate this cartridge as one of its owners" >&2
  exit 1
}
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -qn 'Unknown owner'; then
  echo "the owner dispatcher does not recognise this cartridge" >&2
  exit 1
fi
if printf '%s\n' "$out" | grep -qn 'FAIL'; then
  echo "an owner gate failed for this cartridge" >&2
  exit 1
fi
```

The profile entry resolves to a real manifest, which is what `just audit` calls a
hard encapsulation failure when it does not. Read from the profile rather than
asserted about it, so a commented-out entry does not pass:

```sh
bun -e '
  const fs = require("node:fs");
  const profile = fs.readFileSync(".cartridge/init.lua", "utf8");
  const live = profile
    .split("\n")
    .filter((line) => !line.trim().startsWith("--"))
    .join("\n");
  const entry = [...live.matchAll(/\{\s*id\s*=\s*"([^"]+)"\s*,\s*path\s*=\s*"([^"]+)"/g)]
    .find(([, id]) => id === "checks");
  if (!entry) { console.error("the composition profile does not compose this cartridge"); process.exit(1); }
  if (!fs.existsSync(entry[2] + "/cartridge.json")) {
    console.error("the profile entry points at a path that carries no manifest: " + entry[2]);
    process.exit(1);
  }
  console.log("the profile composes " + entry[1] + " from " + entry[2]);
'
```

The suite itself, through the composition's own gate rather than a bare cargo
call, so registration and behaviour are proved by one command:

```test
run: sh -c 'export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/checks-verify}"; just test checks'
pass: discovery_records_each_declared_check_with_its_command_and_source
pass: a_repository_declaring_no_check_records_an_empty_set
pass: selection_names_only_checks_reaching_the_changed_files_and_the_declared_verify
pass: the_selection_is_announced_before_any_check_runs
pass: the_post_pass_runs_exactly_its_reported_selection_and_the_gate_runs_the_rest
pass: the_post_pass_stops_at_the_first_failing_check_and_reports_its_output
pass: discovery_and_selection_invoke_no_tool_from_the_path
pass: the_recorded_set_round_trips_through_the_record_owner
```
