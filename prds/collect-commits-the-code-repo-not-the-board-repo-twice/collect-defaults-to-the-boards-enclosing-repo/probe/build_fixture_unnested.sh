#!/bin/bash
# Same board content as build_fixture_nested.sh, but the board is NOT its
# own git repo: `.pearde` sits inside the code repo with no `.git` of its
# own — the old layout. Proves repo_of()'s unchanged branch: board_root ==
# the code repo already (found by walking past `.pearde`), so the fix must
# not go hunting further up. $1 = target dir, made fresh each call.
set -e
ROOT="$1"
rm -rf "$ROOT"
mkdir -p "$ROOT/code"
CODE="$ROOT/code"
cd "$CODE"
git init -q
git config user.email a@b.c; git config user.name tester
mkdir -p resources
echo "print('guard v1')" > resources/guard.py
git add resources/guard.py
git commit -q -m "init code repo"

mkdir -p .pearde/prds/fake-prd/specs .pearde/.state
cat > .pearde/settings.md <<'EOF'
---
name: fixture
language: English
workers: 1
pipeline: 1
weight-default: 20
gantt-day: 8h
---
# fixture board
## Admission
test
## Deliverable
test
EOF
cat > .pearde/prds/fake-prd/prd.md <<'EOF'
---
state: claimed
origin: derived
priority: 50
complexity: 5
blast-radius: low
claim: an-1 2020-01-01 00:00:00
---
# Fake PRD — a fixture

body.
EOF
cat > .pearde/prds/fake-prd/specs/spec01.md <<'EOF'
---
complexity: 5
footprint:
  - resources/guard.py
---
# spec01 — fixture spec

## Acceptance

- [x] fixture box
EOF
git add -A
git commit -q -m "init code repo, board included, no nested .git"
echo "print('guard v2 — fixed')" > resources/guard.py
echo "fixture built at $ROOT"
