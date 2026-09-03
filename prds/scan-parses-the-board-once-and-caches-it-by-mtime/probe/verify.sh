#!/usr/bin/env bash
# Probe verify for scan-parses-the-board-once-and-caches-it-by-mtime.
# Fixture board in a runtime tempdir (never under .pearde/prds/). The REAL
# plan.py scan runs against it, and the cache's contract is checked:
#   1. the cache file exists after a scan, under the board's .state/
#   2. an external edit is seen on the next call (no stale answer)
#   3. a corrupt cache falls back to a full parse silently
#   4. a version-mismatched cache is discarded
#   5. a deleted PRD is not served from the cache
#   6. cold and warm scans print identical output on an unchanged board
#   7. a warm walk does no file read at all — the cache's contract counted as
#      work, not as milliseconds. Nothing in this file asserts on a clock.
set -u
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
REPO="$ROOT"
DIR="$HERE"
PLAN="$REPO/resources/board/plan.py"

TMP="$(mktemp -d /tmp/parsecache-verify.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
BOARD="$TMP/board/.pearde"
mkdir -p "$BOARD/prds"
printf -- '---\nname: fixture\nworkers: 2\n---\n' > "$BOARD/settings.md"

for i in $(seq 1 8); do
  D="$BOARD/prds/prd-$i"
  mkdir -p "$D/specs"
  printf -- '---\nstate: open\npriority: %s\n---\n\n# PRD %s\n\nbody\n' "$i" "$i" > "$D/prd.md"
  printf -- '---\ncomplexity: 3\nfootprint:\n  - src/a%s.ts\n---\n\n## Acceptance\n\n- [ ] box\n' "$i" > "$D/specs/spec01.md"
done

# 6. identical output cold vs warm
python3 "$PLAN" scan "$BOARD" > "$TMP/out-cold.txt" 2>&1
python3 "$PLAN" scan "$BOARD" > "$TMP/out-warm.txt" 2>&1
if ! diff -q "$TMP/out-cold.txt" "$TMP/out-warm.txt" >/dev/null; then
  echo "FAIL: warm scan output differs from cold"
  diff "$TMP/out-cold.txt" "$TMP/out-warm.txt" | head -5
  exit 1
fi

# 1. cache file exists, under the board's .state/
CACHE="$BOARD/.state/parse-cache.json"
if [ ! -f "$CACHE" ]; then
  echo "FAIL: no parse cache written at <board>/.state/parse-cache.json"; exit 1
fi

# 2. external edit is seen on the next call
printf -- '---\nstate: done\npriority: 1\n---\n\n# PRD 1 changed\n' > "$BOARD/prds/prd-1/prd.md"
sleep 0.01
if ! python3 "$PLAN" scan "$BOARD" 2>&1 | grep -q "done 1"; then
  echo "FAIL: external edit not seen by the next scan"; exit 1
fi

# 3. corrupt cache — silent fallback
printf '{not json' > "$CACHE"
if ! python3 "$PLAN" scan "$BOARD" > "$TMP/out-corrupt.txt" 2>&1; then
  echo "FAIL: corrupt cache made scan fail"; exit 1
fi
if ! grep -q "8 PRDs" "$TMP/out-corrupt.txt"; then
  echo "FAIL: corrupt cache broke the count"; exit 1
fi

# 4. version mismatch — discarded
python3 -c "import json;json.dump({'version':999,'files':{}},open('$CACHE','w'))"
if ! python3 "$PLAN" scan "$BOARD" 2>&1 | grep -q "8 PRDs"; then
  echo "FAIL: version-mismatched cache broke scan"; exit 1
fi

# 5. deleted PRD is not served from the cache
rm -rf "$BOARD/prds/prd-8"
if ! python3 "$PLAN" scan "$BOARD" 2>&1 | grep -q "7 PRDs"; then
  echo "FAIL: deleted PRD still served from the cache"; exit 1
fi

# The cache's contract, measured as WORK rather than as elapsed time.
#
# What this used to assert was `warm < cold` and `warm < 40 ms` on a
# wall-clock stopwatch. Both are readings of the machine: measured on
# 2026-09-02, six runs of this file under 64 spinners went red twice, on an
# unchanged tree, with the cache doing its job in every one of them (cold
# 162 ms -> warm 54 ms is a working cache and a busy box). The board runs
# this harness four at a time inside a sweep, so the load is not
# hypothetical. A clock also cannot be trusted here for a second reason: a
# sandboxed shell on this machine reads about 6.7 hours behind the host.
#
# What the cache actually promises is not a number of milliseconds — it is
# that a warm parse does no file read at all. That is what is counted below,
# on the fixture board, by wrapping `open`. It is an integer, it is the same
# integer on an idle box and a hammered one, and it goes red exactly when
# the cache stops caching.
python3 - "$REPO" "$BOARD" <<'PYEOF'
import sys, os, builtins
repo, board = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(repo, "resources", "board"))
sys.path.insert(0, os.path.join(repo, "resources"))
import plan as planlib

scan_root = planlib.prds_dir(board)
opens = []
_real = builtins.open


def counting(f, *a, **k):
    p = f if isinstance(f, str) else ""
    if p.startswith(scan_root) and p.endswith(".md"):
        opens.append(p)
    return _real(f, *a, **k)


def walk(parse):
    n = 0
    for root, dirs, files in os.walk(scan_root):
        dirs[:] = [d for d in dirs if d != "specs"]
        if "prd.md" in files and root != scan_root:
            parse(os.path.join(root, "prd.md")); n += 1
        sdir = os.path.join(root, "specs")
        if os.path.isdir(sdir):
            for f in sorted(os.listdir(sdir)):
                if f.endswith(".md"):
                    parse(os.path.join(sdir, f)); n += 1
    return n


builtins.open = counting
try:
    # the cache's three globals are rebound at run time, so they live in the
    # module that owns them and cannot be re-exported: an assignment on plan
    # would set an attribute nothing reads. Poke them through prdfile.
    planlib.prdfile._PCACHE.clear(); planlib.prdfile._PCACHE_LOADED = True
    del opens[:]; n = walk(planlib.parse_prd); cold = len(opens)
    del opens[:]; walk(planlib.parse_prd); warm = len(opens)
    # one file's mtime moves: exactly that file is re-read, nothing else
    victim = os.path.join(scan_root, "prd-1", "prd.md")
    st = os.stat(victim)
    os.utime(victim, ns=(st.st_atime_ns + 10**9, st.st_mtime_ns + 10**9))
    del opens[:]; walk(planlib.parse_prd); touched = len(opens)
    # the flip, on the same files in the same process: with the cache out of
    # the path every walk is a full re-read. A check that cannot go red on
    # this input is not measuring the cache.
    del opens[:]; walk(planlib._parse_prd_uncached); nocache = len(opens)
finally:
    builtins.open = _real

fail = 0


def check(name, got, want):
    global fail
    if got == want:
        print(f"ok   {name} ({got})")
    else:
        print(f"FAIL: {name} — got {got}, want {want}"); fail += 1


check("files walked", n > 0, True)
check("a cold walk reads every file once", cold, n)
check("a warm walk reads nothing", warm, 0)
check("one changed mtime costs exactly one re-read", touched, 1)
check("the check can fail: without the cache the walk reads every file",
      nocache, n)
print(f"parse-cache verify: {'pass' if not fail else 'FAILED'}")
sys.exit(1 if fail else 0)
PYEOF
exit $?
