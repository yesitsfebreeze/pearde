---
state: open
origin: requested
priority: 40
repo: "/Users/feb/dev/cartridge"
---

# kasuri names the system and each kasuri directory ends in ki

## Outcome

The system is renamed from `cartridge` to `kasuri`, and the word is self-similar:
the whole system is Kasuri, and each unit loaded into it is also a kasuri. There
is no second noun. A unit's directory ends in `.ki` instead of `.ctg`, and the
configuration directory becomes `.ki/` instead of `.cartridge/`, so one suffix
carries the whole scheme.

Kasuri is the Japanese ikat weave in which the threads are resist-dyed before
weaving, so the pattern emerges from the weave rather than being printed on top.
`ki` is 生地, the cloth itself.

The self-similar naming is not a new convention. The repository already works
this way: `cartridge.ctg` is the host crate — crate name `cartridge` — and it
sits in a `.ctg` directory alongside the loadable units, wearing the same suffix
without being loadable itself. The system and its parts already share one word
and one shape. This PRD substitutes the word and changes nothing structural.

Ambiguity between the system and a unit is resolved the way it already is, by
the runtime nouns that stay untouched: `host` is the runtime that loads them,
`node` is a loaded instance in memory, `daemon` is the process. "Restart the
kasuri" is ambiguous; "restart the node" is not, and that is the sentence the
code and the memos already use.

The word `fabric` also keeps its current internal meaning — it is load-bearing in
`event-fabric`, `fabric-announce` and the memo tool's `{"op":"fabric"}` — and this
rename does not touch it.

Name availability was checked before this PRD was written: `kasuri` is free on
crates.io, npm and PyPI, and `kasuri.sh` is unregistered, while `.dev`, `.io` and
`.com` are taken. Known minor collisions: searching `kasuri` alone surfaces
*kasuri methi* (fenugreek); `.ki` is the Kiribati ccTLD; `ki` is the integral gain
in PID code. None affects a binary name or a directory suffix.

### `.ki/` as the configuration directory

Using one suffix for both the unit directory and the configuration directory is
safe here, because nothing in the code matches on the suffix. Units are listed by
explicit path in `.cartridge/init.lua` — `{ id = "auth", path = "auth.ctg" }` —
never globbed and never selected by extension; no Rust, Lua or TypeScript source
compares a path against `ctg` at all. A dotted `.ki/` and a suffixed `memo.ki`
therefore cannot be confused by any existing code path. The rule to preserve is
that they must stay distinguishable in anything added later: a shell glob `*.ki`
does not match `.ki`, and Rust's `Path::extension()` returns `None` for `.ki`, but
a naive `ends_with(".ki")` matches both, so suffix matching must not be
introduced.

The visible consequence is nesting: a unit carries its own configuration
directory, so `prd.ctg/.cartridge/` becomes `prd.ki/.ki/`. This is unambiguous
and has precedent in a bare `foo.git` holding `.git` internals.

This finding also narrows the unit-directory rename: because no code parses the
suffix, moving `*.ctg` to `*.ki` is git plumbing, `.gitmodules`, `init.lua`,
Cargo path dependencies and documentation — not a parser change.

### The data directory moves with the same rule

A kasuri keeps everything it generates in one of two places, and the rename
applies to both identically, with no special cases:

- `~/.cartridge/` — the machine scope: `catalog.json`, `config.lua`, whatever
  `$CARTRIDGE_HOME` points at. Becomes `~/.ki/`.
- `<project>/.cartridge/` — the project scope. Becomes `<project>/.ki/`.

This is already one rule in the code rather than two code paths: given a scope
directory, the data is at `<scope>/.cartridge/`. `src/cli/setup.rs` resolves it as
`root.join(".cartridge")`, `trust.rs` tests `dir.join(".cartridge/init.lua")`, and
`manual.rs` reads `dir.join(".cartridge").join(PAGE)`. A unit is itself a project,
so a unit's own data lives at `<name>.ki/.ki/` by the same rule and needs no
separate treatment. Nineteen such directories exist today, holding roughly 40,000
files — `prd` 14,571, `policy` 12,393, `memory` 7,431, the superproject 4,449,
`cartridge` 1,109, the rest a few dozen each.

