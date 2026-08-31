---
complexity: 12
footprint:
  - resources/doctor.sh
---

# spec01 — the board row walks up for `.pearde/`, not `prds/`

`resources/doctor.sh`'s contract-path (`board`) row walked up from `$START`
looking for a directory literally named `prds/` — the pre-migration
contract. On a repo already on the `.pearde/` layout it walked straight past
the real board and, if some unrelated ancestor happened to hold a `prds/`
dir (a master board one level up, in this repo's own case), reported that
one `ok` instead — the false-ok failure mode the PRD names. Every other row
in the file (`members`, `vision`, `origin`, `memos`, `workflows`,
`knowledge`, `serve`, `plan`, `harnesses`) already treats `$BOARD` as the
`.pearde/` root, matching `resources/board/plan.py`'s `find_board()` and
`resources/guard.py`'s `board_of()` — this was the one row left on the old
assumption.

This unit is already built: the walk now looks for `$d/.pearde` (mirroring
`find_board`/`board_of`, no git-toplevel comparison — that check does not
hold once `.pearde/` can be its own nested repo, and neither reference
implementation keeps it), `BOARD` is set to the `.pearde/` root, and `PRDS`
(`$BOARD/prds`) is what the PRD count and the `find` walk read. The
"leftover old layout" fallback (three levels down, dot-dirs too) now names
`.pearde/prds` as the fix's destination and calls out the sibling dirs
(`memos/`, `workflows/`, `settings.md`, `vision.md`, `.state/`) that move
alongside it — there is no single `pearde` command that migrates a board yet,
so the fix line is the literal `git mv` a person or a script can run.

## Acceptance

- [x] On this repo, `resources/doctor.sh` reports the `board` row `ok`
  against `.pearde/prds`, not against any other `prds/` directory on the
  machine.
- [x] The `board` row alone never sets doctor's `BROKEN` flag when it reads
  `ok` — `row()` only sets `BROKEN` on the literal string `broken`.
- [x] Run against a fixture repo with a root-level `prds/` and no `.pearde/`,
  the row reports `broken` and its `fix:` line names `git mv <found-prds>
  <root>/.pearde/prds` as the destination.
- [x] Run against a fixture with `.pearde/prds/` in place, the row reports
  `ok` and the PRD count matches what is actually under `.pearde/prds/`.
- [x] Run against a fixture with no board at all, the row still reports
  `off`, unchanged.

## Verify and Proof

```sh
# `collect` runs this block with `bash -e -o pipefail`. `doctor` exits 1
# whenever ANY row is broken — `skills`, `guard` and `origin` are broken here
# for reasons this PRD does not own — so `doctor | grep` fails the whole
# pipeline even when the grep matches. Every doctor run is therefore captured
# with `|| true` and grepped from the variable, never piped directly.
DOCTOR=/Users/feb/dev/infra/pearde/resources/doctor.sh
say() { printf '%s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; exit 1; }

out=$(bash "$DOCTOR" /Users/feb/dev/infra/pearde 2>&1 || true)
printf '%s\n' "$out" | grep -q '^  board .*ok .*\.pearde/prds' \
  || fail "live board row is not ok on .pearde/prds"
say "ok  live board row"

T=$(mktemp -d); OLD="$T/old-layout"
mkdir -p "$OLD/prds/some-prd"
printf -- '---\nstate: open\n---\n# a prd\n' > "$OLD/prds/some-prd/prd.md"

out=$(bash "$DOCTOR" "$OLD" 2>&1 || true)
printf '%s\n' "$out" | grep -q '^  board .*broken' \
  || { rm -rf "$T"; fail "old layout not reported broken"; }
printf '%s\n' "$out" | grep -q 'fix:.*mkdir -p .*\.pearde.*git mv .*\.pearde/prds' \
  || { rm -rf "$T"; fail "fix line does not lead with mkdir -p"; }
say "ok  old layout broken, fix line repairs"

# the fix line must actually work, not merely read well: run doctor's own
# emitted command verbatim rather than a hand-written equivalent
( cd "$OLD" && git init -q . && git add -A && git -c user.email=t@t -c user.name=t commit -qm x )
fixline=$(printf '%s\n' "$out" | sed -n 's/^ *fix: \(.*\) — the board path.*/\1/p' | head -1)
test -n "$fixline" || { rm -rf "$T"; fail "could not extract the fix line"; }
( cd "$OLD" && eval "$fixline" ) || { rm -rf "$T"; fail "doctor's own fix line failed"; }
say "ok  fix line executed clean"

printf -- '---\nlanguage: English\n---\n' > "$OLD/.pearde/settings.md"
out=$(bash "$DOCTOR" "$OLD" 2>&1 || true)
printf '%s\n' "$out" | grep -q '^  board .*ok .*1 PRDs' \
  || { rm -rf "$T"; fail "repaired board not ok"; }
say "ok  repaired board reads ok"

EMPTY="$T/no-board"; mkdir -p "$EMPTY"
out=$(bash "$DOCTOR" "$EMPTY" 2>&1 || true)
printf '%s\n' "$out" | grep -q '^  board .*off' \
  || { rm -rf "$T"; fail "absent board not reported off"; }
say "ok  absent board reads off"

rm -rf "$T"
echo VERIFY_OK
```
