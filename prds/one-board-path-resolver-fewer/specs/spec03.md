---
complexity: 2
footprint:
  - references/parts/board.md
---

# spec03 — the roster names the walk `statusline.sh` also carries

`references/parts/board.md` ("Where the board is") says the walk is
"written seven times on purpose" and names six Python modules plus
`doctor.sh`'s shell one. `resources/statusline.sh` runs the identical climb
(`board segment` block) and is not in the list — an eighth copy the
reference does not account for. `serve.py` is correctly absent: it calls
`planlib.find_board`, one function, not a copy.

This spec only corrects the roster to match what is on disk today. It does
not touch the numbered four-rule list two paragraphs above ("1. `.pearde/`
... 2. `pearde/` ... 3. ... 4. ...") — collapsing that to three rules is
`resources/board/init.py`'s and the resolvers' job (`legacy-migrations-retire`,
already claimed, already specced), not a documentation edit that can run
ahead of the code it would be describing.

## Acceptance

- [x] "written seven times" becomes "written eight times" (or is rephrased to not carry a stale count at all).
  - `board.md:90`: "The walk is written eight times on purpose".
- [x] `resources/statusline.sh` is named in the roster alongside `doctor.sh`.
  - `board.md:92`: "in `doctor.sh` and `statusline.sh`".
- [x] The four-rule numbered list above it is untouched.
  - `grep -c '^[1-4]\. '` → `4`.

## Verify and Proof

```sh
cd "$REPO"
grep -n 'written .* times' references/parts/board.md
grep -n 'statusline\.sh' references/parts/board.md
# the four-rule list still has exactly four numbered items
grep -c '^[1-4]\. ' references/parts/board.md
```
