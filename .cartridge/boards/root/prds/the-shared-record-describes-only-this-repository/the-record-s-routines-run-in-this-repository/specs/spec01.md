---
complexity: small
footprint:
  - ".cartridge/memos/routine/quality.md"
  - ".cartridge/memos/routine/hygiene.md"
  - ".cartridge/memos/routine/improve.md"
  - ".cartridge/memos/routine/legible.md"
  - ".cartridge/memos/routine/self-improve.md"
  - ".cartridge/memos/routine/new-routine.md"
  - ".cartridge/memos/routine/distill.md"
---

# spec01 — delete the five foreign routines, rewrite new-routine, unlink distill

Base: superproject HEAD `801aa8e`. All seven files are clean at base (`git status --short
.cartridge/memos/routine` lists only the untracked `rank-cartridges.md`, outside this footprint).

## Decision per routine

| Routine | Verdict | Why |
|---|---|---|
| `quality.md` | **delete** | Every probe runs `kern`, `cargo machete` over `src/`, `tests/one_dispatch.rs`, `just eval-ground`, or `just lane`/`just land`. None exists here: the superproject has no `src/`, and code is changed in PRD lanes (`prd claim` → `prd.ctg/.cartridge/boards/<board>/.lanes/<slug>`, landed by `prd collect`). `audit-cartridges` and `check-cartridge-isolation` (`just audit`, `just isolation`) are what this repo actually gates. |
| `hygiene.md` | **delete** | Probes read `memos/intake/`, `memos/code-fact`, `.kern/data/reflex.json`, and run `kern compact/audit/doctor`. Record upkeep here is `distill` plus the PRD planner routines (`@prd/routine/plan-cartridge-work.md`). |
| `legible.md` | **delete** | Probes walk `src/**/*.rs`, `tests/cited_paths.rs`, `head -3 src/*/src/lib.rs`, and land through `just lane legible-<probe>`/`just land`. |
| `improve.md` | **delete** | Writes `kind: work` memos into `memos/intake/` (work memos retired 2026-09-15; PRDs are the only work record), `kern query`, `git -C memos commit`, `just prd scan`. Its job (find the next thread) is `prd plan` / `@prd/routine/run-board.md` here. |
| `self-improve.md` | **delete** | Built on `memos/SYSTEM.md`, `memos/intake/`, `mcp__kern__query`, `git -C memos`, `.agents/skills/` (this repo has no `.agents/`), and `[[improve]]`, deleted above. A rewrite is a new routine, not an edit; nothing in the record links it. |
| `new-routine.md` | **rewrite** (below) | Its job is real here, and three memos outside the footprint link `[[new-routine]]` (`memory.ctg/.cartridge/memos/system/routine.md`, `memory.ctg/.cartridge/memos/insight/routine-is-prepared-context.md`, `memory.ctg/.cartridge/memos/decision/the-surface-is-declared-in-the-record.md`), plus `prd.ctg/.cartridge/memos/decision/memory--new-work-is-on-the-plan-by-default.md`. Deleting it would break links outside the footprint. |
| `distill.md` | **edit** (below) | Grounded in this repo (`.cartridge/memos`, `memo(op="write")`, `distill_due`) except two wikilinks to deleted routines and two cited paths that do not exist. |

No legacy retention: no stub, alias or "moved to" note replaces a deleted file. Git is the archive.

## Inbound wikilinks (checked, `rg --hidden` over every `*.md` in the repo, excluding `.lanes/`, `target/`, `.state/`)

- To `quality`, `hygiene`, `legible`, `improve`, `self-improve` in the **root record**: only from files
  in this footprint (`distill.md`, `improve.md`, `legible.md`, `hygiene.md`, `self-improve.md`). All go
  with the deletes or the `distill.md` edit.
