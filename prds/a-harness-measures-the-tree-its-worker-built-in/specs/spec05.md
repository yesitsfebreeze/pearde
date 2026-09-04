---
complexity: 6
footprint:
  - .pearde/prds/a-harness-measures-the-tree-its-worker-built-in/probe/verify.sh
---

# spec05 — the PRD's own harness, and the two sweeps that close it

The three preceding specs each prove themselves file by file. This one is the
PRD's own acceptance, in one file that the sweep will then run forever after:
that a harness takes its root from its runner, that `E14` is decided by its own
fixture, and that the set answers the same way run four-at-a-time and run one
at a time.

The harness is `probe/verify.sh`, built out of the three probes pass one
leaves in the tree — `root-probe.sh`, `rootwalk-probe.sh` and `e14-probe.sh` —
which stay beside it as the working they came from. It pins its own total, as
this board requires, and ends on a check that carries its exit code.

The two sweeps are the last box and the expensive one. Run the set once at the
default cap and once with `PEARDE_HCAP=1`, and compare the failure sets, not
the totals: a harness that is red for a reason of its own is red both times and
proves nothing either way, while one that is red only in company is what this
PRD exists to remove. The comparison is a `diff` of two sorted lists of harness
paths, and the box is that the diff is empty.

**Compute cost.** Each sweep runs all sixty harnesses. Measured this session on
this machine: 88-98s at `HCAP=4`, 307s at `HCAP=1` — about seven minutes of
wall clock for the pair, and roughly 270% CPU for the first. It is the most
expensive box on this PRD by an order of magnitude and it cannot be scoped down
without ceasing to measure the thing. Run it once, at the end, after specs
01-04 are all in.

**Already standing (this analyst's uncommitted pass one):** both sweeps were
run twice — once as a baseline before any edit, and once through the
`doctor.sh` of spec03 with two harnesses already re-rooted. All four runs
failed the same 16 harnesses, name for name, `diff`-clean. So the serial and
parallel answers already agree on this tree, and the box is a re-measurement
after the other four specs land rather than a hunt for a difference. No
`verify.sh` is written yet.

## Acceptance

- [x] `probe/verify.sh` exists, pins its own check total, and ends on a check carrying its exit code.
- [x] It asserts every harness named in the `footprint:` of `spec01`, `spec02` and `spec04` reads `${PEARDE_ROOT:-`, walks up to its own board, counts no `..` and holds no absolute root — 59 files, the population this PRD converted. It **prints** the board-wide census beside that, naming every harness on the board that lacks the preamble, and the census decides nothing.
- [x] It asserts no harness reaches the repo by counting `..`, and none holds an absolute `/Users/` path.
- [x] It asserts the walk resolves the board and its repo from every harness directory on the board, and that `PEARDE_ROOT` overrides the root while leaving the board alone.
- [x] It asserts a defect planted only in a lane is seen when the runner names that lane and not otherwise — the `root-probe.sh` experiment, self-cleaning.
- [x] It asserts `E14`'s glob names one directory and that directory is the fixture's own.
- [x] The set run at `HCAP=4` and at `HCAP=1` fails the same harnesses: `diff` of the two sorted failure lists is empty.
- [ ] `doctor.sh --harnesses` reports this harness among the green ones, and its own census line names this harness among the harnesses on the board.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
P=.pearde/prds/a-harness-measures-the-tree-its-worker-built-in/probe/verify.sh
hout=$(bash "$P" </dev/null) && hrc=0 || hrc=$?
printf '%s\n' "$hout"
[ "$hrc" = 0 ]
# the two sweeps — about seven minutes; run last. `doctor` exits non-zero on
# any red harness on the board, so its exit is captured, never the block's:
# what this box asserts is that the two failure sets are the same, not that
# the board is green.
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT
bash resources/doctor.sh --harnesses . > "$D/par.txt" 2>&1 || true
PEARDE_HCAP=1 bash resources/doctor.sh --harnesses . > "$D/ser.txt" 2>&1 || true
for f in par ser; do
  { grep 'exit ' "$D/$f.txt" || true; } | { grep '.pearde/prds' || true; } \
    | sed 's/ — exit.*//;s/^ *//' | sort > "$D/$f-fails.txt"
done
grep '  harnesses ' "$D/par.txt"
echo "failing at HCAP=4: $(wc -l < "$D/par-fails.txt") · at HCAP=1: $(wc -l < "$D/ser-fails.txt")"
diff "$D/par-fails.txt" "$D/ser-fails.txt" && echo "same harnesses both ways"
# Box 8, read off the sweep that already ran rather than paid for again. The
# sweep is board-wide, so only the lines naming this spec's own footprint path
# are allowed to decide anything: this harness must be in the census doctor
# swept and absent from the harnesses it names as failing — which is what
# `doctor` means by green — and its own census line must name it.
if grep -qF "$P" "$D/par-fails.txt"; then
  echo "this harness is among the sweep's failing ones"; grep -F "$P" "$D/par.txt"; exit 1
fi
echo "green in the sweep at HCAP=4: $P"
printf '%s\n' "$hout" | grep -E 'A5 this harness is itself one of|census \(printed'
```
