---
complexity: 1
footprint:
  - README.md
---

# spec01 — the README exists, is substantial, and agrees with the manifest

## Base and dependencies

The README was written and committed outside the engine by session
`cartridge-ae`, whose user asked it to make `just audit` pass. This spec does
not propose writing it; it makes the three Acceptance clauses reproducible, so
the record rests on a rerunnable check rather than on a report.

The blocks are repository-local on purpose. `just audit` runs from the
superproject and is not reachable from this cartridge's own repository, so the
blocks assert the same two properties the audit's hard check asserts — a README
of at least ten non-blank lines — plus the agreement with `cartridge.json` that
the audit does not check at all.

## Acceptance

- [x] `README.md` exists with at least ten non-blank lines, which is what the
      audit's hard check requires.
- [x] Every event the README names under **Defines** is declared in
      `cartridge.json`, every declared event appears there, and every event
      under **Listens to** is one this cartridge really listens to.

## Verify

```sh
test -f README.md
lines=$(grep -c . README.md)
test "$lines" -ge 10 || { echo "README.md has $lines non-blank lines, the audit requires 10"; exit 1; }
echo "README.md: $lines non-blank lines"
```

```sh
python3 - <<'PY'
import json, pathlib, re, sys

readme = pathlib.Path("README.md").read_text()
manifest = json.loads(pathlib.Path("cartridge.json").read_text())
declared = set(manifest.get("events", {}).keys())
listens = set(manifest.get("listens", manifest.get("listen", [])) or [])

def named(label):
    match = re.search(r"\*\*" + label + r"\*\*\s*—\s*(.+)", readme)
    if not match:
        sys.exit(f"README.md has no **{label}** line")
    return set(re.findall(r"`([^`]+)`", match.group(1)))

defines, hears = named("Defines"), named("Listens to")
if defines != declared:
    sys.exit(f"README Defines {sorted(defines)} but cartridge.json declares {sorted(declared)}")
if not hears <= listens:
    sys.exit(f"README Listens to {sorted(hears)} is not within {sorted(listens)}")
print(f"README agrees with the manifest: defines {sorted(defines)}, listens to {sorted(hears)}")
PY
```
