#!/usr/bin/env bash
# Builds a throwaway board under mktemp (never under prds/) and exercises
# every case the PRD's acceptance sketch and constraints name: a self-claim
# accepted with no --force and no `· forced`, a different worker still
# refused `held`, a self-claim still refused by a second gate (needs,
# footprint, workflow), an out-of-range state still refused regardless of
# worker, and the PRD's own state/claim untouched by every run (brief
# writes nothing). Run from the CODE repo root:
#   bash .pearde/prds/brief-does-not-refuse-the-claim-it-was-just-handed/probe/verify.sh
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
cd "$REPO" || exit 1
BOARD="$(mktemp -d)"
fail=0
note() { echo "  - $1"; }
check() { # check <label> <expected-exit> <actual-exit>
  if [ "$3" -eq "$2" ]; then note "ok   $1 (exit $3)"; else
    note "FAIL $1 (wanted exit $2, got $3)"; fail=1; fi
}

mkdir -p "$BOARD/.pearde/prds"
cat > "$BOARD/.pearde/settings.md" <<'EOF'
---
name: probe
language: English
workers: 6
pipeline: 8
weight-default: 20
gantt-day: 8h
context-budget: off
---
EOF

mk_prd() { # mk_prd <dir> <content-after-frontmatter-open>
  mkdir -p "$BOARD/.pearde/prds/$1"
  cat > "$BOARD/.pearde/prds/$1/prd.md"
}

mk_prd leaf1 <<'EOF'
---
state: analyzing
origin: derived
priority: 50
complexity:
blast-radius:
repo:
time:
  est:
  actual:
claim: w1 2026-08-31 18:00
---
# leaf1 — plain self-claim, no other gate
EOF

mk_prd leaf2spec <<'EOF'
---
state: claimed
origin: derived
priority: 50
complexity: 5
blast-radius: low
repo:
time:
  est:
  actual:
claim: w1 2026-08-31 18:00
---
# leaf2spec — specced/claimed, implementer role expected
EOF
mkdir -p "$BOARD/.pearde/prds/leaf2spec/specs"
cat > "$BOARD/.pearde/prds/leaf2spec/specs/spec01.md" <<'EOF'
---
complexity: 5
footprint:
  - foo.py
---
# spec01 — placeholder
## Acceptance
- [ ] it works
## Verify and Proof
```sh
echo ok
```
EOF

mk_prd needsdep <<'EOF'
---
state: open
origin: derived
priority: 50
complexity:
blast-radius:
repo:
time:
  est:
  actual:
---
# needsdep — not done, blocks needsleaf
EOF

mk_prd needsleaf <<'EOF'
---
state: analyzing
origin: derived
priority: 50
complexity:
blast-radius:
repo:
needs:
  - needsdep
time:
  est:
  actual:
claim: w1 2026-08-31 18:00
---
# needsleaf — self-claimed, but needs: is not done
EOF

mk_prd fpother <<'EOF'
---
state: claimed
origin: derived
priority: 50
complexity: 5
blast-radius: low
repo:
footprint:
  - shared/thing.py
time:
  est:
  actual:
claim: someoneelse 2026-08-31 18:00
---
# fpother — claimed by a different worker, holds the footprint
EOF

mk_prd fpleaf <<'EOF'
---
state: analyzing
origin: derived
priority: 50
complexity:
blast-radius:
repo:
footprint:
  - shared/thing.py
time:
  est:
  actual:
claim: w1 2026-08-31 18:00
---
# fpleaf — self-claimed, footprint clashes with fpother
EOF

mk_prd blockedone <<'EOF'
---
state: blocked
origin: derived
priority: 50
complexity:
blast-radius:
repo:
time:
  est:
  actual:
claim: w1 2026-08-31 18:00
---
# blockedone — a state outside open/specced/analyzing/claimed
EOF

BRIEF="python3 $REPO/resources/board/brief.py"

