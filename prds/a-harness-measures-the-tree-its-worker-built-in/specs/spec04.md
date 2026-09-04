---
complexity: 3
footprint:
  - .pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh
---

# spec04 — E14 is decided by the fixture, not by what else is running

`nothing-left-open/the-line-tells-the-truth` asserts, as its E14:

    ls -d /tmp/pearde-index-* "${TMPDIR:-/tmp}"/pearde-index-* | wc -l  ==  0

The glob is machine-wide and the check reads nothing about the tree under test.
`collect.private_index` makes its scratch with
`tempfile.mkdtemp(prefix="pearde-index-")`, so any concurrent `collect` — a
sibling harness in the same sweep, another session, the person's own — decides
it for the duration of its window.

The fix is to give the fixture its own temporary directory and look only there.
`tempfile.gettempdir()` reads `TMPDIR` before falling back to `/tmp`, so
exporting `TMPDIR` under the fixture's own scratch puts every scratch index
this run makes in one place nothing else writes to, and E14 globs that place.

This file also takes spec01's preamble — it is one of the fifty-nine and is
listed in neither spec01's nor spec02's footprint precisely so that this spec
owns it whole. It belongs with spec02's group: it spells `"$ROOT/.pearde"`.

**Already standing (this analyst's uncommitted pass one):** `export
TMPDIR="$SCRATCH/tmp"` is in place beside the existing `TOP`/`SCRATCH`
`mktemp -d` pair, E14 globs `"$TMPDIR"/pearde-index-*` alone, and E14 reads
`ok` with a `/tmp/pearde-index-*` directory deliberately held by a sibling.
The preamble is not in this file yet. `probe/e14-probe.sh` holds the mechanism:
a real `private_index` held open reddens the old spelling and leaves the scoped
one green, at the same instant, on the same tree.

Note for whoever runs this: the rest of this harness is red on the
orchestrator's checkout at the time of writing — 36 of 85 checks, from `A10`
down through the `B`, `C`, `E` and `G` sections, all about `PEARDE_AS` and
`--force`. It was green in the sweeps of this session and went red partway
through them, so it is a sibling's regression landing in the shared checkout,
not this edit's. Do not chase it here.

## Acceptance

- [x] The harness exports a `TMPDIR` under its own scratch, created before the first fixture is built, and removed by the existing `EXIT` trap.
- [x] E14 globs that directory alone: no `/tmp/pearde-index-*` term and no `${TMPDIR:-/tmp}` fallback survives on the E14 line.
- [x] With a `/tmp/pearde-index-<anything>` directory held by something else, E14 reads `ok`.
- [x] With a scratch index actually left behind inside the fixture's own `TMPDIR`, E14 reads `FAIL` — the check can still fail.
- [x] The file carries spec01's preamble, and names the board through `$BOARD` rather than `$ROOT/.pearde`.
- [x] The harness's own pinned total is unchanged: it still runs 85 checks.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
N=0
H=.pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh
grep -n 'export TMPDIR' "$H"
grep -qF 'basename "$BOARD"' "$H" || { echo "no preamble"; N=$((N+1)); }
if grep -nE '\$\{?(ROOT|REPO|CODE|R|PWD)\}?/\.pearde' "$H"; then
  echo "still derives the board from its root"; N=$((N+1))
fi
# the E14 assertion itself — the line that names E14 and globs a scratch index
e14=$(grep 'E14' "$H" | grep 'pearde-index-' | grep -v '^[[:space:]]*#') || true
printf '%s\n' "$e14"
printf '%s\n' "$e14" | grep -qF '"$TMPDIR"/pearde-index-*' || { echo "E14 does not glob the fixture's TMPDIR"; N=$((N+1)); }
if printf '%s\n' "$e14" | grep -qE '/tmp/pearde-index-|TMPDIR:-/tmp'; then
  echo "a machine-wide term survives on the E14 line"; N=$((N+1))
fi
# the mechanism, live: a real private_index held open reddens the old spelling
# and leaves the scoped one green, at the same instant on the same tree
bash .pearde/prds/a-harness-measures-the-tree-its-worker-built-in/probe/e14-probe.sh
# and the harness itself, while a sibling holds a machine-wide scratch index:
# E14 reads ok, and the pinned total is still 85.
mkdir -p /tmp/pearde-index-sibling-probe
out=$(bash "$H" </dev/null 2>&1) || true
rmdir /tmp/pearde-index-sibling-probe
[ -n "$out" ]
printf '%s\n' "$out" | grep -E '^[[:space:]]+(ok|FAIL)[[:space:]]+E14' || true
printf '%s\n' "$out" | grep -qE '^[[:space:]]+ok[[:space:]]+E14' || { echo "E14 is not ok while a sibling holds one"; N=$((N+1)); }
printf '%s\n' "$out" | tail -1
printf '%s\n' "$out" | grep -q '85 checks' || { echo "the pinned total moved off 85"; N=$((N+1)); }
echo "spec04: $N offending"
[ "$N" = 0 ]
```
