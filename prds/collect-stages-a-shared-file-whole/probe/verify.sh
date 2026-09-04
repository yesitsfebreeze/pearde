#!/usr/bin/env bash
# Fixture for collect-stages-a-shared-file-whole.
#
# Builds a throwaway layout at run time — a code repo whose board is a
# LINKED WORKTREE at `.pearde`, exactly the layout this machine is on, so
# `repo_root(prd["dir"])` is the board worktree and not the code repo.
# Two PRDs share `shared.py`; `prds-a` is finished and collecting, `prds-b`
# holds uncommitted work in the same file. Every check prints
# `PASS <name>` or `FAIL <name>: <why>`.
#
# Usage: probe/verify.sh           (all scenarios — what the board's
#                                   harness sweep runs)
#        probe/verify.sh 1 3       (selected scenarios only)
#
# Scenarios 1 and 2 are the two independent gaps the PRD names. They are
# written as the CORRECT behaviour, so they are RED before the fix and
# GREEN after it. Scenarios 3-5 and 7 are the controls and must never go
# red. The total this prints is NOT pinned by any spec: a check added
# here must never redden the unit it backs.
set -u
# The repo this harness lives in: <repo>/.pearde/prds/<prd>/probe/verify.sh.
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
COLLECT=${COLLECT:-$ROOT/resources/board/collect.py}
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
lacks() {  # lacks <name> <got> <needle>
  case "$2" in *"$3"*)
    report no "$1" "did NOT expect [$3] in: $(echo "$2" | tail -3)";; *)
    report ok "$1";; esac
}
is() {  # is <name> <got> <want>
  if [ "$2" = "$3" ]; then report ok "$1"
  else report no "$1" "got [$2], want [$3]"; fi
}

# build <dir> — $SIB_STATE is prds-b's state, $SIB_FP its prd.md footprint
# block, $SIB_SPEC_FP its spec footprint. $PRE_EDIT, when set, is run
# after the code repo's first commit and BEFORE prds-a's claim snapshot,
# so whatever it writes is in the claim's baseline.
build() {  # build <dir>
  T=$1
  mkdir -p "$T/code"
  git -C "$T/code" init -q -b main
  git -C "$T/code" config user.email probe@probe
  git -C "$T/code" config user.name probe
  printf 'one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten\n' \
    > "$T/code/shared.py"
  printf 'own\n' > "$T/code/own.py"
  printf '.pearde/\n' > "$T/code/.gitignore"
  git -C "$T/code" add . && git -C "$T/code" commit -qm init

  # ── the board as a LINKED WORKTREE of the same repo, this machine's
  #    layout: `.pearde/.git` is a gitdir: file, and `repo_root` of any
  #    path under it is `$T/code/.pearde`, never `$T/code`.
  git -C "$T/code" worktree add -q -b pearde "$T/code/.pearde" HEAD
  git -C "$T/code/.pearde" rm -rq --cached . >/dev/null 2>&1
  rm -f "$T/code/shared.py.board" 2>/dev/null
  ( cd "$T/code/.pearde" && rm -f shared.py own.py .gitignore )
  mkdir -p "$T/code/.pearde/prds/prds-a/specs" \
           "$T/code/.pearde/prds/prds-b/specs" "$T/code/.pearde/.state"
  : > "$T/code/.pearde/.state/transitions.jsonl"
  printf '.claims/\n.state/\n' > "$T/code/.pearde/.gitignore"

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
  git -C "$T/code/.pearde" add -A
  git -C "$T/code/.pearde" -c user.email=probe@probe -c user.name=probe \
      commit -qm board

  # dirt that must be IN the claim's baseline goes down before the snapshot
  if [ -n "${PRE_EDIT:-}" ]; then eval "$PRE_EDIT"; fi
  PEARDE_AS=an-probe python3 "$COLLECT" --snapshot prds-a \
      --board "$T/code/.pearde" >/dev/null
}

collect_run() {  # collect_run <dir> <args...>
  local T=$1; shift
  python3 "$COLLECT" prds-a --board "$T/code/.pearde" --as an-probe "$@" 2>&1
}

teardown() { git -C "$1/code" worktree remove --force "$1/code/.pearde" \
             >/dev/null 2>&1; rm -rf "$1"; }

