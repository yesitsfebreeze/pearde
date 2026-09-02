---
complexity: 4
footprint:
  - resources/doctor.sh
---

# spec02 — `doctor` says when the SessionStart hook is missing

`doctor`'s `guard` row gains one note, exactly the one
`@resources/guard.py status` already prints: an install whose
`.claude/settings.json` holds the three guard hooks and not the fourth is told
so, in the row that already reads that file.

**Not built.** `@resources/doctor.sh` was held by two other implementers'
uncommitted work through this PRD's probe pass and was left untouched.
`@resources/guard.py` carries the same note already (spec01), so the two
readers agree the moment this lands. This PRD's probe harness section E is red
until it does, and green after — it is the check for this spec.

**The edit.** One insertion in the guard row's `ok` branch. The anchor is the
two lines:

```sh
    row guard ok "wired in $GSET${tk:+ · $tk} · skill tree guarded"
    [ -z "$tk" ] && note "no MAX_THINKING_TOKENS — the other half of the fix, @references/parts/guard.md"
```

Add directly under them, at the same indent, inside the same `elif` branch:

```sh
    grep -q 'serve\.py ensure' "$GSET" 2>/dev/null \
      || note "no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it"
```

Nothing else moves. The row stays `ok` — a missing session hook is not a
broken guard, the same way a missing `MAX_THINKING_TOKENS` is not. `--fix`
writes nothing: a settings file is the reader's, and `pearde guard on` is the
reader asking — @references/parts/guard.md.

## Acceptance

- [x] `bash resources/doctor.sh <repo>` on a repo wired by `pearde guard on` prints no `no SessionStart hook` line
- [x] The same command on a repo whose `SessionStart` entry has been deleted by hand prints, under the `guard` row, `no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it`
- [x] That repo's `guard` row still reads `ok`, and `doctor`'s exit code is unchanged by the note alone
- [x] `doctor --fix` on that repo writes nothing into its `.claude/settings.json`
- [x] Section E of this PRD's probe harness is green
- [x] `bash resources/doctor.sh` in this repo prints the same rows it printed before, plus this note where it applies

## Verify and Proof

`bash resources/doctor.sh` is a board-wide gate whose exit carries every other
PRD's row, so it is captured and grepped rather than gated on: the rows stay
visible and only this spec's own footprint decides the exit.

```sh
bash .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
out=$(bash resources/doctor.sh 2>&1 || true)
printf '%s\n' "$out" | grep -E '^  guard +ok'
printf '%s\n' "$out" | grep -F 'no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it'
bash .pearde/prds/seven-closed-probes-drifted-red/the-doctor-completes-without-a-home/probe/verify.sh
bash .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh
```
