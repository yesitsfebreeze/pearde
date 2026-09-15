---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
---

# Fourteen of the twenty-two agent worktrees hold a HEAD already an ancestor of `main`, so their work landed and their lane was never closed; the directory is 4.4 GB and the repository carries 87 branches.

## Do

Approved 2026-09-08 as "Approve, and prune merged branches too" [[approve-closing-the-landed-lanes]]. The fourteen lane removals are authorized, and so is deleting merged branches beyond them — each proved merged into `main` by its own ancestry test first.

Observed defect, measured 2026-09-08 at 11:11 in `/Users/feb/dev/memory`, code revision `36d6def6`. [[git-policy]] requires that after landing, an agent verifies its worktree's HEAD is an ancestor of `main` and closes the lane with `just lane-rm <name>`, and states plainly that finished routine lanes close too and that cached build output is not a reason to keep an abandoned worktree. Walking `.claude/worktrees/` and testing each HEAD with `git merge-base --is-ancestor <head> main`, 14 of 22 lanes are already landed and still present: `agent-a1428197a9059983d`, `agent-a85691e7482ae3921`, `codex-finish`, `drive`, `graph-herd-context`, `graph-source-provenance`, `herd-improve-b2b-1-0`, `herd-improve-b2b-1-1`, `herd-improve-b2b-1-2`, `herd-legible-b2b-1-1`, `improve`, `legible-cold-open`, `mine-compact-integration`, `store-cold-v11-v12`. Eight are unlanded and stay. `du -sh .claude/worktrees` is 4.4 GB and `git branch --list | wc -l` is 87. No `claim:` line appears in any work memo, so no lane is recorded as held.

Proposed scope: run `just lane-rm <name>` once per named lane, in the order listed, from the trunk. That recipe is the existing mechanism and already carries the safety: it checks ancestry before removal, refuses a dirty worktree, never forces deletion, and deletes the branch only after removal succeeds. A lane that refuses is left exactly as it is and reported, not forced. Then prune the merged branches beyond those fourteen: each one tested with `git merge-base --is-ancestor` against `main` immediately before deletion, never as a group and never on the strength of this list. Do not touch the eight unlanded lanes or their branches, and re-run the ancestry test immediately before each lane removal too — the list was measured at 11:11 and another session may land or open a lane after it.

Benefit: the policy's closure step actually happens, 4.4 GB of build output is recoverable, and `git worktree list` stops hiding the eight lanes that are real. Tradeoff: a lane's cached `target/` is rebuilt if that name is ever reopened, which [[git-policy]] already judges not to be a reason to keep it. Preserve what works: the eight unlanded lanes and their branches, and any lane whose removal `lane-rm` refuses — a refusal means someone's uncommitted work is there and is the correct outcome, not an obstacle.

## Acceptance
Already run, 2026-09-08: a walk of `.claude/worktrees/*/` testing `git merge-base --is-ancestor HEAD main` printed the 14 names above and counted 8 unlanded; `du -sh .claude/worktrees` printed 4.4G; `git branch --list | wc -l` printed 87; `rg -n '^claim:' memos/work/*.md` returned nothing.

Unrun: after the removals, the same walk lists only the unlanded lanes, `git worktree list` shows the trunk plus those, every lane that refused is named with the reason `lane-rm` gave, and the branch count is reported before and after with every deleted branch proved merged.

Run `just memos-check` once after the work and require success.

Run 2026-09-08 from the trunk at `48148626`. Of the fourteen authorized lanes, eight removed with `just lane-rm` — `drive`, `herd-improve-b2b-1-0`, `herd-improve-b2b-1-1`, `herd-improve-b2b-1-2`, `herd-legible-b2b-1-1`, `improve`, `mine-compact-integration`, `store-cold-v11-v12` — each branch deleted only after its worktree was gone. Six refused and were left exactly as they are: `codex-finish` (37 dirty paths), `legible-cold-open` (21), `graph-source-provenance` (4), `graph-herd-context` (2), all with `contains modified or untracked files, use --force to delete it`; `agent-a1428197a9059983d` and `agent-a85691e7482ae3921` refused one step earlier at `git merge-base --is-ancestor` with `fatal: Not a valid object name` — their worktree directory is named `agent-…` but their branch is `worktree-agent-…`, so `lane-rm <dirname>` cannot address them, and both also hold two dirty paths.

Branches beyond the fourteen: 37 deleted, each tested with `git merge-base --is-ancestor <b> main` immediately before `git branch -d`, which re-tests; every branch checked out in a live worktree was skipped, none refused. `git branch --list | wc -l` 91 before, 54 after. `du -sh .claude/worktrees` 6.2G before, 4.2G after — the directory had grown past the 4.4G measured at 11:11.

Not done, and deliberately: the walk still prints landed-and-present lanes that the fourteen never named — `herd-drive-1107-3`, `herd-improve-1107-0`, `herd-quality-1107-2` (3 dirty), and `compose-services-provide-and-inject`, `the-exit-flag-tests-race-each-other`, `workstation-layout-contract`, the last three sitting on `main`'s own commit because live sessions opened them after this memo was written. A lane opened at `main` is an ancestor of `main` and clean, so the ancestry test cannot tell it from an abandoned one; closing it would take a running session's tree. A stale entry for another session's scratchpad worktree at `/private/tmp/claude-501/-Users-feb-dev-memory/823a29bc-…/mergecheck` shows `prunable` in `git worktree list` and was left alone.
