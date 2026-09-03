---
complexity: 16
footprint:
  - resources/board/dispatch.py
---

# spec02 — the dispatcher checkpoints a live worker's lane on a timer

A dispatched worker is already detached from its launching window —
`dispatch.launch` spawns with `start_new_session=True`, and the probe replays
the window's Ctrl+C to show the attached child dying while the detached one
keeps writing. What is not covered is the worker's own lane while it runs:
eighteen workers verified alive and growing stopped to the second with their
lanes dirty. This unit puts the checkpoint on the dispatcher's poll loop —
every `PEARDE_CHECKPOINT_S` (default 120, 0 turns it off) it commits what
stands in each live worker's lane through `lanes.commit_all`, so a death
costs the verdict and not the build. A git that says no — the worker's own
git holding the index, most likely — is logged and skipped; the next
interval retries.

What already stands (built and probed in this pass, uncommitted in the
lane): `Job.checkpoint(log)` — no lane named by the job's `rel` is silent, a
`LaneError` logs `ckpt <addr> · skipped`; `Job.ckpt_t` seeded at launch; and
the reap loop calling `checkpoint` on every live job whose `ckpt_t` is more
than `CHECKPOINT_S` seconds old, resetting `ckpt_t` after each call.

## Acceptance

- [x] `Job.checkpoint` commits what stands in the live worker's lane to `lane/<slug>` and logs `ckpt <addr> · committed as <sha>`
- [x] a job whose PRD holds no lane checkpoints silently — no log line, no crash
- [x] the reap loop calls `checkpoint` on a live job only after `PEARDE_CHECKPOINT_S` seconds, and not before
- [x] a `LaneError` from the commit logs `ckpt <addr> · skipped` and the dispatcher keeps running
- [x] `PEARDE_CHECKPOINT_S=0` disables the timer entirely

## Verify and Proof

```sh
LANE="$(git rev-parse --show-toplevel)"
D="$(mktemp -d)"; mkdir -p "$D/w/.pearde"
cp -R "$LANE/resources/board/example/." "$D/w/.pearde/"
mkdir -p "$D/w/.pearde/.state" "$D/w/src"
printf 'base\n' > "$D/w/src/app.py"
printf '.pearde/.lanes/\n.pearde/.state/\n.pearde/prds/**/probe/\n' > "$D/w/.gitignore"
find "$D/w" -type f -exec touch {} +
git -C "$D/w" init -q -b main && git -C "$D/w" add -A && git -C "$D/w" commit -q -m fixture
python3 - "$D/w" "$LANE" <<'EOF'
import os, sys
d, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "building")
open(os.path.join(lane, "src", "app.py"), "w").write("the worker's line\n")
EOF
out="$(python3 - "$D/w" "$LANE" <<'EOF'
import os, subprocess, sys
d, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import dispatch
row = {"addr": "example/building", "board": "example", "rel": "building",
       "path": os.path.join(d, ".pearde"), "feet": ["src/app.py"]}
proc = subprocess.Popen(["sleep", "30"], start_new_session=True)
job = dispatch.Job(row, proc, os.path.join(d, ".pearde", ".state", "run-x.log"))
lines = []
job.checkpoint(lines.append)
proc.kill()
print(" | ".join(lines))
EOF
)"
echo "$out" | grep -q "committed as" || { echo "FAIL: no ckpt line"; exit 1; }
got="$(git -C "$D/w" show lane/building:src/app.py 2>/dev/null || echo lost)"
[ "$got" = "the worker's line" ] || { echo "FAIL: work not on branch"; exit 1; }
echo "dispatcher-checkpoint: ok"
```
