---
memo: also-resolves-against-the-board-first
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: collect --also resolves against the board first, then the caller's cwd, and refuses a path neither holds
date: 2026-09-02
updated: 2026-09-02
prds:
  - filing-refuses-a-file-it-does-not-hold
supersedes: also-drops-a-path-it-cannot-find
---

# also-resolves-against-the-board-first — a rider is looked for where the board keeps its notes, then where the caller stands

## Decision

**`collect --also <path>` resolves a relative path against the board root
first and the caller's working directory second, and refuses the whole call
when neither holds it.** A name both hold resolves to the board's. So
`--also memos/foo.md` from anywhere names the board's memo, `--also
resources/x.py` from the repo root still names the repo file, and a path
that exists in neither place stops the collect with nothing written for any
PRD on the call — the refusal names the path as given, where it was looked
for, and the board root.

This inverts the first half of `also-drops-a-path-it-cannot-find`: a board
file no longer needs its `.pearde/` prefix, and spelling one is now the
odd case rather than the rule. It was the user's call, put as a drill
question on `filing-refuses-a-file-it-does-not-hold` on 2026-09-02 and
answered *look in the notes first, then where you are standing*.

**The second half of that memo stands and is carried here unchanged:** after
any collect carrying `--also`, `git show --stat` the commits it printed and
check the riders actually landed, and `git status` the board afterwards. The
resolution rule removes the silent-drop path; it does not make the commit
message evidence, and a `--also` on a container collect is still ignored
(`close_container()` never reads it).

## Why

Every other board command — `collect`, `claim`, `brief`, `scan`, and
`--widen` on this same command — takes board-relative paths. `--also` was
the one flag that read the cwd, and the memo this supersedes records what
that cost: ten riders dropped on the floor under a commit message that named
them. Board-first resolution makes `--also` spell the way the rest of the
tool spells, and the cwd fallback keeps every absolute-path and repo-root
invocation on record runnable as written.

## Alternatives considered

**Board only — refuse anything not under `.pearde/`.** Cleanest rule, but a
rider is as often a repo file (a workflow atomic, a reference page) as a
board file, and every recorded `--also resources/…` would start refusing.
Lost on the second half of the user's answer: *then where you are standing*.

**Cwd only, with the existence guard added.** The refusal alone would have
fixed the silent drop. Lost because it keeps `--also` the one flag spelled
differently from its neighbours, which is the inconsistency the superseded
memo names as the cause.

**Keep the old rule and mandate the `.pearde/` prefix.** What the superseded
memo decided. Lost when the user chose the resolution order over a spelling
convention that only the memo enforced.

## Consequences

- A name present under both roots goes to the board's, with no warning. A
  caller who means the repo's copy passes an absolute path.
- The refusal is the call's: two PRDs named on one collect with one bad
  `--also` both stay `claimed`, and nothing is committed.
- `also-drops-a-path-it-cannot-find` is `superseded`, not deleted — its
  account of what a silent drop did is still the reason this rule exists.
