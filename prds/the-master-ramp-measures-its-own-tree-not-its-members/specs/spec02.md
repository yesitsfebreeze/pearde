---
complexity: 10
footprint:
  - resources/invariants/a-master-need-is-the-union-of-its-members.sh
  - .pearde/memos/a-master-need-is-the-union-of-its-members.md
  - references/parts/ramp.md
  - references/files.md
---

# spec02 — a check that fails when the ramp measures the wrong tree, and the words that say so

The union in spec01 is invisible to every harness this repo runs: `index.py
check` and the one invariant would both stay green if `needs` went back to
measuring the master's own repo. This unit turns the probe's fixture into a
standing check, and writes the master case into the reference that describes
the ramp — which today says nothing about members and whose `have` row still
claims the ramp measures *this* repo.

## What already stands

`probe/fixture.sh` — ten assertions over three to six git repos built in a
`mktemp -d`, tearing down on exit. It depends on nothing but python3, git and
perl, so it is already shaped like an invariant script. It is in `probe/`,
which nothing runs.

## What is left

Promote the fixture to `resources/invariants/`, give it the memo an invariant
script is named for, and correct the reference.

`references/parts/ramp.md` needs the master case: `need` is the union over
`members:` to any depth, the master's own tree is one member of it, the floor
lands on the sum, and a row credits members. Its `have` row currently reads
"every skill this machine offers *this* repo" — true, and now inconsistent
with a `need` measured over five. Say plainly that `have` is still the one
machine and `gap` is a union `need` against a single machine's skills, so a
reader is not left to infer a symmetry that is not there.

`references/files.md` gains the row for the new script. **The file is being
edited by another PRD in this same tree** — add the row, do not reflow the
table.

## Acceptance

- [x] `resources/invariants/a-master-need-is-the-union-of-its-members.sh`
      exists, builds every fixture under a `mktemp -d` it removes on exit,
      writes nothing under `.pearde/`, and prints one `PASS`/`FAIL` line per
      assertion in the shape of the invariant already in that directory
- [x] it exits non-zero when `scan_roots` is reverted to returning only the
      board — proved by running it against the committed `ramp.py`, not by
      assertion
- [x] it covers, at minimum: a plain board unchanged, the union sum, the
      floor on the sum, the member credit in `why`, a master under a master,
      and a `members:` cycle that terminates
- [x] it bounds any command that could hang with `perl -e 'alarm N; exec
      @ARGV'` — this machine ships no `timeout(1)`
- [x] `.pearde/memos/a-master-need-is-the-union-of-its-members.md` is
      `kind: invariant`, carries a `verify:` naming the script, and passes
      `python3 resources/memos.py check`
- [x] `references/parts/ramp.md` describes the master case: union over
      `members:` to any depth, the master's own tree as one member, the floor
      on the sum, the member credit in a row
- [x] `references/parts/ramp.md`'s `have` row no longer reads as if `have`
      and `need` measure the same scope, and says what `gap` therefore is on
      a master
- [x] `references/files.md` holds one row for the new script and no other
      change
- [x] `index.py check` is captured and printed in full, and decides the
      exit only on lines whose subject is a path in this spec's
      `footprint:` — guarded on a non-zero exit and on a `Traceback`,
      and with a wiring proof that the footprint matcher matches the
      line shape `check` prints

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde

# Green on this tree: every line PASS, exit 0.
bash resources/invariants/a-master-need-is-the-union-of-its-members.sh

# And it can fail. The whole module is swapped for the committed, pre-union
# one — a behavioural mutation, not a renamed string.
D=$(mktemp -d /tmp/rampold.XXXXXX)
git archive HEAD | tar -x -C "$D"
RAMP="$D/resources/board/ramp.py" \
  bash resources/invariants/a-master-need-is-the-union-of-its-members.sh \
  >/dev/null 2>&1 && mrc=0 || mrc=$?
rm -rf "$D"
if [ "$mrc" = 0 ]; then echo "FAIL the invariant passed against the pre-union ramp.py"; exit 1; fi
echo "the invariant exits $mrc against the committed ramp.py"

# `memos.py check` reads every memo on the board, so a neighbour's malformed
# one would decide this unit's colour. Same treatment: captured, printed, and
# gated on the one memo this spec owns.
mout=$(python3 resources/memos.py check /Users/feb/dev/infra/pearde/.pearde 2>&1) && mcrc=0 || mcrc=$?
printf 'memos.py check exit %s:\n%s\n' "$mcrc" "${mout:-(silent)}"
if printf '%s\n' "$mout" | grep -q Traceback; then echo "FAIL memos.py check raised"; exit 1; fi
if printf '%s\n' "$mout" | grep -q 'a-master-need-is-the-union-of-its-members'; then
  echo "FAIL memos.py check names this spec's memo"; exit 1
fi
if [ ! -f /Users/feb/dev/infra/pearde/.pearde/memos/a-master-need-is-the-union-of-its-members.md ]; then
  echo "FAIL the memo is not on the board"; exit 1
fi
grep -q '^kind: invariant' /Users/feb/dev/infra/pearde/.pearde/memos/a-master-need-is-the-union-of-its-members.md
grep -q '^verify: bash resources/invariants/a-master-need-is-the-union-of-its-members.sh' \
  /Users/feb/dev/infra/pearde/.pearde/memos/a-master-need-is-the-union-of-its-members.md

# `index.py check` reads the whole checkout, so a neighbour's in-flight file
# reddens it and that is not this unit's colour to carry —
# @.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md.
# Its output is captured, printed in full, and decides the exit only on lines
# whose subject is a path in this spec's own `footprint:`.
FOOT='resources/invariants/a-master-need-is-the-union-of-its-members\.sh|references/parts/ramp\.md|references/files\.md|\.pearde/memos/a-master-need-is-the-union-of-its-members\.md'
out=$(python3 resources/index.py check 2>&1) && irc=0 || irc=$?
printf 'index.py check exit %s:\n%s\n' "$irc" "${out:-(silent)}"

# Two guards, because a checker that dies prints no line and would otherwise
# read as a clean tree. `check` exits 1 on problems and 1 on an uncaught
# exception alike, so the exit code alone cannot tell them apart.
if [ "$irc" -gt 1 ]; then echo "FAIL index.py check exited $irc"; exit 1; fi
if printf '%s\n' "$out" | grep -q Traceback; then echo "FAIL index.py check raised"; exit 1; fi

# And a third: the footprint matcher must match the shape `check` actually
# prints, or the gate below is a grep that can never fire.
wired=$(printf '%s\n' 'references/parts/ramp.md references @nope.py — not on disk' \
        | awk '{print $1}' | grep -Ex "$FOOT" || true)
if [ -z "$wired" ]; then echo "FAIL the footprint matcher misses index.py's own line shape"; exit 1; fi

mine=$(printf '%s\n' "$out" | awk 'NF{print $1}' | grep -Ex "$FOOT" || true)
if [ -n "$mine" ]; then printf 'FAIL index.py check names this footprint:\n%s\n' "$mine"; exit 1; fi
echo "index.py check names no path in this spec's footprint"
```
