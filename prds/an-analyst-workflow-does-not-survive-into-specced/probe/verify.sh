#!/usr/bin/env bash
# an-analyst-workflow-does-not-survive-into-specced — the harness. Copies the
# example board to a temp dir (never under prds/, never run in place), adds
# the PRDs the checks need, and drives specs.py against it. One line per
# assertion, a count at the end.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
SPECS="$ROOT/resources/board/specs.py"
BR="$ROOT/resources/board/brief.py"
EX="$ROOT/resources/board/example"
D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT
B="$D/.pearde"; PRDS="$B/prds"
export PEARDE_AS=engineer
pass=0; fail=0
ok()  { pass=$((pass+1)); echo "  ok   $1"; }
bad() { fail=$((fail+1)); echo "  FAIL $1"; }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }
run() { python3 "$SPECS" "$@" --board "$B"; }
force() { python3 "$ROOT/resources/board/transitions.py" set "$1" "$2" --force --board "$B" >/dev/null; }
WFL=fix-a-line

[ -d "$EX" ] || EX="$ROOT/resources/board/example"
[ -d "$EX" ] || { echo "no example board"; exit 1; }
cp -R "$EX/." "$B/"
mkdir -p "$B/.state"

prd() { # dir state [extra-fm]
  mkdir -p "$PRDS/$1"
  printf -- '---\nstate: %s\norigin: derived\npriority: 50\ncomplexity: 0\nblast-radius:\nrepo: example\n%s---\n\n# %s — a fixture\n\nWhat exists when it is done.\n' "$2" "${3:-}" "$1" > "$PRDS/$1/prd.md"
}
spec() { # dir file wf
  mkdir -p "$PRDS/$1/specs"
  printf -- '---\ncomplexity: 4\nfootprint:\n  - src/a.py\n%s---\n\n# %s — a unit\n\n## Acceptance\n\n- [ ] a box that can fail\n\n## Verify and Proof\n\n```sh\npython3 -m pytest src/a.py\n```\n' "$3" "$2" > "$PRDS/$1/specs/$2"
}
WFMAJOR=$'workflow: fix-a-line\n'

# ── derived write ────────────────────────────────────────────────────────────
echo "derive"
prd one analyzing
spec one spec01.md "$WFMAJOR"
OUT=$(run specced one --blast low 2>"$D/e"); rc=$?
check "one spec naming a workflow → exit 0"       "[ $rc = 0 ]"
check "…state: specced"                           "grep -q '^state: specced' $PRDS/one/prd.md"
check "…workflow: fix-a-line written up"          "grep -q '^workflow: fix-a-line' $PRDS/one/prd.md"
check "…no note on stderr"                        "[ ! -s \"$D/e\" ]"
# --check writes nothing
prd seven analyzing
spec seven spec01.md "$WFMAJOR"
OUT=$(run specced seven --blast low --check 2>&1); rc=$?
check "--check exits 0, prints the sum"           "[ $rc = 0 ] && grep -q 'seven: ok · complexity 4' <<<\"\$OUT\""
check "…and writes no workflow key"               "! grep -q '^workflow:' $PRDS/seven/prd.md"
# commented-out key counts as absent
prd nine analyzing $'# workflow:  # commented\n'
spec nine spec01.md "$WFMAJOR"
OUT=$(run specced nine --blast low 2>/dev/null); rc=$?
check "a commented # workflow: derives too"       "[ $rc = 0 ] && grep -q '^workflow: fix-a-line' $PRDS/nine/prd.md"
# dry shows the slug, writes nothing
prd three analyzing
spec three spec01.md "$WFMAJOR"
OUT=$(run specced three --blast low --dry 2>/dev/null); rc=$?
check "--dry exit 0, shows the derived slug"      "[ $rc = 0 ] && grep -q 'dry · workflow: fix-a-line' <<<\"\$OUT\""
check "…and changes no file"                      "! grep -q '^workflow:' $PRDS/three/prd.md && grep -q '^state: analyzing' $PRDS/three/prd.md"

