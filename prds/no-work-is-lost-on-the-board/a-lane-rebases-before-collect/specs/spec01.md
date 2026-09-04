---
complexity: 8
footprint:
  - resources/board/lanes.py
  - resources/board/collect.py
---

# spec01 — collect names the footprint files that moved under the lane

`collect` already rebases the lane onto the checkout's branch before it runs
verify — a control run against `HEAD` proved that half of the contract green,
so nothing here changes it. What it did not do was say so: the worker wrote
its report before any of this landed and cannot know what moved, and the run
printed the merge without naming a file. This unit reads the cut point
**before** the merge, narrows it to the PRD's footprint, and says the same
sentence in both places the board keeps — the run's output and the PRD's
`## Report`.

The read has to happen before `lanes.merge`: that call rebases the lane onto
the checkout's HEAD, and from that moment the merge base **is** that HEAD and
the comparison has no answer left to give.

## What stands

- `lanes.cut_base(repo, slug)` — the merge base of the checkout's branch and
  `lane/<slug>`, `None` when there is no lane branch.
- `lanes.moved_since_cut(repo, slug)` — the files the checkout's branch changed
  since the cut, sorted, `[]` when there is no lane and when nothing landed.
- `collect.moved_onto(repo)` and `collect.moved_line(rel, onto, moved)` — the
  one sentence, so the run and the report say it in the same words.
- `land_lane` returns `(pre, n, moved)` and prints the line before merging;
  `moved` is narrowed to the footprint by `inside(p, feet)`.
- `collect_one` prefixes the posted report text with the same line.
- `post_report` skips a daemon board registered with no path. The `all` board
  is registered that way on this machine, and `os.path.abspath(None)` raised
  a `TypeError` that this function reported as "another shape" — so **every**
  report on the machine was silently dropped, this PRD's included.

## What is left

Nothing in these two files. The boxes below are the checks that the standing
code is what it claims; an implementer that finds one red fixes the code, not
the box.

## Acceptance

- [x] The probe is green end to end: `bash probe/run.sh` exits 0 with five
      `PASS` lines and no `FAIL`.
- [x] The line names only footprint files — the probe's fixture moves
      `resources/b.py` outside the footprint and the line does not mention it.
- [x] The line does not print when nothing moved — the probe's second run cuts
      the lane after main's last commit and the output is silent.
- [x] The text handed to `post_report` carries the same sentence as the run's
      output, byte for byte.
- [x] `moved_since_cut` is read before `lanes.merge` runs, not after: in
      `land_lane` the `moved = [...]` line stands above the `laneslib.merge`
      call.
- [x] `post_report` matches on `b.get("path")` before calling
      `os.path.abspath` on it, so a pathless board in `/status` is skipped
      rather than raising.

## Verify and Proof

```sh
bash .pearde/prds/no-work-is-lost-on-the-board/a-lane-rebases-before-collect/probe/run.sh
python3 -c "import ast,sys; s=open('resources/board/lanes.py').read(); [sys.exit('missing '+n) for n in ('cut_base','moved_since_cut') if 'def '+n+'(' not in s]"
python3 - <<'PY'
s = open("resources/board/collect.py").read()
body = s[s.index("def land_lane("):s.index("def unland(")]
assert body.index("moved_since_cut") < body.index("laneslib.merge"), \
    "moved_since_cut is read after the merge — the cut point is gone by then"
p = s[s.index("def post_report("):s.index("# ── the line")]
assert 'b.get("path")' in p, "post_report does not guard a pathless board"
print("ok")
PY
```
