#!/bin/sh
# Every template a writer copies still round-trips after the rewrite.
# Run from the repo root of the checkout under test:
#     sh .pearde/prds/<prd>/probe/roundtrip.sh
# Builds a throwaway board in a temp dir — never under .pearde/prds/, where a
# directory holding prd.md would read as a PRD.
#
# grammar.py and memos.py copy their template's BODY, so a rewrite of
# references/templates/grammar.md or memo.md lands in every board these write.
# workflows.py only existence-checks references/templates/workflow.md and
# atomic.md and takes the body on stdin, so those two are documentation only.
set -e
R=$(mktemp -d)/repo
mkdir -p "$R/pearde/prds" "$R/pearde/memos" "$R/pearde/workflows"
printf -- '---\nname: probe\n---\n' > "$R/pearde/settings.md"

python3 resources/grammar.py init "$R/pearde" >/dev/null
python3 resources/grammar.py check "$R/pearde"
grep -q '^## This repo' "$R/pearde/grammar.md"
echo "grammar: round-trip ok"

python3 resources/memos.py add "a probe subject" "$R/pearde" >/dev/null
python3 resources/memos.py check "$R/pearde"
echo "memo: round-trip ok"

printf '# a-probe-step — the unit in a phrase\n\n## Do\n\n1. Run the probe.\n\n## Done when\n\n- The probe exits 0.\n\n## Fails when\n\n| seen | means | do |\n|------|-------|----|\n' \
  | python3 resources/workflows.py add a-probe-step atomic "a probe step" "$R/pearde" >/dev/null
printf '# a-probe-job — the job in a phrase\n\n## Use when\n\n- A probe job.\n- Not a real job; use `probe-then-spec`.\n\n## Steps\n\n| # | atomic | why | on failure |\n|---|--------|-----|------------|\n| 1 | `a-probe-step` | proves the copy | `stop` |\n' \
  | python3 resources/workflows.py add a-probe-job workflow "a probe job" "$R/pearde" >/dev/null
python3 resources/workflows.py check "$R/pearde"
echo "workflow: existence check ok"

rm -rf "$(dirname "$R")"
