---
complexity: 5
footprint:
  - resources/doctor.sh
---

# spec01 — doctor globs `references/skills/`, not the pre-rename `skills/`

`resources/doctor.sh`'s `skills` row globbed `"$SKILL_ROOT"/skills/*.md`, a
path commit `aea6dae` (apply-the-prds-rename-table) never updated when the
skill files moved to `references/skills/`. Since that commit, `skills/`
matches nothing on disk, so the row falsely reports `skills broken · skills/
holds no .md file — there is nothing to install` even though all 14 skills
under `references/skills/` are well-formed — the board's own quality gate
failing on a stale path, not a real defect.

This build is already done: both globs (the well-formedness loop and the
`NAMES=` summary line) now read `"$SKILL_ROOT"/references/skills/*.md`, and
the three diagnostic strings that named the old `skills/$base.md` path in
`note`/`fix` text now say `references/skills/$base.md` (and `references/skills/
holds no .md file` for the empty-directory case), so a failure message still
points at a path that exists. Nothing else in the script, and no other file
under `resources/` or `references/`, held the stale glob — checked with
`grep -rn 'skills/\*\.md\|SKILL_ROOT.*skills\b'` across `resources/*.sh` and
`resources/*.py`.

## Acceptance

- [x] `bash resources/doctor.sh` reports the `skills` row `ok`, naming all 14
      files under `references/skills/`, not `broken`.
- [x] No remaining reference in `resources/doctor.sh` globs the pre-rename
      `skills/*.md` path; every skills-row message names `references/skills/`.
- [x] A fixture install holding no skill still reports `skills broken` — the
      new glob reports the tree, it does not report `ok` unconditionally.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
OUT=$(bash resources/doctor.sh 2>&1 || true)
printf '%s\n' "$OUT" | grep -E '^  skills +ok +14 well-formed' > /tmp/skills_row.txt || true
[ -s /tmp/skills_row.txt ] && echo "skills row: OK ($(cat /tmp/skills_row.txt))" || echo "skills row: STILL BROKEN"
STALE=$(grep -rn 'SKILL_ROOT"/skills/\*\.md\|"skills/\$base\|"skills/ holds' resources/doctor.sh || true)
[ -z "$STALE" ] && echo "no stale skills/ path remains" || echo "stale path still present: $STALE"

# The row must still be able to fail: a fixture install with no skill file.
T=$(mktemp -d)
mkdir -p "$T/fx"
cp -R references resources index.md SKILL.md board "$T/fx"/ 2>/dev/null || true
CTL=$(bash "$T/fx/resources/doctor.sh" "$T/fx" 2>&1 | grep -E '^  skills' || true)
rm -f "$T/fx"/references/skills/*.md
NEG=$(bash "$T/fx/resources/doctor.sh" "$T/fx" 2>&1 | grep -E '^  skills' || true)
rm -rf "$T"
case "$CTL" in *ok*) echo "fixture control: ok — $CTL" ;; *) echo "fixture control: UNEXPECTED — $CTL" ;; esac
case "$NEG" in
  *"broken"*"references/skills/ holds no .md file"*)
    echo "fixture negative: broken as required — $NEG" ;;
  *) echo "fixture negative: CHECK IS UNCONDITIONAL — $NEG" ;;
esac
echo "verify complete"
```
