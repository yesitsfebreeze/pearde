---
complexity: small
footprint:
  - .cartridge/tests/integration/smoke.test.ts
---

# spec01: the mcp smoke case starts cold

The smoke fixture's `mcp` case runs `cartridge mcp` against a project with no
daemon. It no longer starts a daemon itself or polls `status` until the host
settles first.

## Change

In `.cartridge/tests/integration/smoke.test.ts`, `mcp` branch only:

- Delete the `// Pre-settled: ...` comment. It names
  `@root/cartridge-mcp-waits-for-a-cold-host-to-settle-...`.
- Delete the `Bun.spawn([...command, "daemon"], ...)`, the `stderr` promise,
  the settle loop, the `try { ... } finally { await stop(daemon); }` and the
  `let out`.
- Replace them with one line:
  `const out = await ok([...command, "mcp"], cwd, env, messages.map(m => JSON.stringify(m) + "\n").join(""), 25_000);`
- Keep the assertions after that line as they are. The `proxy` branch, `stop`,
  `reap`, `profile` and the timeouts stay the same. `stop` is still used by
  `proxy`. The daemon that `cartridge mcp` spawns (`cartridge --dir
  <root>/mcp/builtin daemon ...`) is still cleaned up by `reap(root)` in the
  outer `finally`: `reap` matches it by argv, and its `cartridge node`
  children by binary and cwd.

## Acceptance

- [x] The `mcp` case no longer starts a daemon before `cartridge mcp`. All
      three cases of this file pass in one combined run (Verify block 1). The
      `mcp` case then passes cold 10 more times in a row (Verify block 2).
- [x] The comment naming the cold-host PRD is gone, and only the `proxy` case
      still starts a daemon itself (Verify block 3).
