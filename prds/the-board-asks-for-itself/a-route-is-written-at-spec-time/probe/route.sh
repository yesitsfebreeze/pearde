#!/usr/bin/env bash
# Probe for a-route-is-written-at-spec-time: proves `pearde specced --route -`
# drafts a workflow the library does not hold, refuses on a bad route with
# nothing written, refuses `--workflow none` and a `--route` naming a slug
# the library already has, and leaves an existing-atomic step un-blocked.
# Builds its own fixture board under a fresh mktemp -d — never under prds/.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
SPECS="$REPO/resources/board/specs.py"
WF="$REPO/resources/workflows.py"
FB="$(mktemp -d)/.pearde"
mkdir -p "$FB/workflows"

spec_prd() {  # spec_prd <name>
  mkdir -p "$FB/prds/$1/specs"
  cat > "$FB/prds/$1/prd.md" <<EOF
---
state: analyzing
origin: requested
priority: 50
complexity: 0
blast-radius:
repo: pearde
footprint:
  - resources/board/specs.py
---

# $1
EOF
  cat > "$FB/prds/$1/specs/spec01.md" <<'EOF'
---
complexity: 5
footprint:
  - resources/board/specs.py
---

# spec01

## Acceptance

- [ ] a thing happened

## Verify and Proof

```sh
echo ok
```
EOF
}

cat > "$FB/settings.md" <<'EOF'
---
language: English
workers: 3
split-above: 40
specs-above: 6
---
EOF

cat > "$FB/workflows/existing-atomic.md" <<'EOF'
---
atomic: existing-atomic
subject: a step already in the library, for the route to name without a block
date: 2026-08-01
runs: 3
---

# existing-atomic — a step already known

## Do

1. Do the known thing.

## Done when

- It is done.
EOF

route() {
  cat <<'EOF'
## Scores

complexity: 5
blast-radius: low
workflow: fixture-route

## Route

## Use when

- A PRD like this fixture, first of its kind — nothing in the library fits.

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `existing-atomic` | reuse the known first move | stop |
| 2 | `probe-the-fixture` | prove the new step the run actually took | → 1 |

### atomic probe-the-fixture

## Do

1. Run `echo ok` in the fixture directory.

## Done when

- The command prints `ok`.

## Fails when
EOF
}

echo "== case: fresh route drafts workflow + new atomic, existing step gets no block =="
spec_prd fixture-prd
route | PEARDE_AS=probe python3 "$SPECS" specced fixture-prd --blast low \
  --workflow fixture-route --route - --board "$FB"
test -f "$FB/workflows/fixture-route.md"
test -f "$FB/workflows/probe-the-fixture.md"
test ! -f "$FB/workflows/existing-atomic-2.md"   # no duplicate written for the existing step
grep -q '^workflow: fixture-route$' "$FB/prds/fixture-prd/prd.md"
python3 "$WF" check "$FB"

echo "== case: --workflow none without --route is refused =="
spec_prd case-none
if PEARDE_AS=probe python3 "$SPECS" specced case-none --blast low --workflow none \
     --board "$FB" 2>/tmp/probe-none.err; then
  echo "FAIL: --workflow none should have been refused"; exit 1
fi
grep -q 'Route' /tmp/probe-none.err

echo "== case: --route naming a slug already in the library is refused =="
spec_prd case-exists
if route | PEARDE_AS=probe python3 "$SPECS" specced case-exists --blast low \
     --workflow fixture-route --route - --board "$FB" 2>/tmp/probe-exists.err; then
  echo "FAIL: --route on an existing slug should have been refused"; exit 1
fi
grep -q 'exists' /tmp/probe-exists.err

echo "== case: a route that fails workflow check writes nothing, PRD stays analyzing =="
spec_prd case-red
cat <<'EOF' > /tmp/probe-route-bad.md
## Scores

complexity: 5
blast-radius: low
workflow: bad-route

## Route

## Use when

- A broken route, on purpose, to prove the rollback.

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `no-such-atomic` | names a step nobody wrote | stop |
EOF
if PEARDE_AS=probe python3 "$SPECS" specced case-red --blast low --workflow bad-route \
     --route - --board "$FB" < /tmp/probe-route-bad.md 2>/tmp/probe-red.err; then
  echo "FAIL: a red route should have been refused"; exit 1
fi
test ! -f "$FB/workflows/bad-route.md"
grep -q '^state: analyzing$' "$FB/prds/case-red/prd.md"

echo "== case: --dry with --route writes nothing =="
spec_prd case-dry
if ! route | sed -e 's/fixture-route/dry-route/' \
       -e 's/probe-the-fixture/dry-probe-the-fixture/g' | \
     PEARDE_AS=probe python3 "$SPECS" specced case-dry --blast low \
     --workflow dry-route --route - --dry --board "$FB" >/tmp/probe-dry.out; then
  echo "FAIL: dry route should have exited 0"; exit 1
fi
test ! -f "$FB/workflows/dry-route.md"
grep -q '^state: analyzing$' "$FB/prds/case-dry/prd.md"

echo "ALL PROBE CASES PASSED"
