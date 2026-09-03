---
complexity: 15
footprint:
  - resources/knowledge.py
  - references/knowledge.md
  - resources/board/knowledge/WORKFLOW.md
  - resources/board/knowledge/pending/.expired/_index.md
  - references/files.md
---

# spec01 — pending questions expire by date, not by hand-deletion

`.pearde/wiki/pending/` questions now carry an `expires:` date instead of
being judged by raw age. `query` reads pending last on every call and
archives anything past its own `expires:` to `pending/.expired/` — moved,
never deleted, and named in the response so the death is on the record.
`doctor` stops naming a row stale by age; it names only a row whose own
`expires:` has passed and is still sitting un-archived. A `keep:` row is
exempt from both. All of this already stands, verified by
`.pearde/prds/pending-gets-an-expiry-not-a-decree/probe/verify.sh` (11/11
green against this footprint; 3/11 green against the unmodified tool, so
the checks are not vacuous).

The build is complete: no defined work remains. What is here is a spec of
record, not a plan — the acceptance boxes are its receipt.

## What already stands

- `CONFIG["pending_expiry_days"]` (default `14`) in `resources/knowledge.py`
  — `WORKFLOW.md`'s new knob, coerced the same way as every other key.
  `pending_expiry_days: 0` keeps nothing: a freshly enqueued row is due the
  same day.
- `cmd_enqueue` writes `expires: <date + pending_expiry_days>` into every
  new pending file's frontmatter.
- `pending_expiry_date(meta, config)` reads a file's own `expires:`, or —
  for a file enqueued before this existed — falls back to its `date:` plus
  the configured window, so no existing pending file needs migrating by
  hand.
- `archive_expired_pending(store, config)` moves every pending file whose
  expiry has passed (and that carries no truthy `keep:`) to
  `pending/.expired/`, `rename()`, never a delete.
- `cmd_query` calls `archive_expired_pending` last, after its own hit/gap
  reporting, and prints one line per archived file: `pending: <name>
  expired on <date> — re-enqueue with knowledge.py enqueue`.
- `cmd_enqueue`'s own dedupe check ignores a match whose expiry has already
  passed (and is not `keep:`), so re-asking an identical question while its
  stale duplicate still sits un-archived writes a fresh live row instead of
  reporting "already pending" and losing the question — the guard the
  contract's `## Fails when` asks for.
- `cmd_doctor`'s pending check now flags a row only when
  `pending_expiry_date` has passed and the row is not `keep:` — a folder of
  pending files that are merely old but still inside their own window
  reads `ok`.
- The board seed (`resources/board/knowledge/`) plants
  `pending_expiry_days: 14` in a fresh board's `WORKFLOW.md` and a
  `pending/.expired/_index.md` marker, matching the existing
  `sources/.absorbed/` convention — a new board gets the mechanism from
  its first `init`.
- `references/knowledge.md` and the seed `WORKFLOW.md`'s own prose describe
  the mechanism (`expires:`, `pending_expiry_days`, `.expired/`, `keep:`)
  in place of the old age-only decree.

## Acceptance

- [ ] `python3 resources/knowledge.py enqueue "<question>"` writes an
      `expires:` line into the new pending file's frontmatter.
- [ ] A pending file whose `expires:` (or, absent that, `date:` +
      `pending_expiry_days`) has passed, and carries no truthy `keep:`, is
      moved by the next `query` call to `pending/.expired/` — never
      deleted — and the `query` output names it: `pending: <file> expired
      on <date> — re-enqueue with knowledge.py enqueue`.
- [ ] `doctor` names a pending file only while it is past its own expiry
      and still un-archived; a folder holding only rows still inside their
      window reports no pending problem.
- [ ] A pending file with `keep: true` is left alone by both `doctor` and
      `query`'s archiving, regardless of how far past its `expires:` it is.
- [ ] `pending_expiry_days: 0` in `WORKFLOW.md` means a row enqueued today
      is due for archiving the same day.
- [ ] Re-running `enqueue` on a question whose only pending match has
      already expired writes a fresh row rather than reporting "already
      pending" — the in-flight question is never silently dropped.

## Verify and Proof

```sh
python3 -c "import ast; ast.parse(open('resources/knowledge.py').read())"
PEARDE_ROOT=<repo-root> bash .pearde/prds/pending-gets-an-expiry-not-a-decree/probe/verify.sh
python3 resources/index.py check   # unchanged from baseline: common.py / hotreload-test.js rows only, both pre-existing
bash resources/doctor.sh           # unchanged from baseline: knowledge/questions rows are pre-existing, unrelated to this footprint
```
