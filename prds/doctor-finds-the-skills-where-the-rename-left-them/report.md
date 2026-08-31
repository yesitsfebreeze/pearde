# Report — doctor-finds-the-skills-where-the-rename-left-them

**Verdict: DONE.** 1 spec, 3 acceptance boxes, all 3 re-run personally and
closed. Repo gate: `index.py check` green, `memos.py check` green,
`doctor.sh` `skills` row green.

## Specs

| Spec | Boxes | Verify block | Result |
|---|---|---|---|
| spec01 — doctor globs `references/skills/` | 3/3 | exit 0 under `bash -e -o pipefail` | pass |

## What was on disk

The probe's pass-one edit was already in the working tree, uncommitted, and
correct. `git diff resources/doctor.sh` shows five lines: both globs
(`for f in "$SKILL_ROOT"/references/skills/*.md` at line 69, `NAMES=` at line
100) and the three diagnostic strings that named `skills/$base.md`. I changed
no code. I re-ran every check rather than trusting the analyst's pre-ticked
boxes.

## Box 1 — the row reports ok

```
  skills      ok      14 well-formed · pearde-doctor pearde-drill pearde-graph
  pearde-knowledge pearde-master pearde-memo pearde-persona-ask
  pearde-persona-create pearde-persona pearde-report pearde-scout pearde-view
  pearde-workflow pearde
```

14 files, matching `ls references/skills/*.md | wc -l` = 14.

## Box 2 — no stale path remains

Swept the whole tree, not just `doctor.sh`:

```
$ grep -rn 'SKILL_ROOT"/skills\|/skills/\*\.md' --include='*.sh' --include='*.py' --include='*.md' .
resources/doctor.sh:69:   for f in "$SKILL_ROOT"/references/skills/*.md; do
resources/doctor.sh:100:  NAMES=$(for f in "$SKILL_ROOT"/references/skills/*.md; ...
resources/install.sh:75:  for f in "$ROOT"/references/skills/*.md; do
```

No hit on the pre-rename path. `install.sh` was already correct — it was never
part of the regression. Every skills-row message string in `doctor.sh`
(lines 78, 80, 82, 92) names `references/skills/`.

## Box 3 — the row can still fail

This is the box that mattered: a fix that makes a check unconditional passes
the first two boxes and tests nothing. I built a fixture install — the repo
tree copied to a temp dir, `doctor.sh` pointed at it — and ran four cases.

| Case | Fixture state | `skills` row |
|---|---|---|
| A control | 14 skills present | `ok 14 well-formed · …` |
| B empty | `references/skills/*.md` deleted | `broken references/skills/ holds no .md file — there is nothing to install` |
| C absent | `references/skills/` directory removed | `broken references/skills/ holds no .md file …` |
| D malformed | 2 skills, one whose `name:` disagrees with its filename | `broken 2 skills · 1 problem` + `references/skills/wrong-name.md says name: pearde-view — an install would build it as pearde-view/` |

Case E: with the fixture emptied, `doctor.sh` exits 1.

The mechanism that keeps case C honest is `[ -e "$f" ] || continue` at line 70
— an unmatched glob leaves `$f` as the literal pattern, `-e` fails, `SKN` stays
0, and the `-eq 0` branch fires. That is the same guard that made the old stale
glob report `broken`, so the failure path is unchanged by this fix; only the
path it globs moved.

Every `broken` message now names a path that exists on disk, so the fix line a
reader is handed points somewhere real.

## Spec amended

`specs/spec01.md` carried only two acceptance boxes. I added the third box and
extended its `## Verify and Proof` block with the fixture control/negative pair,
so the regression stays guarded on every future `collect`. The block ends on an
explicit `echo "verify complete"` and exits 0 — no bare trailing `grep`.

## Repo gate

| Check | Result |
|---|---|
| `python3 resources/index.py check` | exit 0 |
| `python3 resources/memos.py check` | exit 0 |
| `bash resources/doctor.sh` — `skills` row | `ok` |

## Defects outside this scope — not fixed

`doctor.sh` exits 1 on this tree for two rows this PRD does not own:

| Row | Message |
|---|---|
| `guard` | `resources/guard.py does not refuse a hand-walked board` |
| `origin` | `19 derived · 3 with no from:` |

Both are reported, not touched. Until they are closed, `doctor.sh` exits 1 as a
whole, so any verify block on this board must capture its output with `|| true`
rather than piping it into `grep`.

## Footprint

`resources/doctor.sh` — unchanged by me; the probe's uncommitted edit stands
as pass one. Nothing committed; the orchestrator collects.
