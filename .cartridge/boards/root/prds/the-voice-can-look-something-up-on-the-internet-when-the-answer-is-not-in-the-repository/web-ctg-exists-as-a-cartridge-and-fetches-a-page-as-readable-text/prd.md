---
state: "done"
origin: requested
priority: 78
repo: "/Users/feb/dev/cartridge"
capability-owner: web
footprint:
- "web.ctg"
- ".cartridge/init.lua"
commit: "3dba7f2ab6a958eb1c710fe762aebeb521637e24"
---

# web.ctg exists as a cartridge and fetches a page as readable text

## Outcome

A new TypeScript cartridge in `auth.ctg`'s shape, owning one capability:
reaching the network on purpose. `{op: "fetch", url}` returns
`{url, title, text, bytes, truncated}`. A URL whose host is outside the declared
allowlist, or whose scheme is not `http`/`https`, is refused with a reported
error rather than attempted. `grant.net` names the hosts it may reach.

This child takes no credential and so is not blocked by the backend question on
its sibling `search-returns-ranked-results-each-with-its-source-url`. Only its
`grant.net` line changes once that backend is chosen.

## What the analyst established (2026-09-17, against fd68eae)

- `web.ctg` does not exist; the directory is greenfield.
- The closest sibling in shape is `auth.ctg`: `auth.ctg/cartridge.json:1` (a
  manifest with described, schema'd events, typed and documented settings, a
  `commands` block, `grant` and `listen`), `auth.ctg/init.lua:3`
  (`cartridge.spawn({"bun", cartridge.root .. "/src/main.ts"}, …)`, nineteen
  lines of Lua in total) and `auth.ctg/src/main.ts:5`, whose injected-client
  seam is what keeps its tests off the live network. Copy that seam.
- A Rust cartridge is **not** available inside this footprint: every Rust
  cartridge builds through `../cartridge.ctg/justfile` and is a member of the
  host's Cargo workspace, which would need edits outside the footprint.
  TypeScript plus a `bun` helper is the only shape that stays local.
- **The host reads `grant.net` as a boolean.**
  `cartridge.ctg/src/sandbox/mod.rs:305` emits `(allow network*)` whenever the
  list is non-empty, and `linux.rs:129` and `windows.rs:103` are the same
  switch. The host names in the list are documentation, not a filter — six
  cartridges declare `net: ["*"]` today. So the parent's box 1 ("a network grant
  naming what it may reach") is only true if `web.ctg` enforces its own host
  allowlist before the request. That is why it is an Acceptance box here.
- `just audit` hard checks: the manifest parses and has a `description`; every
  event has a `description` and a `schema`; every setting has a `type` and a
  `doc`; the root `.cartridge/init.lua` has an entry whose `path` resolves to a
  `cartridge.json`; `README.md` has at least ten non-blank lines;
  `.cartridge/help.md` exists and is non-empty. Baseline measured on
  2026-09-17: audit 17 of 17, isolation passed for 17. `web.ctg` is the
  eighteenth and must not break either number.
- `just isolation` checks two things: a source line reaching for a key another
  cartridge provides without declaring it in `needs`, and any file naming
  `../<sibling>.ctg`. A self-contained `web.ctg` with `needs: []` passes both.
  Do not add a Cargo path dependency, a symlink or a `../auth.ctg` reference.

## Acceptance

- [x] `web.ctg/cartridge.json` declares `web` and `tool.web`, each with a `description` and a `schema`, every setting with a `type` and a `doc`, and `grant` with `exec: ["bun"]` and an explicit `net` list that does not contain `*`.
- [x] `.cartridge/init.lua` has `{ id = "web", path = "web.ctg" }`, `web.ctg/README.md` has at least ten non-blank lines and `web.ctg/.cartridge/help.md` is non-empty — together the three things that make `cartridge help web` print a page and exit zero **in a trusted checkout**. `cartridge help web` itself is a post-merge check in a trusted checkout, not a Verify block. (Reworded 2026-09-17 on measurement: the original box said the command "prints the page and exits zero", which no Verify pass can prove. Measured twice, in a lane and in a worktree, it exits 1 with `is in no trusted project; review it, then run `cartridge trust <dir>``, and the trust prompt does not wait on a non-tty.)
- [x] `web.ctg/README.md` (at least ten non-blank lines) and `web.ctg/.cartridge/help.md` describe the cartridge as a stranger who found the folder alone would need.
- [x] `{op: "fetch", url}` returns the page as text with its URL; a `file://`, a `data:` or an off-allowlist host is refused with an error naming the reason, and the refusal is returned to the caller rather than thrown away.
- [x] `bun test` in `web.ctg` proves fetch and every refusal against a local server — no live network in any test, using the injected-client seam at `auth.ctg/src/main.ts:5`.
- [x] `just audit web` and `just isolation` report nothing hard for it, and both still pass for every sibling.

