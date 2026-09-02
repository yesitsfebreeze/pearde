#!/usr/bin/env bash
# one-copy-per-machine-of-what-every-lane-regenerates — the verify command of
# the memo `lanes-share-one-copy-of-what-they-regenerate`. Run from the repo
# root:
#
#     sh resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant, in four claims:
#
#   1  every worktree the survey covers answers ONE store path — that is the
#      whole reason `<git-common-dir>/pearde-shared/` is the store, and a
#      tree pointing somewhere else is a second copy by another name;
#   2  no shared path is a real copy in two trees at once — one real copy is
#      seeding, two is the duplication this exists to remove;
#   3  no linked path is visible to `git status` in the tree that holds it —
#      a link git shows is worse than the bytes it saves, because it is a
#      modification on every status and a deletion on the next checkout;
#   4  one store path per shared object — a second spelling of one directory
#      must not grow a second copy of it in the store, which is the same
#      duplication moved from the lanes into the store.
#
# The survey is `pearde share --json`, which reports every tree, path and
# state and writes nothing. `SHARE_JSON` points the run at another survey
# instead — a file — which is how a claim here is proved able to fail:
#
#     D=$(mktemp -d); mkdir -p "$D/a/x" "$D/b/x"          # two real copies
#     printf '{"store":"%s","rows":[
#       {"tree":"a","path":"%s/a","rel":"x","state":"local"},
#       {"tree":"b","path":"%s/b","rel":"x","state":"local"}]}' "$D" "$D" "$D" \
#       > "$D/s.json"
#     SHARE_JSON="$D/s.json" sh resources/invariants/<this>.sh
#
# Claim 1 stands down for a tree that is not a git worktree, so a fixture
# proves claims 2 and 3 without having to be a repo; a fixture that IS one
# proves claim 3 as well.
#
# `SHARE` points claim 4 at another copy of the module, the way the master
# invariant points at another `ramp.py`. Both defaults are read from this
# script's own location, so it runs from anywhere.
set -u
ROOT=$(cd "$(dirname "$0")/../.." && pwd -P)
SHARE=${SHARE:-$ROOT/resources/board/shared.py}
SHARE_JSON=${SHARE_JSON:-}

if [ -n "$SHARE_JSON" ]; then
  if [ ! -f "$SHARE_JSON" ]; then
    printf 'FAIL  no survey at %s\n' "$SHARE_JSON"
    exit 1
  fi
  SURVEY=$SHARE_JSON
else
  SURVEY=$(mktemp -t pearde-share-survey) || exit 1
  trap 'rm -f "$SURVEY"' EXIT INT TERM
  if ! (cd "$ROOT" && python3 resources/pearde.py share --json) > "$SURVEY" \
        2>/dev/null; then
    printf 'FAIL  `pearde share --json` did not run from %s\n' "$ROOT"
    exit 1
  fi
fi

if [ ! -s "$SURVEY" ]; then
  printf 'FAIL  the survey is empty — nothing to check\n'
  exit 1
fi

SURVEY=$SURVEY SHARE=$SHARE python3 - <<'PY'
import json
import os
import subprocess
import sys

survey = os.environ["SURVEY"]
share = os.environ["SHARE"]
fails = 0


def no(msg):
    global fails
    fails += 1
    print(f"FAIL  {msg}")


def ok(msg):
    print(f"PASS  {msg}")


try:
    doc = json.load(open(survey))
    store = os.path.realpath(doc["store"])
    rows = doc["rows"]
except (OSError, ValueError, KeyError) as e:
    print(f"FAIL  the survey does not parse: {e}")
    sys.exit(1)

if not rows:
    print("FAIL  the survey covers no tree at all")
    sys.exit(1)

trees = sorted({r["path"] for r in rows})

# 1 — one store for every tree.
elsewhere = []
for t in trees:
    r = subprocess.run(["git", "-C", t, "rev-parse", "--git-common-dir"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        continue                       # not a worktree — claim 1 says nothing
    d = r.stdout.strip()
    if not os.path.isabs(d):
        d = os.path.join(t, d)
    mine = os.path.join(os.path.realpath(d), "pearde-shared")
    if mine != store:
        elsewhere.append((t, mine))
for t, mine in elsewhere:
    no(f"{t} points at {mine}, not at {store}")
if not elsewhere:
    ok(f"{len(trees)} tree(s) point at one store: {store}")

# 2 — no shared path is a real copy in two trees at once.
real = {}
for r in rows:
    p = os.path.join(r["path"], r["rel"])
    if os.path.lexists(p) and not os.path.islink(p):
        real.setdefault(r["rel"], []).append(r["path"])
doubled = {rel: ts for rel, ts in real.items() if len(ts) > 1}
for rel, ts in sorted(doubled.items()):
    no(f"{rel} is a real copy in {len(ts)} trees at once: "
       + ", ".join(sorted(ts)))
if not doubled:
    ok(f"{len(real)} path(s) hold a real copy, none in two trees at once")

# 3 — no linked path is visible to git.
seen, shown, links = set(), [], 0
for r in rows:
    pair = (r["path"], r["rel"])
    if pair in seen:
        continue
    seen.add(pair)
    p = os.path.join(r["path"], r["rel"])
    if not os.path.islink(p):
        continue
    links += 1
    g = subprocess.run(
        ["git", "-C", r["path"], "status", "--porcelain", "--", r["rel"]],
        capture_output=True, text=True)
    if g.returncode == 0 and g.stdout.strip():
        shown.append((r["path"], r["rel"], g.stdout.strip().splitlines()[0]))
for t, rel, line in shown:
    no(f"{t}: git shows the link at {rel} — `{line}`")
if not shown:
    ok(f"{links} link(s), none of them visible to git status")

# 4 — one store path per shared object.
sys.path.insert(0, os.path.dirname(os.path.abspath(share)))
try:
    import shared as sharedlib
except Exception as e:                                    # noqa: BLE001
    no(f"{share} does not import: {e}")
    sharedlib = None
if sharedlib is not None:
    twice = [old for old, new in sharedlib.RETIRED
             if os.path.isdir(os.path.join(store, old))
             and not os.path.islink(os.path.join(store, old))]
    for old in twice:
        new = dict(sharedlib.RETIRED)[old]
        no(f"the store holds {old} beside {new} — one object, two copies")
    keys = {s.key for s in sharedlib.SHARED}
    if not twice:
        ok(f"{len(sharedlib.SHARED)} shared row(s) reach {len(keys)} "
           "store path(s), none of them retired")

print(f"{fails} claim(s) failed")
sys.exit(1 if fails else 0)
PY
