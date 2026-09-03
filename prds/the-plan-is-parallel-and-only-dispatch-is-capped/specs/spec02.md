---
complexity: 10
footprint:
  - resources/board/plan.py
---

# spec02 — `pearde plan` prints the band, not a number, and stops hiding a clashing row

`cmd_plan` is the one reader of `spec01`'s new fields. It now shows both
walls always, shows a clashing PRD in `ready now` beside its non-clashing
peers with a note naming what it shares and with whom, and only shows a
third, staffed-simulation number when the caller explicitly asked for a cap.

**What stands** — the `gated` list (`then, as gates clear`) no longer
includes a PRD for `after[x]` alone; a PRD with an unmet footprint clash and
nothing else is in `ready now`. The `share(x)` helper builds `shares <path>
with <prd>` from `overlap_paths` (spec01) and is called on both the
`ready now` and the `gated` rows — a gated PRD held for a real reason still
says if it also clashes. The band print is unconditional:
`≈ <wall_floor> on the critical path — the dependency floor, needs: alone ·
≈ <wall_ceiling> if every footprint clash serialises — the ceiling`. Below
it, `peak <N> at once, unlimited agents` on a bare call, or — when `workers`
(the raw argument `cmd_plan` was handed, not the board's resolved default)
is not `None` — `≈ <wall> @ <workers> workers — the staffed simulation
asked for, not the plan · peak <N> at once`, using `r["wall"]`/`r["peak"]`,
which under an explicit cap are the capped simulation's own numbers, never
mistaken for the floor.

**What is left** — `resources/board/mapfile.py`'s `after=` comment and
`references/parts/view.md`'s Gantt prose are corrected in `spec03`, not
here, because neither is `plan.py`. The rendered HTML view's own header
tile (`resources/board/view.js`, "at N workers: <cal>") still phrases the
peak-agents tile as if the board's `workers:` setting shapes the drawn
calendar — it does not any more, since the view always calls
`compute_plan(board, None)`. Teaching that tile the same floor/ceiling band
`cmd_plan`'s text now prints is a real follow-on, sized enough (payload,
JS, and probably a second tile) to be its own unit — reported in the PRD's
report as a finding, not started here.

## Acceptance

- [x] a PRD held only by a footprint clash appears in `ready now`, with a
      `shares <path> with <prd>` note on its row, and does not also appear
      in `then, as gates clear`
- [x] a PRD gated for a real reason (`needs:` unmet, or a claim gate) that
      ALSO clashes shows both its real reason and the clash note
- [x] `pearde plan` with no `--workers` flag prints exactly two wall numbers,
      labelled floor and ceiling, and no `wall @ N workers` line
- [x] `pearde plan --workers N` prints the floor and ceiling AND a third
      line naming the staffed simulation's own wall and peak at `N`
- [x] neither wall line is ever labelled with the other's name

## Verify and Proof

```sh
cd resources/board
python3 - <<'PY'
import subprocess, sys, os, tempfile

def board(td):
    b = os.path.join(td, "board")
    for n in ("a", "b"):
        os.makedirs(os.path.join(b, "prds", n))
    open(os.path.join(b, "settings.md"), "w").write("---\n---\n")
    for n, p in (("a", 50), ("b", 40)):
        open(os.path.join(b, "prds", n, "prd.md"), "w").write(f"""---
state: open
origin: requested
priority: {p}
complexity: 10
blast-radius: low
footprint:
  - shared/file.md
---

# {n}
""")
    return b

ok = True
with tempfile.TemporaryDirectory() as td:
    b = board(td)
    bare = subprocess.run([sys.executable, "plan.py", "plan", b],
                          capture_output=True, text=True).stdout
    capped = subprocess.run([sys.executable, "plan.py", "plan", b,
                             "--workers", "1"],
                            capture_output=True, text=True).stdout
    checks = [
        ("shares note on a's or b's row (bare)",
         "shares shared/file.md with" in bare),
        ("no `then, as gates clear` section (bare, nothing else gates)",
         "then, as gates clear" not in bare),
        ("bare prints floor and ceiling, not `wall @ N workers`",
         "the dependency floor" in bare and "the ceiling" in bare
         and "wall @" not in bare),
        ("capped run ALSO prints floor/ceiling",
         "the dependency floor" in capped and "the ceiling" in capped),
        ("capped run additionally names the staffed simulation",
         "the staffed simulation asked for" in capped),
    ]
    for name, cond in checks:
        print(("PASS" if cond else "FAIL") + f": {name}")
        ok = ok and cond
sys.exit(0 if ok else 1)
PY
```
