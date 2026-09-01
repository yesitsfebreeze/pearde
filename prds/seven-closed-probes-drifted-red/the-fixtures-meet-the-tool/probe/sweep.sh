#!/bin/bash
# sweep every committed harness sequentially, one line each.
# Sequential on purpose: doctor's unbounded-parallel sweep makes two harnesses
# that both run `collect` fight over the shared /tmp/pearde-index-* prefix.
# Absolute paths only, and no git write anywhere — a relative `cd` in a runner
# is how the previous sweep committed the real repo by accident.
ROOT=/Users/feb/dev/infra/pearde
cd "$ROOT" || exit 2
[ "$PWD" = "$ROOT" ] || { echo "refusing: cwd is $PWD"; exit 2; }
OUT=${1:-/tmp/pearde-sweep-$$}
mkdir -p "$OUT"
red=0; green=0
for f in $(find "$ROOT/.pearde/prds" -name verify.sh | sort); do
  name=${f#$ROOT/.pearde/prds/}; name=${name%/probe/verify.sh}
  log="$OUT/$(echo "$name" | tr / _).log"
  bash "$f" >"$log" 2>&1; rc=$?
  ok=$(grep -ciE '^ *(ok|PASS)' "$log"); bad=$(grep -ciE '^ *FAIL' "$log")
  if [ "$rc" = 0 ]; then green=$((green+1)); else red=$((red+1)); fi
  printf '%s rc=%s ok=%s fail=%s %s\n' \
         "$([ "$rc" = 0 ] && echo GREEN || echo '  RED')" "$rc" "$ok" "$bad" "$name"
  [ "$rc" = 0 ] || grep -iE '^ *FAIL' "$log" | head -4 | sed 's/^/       /'
done
echo
echo "$((green+red)) harnesses · $green green · $red red · logs in $OUT"
[ "$red" = 0 ]
