#!/bin/bash
# probe harness — install-fetches-nothing
#
# The installer is links and nothing else: `install.sh` reaches no network, on
# any mode, and `--remove` deletes no plugin bundle. The fetch it used to do
# lives behind `pearde vault`, the one verb that says "I want this vault", and
# it fetches only what the preset does not already hold at the pinned version.
#
# Seven checks, and the denominator is pinned below — a harness that only
# counts what it ran cannot tell a skipped check from a check that vanished.
# Checks 3 and 4 need the network; with none they count as skipped, never as
# passed.
#
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green run
# would prove a tree holding none of the work. BOARD is the board this harness
# sits under, found by walking; ROOT is PEARDE_ROOT (or PEARDE_TREE) when the
# runner set one, that board's repo otherwise.
#
# Nothing here writes into the tree under test. Checks 3-5 run the fetch
# against a COPY of the preset — the real one is a shared-store symlink per
# lane, and writing a real file over it silently detaches the lane from the
# store until `pearde share apply` runs again.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd -P)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] \
                        && [ "$(basename "$BOARD")" != pearde ]; do
  BOARD="$(dirname "$BOARD")"
done
ROOT="${PEARDE_ROOT:-${PEARDE_TREE:-$(dirname "$BOARD")}}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

pass=0; fail=0; skip=0
ok()   { printf 'PASS  %s\n' "$1"; pass=$((pass+1)); }
no()   { printf 'FAIL  %s\n' "$1"; fail=$((fail+1)); }
skipt(){ printf 'SKIP  %s\n' "$1"; skip=$((skip+1)); }

INSTALL="$ROOT/resources/install.sh"

# 1 — the installer names no network call, in any mode
if grep -qE 'curl|wget|https?://' "$INSTALL"; then
  no "1 install.sh names a fetch: $(grep -nE 'curl|wget|https?://' "$INSTALL" | head -1)"
else
  ok "1 install.sh names no curl, no wget, no URL"
fi

# 2 — --remove deletes no bundle
if grep -qE 'main\.js|manifest\.json|styles\.css|bundle' "$INSTALL"; then
  no "2 install.sh still names a bundle file: $(grep -nE 'main\.js|manifest\.json|styles\.css|bundle' "$INSTALL" | head -1)"
else
  ok "2 install.sh names no bundle file — --remove cannot delete one"
fi

# 3 — the install itself, with every route to the network cut
SK="$TMP/skills"; mkdir -p "$SK"
out="$TMP/apply.txt"
if env http_proxy=http://127.0.0.1:1 https_proxy=http://127.0.0.1:1 \
       ALL_PROXY=http://127.0.0.1:1 \
       bash "$INSTALL" --apply "$SK" >"$out" 2>&1; then
  n=$(find "$SK" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')
  if grep -qi 'could not fetch\|network' "$out"; then
    no "3 the offline install still reports a fetch"
  else
    ok "3 install --apply exit 0 behind a dead proxy · $n skill folder(s), no fetch line"
  fi
else
  no "3 install --apply failed with the network cut (exit $?)"; sed -n '1,20p' "$out"
fi

# The fetch, against a copy of the preset. `initlib` is loaded by path and its
# OBSIDIAN_PRESET repointed, so the real preset — a shared-store symlink in a
# lane — is never written through.
loadpy() {
  cat <<PY
import importlib.util, os, sys
root = "$ROOT"
sys.path.insert(0, os.path.join(root, "resources", "board"))
_s = importlib.util.spec_from_file_location(
    "initlib", os.path.join(root, "resources", "board", "init.py"))
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)
m.OBSIDIAN_PRESET = "$TMP/preset"
PY
}
mkdir -p "$TMP/preset/plugins"

if python3 -c "import urllib.request;urllib.request.urlopen('https://github.com',timeout=8)" 2>/dev/null; then
  # 4 — a bundle the preset does not hold is fetched at the pin
  r1="$( { loadpy; cat <<'PY'
print("run", m.ensure_bundles(("dataview",)))
print("state", m.bundle_state("dataview"))
PY
} | python3 - )"
  if printf '%s' "$r1" | grep -q "state ok"; then
    ok "4 pearde vault's fetch brought dataview in at the pinned version"
  else
    no "4 the fetch did not land: $r1"
  fi
  # 5 — a bundle already there at the pin is not fetched again
  r2="$( { loadpy; cat <<'PY'
print(m.ensure_bundles(("dataview",)))
PY
} | python3 - )"
  [ "$r2" = "([], [])" ] && ok "5 a second run fetches nothing (got $r2)" \
                         || no "5 a second run refetched: $r2"
else
  skipt "4 no network — the fetch was not exercised"
  skipt "5 no network — the no-op second run was not exercised"
fi

# 6 — a vault seeded before the bundles arrived gets them, and an installed
#     plugin is left alone
r3="$( { loadpy; cat <<'PY'
import os, shutil, tempfile
d = tempfile.mkdtemp()
dest = os.path.join(d, ".obsidian")
os.makedirs(os.path.join(dest, "plugins", "obsidian-local-rest-api"))
src = os.path.join(m.OBSIDIAN_PRESET, "plugins", "dataview")
os.makedirs(src, exist_ok=True)
open(os.path.join(src, "main.js"), "w").write("//")
first = m.copy_bundles(dest)
kept = os.listdir(os.path.join(dest, "plugins", "obsidian-local-rest-api"))
second = m.copy_bundles(dest)
print("first", first, "kept", kept, "second", second)
shutil.rmtree(d)
PY
} | python3 - )"
if [ "$r3" = "first ['dataview'] kept [] second []" ]; then
  ok "6 copy_bundles fills an empty vault once and leaves an installed plugin alone"
else
  no "6 copy_bundles: $r3"
fi

# 7 — nothing in the tree still says the install fetches the bundles
hits="$(grep -rniE 'install[^\n]{0,40}fetch|fetch[^\n]{0,30}install --apply' \
          "$ROOT/references" "$ROOT/index.md" "$ROOT/README.md" \
          "$ROOT/resources/board/init.py" "$ROOT/resources/board/shared.py" \
          2>/dev/null | grep -vi 'git .*fetch' | head -3)"
[ -z "$hits" ] && ok "7 no file claims the install fetches the plugin bundles" \
               || no "7 a file still says the install fetches: $hits"

echo
[ "$((pass + fail + skip))" = 7 ] || { echo "harness ran $((pass+fail+skip)) of 7 checks — a check went missing"; fail=$((fail+1)); }
echo "$pass passed, $fail failed${skip:+, $skip skipped}"
[ "$fail" = 0 ]