- From `memory.ctg/.cartridge/memos/**` to `[[quality]]`, `[[hygiene]]`, `[[legible]]`: memory ships
  its own `routine/quality.md`, `hygiene.md`, `legible.md` (different files from the root's), and
  `lookup_from` (`memo.ctg/src/usage.rs:113`) prefers the linking memo's own cartridge. These links
  keep resolving. No widening.
- From board files (`prd.ctg/.cartridge/boards/root/reviews/round-1/keep-the-tree-and-record-true.md`,
  `prd.ctg/.cartridge/boards/memory/prds/**`): not memos of any record; the memo tool never resolves
  them. No widening.
- `.cartridge/memos/decision/the-work-checkpoint-journals-are-not-this-passs-candidate.md` links
  `[[distill]]`, which stays.

Footprint therefore stays exactly the seven files.

## Steps (files edited in the lane; every `cartridge run memo` call runs from the live repo root)

The record is owned through the memo tool (`system/memos.md`). The tool has no delete op, so:

**Never run `cartridge run memo` with the process cwd inside the lane.** The lane checks out the
tracked `.cartridge/init.lua`, and `cartridge.ctg/src/loader/mod.rs::root()` takes the nearest
ancestor holding `.cartridge/init.lua` as the project, so from the lane the CLI treats the lane as
a separate project (no daemon, a second host, or a trust check against the lane's config). Run
every memo call from `/Users/feb/dev/cartridge` and pass the lane in the payload:
`lane=/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/.lanes/<slug>` (the absolute lane
path). `memo.ctg/src/service.rs::native` takes `cwd` from the payload and `record.rs::root` stops at
the lane's `.cartridge/`, so the write lands in the lane's record.

1. `git rm .cartridge/memos/routine/{quality,hygiene,legible,improve,self-improve}.md`.
2. Rewrite `routine/new-routine.md` and edit `routine/distill.md` through managed writes, which
   validate every link of the written memo and refresh the derived index. `body` is the whole file,
   frontmatter included:
   ```sh
   cd /Users/feb/dev/cartridge   # live root, never the lane
   cartridge run memo "$(jq -n --arg cwd "$lane" --rawfile body <draft> \
     '{op:"write",cwd:$cwd,path:"routine/distill.md",body:$body}')"
   ```
   Read the result's warnings and saved status. Write `distill.md` last: it is the surviving memo
   that linked the deleted leaves, so its write is the index refresh after the `git rm`.
3. From `/Users/feb/dev/cartridge`: `cartridge run memo "{\"op\":\"index\",\"cwd\":\"$lane\"}" | jq '.. | strings' | grep -E 'routine/(quality|hygiene|legible|improve|self-improve)\.md'`
   returns nothing for the root record (memory's `@memory/routine/...` entries are expected).

### `distill.md` edits

- Replace the first paragraph ("Sibling of [[hygiene]] ... distill removes volume, never claims.")
  with: "Distillation takes a whole cluster of the record and makes it smaller without making it say
  less. [[@prd/routine/plan-cartridge-work.md]] adds what the record does not hold; distill removes
  volume, never claims."
- `builtin/memo/src/record.rs` → `memo.ctg/src/record.rs` (`distill_due` is at line 426 there).
- `builtin/harness/main.rs` → `harness.ctg/src/lib.rs` (`build_system` is at line 349 there).
- Step 1's `` `type/type.md` `` (the root record holds none; `memo.ctg` ships it) →
  `[[@memo/type/type.md]]`, which resolves (`op:"read"`, `path:"@memo/type/type.md"` returns
  "Declares a kind of authored memo").
- Nothing else changes; frontmatter unchanged.

### `new-routine.md` content (keep frontmatter `kind` and `uses`; replace `description` and the body)

New `description`: "Write a new routine: name the job, gather every ingredient by name, save it
through a managed memo write, prove it resolves." 

Follow `type/routine.md`'s shape (Inputs, Do, Check, Failure):

- **Inputs** — the job in one sentence (an "and" means two routines); read `[[@memo/type/type.md]]`,
  `type/routine.md`, `usage/run-usage.md`; copy the shape of the nearest routine, e.g.
  `@prd/routine/spec-a-prd.md` or `routine/audit-cartridges.md`.
- **Do** — pick the kebab-case leaf (the file name is the handle; `just prompt` and `memo resolve`
  find it by `uses` + `when`, no skill file or slash command is written). Gather every ingredient by
  name: memos by leaf, linked; gates as exact `just` recipes from `.cartridge/justfile`
  (`just --list`); literal `rg`/`git`/`gh`/`cartridge run` commands; files by repo-relative path. A
  routine that changes code says it runs as a PRD (`prd add`, then the board's lane via `prd claim`
  and `prd collect`), never as a direct edit of the shared checkout. Write
  `.cartridge/memos/routine/<leaf>.md` through `memo` `op:"write"` with `kind: routine`,
  `description`, and `uses: - usage: "[[run-usage]]" when: [...]`. Run every
  `cartridge run memo` from the live repo root with the target checkout as payload `cwd`; from
  inside a lane the CLI treats the lane as its own project (its tracked `.cartridge/init.lua`).
- **Check** — the managed write returns saved with no unresolved-link warning;
  `cartridge run memo '{"op":"resolve","cwd":"<checkout>","usage":"run","query":"<a when phrase>"}'`
  lists the new leaf; the cold-read test (mark every point a cold agent would have to go looking;
  each mark is a missing ingredient).
- **Failure** — a refused write names the bad field or link: fix the draft, never write the file by
  hand. A resolve that misses it means the `when` phrases do not name the situation.

Keep it under ~50 lines. It must not name `kern`, `just lane`/`just land`, `.agents/skills`,
`mcp__kern`, `memos/SYSTEM.md` or `lanes-not-a-shared-tree`.

## Acceptance

- [x] `quality.md`, `hygiene.md`, `legible.md`, `improve.md`, `self-improve.md` are gone from `.cartridge/memos/routine/`; `new-routine.md` and `distill.md` remain.
- [x] No routine in `.cartridge/memos/routine/` names the foreign layout (`memos/SYSTEM.md`, `lanes-not-a-shared-tree`, `kern`, `mcp__kern`, `just lane`/`just land`, `memos/intake`, `git -C memos`, `.agents/skills`), and `distill.md` cites no `builtin/` path.
- [x] No memo in the root record or any cartridge's `.cartridge/memos` wikilinks a deleted routine that its own record and the root record no longer hold.
- [x] `new-routine.md`'s `description` matches its new body, and neither it nor `distill.md` cites the unresolvable `type/type.md` (both name `[[@memo/type/type.md]]`).
- [x] `new-routine.md` and `distill.md` were saved through managed `memo` writes with no unresolved-link warning (implementer quotes the write results).

## Verify

Text gate for the layout (weak but sufficient for prose); the link sweep is executed over every
record on disk and was mutation-tested (see analyst-1.md). Exit at base (`801aa8e`, repo, revision 1): **1**
(`not deleted: .cartridge/memos/routine/quality.md`).

```sh
r=.cartridge/memos/routine
for leaf in quality hygiene legible improve self-improve; do
  if [ -e "$r/$leaf.md" ]; then echo "not deleted: $r/$leaf.md"; exit 1; fi
done
for leaf in new-routine distill; do
  if [ ! -f "$r/$leaf.md" ]; then echo "missing: $r/$leaf.md"; exit 1; fi
done
if grep -rEn 'memos/SYSTEM\.md|lanes-not-a-shared-tree|(^|[^a-z_])kern([^a-z]|$)|mcp__kern|just lan[de]([^a-z]|$)|memos/intake|git -C memos|\.agents/skills' "$r"; then
  echo "a routine names the foreign layout"; exit 1
fi
if grep -nE '(^|[^/])type/type\.md' "$r/distill.md" "$r/new-routine.md"; then echo "cite @memo/type/type.md"; exit 1; fi
if grep -nE 'register the handle|prove the gate' "$r/new-routine.md"; then echo "new-routine description is stale"; exit 1; fi
if grep -n 'builtin/' "$r/distill.md"; then echo "distill cites a path this repo does not have"; exit 1; fi
for rec in memory.ctg prd.ctg; do
  if [ ! -d "$rec/.cartridge/memos" ]; then echo "unseeded record: $rec"; exit 1; fi
done
checked=0
for leaf in quality hygiene legible improve self-improve new-routine distill; do
  if [ -e "$r/$leaf.md" ]; then continue; fi
  for rec in .cartridge/memos */.cartridge/memos; do
    if [ ! -d "$rec" ]; then continue; fi
    checked=$((checked + 1))
    if [ -n "$(find "$rec" -name "$leaf.md" -print)" ]; then continue; fi
    if grep -rEn --include='*.md' "\[\[(routine/)?$leaf(\.md)?(\|[^]]*)?\]\]" "$rec"; then
      echo "dangling wikilink to deleted routine $leaf in $rec"; exit 1
    fi
  done
done
if [ "$checked" -lt 17 ]; then echo "link sweep read only $checked records"; exit 1; fi
```

The seeding guard is the explicit `memory.ctg`/`prd.ctg` check: those two records hold every
out-of-footprint link to these leaves. The `checked` floor alone is not a seeding guard, because
`web.ctg/.cartridge/memos` is tracked in the superproject, so root + web already count 5 × 2 = 10.
Floor 17 only proves the sweep ran over more than those two (85 with all 17 records present). The
block writes nothing.

## Follow-ups (outside this footprint, not widened)

- `.cartridge/memos/decision/the-trunk-checkout-is-a-landing-pad.md` is superseded (it names
  `/Users/feb/dev/sys`, `just lane`, `just land`, `just lane-rm`). It is out of scope here. The
  prd-owning coordinator is adding a separate PRD for it.
- `.cartridge/memos/system/vision.md:144` lists `quality.md`/`hygiene.md` as a dated finding; it is
  prose, not a link, and stays true as history. The parent PRD may want to strike it when this lands.

## Review notes carried into implementation (round 2, clarification only)

- The lane is `/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/root/.lanes/the-shared-record-describes-only-this-repository-the-record-s-routines-run-in-this-repository`
  (`lane()` joins the parent and child slugs with `-`). Check it with `test -d` before the first memo write.
- In the lane pass, the memory.ctg/prd.ctg check proves only that the submodules were seeded (memory.ctg's
  record is gitignored except `type/`); the outside links are checked against the live records in the repo
  pass. In step 3, any `@memory/routine/...` or `@prd/...` entry in the index output is expected; only a root
  `routine/(quality|hygiene|legible|improve|self-improve).md` entry is a failure.
- The superseded landing-pad decision is handled by `@root/the-landing-pad-decision-describes-this-repository-s-lanes-not-a-checkout-that-no-longer-exists`.