- [x] Not gated: with the cold-host fix reverted, a cold `mcp` run fails about
      1 time in 5 (recorded: 2 of 12 against this spec's exact variant). The
      11 cold runs in blocks 1 and 2 catch such a revert about 91% of the time
      (1 − 0.8^11). This box is ticked from the recorded run, and the diff
      reviewer confirms that the committed `mcp` branch is that variant (see
      "Box 3" below).

## Verify

What blocks 1 and 2 need, and what the receipt records:

- **They need the live debug host.** Blocks 1 and 2 run
  `cartridge.ctg/target/debug/cartridge` and the live module dylibs. They
  build nothing, and they clear `CARTRIDGE_YOLO`, `CARGO_TARGET_DIR` and
  `CARTRIDGE_SMOKE_BUILT`, so they match `just smoke`. The debug host must be
  built at or after `cartridge.ctg` `d169293`, the cold-host fix. A stale
  debug binary turns the cold runs red for a reason unrelated to this diff:
  run `just build runtime` first.
- **The lane pass skips.** In a superproject lane, `cartridge.ctg` is a fresh
  worktree with no `target/`, and the module dylibs are missing too, so the
  host cannot run there. The lane pass says so and exits 0.
- **The repo pass cannot skip.** There `.git` is a directory, and a missing
  host fails the block.
- **The receipt keeps pass 2's output.** With a lane, `collect` replaces pass
  1's evidence with pass 2's, so the receipt records the repo run, never the
  lane's skip message. With no lane, the single pass runs in the repo.
- **Recovery:** pass 2 runs after the fast-forward. If it fails there (a
  timeout, or a live module rebuilt by another session mid-run), the change
  is already on HEAD. Rerun `prd collect` once the host is quiet (`cartridge
  status` shows every cartridge active).

Block 1 is the combined run. Measured with the change applied, meaning the
cold variant with the same text and the path pointing at a scratch copy: exit
0 in 12 s at load average 30.

```sh
if [ ! -x cartridge.ctg/target/debug/cartridge ]; then
  if [ -d .git ]; then echo "repo pass: no built host at cartridge.ctg/target/debug/cartridge" >&2; exit 1; fi
  echo "lane pass: a superproject lane has no built host or module libraries; the repo pass runs the smoke"
  exit 0
fi
out="$(mktemp -d)"
env -u CARTRIDGE_YOLO -u CARGO_TARGET_DIR -u CARTRIDGE_SMOKE_BUILT CARTRIDGE_SMOKE=all \
  bun test --reporter=junit --reporter-outfile="$out/all.xml" ./.cartridge/tests/integration/smoke.test.ts
for name in "policy: real isolated protocol" "mcp: real isolated protocol" "proxy: real isolated protocol"; do
  if grep -qF "name=\"$name\"" "$out/all.xml"; then :; else echo "smoke case did not run: $name" >&2; exit 1; fi
done
if grep -qE '<failure|<skipped|<error' "$out/all.xml"; then echo "a smoke case failed or skipped" >&2; exit 1; fi
rm -rf "$out"
```

Block 2 is the 10 cold `mcp` runs. Measured the same way: exit 0 in 52 s at
load average 29–30 (43% of the 120 s cap). The review measured 3.5–7.3 s per
run at load 20.

```sh
if [ ! -x cartridge.ctg/target/debug/cartridge ]; then
  if [ -d .git ]; then echo "repo pass: no built host at cartridge.ctg/target/debug/cartridge" >&2; exit 1; fi
  echo "lane pass: a superproject lane has no built host or module libraries; the repo pass runs the smoke"
  exit 0
fi
out="$(mktemp -d)"
i=0
while [ "$i" -lt 10 ]; do
  env -u CARTRIDGE_YOLO -u CARGO_TARGET_DIR -u CARTRIDGE_SMOKE_BUILT CARTRIDGE_SMOKE=mcp \
    bun test --reporter=junit --reporter-outfile="$out/mcp-$i.xml" ./.cartridge/tests/integration/smoke.test.ts
  if grep -qF 'name="mcp: real isolated protocol"' "$out/mcp-$i.xml"; then :; else echo "cold mcp run $i did not run the mcp case" >&2; exit 1; fi
  if grep -qE '<failure|<skipped|<error' "$out/mcp-$i.xml"; then echo "cold mcp run $i failed" >&2; exit 1; fi
  i=$((i + 1))
done
rm -rf "$out"
```

Block 3 is structural and needs no host. Measured at HEAD: exit 1 with "still
names the cold-host PRD", as it should while the workaround is present. Against
the cold variant: exit 0.

```sh
f=.cartridge/tests/integration/smoke.test.ts
if grep -qF 'cartridge-mcp-waits-for-a-cold-host' "$f"; then echo "the smoke fixture still names the cold-host PRD" >&2; exit 1; fi
n="$(grep -c '"daemon"\]' "$f" || true)"
if [ "$n" != 1 ]; then echo "the mcp case still starts its own daemon before cartridge mcp" >&2; exit 1; fi
```

## Box 3: why no Verify block gates it

- **The defect is a race.** A single cold run against a host with the fix
  reverted fails only about 1 time in 5. The cold-host PRD's verifier measured
  5 failures in 24 runs (21%). This analyst measured 2 in 12 (17%), each with
  `` service `mcp` unavailable: no active listener ``. With the fix, the same
  variant passed every run: 18 by the analyst and 12 by the reviewer.
- **Building a mutant does not fit the Verify rules.** The mutant is HEAD's
  `cartridge.ctg` with `git diff d169293^ d169293 -- src/cli/host.rs` applied in
  reverse (it applies cleanly). It built in 16 s, but only because the global
  `kache` rustc-wrapper cache was warm; a cold build is untested. Then about 20
  cold runs are needed to push the chance of a false pass near 1%. Every block
  runs twice, and the lane has no module dylibs. A red in the repo pass could
  not tell a real regression from a flake or from another session restarting
  the shared host.
- **Where the proof lives:** the recorded run above (recipe in analyst-1.md),
  plus the diff reviewer checking that the committed `mcp` branch is exactly
  the measured variant: a bare `ok([...command, "mcp"], ..., 25_000)` with
  no daemon spawn and no settle loop.

## Out of scope

- **`just smoke` is red for another reason.** It exits 1 at HEAD because
  `mcp.ctg/.cartridge/tests/integration/refresh.test.ts:93` expects the tool
  list `['alpha']`, and the host now also contributes `asp`.
  `@mcp/the-mcp-refresh-test-expects-the-host-s-synthetic-asp-tool` owns that
  failure. Blocks 1 and 2 therefore gate this file's cases directly.
- **Run directories pile up.** Every fixture run leaves a run directory under
  the shared socket base `/tmp/cartridge-501` (about 1784 entries at review).
  This PRD's 11 runs per pass add to them. Cleaning them up is not this
  footprint's job.
