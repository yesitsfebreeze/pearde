---
complexity: small
footprint:
  - .cartridge/memos/system/vision.md
---

# spec01 — the vision memo's "Where the composition actually stands" section states today's measurements

## Acceptance

- [ ] The section `## Where the composition actually stands` in `system/vision.md` opens with a `Measured ...` line dated on or after 2026-09-17 (the day it is written) and names `just audit`, `just isolation` and the root profile `` `.cartridge/init.lua` ``.
- [ ] It has at least five bullets, each re-measured that day: root profile entries, `just audit` result and soft findings, README/help presence per `*.ctg`, size (memory.ctg source lines vs median, prd.ctg tracked files), record hygiene (foreign routines deleted, link test in `just test layout`), and the isolation gate.
- [ ] It no longer claims `live-record`/`live-mcp` profile entries, cartridges without a help page or README, the foreign routines `quality.md`/`hygiene.md`, "17 cartridges", "0 of 17", or that the boundary rule holds.
- [ ] While `routine/check-cartridge-isolation.md` still reads `cartridge.ctg/.cartridge/init.lua`, the section says so and says the key check is inert (it reads `provide`, which no manifest carries). If that PRD has already landed, the bullet is dropped and the section says what `just isolation` then measures.
- [ ] Nothing outside that section changes; the frontmatter (description is 194 chars, under the 200 limit) stays byte-identical.
- [ ] The write goes through the memo tool and returns `"saved":true`.

## How to write it

From the live root `/Users/feb/dev/cartridge` (never with the lane as working directory; the CLI then treats the lane as its own project):

1. `env -u CARTRIDGE_YOLO cartridge run memo '{"op":"read","cwd":"<abs lane path>","path":"system/vision.md"}'` and keep `.text` (the whole file, frontmatter included) and `.revision` (sha256 of the file).
2. Re-measure (`just audit`, `just isolation`, `.cartridge/init.lua` entries, `test -f` of `README.md` and `.cartridge/help.md` per `*.ctg`, `git -C prd.ctg ls-files | wc -l`). Replace only the lines from `## Where the composition actually stands` up to (not including) `## Where this is going` with the drafted text in analyst-1.md, numbers updated to the day.
3. `cartridge run memo '{"op":"write","cwd":"<abs lane path>","path":"system/vision.md","body":<full new text>,"expected_revision":"<revision>"}'`. `body` is the whole file, not just the markdown body. Build the JSON with `jq -n --rawfile` so quoting survives.

## Verify

```sh
f=.cartridge/memos/system/vision.md
r=.cartridge/memos/routine/check-cartridge-isolation.md
test -f "$f"
test -f "$r"
s=$(sed -n '/^## Where the composition actually stands$/,/^## Where this is going$/p' "$f")
n=$(printf '%s\n' "$s" | grep -c '^- ' || true)
if [ "$n" -lt 5 ]; then echo "section missing or thin: $n bullets"; exit 1; fi
for t in 'just audit' 'just isolation' '`.cartridge/init.lua`'; do
  if printf '%s\n' "$s" | grep -qF "$t"; then :; else echo "section does not name a measurement command or the root profile"; exit 1; fi
done
d=$(printf '%s\n' "$s" | grep -E '^Measured ' | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' | head -1 || true)
if [ -z "$d" ]; then echo "no dated Measured line"; exit 1; fi
if [ "$d" \< "2026-09-17" ]; then echo "measurement date $d predates the sibling children"; exit 1; fi
if printf '%s\n' "$s" | grep -nE 'live-record|live-mcp|quality\.md|hygiene\.md|ship no|0 of 17|for 17 cartridges|rule holds'; then echo "section repeats a claim that is no longer true"; exit 1; fi
if grep -qF 'cartridge.ctg/.cartridge/init.lua' "$r"; then
  if printf '%s\n' "$s" | grep -qF 'cartridge.ctg/.cartridge/init.lua'; then :; else echo "the isolation gate still reads the host profile and the section no longer says so"; exit 1; fi
fi
echo vision-section-ok
```
