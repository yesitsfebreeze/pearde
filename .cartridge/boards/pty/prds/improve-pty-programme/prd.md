---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: pty
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: improve-pty-programme
needs:
- '@pty/improve-pty-shell-identity'
- '@pty/improve-pty-input-ownership'
- '@pty/improve-pty-command-wait'
---

# PTY and shared shell improvement plan

Roll-up only; claim a leaf for implementation. Shell identity is done (pty e8e6b31).
Preemption and busy behaviour are settled once, in input ownership; command ids and waits
live only in command wait. `@pty/pty-document` reuses both and is not a child here.
Both open leaves share `src/main.rs`, `src/tool.rs` and the integration test file: land them
sequentially, rebasing the second.

## Acceptance

- [ ] Each linked leaf is done with its own revision-bound proof and passed review.
- [ ] At one pinned pty revision, `just test pty` (cwd `/Users/feb/dev/cartridge`) passes, or each remaining failure is named (release-status currently lists two).
- [ ] Remaining limitations are recorded at that revision.

## Work items

- [Return explicit shell and working-directory identity](../improve-pty-shell-identity/prd.md) — done
- [Coordinate human and agent input on the shared terminal](../improve-pty-input-ownership/prd.md) — open
- [Wait and retrieve output for one terminal command](../improve-pty-command-wait/prd.md) — open

## Failure and review

If a leaf exhausts its review allowance, this parent stays open and records that leaf's gaps;
done leaves are not reopened. [Review history](review.md); limit five rounds.
