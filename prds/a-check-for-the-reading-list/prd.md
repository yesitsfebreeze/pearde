---
state: done
origin: requested
priority: 42
complexity: 12
blast-radius: low
workflow: probe-then-spec
actual: 0.22h
---

# A check for the reading list

*Source: `docs/content/docs/improvements/scout-reading-check.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** scout · **Axis:** sensibility (6 → 7) · **Pulls the score up by
~4 points**

## Why now

Four layers, three have a tool behind them: sweep and delta write snapshots,
route writes findings. The curate layer — `reading-list.md`, "what is worth
*reading*, mapped to what it teaches a specific tree" — is the layer whose
rows are written by hand, with no generator, no check and no expiry. A row
naming a repo that archived last month reads as advice; nothing says so.
The tool's own rule — stars are the discovery layer, never the verdict — is
enforced everywhere but here.

## The change

`scout.sh reading` gains a check pass, run as part of the verb: every row's
repo is resolved through `toolscout`'s state reader — `ARCHIVED`, days since
push, issue load — and a stale row is marked in place (`<!-- stale: archived
2026-07-14 -->`), never deleted. The row's *mapping* column (what it teaches
this tree) is required on every row; a row without it fails the check the
way a conclusion under two sources is refused.

## Done when

- Every row in `reading-list.md` carries the mapping column — the check
  exits non-zero until they do, and names the bare rows.
- A row whose repo state reads archived is marked stale by the next
  `scout.sh reading` run, visibly, in place.
- The check is part of the verb, not a doctor row — scout's tree is not a
  board.

## Fails when

- The state reader hits the network per row — a 20-row list is a rate-limit
  wait. Guard: rows are checked against the *latest snapshot* first, and the
  network is reached only for rows with no snapshot row at all.

## What stays out

No auto-generation of rows — curation is a judgment the tool cannot make.
The check only holds the *shape* honest and the state current; the taste
stays human.

## Report

spec01: exit 0
ok    bare row fails (exit 1)
ok    non-GitHub bare row named by its link text
ok    failing run left the content alone
ok    failing run left the mode alone (644)
ok    archived+active mix exits 0
ok    marking run kept the list's mode (644)
ok    archived row marked in place
ok    active row left alone
ok    second run is idempotent
ok    snapshot-first guard held — no network call

verify: all checks passed
11