# ── the flag wins, both directions ───────────────────────────────────────────
echo "flag"
prd two analyzing
spec two spec01.md "$WFMAJOR"
run specced two --blast low --workflow fix-a-line >/dev/null; rc=$?
check "explicit same slug → exit 0, written"      "[ $rc = 0 ] && grep -q '^workflow: fix-a-line' $PRDS/two/prd.md"
# flag overrides a different spec slug: dry shows the flag's slug
prd ten analyzing
spec ten spec01.md "$WFMAJOR"
OUT=$(run specced ten --blast low --dry --workflow fix-a-line 2>&1); rc=$?
check "--dry shows the flag's slug, not the spec's" "[ $rc = 0 ] && grep -q 'dry · workflow: fix-a-line' <<<\"\$OUT\""
# a PRD that already carries a workflow keeps it
prd six analyzing $'workflow: fix-a-line\n'
spec six spec01.md "$WFMAJOR"
run specced six --blast low >/dev/null; rc=$?
check "PRD key kept when a spec names one"        "[ $rc = 0 ] && [ \"\$(grep -c '^workflow: fix-a-line' $PRDS/six/prd.md)\" = 1 ]"
PRDFM=$'workflow: implement-a-spec\n'
mkdir -p "$B/prds/keeps/specs"
printf -- '---\nstate: analyzing\norigin: derived\npriority: 50\ncomplexity: 0\nblast-radius:\nrepo: example\n%s---\n\n# keeps — a fixture\n\nWhat exists when it is done.\n' "$PRDFM" > "$B/prds/keeps/prd.md"
printf -- '---\nworkflow: implement-a-spec\nsubject: x\ndate: 2026-08-31\n---\n\n# implement-a-spec\n\n## Use when\n\n- x\n\n## Steps\n\n| # | atomic | why | on failure |\n|---|---|---|---|\n' > "$B/workflows/implement-a-spec.md"
spec keeps spec01.md "$WFMAJOR"
ERR=$(run specced keeps --blast low 2>&1 >/dev/null); rc=$?
check "a carried key is not overwritten"          "[ $rc = 0 ] && grep -q '^workflow: implement-a-spec' $PRDS/keeps/prd.md"
rm "$B/prds/keeps"; rm -rf "$B/prds/keeps"; rm -f "$B/workflows/implement-a-spec.md"

# ── ambiguity: two specs, two slugs ──────────────────────────────────────────
echo "ambiguous"
mkdir -p "$B/workflows"
printf -- '---\nworkflow: implement-a-spec\nsubject: x\ndate: 2026-08-31\n---\n\n# implement-a-spec\n\n## Use when\n\n- x\n\n## Steps\n\n| # | atomic | why | on failure |\n|---|---|---|---|\n' > "$B/workflows/implement-a-spec.md"
prd four analyzing
spec four spec01.md "$WFMAJOR"
spec four spec02.md $'workflow: implement-a-spec\n'
ERR=$(run specced four --blast low 2>"$D/e4" >/dev/null); rc=$?
check "two slugs → exit 0, PRD still specced"      "[ $rc = 0 ] && grep -q '^state: specced' $PRDS/four/prd.md"
check "…no workflow key written"                   "! grep -q '^workflow:' $PRDS/four/prd.md"
check "…the note names both slugs on stderr"       "grep -q 'note: 2 specs name different workflows — fix-a-line, implement-a-spec' \"$D/e4\""
rm -f "$B/workflows/implement-a-spec.md"

# ── validation untouched ─────────────────────────────────────────────────────
echo "validate"
prd five analyzing
spec five spec01.md $'workflow: nosuchwf\n'
ERR=$(run specced five --blast low 2>&1 >/dev/null); rc=$?
check "unknown slug refused, file and line"       "[ $rc = 1 ] && grep -q 'spec01.md:5: workflow .nosuchwf. names no workflow' <<<\"\$ERR\""
check "…and the PRD is not written"               "grep -q '^state: analyzing' $PRDS/five/prd.md"
# no workflow named anywhere: silent
prd eight analyzing
spec eight spec01.md ""
OUT=$(run specced eight --blast low 2>"$D/e8"); rc=$?
check "no slug anywhere → exit 0, silent"         "[ $rc = 0 ] && ! grep -q 'workflow' \"$D/e8\" && ! grep -q '^workflow:' $PRDS/eight/prd.md"

# ── the brief reads the key back ─────────────────────────────────────────────
echo "brief"
OUT=$(cd "$D" && python3 "$BR" one --as engineer --role analyst 2>&1); rc=$?
check "analyst brief head carries wf fix-a-line"  "grep -q '^# brief one · analyst · as engineer · wf fix-a-line' <<<\"\$OUT\""
OUT=$(cd "$D" && python3 "$BR" one --as engineer --role implementer 2>&1); rc=$?
check "implementer brief head carries wf too"     "grep -q '^# brief one · implementer · as engineer · wf fix-a-line' <<<\"\$OUT\""

echo
echo "verify: $pass/$((pass+fail)) checks pass"
[ "$fail" = 0 ]