echo "== case 1: open PRD claimed by w1, no --worker -> still held (today's behaviour, unchanged) =="
before="$(md5sum "$BOARD/.pearde/prds/leaf1/prd.md")"
out=$($BRIEF leaf1 --board "$BOARD" 2>&1); code=$?
echo "$out" | sed 's/^/    /'
check "no-worker still refused" 1 "$code"
[ "$(echo "$out" | grep -c 'held —')" -ge 1 ] && note "ok   says held" || { note "FAIL no held word"; fail=1; }

echo "== case 2: same PRD, --worker w1 (self-claim) -> accepted, no --force, no forced =="
out=$($BRIEF leaf1 --worker w1 --board "$BOARD" 2>&1); code=$?
head -1 <<<"$out" | sed 's/^/    /'
check "self-claim accepted" 0 "$code"
[ "$(head -1 <<<"$out" | grep -c ' forced')" -eq 0 ] && note "ok   no forced mark" || { note "FAIL forced mark present with no --force"; fail=1; }
[ "$(head -1 <<<"$out" | grep -c '· analyst ·')" -eq 1 ] && note "ok   analyst role" || { note "FAIL wrong role"; fail=1; }

echo "== case 3: same PRD, --worker w2 (a different worker) -> still held =="
out=$($BRIEF leaf1 --worker w2 --board "$BOARD" 2>&1); code=$?
echo "$out" | sed 's/^/    /'
check "other worker still refused" 1 "$code"

after="$(md5sum "$BOARD/.pearde/prds/leaf1/prd.md")"
[ "$before" = "$after" ] && note "ok   leaf1's prd.md byte-identical across all three brief runs" \
  || { note "FAIL leaf1's prd.md changed — brief wrote something"; fail=1; }

echo "== case 4: specced/claimed PRD, self-claim -> implementer brief, no forced =="
out=$($BRIEF leaf2spec --worker w1 --board "$BOARD" 2>&1); code=$?
head -1 <<<"$out" | sed 's/^/    /'
check "specced/claimed self-claim accepted" 0 "$code"
[ "$(head -1 <<<"$out" | grep -c '· implementer ·')" -eq 1 ] && note "ok   implementer role" || { note "FAIL wrong role"; fail=1; }
[ "$(head -1 <<<"$out" | grep -c ' forced')" -eq 0 ] && note "ok   no forced mark" || { note "FAIL forced mark present"; fail=1; }

echo "== case 5: self-claimed, but needs: undone -> still refused, gated =="
out=$($BRIEF needsleaf --worker w1 --board "$BOARD" 2>&1); code=$?
echo "$out" | sed 's/^/    /'
check "needs gate still fires" 1 "$code"
[ "$(echo "$out" | grep -c 'gated —')" -eq 1 ] && note "ok   says gated" || { note "FAIL no gated word"; fail=1; }

echo "== case 6: self-claimed, but footprint clashes with another claimed PRD -> still refused, clash =="
out=$($BRIEF fpleaf --worker w1 --board "$BOARD" 2>&1); code=$?
echo "$out" | sed 's/^/    /'
check "footprint gate still fires" 1 "$code"
[ "$(echo "$out" | grep -c 'clash —')" -eq 1 ] && note "ok   says clash" || { note "FAIL no clash word"; fail=1; }

echo "== case 7: a state outside open/specced/analyzing/claimed, worker matches the claim -> still refused, state =="
out=$($BRIEF blockedone --worker w1 --board "$BOARD" 2>&1); code=$?
echo "$out" | sed 's/^/    /'
check "out-of-range state still refused" 1 "$code"
[ "$(echo "$out" | grep -c 'state —')" -eq 1 ] && note "ok   says state" || { note "FAIL no state word"; fail=1; }

rm -rf "$BOARD"

if [ "$fail" -eq 0 ]; then
  echo "ALL CASES PASSED"
else
  echo "SOME CASES FAILED"
fi
exit "$fail"