# ── 0: the layout itself — the board IS its own repo root, so the claim
#      baseline that `snapshot` writes must still hold the CODE repo's
#      dirt. This is gap 2 at its source, measured before any collect. ────
s0() {
  local T; T=$(mktemp -d)
  SIB_STATE=specced; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  PRE_EDIT='printf "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n" > "$T/code/shared.py"'
  build "$T"
  local root
  root=$(python3 - "$T" "$ROOT" <<'PY'
import sys, os
sys.path.insert(0, os.path.join(sys.argv[2], "resources/board"))
import plan as planlib
print(planlib.repo_root(os.path.join(sys.argv[1], "code/.pearde/prds/prds-a")))
PY
)
  is 0a-board-is-its-own-root "$root" "$T/code/.pearde"
  # the recorded baseline must explain the code repo's dirty file
  local d="$T/code/.pearde/.claims/prds-a"
  if grep -rq 'shared\.py' "$d" 2>/dev/null; then
    report ok 0b-baseline-holds-code-path
  else
    report no 0b-baseline-holds-code-path \
      "claim baseline names no code-repo path; files: $(ls "$d" | tr '\n' ' ')"
  fi
  teardown "$T"
}

# ── 1: gap one — the sibling refusal is scoped to analyzing/claimed/
#      blocked, so a `specced` sibling with code standing in the tree is
#      invisible. b's edit lands AFTER a's claim: nothing explains it, so
#      collect must stop rather than sweep it into a's commit. ────────────
s1() {
  local T; T=$(mktemp -d)
  SIB_STATE=specced; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  PRE_EDIT=""
  build "$T"
  printf 'one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n' \
    > "$T/code/shared.py"                       # b's edit, after the claim
  printf 'own\nown-a\n' > "$T/code/own.py"      # a's own edit
  local out rc sha
  sha=$(git -C "$T/code" rev-parse HEAD)
  out=$(collect_run "$T" --dry); rc=$?
  want 1a-specced-sibling-refused "$out" "is in prds-b's footprint too"
  is 1b-dry-exit "$rc" 1
  out=$(collect_run "$T"); rc=$?
  is 1c-real-exit "$rc" 1
  is 1d-nothing-committed "$(git -C "$T/code" rev-parse HEAD)" "$sha"
  lacks 1e-b-not-carried "$(git -C "$T/code" show HEAD:shared.py)" "ten-B"
  # the refusal must OFFER the way out, not only name the clash
  want 1f-widen-offered "$out" '`--widen shared.py` takes it whole'
  # …and must NOT blame the claim: this claim DOES hold a code side, so the
  # stale-claim clause belongs to scenario 6 and nowhere else
  lacks 1g-no-stale-clause "$out" "recorded before the baseline covered"
  teardown "$T"
}

# ── 2: gap two — the hunk-splitter. b's edit is in the tree BEFORE a's
#      claim, so the baseline explains it; a edits a distant line after.
#      The file must be staged by hunk: a's line committed, b's left in
#      the working tree. Today the baseline holds no code path at all, so
#      the split never happens. ────────────────────────────────────────────
s2() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  # b's line 10 edit, before a's claim — this is what the baseline holds
  PRE_EDIT='printf "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n" > "$T/code/shared.py"'
  build "$T"
  # a's line 1 edit, after the claim — far from b's, so `-U0` keeps them
  # two hunks and `two_authors` has nothing to merge
  printf 'one-A\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n' \
    > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  is 2a-dry-exit "$rc" 0
  want 2b-dry-splits "$out" "shared.py"
  out=$(collect_run "$T"); rc=$?
  is 2c-real-exit "$rc" 0
  want 2d-a-line-committed "$(git -C "$T/code" show HEAD:shared.py)" "one-A"
  lacks 2e-b-line-not-committed \
    "$(git -C "$T/code" show HEAD:shared.py)" "ten-B"
  want 2f-b-line-still-in-tree "$(cat "$T/code/shared.py")" "ten-B"
  teardown "$T"
}

# ── 3: control — no overlap, a's own edits still commit whole ────────────
s3() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed; SIB_FP="  - other.py"
  SIB_SPEC_FP="footprint:
  - other.py"
  PRE_EDIT=""
  build "$T"
  printf 'one-A\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten\n' \
    > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  is 3a-dry-ok "$rc" 0
  want 3b-dry-adds "$out" "own.py"
  out=$(collect_run "$T"); rc=$?
  is 3c-real-ok "$rc" 0
  want 3d-committed "$(git -C "$T/code" show HEAD:shared.py)" "one-A"
  teardown "$T"
}

# ── 4: control — `--widen` still takes the shared file whole, on the
#      worker's word, and says so ─────────────────────────────────────────
s4() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  PRE_EDIT=""
  build "$T"
  printf 'one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n' \
    > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --widen "$T/code/shared.py"); rc=$?
  is 4a-widen-ok "$rc" 0
  want 4b-widen-named "$out" "widened shared.py"
  want 4c-whole-file "$(git -C "$T/code" show HEAD:shared.py)" "ten-B"
  teardown "$T"
}