## Open decision that does not block this child

Whether `web.ctg` becomes its own git submodule like all eighteen siblings, or
lands as a plain directory in the superproject. The analyst recommends a plain
directory: a new submodule needs `.gitmodules` plus a remote, and a superproject
PRD with a submodule in its footprint cannot verify in a lane. The only price is
cosmetic — `just audit` runs `git -C <dir> status --porcelain`, which for a plain
directory reports the whole superproject's dirty files as soft `find:` lines,
and those are findings, not hard failures. Implement as a plain directory unless
the user says otherwise.

## Known ceiling of the gate (2026-09-17, round 2, finding N5)

The spec passed round 2 at 94/100 with no blocking findings, after both the
analyst and an independent reviewer built cheating implementations and measured
every block against each. Block 2 could not be beaten by any genuinely wrong
implementation — not by one that declares the allowlist and never checks it, not
by one whose `apply` ignores its configuration, and not by deliberate
seam-aware sabotage.

One hole is known and left open on purpose. A suite of six correctly titled
tests padded with about thirty trivial assertions passes all three blocks: the
count-based guards in block 3 measure that tests exist and that assertions are
made, not that the assertions are about anything. Block 2 still gates the code
itself, so what escapes is the suite's value rather than the implementation's
correctness.

Whoever implements this should know that the gate will not catch a hollow test
written to satisfy it, and whoever reviews the diff is the backstop for that.
Do not read a green collect as proof that the tests are good ones.

## Verified, and held from collection by a foreign gate failure (2026-09-17)

The work is done and independently verified in the lane
`.lanes/the-voice-can-look-something-up-...-web-ctg-exists-...` at
`d3442267c789f4e2d433cdd57e455a01eb4996f5` — 14 files, 743 insertions, every
path inside `web.ctg/**` or `.cartridge/init.lua`.

All three Verify blocks exit 0 in the lane, with block 3 at 6 pass / 0 fail /
47 expect() calls. `just audit web` is 1 of 1 and `just isolation` passes in the
lane. A verifier reproduced all three of the implementer's mutations itself and
matched every number: deleting the allowlist check gives 3 pass / 3 fail,
deleting the scheme check 4 pass / 2 fail, ignoring the HTML drop counter
5 pass / 1 fail, and none of them leaves a block green.

The round-2 hollow-suite ceiling recorded above does **not** apply to what was
built. The verifier read all six bodies: tests 1 and 5 drive the whole
production path against a real `Bun.serve` on 127.0.0.1 with no injected client
and assert the server's request log in full; test 2 proves the empty recorder is
the allowlist working rather than a dead client, by fetching an allowed host on
the same instance afterwards and requiring it to arrive; test 6 drives the real
handlers over a real wire and proves the refusal envelope, `cancel`, and that a
re-applied `allow_hosts` takes effect. The allowlist is enforced in
`web.ctg/src/web.ts:64-75`, not merely declared — which matters, because the
host reads `grant.net` as a boolean.

**It cannot collect yet, and the reason is not this PRD.** Verify block 1 ends
with `just isolation`, and collection runs pass 2 in `repo`, where
`just isolation` exits 1 on
`mcp.ctg/.cartridge/tests/integration/instances.test.ts:63` copying files out of
`../policy.ctg`. That is a regression from a different PRD collected earlier the
same day, owned by
`@mcp/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary`.
Blocks 2 and 3 have no such dependency.

So this PRD waits, with its claim and lane intact, until that gate is green
again. It is not blocked on anything about itself.

## The blocking gate is green, and box 6's post-merge half (2026-09-17)

`just isolation` passes again — `Isolation passed for 17 cartridges`,
`isolation composition pass` — after
`@mcp/the-mcp-instances-fixture-composes-policy-without-reaching-across-the-boundary`
collected at `mcp.ctg` `5a7c54c`. So this PRD's Verify block 1 can complete its
second pass and this lane can land.

Boxes 1, 2, 4 and 5 were proven in the lane by a verifier that reproduced all
three of the implementer's mutations itself and matched every number. Box 3 is
prose and has no gate; the verifier read it and judged it sufficient (README 54
non-blank lines, help.md 1949 bytes).

Box 6's second half — "and both still pass for every sibling" — cannot be
observed in a lane, where the submodule directories are empty. It is settled by
collection itself rather than asserted ahead of it: the engine runs Verify block
1 a second time in the integrated repository, and that block ends with
`just audit web` and `just isolation`. The pre-merge baseline was measured
immediately before collecting: `just audit` 17 of 17 and `just isolation` 17
cartridges, both green. `web.ctg` becomes the eighteenth, and the collection
receipt records what the second pass observed.
