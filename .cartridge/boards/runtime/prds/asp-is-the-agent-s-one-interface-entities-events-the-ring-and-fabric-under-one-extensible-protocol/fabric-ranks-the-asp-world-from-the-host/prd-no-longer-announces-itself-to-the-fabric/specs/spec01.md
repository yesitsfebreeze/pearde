---
complexity: moderate
footprint:
  - "cartridge.json"
  - "init.lua"
  - "src/service.ts"
  - "README.md"
---

# spec01: prd no longer announces itself to the fabric

Base revision: `90bda87bd59de8627f50a08dffccf638adcf58a2`.

## Change

1. `src/service.ts`: delete the `graph.announce` listener.
2. `cartridge.json`, `init.lua`: drop `graph.announce` from `listen`.
3. `README.md`: drop it from Listens to.

## Acceptance

- [x] No file of prd names `graph.announce`, and `cartridge.json` parses.

## Verify

The change is a deletion, so the check is that the event is named nowhere in
prd's source, manifest, entry or README, and that the manifest still parses.

```sh
if grep -rn "graph.announce" src cartridge.json init.lua README.md; then
	echo "prd still names graph.announce" >&2
	exit 1
fi
bun -e 'JSON.parse(await Bun.file("cartridge.json").text())'
```