# ── 5: control — a `done` sibling never contends: its work is committed,
#      so its footprint must not refuse anything ──────────────────────────
s5() {
  local T; T=$(mktemp -d)
  SIB_STATE=done; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  PRE_EDIT=""
  build "$T"
  printf 'one-A\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten\n' \
    > "$T/code/shared.py"
  printf 'own\nown-a\n' > "$T/code/own.py"
  local out rc
  out=$(collect_run "$T" --dry); rc=$?
  is 5a-done-sibling-ok "$rc" 0
  teardown "$T"
}

# ── 6: a claim recorded before the baseline covered the code repo — the
#      claim dir every board on this machine already holds. It cannot
#      split, and the refusal must say that rather than blame the worker. ─
s6() {
  local T; T=$(mktemp -d)
  SIB_STATE=claimed; SIB_FP="  - shared.py"
  SIB_SPEC_FP="footprint:
  - shared.py"
  PRE_EDIT='printf "one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n" > "$T/code/shared.py"'
  build "$T"
  # age the claim dir back to the one-repo shape `snapshot` used to write
  rm -f "$T/code/.pearde/.claims/prds-a/diff.repo" \
        "$T/code/.pearde/.claims/prds-a/untracked.repo" \
        "$T/code/.pearde/.claims/prds-a/repo"
  printf 'one-A\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten-B\n' \
    > "$T/code/shared.py"
  local out rc sha
  sha=$(git -C "$T/code" rev-parse HEAD)
  out=$(collect_run "$T" --dry); rc=$?
  is 6a-exit "$rc" 1
  want 6b-says-why "$out" "recorded before the baseline covered"
  lacks 6c-b-not-carried "$(git -C "$T/code" show HEAD:shared.py)" "ten-B"
  is 6d-nothing-committed "$(git -C "$T/code" rev-parse HEAD)" "$sha"
  teardown "$T"
}

# ── 7: control — a board that is NOT its own repo (a plain `.pearde/`
#      inside the code repo, no worktree and no `.git` of its own). There
#      is only one root, so no second side may be written and `baseline`
#      must read exactly as it did before there were two. ────────────────
s7() {
  local T; T=$(mktemp -d)
  mkdir -p "$T/code/.pearde/prds/prds-a"
  git -C "$T/code" init -q -b main
  git -C "$T/code" config user.email probe@probe
  git -C "$T/code" config user.name probe
  printf 'one\ntwo\nthree\n' > "$T/code/shared.py"
  cat > "$T/code/.pearde/prds/prds-a/prd.md" <<'EOF'
---
state: claimed
priority: 1
claim: w1 2026-08-31 22:00
footprint:
  - shared.py
---
# prds-a — a finishes

body
EOF
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
  git -C "$T/code" add -A && git -C "$T/code" commit -qm init
  printf 'one-A\ntwo\nthree\n' > "$T/code/shared.py"   # dirt, pre-snapshot
  local out
  out=$(python3 - "$T" "$ROOT" "$COLLECT" <<'ONEREPO'
import os, sys
T, R, C = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(R, "resources"))
sys.path.insert(0, os.path.dirname(C))
import plan as planlib, collect as c
B = os.path.join(T, "code", ".pearde")
say = []
root = planlib.repo_root(os.path.join(B, "prds", "prds-a"))
say.append(("7a-board-is-not-its-own-root",
            root == os.path.join(T, "code"), "repo_root=%s" % root))
d = c.snapshot(B, "prds-a", gate="")
extra = [n for n in ("repo", "diff.repo", "untracked.repo")
         if os.path.isfile(os.path.join(d, n))]
say.append(("7b-no-repo-side-written", not extra, "wrote " + ",".join(extra)))
b = c.baseline(B, "prds-a")
say.append(("7c-sides-board-only",
            b is not None and sorted(b["sides"]) == ["board"],
            "sides=%s" % (sorted(b["sides"]) if b else None)))
say.append(("7d-alias-is-the-board-side",
            b is not None and b["hunks"] is b["sides"]["board"]["hunks"]
            and b["untracked"] is b["sides"]["board"]["untracked"],
            "top level diverged from the board side"))
say.append(("7e-code-dirt-in-the-one-side",
            b is not None and "shared.py" in b["hunks"],
            "hunks=%s" % (list(b["hunks"]) if b else None)))
for name, good, why in say:
    print("ok\t%s\t" % name if good else "no\t%s\t%s" % (name, why))
ONEREPO
)
  local verdict name why
  while IFS=$'\t' read -r verdict name why; do
    [ -n "$name" ] && report "$verdict" "$name" "$why"
  done <<< "$out"
  rm -rf "$T"
}

SEL=${*:-"0 1 2 3 4 5 6 7"}
for s in $SEL; do "s$s"; done
note "---- $PASS passed, $FAIL failed"
if [ "$FAIL" -eq 0 ]; then note "verify.sh exit 0"; exit 0; fi
note "verify.sh exit 1"; exit 1
