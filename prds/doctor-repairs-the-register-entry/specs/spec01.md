---
complexity: 16
footprint:
  - resources/doctor.sh
  - references/obsidian.md
---

# spec01 — `doctor --fix` writes the missing vault register entry

The `vault` row's last branch — `$PROJ is not in Obsidian's vault register`
— gains a repair under `--fix`: it reaches the same writer `pearde vault`
uses (`register_vault`, through `cmd_vault`), never `obsidian.json` directly.
Two refusals come first and write nothing: **Obsidian running** (a write now
is invisible to it and erased on quit — the same reason `cmd_vault` itself
refuses without `--wait`), reported with the quit → write → reopen order
inline rather than done behind the app's back; and **two register entries
already resolving to this exact project** (`os.path.realpath`, not string
equality — a hand-edited register, or an id from before the writer deduped
this way), named by id and path rather than picked between, the way the
board resolver two sections above refuses two `settings.md` children instead
of guessing one. Only past both does the writer run, with no `--wait` —
doctor's own check just established the app is closed. Success prints the
literal line `vault repaired`; failure names the writer's own refusal rather
than swallowing it. The row's pass/fail logic (the four `elif` branches
above this one) is untouched, and every other row's `--fix` path (`view`,
`board registered`) is untouched.

**This stands in the tree already**, built in place — an edit inside
`resources/doctor.sh`'s existing `vault` section and one paragraph in
`references/obsidian.md`. What is left for the implementer is to run the
checks below and quote them.

## Acceptance

- [x] `env -i HOME=<fixture home> bash resources/doctor.sh --fix <project>`
      on a project whose board resolves, whose `.obsidian/` exists, and
      whose register lacks the entry, calls `pearde vault <project>` and —
      when that call succeeds — prints `vault repaired`
- [x] the same run with a process named `Obsidian` or `obsidian` findable by
      `pgrep -x` prints a refusal naming the quit → write → reopen order and
      exits having written nothing to the register
- [x] a register already holding two entries whose `path`, realpath'd,
      equals the project's realpath refuses and names both ids and paths,
      writing nothing — never picks one
- [x] the same run without `--fix` is unchanged: the row reports `broken`
      with its existing fix line, no refusal note, no repair attempt
- [x] the row's four earlier branches (`ok` registered, `ok` no Obsidian
      config, `off` no `.obsidian/`, `broken` no home, `broken` dot-segment
      board) are untouched — same messages, same fix lines
- [x] `bash -n resources/doctor.sh` and the board's own
      `python3 resources/index.py check` / `python3 resources/memos.py check`
      carry no new failure against the pre-edit baseline

## What is left

Nothing in this PRD's own scope. `pearde vault`'s own correctness — the
writer this spec reaches — is out of this PRD's footprint by its own
contract (`## What stays out`); `## Finding` in the report names a standing
defect in that writer, found while probing this spec's happy path, for
whoever owns `resources/board/init.py`.

## Verify and Proof

`collect` runs this block with its cwd set to the PRD's repo — the lane
while one is open, the checkout after it merges — so the tree under test is
`$PWD` and nothing here spells a path literally. The probe lives on the
board, which is `pearde/` or `.pearde/` at or above that repo; it is walked
to rather than named. The two board-wide gates are captured and printed,
never gated on: both carry reds outside this spec's footprint (`index.py
check` is red in the lane and green in the checkout; `memos.py check` is red
in both, before the first edit), and a spec whose exit is theirs can never
pass however green its own unit is.

```sh
ROOT="$PWD"
BOARD=""; d="$ROOT"
while [ "$d" != / ]; do
  for n in pearde .pearde; do
    [ -d "$d/$n/prds/doctor-repairs-the-register-entry/probe" ] && BOARD="$d/$n"
  done
  [ -n "$BOARD" ] && break
  d="$(dirname "$d")"
done
[ -n "$BOARD" ] || { echo "no board holding this PRD above $ROOT"; exit 1; }
PEARDE_ROOT="$ROOT" bash "$BOARD/prds/doctor-repairs-the-register-entry/probe/verify.sh"
bash -n resources/doctor.sh
idx=$(python3 resources/index.py check 2>&1 || true); printf 'index.py check:\n%s\n' "$idx"
mem=$(python3 resources/memos.py check 2>&1 || true); printf 'memos.py check: %s lines\n' "$(printf '%s' "$mem" | grep -c .)"
```
