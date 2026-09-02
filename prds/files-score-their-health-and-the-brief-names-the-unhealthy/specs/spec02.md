---
complexity: 4
footprint:
  - resources/board/brief.py
  - references/parts/workers.md
---

# spec02 — the implementer's brief names the unhealthy files in its footprint

The implementer block in `references/parts/workers.md` carries a `<health>`
placeholder that `brief.py` fills from `health list --under <floor>` over the
PRD's footprint union, worst first. A footprint with nothing under the floor
gets one line saying so; a board with no record gets one line saying that
instead. A bad file is named when a PRD touches it, so it is named rather
than discovered.

## What already stands

All of it, committed. `brief.py` `health_of(prd, board)` (line 246) shells
`health.py list --under` over `planlib.spec_data(prd)`'s footprint union and
returns its lines, or `no health record — pearde health score writes one`
when the board has none. It is wired into `brief_prd`'s placeholder dict at
line 383 as `"<health>": health_of(prd, board)`. The implementer block in
`references/parts/workers.md` ends on `> <health>` (line 352), and the
placeholder has its row in the same file's placeholder table (line 118)
naming the fallback wordings. `doctor`'s `briefs` row is green on it:
`briefs ok 5 blocks in references/parts/workers.md · every placeholder named
· the verdict line named`.

## What is left

Nothing in the code. The fixture path is what the probe exercises — there is
no live specced PRD on this board right now whose footprint holds an
unhealthy file, so J1-J3 are the check that can fail, and they do fail when
the code is broken (see the negative control in the report).

## Acceptance

- [x] A brief for a PRD whose footprint holds a file under the floor names
  that file, and does not name a healthy file in the same footprint.
  `  ok    J1 the brief names src/deep.py under the health floor` ·
  `  ok    J2 and not tiny.py, which is healthy`
- [x] With no health record on the board the brief says so rather than
  printing an empty block or failing.
  `  ok    J3 with no record the brief says so`
- [x] The `<health>` placeholder is declared in the placeholder table and
  present in the implementer block, and `brief.py --check` is clean.
  `references/parts/workers.md:118` `| `<health>` | `health.py list --under <health-floor>` …` ·
  `references/parts/workers.md:352` `> <health>` · `brief.py --check` exit 0, no output
- [x] `doctor`'s `briefs` row is green.
  `briefs      ok      5 blocks in references/parts/workers.md · every placeholder named · the verdict line named`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
N=0
bash .pearde/prds/files-score-their-health-and-the-brief-names-the-unhealthy/probe/verify.sh 2>&1 | grep -c '^  ok    J' | grep -qx 3 || N=$((N+1))
grep -q 'def health_of' resources/board/brief.py || N=$((N+1))
grep -q '"<health>": health_of' resources/board/brief.py || N=$((N+1))
grep -q '^> <health>$' references/parts/workers.md || N=$((N+1))
grep -q '^| `<health>` |' references/parts/workers.md || N=$((N+1))
python3 resources/board/brief.py --check || N=$((N+1))
out=$(bash resources/doctor.sh 2>&1 || true)
[ -n "$out" ] || N=$((N+1))
printf '%s\n' "$out" | grep -E '^  briefs +ok' || N=$((N+1))
echo "spec02 failures: $N"
[ "$N" = 0 ]
```
