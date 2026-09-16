---
state: "done"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/sessions.ctg"
capability-owner: sessions
needs:
- "one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it/an-instance-attaches-to-the-daemon-and-never-composes-silently"
footprint:
- "src/lib.rs"
- ".cartridge/tests/integration/instances.test.ts"
- ".cartridge/tests/integration/native.ts"
commit: "02dcc85a00d29e2bbc87ae54ed1c913fa1e02df2"
---

# Sessions runs once in the daemon with one buffer-id space

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`,
per-cartridge audit item. The parent's audit classifies sessions as
must-exist-once: it loads its store into memory once (`lib.rs:261`), so under
two compositions the last rename wins and buffer ids come from a counter
local to each process.

## Outcome

Sessions is composed exactly once in the daemon. Buffer ids come from one
counter in that one node, so ids from different attached instances never
collide, and store renames land on the single in-memory copy.

## What changes

- With the host-attach contract in force there is one sessions node; this
  child verifies that and removes any per-process assumption left in the
  code (the in-process buffer-id counter must be the daemon's, not an
  instance's).
- If any sessions API is per-instance by design (a client's own buffer list),
  key it by attached instance inside the one node, the way the parent's
  audit prescribes.

## Acceptance

- [x] Two attached instances calling sessions draw buffer ids from one space
      (no id is handed out twice), and a buffer opened under one session is
      never returned by a listing that names another session; an instance
      reaches another session's buffers only by asking — by that session's id,
      or by an unfiltered `buffers list`.
- [x] A rename made through one instance is visible through the other.
- [x] Exactly one sessions node exists with the daemon running (covered again
      by the composed acceptance test).

## Planning note

2026-09-16, coordinator cartridge-1b, from analyst-1. **Both audit findings
dissolve under one daemon**, so there is no Rust change.

- *Id space*: `Store.next` (`src/lib.rs:101`) is a **store** field, seeded from
  disk by `install` (`:344`) and reserved under the store's write lock
  (`:1061-1064`). It was per-process only because the store was — `Store::load`
  has one call site (`:1214`), installed in `static STORE: OnceLock` (`:1185`),
  with a second `start` refused (`:1226`). One node is one counter.
- *Last-rename-wins*: **sessions has no rename op at all.** The only `rename` is
  the `std::fs::rename` snapshot commit in `Store::save` (`:394`). The audit's
  symptom came from two stale full-store copies, which one node removes. Box 2's
  "rename" means `sessions update {id, name}` (`:695-700`).

**Box 1 was narrowed, and the reason matters.** Its literal second clause —
"do not see each other's buffers unless they ask for them" — reads as *instance*
isolation, which is neither provable nor deliverable here: no instance identity
reaches this cartridge (`cartridge call` is `client::ask(project,"bail",…)`,
`cartridge.ctg/src/cli/mod.rs:108-114`, with args arriving as caller-supplied
JSON), and an unfiltered `buffers list` returns every buffer in the store — as it
always did, since both compositions read one directory. Scoping in sessions is by
**session record** (`Buffer.session`, `:55`; filtered listings `:594-604`,
`:846-856`), which already gives the property the box is reaching for. The new
wording names the session as the scope and says plainly that the unfiltered
listing is how you ask; the test asserts that listing too, so the behaviour is
recorded rather than hidden.

Boxes 2 and 3 stay as written. Notably the analyst did **not** claim the node
count unobservable: the sessions fixture already runs a real `cartridge daemon`
and real `cartridge call` instance processes
(`.cartridge/tests/integration/native.ts:67-70`, `:81-95`, `:123-136`), and the
assertion pins `state === "active"` so it cannot pass with the node absent. That
is the trap three earlier rows on this board fell into.

Footprint gained `.cartridge/tests/integration/instances.test.ts` (new) and
`.cartridge/tests/integration/native.ts` (drops `private` from `cli`, one word).
`src/lib.rs` is unmodified but stays in the footprint because the guards read it;
a test cannot live there (unit modules are `#[path]`-attributed to
`.cartridge/tests/unit/main/`) and could not reach a daemon anyway.

## Evidence note for the ticked boxes

2026-09-16, coordinator cartridge-1b, after round 1 (PASS 93) and verifier-1.

Every box has a **red world**, constructed and observed, not argued:

- Box 1: the counter frozen → `new Set(ids).size` Expected 6 / Received 1; the
  session filter ignored → `Expected -0 / +Received +3`, the diff adding ids 4,
  5 and 8 to a 3-element expectation, which is what shows the filtered listings
  are genuinely non-empty rather than trivially equal.
- Box 2: the verifier added a **seventh** world beyond the six required —
  `sessions update` dropping the `name` write → Expected `"renamed"`, Received
  `"alpha"`. Box 2 therefore no longer rests only on round 1's two-daemon
  measurement.
- Box 3: the node-absent world → `sessions failed: … node refuses to start`.

Two limits recorded rather than smoothed over:

- Box 3's catch lands at the fixture's own `active()` gate (`native.ts:91`)
  before `expect(nodes[0].state).toBe("active")` is reached, so the assertion's
  distinct content is `nodes.length === 1`. The second-*slot* world is not
  constructed here and stays delegated, as the spec says.
- A shared probe used across several rows today is wrong and is corrected here:
  `pgrep -fl "cartridge daemon"` **cannot** match a fixture daemon, whose argv
  reads `…/cartridges daemon`. The verifier used the fixture's own temp-dir
  prefixes instead.

**Coverage gap, deliberately left and worth naming:** after box 1's narrowing,
no row on this board asserts instance-level buffer isolation. Delivering it
would need an instance identity in the host call protocol — a runtime-wide
contract change — and `cartridge call` carries only `{name, data}`
(`cartridge.ctg/src/cli/mod.rs:107-114`), with `grep -rn 'sessions'
cartridge.ctg/src` returning zero lines. The sibling that would carry such an
identity for MCP, `mcp-keys-sessions-and-inflight-calls-by-attached-instance`,
is still `specced`.
