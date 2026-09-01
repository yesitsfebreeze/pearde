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
# and the number the PRD sets is measured with the previous analyst's bench:
# the walk+parse that the cache covers, cold vs warm, on THIS board.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$DIR"
for _ in 1 2 3 4 5 6; do
  [ -f "$REPO/resources/board/plan.py" ] && break
  REPO="$(dirname "$REPO")"
done
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

# the number the PRD sets: the walk+parse the cache covers, cold vs warm,
# measured the way bench.py measures it — in-process, on THIS board
python3 - "$REPO" <<'PYEOF'
import sys, os, time, statistics
repo = sys.argv[1]
sys.path.insert(0, os.path.join(repo, "resources", "board"))
sys.path.insert(0, os.path.join(repo, "resources"))
import plan as planlib
board = os.path.join(repo, ".pearde")

def walk_parse():
    # what the cache covers: every prd.md + every spec frontmatter
    scan_root = planlib.prds_dir(board)
    n = 0
    for root, dirs, files in os.walk(scan_root):
        dirs[:] = [d for d in dirs if d not in ("specs",)]
        if "prd.md" in files and root != scan_root:
            planlib.parse_prd(os.path.join(root, "prd.md")); n += 1
        sdir = os.path.join(root, "specs")
        if os.path.isdir(sdir):
            for f in sorted(os.listdir(sdir)):
                if f.endswith(".md"):
                    planlib.parse_prd(os.path.join(sdir, f)); n += 1
    return n

def cold():
    planlib._PCACHE.clear(); planlib._PCACHE_LOADED = False
    planlib.parse_cache_load(board)
    t0 = time.perf_counter(); walk_parse(); return (time.perf_counter()-t0)*1000

def warm():
    planlib.parse_cache_load(board)
    t0 = time.perf_counter(); walk_parse(); return (time.perf_counter()-t0)*1000

planlib.scan(board)  # fill + persist
cold = statistics.median(cold() for _ in range(3))
warm = statistics.median(warm() for _ in range(5))
print(f"walk+parse cold {cold:.1f} ms -> warm {warm:.1f} ms ({os.environ.get('N','?')} files)")
if warm >= cold:
    print("FAIL: warm not faster than cold"); sys.exit(1)
if warm > 40:
    print(f"FAIL: warm walk+parse {warm:.1f} ms above the 40 ms bar"); sys.exit(1)
print("parse-cache verify: pass")
PYEOF
RC=$?
exit $RC
