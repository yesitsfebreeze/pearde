# The in-flight rewrite lands in reviewable commits — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits` (`prd.md`).
Scope: one leaf. `cartridge.ctg` has one line of history.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; ratings are delegated to the agent.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL). Children inherit the used rounds (review-plan step 7).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**. The original outcome was to commit the 2026-09-14 working tree. That tree landed as the single commit `b4d553f`. It cannot be split now without rewriting pushed history, which the PRD itself forbids. Its `fabric`/`graph`/`evidence` modules were then deleted by `939e7d1`. The same need, one reviewable base for every sibling leaf, reappeared as a divergence:

- Local `main` `e8a4da3` has two unpushed commits, `c9ef10b` and `e8a4da3`.
- `origin/main` = `transport-design` `ba198f4` (worktree `ws/cartridge.ctg`) has nine commits `main` lacks.
- The merge base is `b02b200`, and 16 files changed on both lines.
- `origin/main`'s `src/transport/rpc.rs` uses `mpsc::unbounded_channel`. The bounded queues exist only in the unpushed `c9ef10b`.

The PRD was rewritten to that outcome.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `91302f9db6a8a988c2be9f5614e1f53891102bf9645a533c382a59eb6e8631e7`. Prior text (prd.ctg HEAD `077e57a2`): `f37d2e216fcdcfbdd648826caa4515483baef92d34ac4278b6ebf732b5298517`.
Composition:
- root `24aa2be` (dirty; cartridge.ctg gitlink `d2a761e`);
- cartridge.ctg `main` `e8a4da3`, clean, ahead 2 and behind 9 of `origin/main`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`, clean;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 18 | Every sibling leaf needs one base, and the bounded queues are missing on the route taken. −2: two live sessions are committing minutes apart, so the gap may close before anyone claims the leaf. |
| Ownership and reuse | 17 | Runtime-owned; reuses `git rebase` and PORTING.md coordination. −3: the landing overlaps the active transport-design session, and the root gitlink is the coordinator's. |
| Dependencies and slices | 18 | No hard prerequisites, and it is the first ready leaf. −2: a 16-file conflict set may need more than one session. |
| Acceptance and baseline | 19 | `rev-list --left-right` gives a binary check; the kept and surviving parts are named; gates have a cwd. −1: "survive" is judged by review, not a test. |
| Failure and compatibility | 18 | Disposable branch, no force-push, and unpushed commits kept until the gates pass; a design choice escalates to a question memo. −2: no rollback for porting branches already rebuilt on the new head. |
| Reviewer total | 90 / 100 | |

Result: **PASS**.
Findings:
1. Non-blocking: re-probe the divergence before claiming, because it may already be resolved.
2. Non-blocking: the leaf is about 305 words, above the 300 aim.

Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- `git log`, `git rev-list`, `git merge-base` and `git diff --name-only` in `cartridge.ctg` and `ws/cartridge.ctg`;
- `rg` over `src/transport/rpc.rs` on both lines;
- `just --list` from `/Users/feb/dev/cartridge`, where `check` and `test` route through `cartridge-development.md` to `cartridge.ctg/justfile`;
- `shasum -a 256`.

No product gates were run.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: probe the divergence, then claim.
