---

kind: work
level: 10
status: done
description: "`part` joins the dispatch table — list the record's files, read one, write one — so a caller edits the record through the daemon and the watcher sees the change like any other"
read_when: "letting a caller edit the record"
---

# part-is-a-verb

## Do

A new arm in `rpc::Server::invoke`: `part {op: list|read|write, path, body?}`.
`list` walks the watched roots (`the-watcher-watches-parts`) and answers
path, kind, frontmatter for every `.md`; `read` answers one file's text;
`write` replaces one file's text. Every path is resolved under a watched root
and refused outside it. The write lands on disk only — the watcher's own
ingest carries it into the graph, so there is no second write path
(`who-writes-where`; `cli-ingest-has-no-provenance` names why a direct
entity write would lose the kind).

The CLI gets no new command for it; the daemon's consumers are the callers.

## Check

A test in the rpc crate: `write` of a `kind: work` part under a temp watched
root lands on disk with the body sent, `read` returns it, `list` names it with
`kind: work` and its `status`, and a path with `..` or outside the root is
refused. `tests/one_dispatch.rs` still passes with the arm counted.

Done 2026-09-06: `src/rpc/src/part.rs` carries the three ops behind one
`"part" =>` arm. A path is refused when it climbs, when it is not `.md`, or
when its deepest existing ancestor canonicalizes outside every watched root;
`list` and `read` answer the whole front matter as a map rather than three
chosen keys, so a caller's `status` and `kind` come off one call.
Three tests in the crate, and `tests/one_dispatch.rs` counts 23 operations
from one table.
