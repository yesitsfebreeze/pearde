---
complexity: 15
footprint:
  - resources/health.py
  - references/health.md
  - references/parts/health.md
  - references/parts/workers.md
  - references/templates/grammar.md
  - references/skills/pearde-health.md
---

# spec01 — the `<health>` line names the note, not just the file, and the rule it follows is written once

`health.py list` (the command `pearde brief` runs to fill `<health>` in the
implementer's block) names, per unhealthy file: its score, its worst axis,
and now its note's path — the anchor a pointer needs to actually point
somewhere. A file scoring under the floor whose note is missing from disk is
named as missing its note (`no note at <path> — pearde health score writes
one`), never named with a bare score and no anchor. The reference prose that
states "a score is a pointer, never a verdict" is trimmed from two of its
three homes (`references/templates/grammar.md`, `references/skills/pearde-
health.md`) down to a citation of `references/health.md`, which keeps the
one full statement, and gains one explicit sentence next to it and beside
the `<health>` placeholder row in `references/parts/workers.md`: the score
never reorders the plan — `plan.py` reads no health key, verified below by a
byte-diff.

Already built and proven in
`.pearde/prds/enforce-pointer-not-verdict/probe/check_pointer_not_verdict.sh`
against a throwaway board+repo built at run time (not this PRD's own
directory):

- `health.py list` on a file scored under the floor prints one line
  carrying the score, the worst axis (`branching, longest`) and the note's
  path (`.pearde/health/files/small.py.md`).
- The same file with its note deleted from disk prints `no note at
  <path> — pearde health score writes one` in place of a bare score —
  still named, never silently dropped, never named without its anchor.
- `plan.py scan` over a two-PRD board is byte-identical under `health-floor:
  1` and `health-floor: 100` — the file this PRD's own frontmatter check
  demands.

Nothing in `resources/board/`, `resources/pearde.py` or `resources/
doctor.sh` reads the shape of a `health.py list` line beyond passing it
through whole (`health_of` in `resources/board/brief.py` joins the raw
lines; `doctor.sh`'s `health` row reads `ranking.md`'s frontmatter counts,
never `list`'s stdout) — the new column is additive and needed no other
caller to change.

## What was found, not fixed here

`docs/content/docs/health/index.mdx` and two sibling pages under `docs/`
carry the same "worst first on one page — so a monolith is named before a
worker meets it" phrasing and a fourth restatement of the pointer-not-
verdict rule. `docs/` holds zero files tracked by git (`git ls-files docs/`
is empty) — it is outside the manifest, outside every doctor row and outside
the footprint this PRD's contract names paths under. Left alone; named here
per the contract's own words ("A wrong claim you find elsewhere ... goes in
your report as a finding — not into a spec").

## Acceptance

- [x] `health.py list --board <board>` on a board holding one file scored
  under the floor, with its note present, prints a line matching `^\s*\d+
  \s+\S+\s+.+\s+\.pearde/health/files/.+\.md$` — score, file, worst axis,
  note path, in that order.
- [x] The same file with `.pearde/health/files/<slug>.md` deleted: `health.py
  list` still names the file, now with `no note at ` immediately before the
  note's path, and `pearde health score writes one` after it — never a line
  with the score and file alone.
- [x] `plan.py scan --board <board>` on a two-PRD board is byte-identical
  (`diff` exits 0) between a run under `health-floor: 1` in `settings.md` and
  a run under `health-floor: 100`.
- [x] `python3 resources/board/brief.py`'s own `read_blocks()` returns no
  `bad` entries after the edit to `references/parts/workers.md` — the
  `<health>` row's added sentence does not break the brief's own block
  parser.
- [x] `grep -c "pointer, never a verdict" references/health.md
  references/templates/grammar.md references/skills/pearde-health.md`
  shows the full phrase in `references/health.md` only; the other two name
  it by pointing at that file, not by repeating it.
- [x] `python3 resources/index.py check` and `python3 resources/health.py
  check` name no new line beyond what stood before this PRD's edit: `index.py
  check` prints the same two pre-existing lines (`resources/common.py` with
  no manifest row, `hotreload-test.js` not on disk) with and without this
  diff — inherited, not this PRD's — and `health.py check` prints only a
  pre-existing `stale:` note, exit 0, both before and after.

## Verify and Proof

The probe takes its tree the way the board's harnesses do — `PEARDE_ROOT`
when the runner set one, the checkout the board sits in otherwise. Before
this spec's edit lands in the checkout, run the block with
`PEARDE_ROOT=<lane>`; from the checkout without it the probe must fail on
the note path it cannot name — that failure is the flip this unit owns.

```sh
ROOT="${PEARDE_ROOT:-$(pwd)}"   # the lane holding the build when the runner names one, the checkout otherwise
bash .pearde/prds/enforce-pointer-not-verdict/probe/check_pointer_not_verdict.sh

python3 - <<'PY'
import os, sys
root = os.environ.get("PEARDE_ROOT") or os.getcwd()
sys.path.insert(0, os.path.join(root, "resources"))
sys.path.insert(0, os.path.join(root, "resources", "board"))
import brief as b
_, bad = b.read_blocks()
assert bad == [], bad
print("workers.md sound")
PY

for f in "$ROOT/references/health.md" "$ROOT/references/templates/grammar.md" "$ROOT/references/skills/pearde-health.md"; do
  n=$(grep -c "pointer, never a verdict" "$f" || true)
  if [ "$f" = "$ROOT/references/health.md" ] && [ "$n" -lt 1 ]; then
    echo "FAIL: the rule is gone from its one home"; exit 1
  fi
  if [ "$f" != "$ROOT/references/health.md" ] && [ "$n" -gt 0 ]; then
    echo "FAIL: $f restates the rule instead of citing references/health.md"; exit 1
  fi
done
echo "pointer rule stated once, in references/health.md"

out=$(python3 "$ROOT/resources/index.py" check 2>&1) && rc=0 || rc=$?
if [ "$rc" -ge 2 ]; then echo "FAIL: index.py check crashed (rc=$rc)"; exit 1; fi
if printf '%s\n' "$out" | grep -Eq 'resources/health\.py|references/(health\.md|parts/health\.md|parts/workers\.md|templates/grammar\.md|skills/pearde-health\.md)'; then
  echo "FAIL: the map names a file of this footprint:"
  printf '%s\n' "$out" | grep -E 'resources/health\.py|references/'
  exit 1
fi
printf '%s\n' "$out"

out=$(python3 "$ROOT/resources/health.py" check .pearde 2>&1) && rc=0 || rc=$?
if [ "$rc" -ge 2 ]; then echo "FAIL: health.py check could not read a board (rc=$rc)"; exit 1; fi
if printf '%s\n' "$out" | grep -Eq 'health/files/(references-|resources-health\.py)'; then
  echo "FAIL: the health record names a file of this footprint:"
  printf '%s\n' "$out" | grep -E 'health/files/'
  exit 1
fi
printf '%s\n' "$out"
```
