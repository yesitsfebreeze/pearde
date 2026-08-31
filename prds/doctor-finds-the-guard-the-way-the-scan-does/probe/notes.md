# Probe notes

## Repro (before fix)

`bash resources/doctor.sh /Users/feb/dev/infra/pearde` reported:

    guard   broken  /Users/feb/dev/infra/pearde/resources/guard.py does not refuse a hand-walked board

Root cause: `doctor.sh`'s guard-row walk (around line 249, pre-fix) searched
upward for a literal `d/prds` directory (the pre-migration board layout) to
locate `.claude/settings.json`. `/Users/feb/dev/infra/pearde/prds` does not
exist (this board is migrated to `.pearde/prds`), but `/Users/feb/dev/infra/prds`
does exist — it is a DIFFERENT project's (old-layout) board. The walk climbed
past this repo and picked `/Users/feb/dev/infra/.claude/settings.json`
instead of `/Users/feb/dev/infra/pearde/.claude/settings.json`. The guard
probe was then run with `cwd=/Users/feb/dev/infra/.claude`, from which
`guard.py`'s own `board_of` walk (which correctly looks for `.pearde/`, not
`prds/`) finds no board and no-ops — so the probe never denies, and doctor
reports `guard broken`.

Confirmed directly (measurement matches the brief's contract):

    echo '{"tool_name":"Bash","tool_input":{"command":"find prds -name prd.md"},"cwd":"/Users/feb/dev/infra/pearde"}' \
      | PEARDE_GUARD_STATE=$(mktemp -d) python3 resources/guard.py pre
    -> contains "deny"

    echo '{"tool_name":"Bash","tool_input":{"command":"find prds -name prd.md"},"cwd":"/Users/feb/dev/infra"}' \
      | PEARDE_GUARD_STATE=$(mktemp -d) python3 resources/guard.py pre
    -> empty (no deny)

## Fix

`doctor.sh`'s guard-row walk now searches for `d/.pearde` (mirroring the
`board` row's own walk just below it, and `resources/guard.py`'s `board_of`)
instead of `d/prds`, with the same dirname-fixpoint guard the board row uses.

## After fix

`bash resources/doctor.sh /Users/feb/dev/infra/pearde` reports:

    guard   ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json ...
