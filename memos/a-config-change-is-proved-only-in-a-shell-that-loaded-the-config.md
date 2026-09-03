---
memo: a-config-change-is-proved-only-in-a-shell-that-loaded-the-config
kind: note
status: decided
tags:
  - memo
  - kind/note
  - status/decided
subject: a probe that asserts a config change must run in a shell that loaded the config, or it reports a convincing false negative
date: 2026-09-02
---

# a-config-change-is-proved-only-in-a-shell-that-loaded-the-config — the false negative answers other questions correctly

## Decision

A harness asserting that a shell config change is deployed runs in a shell
that loaded the config. `nu -c '<code>'` loads neither `env.nu` nor
`config.nu`, so a correct, deployed change reports ABSENT under it — and the
report is convincing, because unrelated variables still answer from the parent
process's environment.

Folded in from [[a-nushell-config-change-must-be-proved-in-a-shell-that-loade]],
which holds the provenance and the two independent measurements.

## Why

The failure is not that the probe is wrong; it is that the probe is wrong in a
way that looks right. Measured twice on nushell 0.115.1: `print $env.EDITOR?`
answered `nvim` in the same non-loading shell that reported the deployed
variable unset, because `EDITOR` was inherited rather than read from `env.nu`.
A reader checking whether the probe works at all gets a green answer from it.

This is the shape @pearde/memos/a-crashing-checker-reads-as-a-failing-check.md
already names on the board: a check whose mechanism is broken must not be
readable as a verdict about the thing it checks. A non-loading shell is that
mechanism failure, wearing the mask of a clean negative.

Recorded here rather than left in the KB because a memo is where the next
session looks before writing a probe, and the conclusion is where the
measurement lives. The memo cites; the KB holds provenance.

## Alternatives considered

**Leave it in the knowledge base only** — the conclusion is complete and
sourced. It is also only reached by a query someone thinks to run, and nobody
queries the KB while writing a one-line probe.

**Write it as an invariant** — a command grepping this tree's harnesses for
`nu -c` assertions would bind it. Rejected for now: the measurement came from a
sibling repo's pass, this tree has no nushell probe to guard, and an invariant
with nothing to prove is a claim.

## Consequences

- A probe asserting shell state is written `nu -l -c`, or through a real
  interactive load, and says in a comment which config it depends on.
- It generalises past nushell: any shell's `-c` is a fresh process with the
  parent's environment, so the same false negative is available in bash and
  zsh probes that assert on `.zshrc` state.
- It does not make the existing harnesses correct — nothing here was audited
  for this; the note exists so the next one is written right.
