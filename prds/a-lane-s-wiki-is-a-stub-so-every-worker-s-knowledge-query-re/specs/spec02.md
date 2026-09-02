---
complexity: 10
footprint:
  - resources/knowledge.py
---

# spec02 — `knowledge.py harvest` recovers what the stub wikis are already holding

Fixing the resolver stops new stubs. It does not recover the ones on disk.
Counted on this board 2026-09-02, while spec01's probe ran: **26 lanes held a
wiki of their own, with 34 notes in them — 29 pending gaps and 5 `remember`
findings**. `git worktree remove` deletes a lane whole, so those five findings
are work already done and about to be thrown away, and the 29 gaps are
questions the board thinks nobody asked.

`knowledge.py harvest [--dry]` moves them into the live record and removes the
emptied stub. Three parts carry the whole of it:

`stub_wikis(store)` — every `<board>/.lanes/*/{pearde,.pearde}/wiki` that is a
directory and does not `resolve()` to the live store. A wiki that IS the live
one (a symlink, a board mounted there on purpose) is not a stub.

`note_key(path)` — what makes two notes the same note. `cmd_enqueue` dedupes a
pending note on its `question:` frontmatter and on nothing else, so harvesting
must ask the same question or it re-queues every gap a lane already asked; a
source or a conclusion is its `title:`. The filename is never the key —
`note_id` is time entropy, so two lanes writing the same finding a second
apart get two different names. Measured on this board: 34 notes moved and 1
skipped as already on record.

`cmd_harvest` — walks `pending/`, `sources/`, `conclusions/` under each stub,
skips `_index.md`, writes each note to the same relative path under the live
store (shifting the id on a filename collision, the way `cmd_remember`
already does), and deletes the source. When no `.md` is left it removes the
stub directory and, if that leaves the lane's `pearde/` empty, that too.

**It never reaches through `<lane>/pearde/graphify`** — that is a symlink into
`<git-common-dir>/pearde-shared/` and deleting through it takes every lane's
cache with it (@pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md).
Only the `wiki` directory is removed, and only when it holds no note.

`--dry` prints every line prefixed `dry · ` and moves nothing.

## What already stands

Built in the lane, uncommitted, in `resources/knowledge.py`: `stub_wikis`,
`note_key`, `cmd_harvest`, the `harvest` subparser with `--dry`, the verb
table row, and `import shutil`. Section G of
`pearde/prds/a-lane-s-wiki-is-a-stub-.../probe/verify.sh` proves it in the
clean-room fixture: a stub holding one new finding and one already-queued
question, a shared-cache symlink beside it, then `--dry` (reports, moves
nothing), the real run (`1 note(s) recovered, 1 already on record`), the note
standing in the board's wiki, the stub gone, the symlink and its target
intact, and a second run reporting `nothing stranded`.

`harvest --dry` has been run against the live board and printed
`34 note(s) recovered, 1 already on record, from 26 lane wiki(s)`.

## What is left

The real run against this board, which the probe deliberately did not make —
it writes into the shared wiki, so it belongs to the implementer, once, with
the count quoted. The number will have moved: every lane still carrying the
old resolver keeps making stubs until spec01 lands, so **spec01 lands first**
and `harvest` is run after it.

## Acceptance

- [x] Section G of `PEARDE_ROOT=<tree> bash pearde/prds/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re/probe/verify.sh` is all `ok`: `--dry` moves nothing, the real run recovers 1 and skips 1, the stranded finding stands in the board's wiki, the stub is gone, the shared graphify symlink and its target survive, and a second run reports `nothing stranded`.
- [x] `python3 resources/knowledge.py harvest --dry` on this board prints one `dry · ` line per stranded note and a trailing count, and `find pearde/.lanes -path '*/wiki/*.md' | wc -l` is unchanged afterwards.
- [x] `python3 resources/knowledge.py harvest` on this board reports the count it moved; afterwards `find pearde/.lanes -path '*/wiki/*.md'` prints nothing, and the note total `python3 resources/knowledge.py doctor` reports has risen by the number of sources and conclusions it moved.
- [x] Every `sources/` note it moved is readable by the tool it moved into: `python3 resources/knowledge.py doctor` reports `clean` — no missing frontmatter, no dangling wikilink — or names only problems that predate the run.
- [x] The shared store survives: `ls <git-common-dir>/pearde-shared/` still lists what `pearde share status` said it held before the run, and `pearde share status` reports no path as `absent` that was `linked` before.
- [x] A second `python3 resources/knowledge.py harvest` prints `no lane holds a wiki of its own — nothing stranded` and exits 0.

## Verify and Proof

```sh
python3 resources/knowledge.py harvest --dry
find pearde/.lanes -path '*/wiki/*.md' | wc -l
python3 resources/knowledge.py doctor
share=$(python3 resources/pearde.py share status 2>&1) && src=0 || src=$?
if [ -z "$share" ]; then echo "share status printed nothing (exit $src)"; exit 1; fi
printf '%s\n' "$share" | tail -1
PEARDE_ROOT="$PWD" bash pearde/prds/a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re/probe/verify.sh
echo "verify block complete"
```
