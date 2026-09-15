---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# every `routine:<leaf>` tool call runs a full `part list` — 661 `.md` read in full, 2.0 MB, one `git log` subprocess — to pick one of eleven paths it then reads; a directory scan for `<leaf>.md` finds the same file in 1.3 ms

Landed 2026-09-07 on lane `herd-drive-p2-3`: `memo::locate` beside `list` in `src/rpc/src/memo.rs` (the module is `memo.rs` now, `part.rs` above is its old name) walks the roots from directory entries alone, and `tool_declaration` in `src/rpc/src/server.rs` uses it, keeps the `read`, and checks `kind` on the front matter that answer carries; `cargo test -p rpc` is green at 115 with `locate_finds_a_leaf_in_any_directory_without_reading_the_record` resolving a leaf from `routine/` and from `intake/` past a dot directory. The `dtruss` half of the Check was read off the code, not a live daemon: the shared daemon runs the trunk binary and a lane never restarts it, so the first `routine:improve` call after `just land` and `just install` is where that observation falls.

`tool_routine` (`src/rpc/src/server.rs:157-186`) is handed the leaf name of the
routine it must answer, and its first move is
`crate::part::invoke(op: "list")` (`:168`) — the whole record — which it then
filters to `kind: routine`, matches by file name and throws away. `part::list`
(`src/rpc/src/part.rs:64-105`) walks every non-dot directory under the watched
roots, reads each `.md` **in full**, parses its front matter, and calls
`git_stamps` — one `git log --format=%ct --name-only -- *.md` subprocess per
root (`:118`) — before sorting and building the answer. Measured against this
record on 2026-09-07, warm cache, roots defaulting to the repo directory:
**661 `.md` files, 2,002,515 bytes read, 1 subprocess (3,750 lines of `git log`
output parsed), ~85 ms**, of which the git subprocess alone is a fixed ~38 ms.
Eleven of those 661 rows carry `kind: routine`; exactly one path is used, and
`tool_routine` then does the `op: "read"` it wanted all along.

Scanning the same tree for a directory entry named `<leaf>.md` and stopping at
the first hit reads no file and spawns nothing: **998 entries, 1.3 ms** — about
60× cheaper, and it is the shape `just memo <leaf>` already resolves a wikilink
with (`justfile:134-144`). [part-list-answers-the-whole-record-uncapped](../part-list-answers-the-whole-record-uncapped/prd.md)
measures the same operation from the other side, as an answer no agent context
can hold (~303,000 characters, ~76,000 tokens); it does not know about this
caller, which never sends the answer anywhere and pays the whole walk
server-side. The cost is per call and it is on the entry path of every agent
session here: [routines-are-tools](../routines-are-tools/prd.md) puts one `routine:<leaf>` tool on the
surface per routine part, and [the-routine-call-is-not-counted-under-its-name](../the-routine-call-is-not-counted-under-its-name/prd.md)
moved the two-`part`-reads composition off the client and into this one daemon
operation, which is where the uncapped walk now sits. `herd` fires several
routine calls at once and each spawns its own `git log`.

The other two `op: "list"` callers stay as they are, and this is why the fix
is only in `tool_routine`: `routines(node)` (`commands_mcp.rs:172`) needs every
part's kind and description to build `tools/list`, and `server.rs:150` is
the agent asking for `part` itself. Only `tool_routine` asks for all 661 rows
to use one.

## Do

In `src/rpc/src/part.rs`, add a leaf resolver beside `list` — given a leaf, walk
the roots the way `list` does (dot directories skipped) and return the first
path whose file name is `<leaf>.md`, reading no file and running no `git`. In
`src/rpc/src/server.rs`, replace the `op: "list"` call and the filter chain in
`tool_routine` (`:168-179`) with that resolver, keep the existing
`op: "read"` so `resolve` still refuses a path outside the watched roots, and
keep the `kind: routine` check against the front matter the `read` answer
already carries — a wrong-kind part with that leaf must still fail with
``no routine `<leaf>` in the record``. The resolver must find a routine part in
`intake/` as well as in `routine/`: a routine part may sit in `intake/` before
it is promoted, so a hardcoded `memos/routine/<leaf>.md` is wrong.

## Acceptance
`cargo test -p rpc` green, with a test in `src/rpc/src/part.rs`'s module
resolving a leaf from a scratch root that also holds a same-named part in a
second directory. Then, against this record: a `routine:improve` call spawns no
`git` subprocess — `dtruss`/`fs_usage` on the daemon shows no `git log` and no
read of any `.md` but the one routine file — and a routine part placed under
`memos/intake/` still answers from there.
