#!/usr/bin/env bash
# Fixture for collect-commits-only-the-prd-s-own-edits-not-the-footprint-s.
# Builds a throwaway layout at runtime — a code repo with a nested board
# repo, a finished PRD `prds-a` collecting while a held sibling `prds-b`
# shares part of its footprint — and exercises collect against it. Every
# check prints `PASS <name>` or `FAIL <name>: <why>`.
# Usage: probe/run.sh            (all scenarios)
#        probe/run.sh 1 3        (selected scenarios only)
set -u
# Overridable so the fixture can be aimed at a mutated copy — the pre-fix
# proof runs the same scenarios against a collect.py with the guard cut out.
COLLECT=${COLLECT:-/Users/feb/dev/infra/pearde/resources/board/collect.py}
PASS=0; FAIL=0

note() { printf '%s\n' "$*"; }

report() {  # report <ok|no> <name> [why]
  if [ "$1" = ok ]; then PASS=$((PASS+1)); note "PASS $2";
  else FAIL=$((FAIL+1)); note "FAIL $2: ${3:-}"; fi
}

want() {  # want <name> <got> <needle>
  case "$2" in *"$3"*) report ok "$1";; *)
    report no "$1" "expected [$3] in: $(echo "$2" | tail -3)";; esac
}

is() {  # is <name> <got> <want> — every assertion counts, pass or fail
  if [ "$2" = "$3" ]; then report ok "$1"
  else report no "$1" "got [$2], want [$3]"; fi
}

