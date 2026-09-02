---
memo: dates-are-written-not-stamped
kind: decision
status: decided
subject: Every date on this board is a fixed string, so a copy renders the same page every time
date: 2026-08-28
prds:
  - building
---

# dates-are-written-not-stamped — a fixed date, not the clock

## Decision

Every `claim:`, `date:` and `actual:` on this board is written by hand, never
updated by a tool. `building`'s claim reads `2026-08-28 13:49` and stays
there.

## Why

The board is copied and compared. A claim stamped at copy time renders the
same holding time every run, hiding the one thing the view's gate must
normalise. A claim written once renders a growing holding time — what the real
board does, and what the gate learns to read past.

## Alternatives considered

**Stamp the claim at copy time** — an identical page every run, and a
regression in the unexercised normaliser goes unseen.

**Carry no claim at all** — no holding time to normalise, and no in-flight
band to check.

## Consequences

- `building`'s rendered holding time differs on every run, and every snapshot
  comparison normalises it before reading.
- The memo fixes where a date comes from, never whether a date is right.
