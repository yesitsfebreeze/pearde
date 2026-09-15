---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "30m"
---

# [[@prd/routine/plan-cartridge-work.md]] ends at `just memos-check` and never commits, so an assessment's proposals sit untracked in a record repository that another session is free to sweep with `git add -A`.

## Do

Approved 2026-09-08 as "Approve, and extend to /improve" [[approve-committing-the-assessment-output]]. The step is added to both `memos/routine/self-improve.md` and `memos/routine/improve.md`.

Observed defect, measured 2026-09-08 at 10:55 in `/Users/feb/dev/memory`, code revision `36d6def6`. [[@prd/routine/plan-cartridge-work.md]] step 4 requires `just memos-check` and step 5 requires it again; neither step commits, and [[@prd/routine/plan-cartridge-work.md]] step 6 ends the same way. `git -C memos status --short` shows 172 dirty paths, five of them this assessment's own output — `work/memory-mcp-never-answers-initialize.md`, `work/the-build-cache-is-off-while-its-store-sits-over-limit.md`, `intake/approve-memory-mcp-handshake-investigation.md`, `intake/approve-kache-index-open-investigation.md`, `intake/a-swapped-skills-directory-goes-stale-until-restart.md` — all untracked, beside another session's in-flight compaction. [[git-policy]] says the shared memo repository has separate ownership and commits and that git history, not a clean status or an agent's assurance, proves work was preserved; nothing in the tree commits the record, so an assessment whose proposals are never answered leaves them at the mercy of the next `git add -A`.

Proposed scope: add one step to `memos/routine/self-improve.md`, after the step-4 gate, and the same step to `memos/routine/improve.md`, after its step-6 gate. Commit the files that run authored in `memos/`, by explicit path, with a message naming the run — never `git add -A`, never another session's dirty paths, never the generated indexes beyond what the named memos' own regeneration touched. Change nothing else in either routine.

Benefit: an assessment's output survives a sibling session and a restart. Tradeoff: a commit per assessment in a record repository that already carries many, which [[git-policy]] already accepts as microscopic commits. Preserve what works: the gate stays exactly one run, the indexes stay generated, and blocked work stays blocked — committing a proposal is preservation, not approval.

## Acceptance
Already run, 2026-09-08: `git -C memos status --short | wc -l` printed 172, and the five paths above appear as `??`.

Unrun: after the instruction change, an assessment run ends with `git -C memos log --oneline -1` naming its own commit, and `git -C memos status --short` no longer lists that run's authored files while every path it did not author stays exactly as it was.

Run `just memos-check` once after the change and require success.

Done 2026-09-08. The commit bullet landed after the `just memos-check` gate in
`memos/routine/self-improve.md` step 4 and in `memos/routine/improve.md`
step 6, nothing else in either file changed. This run executed the unrun check
on itself: `git -C memos log --oneline -1` printed `4af7dc9c improve ends by
committing the memo it authored`, `git -C memos status --short` no longer
listed either routine file, and the 65 paths it did not author stayed exactly
as they were. `just memos-check` green, 3 tests passed.
