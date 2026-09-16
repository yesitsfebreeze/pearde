---
complexity: low
footprint:
  - .gitmodules
  - .cartridge/init.lua
---

# spec02 — prove the composition is clean after gitfs.ctg was retired

Base: superproject `/Users/feb/dev/cartridge` at `65a1810`, with `9a84e46`
("Drop the gitfs submodule, absorbed into fs", the user's own commit) an
ancestor of HEAD.

**`repo:` must move from `/Users/feb/dev/cartridge/fs.ctg` to
`/Users/feb/dev/cartridge`, and the footprint from
`/Users/feb/dev/cartridge/.cartridge/config.lua` to the two paths above.
Collect with NO lane.** Reasons in "Option chosen".

## Option chosen

**No change in any repository. This slice is verification only.**

The PRD's question was answered (b) by the user, and the user landed the work
himself in `9a84e46`. Every line of it is already on disk:

- `.gitmodules` has no `submodule "gitfs.ctg"` stanza (18 stanzas, none gitfs);
  `git ls-files --stage -- gitfs.ctg` is empty; no `gitfs.ctg` directory exists
  under the cartridge root.
- `.cartridge/init.lua` never listed gitfs again after `3979437` (2026-09-15);
  its 19 entries are the 19 `cartridge help` reports as enabled.
- `fs.ctg/cartridge.json` is the only manifest in the composition that names
  `tool.gitfs` or `tool.ship` at all — `cartridge ledger` resolves both keys to
  the single row `fs.ctg  (fs)`, so the second-provider refusal at
  `cartridge.ctg/src/host/plan.rs:244` has nothing to fire on.
- `cartridge help` now prints `19 cartridges enabled, 0 installed and not
  enabled` (it printed `1 installed and not enabled`, gitfs, before `9a84e46`).
  The count is `modules.len() - 1 - enabled` at
  `cartridge.ctg/src/cli/manual.rs:335-337` over the ledger scan of top-level
  directories holding a `cartridge.json`.
- The live host has all 19 cartridges `"state":"active"` (`cartridge status`),
  and fs's branch-backed write/read path answers end to end through it.

So the ladder stops at rung 1: **there is nothing to build.** Rejected
alternatives, both of which would be invented work:

- *Add a bun regression test that asserts `0 installed and not enabled`.*
  Rejected: `cartridge setup` deliberately lets a project install a cartridge
  and leave it out of `init.lua`, so the invariant is false in general; the
  overview line already reports it on every `cartridge help`.
- *Clean the `gitfs.ctg` strings still in
  `prd.ctg/.cartridge/reports/record-migration/manifest.json`.* Rejected: that
  file is a historical record of where records came from, not a live reference.

Three references that look dangling and are **correct as they are** — do not
touch them:

- The `gitfs` planning board (`boards/gitfs/settings.md`) keeps the owner alias
  with `repo: /Users/feb/dev/cartridge/fs.ctg`, by design.
- `.cartridge/config.lua` policy rows `gitfs = "allow"` and `ship = "allow"`
  are *tool* names, and fs serves both.
- `.cartridge/config.lua` `fs = { store_dir = ".cartridge/gitfs" }` is fs's own
  declared setting key.

## Why repo, footprint and "no lane" must change

- **repo → the superproject.** Every box is a claim about the composition root:
  the installed `*.ctg` set, `.cartridge/init.lua`, `.gitmodules`, and the host
  composed from them. None of that is inside `fs.ctg`.
- **footprint → `.gitmodules`, `.cartridge/init.lua`.** A footprint is required
  (`prd.ctg/src/lifecycle.ts:31`) but need not be dirty: with nothing changed,
  `collect` skips the commit (`lifecycle.ts:167`) and the receipt records HEAD.
  These two paths are exactly what would have to change for the outcome to
  become false again — a re-added submodule stanza, or a re-added composition
  entry. Both are tracked and clean.
  The current footprint is also *unusable*: `collect` maps each foot with
  `path.relative(code, f)` (`lifecycle.ts:133,142,173`), so
  `/Users/feb/dev/cartridge/.cartridge/config.lua` under `repo: fs.ctg` becomes
  `../.cartridge/config.lua` and escapes the repo.
- **No lane.** A lane is a worktree of `repo`
  (`prd.ctg/.cartridge/boards/gitfs/.lanes/gitfs-is-back-in-the-composition`);
  a worktree of the superproject has empty submodule directories, so pass 1
  would find no cartridges and every block below would fail. `collect` uses the
  lane only if that directory exists (`lifecycle.ts:130`), so the coordinator
  simply must not create it. None exists today.

## Steps

1. Coordinator sets `repo: "/Users/feb/dev/cartridge"` and
   `footprint: [".gitmodules", ".cartridge/init.lua"]` on the PRD, publishes
   this spec, and collects **without creating a lane**.
2. Nothing else. No file in any repository is edited. If a step wants to write
   under `src/`, a manifest or `init.lua`, stop and report: the retirement
   already landed in `9a84e46` and the diff would be churn.

## Acceptance

- [x] `cartridge help` reports no cartridge as "installed and not enabled", and
      no `gitfs.ctg` remains in `.gitmodules`, the index, the worktree or
      `.cartridge/init.lua`.
- [x] fs is the single provider of `tool.gitfs` and `tool.ship`: `cartridge
      ledger` resolves each key to exactly one installed cartridge, `fs.ctg`,
      and `fs.ctg/cartridge.json` is the only manifest in the composition that
      names either key — so `cartridge.ctg/src/host/plan.rs:244` cannot fire.
- [x] The host starts cleanly — every cartridge of the running host is
      `active`, none failed on a duplicate key — and fs's write/read path still
      passes end to end through it: a `tool.write` commits on
      `refs/gitfs/<session>`, `tool.read` reads it back, `tool.gitfs ls` shows
      the branch, and the worktree is untouched.

## Verify and Proof

<!--
Blocks run as `sh -eu -c`, 120 s each, cwd = the repo root (the superproject),
paths relative to it. No lane, so each block runs once, in `repo`. No cargo
here on purpose: a cold isolated CARGO_TARGET_DIR would not fit 120 s, and
building in the live checkout hot-restarts cartridges other sessions are using.
`cartridge help` exits non-zero today for an unrelated reason — `host` ships no
`.cartridge/help.md`, so `print_overview` returns the broken count
(`cartridge.ctg/src/cli/manual.rs:345-355`) — so its status is tolerated and
the overview line is the gate.
-->

```sh
bin="${CARTRIDGE_BIN:-cartridge}"
test -f .gitmodules
test -f .cartridge/init.lua
if test -e gitfs.ctg; then echo "gitfs.ctg is still installed under the cartridge root"; exit 1; fi
if git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | grep -q 'gitfs\.ctg'; then echo ".gitmodules still registers gitfs.ctg"; exit 1; fi
if git ls-files --stage -- gitfs.ctg | grep -q .; then echo "a gitfs.ctg gitlink is still in the index"; exit 1; fi
if grep -qn 'gitfs' .cartridge/init.lua; then echo ".cartridge/init.lua still composes a gitfs cartridge"; exit 1; fi
out=$("$bin" help </dev/null 2>&1 || true)
printf '%s\n' "$out" | head -1
printf '%s\n' "$out" | head -1 | grep -q ', 0 installed and not enabled$'
if printf '%s\n' "$out" | grep -qn 'gitfs\.ctg'; then echo "cartridge help still lists gitfs.ctg"; exit 1; fi
```

```sh
bin="${CARTRIDGE_BIN:-cartridge}"
test -f fs.ctg/cartridge.json
led=$("$bin" ledger </dev/null 2>&1)
# One installed cartridge per key. Rows start at column 0; resolved needs are indented.
gitfs_owners=$(printf '%s\n' "$led" | grep -E '^[^[:space:]].*[[:space:]]tool\.gitfs(,|$)' || true)
ship_owners=$(printf '%s\n' "$led" | grep -E '^[^[:space:]].*[[:space:]]tool\.ship(,|$)' || true)
printf 'tool.gitfs owners:\n%s\ntool.ship owners:\n%s\n' "$gitfs_owners" "$ship_owners"
test "$(printf '%s\n' "$gitfs_owners" | grep -c .)" -eq 1
test "$(printf '%s\n' "$ship_owners" | grep -c .)" -eq 1
printf '%s\n' "$gitfs_owners" | grep -q '^fs\.ctg  (fs)  '
printf '%s\n' "$ship_owners" | grep -q '^fs\.ctg  (fs)  '
# And on disk: exactly one manifest in the composition names either key at all.
declarers=$(grep -l '"tool\.gitfs"' ./*.ctg/cartridge.json ./*.ctg/*/cartridge.json 2>/dev/null | sort -u)
printf 'tool.gitfs manifests: %s\n' "$declarers"
test "$declarers" = "./fs.ctg/cartridge.json"
declarers=$(grep -l '"tool\.ship"' ./*.ctg/cartridge.json ./*.ctg/*/cartridge.json 2>/dev/null | sort -u)
printf 'tool.ship manifests: %s\n' "$declarers"
test "$declarers" = "./fs.ctg/cartridge.json"
```

```sh
bin="${CARTRIDGE_BIN:-cartridge}"
st=$("$bin" status </dev/null 2>&1)
printf '%s' "$st" | grep -q '"id":"fs"'
if printf '%s' "$st" | grep -o '"state":"[a-z]*"' | grep -v '"state":"active"'; then echo "a cartridge of the running host is not active"; exit 1; fi
echo "cartridges active: $(printf '%s' "$st" | grep -o '"state":"active"' | grep -c .)"
sid=$("$bin" call sessions '{"op":"create"}' </dev/null | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')
test -n "$sid"
probe=".cartridge/gitfs-composition-probe.txt"
ctx="{\"session\":\"$sid\",\"run\":\"$sid:1\",\"call\":\"gitfs-composition-w\",\"cwd\":\"$PWD\"}"
w=$("$bin" call tool.write "{\"op\":\"call\",\"context\":$ctx,\"input\":{\"path\":\"$probe\",\"text\":\"gitfs-composition-probe\n\"}}" </dev/null 2>&1)
echo "write: $w"
printf '%s' "$w" | grep -q '"error":false'
printf '%s' "$w" | grep -q "refs/gitfs/$sid"
ctx="{\"session\":\"$sid\",\"run\":\"$sid:1\",\"call\":\"gitfs-composition-r\",\"cwd\":\"$PWD\"}"
r=$("$bin" call tool.read "{\"op\":\"call\",\"context\":$ctx,\"input\":{\"path\":\"$probe\"}}" </dev/null 2>&1)
echo "read: $r"
printf '%s' "$r" | grep -q '"error":false'
printf '%s' "$r" | grep -q 'gitfs-composition-probe'
ctx="{\"session\":\"$sid\",\"run\":\"$sid:1\",\"call\":\"gitfs-composition-l\",\"cwd\":\"$PWD\"}"
l=$("$bin" call tool.gitfs "{\"op\":\"call\",\"context\":$ctx,\"input\":{\"op\":\"ls\"}}" </dev/null 2>&1)
echo "ls: $l"
printf '%s' "$l" | grep -q '"error":false'
printf '%s' "$l" | grep -q "refs/gitfs/$sid"
if test -e "$probe"; then echo "git-mode write leaked into the worktree"; exit 1; fi
```

## Remaining risk

- Block 3 needs the project daemon answering. That is the claim ("the host
  starts cleanly"), so a missing host must fail the block rather than be
  skipped — but it means this PRD cannot be collected with the daemon down.
  Nothing here starts, stops or reloads it.
- Block 3 creates one session and one `refs/gitfs/<session>` commit in fs's
  store (`.cartridge/gitfs`, gitignored). It never materializes, so the
  worktree and the footprint stay clean — confirmed by the last guard.
- `cartridge help` exiting non-zero because `host` ships no `.cartridge/help.md`
  is a separate, pre-existing defect. It is out of this footprint and belongs
  in its own PRD.
