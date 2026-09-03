---
memo: no-destructive-git-runs-in-a-tree-the-session-does-not-own
kind: invariant
status: decided
tags:
  - memo
  - kind/invariant
  - status/decided
subject: every destructive git in the board's own Python asks who owns the tree first, or it is a finding
date: 2026-09-02
verify: bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
prds:
  - every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own
---
<!-- Unlike a prd.md, a memo's keys are a CLOSED set: an undeclared key is a
     typo and @resources/doctor.sh fails on it. @references/memo.md is the
     format. -->

# no-destructive-git-runs-in-a-tree-the-session-does-not-own — the rule holds at every call site, not at the four we found

## Decision

`a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work`
settles **what** is out of bounds and why. This memo settles **how** the board
is held to it, and adds nothing to the rule itself.

Every `git` in the board's own Python that can leave uncommitted bytes
somewhere git cannot reach — `reset --hard`, `checkout --`, `checkout -f`,
`clean`, a real `stash`, `restore`, `switch --discard-changes` — asks
@resources/board/refuse.py who owns the target tree before it runs. A call
site that does not ask is a defect, whatever it is for.

Three shapes are accepted, and nothing else:

1. **Gated.** The call is inside a function that also asks —
   `_may_discard(…)`, `refuse.guard(…)`, `refuse.allowed(…)`,
   `refuse.check_line(…)`. `lanes.py`'s redundant `reset --hard` after a
   failed rebase is this shape.
2. **Exempt with its reason in the file.** `collect.py`'s `_park` and the
   `stash pop` in `guarded_run`'s `finally` are one stash-then-pop pair whose
   purpose is to move a peer's dirt out of a verify block's reach and put it
   back. The exemption is spent only while the recorded measurement above
   `_park` still stands; delete the comment and the check goes red.
3. **Not destructive at all**, by @resources/board/refuse.py's own
   `SPELLINGS` table — `stash create`, `clean -n`, `reset --keep`,
   `restore --staged`, a plain `checkout <branch>`. `session.py`'s reaper is
   green by construction here: it snapshots through `write-tree` and
   `commit-tree` and spells no stash at all.

The check reads `SPELLINGS` out of the tree it is scanning, so the invariant
and the mechanism can never drift into two answers about what discards, and
deleting `refuse.py` fails the invariant outright.

## Why

The loss is the other memo's and is not retold here. What is this memo's is
the shape of the repair. Fixing the one call site that caused it —
`collect`'s `unland` — left every call site that had not been looked at, and
the next one written would have cost the same afternoon. A mechanism was
built for that: one reader, asked by the board's code and by
@resources/guard.py's `PreToolUse` hook.

A mechanism still only guards the call sites that ask it. The failure that
remains is a **new** `git reset --hard` written into a board module by
somebody who has not read this, and there is nothing in a passing test suite
that notices one: the tool keeps working, every probe stays green, and the
damage shows up once, in somebody else's uncommitted work, with no object in
the store to recover it from. That is a rule about every future line rather
than about the code as it stands, which is what makes it an invariant with a
command instead of a comment above a function.

The check is a reader, not a grep, because a grep for `"reset"` cannot tell
`--hard` from `--keep`, cannot see the verb through `git -C <dir>`, and
cannot see a `clean` whose pathspec is concatenated on — the spelling
`_park` uses, and the one that got past the first draft of this very check.
It parses each module, finds the argument lists, and asks `refuse.py`.

A scanner that has stopped matching passes everything, so two synthetic
modules run before the tree does: one holding a `reset --hard`, a
concatenated `clean` and a real `stash`, which must all be seen, and one
holding `reset --keep`, `stash create` and a plain `checkout`, which must all
be let through.

## Alternatives considered

**A comment above each call site.** What the board had. It is invisible to
the person writing the next one, and it is what left `unland` holding a
`reset --hard` for as long as it did.

**Making `refuse.guard` impossible to skip — a wrapper every git goes
through.** The honest version of this, and it was not taken because the board
calls git through at least three spellings already (`subprocess.run` with a
list, `lanes.git`, `collect.git_out`) and a fourth wrapper is a refactor
across files this PRD does not own. The invariant catches a call site written
through any of them, including one written tomorrow through a fifth.

**Asserting the count of destructive sites.** Cheap, and a wall: the next
gated call site legitimately added would fail a check about a number rather
than about the rule. The check asserts the property of each site instead, and
its own totals are printed rather than asserted.

**Putting `_park` under the refusal so there is no exemption.** Tried and
measured before this memo was written: four checks of
`prds/collect-must-not-reset-the-checkout-it-did-not-write` flipped from pass
to fail, "the neighbour's uncommitted work is still there" stopped being
true, and six harnesses reddened. Refusing a protective stash destroys
exactly the work the refusal exists to protect. The distinction that keeps
the exemption honest: a `stash` a session **types** has no matching pop.

## Consequences

- A new destructive git in `resources/**.py` fails
  `pearde memo verify no-destructive-git-runs-in-a-tree-the-session-does-not-own`
  by file and line, with the sentence saying to ask `refuse.py` first.
- The exemption list is two entries and both name the same reason string in
  `collect.py`. Rewording that comment reddens the invariant, which is the
  intent: the exemption is the measurement, not the function name.
- It reads `resources/**.py` and nothing else. A destructive git in a shell
  harness, in a `justfile`, or typed by a person is not this check's — the
  last of those is @resources/guard.py's hook, which needs no invariant
  because it reads every Bash line there is.
- It does not catch `rm -rf <a peer's tree>` or `git worktree remove
  --force`, neither of which is one of the four. Both are open, and reported
  on this PRD rather than closed here.
- It cannot see a git built from a variable — `subprocess.run(cmd)` where
  `cmd` was assembled elsewhere. Nothing in the board is written that way
  today, and a checker that guessed at one would report the guess.
