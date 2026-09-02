---
complexity: 5
footprint:
  - references/parts/machine.md
  - references/skills/pearde-all.md
  - references/files.md
  - index.md
---

# spec05 — the dispatch verb described where the machine is described

`references/parts/machine.md` says, in three places, that this command moves
nothing and that dispatch is the sibling PRD. That was true when it was
written and stops being true with spec01. This unit corrects those claims where
they stand, gives `dispatch.py` its manifest row and its `@@machine` scope
place, and gives the skill its verb.

## What already stands

Nothing — this is the documentation half, and the probe wrote no reference
file. The claims to correct were read and located:

- `references/parts/machine.md` line 18: *"**It moves nothing.** No claim, no
  transition, no dispatch, no write to any board"*, and line 20 naming
  `the-machine-frontier-is-dispatched-in-parallel` as the future PRD; its
  `## What it does not do` section; its `## The waves` section, which describes
  the wave cut as a plan and must now say what the pool does with it.
- `references/skills/pearde-machine.md` line 22, the same claim.
- `references/files.md` line 148, the `resources/board/machine.py` row.
- `index.md` line 75, the `@@machine` scope row.

## What is left

Correct the four files. The read-only claim becomes a claim about the **default
mode**, not the command: `pearde machine` still moves nothing, and `pearde
machine dispatch` is the verb that does. Add the verb, its flags, the liveness
rule and the refusal rule to `references/parts/machine.md`; add
`@resources/board/dispatch.py` to the `@@machine` row and a row of its own to
`references/files.md`.

`references/settings.md` is held by a concurrent session — append after the
last row only, and only if a new key is needed. None is: `--workers` is a
dispatch-time flag and `machine-ceiling` already exists.

## Design notes

- **The three settled forks stay settled and stay written.** `/board/all` is
  still a read-only page with no write door; discovery is still `ensure` +
  `/status` with no machine-wide registry; a board's own `settings.md` is still
  never written. Say so where the dispatch verb is described, because the verb
  is what would make a reader doubt it.
- **Correct the claim, do not add a second one.** @references/parts/machine.md
  is the one place the command is described; a dispatch section beside a
  paragraph still saying "no dispatch" is the drift this repo has a workflow
  named after.

## Acceptance

- [x] `references/parts/machine.md` no longer says the command moves nothing without qualifying it to the default mode
- [x] It carries a `## Dispatch` section naming the verb, `--dry`, `--once`, `--workers`, `--adapter`, `--deadline`, and what each does
- [x] That section states the liveness rule (a launch is not a worker; grace window plus log scan; one re-dispatch) and the refusal rule (`gate_claim` re-asked per row; every refusal named)
- [x] It restates that no board's `settings.md` is written, that discovery is still `ensure` + `/status`, and that `/board/all` gains no write door
- [x] `references/skills/pearde-machine.md` describes the verb and drops the unqualified "no dispatch" claim
- [x] `references/files.md` has a row for `@resources/board/dispatch.py`
- [x] `index.md`'s `@@machine` row names `@resources/board/dispatch.py`
- [x] `python3 resources/index.py check` reports no new problem and `bash resources/doctor.sh` is no worse than before the change
- [x] `references/settings.md` is in no spec's `footprint:` in this PRD, so `collect` cannot commit it whoever else is editing it — no new settings key is needed (`--workers` is a dispatch-time flag, `machine-ceiling` already exists)

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
set -e -o pipefail
# the unqualified claim is gone from both, and each says what the verb does
if grep -qE '^\*\*It moves nothing\.\*\*' references/parts/machine.md; then
  echo "FAIL the unqualified claim still stands"; exit 1
fi
grep -q '^## Dispatch' references/parts/machine.md
for w in -- '`--dry`' '`--once`' '`--workers N`' '`--adapter <id>`' '`--deadline S`'; do
  [ "$w" = "--" ] || grep -q -- "$w" references/parts/machine.md
done
grep -q 'launch grace' references/parts/machine.md
grep -q 'transitions.gate_claim' references/parts/machine.md
grep -q "No board's .settings.md. written" references/parts/machine.md
grep -q 'no registry' references/parts/machine.md
grep -q 'machine dispatch' references/skills/pearde-all.md
if grep -q 'This command reads. It does not move.' references/skills/pearde-all.md; then
  echo "FAIL the skill still makes the unqualified claim"; exit 1
fi
# the manifest and the scope row
grep -q '@resources/board/dispatch.py' references/files.md
grep -q '@resources/board/dispatch.py' index.md
# This unit does not own references/settings.md and cannot commit it: `collect`
# scopes the commit to the specs' `footprint:` paths, and the path is in none
# of them. That is what the box claims. A `git diff` over the path would assert
# the WHOLE TREE is clean there — a different, stronger claim this unit is not
# entitled to make, and one a third session editing that file breaks daily.
feet=$(sed -n '/^footprint:/,/^---$/p' \
  .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/specs/spec01.md \
  .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/specs/spec02.md \
  .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/specs/spec03.md \
  .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/specs/spec04.md \
  .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/specs/spec05.md)
# the guard on the guard: an empty read here would pass this check for the
# wrong reason, the way a glob that matches nothing did before it was spelled out
[ -n "$feet" ]
printf '%s\n' "$feet" | grep -q 'resources/board/dispatch.py'
if printf '%s\n' "$feet" | grep -q 'references/settings.md'; then
  echo "FAIL a spec footprint claims references/settings.md"; exit 1
fi
# index.py check is repo-wide: printed, deciding only its own footprint's lines
idx=$(python3 resources/index.py check 2>&1 || true)
[ -n "$idx" ] || idx="(index.py check printed nothing)"
printf '%s\n' "$idx"
if printf '%s\n' "$idx" | grep -qE '^(resources/board/(dispatch|machine)\.py|references/(parts/machine|skills/pearde-all)\.md)\b'; then
  echo "FAIL index.py check names a file this spec owns"; exit 1
fi
```
