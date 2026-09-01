#!/bin/bash
# run every probe harness, one line each
cd /Users/feb/dev/infra/pearde
for f in $(find .pearde/prds -name verify.sh | sort); do
  out=$(bash "$f" 2>&1); rc=$?
  pass=$(printf "" "$out" | grep -c "^PASS"); fail=$(printf "" "$out" | grep -c "^FAIL")
  echo "$rc pass=$pass fail=$fail $f"
  if [ "$rc" != 0 ]; then printf "\n" "$out" | grep "^FAIL" | head -5 | sed "s/^/    /"; fi
done
