---
memo: also-drops-a-path-it-cannot-find
kind: decision
status: decided
subject: collect --also resolves paths against the caller's cwd and silently drops one that lands in the wrong repo, while the commit message it writes still names the file
date: 2026-09-01
prds:
  - seven-closed-probes-drifted-red/the-doctor-completes-without-a-home
---

# also-drops-a-path-it-cannot-find — the message named ten files the commit did not hold

## Decision

**`--also` paths are spelled from the caller's working directory, and a board
file therefore needs its `.pearde/` prefix** — `--also .pearde/memos/foo.md`,
never `--also memos/foo.md`, even though every other board command takes
board-relative paths.

And because the tool will not say when it drops one: **after any collect
carrying `--also`, `git show --stat` the commits it printed and check the
riders are actually in them.** The commit message is not evidence that they
landed; it is written from the flags, not from the tree.

## Why

The doctor PRD's collect was handed eleven `--also` paths spelled
board-relative — six workflow files and five memo files. `collect.py:853` does
`os.path.abspath(a)` against the cwd (the code repo root), then
`planlib.repo_root()` on the result. `memos/a-report-must-say-verdict.md`
resolved to `<repo>/memos/a-report-must-say-verdict.md`, which does not exist —
but `repo_root` walks *directories*, so it found the code repo anyway and
filed the path there. The file was absent, `plan.add` skipped it, and the
collect printed `commit ca29535 5ebefc7 · inherited 143` with no complaint.

All ten riders stayed uncommitted. Worse, the `--also-note` went into the
commit message verbatim, so `ca29535` reads *"Four memos and the regenerated
kind index: a-report-must-say-verdict, one-author-is-not-an-accepted-spec,
a-crashing-checker-reads-as-a-failing-check, a-check-decided-by-scheduling"* —
naming four files that are not in that commit or any other. A record that
claims what the tree does not hold is worse than no record, because the next
reader has no reason to check.

The dry run did print the truth and it was misread. Its two blocks named
`footprint:` and `would add:` separately; the riders appeared under
`footprint:` and not under `would add:`, which reads as "already covered"
exactly as easily as "will not be written". This memo's own author read it the
first way. That is the same failure `one-author-is-not-an-accepted-spec.md`
describes, one layer up: a check was consulted, it could not fail, and the
consulting was mistaken for verification.

The `.pearde/` prefix is a real inconsistency, not a preference. `collect`,
`claim`, `brief` and `scan` all take board-relative PRD names; `--widen` on
this same command resolves against `board_root`. Only `--also` uses the cwd.

## Alternatives considered

**Make `--also` resolve against the board first, then the cwd** — the fix that
matches every other flag. It lost only on scope: it is a change to
`collect.py` with no PRD behind it, made mid-round by an orchestrator on a tree
with a live sibling session, and @references/parts/derived.md rule 2 routes an
instrument defect to a memo for exactly that reason. The repair is owed, and
this memo is the debt.

**Refuse the whole collect when an `--also` path does not exist** — strictly
better than dropping it, and cheap: `collect` already refuses a *footprint*
path that is under no repo (`collect.py:850`), so the machinery is there and
`--also` simply does not use it. This is the change to make when the repair is
made. It lost as a same-round fix for the same scope reason.

**Always pass absolute paths** — sidesteps the ambiguity entirely and needs no
code change at all. It lost as the primary rule because absolute paths make
every recorded command in a round file and a report unrunnable on another
machine, and this board's records are meant to be re-run. Fine as a fallback
when the prefix is in doubt.

**Note it in the round file and move on** — what a busy round would do. It
lost because the failure is silent and repeats: the very next collect would
have been spelled the same way, and the one after that. A silent drop needs a
written rule or it is rediscovered every time.

## Consequences

- `ca29535`'s message permanently names four memos it does not contain. It is
  not amendable — it is somebody's HEAD by now and the board's rule is never to
  amend a HEAD that is not yours. The riders go into the next collect instead,
  with an `--also-note` that says why they are late.
- Every collect carrying `--also` now costs one extra `git show --stat`. That
  is the same tax `a-crashing-checker-reads-as-a-failing-check.md` levies on a
  red doctor row, and for the same reason: the instrument reports success it
  did not observe.
- It deliberately does not fix `--also`. The path resolution and the missing
  refusal both stand, and the next caller who spells a board path without the
  prefix gets the same silent drop with the same confident message.
- It says nothing about `--also` paths that exist in the *wrong* repo — a file
  present at both `<repo>/x.md` and `<board>/x.md` would be committed, from the
  wrong root, with no warning at all. Nothing on this board has that shape yet.