# build <dir> — prds-b's state and footprint come in $SIB_STATE,
# $SIB_FP (its prd.md footprint block, "" for none) and $SIB_SPEC_FP
# (its spec's footprint entry, "" for none).
build() {  # build <dir>
  T=$1
  mkdir -p "$T/code/.pearde/prds/prds-a/specs" "$T/code/.pearde/prds/prds-b/specs" \
           "$T/code/.pearde/.state"
  : > "$T/code/.pearde/.state/transitions.jsonl"
  git -C "$T/code" init -q
  git -C "$T/code" config user.email probe@probe
  git -C "$T/code" config user.name probe
  # the board is its own nested repo the code repo never tracks, as here
  printf '.pearde/\n' > "$T/code/.gitignore"
  printf 'one\ntwo\nthree\nfour\nfive\n' > "$T/code/shared.py"
  printf 'own\n' > "$T/code/own.py"
  git -C "$T/code" add . && git -C "$T/code" commit -qm init

  cat > "$T/code/.pearde/settings.md" <<'EOF'
---
name: probe
language: English
workers: 2
pipeline: 8
weight-default: 20
---
# probe board
EOF
  cat > "$T/code/.pearde/prds/prds-a/prd.md" <<EOF
---
state: claimed
priority: 1
claim: w1 2026-08-31 22:00
footprint:
  - shared.py
  - own.py
$A_FP_EXTRA
---
# prds-a — a finishes

body
EOF
  cat > "$T/code/.pearde/prds/prds-a/specs/spec01.md" <<'EOF'
---
complexity: 5
footprint:
  - shared.py
  - own.py
---
# spec01 — a works

## Acceptance

- [x] something true

## Verify and Proof

```sh
echo verify-ok
```
EOF
  {
    printf -- '---\nstate: %s\npriority: 1\n' "$SIB_STATE"
    if [ -n "$SIB_FP" ]; then printf 'footprint:\n%s\n' "$SIB_FP"; fi
    printf -- '---\n# prds-b — b in flight\n\nbody\n'
  } > "$T/code/.pearde/prds/prds-b/prd.md"
  cat > "$T/code/.pearde/prds/prds-b/specs/spec01.md" <<EOF
---
complexity: 5
$SIB_SPEC_FP
---
# spec01 — b works

## Acceptance

- [x] something true

## Verify and Proof

\`\`\`sh
echo verify-ok
\`\`\`
EOF
  git -C "$T/code/.pearde" init -q
  git -C "$T/code/.pearde" config user.email probe@probe
  git -C "$T/code/.pearde" config user.name probe
  git -C "$T/code/.pearde" add .
  # the claims dir and the machine's state dir are board-local, not records
  printf '.claims/\n.state/\n' > "$T/code/.pearde/.gitignore"
  git -C "$T/code/.pearde" add .
  git -C "$T/code/.pearde" commit -qm board
  # a's claim baseline, taken at a clean tree — what `claim` records
  PEARDE_AS=an-probe python3 "$COLLECT" --snapshot prds-a \
      --board "$T/code/.pearde" >/dev/null
}

collect_run() {  # collect_run <dir> <args...>
  local T=$1; shift
  python3 "$COLLECT" prds-a --board "$T/code/.pearde" --as an-probe "$@" 2>&1
}

# ── scenario 1: the sweep — a held sibling's hunk inside a's footprint,
#    taken after a's claim — is refused, nothing written ─────────────────────
s1() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed
  SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  A_FP_EXTRA=""
  build "$T"
  printf 'one\ntwo-B\nthree\nfour\nfive\n' > "$T/code/shared.py"   # b's edit
  printf 'own\nown-a\n' > "$T/code/own.py"                        # a's edit
  local out rc sha
  sha=$(git -C "$T/code" rev-parse HEAD)
  out=$(collect_run "$T" --dry); rc=$?
  want 1a-dry-refuses "$out" "is in prds-b's footprint too"
  want 1i-widen-offered "$out" '`--widen shared.py` takes it whole'
  is 1b-dry-exit "$rc" 1
  is 1c-no-commit "$(git -C "$T/code" rev-parse HEAD)" "$sha"
  out=$(collect_run "$T"); rc=$?
  want 1e-real-refuses "$out" "is in prds-b's footprint too"
  is 1f-real-exit "$rc" 1
  is 1g-nothing-written "$(git -C "$T/code" rev-parse HEAD)" "$sha"
  is 1h-state-held \
    "$(grep -c '^state: claimed' "$T/code/.pearde/prds/prds-a/prd.md")" 1
  [ -f "$T/code/.pearde/.claims/prds-a/at" ] && report ok 1d-snapshot-exists \
    || report no 1d-snapshot "claims snapshot missing"
  rm -rf "$T"
}

# ── scenario 2: --widen takes the file whole, the worker's word ─────────────
s2() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed
  SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  A_FP_EXTRA=""
  build "$T"
  printf 'one\ntwo-B\nthree\nfour\nfive\n' > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --widen "$T/code/shared.py"); rc=$?
  if [ $rc -ne 0 ]; then
    report no 2a-widen-collect "exit $rc: $(echo "$out" | tail -3)"
    rm -rf "$T"; return
  fi
  report ok 2a-widen-collect
  want 2b-widen-in-message "$out" "widened shared.py"
  git -C "$T/code" diff --quiet HEAD && report ok 2d-committed \
    || report no 2d-committed "tree still dirty after collect"
  want 2e-commit-whole "$(git -C "$T/code" show HEAD:shared.py)" "two-B"
  rm -rf "$T"
}

# ── scenario 3: the control — no overlap, a's own edits still commit ────────
s3() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed
  SIB_FP="  - other.py"
  SIB_SPEC_FP="footprint:
  - other.py"
  A_FP_EXTRA=""
  build "$T"
  printf 'one\ntwo-A\nthree\nfour\nfive\n' > "$T/code/shared.py"  # a's own edit
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  is 3a-dry-ok "$rc" 0
  want 3b-dry-adds "$out" "would add: own.py, shared.py"
  out=$(collect_run "$T"); rc=$?
  is 3c-real-ok "$rc" 0
  git -C "$T/code" diff --quiet HEAD && report ok 3d-committed \
    || report no 3d-committed "own edits not committed"
  rm -rf "$T"
}

# ── scenario 4: the analyzing window — a sibling with no specs and no
#    footprint is invisible to the guard; the documented gap, sweep persists ─
s4() {
  local T; T=$(mktemp -d)
  SIB_STATE=analyzing
  SIB_FP=""
  SIB_SPEC_FP=""
  build "$T"
  printf 'one\ntwo-B\nthree\nfour\nfive\n' > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  if [ $rc -eq 0 ]; then report ok 4a-gap-persists
  else report no 4a-gap-persists "unexpected refusal: $(echo "$out" | tail -2)"; fi
  rm -rf "$T"
}

# ── scenario 5: the untracked sibling file — a new file inside the shared
#    footprint after the claim is refused, not swept whole ───────────────────
s5() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed
  SIB_FP="  - shared"
  SIB_SPEC_FP="footprint:
  - shared"
  A_FP_EXTRA="  - shared"
  build "$T"
  mkdir -p "$T/code/shared"
  printf 'brand new\n' > "$T/code/shared/new.py"   # b's untracked file
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  want 5a-untracked-refused "$out" "is in prds-b's footprint too"
  want 5c-widen-offered "$out" '`--widen shared/new.py` takes it whole'
  is 5b-dry-exit "$rc" 1
  out=$(collect_run "$T"); rc=$?          # the real run, not only the dry one
  is 5e-real-exit "$rc" 1
  git -C "$T/code" ls-files --error-unmatch shared/new.py >/dev/null 2>&1 \
    && report no 5d-not-swept "the sibling's untracked file was committed" \
    || report ok 5d-not-swept
  rm -rf "$T"
}

SEL=${*:-"1 2 3 4 5"}
for s in $SEL; do "s$s"; done
note "---- $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then note "run.sh exit 0"; exit 0; fi
note "run.sh exit 1"; exit 1