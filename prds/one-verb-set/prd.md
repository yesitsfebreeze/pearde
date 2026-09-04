---
state: done
origin: requested
priority: 42
complexity: 12
blast-radius: low
workflow: probe-then-spec
commit: 7f760c2 3f8bfd1
---

# One verb set

*Source: `docs/content/docs/improvements/scout-one-verb.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** scout · **Axis:** usability (5 → 7) · **Pulls the score up by
~5 points**

## Why now

Four commands answer "what is out there": `scout.sh sweep|delta|trending`
and `toolscout.sh '<query>'`. They share the buckets, the snapshots, the
ranking-page shape and the findings record, but a newcomer meets them as
four files, four `--help` texts and a README table — and the distinction
(daily measurement vs one-off ranker) is held in the head, not printed in
the output. The `toolscout.sh` name suggests a fifth tool; it is a verb of
the same one.

## The change

One entry, `scout.sh <verb>`: `sweep`, `delta`, `trending`, `tool <query>`,
`find`, `reading`, `quality` — the seven verbs the reference already
promises, with `toolscout.sh`, `route.sh` and `findings.md` as the storage
they read and write. Every verb's output ends with one line naming the layer
that answered and the file the record landed in. `toolscout.sh` stays as a
compat entry that execs `scout.sh tool "$@"`.

## Done when

- `scout.sh` with no argument prints the verb list, each with its one-line
  contract — the README table's rows, generated from the same source.
- `toolscout.sh 'topic:tui language:rust'` and
  `scout.sh tool 'topic:tui language:rust'` produce byte-identical output.
- Each verb's last line names its landing file (`snapshots/\<date\>.tsv`,
  `findings.md`, …) — the reader never loses the record.

## Fails when

- The verb list drifts from the README's command table — two truths again.
  Guard: the README's command table is generated from the verb registry, or
  a doctor-style check diffs the two.

## What stays out

No change to the sweep, the diff or the scrape — this page renames entry
points and unifies output tails, nothing else. The layers stay four; only
the door becomes one.

## Blocked

**2026-09-03 18:14 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s98669`; 2 file(s) disagree:

- `resources/scout/README.md`
- `resources/scout/scout.sh`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s27323`; 2 file(s) disagree:

- `resources/scout/README.md`
- `resources/scout/scout.sh`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-03 21:35 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-03 21:42 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/one-verb-set` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:47 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

**2026-09-04 02:48 — the lane will not rebase**

`lane/one-verb-set` does not land on `session/s85810`; 2 file(s) disagree:

- `resources/scout/README.md`
- `resources/scout/scout.sh`

Nothing is lost: the worker's commits are on `lane/one-verb-set` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-verb-set`.

## Report

spec01: exit 0
ok
