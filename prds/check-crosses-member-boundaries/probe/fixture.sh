#!/usr/bin/env bash
# Builds the PRD's fixture in a run-time directory and prints what each reader
# says. No argument: a fresh mktemp dir, removed on exit. One argument: build
# it there and leave it. Never writes under prds/ — a dir holding prd.md
# anywhere under the board is a PRD.
set -u
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
if [ $# -ge 1 ]; then TMP="$1"; mkdir -p "$TMP"; else
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT; fi

wf () { # <dir> <slug> — a valid one-step workflow named <slug>
  mkdir -p "$1"
  cat > "$1/$2.md" <<WF
---
workflow: $2
subject: a fixture route
date: 2026-08-01
runs: 0
---

# Workflow $2

## Use when

- a fixture needs a slug that resolves

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | \`step-one\` | the only step | \`stop\` |
WF
  cat > "$1/step-one.md" <<AT
---
atomic: step-one
subject: the only step
date: 2026-08-01
---

## Do

Nothing — this is a fixture.

## Done when

- [ ] nothing happened
AT
}

prd () { # <boarddir> <name> <workflow-value-line-or-empty>
  mkdir -p "$2"
  { echo '---'; echo 'state: specced'; echo 'priority: 10';
    [ -n "${3:-}" ] && echo "$3"; echo '---'; echo;
    echo "# $(basename "$2") — a fixture PRD"; } > "$2/prd.md"
}

# --- the master, and its members -------------------------------------------
mkdir -p "$TMP/master/.pearde" "$TMP/solo/.pearde" "$TMP/ownlib/.pearde"
wf "$TMP/master/.pearde/workflows" mw          # only the MASTER holds `mw`
wf "$TMP/ownlib/.pearde/workflows" ownroute    # only the MEMBER holds `ownroute`

cat > "$TMP/master/.pearde/settings.md" <<SM
---
members:
  - solo: ../../solo/.pearde
  - ownlib: ../../ownlib/.pearde
  - gone: ../../gone/.pearde
---

# fixture master
SM

prd "$TMP/master/.pearde" "$TMP/solo/.pearde/broken"    'workflow: no-such-route'
prd "$TMP/master/.pearde" "$TMP/solo/.pearde/b-master"  'workflow: mw'
prd "$TMP/master/.pearde" "$TMP/ownlib/.pearde/b-own"   'workflow: ownroute'
mkdir -p "$TMP/master/.pearde/listed"
printf -- '---\nstate: specced\npriority: 10\nworkflow:\n  - one-route\n  - two-route\n---\n\n# listed\n' \
  > "$TMP/master/.pearde/listed/prd.md"

run () { # <label> <board>
  out="$(python3 "$REPO/resources/workflows.py" check "$2" 2>&1)"; rc=$?
  echo "--- check on $1 — exit $rc"
  [ -n "$out" ] && echo "$out" | sed 's/^/    /'
  return 0
}

echo "fixture at $TMP"
echo
run "the master   ($TMP/master/.pearde)"  "$TMP/master/.pearde"
run "member solo  ($TMP/solo/.pearde)"    "$TMP/solo/.pearde"
run "member ownlib($TMP/ownlib/.pearde)"  "$TMP/ownlib/.pearde"
echo
echo "--- scan on the master (plan.py), for comparison"
python3 "$REPO/resources/board/plan.py" scan "$TMP/master/.pearde" 2>&1 \
  | grep -E "broken|b-master|b-own|listed|MISSING|gone" | sed 's/^/    /'
