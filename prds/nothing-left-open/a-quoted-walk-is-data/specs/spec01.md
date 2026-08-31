---
complexity: 4
footprint:
  - resources/guard.py
  - references/parts/guard.md
---

# spec01 — the Bash hook matches a walk on what the shell runs

`guard.py pre`, on a `Bash` call, matches the `WALKS` rules against
`data_free(command)` instead of the raw command: heredoc bodies and quoted
strings are blanked first, except a string given to a command that runs it —
`find`, `grep`, `rg`, `ls` (the pattern *is* the walk) and `sh`/`bash`/`zsh`
/`eval` (the string is a command). A prefix (`env`, `sudo`, `X=1`) does not
hide the command word behind it. A walk after a heredoc, after a `;`, or
piped into a quoted interpreter is still the walk. Nothing else in the hook
moves; the deny text is unchanged.

`references/parts/guard.md`'s refusals table says, on the walk row, that a
walk carried as data — a script piped to python, a fixture, a refusal quoted
into a memo — is not a walk.

## Acceptance

- [x] the probe prints `19 checks · 19 pass · 0 fail` — `a-quoted-walk-is-data -> 19 checks · 19 pass · 0 fail`
- [x] guard-on-is-one-command still `78 checks · 78 pass · 0 fail` — `the-tool-keeps-its-word/guard-on-is-one-command -> 78 checks · 78 pass · 0 fail`
- [x] the-skill-tree-is-guarded still `41 checks · 41 pass · 0 fail` — `nothing-left-open/the-skill-tree-is-guarded -> 41 checks · 41 pass · 0 fail`
- [x] the-loop-is-commands: no count dropped from its baseline (`60 checks`, one pre-existing red line `loop.md is 130 lines` from another session's dirty file, or 60/60 once that lands) — `the-loop-is-commands -> 60 checks · 60 pass · 0 fail`, no `  FAIL ` line at all
- [x] `guard status` on this repo still reads `ok … skill tree guarded`

## Verify and Proof

Run from anywhere — `R` walks up to the code repo, `B` is the board under it.
Exits 0 exactly when all five boxes hold.

```sh
R="$PWD"; while [ ! -f "$R/resources/guard.py" ] && [ "$R" != "/" ]; do R="$(dirname "$R")"; done
P="$R/.pearde/prds"; bad=0

# box 1 — this PRD's probe is green
got=$(bash "$P/nothing-left-open/a-quoted-walk-is-data/probe/verify.sh" | tail -1)
echo "a-quoted-walk-is-data -> $got"
[ "$got" = "19 checks · 19 pass · 0 fail" ] || bad=1

# boxes 2-3 — the regression probes hold their baselines
for e in "the-tool-keeps-its-word/guard-on-is-one-command|78 checks · 78 pass · 0 fail" \
         "nothing-left-open/the-skill-tree-is-guarded|41 checks · 41 pass · 0 fail"; do
  got=$(PEARDE_GUARD_STATE=$(mktemp -d) bash "$P/${e%|*}/probe/verify.sh" | tail -1)
  echo "${e%|*} -> $got"
  [ "$got" = "${e#*|}" ] || bad=1
done

# box 4 — the count never drops from 60; only the loop.md length line may be red
# (grep is case-SENSITIVE on `  FAIL ` — the probe's failure format — because
# `grep -i FAIL` also matches "failed"/"Failure" inside *ok* lines and would
# flag a clean run red)
out=$(PEARDE_GUARD_STATE=$(mktemp -d) bash "$P/the-board-runs-itself/the-loop-is-commands/probe/verify.sh")
echo "the-loop-is-commands -> $(echo "$out" | tail -1)"
case "$(echo "$out" | tail -1)" in "60 checks"*) ;; *) bad=1 ;; esac
# a FAIL line other than the tolerated loop.md length one. The blank grep
# finding nothing is the clean case, so it may not exit nonzero under -e.
if echo "$out" | grep '  FAIL ' | grep -v 'loop\.md is [0-9]* lines'; then bad=1; fi

# box 5 — guard status on this repo
python3 "$R/resources/guard.py" status "$R" | head -1 | tee /dev/stderr | grep -q 'ok .*skill tree guarded' || bad=1

exit $bad
```