The rule being uniform is what makes the change tractable, but the name is not
written down once. `.cartridge` is a scattered string literal: 55 occurrences in
the host's `src/` alone and roughly 850 files across the submodules (`prd` 621,
`memory` 119, `memo` 31, `cartridge` 28, `fs` 22, the rest smaller). Editing 850
files by substitution is how a path typo reaches production. Introduce the name
as one constant first, as a behaviour-preserving change that lands and passes the
gates on its own, then change that constant's value.

Two operational facts for the implementer:

- Moving the machine scope is the only step in this whole rename that fails
  without an error message. If `~/.ki/` is absent and `~/.cartridge/` is present,
  the host starts as though the machine were fresh. It needs a one-time migration
  or a read-through fallback at the constant.
- The superproject and `cartridge.ctg` scopes hold state a running daemon owns —
  `credentials`, `daemon.log`, `live-data`, `live-service`, `live-sessions`,
  `mcp-sessions`, `memory`, `sessions`, `router`, `resolver`. Move them with the
  daemon down or lose sessions and in-flight calls.

### Footprint

The footprint splits in two, and that split is the whole difficulty.

**Things that must resolve.** Roughly 4,100 occurrences across about 450 files in
the 18 submodules and the superproject: crate and binary names, the `CARTRIDGE_*`
environment variables, `.cartridge/` configuration directories, the MCP tool IDs
`mcp__cartridge__*`, the `*.ctg` submodule paths in `.gitmodules`, in
`.cartridge/init.lua` and in every Cargo path dependency, and the justfile. These
fail loudly when missed.

**Things that only record history.** Roughly 50,000 occurrences across about
2,400 files, nearly all inside `prd.ctg/.cartridge/`: 584 PRD bodies, review
artifacts and migration reports. Rewriting that prose would churn 584 revisions,
and the engine refuses state and claim changes it did not itself write.
Historical prose keeps the word `cartridge`, because it is describing what the
thing was called when that work happened. Only the machine-read path fields move:
roughly 1,500 `repo:` and `footprint:` lines whose paths the engine resolves.

Two items carry live blast radius and must be settled before any edit:

- The `mcp__cartridge__*` tool IDs are wired into running sessions and into
  `.mcp.json`. Renaming them mid-flight breaks every attached instance. Decide
  whether the host serves both prefixes for a deprecation window, or whether this
  is a hard cut with every session restarted, and record the decision here.
- `*.ctg` is a git submodule directory name. Renaming it means `git mv` plus
  `.gitmodules` plus `.cartridge/init.lua` plus every `../<name>.ctg` path
  dependency, and the lone-worktree sibling requirement still applies. Decide
  whether submodule directories move in this PRD or in a child.

The analyst may split this into children; the two items above and the
must-resolve/history split are the natural seams.

## Acceptance

- [ ] `kasuri --help` runs from a fresh checkout, and the binary name `cartridge` appears in no tracked file outside historical PRD records.
- [ ] A fresh checkout builds and `just check` and `just test` pass with every unit directory ending in `.ki`, with `.gitmodules`, `init.lua` and every Cargo path dependency resolving.
- [ ] `kasuri help` lists every enabled kasuri, and the host's own directory carries the `.ki` suffix the way `cartridge.ctg` carries `.ctg` today.
- [ ] The host reads its configuration from `.ki/`, and the directory name exists as one constant rather than as a literal repeated across the source.
- [ ] Data resolves at `~/.ki/` for the machine scope and `<project>/.ki/` for the project scope, by the same rule, with a unit's own data at `<name>.ki/.ki/` and no separate code path for it.
- [ ] A host started against a machine that has only `~/.cartridge/` finds its catalog and configuration — by migrating once or by reading the old path — and never starts as if the machine were fresh.
- [ ] The move is performed with the daemon down, and `live-sessions`, `mcp-sessions`, `credentials` and `memory` are readable at their new path afterwards.
- [ ] Every `CARTRIDGE_*` environment variable is read under its `KASURI_*` name, and no `CARTRIDGE_*` name remains in tracked source.
- [ ] `prd scan --board root` resolves every `repo:` and `footprint:` path after the rename, and no PRD `state` or `claim` field was changed by the rename.
- [ ] An attached MCP instance reaches the tools under the decided naming, and the deprecation-window decision is written into this PRD.
- [ ] Historical PRD bodies still read `cartridge`: the rename changed no prose under `prd.ki/.ki/boards/*/prds/*/prd.md` beyond machine-read path fields.
- [ ] `host`, `node` and `daemon` keep their current meanings, and no documentation uses "kasuri" where it means a loaded instance.
